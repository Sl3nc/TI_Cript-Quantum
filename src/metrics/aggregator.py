"""
Agregação de métricas de múltiplas execuções.
"""
from typing import List, Dict, Any


def aggregate(metrics_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Agrega métricas de uma única execução.
    
    Args:
        metrics_list: Lista de dicts com métricas brutas (CPU, memória, sistema)
        
    Returns:
        Dict consolidado com métricas agregadas:
            - cpu_time_ms: float
            - memory_mb: float
            - cpu_cycles: int | None
            - cache_misses: int | None
            - hardware_info: dict
    """
    # Placeholder: implementar agregação real
    return {
        "cpu_time_ms": 0.0,
        "memory_mb": 0.0,
        "cpu_cycles": None,
        "cache_misses": None,
        "hardware_info": {}
    }


def aggregate_series(evaluations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Agrega métricas de múltiplas execuções (diferentes volumes).
    
    Args:
        evaluations: Lista de avaliações completas (AlgorithmEvaluation dicts)
        
    Returns:
        Dict com agregados:
            - cpu_time_avg_ms: float
            - cpu_time_std_ms: float
            - memory_peak_mb: float
            - volumes: list (volumes testados)
            - success_rate: float (0-1)
    """
    # Placeholder: implementar agregação de séries
    return {
        "cpu_time_avg_ms": 0.0,
        "cpu_time_std_ms": 0.0,
        "memory_peak_mb": 0.0,
        "volumes": [],
        "success_rate": 1.0
    }
