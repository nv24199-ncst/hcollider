#!/usr/bin/env python3
"""Basic example: find and print a collision in a 16-bit truncated SHA-256 space.

Run with:
    python3 examples/basic_collision.py
"""
from hashcollider.collision.engine import CollisionEngine
from hashcollider.generators.sequential import SequentialGenerator
from hashcollider.hashing.algorithms import get_algorithm


def main() -> None:
    algorithm = get_algorithm("sha256")
    generator = SequentialGenerator(length=16)

    engine = CollisionEngine(
        algorithm=algorithm,
        bits=16,
        generator=generator,
        generator_name="sequential",
        input_length=16,
    )
    result = engine.run()

    if not result.found:
        print("No collision found within the default limits.")
        return

    print(f"Found a collision in {result.attempts} attempts "
          f"({result.elapsed_seconds:.4f}s)")
    print(f"Input A: {result.input_a.hex()}")
    print(f"Input B: {result.input_b.hex()}")
    print(f"Full digest A: {result.hash_a}")
    print(f"Full digest B: {result.hash_b}")
    print(f"Shared truncated digest (16 bits): {result.truncated_hash}")
    print("\nNote: the full SHA-256 digests above are different. Only the "
          "16-bit truncated prefix collides.")


if __name__ == "__main__":
    main()
