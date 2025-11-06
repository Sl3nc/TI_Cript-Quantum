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
            - hardware_info: dict
    """
    # Placeholder: implementar agregação real
    return {
        "cpu_time_ms": 0.0,
        "memory_mb": 0.0,
        "cpu_cycles": None,
        "hardware_info": {}
    }


def aggregate_series(evaluations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Agrega métricas de múltiplas execuções (diferentes volumes).
    
    Args:
        evaluations: Lista de avaliações completas (AlgorithmEvaluation dicts)
        
    Returns:
        Dict com agregados:
            - cpu_time_avg_ms: float (média)
            - cpu_time_std_ms: float (desvio padrão)
            - memory_peak_mb: float (máximo)
            - volumes: list (volumes testados)
            - success_rate: float (0-1)
            - total_evaluations: int
            - successful_evaluations: int
    """
    if not evaluations:
        return {
            "cpu_time_avg_ms": 0.0,
            "cpu_time_std_ms": 0.0,
            "memory_peak_mb": 0.0,
            "volumes": [],
            "success_rate": 0.0,
            "total_evaluations": 0,
            "successful_evaluations": 0
        }
    
    # Filtrar avaliações bem-sucedidas
    successful = [e for e in evaluations if e.get("status") == "success"]
    
    # Extrair volumes
    volumes = [e.get("volume", 0) for e in evaluations]
    
    # Calcular success rate
    success_rate = len(successful) / len(evaluations) if evaluations else 0.0
    
    # Se nenhuma bem-sucedida, retornar agregados vazios
    if not successful:
        return {
            "cpu_time_avg_ms": 0.0,
            "cpu_time_std_ms": 0.0,
            "memory_peak_mb": 0.0,
            "volumes": volumes,
            "success_rate": success_rate,
            "total_evaluations": len(evaluations),
            "successful_evaluations": 0
        }
    
    # Extrair métricas das avaliações bem-sucedidas
    cpu_times = []
    memory_peaks = []
    
    for eval_item in successful:
        metrics = eval_item.get("metrics", {})
        cpu_times.append(metrics.get("cpu_time_ms", 0.0))
        memory_peaks.append(metrics.get("memory_mb", 0.0))
    
    # Calcular agregados
    import statistics
    
    cpu_time_avg = statistics.mean(cpu_times) if cpu_times else 0.0
    cpu_time_std = statistics.stdev(cpu_times) if len(cpu_times) > 1 else 0.0
    memory_peak = max(memory_peaks) if memory_peaks else 0.0
    
    return {
        "cpu_time_avg_ms": cpu_time_avg,
        "cpu_time_std_ms": cpu_time_std,
        "memory_peak_mb": memory_peak,
        "volumes": volumes,
        "success_rate": success_rate,
        "total_evaluations": len(evaluations),
        "successful_evaluations": len(successful)
    }
