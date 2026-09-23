"""Safety-limit checks for brute-force / birthday collision searches.

This module intentionally contains no search loop of its own -- the loop
lives in :mod:`hashcollider.collision.engine` (a single engine handles
both "brute-force style" and "birthday style" searches, since with a
truncated hash they are the same lookup-table algorithm). This module
holds the guardrails that decide whether a requested search is reasonable
to run at all.
"""
from __future__ import annotations

from hashcollider.config import HARD_MAX_BITS


class UnsafeConfigurationError(ValueError):
    """Raised when a requested search configuration is refused for safety."""


def check_bits_allowed(bits: int, max_bits: int, allow_override: bool) -> None:
    """Reject unreasonable ``--bits`` values unless explicitly overridden.

    Args:
        bits: Requested effective hash size in bits.
        max_bits: The soft ceiling (e.g. config.DEFAULT_MAX_BITS).
        allow_override: Whether the caller passed a flag acknowledging the
            risk of a long-running search.

    Raises:
        UnsafeConfigurationError: if bits exceeds the allowed ceiling.
    """
    if bits <= 0:
        raise UnsafeConfigurationError("Invalid bit length: bits must be positive")
    if bits > HARD_MAX_BITS:
        raise UnsafeConfigurationError(
            f"Refusing to run: {bits} bits exceeds the hard maximum of "
            f"{HARD_MAX_BITS} bits. This would not be a reasonable "
            f"educational demonstration."
        )
    if bits > max_bits and not allow_override:
        raise UnsafeConfigurationError(
            f"Requested effective size of {bits} bits exceeds the default "
            f"safety limit of {max_bits} bits (expected attempts grow as "
            f"~sqrt(2^bits)). Pass --i-understand-the-risk to proceed "
            f"anyway, up to a hard maximum of {HARD_MAX_BITS} bits."
        )
