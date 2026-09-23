"""JSON storage and independent re-verification of discovered collisions."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Tuple

from hashcollider.collision.engine import CollisionResult
from hashcollider.config import FORMAT_VERSION
from hashcollider.hashing.algorithms import get_algorithm


class VerificationError(ValueError):
    """Raised when a stored collision file is malformed or unverifiable."""


def save_collision(result: CollisionResult, path: Path) -> None:
    """Write a :class:`CollisionResult` to ``path`` as versioned JSON."""
    if not result.found:
        raise ValueError("Cannot save a result where no collision was found")
    path = Path(path)
    path.write_text(json.dumps(result.to_dict(), indent=2), encoding="utf-8")


def load_collision(path: Path) -> dict:
    """Load a collision JSON file into a plain dict.

    Raises:
        FileNotFoundError: if the file does not exist.
        VerificationError: if the file is not valid JSON or is missing
            required fields.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Collision file does not exist: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise VerificationError(f"Collision file is not valid JSON: {exc}") from exc

    required = {
        "algorithm", "effective_bits", "input_a", "input_b", "truncated_hash",
    }
    missing = required - data.keys()
    if missing:
        raise VerificationError(f"Collision file is missing fields: {sorted(missing)}")

    if data.get("format_version") != FORMAT_VERSION:
        # Not fatal -- future versions may add fields -- but worth knowing.
        pass

    return data


def verify_collision(data: dict) -> Tuple[bool, str]:
    """Independently recompute and verify a stored collision.

    NEVER trusts the ``hash_a`` / ``hash_b`` / ``truncated_hash`` values
    stored in the file -- both inputs are re-hashed from scratch.

    Returns:
        (passed, message) where ``passed`` is True only if input_a !=
        input_b AND their truncated hashes match at the stored bit length.
    """
    try:
        algorithm = get_algorithm(data["algorithm"])
        bits = int(data["effective_bits"])
        input_a = bytes.fromhex(data["input_a"])
        input_b = bytes.fromhex(data["input_b"])
    except (KeyError, ValueError) as exc:
        raise VerificationError(f"Malformed collision data: {exc}") from exc

    if input_a == input_b:
        return False, "FAIL: input_a and input_b are identical (not a collision)"

    recomputed_a = algorithm.truncated_hex(input_a, bits)
    recomputed_b = algorithm.truncated_hex(input_b, bits)

    if recomputed_a != recomputed_b:
        return False, (
            "FAIL: recomputed truncated hashes do not match "
            f"({recomputed_a} != {recomputed_b})"
        )

    full_a = algorithm.hexdigest(input_a)
    full_b = algorithm.hexdigest(input_b)
    note = "PASS"
    if full_a == full_b:
        note += " (note: full digests also match -- an extremely rare full collision)"
    else:
        note += " (full digests differ, as expected -- only the truncated space collides)"
    return True, note
