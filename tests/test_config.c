#include <stdlib.h>
#include <string.h>

#include "../src/config.h"

int main(void) {
    static const char *const expected[] = {
        "KEM", "DSS", "SPHINCS+", "ECDSA", "RSA", "ECDH"
    };
    const size_t expected_count = sizeof(expected) / sizeof(expected[0]);

    if (ALGORITHMS_COUNT != expected_count) {
        return EXIT_FAILURE;
    }

    for (size_t i = 0; i < expected_count; i++) {
        if (strcmp(ALGORITHMS[i].name, expected[i]) != 0) {
            return EXIT_FAILURE;
        }
        if (ALGORITHMS[i].run == NULL) {
            return EXIT_FAILURE;
        }
        if (workload_lookup(expected[i]) != ALGORITHMS[i].run) {
            return EXIT_FAILURE;
        }
    }

    if (workload_lookup("Krypton") != NULL) {
        return EXIT_FAILURE;
    }
    if (workload_lookup("") != NULL) {
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}
