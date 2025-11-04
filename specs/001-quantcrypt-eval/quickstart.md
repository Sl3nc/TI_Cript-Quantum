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

## Executar Série Escalável
```bash
python -m src.orchestration.run_scalability --algorithm MLDSA_87 --volumes 1000 5000 10000
```
Gera relatórios individuais + comparativo.

## Ajustar Parâmetros
- Editar `src/orchestration/config.py`

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

## Próximos Passos
- Implementar esqueleto de módulos e testes falhando.
- Criar script de coleta sequencial de métricas.
