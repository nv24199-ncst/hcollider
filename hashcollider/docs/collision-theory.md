# Collision Theory

## Hash functions

A cryptographic hash function `H` maps an arbitrary-length input to a
fixed-length output (the digest). Three properties matter most:

- **Preimage resistance**: given `H(x)`, it should be infeasible to find `x`.
- **Second-preimage resistance**: given `x`, it should be infeasible to
  find a different `y` with `H(x) == H(y)`.
- **Collision resistance**: it should be infeasible to find *any* `x != y`
  with `H(x) == H(y)`.

## Collisions

A collision is a pair `(x, y)` with `x != y` and `H(x) == H(y)`. For an
ideal hash function with a `b`-bit output, finding one requires on the
order of `2^b` attempts by preimage/second-preimage search, but only
about `2^(b/2)` attempts by a *birthday* search — because you're looking
for any two matching outputs among many samples, not a match against one
fixed target.

## The birthday paradox

The classic version: in a room of just 23 people, there's better than a
50% chance two share a birthday, even though there are 365 possible
birthdays. The same math applies to hash outputs: with a `b`-bit digest
(`2^b` possible values), the expected number of random samples before two
share a digest is approximately:

```
sqrt(pi/2 * 2^b) ≈ 1.25 * sqrt(2^b) = 1.25 * 2^(b/2)
```

## Birthday bound and effective hash size

For a full 256-bit hash like SHA-256, `2^128` attempts are required —
computationally infeasible with any known technology. HashCollider instead
lets you configure an **effective hash size** by truncating the digest to
the first `b` bits (`--bits b`). Searching that reduced space is exactly
the same algorithm, just over a space small enough to finish in
milliseconds on a laptop for `b` up to roughly 24–32 bits.

## Truncation is not weakening the algorithm

Truncating SHA-256 to its first 16 bits doesn't change how SHA-256 itself
works — it changes what *you compare*. The full 256-bit digests of two
"colliding" inputs almost always still differ. This distinction is central
to why HashCollider's demonstrations are honest: they show real collision
math on a real algorithm, at a scale that's actually observable, without
implying anything about the security of the full-size hash.

## Computational complexity summary

| Effective bits | Expected attempts (~2^(b/2)) |
|-----------------|-------------------------------|
| 8                | ~16                            |
| 16               | ~256                           |
| 24               | ~4,096                         |
| 32               | ~65,536                        |
| 64               | ~4.3 billion                   |
| 128 (full MD5)   | ~1.8 * 10^19                    |
| 256 (full SHA-256) | ~3.4 * 10^38                  |

The last two rows are why brute-force collision search against a full-size
modern cryptographic hash is infeasible, and why real-world attacks on
weak hashes (like MD5) use specialized mathematical techniques, not
plain birthday search.
