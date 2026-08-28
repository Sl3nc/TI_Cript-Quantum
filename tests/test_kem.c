#include <stdlib.h>

#include "../src/algorithms/kem.h"

int main(void) {
    if (run_kem(0) != WORKLOAD_INVALID_VOLUME) {
        return EXIT_FAILURE;
    }
    if (run_kem(-100) != WORKLOAD_INVALID_VOLUME) {
        return EXIT_FAILURE;
    }
    if (run_kem(1) != WORKLOAD_OK) {
        return EXIT_FAILURE;
    }
    return EXIT_SUCCESS;
}
