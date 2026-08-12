# TI_Cript-Quantum

Executor de benchmarks de algoritmos criptográficos pós-quânticos (**quantCrypt**) e clássicos
(**cryptography**), usados como baseline comparativo.

## Objetivo

Executar a carga de trabalho — e **apenas** ela. O programa não coleta métricas, não cronometra a
si mesmo e não gera relatórios ou gráficos: a medição e a análise são feitas por programas
externos e dedicados, que envolvem este processo. Assim o que se mede é o algoritmo, não o
overhead da ferramenta.

O programa comunica-se com o coletor externo por duas superfícies apenas: a carga executada e o
código de saída (`0` = sucesso, `1` = falha).

## Algoritmos suportados

| Nome (CLI)       | Biblioteca     | Operação por ciclo                          |
| ---------------- | -------------- | ------------------------------------------- |
| `KEM`            | quantCrypt     | MLKEM_1024: keygen → encaps → decaps        |
| `DSS`            | quantCrypt     | MLDSA_87: keygen → sign → verify            |
| `Krypton`        | quantCrypt     | Krypton: encrypt → decrypt                  |
| `RSA`            | cryptography   | keygen (1024) → sign PSS → verify           |
| `DSA`            | cryptography   | keygen (1024) → sign → verify               |
| `Diffie-Hellman` | cryptography   | key exchange (1024) → HKDF                  |

## Instalação

```bash
pip install -r requirements.txt
```

## Uso

```bash
# Um algoritmo, N operações
python src/index.py --algorithm KEM --volume 1000
python src/index.py -a RSA -v 500

# Vários algoritmos em sequência, sob o mesmo volume
python src/index.py -a KEM DSS Krypton -v 1000
```

`src/index.py` é o único entrypoint. Ele insere `src/` no `sys.path`, então os módulos internos
usam imports diretos (`from config import ...`).

## Medição externa

O programa foi feito para ser envolvido por um coletor. Exemplos:

```bash
/usr/bin/time -v python src/index.py -a KEM -v 1000
perf stat -d python src/index.py -a KEM -v 1000
```

## Testes

```bash
# O layout src/ exige PYTHONPATH (nenhum pytest.ini/pyproject.toml configura isso)
PYTHONPATH=src pytest
PYTHONPATH=src pytest tests/unit/test_mlkem_kem.py -v
```

## Adicionar um algoritmo

1. Criar `src/algorithms/<nome>.py` expondo `run_<nome>(volume: int)`, que executa `volume` ciclos
   completos e idênticos, sem nenhuma lógica de medição.
2. Registrar a função em `ALGORITHMS`, em `src/config.py`.
3. Adicionar o teste correspondente em `tests/unit/`.

## Conformidade

Este projeto segue a [Constituição v3.0.0](.specify/memory/constitution.md):

- **Princípio I**: sem criptografia própria — só quantCrypt e `cryptography`
- **Princípio II**: instrumentação externa — nenhuma medição dentro de `src/`
- **Princípio III**: cargas de trabalho neutras e comparáveis
- **Princípio IV**: TDD obrigatório (pytest)
- **Princípio V**: reprodutibilidade a partir da linha de comando
