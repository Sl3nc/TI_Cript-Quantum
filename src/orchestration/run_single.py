"""
Orquestração de execução única de algoritmo com profiling.

User Story 1: Executar avaliação única com coleta de métricas completas.
"""
from typing import Dict, Any
from datetime import datetime
from pathlib import Path
import logging

from src.metrics import ProfilerManager
from src.metrics.aggregator import aggregate
from src.orchestration.config import DEFAULT_VOLUME, SEED, ALGORITHMS

logger = logging.getLogger(__name__)


def run_single(
    algorithm: str,
    volume: int = DEFAULT_VOLUME,
    seed: int = SEED
) -> Dict[str, Any]:
    """
    Executa avaliação única de algoritmo com profiling completo.
    
    Args:
        algorithm: Nome do algoritmo ("MLKEM_1024", "MLDSA_87", "Krypton")
        volume: Número de operações a executar
        seed: Seed para PRNG (reprodutibilidade - Princípio V)
        
    Returns:
        Dict AlgorithmEvaluation com:
            - id: str (timestamp + algoritmo)
            - algorithm: str
            - challenge_type: str
            - volume: int
            - started_at: str (ISO timestamp)
            - ended_at: str (ISO timestamp)
            - duration_ms: float
            - status: str (success|partial|failed)
            - metrics: dict (agregados)
            - hardware_profile: dict
            - notes: str
            
    Raises:
        ValueError: Se algorithm inválido ou volume <= 0
    """
    # Validação de algoritmo
    if algorithm not in ALGORITHMS:
        valid_algos = ", ".join(ALGORITHMS.keys())
        raise ValueError(f"Unknown algorithm '{algorithm}'. Valid options: {valid_algos}")
    
    # Validação de volume (propagada para funções de algoritmo)
    if volume <= 0:
        raise ValueError(f"volume must be greater than 0, got {volume}")
    
    logger.info(f"action=run_single_start algorithm={algorithm} volume={volume} seed={seed}")
    
    # Importar função específica do algoritmo
    algorithm_functions = {
        "MLKEM_1024": _import_mlkem,
        "MLDSA_87": _import_mldsa,
        "Krypton": _import_krypton
    }
    
    algo_func = algorithm_functions[algorithm]()
    
    # Timestamps
    started_at = datetime.now()
    evaluation_id = f"{algorithm}_{started_at.strftime('%Y%m%d_%H%M%S_%f')}"
    
    # Profiling completo
    profiler = ProfilerManager()
    
    try:
        # Executa algoritmo com profiling
        profiled_result = profiler.profile_function(algo_func, volume=volume, seed=seed)
        
        ended_at = datetime.now()
        duration_ms = (ended_at - started_at).total_seconds() * 1000
        
        # Agrega métricas
        raw_metrics = profiled_result["metrics"]
        aggregated = aggregate([raw_metrics])
        
        # Monta resultado final (AlgorithmEvaluation)
        evaluation = {
            "id": evaluation_id,
            "algorithm": algorithm,
            "challenge_type": ALGORITHMS[algorithm],
            "volume": volume,
            "started_at": started_at.isoformat(),
            "ended_at": ended_at.isoformat(),
            "duration_ms": duration_ms,
            "status": "success",
            "metrics": aggregated,
            "hardware_profile": raw_metrics.get("hardware_info", {}),
            "notes": "",
            "seed": seed
        }
        
        logger.info(f"action=run_single_complete id={evaluation_id} status=success duration_ms={duration_ms:.2f}")
        return evaluation
        
    except Exception as e:
        ended_at = datetime.now()
        duration_ms = (ended_at - started_at).total_seconds() * 1000
        
        logger.error(f"action=run_single_failed algorithm={algorithm} error={str(e)}")
        
        # Retorna estrutura com status failed
        return {
            "id": evaluation_id,
            "algorithm": algorithm,
            "challenge_type": ALGORITHMS[algorithm],
            "volume": volume,
            "started_at": started_at.isoformat(),
            "ended_at": ended_at.isoformat(),
            "duration_ms": duration_ms,
            "status": "failed",
            "metrics": {},
            "hardware_profile": {},
            "notes": f"Error: {str(e)}",
            "seed": seed
        }


def _import_mlkem():
    """Importa função MLKEM_1024."""
    from src.algorithms.mlkem_kem import run_mlkem
    return run_mlkem


def _import_mldsa():
    """Importa função MLDSA_87."""
    from src.algorithms.mldsa_dss import generate_and_sign
    return generate_and_sign


def _import_krypton():
    """Importa função Krypton."""
    from src.algorithms.krypton_cipher import cipher_rounds
    return cipher_rounds
