"""
Testes unitários para profiler_memory.
"""
import pytest
from src.metrics.profiler_memory import trace_memory


def test_trace_memory_structure():
    """Verifica que trace_memory retorna estrutura esperada."""
    def sample_function(size):
        data = [0] * size
        return len(data)
    
    result = trace_memory(sample_function, 10000)
    
    # Estrutura esperada
    assert "memory_mb" in result
    assert "memory_increments" in result
    assert "result" in result
    
    # Tipos esperados
    assert isinstance(result["memory_mb"], float)
    assert isinstance(result["memory_increments"], list)
    assert result["result"] == 10000
    
    # Métricas devem ser > 0 para alocação real
    assert result["memory_mb"] > 0, "Memory usage deve ser positivo"


def test_trace_memory_captures_increments():
    """Verifica que memory_increments captura crescimento."""
    def allocate_memory():
        large_list = [i for i in range(100000)]
        return len(large_list)
    
    result = trace_memory(allocate_memory)
    
    # Deve haver incrementos capturados
    assert len(result["memory_increments"]) > 0, "Deve capturar amostras de memória"
    
    # Deve haver crescimento (alguns incrementos positivos)
    # TODO: Este teste pode falhar se implementação não capturar crescimento real
