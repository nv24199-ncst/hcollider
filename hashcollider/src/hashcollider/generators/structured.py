"""Structured (prefix + zero-padded counter) input generator."""
from __future__ import annotations

from typing import Iterator


class StructuredGenerator:
    """Yields ``prefix`` + zero-padded counter inputs, e.g. ``experiment-000001``.

    Distinct from :class:`SequentialGenerator` in that the counter width
    and prefix are fully configurable and no fixed total length/padding is
    enforced -- the input is exactly ``prefix + counter``.
    """

    def __init__(self, prefix: str = "experiment-", counter_start: int = 1, counter_width: int = 6):
        if counter_width <= 0:
            raise ValueError("counter_width must be positive")
        if counter_start < 0:
            raise ValueError("counter_start must be non-negative")
        self.prefix = prefix
        self.counter_start = counter_start
        self.counter_width = counter_width

    def __iter__(self) -> Iterator[bytes]:
        counter = self.counter_start
        while True:
            text = f"{self.prefix}{counter:0{self.counter_width}d}"
            yield text.encode("utf-8")
            counter += 1

    def describe(self) -> str:
        return (
            f"structured(prefix={self.prefix!r}, counter_start={self.counter_start}, "
            f"counter_width={self.counter_width})"
        )
