"""Registry of supported hash algorithms.

All algorithms are backed by Python's standard-library ``hashlib`` module,
so no third-party cryptography dependency is required.
"""
from __future__ import annotations

import hashlib
from typing import Callable, Dict

from hashcollider.hashing.base import HashAlgorithm

# name -> (factory, output_bits, security_status)
_REGISTRY_SPEC: Dict[str, tuple] = {
    "md5": (hashlib.md5, 128,
            "BROKEN: practical collisions known since 2004. Do not use for security."),
    "sha1": (hashlib.sha1, 160,
             "WEAK: practical collisions demonstrated (SHAttered, 2017). Avoid for security."),
    "sha224": (hashlib.sha224, 224, "Considered secure; less common than SHA-256."),
    "sha256": (hashlib.sha256, 256, "Considered secure and widely used."),
    "sha384": (hashlib.sha384, 384, "Considered secure."),
    "sha512": (hashlib.sha512, 512, "Considered secure."),
    "sha3_224": (hashlib.sha3_224, 224, "Considered secure (Keccak-based)."),
    "sha3_256": (hashlib.sha3_256, 256, "Considered secure (Keccak-based)."),
    "sha3_384": (hashlib.sha3_384, 384, "Considered secure (Keccak-based)."),
    "sha3_512": (hashlib.sha3_512, 512, "Considered secure (Keccak-based)."),
}


def _build_registry() -> Dict[str, HashAlgorithm]:
    registry = {}
    for name, (factory, bits, status) in _REGISTRY_SPEC.items():
        registry[name] = HashAlgorithm(
            name=name, output_bits=bits, security_status=status, _factory=factory
        )
    return registry


SUPPORTED_ALGORITHMS: Dict[str, HashAlgorithm] = _build_registry()

# Algorithms with known, real-world cryptographic weaknesses. Selecting one
# of these triggers an educational warning in the CLI.
WEAK_ALGORITHMS = {"md5", "sha1"}


def _normalize(name: str) -> str:
    """Strip dashes/underscores/whitespace and lowercase, for loose matching."""
    return name.strip().lower().replace("-", "").replace("_", "")


# Maps a fully-normalized name (no dashes/underscores) to the canonical
# registry key, e.g. "sha3256" -> "sha3_256", "sha256" -> "sha256". This lets
# users type "sha256", "sha-256", "SHA256", "sha3-256", or "sha3_256"
# interchangeably.
_NORMALIZED_TO_CANONICAL = {_normalize(name): name for name in SUPPORTED_ALGORITHMS}


def get_algorithm(name: str) -> HashAlgorithm:
    """Look up a supported algorithm by name, tolerant of case/dash/underscore style.

    Raises:
        ValueError: if the algorithm is not supported.
    """
    canonical = _NORMALIZED_TO_CANONICAL.get(_normalize(name))
    if canonical is None:
        supported = ", ".join(sorted(SUPPORTED_ALGORITHMS))
        raise ValueError(
            f"Unsupported algorithm '{name}'. Supported: {supported}"
        )
    return SUPPORTED_ALGORITHMS[canonical]
