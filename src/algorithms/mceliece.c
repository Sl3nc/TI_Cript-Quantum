#include <stdlib.h>
#include <string.h>

#include <openssl/evp.h>
#include <oqs/oqs.h>

#include "mceliece.h"

#define AES_KEY_LEN 32
#define AES_IV_LEN 12
#define AES_TAG_LEN 16

static const uint8_t MESSAGE[] = "Hello World!";
static const size_t MESSAGE_LEN = sizeof(MESSAGE) - 1;

static int derive_key(const uint8_t *shared_secret, size_t shared_secret_len,
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

workload_status run_mceliece(long volume) {
    if (volume <= 0) {
        return WORKLOAD_INVALID_VOLUME;
    }

    OQS_KEM *kem = OQS_KEM_new(OQS_KEM_alg_classic_mceliece_8192128f);
    if (kem == NULL) {
        return WORKLOAD_ERROR;
    }

    uint8_t *public_key = OQS_MEM_malloc(kem->length_public_key);
    uint8_t *secret_key = OQS_MEM_malloc(kem->length_secret_key);
    uint8_t *kem_ciphertext = OQS_MEM_malloc(kem->length_ciphertext);
    uint8_t *shared_secret_e = OQS_MEM_malloc(kem->length_shared_secret);
    uint8_t *shared_secret_d = OQS_MEM_malloc(kem->length_shared_secret);
    EVP_CIPHER_CTX *enc_ctx = EVP_CIPHER_CTX_new();
    EVP_CIPHER_CTX *dec_ctx = EVP_CIPHER_CTX_new();

    static const unsigned char IV[AES_IV_LEN] = {0};
    unsigned char key_e[AES_KEY_LEN];
    unsigned char key_d[AES_KEY_LEN];
    unsigned char aead_ciphertext[sizeof(MESSAGE) - 1];
    unsigned char plaintext[sizeof(MESSAGE) - 1];
    unsigned char tag[AES_TAG_LEN];

    workload_status status = WORKLOAD_OK;

    if (public_key == NULL || secret_key == NULL || kem_ciphertext == NULL ||
        shared_secret_e == NULL || shared_secret_d == NULL || enc_ctx == NULL ||
        dec_ctx == NULL) {
        status = WORKLOAD_ERROR;
    }

    for (long i = 0; status == WORKLOAD_OK && i < volume; i++) {
        if (OQS_KEM_keypair(kem, public_key, secret_key) != OQS_SUCCESS ||
            OQS_KEM_encaps(kem, kem_ciphertext, shared_secret_e, public_key) != OQS_SUCCESS ||
            !derive_key(shared_secret_e, kem->length_shared_secret, key_e) ||
            !aead_encrypt(enc_ctx, key_e, IV, aead_ciphertext, tag) ||
            OQS_KEM_decaps(kem, shared_secret_d, kem_ciphertext, secret_key) != OQS_SUCCESS ||
            !derive_key(shared_secret_d, kem->length_shared_secret, key_d) ||
            !aead_decrypt(dec_ctx, key_d, IV, aead_ciphertext, tag, plaintext)) {
            status = WORKLOAD_ERROR;
        }
    }

    EVP_CIPHER_CTX_free(enc_ctx);
    EVP_CIPHER_CTX_free(dec_ctx);
    OQS_MEM_secure_free(secret_key, kem->length_secret_key);
    OQS_MEM_secure_free(shared_secret_e, kem->length_shared_secret);
    OQS_MEM_secure_free(shared_secret_d, kem->length_shared_secret);
    OQS_MEM_insecure_free(public_key);
    OQS_MEM_insecure_free(kem_ciphertext);
    OQS_KEM_free(kem);

    return status;
}
