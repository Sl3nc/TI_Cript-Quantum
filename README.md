# TI_Cript-Quantum

Programa de avaliação de algoritmos criptográficos pós-quânticos da biblioteca **quantCrypt**.

## Objetivo

Coletar métricas de desempenho e hardware durante a execução de algoritmos pós-quânticos:
- **MLKEM_1024** (Key Encapsulation Mechanism)
- **MLDSA_87** (Digital Signature Scheme)
- **Krypton** (Cipher)

## Métricas Coletadas

1. **CPU Time** (ms) - Tempo total de execução
2. **Memory** (MB) - Consumo máximo de memória
3. **CPU Cycles** - Ciclos de CPU utilizados
4. **Cache Misses** - Falhas de cache L1/L2/L3
5. **Hardware Info** - CPU, cores, frequência, RAM

## Estrutura

```
src/
├── algorithms/        # Implementações usando quantCrypt
├── metrics/           # Profiling e coleta de métricas
└── orchestration/     # Execução e configuração
tests/
├── unit/              # Testes unitários
├── integration/       # Testes de integração
└── contract/          # Testes de contrato
docs/results/          # Relatórios Markdown gerados
```

## Instalação

```bash
pip install -r requirements.txt
```

## Uso Básico

```bash
# Executar avaliação de um algoritmo
python -m src.orchestration.run_single MLKEM_1024 --volume 1000

# Gerar relatório individual
python -m src.orchestration.generate_report MLKEM_1024

# Análise de escalabilidade
python -m src.orchestration.run_scalability MLKEM_1024 --volumes 100,500,1000,5000
```

## Testes

```bash
pytest
```

## Relatórios

Gerados em `docs/results/<algorithm>/` no formato Markdown com timestamp PT-BR.

## Conformidade

Este projeto segue a [Constituição v1.0.0](.specify/memory/constitution.md):
- Uso exclusivo de quantCrypt (sem implementações customizadas)
- TDD obrigatório (pytest)
- Perfilamento com cProfile, line_profiler, memory_profiler
- Métricas padronizadas para todos os algoritmos
