# CLAUDE.md

## What this is

A benchmark *runner* for cryptographic algorithms: it executes post-quantum algorithms via
**quantCrypt** (MLKEM_1024, MLDSA_87, Krypton) alongside classical algorithms via the
`cryptography` library (RSA, DSA, Diffie-Hellman) as a comparison baseline, and nothing else.

- Read `.specify/memory/constitution.md` before changing anything

## Commands

All commands assume the repo root as the working directory. Source modules use bare imports
(`from config import ...`, `from algorithms.kem import ...`), so `src/` must be on `sys.path`.

```bash
pip install -r requirements.txt

# Run benchmarks (script-directory auto-insertion puts src/ on sys.path[0] for you)
python src/index.py --algorithm KEM --volume 1000
python src/index.py -a RSA -v 500
python src/index.py -a KEM DSS Krypton -v 1000   # several algorithms, same volume, sequentially

# Run tests (src/ layout requires PYTHONPATH; no pytest.ini/pyproject.toml configures this)
PYTHONPATH=src pytest
PYTHONPATH=src pytest tests/unit/test_mlkem_kem.py -v
```

## Architecture

**`src/algorithms/*.py`** — each module exposes a single `run_<name>(volume: int)` that validates
`volume > 0`, runs `volume` full operation cycles, and returns `None`. No measurement logic inside
the loop.

**`src/index.py`** is the only CLI entrypoint (argparse), dispatching to `Single` or
`Serialization` depending on how many `--algorithm` values were passed, and converting any
exception into `SystemExit(1)` so an external collector can detect failure by exit code.
