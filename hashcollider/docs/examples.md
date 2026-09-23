# Examples

See the `examples/` directory for runnable scripts:

- `examples/basic_collision.py` — find and print a single 16-bit
  truncated SHA-256 collision using the library API directly (no CLI).
- `examples/birthday_attack.py` — compares the theoretical birthday-bound
  expected attempt count against real search results across several
  bit widths.
- `examples/benchmark.py` — benchmarks collision-search throughput across
  several hash algorithms.

Run any of them with:

```bash
python3 examples/basic_collision.py
```

## CLI walkthrough

```bash
hashcollider algorithms
hashcollider hash --algorithm sha256 --input "hello"
hashcollider collide --algorithm sha256 --bits 16 --generator sequential --length 32 --output collision.json
hashcollider verify collision.json
hashcollider report collision.json
pytest
```
