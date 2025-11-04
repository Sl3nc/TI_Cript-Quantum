# Tasks: Avaliação de Métricas Pós-Quânticas quantCrypt

**Input**: Design documents from `/specs/001-quantcrypt-eval/`
**Prerequisites**: plan.md (required), spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: TDD requerido pela constituição. Incluímos tarefas de testes unitários e de integração.

**Organization**: Tasks são agrupadas por user story para permitir implementação independente.

## Format: `[ID] [P?] [Story] Description`

---
## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Inicializar estrutura de diretórios, configuração e dependências.

- [x] T001 Criar diretórios base `src/algorithms`, `src/metrics`, `src/orchestration`, `tests/unit`, `tests/integration`, `tests/contract`, `docs/results`
- [x] T002 Criar arquivo `requirements.txt` com dependências listadas
- [x] T003 [P] Adicionar `__init__.py` em `src/`, `src/algorithms/`, `src/metrics/`, `src/orchestration/`
- [x] T004 [P] Criar `src/orchestration/config.py` com parâmetros: DEFAULT_VOLUME=1000, SEED=42, RESULTS_DIR
- [x] T006 Criar `README.md` inicial descrevendo objetivo e execução básica
- [x] T007 [P] Criar `tests/__init__.py` e subpastas `__init__.py`
- [x] T008 Definir padrão de timestamp e unicidade em comentário no `config.py`
- [x] T009 Criar `docs/results/.gitkeep` para versionamento

---
## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Infra que TODOS os user stories dependem.

- [ ] T010 Criar esqueleto `src/metrics/profiler_cpu.py` (funções start_cpu_profile, stop_cpu_profile, profile_lines)
- [ ] T011 [P] Criar esqueleto `src/metrics/profiler_memory.py` (função trace_memory)
- [ ] T012 [P] Criar esqueleto `src/metrics/system_stats.py` (class SystemSampler + SystemStatSample dataclass)
- [ ] T013 [P] Criar esqueleto `src/metrics/hardware.py` (função snapshot_hardware)
- [ ] T014 Criar esqueleto `src/metrics/aggregator.py` (funções aggregate, aggregate_series placeholders)
- [ ] T015 [P] Criar esqueleto `src/metrics/report_markdown.py` (funções build_report, build_series_report placeholders)
- [ ] T016 [P] Criar esqueleto `src/metrics/plotting.py` (funções plot_time_series, plot_memory_series, plot_scalability placeholders)
- [ ] T017 Implementar `src/metrics/__init__.py` com classe ProfilerManager orquestrando módulos
- [ ] T018 Criar teste unitário falhando `tests/unit/test_profiler_cpu.py` (verifica start/stop geram estrutura esperada)
- [ ] T019 [P] Criar teste unitário falhando `tests/unit/test_profiler_memory.py`
- [ ] T020 [P] Criar teste unitário falhando `tests/unit/test_system_stats.py`
- [ ] T021 [P] Criar teste unitário falhando `tests/unit/test_aggregator.py`
- [ ] T022 [P] Criar teste unitário falhando `tests/unit/test_report_markdown.py`
- [ ] T023 [P] Criar teste unitário falhando `tests/unit/test_plotting.py`
- [ ] T024 Criar teste integração inicial falhando `tests/integration/test_metrics_flow.py`
- [ ] T025 Adicionar logging estruturado (key=value) em módulos metrics
- [ ] T026 Implementar fallback para ciclos/cache misses (campos None + warning)
- [ ] T027 Validar overhead inicial (script rápido `scripts/measure_overhead.py` placeholder)

**Checkpoint**: Métricas prontas para uso neutro. Todos testes configurados & falhando.

---
## Phase 3: User Story 1 - Executar avaliação única (Priority: P1) 🎯 MVP

**Goal**: Rodar uma avaliação individual com volume configurável e coletar métricas completas.
**Independent Test**: Executar `run_single` para MLKEM_1024 volume 1000 gera objeto AlgorithmEvaluation com métricas e status success.

### Tests (falhando antes da implementação)
- [ ] T028 [P] [US1] Criar teste `tests/unit/test_mlkem_kem.py` (verifica erro se volume<=0 e estrutura retorno vazio antes implementação)
- [ ] T029 [P] [US1] Criar teste `tests/unit/test_mldsa_dss.py`
- [ ] T030 [P] [US1] Criar teste `tests/unit/test_krypton_cipher.py`
- [ ] T031 [US1] Criar teste integração `tests/integration/test_run_single.py` (espera objeto EvaluationReport futuro, falha inicialmente)

### Implementation
- [ ] T032 [P] [US1] Implementar `src/algorithms/mlkem_kem.py` função run_mlkem (placeholder sem lógica)
- [ ] T033 [P] [US1] Implementar `src/algorithms/mldsa_dss.py` função generate_and_sign (placeholder)
- [ ] T034 [P] [US1] Implementar `src/algorithms/krypton_cipher.py` função cipher_rounds (placeholder)
- [ ] T035 [US1] Implementar validação volume>0 em cada função
- [ ] T036 [US1] Implementar coleta incremental métricas dentro das funções usando ProfilerManager
- [ ] T037 [US1] Implementar `src/orchestration/run_single.py` (orquestra hardware snapshot + chamada algoritmo + aggregation)
- [ ] T038 [US1] Criar teste integração valida métricas mínimas (tempo, memória presentes)
- [ ] T039 [US1] Ajustar testes unitários para esperar estrutura final AlgorithmEvaluation

**Checkpoint**: Execução única produz avaliação completa (sem relatório ainda).

---
## Phase 4: User Story 2 - Gerar relatório individual (Priority: P2)

**Goal**: Gerar relatório Markdown completo com gráficos e metadados.
**Independent Test**: Fornecer avaliação simulada gera arquivo `<Algoritmo> - <timestamp>.md` + imagens.

### Tests (antes implementação)
- [ ] T040 [P] [US2] Criar teste `tests/unit/test_report_generation.py` (falha: arquivo não criado)
- [ ] T041 [P] [US2] Criar teste `tests/unit/test_plot_files.py` (falha: imagens não existem)
- [ ] T042 [US2] Criar teste integração `tests/integration/test_run_single_report.py` (espera relatório completo)

### Implementation
- [ ] T043 [P] [US2] Implementar `report_markdown.build_report` (tabela tabulate + seções)
- [ ] T044 [P] [US2] Implementar funções plotting para linhas/barras salvando `.png`
- [ ] T045 [US2] Integrar relatório em `run_single.py` retornando EvaluationReport
- [ ] T046 [US2] Implementar naming com timestamp milissegundos + sufixo se colisão
- [ ] T047 [US2] Atualizar testes para verificar existência de arquivo e imagens
- [ ] T048 [US2] Adicionar metadados hardware ao relatório
- [ ] T049 [US2] Validar unicidade (teste cria 3 execuções rápidas)

**Checkpoint**: Relatórios individuais funcionando. MVP ampliado para análise completa.

---
## Phase 5: User Story 3 - Avaliar escalabilidade (Priority: P3)

**Goal**: Executar múltiplos volumes e gerar relatório comparativo de agregados.
**Independent Test**: Executar `run_scalability` gera relatórios individuais + comparativo agregando métricas.

### Tests (antes implementação)
- [ ] T050 [P] [US3] Criar teste `tests/unit/test_aggregate_series.py` (falha: agregados ausentes)
- [ ] T051 [US3] Criar teste integração `tests/integration/test_run_scalability.py`

### Implementation
- [ ] T052 [P] [US3] Implementar `aggregate_series` em aggregator.py
- [ ] T053 [P] [US3] Implementar `run_scalability.py` (loop volumes + chamada run_single interna)
- [ ] T054 [P] [US3] Implementar `plot_scalability` gráficos comparativos
- [ ] T055 [US3] Implementar `report_markdown.build_series_report` relatório comparativo
- [ ] T056 [US3] Testes verificam métricas agregadas corretas (tempo médio, pico memória)
- [ ] T057 [US3] Teste verificação de persistência de todos arquivos
- [ ] T058 [US3] Manejo de falha parcial (volume falha → status partial marcado)

**Checkpoint**: Série escalável pronta; análise comparativa disponível.

---
## Phase N: Polish & Cross-Cutting Concerns

- [ ] T059 Criar script auditoria `scripts/hardware_audit.py` (hash + versão dependências)
- [ ] T060 [P] Adicionar seed consistente em algoritmos quando aplicável
- [ ] T061 [P] Medir overhead final atualizando `measure_overhead.py`
- [ ] T062 Revisar logs chave=valor e adicionar contexto de execução
- [ ] T063 [P] Criar teste integração `tests/integration/test_overhead_estimation.py`
- [ ] T064 Atualizar `quickstart.md` com novos scripts / exemplos multi-volume
- [ ] T065 Atualizar `README.md` com seção Reprodutibilidade e Auditoria
- [ ] T066 [P] Adicionar `docs/results/README.md` descrevendo convenção de arquivos
- [ ] T067 Verificar neutralidade: script checagem `scripts/check_neutrality.py`
- [ ] T068 Ajustes finais de estilo (ruff/flake8) se configurado
- [ ] T069 Validar ausência de implementação criptográfica própria (scan simples)

---
## Dependencies & Execution Order

### Phase Dependencies
- Setup (Phase 1) → bloqueia Foundational.
- Foundational (Phase 2) → bloqueia todos os User Stories.
- User Story 1 (Phase 3) → independente após Foundational.
- User Story 2 (Phase 4) → depende de User Story 1 completo (avaliação pronta).
- User Story 3 (Phase 5) → depende de User Story 1 (avaliações individuais) e funções de relatório (Phase 4 parcialmente), porém pode iniciar após relatório básico pronto.
- Polish → final.

### User Story Dependencies
- US1: base para avaliação.
- US2: requer US1.
- US3: requer US1 + componentes de relatório de US2.

### Parallel Opportunities
- Métricas módulos (T011–T016) paralelos.
- Testes unitários métricas (T019–T023) paralelos.
- Algoritmos (T032–T034) paralelos.
- Relatório geração vs plotagem (T043–T044) paralelos.
- Série agregação vs plotagem (T052–T054) paralelos.

### Parallel Example: Métricas
```
T019 test_profiler_memory.py
T020 test_system_stats.py
T021 test_aggregator.py
T022 test_report_markdown.py
T023 test_plotting.py
```

### Implementation Strategy
1. Concluir Phase 1 + 2 → base de métricas validada (tests ainda falhando → implementar até verdes).
2. Entregar MVP (US1) → execução única.
3. Expandir com relatório (US2).
4. Adicionar escalabilidade (US3).
5. Polish final.

### Independent Test Criteria
- US1: `run_single` retorna AlgorithmEvaluation com métricas não vazias.
- US2: relatório Markdown contém tabela + gráficos + metadados.
- US3: relatório comparativo contém agregados e referência a todos volumes.

### MVP Scope
- Fases 1–3 (até avaliação única sem relatório).

## Validation
Todos os tasks seguem formato: `- [ ] TXXX [P] [USY] Descrição com caminho`. IDs sequenciais T001–T069.

## Totals
- Total Tasks: 69
- US1 Tasks: 12 (T028–T039)
- US2 Tasks: 10 (T040–T049)
- US3 Tasks: 9 (T050–T058)
- Parallelizable (~[P] marcados): 34

## Notes
Ajustar número de tasks se simplificações ocorrerem ao implementar.
