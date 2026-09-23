#!/usr/bin/env python3
"""Demonstrates the birthday-bound math alongside an actual search.

Compares the theoretical expected number of attempts (sqrt(pi/2 * 2^b))
against what a real run actually took, for a few different bit widths.
"""
from hashcollider.collision.birthday import expected_attempts
from hashcollider.collision.engine import CollisionEngine
from hashcollider.generators.sequential import SequentialGenerator
from hashcollider.hashing.algorithms import get_algorithm


def main() -> None:
    algorithm = get_algorithm("sha256")

    print(f"{'Bits':<6}{'Expected attempts':<20}{'Actual attempts':<18}{'Time (s)'}")
    for bits in (8, 12, 16, 20):
        generator = SequentialGenerator(length=16)
        engine = CollisionEngine(algorithm=algorithm, bits=bits, generator=generator)
        result = engine.run()
        expected = expected_attempts(bits)
        print(f"{bits:<6}{expected:<20.1f}{result.attempts:<18}{result.elapsed_seconds:.4f}")


if __name__ == "__main__":
    main()
