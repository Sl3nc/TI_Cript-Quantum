#include <stdlib.h>
#include <string.h>

#include <openssl/ec.h>
#include <openssl/evp.h>
#include <openssl/obj_mac.h>

#include "ecies.h"

/* Maior elemento de campo entre os níveis (P-521), usado apenas para
 * dimensionar os buffers de pilha; o comprimento efetivo vem do nível. */
#define ECIES_MAX_SHARED_SECRET_LEN 66
#define AES_KEY_LEN 32
#define AES_IV_LEN 12
#define AES_TAG_LEN 16

static const unsigned char MESSAGE[] = "Hello World!";
static const size_t MESSAGE_LEN = sizeof(MESSAGE) - 1;

static int ecies_params(int effort, int *nid, size_t *field_len) {
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

static int ecdh_derive(EVP_PKEY *own_key, EVP_PKEY *peer_key, unsigned char *shared_secret,
                       size_t field_len) {
    EVP_PKEY_CTX *ctx = EVP_PKEY_CTX_new_from_pkey(NULL, own_key, NULL);
    size_t shared_secret_len = field_len;
    int ok = 0;

    if (ctx == NULL) {
        return 0;
    }

    ok = EVP_PKEY_derive_init(ctx) == 1 && EVP_PKEY_derive_set_peer(ctx, peer_key) == 1 &&
         EVP_PKEY_derive(ctx, shared_secret, &shared_secret_len) == 1 &&
         shared_secret_len == field_len;

    EVP_PKEY_CTX_free(ctx);
    return ok;
}

static int derive_key(const unsigned char *shared_secret, size_t shared_secret_len,
                      unsigned char *key) {
    unsigned int digest_len = 0;
    return EVP_Digest(shared_secret, shared_secret_len, key, &digest_len, EVP_sha256(), NULL) ==
               1 &&
           digest_len == AES_KEY_LEN;
}

static int aead_encrypt(EVP_CIPHER_CTX *ctx, const unsigned char *key, const unsigned char *iv,
                        unsigned char *ciphertext, unsigned char *tag) {
    int len = 0;

    return EVP_EncryptInit_ex(ctx, EVP_aes_256_gcm(), NULL, NULL, NULL) == 1 &&
           EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_SET_IVLEN, AES_IV_LEN, NULL) == 1 &&
           EVP_EncryptInit_ex(ctx, NULL, NULL, key, iv) == 1 &&
           EVP_EncryptUpdate(ctx, ciphertext, &len, MESSAGE, (int)MESSAGE_LEN) == 1 &&
           EVP_EncryptFinal_ex(ctx, ciphertext + len, &len) == 1 &&
           EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_GET_TAG, AES_TAG_LEN, tag) == 1;
}

static int aead_decrypt(EVP_CIPHER_CTX *ctx, const unsigned char *key, const unsigned char *iv,
                        const unsigned char *ciphertext, unsigned char *tag,
                        unsigned char *plaintext) {
    int len = 0;

    if (EVP_DecryptInit_ex(ctx, EVP_aes_256_gcm(), NULL, NULL, NULL) != 1 ||
        EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_SET_IVLEN, AES_IV_LEN, NULL) != 1 ||
        EVP_DecryptInit_ex(ctx, NULL, NULL, key, iv) != 1 ||
        EVP_DecryptUpdate(ctx, plaintext, &len, ciphertext, (int)MESSAGE_LEN) != 1 ||
        EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_SET_TAG, AES_TAG_LEN, tag) != 1 ||
        EVP_DecryptFinal_ex(ctx, plaintext + len, &len) != 1) {
        return 0;
    }

    return memcmp(plaintext, MESSAGE, MESSAGE_LEN) == 0;
}

workload_status run_ecies(long volume, int effort) {
    if (volume <= 0) {
        return WORKLOAD_INVALID_VOLUME;
    }

    int nid = 0;
    size_t field_len = 0;
    if (!ecies_params(effort, &nid, &field_len)) {
        return WORKLOAD_INVALID_EFFORT;
    }

    EVP_CIPHER_CTX *enc_ctx = EVP_CIPHER_CTX_new();
    EVP_CIPHER_CTX *dec_ctx = EVP_CIPHER_CTX_new();

    static const unsigned char IV[AES_IV_LEN] = {0};
    unsigned char shared_secret_e[ECIES_MAX_SHARED_SECRET_LEN];
    unsigned char shared_secret_d[ECIES_MAX_SHARED_SECRET_LEN];
    unsigned char key_e[AES_KEY_LEN];
    unsigned char key_d[AES_KEY_LEN];
    unsigned char aead_ciphertext[sizeof(MESSAGE) - 1];
    unsigned char plaintext[sizeof(MESSAGE) - 1];
    unsigned char tag[AES_TAG_LEN];

    workload_status status = WORKLOAD_OK;

    if (enc_ctx == NULL || dec_ctx == NULL) {
        status = WORKLOAD_ERROR;
    }

    for (long i = 0; status == WORKLOAD_OK && i < volume; i++) {
        EVP_PKEY *recipient_key = generate_key(nid);
        EVP_PKEY *ephemeral_key = recipient_key == NULL ? NULL : generate_key(nid);

        if (recipient_key == NULL || ephemeral_key == NULL ||
            !ecdh_derive(ephemeral_key, recipient_key, shared_secret_e, field_len) ||
            !derive_key(shared_secret_e, field_len, key_e) ||
            !aead_encrypt(enc_ctx, key_e, IV, aead_ciphertext, tag) ||
            !ecdh_derive(recipient_key, ephemeral_key, shared_secret_d, field_len) ||
            !derive_key(shared_secret_d, field_len, key_d) ||
            !aead_decrypt(dec_ctx, key_d, IV, aead_ciphertext, tag, plaintext)) {
            status = WORKLOAD_ERROR;
        }

        EVP_PKEY_free(ephemeral_key);
        EVP_PKEY_free(recipient_key);
    }

    EVP_CIPHER_CTX_free(enc_ctx);
    EVP_CIPHER_CTX_free(dec_ctx);

    return status;
}
