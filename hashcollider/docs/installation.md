# Installation

## Requirements

- Kali Linux (or any modern Linux distribution)
- Python 3.10 or newer
- No third-party runtime dependencies

## Steps

```bash
git clone <repository-url>
cd hashcollider

python3 -m venv .venv
source .venv/bin/activate

pip install -e .
```

This installs the `hashcollider` command on your `PATH` (inside the
virtual environment) and makes `python3 -m hashcollider` work as well.

## Verify the install

```bash
hashcollider algorithms
```

You should see a table of supported hash algorithms.

## Development install

To also install test dependencies:

```bash
pip install -e ".[dev]"
pytest
```
