"""Markdown report generation for a discovered collision."""
from __future__ import annotations

from hashcollider.collision.birthday import expected_attempts


def generate_report(data: dict) -> str:
    """Build a Markdown report string from a loaded collision dict."""
    algorithm = data["algorithm"]
    bits = data["effective_bits"]
    generator = data.get("generator", "unknown")
    input_a = data["input_a"]
    input_b = data["input_b"]
    hash_a = data.get("hash_a", "")
    hash_b = data.get("hash_b", "")
    truncated_hash = data["truncated_hash"]
    attempts = data.get("attempts", "unknown")
    elapsed = data.get("elapsed_seconds", "unknown")
    rate = data.get("hashes_per_second", "unknown")
    expected = expected_attempts(bits)

    return f"""# HashCollider Collision Report

## Experiment Information

- **Algorithm:** {algorithm}
- **Effective hash size searched:** {bits} bits
- **Generator:** {generator}

## Inputs

**Input A (hex):**
```
{input_a}
```

**Input B (hex):**
```
{input_b}
```

## Collision Values

- **Full digest A:** `{hash_a}`
- **Full digest B:** `{hash_b}`
- **Truncated digest ({bits} bits) shared by both inputs:** `{truncated_hash}`

## Performance

- **Attempts:** {attempts}
- **Elapsed time:** {elapsed} seconds
- **Hash rate:** {rate} hashes/sec
- **Expected attempts by birthday bound (sqrt(pi/2 * 2^bits)):** {expected:.1f}

## Why This Collision Occurred

Two different inputs were hashed with {algorithm}, and only the first
{bits} bits of each digest were compared. Because the compared space has
only 2^{bits} possible values, the birthday paradox guarantees that a
match is expected after roughly sqrt(2^{bits}) attempts -- a number that
is small enough to demonstrate directly for reduced bit widths, even
though it is astronomically large for a full-size digest.

## Security Interpretation

**This is not a collision in the full {algorithm} algorithm.** Only the
selected {bits}-bit truncated output space was searched. The full digests
of Input A and Input B remain different (unless explicitly noted above).
Finding two inputs that agree on a small truncated prefix of a hash
function's output says nothing about the collision resistance of the
full-size hash function.

## Limitations

- This report demonstrates a collision only within the configured
  truncated bit width.
- No claim is made, or should be inferred, about breaking {algorithm}
  itself.
- Results are reproducible only when a deterministic generator
  (sequential/structured) with the same parameters is used.
"""
