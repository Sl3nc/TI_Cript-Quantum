#include <stdlib.h>

#include "../src/algorithms/dh.h"

int main(void) {
    if (run_diffie_hellman(0) != WORKLOAD_INVALID_VOLUME) {
        return EXIT_FAILURE;
    }
    if (run_diffie_hellman(-100) != WORKLOAD_INVALID_VOLUME) {
        return EXIT_FAILURE;
    }
    if (run_diffie_hellman(1) != WORKLOAD_OK) {
        return EXIT_FAILURE;
    }
    return EXIT_SUCCESS;
}
