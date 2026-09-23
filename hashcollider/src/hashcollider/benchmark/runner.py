"""Benchmarking of raw hashing throughput and collision-search performance."""
from __future__ import annotations

import time
from dataclasses import dataclass

from hashcollider.collision.engine import CollisionEngine
from hashcollider.generators.sequential import SequentialGenerator
from hashcollider.hashing.base import HashAlgorithm


@dataclass
class BenchmarkResult:
    algorithm: str
    bits: int
    iterations: int
    input_length: int
    elapsed_seconds: float
    hashes_per_second: float
    collisions_found: int


def run_benchmark(
    algorithm: HashAlgorithm,
    bits: int,
    iterations: int,
    input_length: int = 16,
) -> BenchmarkResult:
    """Run ``iterations`` independent short collision searches and report throughput.

    This measures realistic engine throughput (hashing + dict lookup),
    not raw hashlib speed alone.
    """
    if iterations <= 0:
        raise ValueError("iterations must be positive")

    total_attempts = 0
    collisions_found = 0
    start = time.perf_counter()

    for _ in range(iterations):
        gen = SequentialGenerator(length=input_length)
        engine = CollisionEngine(
            algorithm=algorithm,
            bits=bits,
            generator=gen,
            generator_name="sequential",
            input_length=input_length,
        )
        result = engine.run()
        total_attempts += result.attempts
        if result.found:
            collisions_found += 1

    elapsed = time.perf_counter() - start
    rate = total_attempts / elapsed if elapsed > 0 else 0.0

    return BenchmarkResult(
        algorithm=algorithm.name,
        bits=bits,
        iterations=iterations,
        input_length=input_length,
        elapsed_seconds=elapsed,
        hashes_per_second=rate,
        collisions_found=collisions_found,
    )
