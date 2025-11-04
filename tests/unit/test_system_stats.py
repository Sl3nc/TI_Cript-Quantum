"""
Testes unitários para system_stats.
"""
import pytest
import time
from src.metrics.system_stats import SystemSampler, SystemStatSample


def test_system_sampler_start():
    """Verifica que SystemSampler pode iniciar."""
    sampler = SystemSampler()
    sampler.start()
    
    assert sampler._sampling is True
    assert len(sampler.samples) == 0


def test_system_sampler_sample_structure():
    """Verifica estrutura de SystemStatSample."""
    sampler = SystemSampler()
    sampler.start()
    
    sample = sampler.sample()
    
    # Verifica campos obrigatórios
    assert hasattr(sample, 'timestamp')
    assert hasattr(sample, 'cpu_percent')
    assert hasattr(sample, 'memory_percent')
    assert hasattr(sample, 'cpu_cycles')
    assert hasattr(sample, 'cache_misses')
    
    # Timestamp deve ser plausível
    assert sample.timestamp > 0
    
    # CPU e memória devem ser >= 0
    assert sample.cpu_percent >= 0
    assert sample.memory_percent >= 0
    
    # cpu_cycles e cache_misses são None por enquanto (placeholder)
    assert sample.cpu_cycles is None
    assert sample.cache_misses is None


def test_system_sampler_stop_aggregates():
    """Verifica que stop() agrega métricas."""
    sampler = SystemSampler()
    sampler.start()
    
    # Coleta algumas amostras
    for _ in range(3):
        sampler.samples.append(sampler.sample())
        time.sleep(0.01)
    
    aggregated = sampler.stop()
    
    # Estrutura esperada
    assert "cpu_percent_avg" in aggregated
    assert "memory_percent_max" in aggregated
    assert "cpu_cycles" in aggregated
    assert "cache_misses" in aggregated
    
    # Valores devem ser razoáveis
    assert aggregated["cpu_percent_avg"] >= 0
    assert aggregated["memory_percent_max"] >= 0
    
    # Placeholders
    assert aggregated["cpu_cycles"] is None
    assert aggregated["cache_misses"] is None
    
    # TODO: Teste falhará quando implementarmos contadores reais de ciclos/cache
