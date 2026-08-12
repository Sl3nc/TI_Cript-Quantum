# CLAUDE.md

## What this is

A benchmarking harness that runs cryptographic algorithms in a loop and records CPU/memory/hardware
metrics, producing Markdown reports (tabulate tables + matplotlib PNGs). It benchmarks post-quantum
algorithms via **quantCrypt** (MLKEM_1024, MLDSA_87, Krypton) alongside classical algorithms via the
`cryptography` library (RSA, DSA, Diffie-Hellman) as a comparison baseline.

- Read `.specify/memory/constitution.md` to implement so(v2.0.0) codifies this: quantCrypt is required for post-quantum algorithms, `cryptography` is required for the classical baseline algorithms, and no other crypto library or hand-rolled crypto logic is allowed anywhere in `src/`.

## Commands

All commands assume the repo root as the working directory. Source modules use bare imports
(`from config import ...`, `from algorithms.kem import ...`), so `src/` must be on `sys.path`.

```bash
pip install -r requirements.txt

# Run a single algorithm benchmark (this is the real, working entrypoint —
# script-directory auto-insertion puts src/ on sys.path[0] for you)
python src/index.py --algorithm KEM --volume 1000
python src/index.py -a RSA -v 500

# Run tests (src/ layout requires PYTHONPATH; no pytest.ini/pyproject.toml configures this)
PYTHONPATH=src pytest
PYTHONPATH=src pytest tests/unit/test_mlkem_kem.py -v
PYTHONPATH=src pytest tests/unit/test_mlkem_kem.py::test_run_mlkem_validates_volume -v
```

`README.md`'s `python -m src.orchestration.run_single ...` examples are stale — that module/function no
longer exists. Use `src/index.py` as shown above.

**Tests are not reliably in sync with the implementation.** Some test files were written against an
earlier, since-refactored module layout (e.g. `tests/integration/test_run_single.py` imports a top-level
`run_single` function that no longer exists — the real API is the `Single` class in
`src/orchestration/single.py`). Before trusting or extending a test file, check it actually imports
things that exist in `src/` today.

## Architecture

**`src/config.py`** is the central registry: `ALGORITHMS` maps short names (`"KEM"`, `"RSA"`, etc.) to
each algorithm's `run_*` function. Adding a new algorithm means adding a module under `src/algorithms/`
exposing `run_<name>(volume: int)` and registering it here — nothing else needs to know about it.

**`src/algorithms/*.py`** — each module exposes a single `run_<name>(volume: int)` function that runs
`volume` iterations of a full operation cycle.

**`src/metrics/profile/manager.py`** (`Profiler` class) is the neutral measurement layer — Constitution
Principle II requires it be applied identically to every algorithm. `Profiler().execution(func, *args,
**kwargs)` wraps a call to any `run_*` function with: cProfile (`profile/cpu.py`), memory_profiler
(`profile/memory.py`), a background psutil sampling thread (`system_sampler.py`), and a one-time
py-cpuinfo/psutil hardware snapshot (`hardware.py`). This is the single point where new metrics
collection should be added so all algorithms stay comparable.

**`src/metrics/aggregator.py`** (`aggregate_series`) rolls up multiple evaluation dicts (e.g. across
volumes in a scalability run) into mean/stdev/peak/success-rate stats.

**`src/orchestration/`** wires workload + measurement + reporting together:
- `single.py` (`Single.run(algorithm, volume)`) — one benchmark run: validates input, calls
  `Profiler().execution(...)`, builds an evaluation dict, and generates a report via `visualize/`.
- `serialization.py` (`Serialization.run(algorithm, volumes)`) — intended for scalability sweeps (one
  algorithm across multiple volumes), aggregating results into a comparative report. Note: `src/index.py`
  currently invokes this with a *list of algorithm names* and a *single volume* rather than one algorithm
  and a list of volumes — the CLI wiring and this class's actual contract disagree; check both ends
  before relying on the multi-`--algorithm` CLI path.

**`src/visualize/`** — `plotting.py` (matplotlib PNGs) and `report_markdown.py` (tabulate-based Markdown, built directly as string lines, not a templating engine).

**`src/index.py`** is the only CLI entrypoint (argparse), dispatching to `Single` or `Serialization`
depending on how many `--algorithm` values were passed.

**Output location**: reports/images are written to `<repo_root>/output/<ALGORITHM>/<timestamp>/`
(`RESULTS_DIR` in `src/config.py`).
