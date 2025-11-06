"""
Estatísticas de sistema (CPU, processos) usando psutil.
"""
import psutil
from dataclasses import dataclass
from typing import Optional, Dict
import time
import logging
import platform
import os

logger = logging.getLogger(__name__)

# Tentar importar bibliotecas de performance
_perf_available = False
_perf_counters = None

try:
    if platform.system() == "Linux":
        import perf
        _perf_available = True
        logger.info("perf counters available on Linux")
except ImportError:
    logger.debug("perf module not available, using fallback counters")

# Fallback: usar ctypes para acessar QueryPerformanceCounter no Windows
_windows_perf_available = False
if platform.system() == "Windows":
    try:
        import ctypes
        from ctypes import wintypes
        
        kernel32 = ctypes.windll.kernel32
        _qpc_freq = wintypes.LARGE_INTEGER()
        kernel32.QueryPerformanceFrequency(ctypes.byref(_qpc_freq))
        _windows_perf_available = True
        logger.info("Windows performance counters available")
    except Exception as e:
        logger.debug(f"Windows performance counters not available: {e}")


@dataclass
class SystemStatSample:
    """Amostra de estatísticas de sistema em um ponto no tempo."""
    timestamp: float
    cpu_percent: float
    memory_percent: float
    cpu_cycles: Optional[int] = None


def _get_windows_cycles() -> Optional[int]:
    """Obtém contagem de ciclos no Windows usando QueryPerformanceCounter."""
    if not _windows_perf_available:
        return None
    try:
        counter = wintypes.LARGE_INTEGER()
        kernel32.QueryPerformanceCounter(ctypes.byref(counter))
        return counter.value
    except Exception as e:
        logger.debug(f"Failed to get Windows performance counter: {e}")
        return None


def _get_linux_perf_counters() -> Dict[str, Optional[int]]:
    """Obtém contadores de performance no Linux usando perf."""
    if not _perf_available:
        return {"cpu_cycles": None}
    
    try:
        # Tentar criar contadores perf
        cycle_counter = perf.perf_counter(perf.PERF_TYPE_HARDWARE, perf.PERF_COUNT_HW_CPU_CYCLES)
        
        cycle_counter.enable()
        cycles = cycle_counter.read()
        cycle_counter.disable()
        
        return {"cpu_cycles": cycles}
    except Exception as e:
        logger.debug(f"Failed to read perf counters: {e}")
        return {"cpu_cycles": None}


class SystemSampler:
    """
    Amostrador contínuo de estatísticas de sistema.
    """
    
    def __init__(self):
        self.process = psutil.Process()
        self.samples = []
        self._sampling = False
        self._start_cycles = None
        self._perf_counters = None
        
        # Inicializar contadores de performance para Linux
        if _perf_available:
            try:
                self._perf_counters = {
                    'cycles': perf.perf_counter(perf.PERF_TYPE_HARDWARE, perf.PERF_COUNT_HW_CPU_CYCLES)
                }
                logger.info("Perf counters initialized for Linux")
            except Exception as e:
                logger.warning(f"Failed to initialize perf counters: {e}")
                self._perf_counters = None
        
    def start(self):
        """Inicia amostragem."""
        self._sampling = True
        self.samples = []
        
        # Capturar estado inicial dos contadores
        if platform.system() == "Windows" and _windows_perf_available:
            self._start_cycles = _get_windows_cycles()
        elif _perf_available and self._perf_counters:
            try:
                self._perf_counters['cycles'].enable()
                self._start_cycles = self._perf_counters['cycles'].read()
            except Exception as e:
                logger.warning(f"Failed to start perf counters: {e}")
                self._start_cycles = None
        
    def sample(self) -> SystemStatSample:
        """
        Coleta uma amostra de estatísticas.
        
        Returns:
            SystemStatSample com métricas atuais
        """
        cpu_cycles = None
        
        # Obter ciclos de CPU
        if platform.system() == "Windows" and _windows_perf_available:
            current_cycles = _get_windows_cycles()
            if current_cycles and self._start_cycles:
                cpu_cycles = current_cycles - self._start_cycles
        elif _perf_available and self._perf_counters:
            try:
                current_cycles = self._perf_counters['cycles'].read()
                if current_cycles and self._start_cycles:
                    cpu_cycles = current_cycles - self._start_cycles
            except Exception as e:
                logger.debug(f"Failed to read perf counters in sample: {e}")
        
        return SystemStatSample(
            timestamp=time.time(),
            cpu_percent=self.process.cpu_percent(interval=None),
            memory_percent=self.process.memory_percent(),
            cpu_cycles=cpu_cycles
        )
        
    def stop(self) -> dict:
        """
        Para amostragem e agrega resultados.
        
        Returns:
            Dict com métricas agregadas
        """
        self._sampling = False
        
        # Parar contadores perf se estiverem ativos
        if _perf_available and self._perf_counters:
            try:
                self._perf_counters['cycles'].disable()
            except Exception as e:
                logger.debug(f"Failed to disable perf counters: {e}")
        
        if not self.samples:
            return {
                "cpu_percent_avg": 0.0,
                "memory_percent_max": 0.0,
                "cpu_cycles": None
            }
        
        # Calcular médias e máximos
        avg_cpu = sum(s.cpu_percent for s in self.samples) / len(self.samples)
        max_mem = max(s.memory_percent for s in self.samples)
        
        # Agregar ciclos de CPU
        cycles_samples = [s.cpu_cycles for s in self.samples if s.cpu_cycles is not None]
        cpu_cycles = max(cycles_samples) if cycles_samples else None
        
        # Log de disponibilidade
        if cpu_cycles is None:
            logger.warning("metric=cpu_cycles status=unavailable fallback=None")
        else:
            logger.info(f"metric=cpu_cycles value={cpu_cycles}")
        
        logger.info(f"action=system_stats_aggregated samples={len(self.samples)} cpu_avg={avg_cpu:.2f} mem_max={max_mem:.2f}")
        
        return {
            "cpu_percent_avg": avg_cpu,
            "memory_percent_max": max_mem,
            "cpu_cycles": cpu_cycles
        }
