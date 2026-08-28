#include <string.h>

#include <openssl/evp.h>
#include <openssl/rand.h>

#include "aes_gcm.h"

#define AES_GCM_KEY_LEN 32
#define AES_GCM_IV_LEN 12
#define AES_GCM_TAG_LEN 16

static const unsigned char PLAINTEXT[] = "Hello World";
static const int PLAINTEXT_LEN = (int)(sizeof(PLAINTEXT) - 1);

static int encrypt_cycle(EVP_CIPHER_CTX *ctx, const unsigned char *key, const unsigned char *iv,
                         unsigned char *ciphertext, int *ciphertext_len, unsigned char *tag) {
    int len = 0;
    int final_len = 0;

    if (EVP_EncryptInit_ex2(ctx, EVP_aes_256_gcm(), NULL, NULL, NULL) != 1) {
        return 0;
    }
    if (EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_AEAD_SET_IVLEN, AES_GCM_IV_LEN, NULL) != 1) {
        return 0;
    }
    if (EVP_EncryptInit_ex2(ctx, NULL, key, iv, NULL) != 1) {
        return 0;
    }
    if (EVP_EncryptUpdate(ctx, ciphertext, &len, PLAINTEXT, PLAINTEXT_LEN) != 1) {
        return 0;
    }
    if (EVP_EncryptFinal_ex(ctx, ciphertext + len, &final_len) != 1) {
        return 0;
    }
    if (EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_AEAD_GET_TAG, AES_GCM_TAG_LEN, tag) != 1) {
        return 0;
    }

    *ciphertext_len = len + final_len;
    return 1;
}

static int decrypt_cycle(EVP_CIPHER_CTX *ctx, const unsigned char *key, const unsigned char *iv,
                         const unsigned char *ciphertext, int ciphertext_len, unsigned char *tag,
                         unsigned char *plaintext, int *plaintext_len) {
    int len = 0;
    int final_len = 0;

    if (EVP_DecryptInit_ex2(ctx, EVP_aes_256_gcm(), NULL, NULL, NULL) != 1) {
        return 0;
    }
    if (EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_AEAD_SET_IVLEN, AES_GCM_IV_LEN, NULL) != 1) {
        return 0;
    }
    if (EVP_DecryptInit_ex2(ctx, NULL, key, iv, NULL) != 1) {
        return 0;
    }
    if (EVP_DecryptUpdate(ctx, plaintext, &len, ciphertext, ciphertext_len) != 1) {
        return 0;
    }
    if (EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_AEAD_SET_TAG, AES_GCM_TAG_LEN, tag) != 1) {
        return 0;
    }
    if (EVP_DecryptFinal_ex(ctx, plaintext + len, &final_len) != 1) {
        return 0;
    }

    *plaintext_len = len + final_len;
    return 1;
}

workload_status run_aes_gcm(long volume) {
    if (volume <= 0) {
        return WORKLOAD_INVALID_VOLUME;
    }

    EVP_CIPHER_CTX *encrypt_ctx = EVP_CIPHER_CTX_new();
    EVP_CIPHER_CTX *decrypt_ctx = EVP_CIPHER_CTX_new();

    unsigned char key[AES_GCM_KEY_LEN];
    unsigned char iv[AES_GCM_IV_LEN];
    unsigned char tag[AES_GCM_TAG_LEN];
    unsigned char ciphertext[sizeof(PLAINTEXT) + EVP_MAX_BLOCK_LENGTH];
    unsigned char plaintext_copy[sizeof(PLAINTEXT) + EVP_MAX_BLOCK_LENGTH];

    workload_status status = WORKLOAD_OK;

    if (encrypt_ctx == NULL || decrypt_ctx == NULL) {
        status = WORKLOAD_ERROR;
    }

    for (long i = 0; status == WORKLOAD_OK && i < volume; i++) {
        int ciphertext_len = 0;
        int plaintext_len = 0;

        if (RAND_bytes(key, AES_GCM_KEY_LEN) != 1 || RAND_bytes(iv, AES_GCM_IV_LEN) != 1 ||
            !encrypt_cycle(encrypt_ctx, key, iv, ciphertext, &ciphertext_len, tag) ||
            !decrypt_cycle(decrypt_ctx, key, iv, ciphertext, ciphertext_len, tag, plaintext_copy,
                           &plaintext_len) ||
            plaintext_len != PLAINTEXT_LEN ||
            memcmp(plaintext_copy, PLAINTEXT, (size_t)PLAINTEXT_LEN) != 0) {
            status = WORKLOAD_ERROR;
        }
    }

    OPENSSL_cleanse(key, sizeof(key));
    EVP_CIPHER_CTX_free(encrypt_ctx);
    EVP_CIPHER_CTX_free(decrypt_ctx);

    return status;
}
