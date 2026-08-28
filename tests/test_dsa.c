#include <stdlib.h>

#include "../src/algorithms/dsa.h"

int main(void) {
    if (run_dsa(0) != WORKLOAD_INVALID_VOLUME) {
        return EXIT_FAILURE;
    }
    if (run_dsa(-100) != WORKLOAD_INVALID_VOLUME) {
        return EXIT_FAILURE;
    }
    if (run_dsa(1) != WORKLOAD_OK) {
        return EXIT_FAILURE;
    }
    return EXIT_SUCCESS;
}
