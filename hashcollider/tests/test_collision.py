import math

import pytest

from hashcollider.collision.birthday import collision_probability, expected_attempts
from hashcollider.collision.brute_force import UnsafeConfigurationError, check_bits_allowed
from hashcollider.collision.engine import CollisionEngine
from hashcollider.generators.sequential import SequentialGenerator
from hashcollider.hashing.algorithms import get_algorithm


def test_expected_attempts_grows_with_bits():
    assert expected_attempts(16) < expected_attempts(24)


def test_expected_attempts_rejects_negative():
    with pytest.raises(ValueError):
        expected_attempts(-1)


def test_collision_probability_bounds():
    p_small = collision_probability(1, 32)
    p_large = collision_probability(1_000_000, 32)
    assert 0.0 <= p_small <= p_large <= 1.0


def test_check_bits_allowed_ok_within_default():
    check_bits_allowed(16, max_bits=32, allow_override=False)  # should not raise


def test_check_bits_allowed_rejects_zero_or_negative():
    with pytest.raises(UnsafeConfigurationError):
        check_bits_allowed(0, max_bits=32, allow_override=False)


def test_check_bits_allowed_requires_override_above_default():
    with pytest.raises(UnsafeConfigurationError):
        check_bits_allowed(40, max_bits=32, allow_override=False)
    check_bits_allowed(40, max_bits=32, allow_override=True)  # should not raise


def test_check_bits_allowed_hard_ceiling_cannot_be_overridden():
    with pytest.raises(UnsafeConfigurationError):
        check_bits_allowed(64, max_bits=32, allow_override=True)


def test_engine_finds_small_collision():
    algo = get_algorithm("sha256")
    gen = SequentialGenerator(length=16)
    engine = CollisionEngine(algorithm=algo, bits=8, generator=gen, max_attempts=200_000, max_seconds=30)
    result = engine.run()
    assert result.found
    assert result.input_a != result.input_b
    assert algo.truncated_hex(result.input_a, 8) == algo.truncated_hex(result.input_b, 8)


def test_engine_distinguishes_collision_from_duplicate_input():
    # Sequential generator never repeats an input, so any match found by the
    # engine must be between two *different* inputs, not the same input seen twice.
    algo = get_algorithm("sha256")
    gen = SequentialGenerator(length=16)
    engine = CollisionEngine(algorithm=algo, bits=10, generator=gen, max_attempts=200_000, max_seconds=30)
    result = engine.run()
    assert result.found
    assert result.input_a != result.input_b


def test_engine_respects_max_attempts():
    algo = get_algorithm("sha256")
    gen = SequentialGenerator(length=16)
    # Effectively impossible to collide in 5 attempts at 64 bits.
    engine = CollisionEngine(algorithm=algo, bits=64, generator=gen, max_attempts=5, max_seconds=30)
    result = engine.run()
    assert result.attempts == 5
    assert not result.found


def test_engine_respects_max_seconds():
    algo = get_algorithm("sha256")
    gen = SequentialGenerator(length=16)
    engine = CollisionEngine(algorithm=algo, bits=64, generator=gen, max_attempts=10**9, max_seconds=0.05)
    result = engine.run()
    assert result.elapsed_seconds < 2.0
    assert not result.found


def test_engine_stop_halts_search():
    algo = get_algorithm("sha256")
    gen = SequentialGenerator(length=16)
    engine = CollisionEngine(algorithm=algo, bits=64, generator=gen, max_attempts=10**9, max_seconds=30)
    engine.stop()
    result = engine.run()
    assert result.attempts == 0
    assert not result.found
