"""
Módulos de coleta e processamento de métricas.
"""
from typing import Dict, Any, Callable
from .cpu import CPU
from .memory import Memory
from ..system_sampler import SystemSampler
from ..hardware import Hardware

class ProfilerManager:
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
        
    def start_profiling(self) -> None:
        """Inicia todos os profilers."""
        self.cpu_profiler = self.profilerCPU.start()
        self.system_sampler.start()
        
        # Captura hardware uma vez por execução
        if self.hardware_info is None:
            self.hardware_info = Hardware().snapshot_hardware()
    
    def stop_profiling(self) -> Dict[str, Any]:
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
    
    def profile_function(self, func: Callable, *args, **kwargs) -> Dict[str, Any]:
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
        self.start_profiling()
        
        # Executa com trace de memória
        memory_result = Memory().trace(func, *args, **kwargs)
        
        metrics = self.stop_profiling()
        metrics["memory_metrics"] = {
            "memory_mb": memory_result["memory_mb"],
            "memory_increments": memory_result["memory_increments"]
        }
        
        return {
            "result": memory_result["result"],
            "metrics": metrics
        }
