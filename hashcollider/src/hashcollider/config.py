"""Shared configuration constants and safety limits."""
from __future__ import annotations

# Maximum "effective bits" a user may request via --bits without passing
# --i-understand-the-risk. Above this, expected attempts grow large enough
# that a demo would either hang or produce a misleading impression.
DEFAULT_MAX_BITS = 32

# Hard ceiling. Even with an override flag, we refuse to go past this,
# because it stops being an "educational demo" and starts being a
# multi-day brute-force job that provides no additional teaching value.
HARD_MAX_BITS = 48

# Default resource guards for a collision search.
DEFAULT_MAX_ATTEMPTS = 50_000_000
DEFAULT_MAX_SECONDS = 120.0

# Storage format version for collision JSON files.
COLLISION_FORMAT_VERSION = 1

FORMAT_VERSION = COLLISION_FORMAT_VERSION
