"""
Testes unitários para aggregate_series.
"""
import pytest


def test_aggregate_series_calculates_averages():
    """Verifica cálculo de médias através de múltiplas avaliações."""
    from metrics.aggregator import aggregate_series
    
    evaluations = [
        {
            "volume": 100,
            "metrics": {"cpu_time_ms": 50.0, "memory_mb": 10.0},
            "status": "success"
        },
        {
            "volume": 500,
            "metrics": {"cpu_time_ms": 200.0, "memory_mb": 40.0},
            "status": "success"
        },
        {
            "volume": 1000,
            "metrics": {"cpu_time_ms": 400.0, "memory_mb": 80.0},
            "status": "success"
        }
    ]
    
    result = aggregate_series(evaluations)
    
    # Estrutura esperada
    assert "cpu_time_avg_ms" in result
    assert "cpu_time_std_ms" in result
    assert "memory_peak_mb" in result
    assert "volumes" in result
    assert "success_rate" in result
    
    # Média CPU: (50 + 200 + 400) / 3 = 216.67
    assert abs(result["cpu_time_avg_ms"] - 216.67) < 1.0, "Média CPU incorreta"
    
    # Pico memória: max(10, 40, 80) = 80
    assert result["memory_peak_mb"] == 80.0, "Pico memória incorreto"
    
    # Volumes testados
    assert result["volumes"] == [100, 500, 1000]
    
    # Success rate: 3/3 = 1.0
    assert result["success_rate"] == 1.0


def test_aggregate_series_handles_failures():
    """Verifica cálculo de success_rate com falhas."""
    from metrics.aggregator import aggregate_series
    
    evaluations = [
        {"status": "success", "volume": 100, "metrics": {"cpu_time_ms": 50.0, "memory_mb": 10.0}},
        {"status": "failed", "volume": 500, "metrics": {}, "notes": "timeout"},
        {"status": "success", "volume": 1000, "metrics": {"cpu_time_ms": 400.0, "memory_mb": 80.0}},
        {"status": "partial", "volume": 5000, "metrics": {"cpu_time_ms": 1800.0, "memory_mb": 350.0}}
    ]
    
    result = aggregate_series(evaluations)
    
    # Success rate: 2 success / 4 total = 0.5
    # (partial não conta como success)
    assert result["success_rate"] == 0.5, "Success rate com falhas incorreto"
    
    # Agregados devem considerar apenas avaliações bem-sucedidas
    # Média CPU: (50 + 400) / 2 = 225
    assert abs(result["cpu_time_avg_ms"] - 225.0) < 1.0


def test_aggregate_series_calculates_std_deviation():
    """Verifica cálculo de desvio padrão."""
    from metrics.aggregator import aggregate_series
    
    evaluations = [
        {"status": "success", "volume": 100, "metrics": {"cpu_time_ms": 100.0, "memory_mb": 20.0}},
        {"status": "success", "volume": 500, "metrics": {"cpu_time_ms": 200.0, "memory_mb": 40.0}},
        {"status": "success", "volume": 1000, "metrics": {"cpu_time_ms": 300.0, "memory_mb": 60.0}}
    ]
    
    result = aggregate_series(evaluations)
    
    # Desvio padrão deve ser > 0 para dados variados
    assert result["cpu_time_std_ms"] > 0, "Desvio padrão deve ser positivo"
    
    # Para [100, 200, 300]: std ≈ 81.65 (population std)
    # ou ≈ 100 (sample std)
    assert 50 < result["cpu_time_std_ms"] < 150, "Desvio padrão fora do esperado"


def test_aggregate_series_empty_list():
    """Verifica comportamento com lista vazia."""
    from metrics.aggregator import aggregate_series
    
    result = aggregate_series([])
    
    # Deve retornar estrutura com valores padrão
    assert result["cpu_time_avg_ms"] == 0.0
    assert result["success_rate"] == 0.0
    assert result["volumes"] == []
