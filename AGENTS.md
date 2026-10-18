# AGENTS.md

## What this is

A benchmark *runner* for cryptographic algorithms, written in C11: it executes post-quantum algorithms via **liboqs** (ML-KEM, ML-DSA, Classic-McEliece) alongside classical algorithms via **libcrypto** (OpenSSL 3.x — ECIES, ECDSA, ECDH) as a comparison baseline, and nothing else. Every algorithm runs at a selectable NIST security level (`--effort/-e`, `1`/`3`/`5`). It never measures itself; an external collector wraps the process.


## Commands

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build

# Run benchmarks (one workload per invocation; --effort/-e is required, 1/3/5)
./build/benchmark --algorithm KEM --effort 5 --volume 1000
./build/benchmark -a ECIES -e 3 -v 500

# Run tests
ctest --test-dir build --output-on-failure
ctest --test-dir build -R test_kem --output-on-failure
```

Requires OpenSSL >= 3.0 dev headers and an installed liboqs. If liboqs is not available locally, build and run through Docker instead — `docker compose build app` compiles liboqs from source.

**MCELIECE does not work locally.** The locally installed liboqs has Classic-McEliece disabled, so
`test_mceliece` fails locally and `./build/benchmark -a MCELIECE` returns `EXIT_FAILURE`. This is
an environment limitation, not a code defect — run MCELIECE through Docker, where liboqs is built
from source with the algorithm enabled (`docker compose run --rm app -a MCELIECE -e 5 -v 20`; keep the
volume small, keygen costs ~0.2 s per cycle).

## Architecture

**`src/workload.h`** — the shared contract: `workload_status` (`WORKLOAD_OK`,
`WORKLOAD_INVALID_VOLUME`, `WORKLOAD_INVALID_EFFORT`, `WORKLOAD_ERROR`) and `workload_fn`.

**`src/algorithms/<name>.c`** — each module exposes a single
`workload_status run_<name>(long volume, int effort)`. It returns `WORKLOAD_INVALID_VOLUME` for
`volume <= 0` and `WORKLOAD_INVALID_EFFORT` for an effort other than `1`/`3`/`5`, maps the effort to
its parameter set (ML-KEM/ML-DSA/McEliece variant or EC curve + hash), allocates algorithm objects
and fixed buffers *outside* the loop, runs `volume` full operation cycles, and checks correctness
unconditionally (`assert` is banned — it disappears under `NDEBUG`). No measurement logic anywhere.

**`src/config.c`** — the `ALGORITHMS` array plus `workload_lookup`; the single extension point.

**`src/index.c`** is the only CLI entrypoint (`getopt_long` with `--algorithm/-a`, `--effort/-e` and
`--volume/-v`; `--effort` is required and must be `1`, `3` or `5`), dispatching one workload per run
and returning `EXIT_FAILURE` on any failure so an external collector can detect it by exit code.

**`profiling/instrument.c`** — per-step timing for every workload's cycle, compiled only with
`-DBENCH_PROFILE=ON` (the `profiling` Docker stage) and linked via `-Wl,--wrap` on the liboqs
(`OQS_KEM_*`, `OQS_SIG_*`) and OpenSSL EVP symbols the modules call directly. It lives outside
`src/algorithms/`; the default `benchmark` image never contains it, so the "no measurement logic
in the workloads" rule holds.
