# TI_Cript-Quantum Constitution

## Core Principles

### I. Sem Criptografia Própria
É PROIBIDO implementar, reimplementar ou modificar internamente a lógica de qualquer algoritmo criptográfico. O código de avaliação só pode orquestrar, configurar e medir execuções de bibliotecas de terceiros estabelecidas. Para algoritmos pós-quânticos, a biblioteca DEVE ser exclusivamente quantCrypt. Para algoritmos clássicos usados como baseline comparativo (ex.: RSA, DSA, Diffie-Hellman), a biblioteca DEVE ser `cryptography`. Nenhuma outra biblioteca criptográfica é permitida sem emenda desta Constituição, e nenhuma dependência pode replicar lógica criptográfica já oferecida por elas.

### II. Métricas Padronizadas Multi-Algoritmo
Todos os algoritmos são avaliados sob um conjunto ÚNICO e IMUTÁVEL de métricas: Tempo de CPU, Uso de memória, Ciclos de CPU, Cache misses, Informações de hardware (arquitetura, núcleos, frequência). As medições DEVEM ser coletadas de forma consistente entre execuções e armazenadas com carimbo de data/hora e identificação do algoritmo + problema resolvido. Resultados DEVEM ser publicados em tabelas Markdown usando a biblioteca tabulate. Nenhuma métrica pode ser omitida sem justificativa documentada.

### III. TDD Pytest (INVIOLÁVEL)
Antes de qualquer código de implementação, DEVEM existir testes pytest que inicialmente falham (estado vermelho). Cada classe pública e função de orquestração requer ao menos um teste inicial. A sequência Red → Green → Refactor é obrigatória. Não há requisito de cobertura mínima, mas TODO código de produção deve ser exercido por pelo menos um teste funcional ou de integração. Cobertura NÃO pode ser usada como métrica de aceitação (neutralidade experimental).

### IV. Perfilamento e Observabilidade de Desempenho
Cada sessão de avaliação DEVE instrumentar: cProfile (tempo global), line_profiler (linhas críticas), memory_profiler (picos e crescimento), psutil (uso de CPU/mem/processo), py-cpuinfo (detalhes de hardware). Perfis não podem alterar lógica do algoritmo. Logs DEVEM ser estruturados (chave=valor) e conter data e hora da execução. Hardware é coletado uma vez por série de testes e referenciado nas saídas.

### V. Reprodutibilidade e Neutralidade Experimental
Execuções DEVEM: (a) usar seeds fixos onde aplicável, (b) registrar ambiente (SO, versão Python, versão quantCrypt, versão de `cryptography`), (c) seguir procedimentos idênticos para todos os algoritmos, exceto pelos desafios e métodos que executam, (d) armazenar parâmetros de entrada e tamanho de desafio. Não há exigência de número mínimo de execuções, porém cada execução precisa ser rastreável e repetível. Otimizações específicas para favorecer um algoritmo são PROIBIDAS. Alterações no ambiente DEVEM disparar nova série completa de medições.

## Restrições e Escopo de Avaliação

- Linguagem: Python (versão definida no ambiente de execução). 
- Bibliotecas criptográficas: quantCrypt para algoritmos pós-quânticos (KEM, DSS, Krypton); `cryptography` para algoritmos clássicos de baseline comparativo (RSA, DSA, Diffie-Hellman). Nenhuma outra biblioteca é permitida sem emenda.
- Domínios de problema: diferentes desafios criptográficos característicos de cada algoritmo (ex.: troca de chaves, assinatura, encapsulamento de segredo), tanto pós-quânticos quanto clássicos (usados como baseline comparativo), sempre com métricas padronizadas.
- Dependências para métricas: cProfile, line_profiler, memory_profiler, psutil, py-cpuinfo.
- Dependências para análise estatística: numpy, pandas.
- Dependência para relatório: tabulate (saída Markdown). 
- Armazenamento de resultados: diretório dedicado `output/` (raiz do projeto, não versionado) com tabelas + metadados de ambiente.
- Proibido: implementação manual de algoritmos, uso de ferramentas não declaradas para profilamento criptográfico.

## Fluxo de Desenvolvimento e Qualidade

1. Definir objetivo de avaliação (problema criptográfico + algoritmo).  
2. Especificar cenários e preparar testes pytest (falhando).  
3. Implementar orquestração mínima para tornar testes verdes.  
4. Adicionar camadas de perfilamento (scripts/utilitários).  
5. Executar bateria controlada e coletar métricas.  
6. Consolidar estatísticas (numpy/pandas) e gerar tabela Markdown (tabulate).  
7. Registrar ambiente e hardware.  
8. Revisão pessoal via checklist de princípios (auto-auditoria).  

Qualidade: (a) Todas as cinco princípios verificados; (b) Nenhum artefato sem testes; (c) Scripts reexecutáveis; (d) Saída tabular legível e completa.

## Governance

- Precedência: Esta Constituição suplanta práticas ad-hoc. 
- Manutenção: Projeto de único mantenedor — responsabilidade total de conformidade e versionamento. 
- Verificação Pré-Commit: Checklist interno confirmando cada princípio. 
- Politica de Versionamento (SemVer): MAJOR para remoção/redesign de princípio; MINOR para novo princípio/seção ou expansão material; PATCH para ajustes linguísticos e clarificações. 
- Processo de Emenda: (1) Propor mudança com justificativa; (2) Atualizar Constituição; (3) Bump de versão conforme regra. 
- Conformidade Experimental: Toda nova avaliação deve incluir: testes iniciais, script de perfilamento, tabela de resultados, metadados de ambiente. 
- Ferramentas Permitidas: Somente listadas nas seções de princípios e restrições. Adições requerem emenda (MINOR). 
- Neutralidade: Não permitir ajustes de parâmetros que beneficiem seletivamente um algoritmo sem replicar para os demais. 
- Auditoria Interna: Relatório simples (Markdown) anexado aos resultados listando hashes de scripts e versões de dependências. 
- TODOs: Devem ser resolvidos antes de versão MINOR/Major; PATCH pode conter TODO apenas se não afeta princípios.

**Version**: 2.0.0 | **Ratified**: 2025-11-04 | **Last Amended**: 2026-08-12

