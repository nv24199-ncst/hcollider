"""Birthday-bound math helpers.

These are pure functions with no I/O, kept separate from the search engine
so they can be unit tested and reused (e.g. by the CLI's pre-flight
"estimated attempts" display).
"""
from __future__ import annotations

import math


def expected_attempts(effective_bits: int) -> float:
    """Expected number of draws before a birthday collision, ``sqrt(pi/2 * 2^b)``.

    This refines the common ``sqrt(2^b)`` approximation with the
    birthday-problem constant ``sqrt(pi/2)`` for a slightly more accurate
    expectation. It remains an *expectation*, not a guarantee -- an actual
    run may find a collision sooner or later.
    """
    if effective_bits < 0:
        raise ValueError("effective_bits must be non-negative")
    return math.sqrt(math.pi / 2) * math.sqrt(2 ** effective_bits)


def collision_probability(num_draws: int, effective_bits: int) -> float:
    """Approximate probability of at least one collision after ``num_draws`` draws.

    Uses the standard approximation ``1 - exp(-n^2 / (2 * 2^b))``.
    """
    if num_draws < 0:
        raise ValueError("num_draws must be non-negative")
    if effective_bits < 0:
        raise ValueError("effective_bits must be non-negative")
    space = 2 ** effective_bits
    exponent = -(num_draws ** 2) / (2 * space)
    return 1.0 - math.exp(exponent)
