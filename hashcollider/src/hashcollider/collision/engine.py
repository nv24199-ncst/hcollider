"""The core collision-search engine.

Implements a birthday-style search: generate inputs, look up their
truncated digest in a dictionary of previously seen digests, and report
a collision the first time a truncated digest repeats for a genuinely
different input.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Iterable, Iterator, Optional

from hashcollider.hashing.base import HashAlgorithm
from hashcollider.config import DEFAULT_MAX_ATTEMPTS, DEFAULT_MAX_SECONDS, FORMAT_VERSION


class MaxAttemptsReached(RuntimeError):
    """Raised internally when the attempt budget is exhausted with no collision."""


class MaxTimeReached(RuntimeError):
    """Raised internally when the time budget is exhausted with no collision."""


@dataclass
class CollisionResult:
    """Structured result of a completed (or interrupted) collision search."""

    algorithm: str
    effective_bits: int
    generator: str
    input_length: Optional[int]
    input_a: Optional[bytes]
    input_b: Optional[bytes]
    hash_a: Optional[str]
    hash_b: Optional[str]
    truncated_hash: Optional[str]
    attempts: int
    elapsed_seconds: float
    hashes_per_second: float
    timestamp: str
    found: bool
    format_version: int = FORMAT_VERSION

    def to_dict(self) -> dict:
        return {
            "format_version": self.format_version,
            "algorithm": self.algorithm,
            "effective_bits": self.effective_bits,
            "generator": self.generator,
            "input_length": self.input_length,
            "input_a": self.input_a.hex() if self.input_a is not None else None,
            "input_b": self.input_b.hex() if self.input_b is not None else None,
            "hash_a": self.hash_a,
            "hash_b": self.hash_b,
            "truncated_hash": self.truncated_hash,
            "attempts": self.attempts,
            "elapsed_seconds": self.elapsed_seconds,
            "hashes_per_second": self.hashes_per_second,
            "timestamp": self.timestamp,
            "found": self.found,
        }


class CollisionEngine:
    """Searches for a collision in the truncated output space of a hash.

    Example:
        engine = CollisionEngine(algorithm=sha256_algo, bits=16, generator=gen)
        result = engine.run()
    """

    def __init__(
        self,
        algorithm: HashAlgorithm,
        bits: int,
        generator: Iterable[bytes],
        max_attempts: int = DEFAULT_MAX_ATTEMPTS,
        max_seconds: float = DEFAULT_MAX_SECONDS,
        generator_name: str = "unknown",
        input_length: Optional[int] = None,
        on_progress=None,
    ):
        self.algorithm = algorithm
        self.bits = bits
        self._generator_iterable = generator
        self.max_attempts = max_attempts
        self.max_seconds = max_seconds
        self.generator_name = generator_name
        self.input_length = input_length
        self.on_progress = on_progress

        self._stopped = False
        self._seen: Dict[int, bytes] = {}
        self._attempts = 0
        self._start_time: Optional[float] = None

    def stop(self) -> None:
        """Request that :meth:`run` halt cleanly at the next opportunity."""
        self._stopped = True

    def statistics(self) -> dict:
        """Return current progress statistics (safe to call mid-search)."""
        elapsed = (time.perf_counter() - self._start_time) if self._start_time else 0.0
        rate = self._attempts / elapsed if elapsed > 0 else 0.0
        return {
            "attempts": self._attempts,
            "elapsed_seconds": elapsed,
            "hashes_per_second": rate,
        }

    def find_collision(self) -> CollisionResult:
        """Run the search to completion and return the result.

        This is the same as :meth:`run`; both names are provided because
        either reads naturally depending on call site.
        """
        return self.run()

    def run(self) -> CollisionResult:
        self._start_time = time.perf_counter()
        deadline = self._start_time + self.max_seconds
        iterator: Iterator[bytes] = iter(self._generator_iterable)

        found_a: Optional[bytes] = None
        found_b: Optional[bytes] = None
        found = False

        try:
            for candidate in iterator:
                if self._stopped:
                    break

                self._attempts += 1
                truncated = self.algorithm.truncated_int(candidate, self.bits)

                previous = self._seen.get(truncated)
                if previous is not None and previous != candidate:
                    found_a, found_b = previous, candidate
                    found = True
                    break
                self._seen[truncated] = candidate

                if self.on_progress and self._attempts % 10000 == 0:
                    self.on_progress(self.statistics())

                if self._attempts >= self.max_attempts:
                    break
                if time.perf_counter() >= deadline:
                    break
        finally:
            elapsed = time.perf_counter() - self._start_time

        rate = self._attempts / elapsed if elapsed > 0 else 0.0
        timestamp = datetime.now(timezone.utc).isoformat()

        hash_a = self.algorithm.hexdigest(found_a) if found_a is not None else None
        hash_b = self.algorithm.hexdigest(found_b) if found_b is not None else None
        truncated_hash = (
            self.algorithm.truncated_hex(found_a, self.bits) if found_a is not None else None
        )

        return CollisionResult(
            algorithm=self.algorithm.name,
            effective_bits=self.bits,
            generator=self.generator_name,
            input_length=self.input_length,
            input_a=found_a,
            input_b=found_b,
            hash_a=hash_a,
            hash_b=hash_b,
            truncated_hash=truncated_hash,
            attempts=self._attempts,
            elapsed_seconds=elapsed,
            hashes_per_second=rate,
            timestamp=timestamp,
            found=found,
        )
