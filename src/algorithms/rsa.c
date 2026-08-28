#include <stdlib.h>

#include <openssl/evp.h>
#include <openssl/rsa.h>

#include "rsa.h"

#define RSA_KEY_BITS 15360

static const unsigned char MESSAGE[] = "Hello World!";
static const size_t MESSAGE_LEN = sizeof(MESSAGE) - 1;

static EVP_PKEY *generate_key(void) {
    EVP_PKEY_CTX *ctx = EVP_PKEY_CTX_new_from_name(NULL, "RSA", NULL);
    EVP_PKEY *pkey = NULL;

    if (ctx == NULL) {
        return NULL;
    }

    if (EVP_PKEY_keygen_init(ctx) == 1 &&
        EVP_PKEY_CTX_set_rsa_keygen_bits(ctx, RSA_KEY_BITS) == 1) {
        if (EVP_PKEY_generate(ctx, &pkey) != 1) {
            pkey = NULL;
        }
    }

    EVP_PKEY_CTX_free(ctx);
    return pkey;
}

static int configure_pss(EVP_PKEY_CTX *ctx) {
    return EVP_PKEY_CTX_set_rsa_padding(ctx, RSA_PKCS1_PSS_PADDING) == 1 &&
           EVP_PKEY_CTX_set_rsa_pss_saltlen(ctx, RSA_PSS_SALTLEN_MAX) == 1 &&
           EVP_PKEY_CTX_set_rsa_mgf1_md(ctx, EVP_sha512()) == 1;
}

static int sign_message(EVP_MD_CTX *md_ctx, EVP_PKEY *pkey, unsigned char **signature,
                        size_t *signature_len) {
    EVP_PKEY_CTX *pkey_ctx = NULL;

    EVP_MD_CTX_reset(md_ctx);

    if (EVP_DigestSignInit(md_ctx, &pkey_ctx, EVP_sha512(), NULL, pkey) != 1 ||
        !configure_pss(pkey_ctx)) {
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
    EVP_PKEY_CTX *pkey_ctx = NULL;

    EVP_MD_CTX_reset(md_ctx);

    if (EVP_DigestVerifyInit(md_ctx, &pkey_ctx, EVP_sha512(), NULL, pkey) != 1 ||
        !configure_pss(pkey_ctx)) {
        return 0;
    }

    return EVP_DigestVerify(md_ctx, signature, signature_len, MESSAGE, MESSAGE_LEN) == 1;
}

workload_status run_rsa(long volume) {
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
