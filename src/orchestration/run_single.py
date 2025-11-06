"""
Orquestração de execução única de algoritmo com profiling.

User Story 1: Executar avaliação única com coleta de métricas completas.
User Story 2: Gerar relatório Markdown individual.
"""
from typing import Dict, Any
from datetime import datetime
from pathlib import Path
import logging
import argparse
import sys

ROOT_DIR = Path(__file__[0:__file__.find('\\src')]).__str__()
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.algorithms.mlkem_kem import run_mlkem
from src.algorithms.mldsa_dss import generate_and_sign
from src.algorithms.krypton_cipher import cipher_rounds

from src.metrics import ProfilerManager
from src.metrics.aggregator import aggregate
from src.metrics.report_markdown import build_report
from src.metrics.plotting import plot_time_series, plot_memory_series
from src.orchestration.config import DEFAULT_VOLUME, SEED, ALGORITHMS, RESULTS_DIR

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
        "MLKEM_1024": run_mlkem,
        "MLDSA_87": generate_and_sign,
        "Krypton": cipher_rounds
    }
    
    algo_func = algorithm_functions[algorithm]
    
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
        
        # Gerar relatório com timestamp PT-BR e milissegundos para unicidade
        report_path, image_paths = _generate_report(evaluation, raw_metrics)
        
        evaluation["report_path"] = str(report_path)
        evaluation["report_images"] = [str(p) for p in image_paths]
        
        logger.info(f"action=run_single_complete id={evaluation_id} status=success duration_ms={duration_ms:.2f} report={report_path}")
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


def _generate_report(evaluation: Dict[str, Any], raw_metrics: Dict[str, Any]) -> tuple[Path, list[Path]]:
    """
    Gera relatório Markdown e gráficos.
    
    Args:
        evaluation: Dict AlgorithmEvaluation
        raw_metrics: Métricas brutas incluindo séries temporais
        
    Returns:
        tuple: (report_path, image_paths)
    """
    algorithm = evaluation["algorithm"]
    started_at = datetime.fromisoformat(evaluation["started_at"])
    
    # Timestamp PT-BR com milissegundos para unicidade
    timestamp_str = started_at.strftime("%d-%m-%Y %Hh%Mm%Ss.%f")[:-3]  # Remove últimos 3 dígitos (microsegundos)
    
    # Nome do arquivo: Algoritmo - DD-MM-YYYY HHhMMmSSs.mmm.md
    filename = f"{algorithm} - {timestamp_str}.md"
    
    # Diretório específico do algoritmo
    algo_dir = RESULTS_DIR / algorithm
    algo_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = algo_dir / filename
    
    # Verificar colisão (raro mas possível)
    counter = 1
    while report_path.exists():
        filename = f"{algorithm} - {timestamp_str}_{counter}.md"
        report_path = algo_dir / filename
        counter += 1
    
    # Gerar gráficos
    image_paths = []
    
    # Gráfico 1: CPU time (se houver dados de série temporal)
    memory_increments = raw_metrics.get("memory_metrics", {}).get("memory_increments", [])
    if memory_increments:
        cpu_time_plot = algo_dir / f"{algorithm}_cpu_time_{timestamp_str}.png"
        try:
            timestamps = list(range(len(memory_increments)))
            # Placeholder: usar incrementos de memória como proxy para série temporal
            plot_time_series(
                timestamps,
                memory_increments[:50] if len(memory_increments) > 50 else memory_increments,
                cpu_time_plot,
                title=f"{algorithm} - CPU Time Series",
                ylabel="Time Offset (arbitrary)"
            )
            image_paths.append(cpu_time_plot)
        except Exception as e:
            logger.warning(f"Failed to generate CPU time plot: {e}")
    
    # Gráfico 2: Memory usage
    if memory_increments:
        memory_plot = algo_dir / f"{algorithm}_memory_{timestamp_str}.png"
        try:
            plot_memory_series(
                memory_increments[:50] if len(memory_increments) > 50 else memory_increments,
                memory_plot
            )
            image_paths.append(memory_plot)
        except Exception as e:
            logger.warning(f"Failed to generate memory plot: {e}")
    
    # Gerar relatório Markdown
    build_report(evaluation, report_path, image_paths)
    
    logger.info(f"action=report_generated path={report_path} images={len(image_paths)}")
    
    return report_path, image_paths


if __name__ == "__main__":
    # Configurar logging para execução direta
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )
    
    parser = argparse.ArgumentParser(description="Execute uma avaliação única de algoritmo")
    parser.add_argument("--algorithm", "-a", default="MLKEM_1024", 
                       choices=list(ALGORITHMS.keys()),
                       help="Algoritmo a executar")
    parser.add_argument("--volume", "-v", type=int, default=DEFAULT_VOLUME,
                       help="Número de operações")
    parser.add_argument("--seed", "-s", type=int, default=SEED,
                       help="Seed para reprodutibilidade")
    
    args = parser.parse_args()
    
    print(f"\n{'='*60}")
    print(f"Executando: {args.algorithm}")
    print(f"Volume: {args.volume}")
    print(f"Seed: {args.seed}")
    print(f"{'='*60}\n")
    
    result = run_single(
        algorithm=args.algorithm,
        volume=args.volume,
        seed=args.seed
    )
    
    print(f"\n{'='*60}")
    print(f"✓ Execução concluída!")
    print(f"Status: {result['status']}")
    print(f"Duração: {result['duration_ms']:.2f} ms")
    if "report_path" in result:
        print(f"Relatório: {result['report_path']}")
    print(f"{'='*60}\n")
