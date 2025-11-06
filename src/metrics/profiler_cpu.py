"""
Profiling de CPU usando cProfile e line_profiler.
"""
import cProfile
import pstats
from io import StringIO
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


def start_cpu_profile() -> cProfile.Profile:
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


def stop_cpu_profile(profiler: cProfile.Profile) -> Dict[str, Any]:
    """
    Para profiling e extrai métricas de tempo.
    
    Args:
        profiler: Profiler ativo retornado por start_cpu_profile
        
    Returns:
        Dict com:
            - cpu_time_ms: float (tempo total em milissegundos)
            - cumulative_time_ms: float
            - primitive_calls: int
            - total_calls: int
    """
    profiler.disable()
    logger.debug("action=stop_cpu_profile status=disabled")
    
    stream = StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    stats.sort_stats('cumulative')
    
    # Extract real metrics
    total_calls = stats.total_calls if hasattr(stats, 'total_calls') else 0
    prim_calls = stats.prim_calls if hasattr(stats, 'prim_calls') else 0
    
    logger.info(f"action=cpu_profile_stopped primitive_calls={prim_calls} total_calls={total_calls}")
    
    # Placeholder: extrair métricas reais do pstats
    return {
        "cpu_time_ms": 0.0,
        "cumulative_time_ms": 0.0,
        "primitive_calls": 0,
        "total_calls": 0
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
