# Troubleshooting

## `hashcollider: command not found`

- Make sure you activated the virtual environment: `source .venv/bin/activate`
- Re-run `pip install -e .` inside that environment.
- Alternatively, run `python3 -m hashcollider <command>` directly.

## Python version errors

HashCollider requires Python 3.10+. Check with:

```bash
python3 --version
```

On Kali, install a newer Python via `pyenv` or your distribution's
package manager if the system Python is older.

## Permission errors during install

Avoid `sudo pip install`. Use a virtual environment instead:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Package installation fails

- Confirm you're in the project root (where `pyproject.toml` lives).
- Try upgrading pip first: `pip install --upgrade pip`.

## `pytest` fails or isn't found

Install dev dependencies first:

```bash
pip install -e ".[dev]"
pytest -v
```

## Slow performance / search doesn't finish

- Lower `--bits` — expected attempts grow like `2^(bits/2)`.
- Lower `--max-seconds` / `--max-attempts` to bound the search, or press
  `Ctrl+C` to stop cleanly at any time.
- Remember `--bits` above 32 requires `--i-understand-the-risk`, and above
  48 is refused entirely — this is by design, not a bug.
