#define _POSIX_C_SOURCE 200809L

#include <errno.h>
#include <getopt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "config.h"

#define DEFAULT_ALGORITHM "KEM"
#define DEFAULT_VOLUME 1
#define BANNER_WIDTH 60

static void print_banner(const char *algorithm, long volume) {
    for (int i = 0; i < BANNER_WIDTH; i++) {
        putchar('=');
    }
    printf("\nRunning: %s - Volume: %ld\n", algorithm, volume);
    for (int i = 0; i < BANNER_WIDTH; i++) {
        putchar('=');
    }
    putchar('\n');
}

static void log_stage(const char *stage) {
    time_t now = time(NULL);
    struct tm utc;
    char stamp[9] = "??:??:??";

    if (now != (time_t)-1 && gmtime_r(&now, &utc) != NULL) {
        strftime(stamp, sizeof(stamp), "%H:%M:%S", &utc);
    }

    fprintf(stderr, "[INFO] %s - %s\n", stage, stamp);
}

static void log_failure(const char *reason) {
    fprintf(stderr, "[ERROR] FAILED error=%s\n", reason);
}

static void print_valid_algorithms(FILE *stream) {
    for (size_t i = 0; i < ALGORITHMS_COUNT; i++) {
        fprintf(stream, "%s%s", i == 0 ? "" : ", ", ALGORITHMS[i].name);
    }
}

static void usage(const char *program) {
    fprintf(stderr, "Usage: %s [--algorithm NAME] [--volume N]\n", program);
    fprintf(stderr, "Valid algorithms: ");
    print_valid_algorithms(stderr);
    fputc('\n', stderr);
}

static int parse_volume(const char *text, long *volume) {
    char *end = NULL;

    errno = 0;
    long parsed = strtol(text, &end, 10);

    if (errno != 0 || end == text || *end != '\0') {
        return -1;
    }

    *volume = parsed;
    return 0;
}

int main(int argc, char *argv[]) {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    static const struct option options[] = {
        {"algorithm", required_argument, NULL, 'a'},
        {"volume", required_argument, NULL, 'v'},
        {NULL, 0, NULL, 0},
    };

    const char *algorithm = DEFAULT_ALGORITHM;
    long volume = DEFAULT_VOLUME;
    int opt;

    while ((opt = getopt_long(argc, argv, "a:v:", options, NULL)) != -1) {
        switch (opt) {
        case 'a':
            algorithm = optarg;
            break;
        case 'v':
            if (parse_volume(optarg, &volume) != 0) {
                log_failure("volume must be an integer");
                return EXIT_FAILURE;
            }
            break;
        default:
            usage(argv[0]);
            return EXIT_FAILURE;
        }
    }

    print_banner(algorithm, volume);

    workload_fn run = workload_lookup(algorithm);
    if (run == NULL) {
        fprintf(stderr, "[ERROR] FAILED error=unknown algorithm '%s'. Valid options: ", algorithm);
        print_valid_algorithms(stderr);
        fputc('\n', stderr);
        return EXIT_FAILURE;
    }

    if (volume <= 0) {
        char reason[64];
        snprintf(reason, sizeof(reason), "volume must be greater than 0, got %ld", volume);
        log_failure(reason);
        return EXIT_FAILURE;
    }

    log_stage("START");

    workload_status status = run(volume);
    if (status != WORKLOAD_OK) {
        log_failure(status == WORKLOAD_INVALID_VOLUME ? "volume must be greater than 0"
                                                      : "workload execution failed");
        return EXIT_FAILURE;
    }

    log_stage("COMPLETE");
    return EXIT_SUCCESS;
}
