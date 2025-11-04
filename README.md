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

## Reprodutibilidade

O projeto garante reprodutibilidade através de:

### Seeds Determinísticos
Todas as execuções utilizam seeds configuráveis:
```python
# config.py
SEED = 42  # Seed global padrão
```

Cada algoritmo aceita seed como parâmetro:
```bash
python -m src.orchestration.run_single MLKEM_1024 --volume 1000 --seed 12345
```

### Hardware Audit
Gere snapshot do ambiente para documentar configuração:
```bash
python scripts/hardware_audit.py --output audit.json
```

O audit inclui:
- Hash SHA256 do ambiente (hardware + dependências)
- Versão Python e implementação
- Especificações CPU (modelo, arquitetura, frequência, núcleos)
- Memória total e disponível
- Versões exatas de todas as dependências

### Timestamp Milissegundos
Relatórios incluem timestamp com precisão de milissegundos (formato PT-BR):
```text
MLKEM_1024 - 04-11-2025 14h30m15s.123.md
```

Garante unicidade mesmo em execuções rápidas sucessivas.

### Metadados nos Relatórios
Cada relatório inclui seção completa de hardware e configuração:
- CPU: modelo, arquitetura, frequência, núcleos
- Memória: total, disponível
- Sistema operacional
- Versão Python
- Seed utilizado
- Volume de operações

## Auditoria

### Validação de Overhead
Verifique que profiling adiciona <10% de overhead (Princípio IV):
```bash
python scripts/measure_overhead.py
```

Saída esperada:
```text
=== Overhead de Profiling ===
Absoluto: 2.34 ms
Relativo: 4.56%
✓ PASS: Overhead < 10% (Princípio IV OK)
```

### Verificação de Neutralidade
Valide que ProfilerManager é usado identicamente em todos os algoritmos:
```bash
python scripts/check_neutrality.py
```

Garante comparabilidade das métricas (Princípio VII).

### Validação de Criptografia
Confirme que nenhuma implementação criptográfica customizada existe:
```bash
# Scan manual ou script automatizado
grep -r "def encrypt\|def decrypt\|def sign\|def verify" src/algorithms/
# Deve retornar vazio (apenas chamadas a quantCrypt)
```

### Testes de Integração
Execute suite completa de testes:
```bash
# Testes unitários
pytest tests/unit/ -v

# Testes de integração (incluindo overhead)
pytest tests/integration/ -v

# Testes de contrato
pytest tests/contract/ -v

# Coverage report
pytest --cov=src --cov-report=html
```

## Conformidade

Este projeto segue a [Constituição v1.0.0](.specify/memory/constitution.md):
- **Princípio I**: Uso exclusivo de quantCrypt (sem implementações customizadas)
- **Princípio II**: Métricas padronizadas (CPU, Memória, Ciclos, Cache, Hardware)
- **Princípio III**: TDD obrigatório (pytest)
- **Princípio IV**: Perfilamento com overhead <10%
- **Princípio V**: Reprodutibilidade via seeds, versões, hardware audit
- **Princípio VI**: Saída Markdown com tabulate
- **Princípio VII**: Neutralidade entre algoritmos (ProfilerManager idêntico)
