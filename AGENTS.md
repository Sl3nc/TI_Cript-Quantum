# AGENTS.md

## What this is

A benchmark *runner* for cryptographic algorithms, written in C11: it executes post-quantum algorithms via **liboqs** (ML-KEM-1024, ML-DSA-87, Classic-McEliece-8192128f) alongside classical algorithms via **libcrypto** (OpenSSL 3.x — ECIES P-521, ECDSA P-521, ECDH P-521) as a comparison baseline, and nothing else. It never measures itself; an external collector wraps the process.


## Commands

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build

# Run benchmarks (one workload per invocation)
./build/benchmark --algorithm KEM --volume 1000
./build/benchmark -a ECIES -v 500

# Run tests
ctest --test-dir build --output-on-failure
ctest --test-dir build -R test_kem --output-on-failure
```

Requires OpenSSL >= 3.0 dev headers and an installed liboqs. If liboqs is not available locally, build and run through Docker instead — `docker compose build app` compiles liboqs from source.

## Architecture

**`src/workload.h`** — the shared contract: `workload_status` (`WORKLOAD_OK`,
`WORKLOAD_INVALID_VOLUME`, `WORKLOAD_ERROR`) and `workload_fn`.

**`src/algorithms/<name>.c`** — each module exposes a single
`workload_status run_<name>(long volume)` that returns `WORKLOAD_INVALID_VOLUME` for `volume <= 0`,
allocates algorithm objects and fixed buffers *outside* the loop, runs `volume` full operation
cycles, and checks correctness unconditionally (`assert` is banned — it disappears under `NDEBUG`).
No measurement logic anywhere.

**`src/config.c`** — the `ALGORITHMS` array plus `workload_lookup`; the single extension point.

**`src/index.c`** is the only CLI entrypoint (`getopt_long` with `--algorithm/-a` and
`--volume/-v`), dispatching one workload per run and returning `EXIT_FAILURE` on any failure so an
external collector can detect it by exit code.
