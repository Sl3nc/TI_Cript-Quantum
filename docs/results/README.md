# Results Directory

Este diretório contém relatórios de avaliação gerados pelo sistema de métricas pós-quânticas.

## Estrutura de Arquivos

Os relatórios são organizados por algoritmo:

```text
docs/results/
├── MLKEM_1024/
│   ├── MLKEM_1024 - 04-11-2025 14h30m15s.123.md
│   ├── MLKEM_1024 - 04-11-2025 14h30m15s.123_cpu_time.png
│   ├── MLKEM_1024 - 04-11-2025 14h30m15s.123_memory_usage.png
│   └── ...
├── MLDSA_87/
│   ├── MLDSA_87 - 04-11-2025 15h20m30s.456.md
│   └── ...
├── Krypton/
│   ├── Krypton - 04-11-2025 16h10m45s.789.md
│   └── ...
└── scalability/
    ├── MLKEM_1024_scalability - 04-11-2025 17h00m00s.000.md
    ├── MLKEM_1024_scalability_cpu_comparison.png
    ├── MLKEM_1024_scalability_memory_comparison.png
    └── ...
```

## Convenção de Nomenclatura

### Relatórios Individuais

Formato: `<Algoritmo> - <timestamp>.md`

- **Algoritmo**: Nome do algoritmo avaliado (MLKEM_1024, MLDSA_87, Krypton)
- **Timestamp**: Formato PT-BR `DD-MM-YYYY HHhMMmSSs.mmm`
  - Dia-Mês-Ano Hora-Minuto-Segundo.Milissegundos
  - Exemplo: `04-11-2025 14h30m15s.123`

### Gráficos Individuais

Formato: `<Algoritmo> - <timestamp>_<métrica>.png`

Métricas disponíveis:
- `cpu_time`: Tempo de CPU ao longo das iterações
- `memory_usage`: Uso de memória ao longo das iterações

### Relatórios de Escalabilidade

Formato: `<Algoritmo>_scalability - <timestamp>.md`

### Gráficos Comparativos

Formato: `<Algoritmo>_scalability_<tipo>_comparison.png`

Tipos de comparação:
- `cpu_comparison`: Tempo de CPU por volume
- `memory_comparison`: Memória por volume
- `combined_comparison`: Métricas normalizadas combinadas

## Conteúdo dos Relatórios

### Relatórios Individuais (.md)

Cada relatório inclui:

1. **Metadados de Execução**
   - Algoritmo avaliado
   - Volume de operações
   - Timestamp de execução
   - Seed utilizado

2. **Informações de Hardware**
   - CPU (modelo, arquitetura, frequência, núcleos)
   - Memória (total, disponível)
   - Sistema operacional

3. **Métricas Coletadas**
   - Tempo de CPU (segundos)
   - Uso de Memória (MB)
   - Ciclos de CPU (quando disponível)
   - Cache Misses (quando disponível)

4. **Gráficos Incorporados**
   - Série temporal de CPU
   - Série temporal de memória

### Relatórios de Escalabilidade (.md)

Relatórios comparativos incluem:

1. **Resumo Executivo**
   - Volumes avaliados
   - Status de cada execução
   - Taxa de sucesso

2. **Métricas Agregadas**
   - Médias por volume
   - Desvios padrão
   - Valores de pico

3. **Análise de Complexidade**
   - Estimativa de ordem de crescimento O(n)
   - Tendências observadas

4. **Resultados por Volume**
   - Breakdown detalhado de cada volume
   - Referências a relatórios individuais

5. **Gráficos Comparativos**
   - Comparação de CPU entre volumes
   - Comparação de memória entre volumes
   - Visualização combinada normalizada

## Unicidade e Colisões

O sistema garante unicidade de nomes através de:

1. **Precisão de Milissegundos**: Timestamps incluem 3 casas decimais
2. **Detecção de Colisão**: Se arquivo já existe, adiciona sufixo numérico
   - Exemplo: `MLKEM_1024 - 04-11-2025 14h30m15s.123_2.md`

## Reprodutibilidade

Para reproduzir resultados:

1. Execute `python scripts/hardware_audit.py --output audit.json` para capturar ambiente
2. Use o mesmo seed especificado no relatório
3. Consulte seção "Informações de Hardware" do relatório para configuração esperada
4. Compare hash de ambiente com `audit.json` gerado

## Auditoria

Para validar integridade dos relatórios:

```bash
# Gerar snapshot de ambiente atual
python scripts/hardware_audit.py --output current_audit.json

# Comparar com ambiente de execução original
# (hash presente no relatório vs hash em current_audit.json)
```

## Análise de Dados

Os relatórios Markdown podem ser processados para análise adicional:

```python
import pandas as pd
import glob

# Carregar múltiplos relatórios
reports = glob.glob("docs/results/MLKEM_1024/*.md")

# Parser customizado pode extrair métricas de tabelas
# para análise estatística mais profunda
```

## Manutenção

- **Limpeza**: Relatórios antigos podem ser arquivados periodicamente
- **Backup**: Recomenda-se versionar relatórios importantes
- **Espaço**: Gráficos PNG (300 DPI) ocupam ~50-200 KB cada
