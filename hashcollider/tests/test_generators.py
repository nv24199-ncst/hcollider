import pytest

from hashcollider.generators import get_generator
from hashcollider.generators.random import RandomGenerator
from hashcollider.generators.sequential import SequentialGenerator
from hashcollider.generators.structured import StructuredGenerator


def test_sequential_is_deterministic_and_reproducible():
    gen1 = SequentialGenerator(length=16, prefix="x-", start=1)
    gen2 = SequentialGenerator(length=16, prefix="x-", start=1)
    it1, it2 = iter(gen1), iter(gen2)
    first5_a = [next(it1) for _ in range(5)]
    first5_b = [next(it2) for _ in range(5)]
    assert first5_a == first5_b
    assert len(first5_a[0]) == 16


def test_sequential_rejects_bad_length():
    with pytest.raises(ValueError):
        SequentialGenerator(length=0)


def test_structured_generator_format():
    gen = StructuredGenerator(prefix="experiment-", counter_start=1, counter_width=6)
    it = iter(gen)
    first = next(it)
    assert first == b"experiment-000001"
    second = next(it)
    assert second == b"experiment-000002"


def test_structured_rejects_bad_width():
    with pytest.raises(ValueError):
        StructuredGenerator(counter_width=0)


def test_random_generator_produces_distinct_values_and_correct_length():
    gen = RandomGenerator(length=8)
    it = iter(gen)
    values = {next(it) for _ in range(20)}
    assert all(len(v) == 8 for v in values)
    assert len(values) > 1  # exceedingly unlikely to collide in 20 draws of 8 bytes


def test_random_rejects_bad_length():
    with pytest.raises(ValueError):
        RandomGenerator(length=-1)


def test_get_generator_factory():
    gen = get_generator("sequential", length=8)
    assert isinstance(gen, SequentialGenerator)


def test_get_generator_invalid_name():
    with pytest.raises(ValueError):
        get_generator("not-a-generator")
