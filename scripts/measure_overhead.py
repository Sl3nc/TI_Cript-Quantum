"""
Script para medir overhead de profiling.

Valida constraint: overhead < 10% conforme Princípio IV da Constituição.
"""
import time
from src.metrics import ProfilerManager


def baseline_workload():
    """Workload de referência sem profiling."""
    data = []
    for i in range(50000):
        data.append(i ** 2)
    return sum(data)


def measure_baseline(iterations: int = 10) -> float:
    """
    Mede tempo baseline sem profiling.
    
    Returns:
        Tempo médio em milissegundos
    """
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        baseline_workload()
        end = time.perf_counter()
        times.append((end - start) * 1000)
    
    return sum(times) / len(times)


def measure_with_profiling(iterations: int = 10) -> float:
    """
    Mede tempo com profiling ativo.
    
    Returns:
        Tempo médio em milissegundos
    """
    times = []
    for _ in range(iterations):
        manager = ProfilerManager()
        start = time.perf_counter()
        manager.profile_function(baseline_workload)
        end = time.perf_counter()
        times.append((end - start) * 1000)
    
    return sum(times) / len(times)


def main():
    """Executa medição e reporta overhead."""
    print("Medindo baseline (sem profiling)...")
    baseline_avg = measure_baseline()
    print(f"  Baseline: {baseline_avg:.2f} ms")
    
    print("\nMedindo com profiling...")
    profiled_avg = measure_with_profiling()
    print(f"  Com profiling: {profiled_avg:.2f} ms")
    
    overhead_ms = profiled_avg - baseline_avg
    overhead_pct = (overhead_ms / baseline_avg) * 100
    
    print(f"\n=== Overhead de Profiling ===")
    print(f"Absoluto: {overhead_ms:.2f} ms")
    print(f"Relativo: {overhead_pct:.2f}%")
    
    if overhead_pct < 10:
        print(f"✓ PASS: Overhead < 10% (Princípio IV OK)")
    else:
        print(f"✗ FAIL: Overhead >= 10% (Princípio IV violado)")
        print("  Revisar instrumentação para reduzir impacto")
    
    return overhead_pct


if __name__ == "__main__":
    main()
