# Performance

## What's measured

The `benchmark` command and `CollisionResult` statistics report:

- `attempts` — number of candidate inputs hashed
- `elapsed_seconds` — wall-clock time using `time.perf_counter()` (a
  monotonic, high-resolution clock — never plain timestamps, which can
  jump backwards or be adjusted by NTP)
- `hashes_per_second` — `attempts / elapsed_seconds`

## What affects throughput

- **Algorithm choice**: MD5/SHA-1 are generally faster than SHA-2/SHA-3
  variants due to smaller internal state and simpler rounds, though actual
  numbers depend heavily on CPU and Python build (OpenSSL-backed vs. pure
  Python fallback).
- **Input length**: longer inputs take marginally more CPU per hash, but
  the effect is small relative to the fixed overhead of a Python
  function call and dict lookup per attempt.
- **Effective bit length**: does not change hashing cost, but changes how
  many attempts are needed to find a collision (see collision-theory.md).
- **Python overhead**: this is a pure-Python search loop (one dict lookup
  and one hashlib call per attempt); it is not competitive with a
  compiled/optimized brute-forcer, and isn't meant to be — it's an
  educational tool, not a performance benchmark of hashlib itself.

## Memory usage

The engine keeps a Python `dict` mapping `truncated_digest -> input` for
every attempt made so far. Memory usage grows linearly with attempts,
which is why `--max-attempts` and `--max-seconds` exist as safety
guards — an unbounded search could otherwise exhaust memory before it
exhausts CPU, especially at bit widths near the top of the safety range.

## Expected attempts vs. bit width

See the table in `docs/collision-theory.md`. Use it, together with your
own benchmark numbers, to estimate how long a given `--bits` value will
take before running a large search.
