#!/bin/sh

/app/benchmark "$@"
status=$?

sleep "${BENCH_LINGER:-7}" 2>/dev/null || true

exit "$status"
