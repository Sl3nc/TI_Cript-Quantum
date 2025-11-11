"""
Profiling de memória usando memory_profiler.
"""
from typing import Dict, Any, Callable, cast
from memory_profiler import memory_usage

class Memory:
    def trace(self, func: Callable, *args, **kwargs) -> Dict[str, Any]:
        """
        Rastreia consumo de memória durante execução.
        
        Args:
            func: Função a monitorar
            *args, **kwargs: Argumentos para função
            
        Returns:
            Dict com:
                - memory_mb: float (pico de memória em MB)
                - memory_increments: list (crescimento incremental)
                - result: Any (retorno da função)
        """
        mem_usage = memory_usage(
            cast(Any, (func, args, kwargs)),
            interval=0.01,
            include_children=True,
            retval=True
        )[0]

        peak_memory = max(mem_usage) if mem_usage else 0.0
        baseline = mem_usage[0] if mem_usage else 0.0
        increments = [m - baseline for m in mem_usage]
        
        return {
            "peak_memory": peak_memory,
            "memory_increments": increments,
        }
