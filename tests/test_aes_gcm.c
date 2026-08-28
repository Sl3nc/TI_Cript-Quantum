#include <stdlib.h>

#include "../src/algorithms/aes_gcm.h"

int main(void) {
    if (run_aes_gcm(0) != WORKLOAD_INVALID_VOLUME) {
        return EXIT_FAILURE;
    }
    if (run_aes_gcm(-100) != WORKLOAD_INVALID_VOLUME) {
        return EXIT_FAILURE;
    }
    if (run_aes_gcm(1) != WORKLOAD_OK) {
        return EXIT_FAILURE;
    }
    return EXIT_SUCCESS;
}
