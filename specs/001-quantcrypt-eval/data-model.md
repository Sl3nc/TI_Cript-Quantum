# Data Model: Avaliação de Métricas Pós-Quânticas quantCrypt

## Entity: AlgorithmEvaluation
| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| id | str | Unique identifier (timestamp + algo) | Non-empty, unique |
| algorithm | enum(str) | MLKEM_1024, MLDSA_87, Krypton | MUST be one of set |
| challenge_type | str | Descrição do desafio (encapsulação, assinatura, cifragem) | Non-empty |
| volume | int | Número de operações configurado | >0 |
| started_at | datetime | Início execução | <= ended_at |
| ended_at | datetime | Fim execução | >= started_at |
| duration_ms | float | Duração total em ms | >=0 |
| status | enum(str) | success, partial, failed | MUST be one of set |
| metrics | list[MetricRecord] | Série temporal/linhas | Non-empty se status=success |
| hardware_profile_id | str | FK to HardwareProfile | Non-empty |
| notes | str | Observações ou erros | Optional |

## Entity: MetricRecord
| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| ts_offset_ms | float | Tempo desde início | >=0 |
| cpu_time_ms | float | Tempo acumulado CPU | >=0 |
| memory_mb | float | Memória utilizada | >=0 |
| cpu_cycles | int | Ciclos CPU (estimativa/coleta) | >=0 or null fallback |
| cpu_percent | float | Percentual de uso CPU processo | 0-100 |

## Entity: HardwareProfile
| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| id | str | Hash baseado em hostname + arquitetura | Unique |
| architecture | str | Arquitetura CPU | Non-empty |
| cores_physical | int | Núcleos físicos | >0 |
| cores_logical | int | Núcleos lógicos | >= cores_physical |
| max_freq_mhz | float | Frequência máxima | >0 or null if unavailable |
| python_version | str | Versão Python | Non-empty |
| quantcrypt_version | str | Versão quantCrypt | Non-empty |
| os_name | str | Nome do sistema operacional | Non-empty |

## Entity: EvaluationReport
| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| id | str | Unique (match AlgorithmEvaluation id) | Unique |
| algorithm | str | Copiado da avaliação | Non-empty |
| path | str | Caminho do arquivo Markdown | Exists after write |
| volume | int | Volume avaliado | >0 |
| summary | str | Texto explicativo | Non-empty |
| table_markdown | str | Tabela de métricas | Non-empty |
| graphs | list[str] | Paths para imagens geradas | Non-empty |
| hardware_profile_id | str | FK | Non-empty |
| created_at | datetime | Momento geração | Non-empty |

## Entity: ScalabilitySeries
| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| id | str | Unique (algo + lista volumes + timestamp) | Unique |
| algorithm | str | Algoritmo alvo | Non-empty |
| volumes | list[int] | Volumes testados | All >0 |
| evaluation_ids | list[str] | IDs das avaliações individuais | Length==len(volumes) |
| comparative_report_path | str | Caminho relatório comparativo | Exists after write |
| metrics_aggregate | dict | Agregados (médias, picos) | Keys: time_mean, mem_peak, cycles_per_op |

## Relationships
- AlgorithmEvaluation.hardware_profile_id → HardwareProfile.id
- EvaluationReport.hardware_profile_id → HardwareProfile.id
- ScalabilitySeries.evaluation_ids → AlgorithmEvaluation.id (one-to-many collection)

## State Transitions (AlgorithmEvaluation)
| State | Event | Next State | Notes |
|-------|-------|------------|-------|
| pending | start() | running | Initialize timers and hardware snapshot |
| running | complete() | success | All metrics collected; final aggregation |
| running | error_partial() | partial | Aborts gracefully; preserves collected subset |
| running | error_fatal() | failed | Minimal data persisted for debugging |

## Validation Rules
- volume MUST be >0.
- success evaluations MUST contain >=1 MetricRecord.
- timestamps MUST ensure started_at <= ended_at.
- uniqueness enforced by id pattern `<ALG>-<TIMESTAMP_MS>`.

## Notes
Este modelo é lógico; implementação em Python utilizará classes ou dataclasses, persistência somente em arquivos Markdown + imagens + possivelmente JSON auxiliar para reutilização.
