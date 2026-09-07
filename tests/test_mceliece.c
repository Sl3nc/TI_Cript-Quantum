#include <stdlib.h>

#include "../src/algorithms/mceliece.h"

int main(void) {
    if (run_mceliece(0) != WORKLOAD_INVALID_VOLUME) {
        return EXIT_FAILURE;
    }
    if (run_mceliece(-100) != WORKLOAD_INVALID_VOLUME) {
        return EXIT_FAILURE;
    }
    if (run_mceliece(1) != WORKLOAD_OK) {
        return EXIT_FAILURE;
    }
    return EXIT_SUCCESS;
}
