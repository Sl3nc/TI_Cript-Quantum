#include <stdlib.h>

#include <openssl/ec.h>
#include <openssl/evp.h>
#include <openssl/obj_mac.h>

#include "ecdsa.h"

#define ECDSA_CURVE_NID NID_secp521r1

static const unsigned char MESSAGE[] = "Hello World";
static const size_t MESSAGE_LEN = sizeof(MESSAGE) - 1;

static EVP_PKEY *generate_key(void) {
    EVP_PKEY_CTX *ctx = EVP_PKEY_CTX_new_from_name(NULL, "EC", NULL);
    EVP_PKEY *pkey = NULL;

    if (ctx == NULL) {
        return NULL;
    }

    if (EVP_PKEY_keygen_init(ctx) == 1 &&
        EVP_PKEY_CTX_set_ec_paramgen_curve_nid(ctx, ECDSA_CURVE_NID) == 1) {
        if (EVP_PKEY_generate(ctx, &pkey) != 1) {
            pkey = NULL;
        }
    }

    EVP_PKEY_CTX_free(ctx);
    return pkey;
}

static int sign_message(EVP_MD_CTX *md_ctx, EVP_PKEY *pkey, unsigned char **signature,
                        size_t *signature_len) {
    EVP_MD_CTX_reset(md_ctx);

    if (EVP_DigestSignInit(md_ctx, NULL, EVP_sha512(), NULL, pkey) != 1) {
        return 0;
    }
    if (EVP_DigestSign(md_ctx, NULL, signature_len, MESSAGE, MESSAGE_LEN) != 1) {
        return 0;
    }

    *signature = OPENSSL_malloc(*signature_len);
    if (*signature == NULL) {
        return 0;
    }

    return EVP_DigestSign(md_ctx, *signature, signature_len, MESSAGE, MESSAGE_LEN) == 1;
}

static int verify_message(EVP_MD_CTX *md_ctx, EVP_PKEY *pkey, const unsigned char *signature,
                          size_t signature_len) {
    EVP_MD_CTX_reset(md_ctx);

    if (EVP_DigestVerifyInit(md_ctx, NULL, EVP_sha512(), NULL, pkey) != 1) {
        return 0;
    }

    return EVP_DigestVerify(md_ctx, signature, signature_len, MESSAGE, MESSAGE_LEN) == 1;
}

workload_status run_ecdsa(long volume) {
    if (volume <= 0) {
        return WORKLOAD_INVALID_VOLUME;
    }

    EVP_MD_CTX *sign_ctx = EVP_MD_CTX_new();
    EVP_MD_CTX *verify_ctx = EVP_MD_CTX_new();

    workload_status status = WORKLOAD_OK;

    if (sign_ctx == NULL || verify_ctx == NULL) {
        status = WORKLOAD_ERROR;
    }

    for (long i = 0; status == WORKLOAD_OK && i < volume; i++) {
        unsigned char *signature = NULL;
        size_t signature_len = 0;

        EVP_PKEY *pkey = generate_key();
        if (pkey == NULL || !sign_message(sign_ctx, pkey, &signature, &signature_len) ||
            !verify_message(verify_ctx, pkey, signature, signature_len)) {
            status = WORKLOAD_ERROR;
        }

        OPENSSL_free(signature);
        EVP_PKEY_free(pkey);
    }

    EVP_MD_CTX_free(sign_ctx);
    EVP_MD_CTX_free(verify_ctx);

    return status;
}
