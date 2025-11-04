# Feature Specification: Avaliação de Métricas Pós-Quânticas quantCrypt

**Feature Branch**: `001-quantcrypt-eval`  
**Created**: 2025-11-04  
**Status**: Draft  
**Input**: User description: "Desejo construir um programa que resolva problemas criptográficos com cada um dos algoritmos criptográficos pós-quânticos disponibilizados pela biblioteca quantCrypt enquanto coleta métricas..." (trecho resumido)

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Executar avaliação única (Priority: P1)

Usuário inicia a avaliação de UM algoritmo pós-quântico (MLKEM_1024, MLDSA_87 ou Krypton) para UM desafio criptográfico correspondente ao algoritmo (MLKEM_1024: Encapsulação de chaves, MLDSA_87: assinatura digital, Krypton: criptografia) informando o parâmetro de volume (ex.: número de chaves) ajustável.

**Why this priority**: Sea execução repetida até alcançar o parâmetro de volume definido, não há coleta de métricas ou geração de relatório.

**Independent Test**: Executar apenas este fluxo produz relatório completo para um algoritmo-problema com métricas exigidas.

**Acceptance Scenarios**:

1. **Given** parâmetro de volume definido (ex.: 1000), **When** inicia execução para MLKEM_1024, **Then** gera chaves, cifra/decifra e coleta todas as métricas.
2. **Given** mudança do parâmetro (ex.: 1000→2000), **When** reexecuta, **Then** relatório reflete novo volume sem alterar outros passos.

---

### User Story 2 - Gerar relatório individual (Priority: P2)

Após execução isolada algoritmo+desafio, sistema produz relatório contendo: resumo textual, tabela Markdown de métricas (todas), gráficos ilustrando uso de recursos ao longo da execução e metadados de ambiente/hardware. Nome do arquivo segue padrão `<Algoritmo> - <timestamp>`.

**Why this priority**: Valor analítico depende de persistir e visualizar métricas de cada execução.

**Independent Test**: Apenas o fluxo de geração de relatório pode ser validado usando dados de uma execução simulada.

**Acceptance Scenarios**:

1. **Given** execução completa concluída, **When** solicita geração de relatório, **Then** cria arquivo e pasta (se inexistente) e inclui tabela + gráficos + metadados.
2. **Given** relatório existente, **When** reexecuta mesmo algoritmo em horário diferente, **Then** novo arquivo distinto com timestamp único.

---

### User Story 3 - Avaliar escalabilidade (Priority: P3)

Usuário executa múltiplas avaliações variando o parâmetro de volume (ex.: 1000, 5000, 10000) para o mesmo algoritmo+desafio e consolida tendência de métricas (tempo, memória, ciclos) em relatório comparativo.

**Why this priority**: Permite análise de crescimento de custo computacional e comparação entre tamanhos de carga.

**Independent Test**: Rodar apenas este fluxo usando um algoritmo gera conjunto de relatórios + comparativo.

**Acceptance Scenarios**:

1. **Given** lista de volumes [1000,5000,10000], **When** inicia execução escalável, **Then** gera 3 relatórios individuais + 1 resumo comparativo.
2. **Given** falha em um volume intermediário, **When** processo continua, **Then** registra erro e gera relatórios dos volumes restantes sem comprometer integridade dos existentes.

---

[Add more user stories as needed, each with an assigned priority]

### Edge Cases

- Parâmetro de volume = 0 (deve rejeitar antes de iniciar).
- Falha ao coletar dados de hardware (usar fallback parcial e registrar aviso).
- Interrupção manual da execução (relatório parcial marcado como incompleto).
- Timestamp colidindo com execução simultânea (garantir unicidade via segundos + sufixo incremental).

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: MUST executar avaliação para um único algoritmo+desafio com parâmetro de volume ajustável.
- **FR-002**: MUST permitir ajuste do parâmetro de volume sem alterar código (ex.: configuração externa ou argumento).
- **FR-003**: MUST gerar relatório individual contendo tabela de métricas, texto descritivo e gráficos de linhas (séries temporais) e barras (resumos agregados) como padrão.
- **FR-004**: MUST nomear relatórios `<Algoritmo> - <timestamp>` usando formato local PT-BR: `DD-MM-YYYY HHhMMmSSs.mmm` (ex.: `04-11-2025 15h15m03s.127`).
- **FR-005**: MUST criar pasta dedicada por algoritmo se não existir e armazenar relatórios incrementais.
- **FR-006**: MUST registrar falhas parciais sem eliminar dados já coletados.
- **FR-007**: MUST permitir execução escalável (lista de volumes) produzindo relatório comparativo agregado.
- **FR-008**: MUST validar volume mínimo (>0) antes de iniciar execução.
- **FR-009**: MUST garantir unicidade de nomes de relatório em execuções simultâneas (uso de milissegundos no timestamp e sufixo incremental se necessário).
- **FR-010**: MUST incluir metadados: algoritmo, tipo de desafio, volumes, horário início/fim, duração total, ambiente e hardware.
- **FR-011**: SHOULD permitir reuso do dataset de métricas para visualizações adicionais sem rerun completo.
- **FR-012**: MUST registrar erro e continuar nas execuções escaláveis restantes se um volume falhar.
- **FR-013**: MUST consolidar comparação de métricas (tempo médio por operação, pico memoria, ciclos por unidade) no relatório de escalabilidade.

### Post-Quantum Evaluation (Constitution-Enforced)

- **FR-POSTQ-001**: System MUST use ONLY quantCrypt algorithms (no custom crypto code).
- **FR-POSTQ-002**: MUST collect metrics: CPU time, memory usage, CPU cycles, cache misses, hardware info for every run.
- **FR-POSTQ-003**: MUST instrument profiling with cProfile, line_profiler, memory_profiler, psutil, py-cpuinfo.
- **FR-POSTQ-004**: MUST output results as Markdown tables via tabulate.
- **FR-POSTQ-005**: Tests (pytest) MUST be written prior to implementation (TDD); coverage percentage is NOT a gate.
- **FR-POSTQ-006**: MUST record environment metadata (OS, Python version, quantCrypt version, hardware specs) once per batch and reference in outputs.

<!-- Example section removed: all clarifications resolved; no pending generic items. -->

### Key Entities *(include if feature involves data)*

- **AlgorithmEvaluation**: Representa uma execução única (algoritmo, desafio, volume, timestamps, status, coleção de métricas).
- **MetricRecord**: Estrutura de valores medidos (tempo CPU, ciclos, cache misses, memória, hardware snapshot id, ordem temporal).
- **HardwareProfile**: Características do ambiente (arquitetura, núcleos, frequência, SO, versão Python, versão quantCrypt).
- **EvaluationReport**: Documento persistido unindo resumo textual, tabela métricas, gráficos, metadados.
- **ScalabilitySeries**: Coleção ordenada de AlgorithmEvaluation para diferentes volumes + resumo comparativo.

### Assumptions

- Parâmetro de volume será fornecido como número inteiro positivo (>0).
- Cada algoritmo possui pelo menos um desafio criptográfico claramente definido (ex.: KEM: geração/cifragem/decifragem de chaves; DSS: geração/assinatura/verificação; Cipher: cifrar/decifrar blocos).
- Coleta de métricas não altera comportamento dos algoritmos.
- Ambiente dispõe de recursos suficientes para volumes iniciais (ex.: 1000 operações) sem otimizações especiais.
- Representação temporal para gráficos usará ordem de coleta incremental.
<!-- Clarificações resolvidas: gráficos (linhas+barras), timestamp (PT-BR com ms), unicidade (milissegundos). -->

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: Realizar avaliação única e gerar relatório completo (todos campos) em <= 1 execução manual (sem etapas adicionais).
- **SC-002**: Ajustar volume e repetir execução exige somente alteração de 1 parâmetro configurável.
- **SC-003**: 100% dos relatórios gerados contêm as 5 métricas obrigatórias e metadados de hardware.
- **SC-004**: Série escalável (>=3 volumes) gera relatório comparativo com métricas agregadas (tempo médio, pico memória) em <= 1 fluxo dedicado.
- **SC-005**: Falhas parciais não removem dados já coletados (persistência garantida em 100% dos casos simulados).
- **SC-006**: Nome de arquivo sempre único (0 colisões em 100 execuções consecutivas simuladas) utilizando milissegundos no timestamp.
