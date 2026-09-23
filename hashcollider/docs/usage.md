# Usage

## List supported algorithms

```bash
hashcollider algorithms
```

## Hash a string

```bash
hashcollider hash --algorithm sha256 --input "hello"
hashcollider hash --algorithm sha256 --input "hello" --bits 16
```

## Search for a collision

```bash
hashcollider collide \
    --algorithm sha256 \
    --bits 16 \
    --generator sequential \
    --length 32 \
    --output collision.json
```

- `--bits` is the *effective* (truncated) hash size searched, not the
  full digest size. Values above 32 bits require
  `--i-understand-the-risk`; values above 48 bits are refused outright.
- `--generator` is one of `random`, `sequential`, `structured`.
- Press `Ctrl+C` to stop cleanly; partial statistics are printed.

## Verify a saved collision

```bash
hashcollider verify collision.json
```

Always recomputes both digests from the stored raw inputs — it never
trusts the hash values written in the file.

## Generate a report

```bash
hashcollider report collision.json --output reports/collision-report.md
```

## Benchmark

```bash
hashcollider benchmark --algorithm sha256 --bits 16 --iterations 100
```

## Educational explanation

```bash
hashcollider explain collision
```
