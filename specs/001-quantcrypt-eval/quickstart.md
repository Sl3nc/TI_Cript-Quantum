# Quickstart: Avaliação quantCrypt

## Pré-requisitos
- Python 3.11
- Instalar dependências (exemplo): quantCrypt, numpy, pandas, tabulate, matplotlib, psutil, py-cpuinfo, line_profiler, memory_profiler, pytest.

## Estrutura Principal
```
src/
  algorithms/          # Arquivos por combinação algoritmo+desafio
  metrics/             # Coleta e processamento de métricas
  orchestration/       # Scripts de execução e configuração
```

## Executar Avaliação Única
```bash
python -m src.orchestration.run_single --algorithm MLKEM_1024 --volume 1000
```
Gera relatório em `docs/results/MLKEM_1024/MLKEM_1024 - <timestamp>.md`.

## Executar Série Escalável (Multi-Volume)
```bash
# Análise de escalabilidade com 3 volumes
python -m src.orchestration.run_scalability --algorithm MLDSA_87 --volumes 1000 5000 10000

# Análise mais granular
python -m src.orchestration.run_scalability --algorithm Krypton --volumes 500 1000 2000 4000 8000

# Com seed customizado para reprodutibilidade
python -m src.orchestration.run_scalability --algorithm MLKEM_1024 --volumes 1000 5000 --seed 12345
```

Cada execução:
- Gera relatórios individuais para cada volume
- Cria relatório comparativo com métricas agregadas
- Produz 3 gráficos comparativos: CPU, Memória, Combinado (normalizado)
- Analisa complexidade algorítmica O(n)

Saída esperada:
```text
docs/results/
├── MLDSA_87/
│   ├── MLDSA_87 - <timestamp1>.md       # Volume 1000
│   ├── MLDSA_87 - <timestamp2>.md       # Volume 5000
│   ├── MLDSA_87 - <timestamp3>.md       # Volume 10000
│   └── ... (gráficos .png)
└── scalability/
    ├── MLDSA_87_scalability - <timestamp>.md
    ├── MLDSA_87_scalability_cpu_comparison.png
    ├── MLDSA_87_scalability_memory_comparison.png
    └── MLDSA_87_scalability_combined_comparison.png
```

## Ajustar Parâmetros
- Editar `src/orchestration/config.py`
- `DEFAULT_VOLUME`: Volume padrão para execuções
- `SEED`: Seed global para reprodutibilidade
- `RESULTS_DIR`: Diretório de saída dos relatórios

## Testes (TDD)
1. Rodar testes iniciais (devem falhar antes da implementação):
```bash
pytest -q
```
2. Implementar funções até ficarem verdes.

## Relatório
- Tabela com métricas (tabulate)
- Gráficos (matplotlib) salvando arquivos `.png` referenciados no Markdown
- Metadados de hardware (py-cpuinfo, psutil)

## Neutralidade
- Não alterar parâmetros internos dos algoritmos quantCrypt; apenas orquestração externa.

## Reprodutibilidade
- Seed definido em `config.py` (quando aplicável).
- Hardware snapshot armazenado uma vez por execução.

## Scripts de Auditoria e Validação

### Hardware Audit
Gera snapshot do ambiente para reprodutibilidade:
```bash
python scripts/hardware_audit.py --output audit.json
```

Compara com relatórios gerados anteriormente para validar consistência de ambiente.

### Overhead Measurement
Valida que profiling adiciona <10% de overhead (Princípio IV):
```bash
python scripts/measure_overhead.py
```

### Neutrality Check
Verifica que ProfilerManager é usado identicamente em todos os algoritmos:
```bash
python scripts/check_neutrality.py
```

## Exemplos Avançados

### Análise Comparativa entre Algoritmos
```bash
# Executar todos os algoritmos com mesmo volume
python -m src.orchestration.run_single --algorithm MLKEM_1024 --volume 5000 --seed 42
python -m src.orchestration.run_single --algorithm MLDSA_87 --volume 5000 --seed 42
python -m src.orchestration.run_single --algorithm Krypton --volume 5000 --seed 42

# Comparar relatórios manualmente ou processar com parser customizado
```

### Análise de Crescimento Algorítmico
```bash
# Série de volumes com crescimento exponencial
python -m src.orchestration.run_scalability \
  --algorithm MLKEM_1024 \
  --volumes 100 200 400 800 1600 3200 6400 \
  --seed 42

# Relatório comparativo incluirá análise de complexidade O(n)
```

## Próximos Passos
- ✓ Estrutura implementada e testada
- ✓ Métricas coletadas e agregadas
- ✓ Relatórios individuais e comparativos funcionando
- TODO: Integrar API real do quantCrypt nos algoritmos
- TODO: Executar análise completa em ambiente de produção
