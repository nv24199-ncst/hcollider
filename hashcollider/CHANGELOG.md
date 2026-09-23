# Changelog

## [0.1.0]

Initial release.

### Added

- `HashAlgorithm` abstraction over `hashlib` with digest/hexdigest/truncation.
- Support for MD5, SHA-1, SHA-224/256/384/512, SHA3-224/256/384/512.
- `CollisionEngine` implementing a birthday-style truncated-hash collision search.
- `RandomGenerator`, `SequentialGenerator`, `StructuredGenerator` input generators.
- Safety limits: default/hard bit-size ceilings, `--max-attempts`, `--max-seconds`.
- JSON collision storage with independent re-verification (`verify`).
- Markdown report generation (`report`).
- Benchmark command for collision-search throughput.
- Educational `explain collision` command.
- CLI commands: `algorithms`, `hash`, `collide`, `benchmark`, `verify`, `report`, `explain`.
- Full test suite (pytest) covering hashing, generators, engine, storage, reports, and CLI.
- Documentation set under `docs/`.
