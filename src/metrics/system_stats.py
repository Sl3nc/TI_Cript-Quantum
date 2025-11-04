"""
Estatísticas de sistema (CPU, processos) usando psutil.
"""
import psutil
from dataclasses import dataclass
from typing import Optional
import time
import logging

logger = logging.getLogger(__name__)


@dataclass
class SystemStatSample:
    """Amostra de estatísticas de sistema em um ponto no tempo."""
    timestamp: float
    cpu_percent: float
    memory_percent: float
    cpu_cycles: Optional[int] = None  # Placeholder para contador de ciclos
    cache_misses: Optional[int] = None  # Placeholder para cache misses


class SystemSampler:
    """
    Amostrador contínuo de estatísticas de sistema.
    """
    
    def __init__(self):
        self.process = psutil.Process()
        self.samples = []
        self._sampling = False
        
    def start(self):
        """Inicia amostragem."""
        self._sampling = True
        self.samples = []
        
    def sample(self) -> SystemStatSample:
        """
        Coleta uma amostra de estatísticas.
        
        Returns:
            SystemStatSample com métricas atuais
        """
        return SystemStatSample(
            timestamp=time.time(),
            cpu_percent=self.process.cpu_percent(interval=None),
            memory_percent=self.process.memory_percent(),
            cpu_cycles=None,  # TODO: implementar contador de ciclos
            cache_misses=None  # TODO: implementar contador de cache
        )
        
    def stop(self) -> dict:
        """
        Para amostragem e agrega resultados.
        
        Returns:
            Dict com métricas agregadas
        """
        self._sampling = False
        
        if not self.samples:
            return {
                "cpu_percent_avg": 0.0,
                "memory_percent_max": 0.0,
                "cpu_cycles": None,
                "cache_misses": None
            }
        
        # Fallback: cpu_cycles e cache_misses retornam None quando não disponíveis
        cpu_cycles_available = False  # TODO: implementar detecção de contador
        cache_misses_available = False  # TODO: implementar detecção de contador
        
        if not cpu_cycles_available:
            logger.warning("metric=cpu_cycles status=unavailable fallback=None")
        if not cache_misses_available:
            logger.warning("metric=cache_misses status=unavailable fallback=None")
        
        avg_cpu = sum(s.cpu_percent for s in self.samples) / len(self.samples)
        max_mem = max(s.memory_percent for s in self.samples)
        
        logger.info(f"action=system_stats_aggregated samples={len(self.samples)} cpu_avg={avg_cpu:.2f} mem_max={max_mem:.2f}")
        
        return {
            "cpu_percent_avg": avg_cpu,
            "memory_percent_max": max_mem,
            "cpu_cycles": None,  # Fallback
            "cache_misses": None  # Fallback
        }
