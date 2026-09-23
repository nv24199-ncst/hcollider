"""Cryptographically strong random input generator."""
from __future__ import annotations

import secrets
from typing import Iterator


class RandomGenerator:
    """Yields cryptographically random byte strings of a fixed length.

    Uses the standard-library ``secrets`` module. Not deterministic and
    not seedable -- use :class:`SequentialGenerator` or
    :class:`StructuredGenerator` when you need reproducibility.
    """

    def __init__(self, length: int = 16):
        if length <= 0:
            raise ValueError("Input length must be positive")
        self.length = length

    def __iter__(self) -> Iterator[bytes]:
        while True:
            yield secrets.token_bytes(self.length)

    def describe(self) -> str:
        return f"random(length={self.length})"
