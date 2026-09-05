# TI_Cript-Quantum

Executor de benchmarks de algoritmos criptográficos pós-quânticos (**liboqs**) e clássicos (**libcrypto**, do OpenSSL 3.x), usados como baseline comparativo. Escrito em C11.

## Objetivo

Executar a carga de trabalho. A medição e a análise são feitas por programas externos e dedicados, que envolvem este processo. Assim o que se mede é o algoritmo, não o overhead da ferramenta.

O programa comunica-se com o coletor externo por duas superfícies apenas: a carga executada e o
código de saída (`0` = sucesso, `1` = falha).

## Algoritmos suportados

| Nome (CLI) | Biblioteca | Operação por ciclo                         |
| ---------- | ---------- | ------------------------------------------ |
| `KEM`      | liboqs     | ML-KEM-1024: keygen → encaps → decaps      |
| `DSS`      | liboqs     | ML-DSA-87: keygen → sign → verify          |
| `SPHINCS+` | liboqs     | SPHINCS+-SHA2-256s: keygen → sign → verify |
| `RSA`      | libcrypto  | keygen (15360) → sign PSS/SHA-512 → verify |
| `ECDSA`    | libcrypto  | P-521: keygen → sign SHA-512 → verify      |
| `ECDH`     | libcrypto  | P-521: key exchange (2 lados)              |

## Pares clássico × pós-quântico

Cada par abaixo compara um algoritmo clássico com seu equivalente pós-quântico, igualados tanto
na operação executada por ciclo quanto no nível de segurança (Categoria NIST 5, ~256 bits, em
todos os pares):

| Par              | Clássico | Pós-Quântico | Operação por ciclo (os dois lados)                     |
| ---------------- | -------- | ------------ | ------------------------------------------------------ |
| Assinatura (RSA) | `RSA`    | `SPHINCS+`   | keygen → sign → verify                                 |
| Assinatura (DSA) | `ECDSA`  | `DSS`        | keygen → sign → verify                                 |
| Troca de chave   | `ECDH`   | `KEM`        | keygen → troca/encapsulamento → verificação (`memcmp`) |

## Dependências

- CMake >= 3.16, compilador C11
- OpenSSL >= 3.0 (headers e biblioteca: `libssl-dev` / `openssl-devel`)
- [liboqs](https://github.com/open-quantum-safe/liboqs) instalado (o `CMakeLists.txt` procura
  `liboqsConfig.cmake` e, se não achar, cai para o `pkg-config`)

## Build

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
```

## Uso

```bash
./build/benchmark --algorithm KEM --volume 1000
./build/benchmark -a RSA -v 500
```

Padrões: `--algorithm KEM`, `--volume 1`. Uma carga por invocação.

## Medição externa

O programa foi feito para ser envolvido por um coletor. Exemplos:

```bash
/usr/bin/time -v ./build/benchmark -a KEM -v 1000
perf stat -d ./build/benchmark -a KEM -v 1000
```

## Docker

A imagem compila o liboqs estaticamente a partir do fonte (tag fixada em `LIBOQS_VERSION`) e
entrega apenas o binário no estágio final.

```bash
docker compose build app
docker compose run --rm app --algorithm KEM --volume 1000
```

`docker-compose.yml` também sobe cAdvisor, Prometheus e Grafana para a coleta e visualização
externas. Atenção: o `scrape_interval` do cAdvisor é de 10 s — execuções curtas podem terminar
antes da primeira amostra, então use volumes altos ou um coletor por processo.

Para identificar o algoritmo nas métricas do cAdvisor (label `container_label_algorithm`),
rode com `-l algorithm=<nome>`:

```bash
docker compose run --rm -l algorithm=KEM app -a KEM -v 4000
```

O Grafana fica em `http://localhost:3000` (login definido em `.env`, copie de `.env.example`)
com o datasource do Prometheus e o dashboard "Benchmarks por algoritmo (cAdvisor)" já
provisionados — os painéis agrupam CPU, memória, rede e disco por `container_label_algorithm`.

## Testes

```bash
ctest --test-dir build --output-on-failure
```

Cada carga tem um executável de teste que verifica a rejeição de `volume <= 0` e a execução de um ciclo completo; `test_config` cobre o registro `ALGORITHMS` e o `workload_lookup`.

## Adicionar um algoritmo

1. Criar `src/algorithms/<nome>.{h,c}` expondo `workload_status run_<nome>(long volume)`, que
   executa `volume` ciclos completos e idênticos, sem nenhuma lógica de medição.
2. Registrar a função no array `ALGORITHMS`, em `src/config.c`, e o fonte em `CMakeLists.txt`.
3. Adicionar `tests/test_<nome>.c` e o nome em `tests/CMakeLists.txt`.
