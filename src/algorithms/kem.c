#include <stdlib.h>
#include <string.h>

#include <oqs/oqs.h>

#include "kem.h"

static const char *kem_algorithm(int effort) {
    switch (effort) {
    case 1:
        return OQS_KEM_alg_ml_kem_512;
    case 3:
        return OQS_KEM_alg_ml_kem_768;
    case 5:
        return OQS_KEM_alg_ml_kem_1024;
    default:
        return NULL;
    }
}

workload_status run_kem(long volume, int effort) {
    if (volume <= 0) {
        return WORKLOAD_INVALID_VOLUME;
    }

    const char *name = kem_algorithm(effort);
    if (name == NULL) {
        return WORKLOAD_INVALID_EFFORT;
    }

    OQS_KEM *kem = OQS_KEM_new(name);
    if (kem == NULL) {
        return WORKLOAD_ERROR;
    }

    uint8_t *public_key = OQS_MEM_malloc(kem->length_public_key);
    uint8_t *secret_key = OQS_MEM_malloc(kem->length_secret_key);
    uint8_t *ciphertext = OQS_MEM_malloc(kem->length_ciphertext);
    uint8_t *shared_secret_e = OQS_MEM_malloc(kem->length_shared_secret);
    uint8_t *shared_secret_d = OQS_MEM_malloc(kem->length_shared_secret);

    workload_status status = WORKLOAD_OK;

    if (public_key == NULL || secret_key == NULL || ciphertext == NULL ||
        shared_secret_e == NULL || shared_secret_d == NULL) {
        status = WORKLOAD_ERROR;
    }

    for (long i = 0; status == WORKLOAD_OK && i < volume; i++) {
        if (OQS_KEM_keypair(kem, public_key, secret_key) != OQS_SUCCESS ||
            OQS_KEM_encaps(kem, ciphertext, shared_secret_e, public_key) != OQS_SUCCESS ||
            OQS_KEM_decaps(kem, shared_secret_d, ciphertext, secret_key) != OQS_SUCCESS ||
            memcmp(shared_secret_e, shared_secret_d, kem->length_shared_secret) != 0) {
            status = WORKLOAD_ERROR;
        }
    }

    OQS_MEM_secure_free(secret_key, kem->length_secret_key);
    OQS_MEM_secure_free(shared_secret_e, kem->length_shared_secret);
    OQS_MEM_secure_free(shared_secret_d, kem->length_shared_secret);
    OQS_MEM_insecure_free(public_key);
    OQS_MEM_insecure_free(ciphertext);
    OQS_KEM_free(kem);

    return status;
}
