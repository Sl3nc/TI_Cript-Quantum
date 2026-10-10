# TI_Cript-Quantum

Executor de benchmarks de algoritmos criptográficos pós-quânticos (**liboqs**) e clássicos (**libcrypto**, do OpenSSL 3.x), usados como baseline comparativo. Escrito em C11.

## Objetivo

Executar a carga de trabalho. A medição e a análise são feitas por programas externos e dedicados, que envolvem este processo. Assim o que se mede é o algoritmo, não o overhead da ferramenta.

O programa comunica-se com o coletor externo por duas superfícies apenas: a carga executada e o
código de saída (`0` = sucesso, `1` = falha).

## Algoritmos suportados

Todos os algoritmos aceitam o nível de segurança `--effort/-e` (`1`, `3` ou `5`), que seleciona o
parameter set equivalente à Categoria NIST.

| Nome (CLI) | Biblioteca | Operação por ciclo                                       | Nível 1 / 3 / 5                               |
| ---------- | ---------- | -------------------------------------------------------- | --------------------------------------------- |
| `KEM`      | liboqs     | keygen → encaps → decaps                                 | ML-KEM-512 / 768 / 1024                       |
| `DSS`      | liboqs     | keygen → sign → verify                                   | ML-DSA-44 / 65 / 87                           |
| `MCELIECE` | liboqs     | keygen → encaps+AES-GCM encrypt → decaps+AES-GCM decrypt | Classic-McEliece-348864f / 460896f / 8192128f |
| `ECIES`    | libcrypto  | keygen → ECDH+AES-GCM encrypt → ECDH+AES-GCM decrypt     | P-256 / P-384 / P-521                         |
| `ECDSA`    | libcrypto  | keygen → sign (SHA-256/384/512) → verify                 | P-256 / P-384 / P-521                         |
| `ECDH`     | libcrypto  | key exchange (2 lados)                                   | P-256 / P-384 / P-521                         |

> O `ML-DSA-44` é a menor opção da liboqs, mas é oficialmente Categoria NIST 2 (não existe assinatura pós-quântica padronizada na Categoria 1).

## Pares clássico × pós-quântico

Cada par abaixo compara um algoritmo clássico com seu equivalente pós-quântico, igualados tanto
na operação executada por ciclo quanto no nível de segurança. Com `--effort/-e`, os dois lados do
par rodam no mesmo nível (Categoria NIST 1, 3 ou 5):

| Par              | Clássico | Pós-Quântico | Operação por ciclo (os dois lados)                     |
| ---------------- | -------- | ------------ | ------------------------------------------------------ |
| Cifração (ECIES) | `ECIES`  | `MCELIECE`   | keygen → encrypt → decrypt                             |
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
./build/benchmark --algorithm KEM --effort 5 --volume 1000
./build/benchmark -a ECIES -e 3 -v 500
```

Padrões: `--algorithm KEM`, `--volume 1`. `--effort/-e` é obrigatório e aceita `1`, `3` ou `5`.
Uma carga por invocação.

## Medição externa

O programa foi feito para ser envolvido por um coletor. Exemplos:

```bash
/usr/bin/time -v ./build/benchmark -a KEM -e 5 -v 1000
perf stat -d ./build/benchmark -a KEM -e 5 -v 1000
```

## Docker

A imagem compila o liboqs estaticamente a partir do fonte (tag fixada em `LIBOQS_VERSION`) e
entrega o binário e um pequeno wrapper de entrypoint (`scripts/entrypoint.sh`) no estágio final.

```bash
docker compose build app
docker compose run --rm app --algorithm KEM --effort 5 --volume 1000
```

`docker-compose.yml` também sobe cAdvisor, Prometheus e Grafana para a coleta e visualização
externas. Para que execuções curtas não sejam subnotificadas, a imagem mantém o container vivo
por alguns segundos após a carga (`BENCH_LINGER`, default 7 s) e o `scrape_interval` do cAdvisor
é de 5 s — assim a leitura final do contador cumulativo é sempre coletada, mesmo em runs de
milissegundos. Ajuste com `-e BENCH_LINGER=<segundos>` (use `0` para desativar; deve ser
maior ou igual ao `scrape_interval`).

Para identificar o algoritmo e o nível nas métricas do cAdvisor (labels
`container_label_algorithm` e `container_label_effort`), rode com `-l algorithm=<nome> -l effort=<nível>`
— todos os painéis de cAdvisor distinguem o par algoritmo · nível. O painel "CPU por operação"
também usa o label `volume` para normalizar a CPU pelo número de ciclos executados:

```bash
docker compose run --rm -l algorithm=KEM -l effort=5 -l volume=4000 app -a KEM -e 5 -v 4000
```

O Grafana fica em `http://localhost:3000` (login definido em `.env`, copie de `.env.example`)
com o datasource do Prometheus e o dashboard "Benchmarks por algoritmo (cAdvisor)" já
provisionados — os painéis agrupam CPU e memória por algoritmo e nível
(`container_label_algorithm` · `container_label_effort`).

O painel **"CPU por operação (CPU-s por ciclo)"** divide a CPU total consumida pela execução
pelo `volume`, permitindo comparar algoritmos pelo **custo** e não pela duração. O painel de
CPU% mede apenas **ocupação** do núcleo (duty cycle): execuções curtas aparecem com percentual
menor por diluição na janela de 1 min, mesmo saturando o núcleo enquanto rodam.

### Profiling por etapa

Além da imagem de execução, o `Dockerfile` tem um estágio `profiling` que linka instrumentação
por etapa (via `-Wl,--wrap` nas funções que os módulos chamam diretamente). O binário padrão
permanece sem qualquer medição — a lógica fica em `profiling/instrument.c`, compilada só com
`-DBENCH_PROFILE=ON`.

```bash
docker compose build app-profile
docker compose up -d pushgateway prometheus grafana cadvisor
docker compose run --rm -l volume=1000 -l algorithm=DSS -l effort=5 app-profile -a DSS -e 5 -v 1000
```

O entrypoint de profiling descobre o algoritmo, o esforço e o volume a partir dos próprios
argumentos (`-a`/`-e`/`-v`), envia a soma e a contagem por etapa ao serviço `pushgateway`, que o
Prometheus raspa (job `pushgateway`, com `honor_labels: true`). Cada nível ocupa um grupo distinto
no Pushgateway (`.../algorithm/<ALG>/effort/<N>`) e ganha o label `effort` nas séries. A média por
etapa no Grafana é `sum/count`, restrita às execuções do período selecionado via `push_time_seconds`:

```promql
(label_join(sum by (algorithm, effort, step) (benchmark_step_seconds_sum{algorithm=~"$algorithm", effort=~"$effort"}), "algo_effort", " · nível ", "algorithm", "effort")
/
label_join(sum by (algorithm, effort, step) (benchmark_step_seconds_count{algorithm=~"$algorithm", effort=~"$effort"}), "algo_effort", " · nível ", "algorithm", "effort"))
and on (algorithm, effort)
(push_time_seconds >= $__from/1000 and push_time_seconds <= $__to/1000)
```

As etapas cobertas, por algoritmo:

| Algoritmo  | Etapas                                             |
| ---------- | -------------------------------------------------- |
| `KEM`      | keygen, encaps, decaps                             |
| `DSS`      | keygen, sign, verify                               |
| `MCELIECE` | keygen, encaps, kdf, encrypt, decaps, kdf, decrypt |
| `ECIES`    | keygen, derive, kdf, encrypt, derive, kdf, decrypt |
| `ECDSA`    | keygen, sign, verify                               |
| `ECDH`     | keygen, derive (dois lados)                        |

Observações:

- O divisor é o número de ciclos (`volume`, definido por `-v`), então o valor é o tempo de cada etapa
  **por ciclo**. Etapas que ocorrem mais de uma vez por ciclo (keygen de ECIES/ECDH, derive, kdf, AEAD)
  somam todas as ocorrências. **`-v` é obrigatório para essa métrica fazer sentido:** sem ele o
  entrypoint não define `BENCH_VOLUME`, o divisor cai para o número de chamadas e os valores ficam
  inconsistentes entre etapas (por chamada nas etapas repetidas, por ciclo nas demais). A métrica
  `benchmark_step_calls` traz o número de chamadas, permitindo a média por chamada, se desejado.
- As funções auxiliares `static` dos módulos (KDF e AEAD) não são envolvíveis pelo linker; suas
  etapas são compostas pelas chamadas EVP que usam (`EVP_Digest` e as três chamadas de cada lado
  do AES-GCM).
- O wrap atribui à etapa o tempo da chamada envolvida, incluindo o trabalho que ela executa na
  biblioteca (é assim que as operações do liboqs/libcrypto são medidas). O que ele não faz é
  detalhar as chamadas aninhadas dentro da biblioteca, nem envolver as funções `static` dos módulos.
- Os painéis **"Tempo medio por etapa"** e **"Tempo acumulado por etapa"** são filtrados pelas
  variáveis **"Algoritmo"** (`algorithm`) e **"Nível de segurança"** (`effort`), ambas multisseleção.
  Cada combinação selecionada vira uma linha própria (`algoritmo · nível N`), graças ao `label_join`.
  Como o Pushgateway guarda só o **último** valor por par (algoritmo, nível), aparece a execução mais
  recente; o filtro por `push_time_seconds` restringe as linhas às execuções cujo push caiu na janela
  de tempo do dashboard. O custo da instrumentação é de ~17 ns por chamada, desprezível frente às
  dezenas de microssegundos de cada operação.

## Testes

```bash
ctest --test-dir build --output-on-failure
```

Cada carga tem um executável de teste que verifica a rejeição de `volume <= 0` e de `effort` fora
de `{1, 3, 5}`, além de um ciclo completo em cada nível; `test_config` cobre o registro `ALGORITHMS`
e o `workload_lookup`.

## Adicionar um algoritmo

1. Criar `src/algorithms/<nome>.{h,c}` expondo `workload_status run_<nome>(long volume, int effort)`,
   que valida `volume` e `effort`, executa `volume` ciclos completos e idênticos no parameter set do
   nível, sem nenhuma lógica de medição.
2. Registrar a função no array `ALGORITHMS`, em `src/config.c`, e o fonte em `CMakeLists.txt`.
3. Adicionar `tests/test_<nome>.c` e o nome em `tests/CMakeLists.txt`.
