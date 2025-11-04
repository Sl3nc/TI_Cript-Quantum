# Contracts: Interfaces Internas

## Overview
Não há API externa de rede; contratos definem funções públicas por módulo para uso interno e testes.

## algorithms/mlkem_kem.py
```text
run_mlkem(volume: int, profiler: ProfilerManager, reporter: ReportBuilder) -> AlgorithmEvaluation
```
- Gera pares de chaves, encapsula e decapsula secret repetidamente.

## algorithms/mldsa_dss.py
```text
generate_and_sign(volume: int, profiler: ProfilerManager, reporter: ReportBuilder) -> AlgorithmEvaluation
```
- Gera chaves, assina mensagem de teste, verifica assinatura.

## algorithms/krypton_cipher.py
```text
cipher_rounds(volume: int, profiler: ProfilerManager, reporter: ReportBuilder) -> AlgorithmEvaluation
```
- Criptografa e descriptografa blocos.

## metrics/profiler_cpu.py
```text
start_cpu_profile(label: str) -> None
stop_cpu_profile(label: str) -> CpuProfileResult
profile_lines(func, *args, **kwargs) -> LineProfileResult
```

## metrics/profiler_memory.py
```text
trace_memory() -> MemoryTraceContext
```

## metrics/system_stats.py
```text
sample_system(interval_ms: int) -> SystemSampler
SystemSampler.next() -> SystemStatSample
```

## metrics/hardware.py
```text
snapshot_hardware() -> HardwareProfile
```

## metrics/aggregator.py
```text
aggregate(evaluation: AlgorithmEvaluation) -> AggregatedMetrics
aggregate_series(series: ScalabilitySeries) -> SeriesAggregate
```

## metrics/report_markdown.py
```text
build_report(evaluation: AlgorithmEvaluation, aggregated: AggregatedMetrics) -> EvaluationReport
build_series_report(series: ScalabilitySeries, aggregates: SeriesAggregate) -> EvaluationReport
```

## metrics/plotting.py
```text
plot_time_series(evaluation: AlgorithmEvaluation) -> str
plot_memory_series(evaluation: AlgorithmEvaluation) -> str
plot_scalability(series: ScalabilitySeries, aggregates: SeriesAggregate) -> list[str]
```

## orchestration/run_single.py
```text
run_single(algorithm: str, volume: int) -> EvaluationReport
```

## orchestration/run_scalability.py
```text
run_scalability(algorithm: str, volumes: list[int]) -> EvaluationReport
```

## orchestration/config.py
```text
get_config() -> EvalConfig
```

## Error Handling Contract
- Função deve lançar ValueError se volume <=0.
- Falha de coleta de hardware retorna perfil parcial com campos nulos e warning logado.

## Logging Contract
- Formato chave=valor: `event=metric_sample algo=MLKEM_1024 volume=1000 ts=... mem_mb=... cpu_pct=...`

## Neutralidade
- ProfilerManager aplica instrumentação idêntica independentemente do algoritmo.
