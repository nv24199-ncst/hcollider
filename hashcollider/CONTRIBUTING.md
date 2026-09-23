# Contributing to HashCollider

Thanks for your interest in contributing!

## Workflow

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/my-change`.
3. Make your changes, with tests for any new behavior.
4. Run the test suite: `pytest -v`.
5. Commit with a clear message and open a pull request against `main`.

## Code style

- Python 3.10+, type hints on public functions.
- Use `pathlib.Path` for filesystem operations.
- Avoid new third-party dependencies unless there's a strong reason;
  HashCollider currently has zero runtime dependencies.
- No global mutable state.
- Docstrings on public classes/functions.

## Testing

All new code should have corresponding tests under `tests/`. Run:

```bash
pip install -e ".[dev]"
pytest -v
```

## Reporting issues

Use GitHub Issues for bugs and feature requests. For security
vulnerabilities, see `SECURITY.md` instead of opening a public issue.

## Scope

Please keep contributions aligned with the project's educational purpose
(see `docs/security.md`). PRs that add real-world attack tooling, exploit
payloads, or instructions for attacking third-party systems will not be
accepted.
