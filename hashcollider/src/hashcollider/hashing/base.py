"""Abstract interface for hash algorithms used by HashCollider."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HashAlgorithm:
    """A thin, uniform wrapper around a hashlib-backed hash function.

    Attributes:
        name: Canonical lowercase name, e.g. "sha256".
        output_bits: Full digest size in bits.
        security_status: One-line note on modern security suitability.
        _factory: Zero-argument callable returning a fresh hashlib object.
    """

    name: str
    output_bits: int
    security_status: str
    _factory: object  # Callable[[], "hashlib._Hash"], kept loose to avoid typing churn

    def digest(self, data: bytes) -> bytes:
        """Return the raw digest bytes for ``data``."""
        h = self._factory()
        h.update(data)
        return h.digest()

    def hexdigest(self, data: bytes) -> str:
        """Return the hex-encoded digest for ``data``."""
        h = self._factory()
        h.update(data)
        return h.hexdigest()

    def hash(self, data: bytes) -> bytes:
        """Alias for :meth:`digest`, kept for interface readability."""
        return self.digest(data)

    def truncated_hex(self, data: bytes, bits: int) -> str:
        """Return the hex string of the digest truncated to ``bits`` bits.

        The number of hex characters returned is ``ceil(bits / 4)``, and any
        partial nibble at the boundary is masked so the *effective* number
        of compared bits is exactly ``bits`` when used with
        :meth:`truncated_int`.
        """
        full = self.digest(data)
        nibbles = (bits + 3) // 4
        hex_str = full.hex()[:nibbles]
        return hex_str

    def truncated_int(self, data: bytes, bits: int) -> int:
        """Return the digest truncated to exactly ``bits`` bits, as an int.

        This masks off any extra bits beyond ``bits`` so two truncations
        are only equal when they genuinely share the same leading ``bits``
        bits of digest.
        """
        full_int = int.from_bytes(self.digest(data), "big")
        total_bits = self.output_bits
        shift = total_bits - bits
        if shift < 0:
            raise ValueError(
                f"Requested {bits} bits exceeds the {total_bits}-bit output "
                f"of {self.name}"
            )
        return full_int >> shift
