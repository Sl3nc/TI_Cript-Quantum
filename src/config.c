#include <string.h>

#include "config.h"

#include "algorithms/dss.h"
#include "algorithms/ecdh.h"
#include "algorithms/ecdsa.h"
#include "algorithms/kem.h"
#include "algorithms/rsa.h"
#include "algorithms/sphincs.h"

const algorithm_entry ALGORITHMS[] = {
    {"KEM", run_kem},
    {"DSS", run_dss},
    {"SPHINCS+", run_sphincs},
    {"ECDSA", run_ecdsa},
    {"RSA", run_rsa},
    {"ECDH", run_ecdh},
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
