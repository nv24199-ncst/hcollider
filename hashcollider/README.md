# HashCollider

An educational hash collision research tool for cybersecurity students and
researchers. HashCollider demonstrates real hash collisions using
**truncated/reduced-size hash outputs**, so you can see the birthday
paradox in action on a laptop in milliseconds — without any false claims
about breaking full-size cryptographic hash functions like SHA-256.

> **Important:** HashCollider cannot and does not find collisions in
> full-size SHA-256, SHA-3, etc. That is computationally infeasible. It
> demonstrates collisions in a *configurable truncated output space*
> (e.g. the first 16 bits of a SHA-256 digest) and always clearly reports
> both the truncated match and the (different) full digests.

## Features

- Ten hash algorithms via `hashlib`: MD5, SHA-1, SHA-224/256/384/512,
  SHA3-224/256/384/512
- Configurable truncated-hash mode for realistic, fast collision demos
- Birthday-attack collision search engine with statistics
- Three input generators: random (via `secrets`), sequential, structured
- Safety limits on bit width, attempts, and time, with clean `Ctrl+C` handling
- Collision storage as versioned JSON, with independent re-verification
  (never trusts stored hash values — always recomputes them)
- Markdown report generation with a birthday-bound estimate
- Benchmark command for search throughput
- Built-in educational explanation (`explain collision`)
- Zero third-party runtime dependencies — pure Python 3.10+ standard library

## Requirements

- Kali Linux (or any modern Linux distribution)
- Python 3.10+

## Installation

```bash
git clone <repository-url>
cd hashcollider

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
pip install -e .
```

## Quick Start

```bash
hashcollider algorithms

hashcollider hash --algorithm sha256 --input "hello"

hashcollider collide \
    --algorithm sha256 \
    --bits 16 \
    --generator sequential \
    --length 32 \
    --output collision.json

hashcollider verify collision.json
hashcollider report collision.json
```

## Example Collision

Running the collide command above searches for two different 32-byte
inputs whose SHA-256 digests agree on their **first 16 bits**. Because
the compared space has only `2^16 = 65,536` possible values, the birthday
paradox predicts a match after roughly `sqrt(2^16) ≈ 256` attempts — and
the tool typically finds one in well under a second. It then prints both
full 256-bit digests, which remain different: only the 16-bit prefix
collides.

## Commands

| Command | Purpose |
|---|---|
| `hashcollider algorithms` | List supported hash algorithms and their security status |
| `hashcollider hash` | Hash arbitrary input, optionally showing a truncated digest |
| `hashcollider collide` | Search for a collision in a truncated hash space |
| `hashcollider benchmark` | Measure collision-search throughput |
| `hashcollider verify` | Independently re-verify a saved collision |
| `hashcollider report` | Generate a Markdown report from a saved collision |
| `hashcollider explain collision` | Print an educational explanation of collisions |

See `docs/usage.md` for full flag documentation.

## Architecture

See [`docs/architecture.md`](docs/architecture.md).

## Theory

See [`docs/collision-theory.md`](docs/collision-theory.md) for the math
behind the birthday paradox and why truncation is used.

## Security

See [`SECURITY.md`](SECURITY.md) and [`docs/security.md`](docs/security.md)
for intended use, limitations, and responsible disclosure.

## Testing

```bash
pip install -e ".[dev]"
pytest -v
```

## Limitations

- Full-size cryptographic hash collision search is computationally
  infeasible and is not attempted by this tool.
- The default safety ceiling on `--bits` is 32 (override with
  `--i-understand-the-risk`); a hard ceiling of 48 bits cannot be
  overridden at all.
- No GPU acceleration or multiprocessing in this release (see
  `docs/architecture.md` for planned extension points).
