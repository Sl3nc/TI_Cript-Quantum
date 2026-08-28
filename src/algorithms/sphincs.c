#include <stdlib.h>

#include <oqs/oqs.h>

#include "sphincs.h"

static const uint8_t MESSAGE[] = "Hello World";
static const size_t MESSAGE_LEN = sizeof(MESSAGE) - 1;

workload_status run_sphincs(long volume) {
    if (volume <= 0) {
        return WORKLOAD_INVALID_VOLUME;
    }

    OQS_SIG *sig = OQS_SIG_new(OQS_SIG_alg_sphincs_sha2_256s_simple);
    if (sig == NULL) {
        return WORKLOAD_ERROR;
    }

    uint8_t *public_key = OQS_MEM_malloc(sig->length_public_key);
    uint8_t *secret_key = OQS_MEM_malloc(sig->length_secret_key);
    uint8_t *signature = OQS_MEM_malloc(sig->length_signature);

    workload_status status = WORKLOAD_OK;

    if (public_key == NULL || secret_key == NULL || signature == NULL) {
        status = WORKLOAD_ERROR;
    }

    for (long i = 0; status == WORKLOAD_OK && i < volume; i++) {
        size_t signature_len = sig->length_signature;

        if (OQS_SIG_keypair(sig, public_key, secret_key) != OQS_SUCCESS ||
            OQS_SIG_sign(sig, signature, &signature_len, MESSAGE, MESSAGE_LEN, secret_key) !=
                OQS_SUCCESS ||
            OQS_SIG_verify(sig, MESSAGE, MESSAGE_LEN, signature, signature_len, public_key) !=
                OQS_SUCCESS) {
            status = WORKLOAD_ERROR;
        }
    }

    OQS_MEM_secure_free(secret_key, sig->length_secret_key);
    OQS_MEM_insecure_free(public_key);
    OQS_MEM_insecure_free(signature);
    OQS_SIG_free(sig);

    return status;
}
