#!/bin/sh
set -u

algorithm="KEM"
volume=""
expect=""

for arg in "$@"; do
    if [ -n "$expect" ]; then
        case "$expect" in
            a) algorithm="$arg" ;;
            v) volume="$arg" ;;
        esac
        expect=""
        continue
    fi

    case "$arg" in
        --algorithm) expect="a" ;;
        --algorithm=*) algorithm="${arg#--algorithm=}" ;;
        -a) expect="a" ;;
        -a*) algorithm="${arg#-a}" ;;
        --volume) expect="v" ;;
        --volume=*) volume="${arg#--volume=}" ;;
        -v) expect="v" ;;
        -v*) volume="${arg#-v}" ;;
    esac
done

export BENCH_STEP_ALGORITHM="$algorithm"
if [ -n "$volume" ]; then
    export BENCH_VOLUME="$volume"
fi

metrics_file="${BENCH_METRICS_FILE:-/tmp/benchmark_steps.prom}"
export BENCH_METRICS_FILE="$metrics_file"
rm -f "$metrics_file"

/app/benchmark "$@"
status=$?

if [ -n "${PUSHGATEWAY_URL:-}" ] && [ -s "$metrics_file" ]; then
    curl -fsS \
        -H 'Content-Type: text/plain; version=0.0.4' \
        --data-binary "@$metrics_file" \
        "${PUSHGATEWAY_URL}/algorithm/${algorithm}" || true
fi

sleep "${BENCH_LINGER:-7}" 2>/dev/null || true

exit "$status"
