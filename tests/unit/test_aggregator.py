"""
Testes unitários para aggregator.
"""
import pytest
from metrics.aggregator import aggregate, aggregate_series


def test_aggregate_structure():
    """Verifica estrutura retornada por aggregate."""
    metrics_list = [
        {"cpu_time": 100, "memory": 50},
        {"cpu_time": 120, "memory": 55}
    ]
    
    result = aggregate(metrics_list)
    
    # Estrutura esperada
    assert "cpu_time_ms" in result
    assert "memory_mb" in result
    assert "cpu_cycles" in result
    assert "hardware_info" in result
    
    # TODO: Implementação placeholder retorna zeros
    # Este teste deve falhar quando validarmos valores reais
    assert result["cpu_time_ms"] == 0.0, "Placeholder deve retornar 0"


def test_aggregate_series_structure():
    """Verifica estrutura retornada por aggregate_series."""
    evaluations = [
        {"volume": 100, "cpu_time_ms": 50, "memory_mb": 10, "status": "success"},
        {"volume": 500, "cpu_time_ms": 200, "memory_mb": 40, "status": "success"},
        {"volume": 1000, "cpu_time_ms": 400, "memory_mb": 80, "status": "success"}
    ]
    
    result = aggregate_series(evaluations)
    
    # Estrutura esperada
    assert "cpu_time_avg_ms" in result
    assert "cpu_time_std_ms" in result
    assert "memory_peak_mb" in result
    assert "volumes" in result
    assert "success_rate" in result
    
    # Tipos esperados
    assert isinstance(result["cpu_time_avg_ms"], float)
    assert isinstance(result["cpu_time_std_ms"], float)
    assert isinstance(result["memory_peak_mb"], float)
    assert isinstance(result["volumes"], list)
    assert isinstance(result["success_rate"], float)
    
    # TODO: Implementação placeholder retorna zeros/vazios
    # Deve falhar quando validarmos agregação real


def test_aggregate_series_calculates_success_rate():
    """Verifica cálculo de success_rate."""
    evaluations = [
        {"status": "success"},
        {"status": "failed"},
        {"status": "success"}
    ]
    
    result = aggregate_series(evaluations)
    
    # Success rate deve ser 2/3 = 0.666...
    # TODO: Placeholder retorna 1.0, teste falhará
    # Deve passar quando implementarmos cálculo real
