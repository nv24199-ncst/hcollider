import json

import pytest

from hashcollider.collision.engine import CollisionEngine
from hashcollider.generators.sequential import SequentialGenerator
from hashcollider.hashing.algorithms import get_algorithm
from hashcollider.storage.collisions import (
    VerificationError,
    load_collision,
    save_collision,
    verify_collision,
)


def _make_collision_result(bits=8):
    algo = get_algorithm("sha256")
    gen = SequentialGenerator(length=16)
    engine = CollisionEngine(algorithm=algo, bits=bits, generator=gen, max_attempts=200_000, max_seconds=30)
    result = engine.run()
    assert result.found
    return result


def test_save_and_load_round_trip(tmp_path):
    result = _make_collision_result()
    path = tmp_path / "collision.json"
    save_collision(result, path)

    data = load_collision(path)
    assert data["algorithm"] == "sha256"
    assert data["effective_bits"] == 8
    assert data["input_a"] != data["input_b"]


def test_save_rejects_unfound_result(tmp_path):
    algo = get_algorithm("sha256")
    gen = SequentialGenerator(length=16)
    engine = CollisionEngine(algorithm=algo, bits=64, generator=gen, max_attempts=3, max_seconds=5)
    result = engine.run()
    assert not result.found
    with pytest.raises(ValueError):
        save_collision(result, tmp_path / "nope.json")


def test_load_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_collision(tmp_path / "does-not-exist.json")


def test_load_invalid_json_raises(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text("{not valid json", encoding="utf-8")
    with pytest.raises(VerificationError):
        load_collision(path)


def test_load_missing_fields_raises(tmp_path):
    path = tmp_path / "incomplete.json"
    path.write_text(json.dumps({"algorithm": "sha256"}), encoding="utf-8")
    with pytest.raises(VerificationError):
        load_collision(path)


def test_verify_collision_passes_for_real_collision(tmp_path):
    result = _make_collision_result()
    path = tmp_path / "collision.json"
    save_collision(result, path)
    data = load_collision(path)
    passed, message = verify_collision(data)
    assert passed
    assert "PASS" in message


def test_verify_collision_never_trusts_stored_hash(tmp_path):
    result = _make_collision_result()
    path = tmp_path / "collision.json"
    save_collision(result, path)
    data = load_collision(path)
    # Tamper with the stored (but not re-checked) full hash values -- verify
    # should still pass because it recomputes truncated hashes independently
    # rather than trusting these fields.
    data["hash_a"] = "deadbeef"
    data["hash_b"] = "deadbeef"
    passed, _ = verify_collision(data)
    assert passed


def test_verify_collision_fails_for_identical_inputs():
    data = {
        "algorithm": "sha256",
        "effective_bits": 8,
        "input_a": b"same-input".hex(),
        "input_b": b"same-input".hex(),
        "truncated_hash": "00",
    }
    passed, message = verify_collision(data)
    assert not passed
    assert "identical" in message


def test_verify_collision_fails_for_non_matching_truncated_hash():
    data = {
        "algorithm": "sha256",
        "effective_bits": 32,
        "input_a": b"aaaaaaaaaaaaaaaa".hex(),
        "input_b": b"bbbbbbbbbbbbbbbb".hex(),
        "truncated_hash": "ffffffff",
    }
    passed, message = verify_collision(data)
    assert not passed
    assert "FAIL" in message
