#include <stdlib.h>
#include <string.h>

#include <openssl/ec.h>
#include <openssl/evp.h>
#include <openssl/obj_mac.h>

#include "ecdh.h"

#define ECDH_CURVE_NID NID_secp521r1
#define ECDH_SHARED_SECRET_LEN 66 /* ceil(521 / 8), the P-521 field element size */

static EVP_PKEY *generate_key(void) {
    EVP_PKEY_CTX *ctx = EVP_PKEY_CTX_new_from_name(NULL, "EC", NULL);
    EVP_PKEY *pkey = NULL;

    if (ctx == NULL) {
        return NULL;
    }

    if (EVP_PKEY_keygen_init(ctx) == 1 &&
        EVP_PKEY_CTX_set_ec_paramgen_curve_nid(ctx, ECDH_CURVE_NID) == 1) {
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

    if (EVP_PKEY_derive_init(ctx) == 1 && EVP_PKEY_derive_set_peer(ctx, peer_key) == 1 &&
        EVP_PKEY_derive(ctx, shared_key, shared_key_len) == 1) {
        ok = 1;
    }

    EVP_PKEY_CTX_free(ctx);
    return ok;
}

workload_status run_ecdh(long volume) {
    if (volume <= 0) {
        return WORKLOAD_INVALID_VOLUME;
    }

    unsigned char *server_shared = OPENSSL_malloc(ECDH_SHARED_SECRET_LEN);
    unsigned char *peer_shared = OPENSSL_malloc(ECDH_SHARED_SECRET_LEN);

    workload_status status = WORKLOAD_OK;

    if (server_shared == NULL || peer_shared == NULL) {
        status = WORKLOAD_ERROR;
    }

    for (long i = 0; status == WORKLOAD_OK && i < volume; i++) {
        size_t server_shared_len = ECDH_SHARED_SECRET_LEN;
        size_t peer_shared_len = ECDH_SHARED_SECRET_LEN;

        EVP_PKEY *server_key = generate_key();
        EVP_PKEY *peer_key = server_key == NULL ? NULL : generate_key();

        if (server_key == NULL || peer_key == NULL ||
            !exchange(server_key, peer_key, server_shared, &server_shared_len) ||
            !exchange(peer_key, server_key, peer_shared, &peer_shared_len) ||
            server_shared_len != peer_shared_len ||
            memcmp(server_shared, peer_shared, server_shared_len) != 0) {
            status = WORKLOAD_ERROR;
        }

        EVP_PKEY_free(peer_key);
        EVP_PKEY_free(server_key);
    }

    OPENSSL_clear_free(server_shared, ECDH_SHARED_SECRET_LEN);
    OPENSSL_clear_free(peer_shared, ECDH_SHARED_SECRET_LEN);

    return status;
}
