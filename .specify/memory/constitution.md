# TI_Cript-Quantum Constitution

## Core Principles

### I. Sem Criptografia Própria
É PROIBIDO implementar, reimplementar ou modificar internamente a lógica de qualquer algoritmo criptográfico. O código só pode orquestrar e configurar execuções de bibliotecas de terceiros estabelecidas. Para algoritmos pós-quânticos, a biblioteca DEVE ser exclusivamente quantCrypt. Para algoritmos clássicos usados como baseline comparativo (ex.: RSA, DSA, Diffie-Hellman), a biblioteca DEVE ser `cryptography`. Nenhuma outra biblioteca criptográfica é permitida sem emenda desta Constituição, e nenhuma dependência pode replicar lógica criptográfica já oferecida por elas.

### II. Instrumentação Externa (INVIOLÁVEL)
Este programa NÃO mede o próprio desempenho. É PROIBIDO em `src/`: profilers (cProfile, line_profiler, memory_profiler), amostradores de sistema (psutil), inventário de hardware (py-cpuinfo), cronometragem interna, análise estatística (numpy, pandas) e geração de relatórios ou gráficos (tabulate, matplotlib). A coleta e a análise de métricas são responsabilidade de programas externos e dedicados, que envolvem este processo. O programa expõe apenas duas superfícies para o mundo externo: a carga de trabalho executada e o código de saída (0 = sucesso, != 0 = falha).

### III. Cargas de Trabalho Neutras e Comparáveis
Cada algoritmo DEVE expor uma função `run_<name>(volume: int)` que executa `volume` ciclos completos e idênticos da operação avaliada, registrada no dicionário `ALGORITHMS` de `src/config.py` — único ponto de extensão. O laço não pode conter lógica de medição, condicionais de ambiente ou trabalho acessório. Procedimentos DEVEM ser idênticos entre algoritmos, exceto pelos desafios e métodos que cada um executa. Otimizações específicas para favorecer um algoritmo são PROIBIDAS.

### IV. TDD Pytest (INVIOLÁVEL)
Antes de qualquer código de implementação, DEVEM existir testes pytest que inicialmente falham (estado vermelho). Cada classe pública e função de orquestração requer ao menos um teste inicial. A sequência Red → Green → Refactor é obrigatória. Não há requisito de cobertura mínima, mas TODO código de produção deve ser exercido por pelo menos um teste funcional ou de integração. Cobertura NÃO pode ser usada como métrica de aceitação (neutralidade experimental).

### V. Reprodutibilidade
Execuções DEVEM: (a) usar seeds fixos onde aplicável, (b) seguir procedimentos idênticos para todos os algoritmos, (c) receber parâmetros de entrada e tamanho de desafio explicitamente pela CLI, sem estado implícito. Não há exigência de número mínimo de execuções, porém cada execução precisa ser rastreável e repetível a partir da linha de comando que a originou. Logs DEVEM ser estruturados (chave=valor) e limitar-se a marcar início e fim das operações.

## Restrições e Escopo

- Linguagem: Python (versão definida no ambiente de execução).
- Bibliotecas criptográficas: quantCrypt para algoritmos pós-quânticos (KEM, DSS, Krypton); `cryptography` para algoritmos clássicos de baseline comparativo (RSA, DSA, Diffie-Hellman). Nenhuma outra biblioteca é permitida sem emenda.
- Domínios de problema: diferentes desafios criptográficos característicos de cada algoritmo (ex.: troca de chaves, assinatura, encapsulamento de segredo), tanto pós-quânticos quanto clássicos.
- Dependências: estritamente as necessárias para executar os algoritmos e os testes. Dependências de medição, análise ou visualização são PROIBIDAS (Princípio II).
- Este programa não escreve arquivos de saída. Armazenamento e formato de resultados são decisão do programa externo de coleta.
- Proibido: implementação manual de algoritmos; instrumentação embutida.

## Fluxo de Desenvolvimento e Qualidade

1. Definir objetivo de avaliação (problema criptográfico + algoritmo).
2. Especificar cenários e preparar testes pytest (falhando).
3. Implementar a carga de trabalho `run_<name>(volume)` e registrá-la em `ALGORITHMS`.
4. Tornar os testes verdes.
5. Revisão pessoal via checklist de princípios (auto-auditoria).

Qualidade: (a) Todos os cinco princípios verificados; (b) Nenhum artefato sem testes; (c) Scripts reexecutáveis; (d) Nenhum vestígio de instrumentação em `src/`.

## Governance

- Precedência: Esta Constituição suplanta práticas ad-hoc.
- Manutenção: Projeto de único mantenedor — responsabilidade total de conformidade e versionamento.
- Verificação Pré-Commit: Checklist interno confirmando cada princípio.
- Politica de Versionamento (SemVer): MAJOR para remoção/redesign de princípio; MINOR para novo princípio/seção ou expansão material; PATCH para ajustes linguísticos e clarificações.
- Processo de Emenda: (1) Propor mudança com justificativa; (2) Atualizar Constituição; (3) Bump de versão conforme regra.
- Conformidade Experimental: Toda nova avaliação deve incluir testes iniciais e uma carga de trabalho registrada em `ALGORITHMS`.
- Ferramentas Permitidas: Somente listadas nas seções de princípios e restrições. Adições requerem emenda (MINOR).
- Neutralidade: Não permitir ajustes de parâmetros que beneficiem seletivamente um algoritmo sem replicar para os demais.
- TODOs: Devem ser resolvidos antes de versão MINOR/Major; PATCH pode conter TODO apenas se não afeta princípios.

**Version**: 3.0.0 | **Ratified**: 2025-11-04 | **Last Amended**: 2026-08-12
