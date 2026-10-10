#!/bin/sh
set -u

algorithm="KEM"
volume=""
effort=""
expect=""

for arg in "$@"; do
    if [ -n "$expect" ]; then
        case "$expect" in
            a) algorithm="$arg" ;;
            e) effort="$arg" ;;
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
        --effort) expect="e" ;;
        --effort=*) effort="${arg#--effort=}" ;;
        -e) expect="e" ;;
        -e*) effort="${arg#-e}" ;;
        --volume) expect="v" ;;
        --volume=*) volume="${arg#--volume=}" ;;
        -v) expect="v" ;;
        -v*) volume="${arg#-v}" ;;
    esac
done

export BENCH_STEP_ALGORITHM="$algorithm"
export BENCH_EFFORT="$effort"
if [ -n "$volume" ]; then
    export BENCH_VOLUME="$volume"
fi

metrics_file="${BENCH_METRICS_FILE:-/tmp/benchmark_steps.prom}"
export BENCH_METRICS_FILE="$metrics_file"
rm -f "$metrics_file"

/app/benchmark "$@"
status=$?

if [ -n "${PUSHGATEWAY_URL:-}" ] && [ -s "$metrics_file" ]; then
    push_path="/algorithm/${algorithm}"
    if [ -n "$effort" ]; then
        push_path="${push_path}/effort/${effort}"
    fi

    curl -fsS \
        -H 'Content-Type: text/plain; version=0.0.4' \
        --data-binary "@$metrics_file" \
        "${PUSHGATEWAY_URL}${push_path}" || true
fi

sleep "${BENCH_LINGER:-7}" 2>/dev/null || true

exit "$status"
