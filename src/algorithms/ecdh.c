#include <stdlib.h>
#include <string.h>

#include <openssl/ec.h>
#include <openssl/evp.h>
#include <openssl/obj_mac.h>

#include "ecdh.h"

/* Tamanho do elemento de campo (ceil(bits / 8)) e, portanto, do segredo
 * compartilhado derivado de cada curva. */
static int ecdh_params(int effort, int *nid, size_t *field_len) {
    switch (effort) {
    case 1:
        *nid = NID_X9_62_prime256v1;
        *field_len = 32; /* P-256 */
        return 1;
    case 3:
        *nid = NID_secp384r1;
        *field_len = 48; /* P-384 */
        return 1;
    case 5:
        *nid = NID_secp521r1;
        *field_len = 66; /* P-521 */
        return 1;
    default:
        return 0;
    }
}

static EVP_PKEY *generate_key(int nid) {
    EVP_PKEY_CTX *ctx = EVP_PKEY_CTX_new_from_name(NULL, "EC", NULL);
    EVP_PKEY *pkey = NULL;

    if (ctx == NULL) {
        return NULL;
    }

    if (EVP_PKEY_keygen_init(ctx) == 1 &&
        EVP_PKEY_CTX_set_ec_paramgen_curve_nid(ctx, nid) == 1) {
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

workload_status run_ecdh(long volume, int effort) {
    if (volume <= 0) {
        return WORKLOAD_INVALID_VOLUME;
    }

    int nid = 0;
    size_t field_len = 0;
    if (!ecdh_params(effort, &nid, &field_len)) {
        return WORKLOAD_INVALID_EFFORT;
    }

    unsigned char *server_shared = OPENSSL_malloc(field_len);
    unsigned char *peer_shared = OPENSSL_malloc(field_len);

    workload_status status = WORKLOAD_OK;

    if (server_shared == NULL || peer_shared == NULL) {
        status = WORKLOAD_ERROR;
    }

    for (long i = 0; status == WORKLOAD_OK && i < volume; i++) {
        size_t server_shared_len = field_len;
        size_t peer_shared_len = field_len;

        EVP_PKEY *server_key = generate_key(nid);
        EVP_PKEY *peer_key = server_key == NULL ? NULL : generate_key(nid);

        if (server_key == NULL || peer_key == NULL ||
            !exchange(server_key, peer_key, server_shared, &server_shared_len) ||
            !exchange(peer_key, server_key, peer_shared, &peer_shared_len) ||
            server_shared_len != field_len || peer_shared_len != field_len ||
            memcmp(server_shared, peer_shared, field_len) != 0) {
            status = WORKLOAD_ERROR;
        }

        EVP_PKEY_free(peer_key);
        EVP_PKEY_free(server_key);
    }

    OPENSSL_clear_free(server_shared, field_len);
    OPENSSL_clear_free(peer_shared, field_len);

    return status;
}
