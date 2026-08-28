#include <stdlib.h>
#include <string.h>

#include <openssl/core_names.h>
#include <openssl/dh.h>
#include <openssl/evp.h>
#include <openssl/kdf.h>

#include "dh.h"

#define DH_P_BITS 1024
#define DH_GENERATOR 2
#define DERIVED_KEY_LEN 32

static const unsigned char INFO[] = "Hello World!";
static const size_t INFO_LEN = sizeof(INFO) - 1;

static EVP_PKEY *generate_parameters(void) {
    EVP_PKEY_CTX *ctx = EVP_PKEY_CTX_new_from_name(NULL, "DH", NULL);
    EVP_PKEY *params = NULL;

    if (ctx == NULL) {
        return NULL;
    }

    unsigned int pbits = DH_P_BITS;
    int generator = DH_GENERATOR;
    OSSL_PARAM settings[] = {
        OSSL_PARAM_construct_uint(OSSL_PKEY_PARAM_FFC_PBITS, &pbits),
        OSSL_PARAM_construct_int(OSSL_PKEY_PARAM_DH_GENERATOR, &generator),
        OSSL_PARAM_construct_end(),
    };

    if (EVP_PKEY_paramgen_init(ctx) == 1 && EVP_PKEY_CTX_set_params(ctx, settings) == 1) {
        if (EVP_PKEY_generate(ctx, &params) != 1) {
            params = NULL;
        }
    }

    EVP_PKEY_CTX_free(ctx);
    return params;
}

static EVP_PKEY *generate_key(EVP_PKEY *params) {
    EVP_PKEY_CTX *ctx = EVP_PKEY_CTX_new_from_pkey(NULL, params, NULL);
    EVP_PKEY *pkey = NULL;

    if (ctx == NULL) {
        return NULL;
    }

    if (EVP_PKEY_keygen_init(ctx) == 1) {
        if (EVP_PKEY_generate(ctx, &pkey) != 1) {
            pkey = NULL;
        }
    }

    EVP_PKEY_CTX_free(ctx);
    return pkey;
}

static int exchange(EVP_PKEY *own_key, EVP_PKEY *peer_key, unsigned char *shared_key,
                    size_t *shared_key_len) {
    EVP_PKEY_CTX *ctx = EVP_PKEY_CTX_new_from_pkey(NULL, own_key, NULL);
    int ok = 0;

    if (ctx == NULL) {
        return 0;
    }

    if (EVP_PKEY_derive_init(ctx) == 1 && EVP_PKEY_CTX_set_dh_pad(ctx, 1) == 1 &&
        EVP_PKEY_derive_set_peer(ctx, peer_key) == 1 &&
        EVP_PKEY_derive(ctx, shared_key, shared_key_len) == 1) {
        ok = 1;
    }

    EVP_PKEY_CTX_free(ctx);
    return ok;
}

static int derive_hkdf(EVP_KDF *kdf, const unsigned char *shared_key, size_t shared_key_len,
                       unsigned char *derived_key) {
    EVP_KDF_CTX *ctx = EVP_KDF_CTX_new(kdf);
    int ok = 0;

    if (ctx == NULL) {
        return 0;
    }

    char digest[] = "SHA256";
    OSSL_PARAM settings[] = {
        OSSL_PARAM_construct_utf8_string(OSSL_KDF_PARAM_DIGEST, digest, 0),
        OSSL_PARAM_construct_octet_string(OSSL_KDF_PARAM_KEY, (void *)shared_key, shared_key_len),
        OSSL_PARAM_construct_octet_string(OSSL_KDF_PARAM_INFO, (void *)INFO, INFO_LEN),
        OSSL_PARAM_construct_end(),
    };

    if (EVP_KDF_derive(ctx, derived_key, DERIVED_KEY_LEN, settings) == 1) {
        ok = 1;
    }

    EVP_KDF_CTX_free(ctx);
    return ok;
}

workload_status run_diffie_hellman(long volume) {
    if (volume <= 0) {
        return WORKLOAD_INVALID_VOLUME;
    }

    EVP_PKEY *params = generate_parameters();
    EVP_KDF *kdf = EVP_KDF_fetch(NULL, "HKDF", NULL);

    const size_t shared_key_capacity = DH_P_BITS / 8;
    unsigned char *server_shared = OPENSSL_malloc(shared_key_capacity);
    unsigned char *peer_shared = OPENSSL_malloc(shared_key_capacity);
    unsigned char server_derived[DERIVED_KEY_LEN];
    unsigned char peer_derived[DERIVED_KEY_LEN];

    workload_status status = WORKLOAD_OK;

    if (params == NULL || kdf == NULL || server_shared == NULL || peer_shared == NULL) {
        status = WORKLOAD_ERROR;
    }

    for (long i = 0; status == WORKLOAD_OK && i < volume; i++) {
        size_t server_shared_len = shared_key_capacity;
        size_t peer_shared_len = shared_key_capacity;

        EVP_PKEY *server_key = generate_key(params);
        EVP_PKEY *peer_key = server_key == NULL ? NULL : generate_key(params);

        if (server_key == NULL || peer_key == NULL ||
            !exchange(server_key, peer_key, server_shared, &server_shared_len) ||
            !derive_hkdf(kdf, server_shared, server_shared_len, server_derived) ||
            !exchange(peer_key, server_key, peer_shared, &peer_shared_len) ||
            !derive_hkdf(kdf, peer_shared, peer_shared_len, peer_derived) ||
            memcmp(server_derived, peer_derived, DERIVED_KEY_LEN) != 0) {
            status = WORKLOAD_ERROR;
        }

        EVP_PKEY_free(peer_key);
        EVP_PKEY_free(server_key);
    }

    OPENSSL_clear_free(server_shared, shared_key_capacity);
    OPENSSL_clear_free(peer_shared, shared_key_capacity);
    EVP_KDF_free(kdf);
    EVP_PKEY_free(params);

    return status;
}
