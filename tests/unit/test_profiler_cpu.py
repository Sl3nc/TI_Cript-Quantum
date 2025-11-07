"""
Testes unitários para profiler_cpu.
"""
import pytest
from metrics.profile.cpu import start_cpu_profile, stop_cpu_profile, profile_lines


def test_start_cpu_profile_returns_profiler():
    """Verifica que start_cpu_profile retorna objeto profiler."""
    profiler = start_cpu_profile()
    assert profiler is not None
    # Limpar
    profiler.disable()


def test_stop_cpu_profile_structure():
    """Verifica que stop_cpu_profile gera estrutura de métricas esperada."""
    profiler = start_cpu_profile()
    
    # Algum trabalho para perfilar
    _ = sum(range(10000))
    
    metrics = stop_cpu_profile(profiler)
    
    # Estrutura esperada
    assert "cpu_time_ms" in metrics
    assert "cumulative_time_ms" in metrics
    assert "primitive_calls" in metrics
    assert "total_calls" in metrics
    
    # Tipos esperados
    assert isinstance(metrics["cpu_time_ms"], float)
    assert isinstance(metrics["cumulative_time_ms"], float)
    assert isinstance(metrics["primitive_calls"], int)
    assert isinstance(metrics["total_calls"], int)
    
    # TODO: Este teste falhará porque implementação retorna zeros
    # Deve passar após implementar extração real de pstats


def test_profile_lines_placeholder():
    """Verifica estrutura retornada por profile_lines."""
    def sample_function(n):
        return sum(range(n))
    
    result = profile_lines(sample_function, 1000)
    
    assert "line_stats" in result
    assert "result" in result
    assert result["result"] == sum(range(1000))
    
    # TODO: Implementação atual retorna dict vazio para line_stats
    # Deve falhar quando validarmos conteúdo real
