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

static void print_banner(const char *algorithm, long volume, int effort) {
    for (int i = 0; i < BANNER_WIDTH; i++) {
        putchar('=');
    }
    printf("\nRunning: %s - Effort: %d - Volume: %ld\n", algorithm, effort, volume);
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
    fprintf(stderr, "Usage: %s --algorithm NAME --effort {1|3|5} [--volume N]\n", program);
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

static int parse_effort(const char *text, int *effort) {
    char *end = NULL;

    errno = 0;
    long parsed = strtol(text, &end, 10);

    if (errno != 0 || end == text || *end != '\0') {
        return -1;
    }

    if (parsed != 1 && parsed != 3 && parsed != 5) {
        return -1;
    }

    *effort = (int)parsed;
    return 0;
}

int main(int argc, char *argv[]) {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    static const struct option options[] = {
        {"algorithm", required_argument, NULL, 'a'},
        {"effort", required_argument, NULL, 'e'},
        {"volume", required_argument, NULL, 'v'},
        {NULL, 0, NULL, 0},
    };

    const char *algorithm = DEFAULT_ALGORITHM;
    long volume = DEFAULT_VOLUME;
    int effort = 0;
    int effort_set = 0;
    int opt;

    while ((opt = getopt_long(argc, argv, "a:e:v:", options, NULL)) != -1) {
        switch (opt) {
        case 'a':
            algorithm = optarg;
            break;
        case 'e':
            if (parse_effort(optarg, &effort) != 0) {
                log_failure("effort must be 1, 3 or 5");
                return EXIT_FAILURE;
            }
            effort_set = 1;
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

    if (!effort_set) {
        usage(argv[0]);
        return EXIT_FAILURE;
    }

    print_banner(algorithm, volume, effort);

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

    workload_status status = run(volume, effort);
    if (status != WORKLOAD_OK) {
        const char *reason = "workload execution failed";
        if (status == WORKLOAD_INVALID_VOLUME) {
            reason = "volume must be greater than 0";
        } else if (status == WORKLOAD_INVALID_EFFORT) {
            reason = "effort must be 1, 3 or 5";
        }
        log_failure(reason);
        return EXIT_FAILURE;
    }

    log_stage("COMPLETE");
    return EXIT_SUCCESS;
}
