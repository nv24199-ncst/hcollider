"""Deterministic sequential input generator."""
from __future__ import annotations

from typing import Iterator


class SequentialGenerator:
    """Yields deterministic, reproducible inputs like ``collision-test-00000001``.

    Two runs with the same parameters always produce the same sequence of
    inputs, which makes experiments and tests reproducible.
    """

    def __init__(self, length: int = 32, prefix: str = "collision-test-", start: int = 1):
        if length <= 0:
            raise ValueError("Input length must be positive")
        if start < 0:
            raise ValueError("start must be non-negative")
        self.length = length
        self.prefix = prefix
        self.start = start

    def __iter__(self) -> Iterator[bytes]:
        counter = self.start
        while True:
            body = f"{self.prefix}{counter:08d}"
            data = body.encode("utf-8")
            if len(data) < self.length:
                data = data.ljust(self.length, b"\0")
            elif len(data) > self.length:
                # Keep the TAIL, not the head: the counter digits are at the
                # end of `body`, so truncating from the front would risk
                # chopping off the very thing that makes each input unique.
                data = data[-self.length :]
            yield data
            counter += 1

    def describe(self) -> str:
        return f"sequential(prefix={self.prefix!r}, start={self.start}, length={self.length})"
