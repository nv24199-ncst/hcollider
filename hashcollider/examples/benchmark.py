#!/usr/bin/env python3
"""Benchmarks collision-search throughput across several algorithms."""
from hashcollider.benchmark.runner import run_benchmark
from hashcollider.hashing.algorithms import get_algorithm


def main() -> None:
    print(f"{'Algorithm':<10}{'Hashes/sec':<15}{'Collisions'}")
    for name in ("md5", "sha1", "sha256", "sha3_256", "sha512"):
        algorithm = get_algorithm(name)
        result = run_benchmark(algorithm=algorithm, bits=12, iterations=20, input_length=16)
        print(f"{name:<10}{result.hashes_per_second:<15,.0f}{result.collisions_found}/{result.iterations}")


if __name__ == "__main__":
    main()
