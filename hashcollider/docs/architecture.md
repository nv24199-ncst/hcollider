# Architecture

HashCollider is organized as a layered pipeline:

```
CLI (cli.py)
  |
  v
Collision Engine (collision/engine.py)
  |
  +--> Hash Algorithm (hashing/base.py, hashing/algorithms.py)
  |
  +--> Input Generator (generators/random.py, sequential.py, structured.py)
  |
  v
Storage / Reports (storage/collisions.py, reports/generator.py)
```

## Modules

- **`cli.py`** — argparse-based command-line interface. Translates flags
  into calls against the engine/storage/report modules and formats output.
  Never contains hashing or search logic itself.

- **`hashing/base.py`** — the `HashAlgorithm` dataclass: a uniform wrapper
  around a `hashlib` constructor exposing `digest`, `hexdigest`,
  `truncated_hex`, and `truncated_int`.

- **`hashing/algorithms.py`** — the registry of supported algorithms
  (`SUPPORTED_ALGORITHMS`) and `get_algorithm()` lookup with tolerant name
  matching (`sha256`, `SHA-256`, `sha3-256`, `sha3_256` all resolve).

- **`generators/`** — three interchangeable input generators
  (`RandomGenerator`, `SequentialGenerator`, `StructuredGenerator`), each a
  plain Python iterable yielding `bytes`.

- **`collision/engine.py`** — `CollisionEngine`: the birthday-style search
  loop. Maintains a `dict[truncated_digest -> input]`, and reports a
  collision the first time a truncated digest repeats for a genuinely
  different input. Enforces `max_attempts` / `max_seconds` and supports a
  cooperative `stop()`.

- **`collision/birthday.py`** — pure math helpers (`expected_attempts`,
  `collision_probability`), used for the pre-flight estimate shown before
  a search starts.

- **`collision/brute_force.py`** — safety-limit checks (`check_bits_allowed`)
  that refuse unreasonably large `--bits` values unless explicitly
  overridden, up to a hard ceiling that cannot be overridden at all.

- **`storage/collisions.py`** — versioned JSON save/load, and independent
  re-verification (`verify_collision`) that never trusts stored hash
  values — it always recomputes them from the stored raw inputs.

- **`benchmark/runner.py`** — repeats short collision searches to measure
  realistic engine throughput (hashing + dictionary lookups).

- **`reports/generator.py`** — builds a Markdown report from a loaded
  collision dict, always including the "this is not a break of the full
  algorithm" disclaimer.

## Design principles

- No global mutable state; each `CollisionEngine` instance owns its own
  search state.
- No third-party runtime dependencies — everything is standard library.
- The search loop is intentionally simple (a single dict lookup per
  attempt) so a future multiprocessing implementation could be added
  without restructuring the module boundaries (see "Future Extension
  Architecture" in the project brief).
