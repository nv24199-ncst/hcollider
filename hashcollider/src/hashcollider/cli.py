"""HashCollider command-line interface."""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

from hashcollider.benchmark.runner import run_benchmark
from hashcollider.collision.birthday import expected_attempts
from hashcollider.collision.brute_force import UnsafeConfigurationError, check_bits_allowed
from hashcollider.collision.engine import CollisionEngine
from hashcollider.config import DEFAULT_MAX_ATTEMPTS, DEFAULT_MAX_BITS, DEFAULT_MAX_SECONDS
from hashcollider.generators import get_generator
from hashcollider.hashing.algorithms import SUPPORTED_ALGORITHMS, WEAK_ALGORITHMS, get_algorithm
from hashcollider.reports.generator import generate_report
from hashcollider.storage.collisions import (
    VerificationError,
    load_collision,
    save_collision,
    verify_collision,
)


class CLIError(Exception):
    """Raised for expected user-facing CLI errors (no traceback shown)."""


def _weak_algorithm_warning(name: str) -> str:
    return (
        f"WARNING: {name.upper()} has known real-world cryptographic collision "
        "weaknesses and must not be used for security-sensitive purposes "
        "(e.g. password hashing, digital signatures, integrity checks against "
        "an adversary). This tool's search demonstrates collisions only in a "
        "configurable truncated output space, and does NOT generate a "
        "cryptographically meaningful full-length collision for this algorithm."
    )


def cmd_algorithms(args: argparse.Namespace) -> int:
    print(f"{'Algorithm':<12} {'Bits':<6} Security status")
    print("-" * 70)
    for name, algo in sorted(SUPPORTED_ALGORITHMS.items()):
        print(f"{name:<12} {algo.output_bits:<6} {algo.security_status}")
    return 0


def cmd_hash(args: argparse.Namespace) -> int:
    algorithm = get_algorithm(args.algorithm)
    if algorithm.name in WEAK_ALGORITHMS:
        print(_weak_algorithm_warning(algorithm.name), file=sys.stderr)
    data = args.input.encode("utf-8")
    print(f"Algorithm:  {algorithm.name}")
    print(f"Input:      {args.input!r}")
    print(f"Hex digest: {algorithm.hexdigest(data)}")
    if args.bits:
        print(f"Truncated ({args.bits} bits): {algorithm.truncated_hex(data, args.bits)}")
    return 0


def cmd_collide(args: argparse.Namespace) -> int:
    algorithm = get_algorithm(args.algorithm)
    if algorithm.name in WEAK_ALGORITHMS:
        print(_weak_algorithm_warning(algorithm.name), file=sys.stderr)

    try:
        check_bits_allowed(args.bits, DEFAULT_MAX_BITS, args.i_understand_the_risk)
    except UnsafeConfigurationError as exc:
        raise CLIError(str(exc)) from exc

    gen_kwargs = {"length": args.length} if args.generator in ("random", "sequential") else {}
    if args.generator == "structured":
        gen_kwargs = {}
    generator = get_generator(args.generator, **gen_kwargs)

    est = expected_attempts(args.bits)

    print("HashCollider\n")
    print(f"Algorithm       {algorithm.name.upper()}")
    print(f"Effective bits  {args.bits}")
    print(f"Generator       {generator.describe()}")
    if args.length:
        print(f"Input length    {args.length} bytes")
    print(f"Expected attempts (birthday bound, approx): {est:,.0f}")
    print("\nSearching for collision... (Ctrl+C to stop)\n")

    engine = CollisionEngine(
        algorithm=algorithm,
        bits=args.bits,
        generator=generator,
        max_attempts=args.max_attempts,
        max_seconds=args.max_seconds,
        generator_name=args.generator,
        input_length=args.length,
    )

    try:
        result = engine.run()
    except KeyboardInterrupt:
        stats = engine.statistics()
        print("\nSearch interrupted.\n")
        print(f"Attempts:     {stats['attempts']}")
        print(f"Elapsed:      {stats['elapsed_seconds']:.4f} seconds")
        print(f"Hashes/sec:   {stats['hashes_per_second']:.0f}")
        return 130

    print(f"Attempts:       {result.attempts}")
    print(f"Time elapsed:   {result.elapsed_seconds:.4f} seconds")
    print(f"Hashes/sec:     {result.hashes_per_second:.0f}\n")

    if not result.found:
        print("No collision found within the configured limits "
              "(--max-attempts / --max-seconds). Try raising them or "
              "reducing --bits.")
        return 1

    print("Collision found\n")
    print(f"Input A:\n{result.input_a.hex()}\n")
    print(f"Input B:\n{result.input_b.hex()}\n")
    print(f"Full hash A:\n{result.hash_a}\n")
    print(f"Full hash B:\n{result.hash_b}\n")
    print(f"Truncated hash ({args.bits} bits):\n{result.truncated_hash}\n")
    print(f"This is a collision in the {args.bits}-bit truncated output space "
          f"of {algorithm.name.upper()} only. The full {algorithm.name.upper()} "
          "digests above remain different.")

    if args.output:
        save_collision(result, Path(args.output))
        print(f"\nSaved to {args.output}")

    return 0


def cmd_benchmark(args: argparse.Namespace) -> int:
    algorithm = get_algorithm(args.algorithm)
    result = run_benchmark(
        algorithm=algorithm,
        bits=args.bits,
        iterations=args.iterations,
        input_length=args.input_length,
    )
    print("HashCollider Benchmark\n")
    print(f"{'Algorithm':<18}{result.algorithm}")
    print(f"{'Effective bits':<18}{result.bits}")
    print(f"{'Iterations':<18}{result.iterations}")
    print(f"{'Input length':<18}{result.input_length} bytes")
    print(f"{'Elapsed seconds':<18}{result.elapsed_seconds:.4f}")
    print(f"{'Hashes/sec':<18}{result.hashes_per_second:,.0f}")
    print(f"{'Collisions found':<18}{result.collisions_found}/{result.iterations}")
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    try:
        data = load_collision(Path(args.path))
        passed, message = verify_collision(data)
    except (FileNotFoundError, VerificationError) as exc:
        raise CLIError(str(exc)) from exc

    print(f"Collision verification: {'PASS' if passed else 'FAIL'}")
    print(message)
    return 0 if passed else 1


def cmd_report(args: argparse.Namespace) -> int:
    try:
        data = load_collision(Path(args.path))
    except (FileNotFoundError, VerificationError) as exc:
        raise CLIError(str(exc)) from exc

    report_text = generate_report(data)
    out_path = Path(args.output) if args.output else Path("reports") / "collision-report.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report_text, encoding="utf-8")
    print(f"Report written to {out_path}")
    return 0


def cmd_explain(args: argparse.Namespace) -> int:
    if args.topic != "collision":
        raise CLIError(f"Unknown explain topic: {args.topic!r} (only 'collision' is supported)")
    print(EXPLAIN_COLLISION_TEXT)
    return 0


EXPLAIN_COLLISION_TEXT = """\
HashCollider — Understanding Hash Collisions
=============================================

1. What is a cryptographic hash function?
   A function that maps arbitrary-length input to a fixed-length output
   (the "digest"), such that the same input always produces the same
   output, and small input changes produce unpredictable output changes.

2. What is a collision?
   Two DIFFERENT inputs that produce the SAME digest:
       input_A != input_B  AND  hash(input_A) == hash(input_B)

3. Why do collisions matter?
   A practical collision can undermine digital signatures, integrity
   checks, and deduplication systems that assume distinct inputs produce
   distinct hashes.

4. The birthday paradox.
   With a b-bit output, you need far fewer than 2^b random samples before
   two of them are likely to share a value -- about sqrt(2^b), the same
   math behind "how many people need to be in a room before two share a
   birthday."

5. Why ~2^(b/2)?
   sqrt(2^b) = 2^(b/2). This is the expected number of attempts to find
   a collision by brute-force birthday search over a b-bit space.

6. Why reduce the output size to demonstrate this?
   For b=16, 2^(b/2) = 256 attempts -- instant. For SHA-256's full 256
   bits, 2^128 attempts is computationally infeasible with any known
   technology. Truncating lets us show the real algorithm and real math
   at a scale a laptop can finish in milliseconds.

7. Why a truncated collision isn't a full collision.
   Matching the first 16 bits of a 256-bit digest says nothing about the
   remaining 240 bits. The full digests almost certainly still differ.
   HashCollider always reports both the truncated match and the full
   digests so this distinction stays visible.
"""


def _add_common_search_limits(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--max-attempts", type=int, default=DEFAULT_MAX_ATTEMPTS,
                         help="Stop after this many attempts (default: %(default)s)")
    parser.add_argument("--max-seconds", type=float, default=DEFAULT_MAX_SECONDS,
                         help="Stop after this many seconds (default: %(default)s)")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hashcollider",
        description="Educational hash collision research tool.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_algos = sub.add_parser("algorithms", help="List supported hash algorithms")
    p_algos.set_defaults(func=cmd_algorithms)

    p_hash = sub.add_parser("hash", help="Hash arbitrary input")
    p_hash.add_argument("--algorithm", required=True, choices=sorted(SUPPORTED_ALGORITHMS))
    p_hash.add_argument("--input", required=True, help="Input string to hash")
    p_hash.add_argument("--bits", type=int, default=None, help="Also show a truncated digest")
    p_hash.set_defaults(func=cmd_hash)

    p_collide = sub.add_parser("collide", help="Search for a collision")
    p_collide.add_argument("--algorithm", required=True, choices=sorted(SUPPORTED_ALGORITHMS))
    p_collide.add_argument("--bits", type=int, required=True, help="Effective (truncated) hash size in bits")
    p_collide.add_argument("--generator", choices=["random", "sequential", "structured"], default="sequential")
    p_collide.add_argument("--length", type=int, default=32, help="Input length in bytes (random/sequential)")
    p_collide.add_argument("--output", default=None, help="Path to save the collision as JSON")
    p_collide.add_argument("--i-understand-the-risk", action="store_true",
                            help=f"Allow --bits above the default safety ceiling (up to the hard max)")
    _add_common_search_limits(p_collide)
    p_collide.set_defaults(func=cmd_collide)

    p_bench = sub.add_parser("benchmark", help="Benchmark collision-search performance")
    p_bench.add_argument("--algorithm", required=True, choices=sorted(SUPPORTED_ALGORITHMS))
    p_bench.add_argument("--bits", type=int, required=True)
    p_bench.add_argument("--iterations", type=int, default=10)
    p_bench.add_argument("--input-length", type=int, default=16)
    p_bench.set_defaults(func=cmd_benchmark)

    p_verify = sub.add_parser("verify", help="Verify a saved collision file")
    p_verify.add_argument("path", help="Path to a collision JSON file")
    p_verify.set_defaults(func=cmd_verify)

    p_report = sub.add_parser("report", help="Generate a Markdown report from a collision file")
    p_report.add_argument("path", help="Path to a collision JSON file")
    p_report.add_argument("--output", default=None, help="Output Markdown path")
    p_report.set_defaults(func=cmd_report)

    p_explain = sub.add_parser("explain", help="Print an educational explanation")
    p_explain.add_argument("topic", choices=["collision"], nargs="?", default="collision")
    p_explain.set_defaults(func=cmd_explain)

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except CLIError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
