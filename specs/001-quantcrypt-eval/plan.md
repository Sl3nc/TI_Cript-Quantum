# Implementation Plan: Avaliação de Métricas Pós-Quânticas quantCrypt

**Branch**: `001-quantcrypt-eval` | **Date**: 2025-11-04 | **Spec**: specs/001-quantcrypt-eval/spec.md
**Input**: Feature specification (execuções de MLKEM_1024, MLDSA_87, Krypton com métricas padronizadas)

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementar uma estrutura de avaliação em Python onde cada combinação algoritmo pós-quântico (quantCrypt) + desafio criptográfico reside em um arquivo isolado dentro de `src/algorithms/`. A coleta e análise de métricas (tempo CPU, memória, ciclos, cache misses, hardware) será implementada em módulos separados dentro de `src/metrics/`. Cada execução gera relatório Markdown com tabela (tabulate), gráficos (matplotlib) e metadados de ambiente/hardware. Volume de execução (ex.: número de chaves ou operações) é configurável externamente. Suporte à execução escalável (múltiplos volumes) com relatório comparativo.

MVP: execução única (User Story 1) + relatório individual (User Story 2). Extensão: série escalável (User Story 3).

Key Interfaces: funções run_mlkem, generate_and_sign, cipher_rounds usando ProfilerManager neutro. ReportBuilder consolida métricas.

Risks: overhead >10% (mitigado por medição inicial); indisponibilidade de ciclos/cache (fallback nulo documentado).

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.11
**Primary Dependencies**: quantCrypt, numpy, pandas, tabulate, matplotlib, psutil, py-cpuinfo, line_profiler, memory_profiler
**Storage**: Arquivos locais (resultados em `docs/results/<algoritmo>/`)
**Testing**: pytest (TDD obrigatório)
**Target Platform**: Desktop multiplataforma (Windows atual, considerar Linux/macOS)
**Project Type**: single (estrutura única src/ + tests/)
**Constraints**: Exclusividade quantCrypt; nenhuma modificação interna dos algoritmos; coleta de todas as 5 métricas; nomes de relatório sempre únicos
**Scale/Scope**: 3 algoritmos iniciais; volumes típicos 1k–10k operações ajustáveis; extensível para novos algoritmos sem refatoração estrutural

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The following MUST be satisfied per TI_Cript-Quantum Constitution v1.0.0:

- Exclusividade quantCrypt: Nenhum algoritmo externo ou implementação própria usada.
- Métricas Padronizadas: Plano define coleta de Tempo CPU, Uso memória, Ciclos CPU, Cache misses, Hardware info.
- TDD Pytest: Lista de testes iniciais (falhando) criada antes da implementação.
- Perfilamento: Estratégia inclui cProfile, line_profiler, memory_profiler, psutil, py-cpuinfo.
- Reprodutibilidade: Seeds, versão Python, versão quantCrypt, detalhes de hardware serão registrados.
- Saída Markdown: Formato de tabela (tabulate) especificado para resultados.
- Neutralidade: Mesmos parâmetros experimentais documentados para todos os algoritmos.
- Sem cobertura mínima: Plano não introduz meta de coverage como gate.

All gates MUST be explicitly acknowledged; absence of any one blocks progression.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
src/
├── algorithms/
│   ├── mlkem_kem.py              # Encapsulação/decapsulação chaves MLKEM_1024
│   ├── mldsa_dss.py              # Geração, assinatura e verificação MLDSA_87
│   ├── krypton_cipher.py         # Criptografia/decifra blocos Krypton
│   └── __init__.py
├── metrics/
│   ├── profiler_cpu.py           # cProfile + line_profiler integração
│   ├── profiler_memory.py        # memory_profiler hooks
│   ├── system_stats.py           # psutil coleta contínua
│   ├── hardware.py               # py-cpuinfo snapshot
│   ├── aggregator.py             # Consolidação numpy/pandas
│   ├── report_markdown.py        # Geração tabela tabulate + texto
│   ├── plotting.py               # matplotlib gráficos linhas + barras
│   └── __init__.py
├── orchestration/
│   ├── run_single.py             # Executa uma combinação algoritmo+desafio
│   ├── run_scalability.py        # Executa múltiplos volumes
│   ├── config.py                 # Parâmetros (volume, paths, seeds)
│   └── __init__.py
└── __init__.py

tests/
├── unit/
│   ├── test_mlkem_kem.py
│   ├── test_mldsa_dss.py
│   ├── test_krypton_cipher.py
│   ├── test_profiler_cpu.py
│   ├── test_aggregator.py
│   └── test_report_markdown.py
├── integration/
│   ├── test_run_single.py
│   └── test_run_scalability.py
└── contract/
  └── test_interfaces.py
```

**Structure Decision**: Single project; separar algoritmos (`src/algorithms/`) das métricas (`src/metrics/`) garante reutilização neutra. Pasta `orchestration/` centraliza fluxo e configurações. Tests espelham módulos assegurando TDD.

## Phase 0: Research Summary (link)
Referência: `research.md` concluído (todas decisões resolvidas, nenhum NEEDS CLARIFICATION restante).

## Phase 1: Design Artifacts
- Data Model: `data-model.md` descreve entidades e transições.
- Contracts: `contracts/interfaces.md` define assinatura de funções internas.
- Quickstart: `quickstart.md` descreve execução e TDD.

## Constitution Re-Check (Post-Design)
- Exclusividade quantCrypt: OK (estruturas não implementam criptografia própria).
- Métricas Padronizadas: OK (módulos separados listados).
- TDD Pytest: OK (tests planejados para cada módulo e integração).
- Perfilamento: OK (profiler_cpu/memory/system/hardware).
- Reprodutibilidade: OK (config + hardware snapshot).
- Saída Markdown: OK (report_markdown.py + plotting).
- Neutralidade: OK (ProfilerManager único e reutilizável).
- Sem cobertura mínima: OK (não estabelecido).

Status: Todas as gates aprovadas. Nenhuma violação.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| (nenhuma) | - | - |
