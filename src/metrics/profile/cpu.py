"""
Profiling de CPU usando cProfile e line_profiler.
"""
import cProfile
import pstats
from io import StringIO
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class CPU:
    def start() -> cProfile.Profile:
        """
        Inicia profiling de CPU com cProfile.
        
        Returns:
            cProfile.Profile: Objeto profiler ativo
        """
        logger.debug("action=start_cpu_profile status=initiated")
        profiler = cProfile.Profile()
        try:
            profiler.enable()
            logger.debug("action=start_cpu_profile status=enabled")
        except ValueError as e:
            # Se já houver um profiler ativo, desabilitar e tentar novamente
            logger.warning(f"Profiler already active, attempting to clear: {e}")
            try:
                profiler.disable()
            except:
                pass
            profiler = cProfile.Profile()
            profiler.enable()
            logger.debug("action=start_cpu_profile status=enabled_after_clear")
        return profiler


    def stop(profiler: cProfile.Profile) -> Dict[str, Any]:
        """Finaliza o profiling e extrai métricas reais de CPU.

        Args:
            profiler: Instância ativa de cProfile.

        Returns:
            Dict com:
                cpu_time_ms: Tempo total (soma do tempo interno de cada função) em ms
                cumulative_time_ms: Maior tempo cumulativo observado (aproxima a duração total) em ms
                primitive_calls: Chamadas primitivas
                total_calls: Chamadas totais (inclui recursivas)
        """
        profiler.disable()
        logger.debug("action=stop_cpu_profile status=disabled")

        stream = StringIO()
        stats = pstats.Stats(profiler, stream=stream)
        stats.sort_stats("cumulative")

        total_calls = getattr(stats, "total_calls", 0)
        prim_calls = getattr(stats, "prim_calls", 0)

        total_inline_time = 0.0  
        max_cum_time = 0.0      

        # stats.stats: {(filename, line, funcname): (prim_calls, total_calls, inline_time, cumulative_time, callers)}
        for func_key, func_stats in getattr(stats, "stats", {}).items():
            inline_time = func_stats[2]
            cumulative_time = func_stats[3]
            total_inline_time += inline_time
            if cumulative_time > max_cum_time:
                max_cum_time = cumulative_time

        cpu_time_ms = total_inline_time * 1000.0
        cumulative_time_ms = max_cum_time * 1000.0

        logger.info(
            "action=cpu_profile: STOPPED primitive_calls=%d total_calls=%d cpu_time_ms=%.3f cumulative_time_ms=%.3f",
            prim_calls, total_calls, cpu_time_ms, cumulative_time_ms
        )

        return {
            "cpu_time_ms": cpu_time_ms,
            "cumulative_time_ms": cumulative_time_ms,
            "primitive_calls": prim_calls,
            "total_calls": total_calls,
        }


    def profile_lines(func, *args, **kwargs) -> Dict[str, Any]:
        """
        Perfila linhas críticas usando line_profiler.
        
        Args:
            func: Função a perfilar
            *args, **kwargs: Argumentos para função
            
        Returns:
            Dict com métricas de linha (placeholder)
        """
        # Placeholder: integrar line_profiler
        result = func(*args, **kwargs)
        return {
            "line_stats": {},
            "result": result
        }
