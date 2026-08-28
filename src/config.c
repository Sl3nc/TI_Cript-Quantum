#include <string.h>

#include "config.h"

#include "algorithms/aes_gcm.h"
#include "algorithms/dh.h"
#include "algorithms/dsa.h"
#include "algorithms/dss.h"
#include "algorithms/kem.h"
#include "algorithms/rsa.h"

const algorithm_entry ALGORITHMS[] = {
    {"KEM", run_kem},
    {"DSS", run_dss},
    {"AES-GCM", run_aes_gcm},
    {"DSA", run_dsa},
    {"RSA", run_rsa},
    {"Diffie-Hellman", run_diffie_hellman},
};

const size_t ALGORITHMS_COUNT = sizeof(ALGORITHMS) / sizeof(ALGORITHMS[0]);

workload_fn workload_lookup(const char *name) {
    if (name == NULL) {
        return NULL;
    }

    for (size_t i = 0; i < ALGORITHMS_COUNT; i++) {
        if (strcmp(ALGORITHMS[i].name, name) == 0) {
            return ALGORITHMS[i].run;
        }
    }

    return NULL;
}
