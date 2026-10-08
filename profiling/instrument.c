/*
 * Instrumentação por etapa dos workloads.
 *
 * Este arquivo NÃO faz parte da imagem de execução: só é compilado quando a
 * opção BENCH_PROFILE do CMake está ligada, e é linkado apenas no binário da
 * imagem de profiling. O linker reescreve as chamadas diretas dos módulos em
 * src/algorithms/ para __wrap_*, que cronometram a chamada real entre dois
 * clock_gettime e acumulam soma e número de chamadas por etapa.
 *
 * Cobre as etapas de todos os algoritmos:
 *
 *   KEM       keygen -> encaps -> decaps
 *   DSS       keygen -> sign -> verify
 *   MCELIECE  keygen -> encaps -> kdf -> encrypt -> decaps -> kdf -> decrypt
 *   ECIES     keygen -> derive -> kdf -> encrypt -> derive -> kdf -> decrypt
 *   ECDSA     keygen -> sign -> verify
 *   ECDH      keygen -> derive (2 lados)
 *
 * As funções estáticas dos módulos (kdf e AEAD) não são envolvíveis pelo linker,
 * então as etapas "kdf", "encrypt" e "decrypt" são compostas pelas chamadas EVP
 * que elas usam (EVP_Digest e as três chamadas de cada lado do AES-GCM).
 *
 * O resultado é emitido uma única vez ao final do processo, no formato de
 * exposição do Prometheus. Se BENCH_METRICS_FILE estiver definido, escreve nele;
 * caso contrário, escreve em stdout.
 */

#define _POSIX_C_SOURCE 200809L

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include <openssl/evp.h>
#include <oqs/oqs.h>

/* ---- símbolos reais ---------------------------------------------------- */

OQS_STATUS __real_OQS_KEM_keypair(const OQS_KEM *kem, uint8_t *public_key, uint8_t *secret_key);
OQS_STATUS __real_OQS_KEM_encaps(const OQS_KEM *kem, uint8_t *ciphertext, uint8_t *shared_secret,
                                 const uint8_t *public_key);
OQS_STATUS __real_OQS_KEM_decaps(const OQS_KEM *kem, uint8_t *shared_secret, const uint8_t *ciphertext,
                                 const uint8_t *secret_key);

OQS_STATUS __real_OQS_SIG_keypair(const OQS_SIG *sig, uint8_t *public_key, uint8_t *secret_key);
OQS_STATUS __real_OQS_SIG_sign(const OQS_SIG *sig, uint8_t *signature, size_t *signature_len,
                               const uint8_t *message, size_t message_len, const uint8_t *secret_key);
OQS_STATUS __real_OQS_SIG_verify(const OQS_SIG *sig, const uint8_t *message, size_t message_len,
                                 const uint8_t *signature, size_t signature_len, const uint8_t *public_key);

int __real_EVP_Digest(const void *data, size_t count, unsigned char *md, unsigned int *size,
                      const EVP_MD *type, ENGINE *impl);
int __real_EVP_PKEY_generate(EVP_PKEY_CTX *ctx, EVP_PKEY **ppkey);
int __real_EVP_PKEY_derive(EVP_PKEY_CTX *ctx, unsigned char *key, size_t *keylen);
int __real_EVP_DigestSign(EVP_MD_CTX *ctx, unsigned char *sigret, size_t *siglen, const unsigned char *tbs,
                          size_t tbslen);
int __real_EVP_DigestVerify(EVP_MD_CTX *ctx, const unsigned char *sigret, size_t siglen,
                            const unsigned char *tbs, size_t tbslen);
int __real_EVP_EncryptInit_ex(EVP_CIPHER_CTX *ctx, const EVP_CIPHER *cipher, ENGINE *impl,
                              const unsigned char *key, const unsigned char *iv);
int __real_EVP_EncryptUpdate(EVP_CIPHER_CTX *ctx, unsigned char *out, int *outl, const unsigned char *in,
                             int inl);
int __real_EVP_EncryptFinal_ex(EVP_CIPHER_CTX *ctx, unsigned char *out, int *outl);
int __real_EVP_DecryptInit_ex(EVP_CIPHER_CTX *ctx, const EVP_CIPHER *cipher, ENGINE *impl,
                              const unsigned char *key, const unsigned char *iv);
int __real_EVP_DecryptUpdate(EVP_CIPHER_CTX *ctx, unsigned char *out, int *outl, const unsigned char *in,
                             int inl);
int __real_EVP_DecryptFinal_ex(EVP_CIPHER_CTX *ctx, unsigned char *outm, int *outl);

/* ---- acumuladores ------------------------------------------------------ */

enum step_id {
    STEP_KEYGEN,
    STEP_SIGN,
    STEP_VERIFY,
    STEP_ENCAPS,
    STEP_DECAPS,
    STEP_DERIVE,
    STEP_KDF,
    STEP_ENCRYPT,
    STEP_DECRYPT,
    STEP_COUNT
};

struct step_stats {
    const char *name;
    uint64_t sum_ns;
    uint64_t calls;
};

static struct step_stats steps[STEP_COUNT] = {
    [STEP_KEYGEN] = {"keygen", 0, 0},
    [STEP_SIGN] = {"sign", 0, 0},
    [STEP_VERIFY] = {"verify", 0, 0},
    [STEP_ENCAPS] = {"encaps", 0, 0},
    [STEP_DECAPS] = {"decaps", 0, 0},
    [STEP_DERIVE] = {"derive", 0, 0},
    [STEP_KDF] = {"kdf", 0, 0},
    [STEP_ENCRYPT] = {"encrypt", 0, 0},
    [STEP_DECRYPT] = {"decrypt", 0, 0},
};

static uint64_t now_ns(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (uint64_t)ts.tv_sec * 1000000000ULL + (uint64_t)ts.tv_nsec;
}

static void record(enum step_id id, uint64_t start_ns) {
    steps[id].sum_ns += now_ns() - start_ns;
    steps[id].calls++;
}

/* ---- liboqs: KEM (KEM, MCELIECE) --------------------------------------- */

OQS_STATUS __wrap_OQS_KEM_keypair(const OQS_KEM *kem, uint8_t *public_key, uint8_t *secret_key) {
    uint64_t start_ns = now_ns();
    OQS_STATUS status = __real_OQS_KEM_keypair(kem, public_key, secret_key);
    record(STEP_KEYGEN, start_ns);
    return status;
}

OQS_STATUS __wrap_OQS_KEM_encaps(const OQS_KEM *kem, uint8_t *ciphertext, uint8_t *shared_secret,
                                 const uint8_t *public_key) {
    uint64_t start_ns = now_ns();
    OQS_STATUS status = __real_OQS_KEM_encaps(kem, ciphertext, shared_secret, public_key);
    record(STEP_ENCAPS, start_ns);
    return status;
}

OQS_STATUS __wrap_OQS_KEM_decaps(const OQS_KEM *kem, uint8_t *shared_secret, const uint8_t *ciphertext,
                                 const uint8_t *secret_key) {
    uint64_t start_ns = now_ns();
    OQS_STATUS status = __real_OQS_KEM_decaps(kem, shared_secret, ciphertext, secret_key);
    record(STEP_DECAPS, start_ns);
    return status;
}

/* ---- liboqs: assinatura (DSS) ------------------------------------------ */

OQS_STATUS __wrap_OQS_SIG_keypair(const OQS_SIG *sig, uint8_t *public_key, uint8_t *secret_key) {
    uint64_t start_ns = now_ns();
    OQS_STATUS status = __real_OQS_SIG_keypair(sig, public_key, secret_key);
    record(STEP_KEYGEN, start_ns);
    return status;
}

OQS_STATUS __wrap_OQS_SIG_sign(const OQS_SIG *sig, uint8_t *signature, size_t *signature_len,
                               const uint8_t *message, size_t message_len, const uint8_t *secret_key) {
    uint64_t start_ns = now_ns();
    OQS_STATUS status = __real_OQS_SIG_sign(sig, signature, signature_len, message, message_len, secret_key);
    record(STEP_SIGN, start_ns);
    return status;
}

OQS_STATUS __wrap_OQS_SIG_verify(const OQS_SIG *sig, const uint8_t *message, size_t message_len,
                                 const uint8_t *signature, size_t signature_len, const uint8_t *public_key) {
    uint64_t start_ns = now_ns();
    OQS_STATUS status =
        __real_OQS_SIG_verify(sig, message, message_len, signature, signature_len, public_key);
    record(STEP_VERIFY, start_ns);
    return status;
}

/* ---- OpenSSL: chaves, assinatura e KDF --------------------------------- */

int __wrap_EVP_PKEY_generate(EVP_PKEY_CTX *ctx, EVP_PKEY **ppkey) {
    uint64_t start_ns = now_ns();
    int ret = __real_EVP_PKEY_generate(ctx, ppkey);
    record(STEP_KEYGEN, start_ns);
    return ret;
}

int __wrap_EVP_PKEY_derive(EVP_PKEY_CTX *ctx, unsigned char *key, size_t *keylen) {
    uint64_t start_ns = now_ns();
    int ret = __real_EVP_PKEY_derive(ctx, key, keylen);
    record(STEP_DERIVE, start_ns);
    return ret;
}

int __wrap_EVP_Digest(const void *data, size_t count, unsigned char *md, unsigned int *size,
                      const EVP_MD *type, ENGINE *impl) {
    uint64_t start_ns = now_ns();
    int ret = __real_EVP_Digest(data, count, md, size, type, impl);
    record(STEP_KDF, start_ns);
    return ret;
}

int __wrap_EVP_DigestSign(EVP_MD_CTX *ctx, unsigned char *sigret, size_t *siglen, const unsigned char *tbs,
                          size_t tbslen) {
    uint64_t start_ns = now_ns();
    int ret = __real_EVP_DigestSign(ctx, sigret, siglen, tbs, tbslen);
    record(STEP_SIGN, start_ns);
    return ret;
}

int __wrap_EVP_DigestVerify(EVP_MD_CTX *ctx, const unsigned char *sigret, size_t siglen,
                            const unsigned char *tbs, size_t tbslen) {
    uint64_t start_ns = now_ns();
    int ret = __real_EVP_DigestVerify(ctx, sigret, siglen, tbs, tbslen);
    record(STEP_VERIFY, start_ns);
    return ret;
}

/* ---- OpenSSL: AEAD ----------------------------------------------------- */

int __wrap_EVP_EncryptInit_ex(EVP_CIPHER_CTX *ctx, const EVP_CIPHER *cipher, ENGINE *impl,
                              const unsigned char *key, const unsigned char *iv) {
    uint64_t start_ns = now_ns();
    int ret = __real_EVP_EncryptInit_ex(ctx, cipher, impl, key, iv);
    record(STEP_ENCRYPT, start_ns);
    return ret;
}

int __wrap_EVP_EncryptUpdate(EVP_CIPHER_CTX *ctx, unsigned char *out, int *outl, const unsigned char *in,
                             int inl) {
    uint64_t start_ns = now_ns();
    int ret = __real_EVP_EncryptUpdate(ctx, out, outl, in, inl);
    record(STEP_ENCRYPT, start_ns);
    return ret;
}

int __wrap_EVP_EncryptFinal_ex(EVP_CIPHER_CTX *ctx, unsigned char *out, int *outl) {
    uint64_t start_ns = now_ns();
    int ret = __real_EVP_EncryptFinal_ex(ctx, out, outl);
    record(STEP_ENCRYPT, start_ns);
    return ret;
}

int __wrap_EVP_DecryptInit_ex(EVP_CIPHER_CTX *ctx, const EVP_CIPHER *cipher, ENGINE *impl,
                              const unsigned char *key, const unsigned char *iv) {
    uint64_t start_ns = now_ns();
    int ret = __real_EVP_DecryptInit_ex(ctx, cipher, impl, key, iv);
    record(STEP_DECRYPT, start_ns);
    return ret;
}

int __wrap_EVP_DecryptUpdate(EVP_CIPHER_CTX *ctx, unsigned char *out, int *outl, const unsigned char *in,
                             int inl) {
    uint64_t start_ns = now_ns();
    int ret = __real_EVP_DecryptUpdate(ctx, out, outl, in, inl);
    record(STEP_DECRYPT, start_ns);
    return ret;
}

int __wrap_EVP_DecryptFinal_ex(EVP_CIPHER_CTX *ctx, unsigned char *outm, int *outl) {
    uint64_t start_ns = now_ns();
    int ret = __real_EVP_DecryptFinal_ex(ctx, outm, outl);
    record(STEP_DECRYPT, start_ns);
    return ret;
}

/* ---- emissão ----------------------------------------------------------- */

static uint64_t cycle_count(void) {
    const char *text = getenv("BENCH_VOLUME");
    if (text != NULL && text[0] != '\0') {
        char *end = NULL;
        long parsed = strtol(text, &end, 10);
        if (end != text && *end == '\0' && parsed > 0) {
            return (uint64_t)parsed;
        }
    }
    return 0;
}

__attribute__((destructor)) static void emit_metrics(void) {
    uint64_t cycles = cycle_count();
    int any = 0;

    for (int i = 0; i < STEP_COUNT; i++) {
        if (steps[i].calls > 0) {
            any = 1;
            break;
        }
    }
    if (!any) {
        return;
    }

    const char *algorithm = getenv("BENCH_STEP_ALGORITHM");
    if (algorithm == NULL || algorithm[0] == '\0') {
        algorithm = "KEM";
    }

    const char *path = getenv("BENCH_METRICS_FILE");
    FILE *out = (path != NULL && path[0] != '\0') ? fopen(path, "w") : stdout;
    if (out == NULL) {
        return;
    }

    fputs("# HELP benchmark_step_seconds_sum Tempo de parede acumulado por etapa do workload.\n", out);
    fputs("# TYPE benchmark_step_seconds_sum counter\n", out);
    fputs("# TYPE benchmark_step_seconds_count counter\n", out);
    fputs("# TYPE benchmark_step_calls counter\n", out);

    for (int i = 0; i < STEP_COUNT; i++) {
        const struct step_stats *stats = &steps[i];
        if (stats->calls == 0) {
            continue;
        }

        uint64_t count = cycles > 0 ? cycles : stats->calls;

        fprintf(out, "benchmark_step_seconds_sum{algorithm=\"%s\",step=\"%s\"} %.9f\n", algorithm,
                stats->name, (double)stats->sum_ns / 1e9);
        fprintf(out, "benchmark_step_seconds_count{algorithm=\"%s\",step=\"%s\"} %llu\n", algorithm,
                stats->name, (unsigned long long)count);
        fprintf(out, "benchmark_step_calls{algorithm=\"%s\",step=\"%s\"} %llu\n", algorithm, stats->name,
                (unsigned long long)stats->calls);
    }

    if (out != stdout) {
        fclose(out);
    }
}
