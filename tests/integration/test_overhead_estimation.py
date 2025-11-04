"""
Teste de integração para validação do overhead de profiling.

Valida que overhead medido está dentro dos limites constitucionais (<10%).
"""
import pytest
import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from ...scripts.measure_overhead import measure_baseline, measure_with_profiling


def test_overhead_estimation_within_limits():
    """
    Valida que overhead de profiling é < 10%.
    
    CONSTITUIÇÃO Princípio IV: overhead < 10%
    """
    iterations = 5  # Fewer iterations for test speed
    
    baseline_avg = measure_baseline(iterations)
    profiled_avg = measure_with_profiling(iterations)
    
    assert baseline_avg > 0, "Baseline deve ter tempo mensurável"
    assert profiled_avg > 0, "Profiled deve ter tempo mensurável"
    
    overhead_pct = ((profiled_avg - baseline_avg) / baseline_avg) * 100
    
    assert overhead_pct < 10, (
        f"Overhead {overhead_pct:.2f}% excede limite de 10% "
        f"(baseline={baseline_avg:.2f}ms, profiled={profiled_avg:.2f}ms)"
    )


def test_overhead_measurement_consistency():
    """
    Valida que múltiplas medições de overhead são consistentes.
    """
    iterations = 3
    
    measurements = []
    for _ in range(3):
        baseline = measure_baseline(iterations)
        profiled = measure_with_profiling(iterations)
        overhead_pct = ((profiled - baseline) / baseline) * 100
        measurements.append(overhead_pct)
    
    # Verifica que todas medições estão abaixo do limite
    for measurement in measurements:
        assert measurement < 10, f"Measurement {measurement:.2f}% exceeds limit"
    
    # Verifica consistência (desvio padrão razoável)
    import statistics
    if len(measurements) > 1:
        stdev = statistics.stdev(measurements)
        assert stdev < 5, f"Overhead measurements too inconsistent (stdev={stdev:.2f}%)"


def test_profiling_adds_measurable_overhead():
    """
    Valida que profiling adiciona overhead detectável (sanity check).
    
    Se overhead for 0%, pode indicar que profiling não está ativo.
    """
    baseline_avg = measure_baseline(5)
    profiled_avg = measure_with_profiling(5)
    
    # Profiling deve adicionar algum overhead (>0.1%)
    overhead_pct = ((profiled_avg - baseline_avg) / baseline_avg) * 100
    
    assert overhead_pct > 0.1, (
        "Overhead muito baixo pode indicar que profiling não está funcionando"
    )
