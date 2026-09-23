import hashlib

import pytest

from hashcollider.hashing.algorithms import SUPPORTED_ALGORITHMS, get_algorithm


@pytest.mark.parametrize("name", sorted(SUPPORTED_ALGORITHMS))
def test_hexdigest_matches_hashlib(name):
    algo = get_algorithm(name)
    data = b"hello world"
    expected = hashlib.new(name, data).hexdigest()
    assert algo.hexdigest(data) == expected


@pytest.mark.parametrize("name", sorted(SUPPORTED_ALGORITHMS))
def test_digest_length_matches_output_bits(name):
    algo = get_algorithm(name)
    digest = algo.digest(b"test")
    assert len(digest) * 8 == algo.output_bits


def test_get_algorithm_case_insensitive_and_dash():
    a = get_algorithm("SHA256")
    b = get_algorithm("sha-256")
    assert a.name == b.name == "sha256"


def test_get_algorithm_invalid_raises():
    with pytest.raises(ValueError):
        get_algorithm("not-a-real-algo")


def test_truncated_hex_length():
    algo = get_algorithm("sha256")
    h = algo.truncated_hex(b"abc", 16)
    assert len(h) == 4  # 16 bits = 4 hex chars


def test_truncated_int_masks_correctly():
    algo = get_algorithm("sha256")
    full = int.from_bytes(algo.digest(b"abc"), "big")
    truncated = algo.truncated_int(b"abc", 12)
    assert truncated == full >> (256 - 12)


def test_truncated_int_rejects_too_many_bits():
    algo = get_algorithm("sha256")
    with pytest.raises(ValueError):
        algo.truncated_int(b"abc", 1000)
