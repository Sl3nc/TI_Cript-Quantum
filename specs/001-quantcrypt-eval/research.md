# Research: Avaliação de Métricas Pós-Quânticas quantCrypt

**Date**: 2025-11-04
**Branch**: 001-quantcrypt-eval

## Decisions & Rationale

### 1. Linguagem e Versão
- Decision: Python 3.11
- Rationale: Versão estável com melhorias de performance; ampla compatibilidade com bibliotecas de profilamento e análise.
- Alternatives considered: 3.10 (mais antigo), 3.12 (potencial incompatibilidade inicial com line_profiler). Escolhida 3.11 por equilíbrio estabilidade/recursos.

### 2. Estrutura de Diretórios
- Decision: Separar `src/algorithms/` e `src/metrics/` + `src/orchestration/`.
- Rationale: Isolação garante neutralidade experimental; métricas reutilizáveis e não acopladas a cada algoritmo.
- Alternatives: Pasta única com tudo misturado (reduz clareza); subpacotes por algoritmo (duplicação de métricas).

### 3. Volume Configurável
- Decision: Definido em arquivo `config.py`
- Rationale: Simples de alterar; permite experimentos rápidos.
- Alternatives: Arquivo YAML único (mais complexo e necessidade parser adicional).

### 4. Métricas Obrigatórias
- Decision: cProfile, line_profiler, memory_profiler, psutil, py-cpuinfo; armazenar séries temporais + agregados.
- Rationale: Cobre tempo total, linhas críticas, consumo incremental de memória e dinâmica de CPU.
- Alternatives: Perf do SO (mais complexo, fora escopo); eBPF (alto custo de adoção).

### 5. Visualizações
- Decision: Linhas (evolução) + Barras (resumos) com matplotlib.
- Rationale: Atende clareza para padrões temporais e comparações agregadas.
- Alternatives: Seaborn (camada extra), Plotly (interativo fora do requerimento).

### 6. Timestamp e Unicidade
- Decision: Formato PT-BR com milissegundos `DD-MM-YYYY HHhMMmSSs.mmm`; unicidade via ms + fallback sufixo.
- Rationale: Legível localmente mantendo singularidade; milissegundos minimizam colisões.
- Alternatives: ISO 8601 (mais neutro porém pedido de legibilidade local), hash curto (acréscimo irrelevante).

### 7. Reprodutibilidade
- Decision: Capturar hardware uma vez por execução; seeds fixos (quando aplicável) em `config.py`.
- Rationale: Garantia de repetição; neutralidade experimental.
- Alternatives: Captura contínua de hardware (redundante) ou ausência de seed (menor controle).

### 8. Formato de Relatório
- Decision: Markdown + tabulate para tabela; subseções: Resumo, Métricas, Gráficos, Metadados.
- Rationale: Simplicidade, compatível com versionamento git.
- Alternatives: HTML (mais pesado), JSON puro (menos legível para humanos).

### 9. Escalabilidade Multi-Volume
- Decision: Script `run_scalability.py` gera avaliações sequenciais; agrega estatísticas em relatório comparativo.
- Rationale: Controla ordem e garante ambiente consistente.
- Alternatives: Execuções paralelas (risco de interferência em métricas de CPU/memória).

### 10. Test Strategy (TDD)
- Decision: Criar testes unitários para cada módulo de métricas e algoritmos; integração para orquestração.
- Rationale: Garantir falha inicial e evolução; evita regressões.
- Alternatives: Somente integração (menor granularidade de falha); cobertura agressiva (desnecessária por constituição).

## Unresolved Items
Nenhum.

## Risks
- Risco de overhead >10% com múltiplos profiler simultâneos (Mitigation: medir overhead inicial e documentar).
- Risco de falta de ciclos CPU/cache misses se API não disponível em ambiente (Mitigation: fallback com aviso e marcação de campo nulo).

## Research Tasks (Completed)
- Perf libs comparadas.
- Estratégias de unicidade avaliadas.
- Estrutura de modularização validada.

## Conclusion
Pesquisa conclui viabilidade. Nenhuma clarificação pendente. Pronto para design (Phase 1).
