#include <stdlib.h>

#include "../src/algorithms/ecdh.h"

int main(void) {
    static const int efforts[] = {1, 3, 5};

    if (run_ecdh(0, 5) != WORKLOAD_INVALID_VOLUME) {
        return EXIT_FAILURE;
    }
    if (run_ecdh(-100, 5) != WORKLOAD_INVALID_VOLUME) {
        return EXIT_FAILURE;
    }
    if (run_ecdh(1, 2) != WORKLOAD_INVALID_EFFORT) {
        return EXIT_FAILURE;
    }
    if (run_ecdh(1, 4) != WORKLOAD_INVALID_EFFORT) {
        return EXIT_FAILURE;
    }

    for (size_t i = 0; i < sizeof(efforts) / sizeof(efforts[0]); i++) {
        if (run_ecdh(1, efforts[i]) != WORKLOAD_OK) {
            return EXIT_FAILURE;
        }
    }

    return EXIT_SUCCESS;
}
