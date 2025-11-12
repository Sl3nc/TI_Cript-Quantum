"""
Módulos de coleta e processamento de métricas.
"""
from typing import Dict, Any, Callable
from .cpu import CPU
from .memory import Memory
from ..system_sampler import SystemSampler
from ..hardware import Hardware

class Profiler:
    """
    Orquestrador de profiling garantindo neutralidade entre algoritmos.
    
    Aplica instrumentação idêntica a MLKEM_1024, MLDSA_87, Krypton seguindo
    Princípio II da Constituição: métricas padronizadas.
    """
    
    def __init__(self):
        self.profilerCPU = CPU()
        self.cpu_profiler = None
        self.system_sampler = SystemSampler()
        self.hardware_info = None
        
    def _start(self) -> None:
        """Inicia todos os profilers."""
        self.cpu_profiler = self.profilerCPU.start()
        self.hardware_info = Hardware().snapshot_hardware()
        self.system_sampler.start()
        
    def _stop(self) -> Dict[str, Any]:
        """
        Para todos os profilers e coleta métricas.
        
        Returns:
            Dict com:
                - cpu_metrics: dict (tempo, chamadas)
                - system_metrics: dict (CPU%, memória%)
                - hardware_info: dict (CPU, RAM, etc)
        """
        cpu_metrics = self.profilerCPU.stop(self.cpu_profiler) if self.cpu_profiler else {}
        system_metrics = self.system_sampler.stop()
        
        return {
            "cpu_metrics": cpu_metrics,
            "system_metrics": system_metrics,
            "hardware_info": self.hardware_info or {}
        }
    
    def execution(self, func: Callable, *args, **kwargs) -> Dict[str, Any]:
        """
        Perfila uma função completa com todas as métricas.
        
        Args:
            func: Função a perfilar (run_mlkem, generate_and_sign, cipher_rounds)
            *args, **kwargs: Argumentos da função
            
        Returns:
            Dict com:
                - result: Any (retorno da função)
                - metrics: dict (todas as métricas coletadas)
        """
        self._start()

        # Executa com trace de memória
        memory_result = Memory().trace(func, *args, **kwargs)

        metrics = self._stop()
        metrics["memory_metrics"] = {
            "memory_mb": memory_result["peak_memory"],
            "memory_increments": memory_result["memory_increments"]
        }
        
        return metrics
