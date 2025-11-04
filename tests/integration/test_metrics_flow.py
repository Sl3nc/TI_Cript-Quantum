"""
Teste de integração do fluxo completo de métricas.
"""
import pytest
from src.metrics import ProfilerManager


def test_profiler_manager_complete_flow():
    """
    Testa fluxo completo: start → execução → stop → métricas coletadas.
    
    Este teste valida integração entre CPU, memória, sistema, hardware.
    """
    manager = ProfilerManager()
    
    # Função de teste
    def workload():
        data = []
        for i in range(10000):
            data.append(i ** 2)
        return sum(data)
    
    # Fluxo completo
    result = manager.profile_function(workload)
    
    # Estrutura esperada
    assert "result" in result
    assert "metrics" in result
    
    # Resultado da função
    assert result["result"] == sum(i ** 2 for i in range(10000))
    
    # Métricas devem conter todas as categorias
    metrics = result["metrics"]
    assert "cpu_metrics" in metrics
    assert "system_metrics" in metrics
    assert "hardware_info" in metrics
    assert "memory_metrics" in metrics
    
    # CPU metrics
    cpu = metrics["cpu_metrics"]
    assert "cpu_time_ms" in cpu
    # TODO: Implementação placeholder retorna 0, deve falhar quando real
    
    # System metrics
    system = metrics["system_metrics"]
    assert "cpu_percent_avg" in system
    assert "memory_percent_max" in system
    
    # Hardware info
    hw = metrics["hardware_info"]
    assert "cpu_brand" in hw or "warning_logged" in hw
    
    # Memory metrics
    mem = metrics["memory_metrics"]
    assert "memory_mb" in mem
    assert mem["memory_mb"] > 0, "Deve capturar uso de memória real"


def test_profiler_manager_neutrality():
    """
    Verifica que ProfilerManager aplica mesma instrumentação independente da carga.
    
    Princípio II da Constituição: métricas padronizadas.
    """
    manager1 = ProfilerManager()
    manager2 = ProfilerManager()
    
    def fast_workload():
        return sum(range(100))
    
    def slow_workload():
        return sum(range(100000))
    
    result1 = manager1.profile_function(fast_workload)
    result2 = manager2.profile_function(slow_workload)
    
    # Ambos devem ter mesma estrutura de métricas
    assert set(result1["metrics"].keys()) == set(result2["metrics"].keys())
    assert set(result1["metrics"]["cpu_metrics"].keys()) == set(result2["metrics"]["cpu_metrics"].keys())
    
    # Valores devem ser diferentes (workload diferente)
    # TODO: Quando implementação real, validar tempos diferentes


def test_profiler_manager_handles_exceptions():
    """Verifica comportamento quando função perfilada lança exceção."""
    manager = ProfilerManager()
    
    def failing_workload():
        raise ValueError("Test exception")
    
    # Deve propagar exceção mas garantir cleanup
    with pytest.raises(ValueError, match="Test exception"):
        manager.profile_function(failing_workload)
    
    # TODO: Verificar se profilers foram parados corretamente (cleanup)
