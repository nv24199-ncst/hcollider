# Supported Algorithms

All algorithms are provided by Python's standard-library `hashlib` module.

| Name       | Digest size (bits) | Recommended for security today? | Notes |
|------------|---------------------|----------------------------------|-------|
| md5        | 128                 | No                                | Practical collisions known since 2004. |
| sha1       | 160                 | No                                | Practical collisions demonstrated (SHAttered, 2017). |
| sha224     | 224                 | Yes                               | Less common than SHA-256. |
| sha256     | 256                 | Yes                               | Widely used (TLS, Bitcoin, Git's newer object hashing, etc.). |
| sha384     | 384                 | Yes                               | Larger SHA-2 variant. |
| sha512     | 512                 | Yes                               | Larger SHA-2 variant. |
| sha3_224   | 224                 | Yes                               | Keccak-based, structurally different from SHA-2. |
| sha3_256   | 256                 | Yes                               | Keccak-based. |
| sha3_384   | 384                 | Yes                               | Keccak-based. |
| sha3_512   | 512                 | Yes                               | Keccak-based. |

Names are matched case-insensitively and tolerate dashes/underscores:
`sha256`, `SHA-256`, `sha3-256`, and `sha3_256` all resolve correctly.

MD5 and SHA-1 trigger an educational warning when selected via the CLI.
HashCollider's collision search never claims to produce a cryptographically
meaningful full-length collision for any algorithm — it only ever
demonstrates collisions in a configurable truncated output space.
