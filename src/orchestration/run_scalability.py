"""
Orquestração de análise de escalabilidade multi-volume.

User Story 3: Avaliar escalabilidade executando múltiplos volumes.
"""
from typing import Dict, Any, List
from datetime import datetime
from pathlib import Path
import logging
import sys

# Adiciona o diretório raiz ao path para permitir importações
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.orchestration.run_single import run_single
from src.metrics.aggregator import aggregate_series
from src.metrics.report_markdown import build_series_report
from src.metrics.plotting import plot_scalability
from src.orchestration.config import SEED, ALGORITHMS, RESULTS_DIR

logger = logging.getLogger(__name__)


def run_scalability(
    algorithm: str,
    volumes: List[int],
    seed: int = SEED
) -> Dict[str, Any]:
    """
    Executa análise de escalabilidade com múltiplos volumes.
    
    Args:
        algorithm: Nome do algoritmo ("MLKEM_1024", "MLDSA_87", "Krypton")
        volumes: Lista de volumes a testar (ex: [100, 500, 1000, 5000])
        seed: Seed base para PRNG (cada volume usa seed+index)
        
    Returns:
        Dict ScalabilitySeries com:
            - id: str
            - algorithm: str
            - volumes: list[int]
            - evaluation_ids: list[str]
            - individual_reports: list[str] (paths)
            - comparative_report_path: str
            - comparison_images: list[str] (paths)
            - aggregated_metrics: dict
            - status: str (success|partial|failed)
            
    Raises:
        ValueError: Se algorithm inválido ou volumes vazio
    """
    # Validações
    if algorithm not in ALGORITHMS:
        valid_algos = ", ".join(ALGORITHMS.keys())
        raise ValueError(f"Unknown algorithm '{algorithm}'. Valid options: {valid_algos}")
    
    if not volumes:
        raise ValueError("volumes list must not be empty")
    
    if any(v <= 0 for v in volumes):
        raise ValueError("All volumes must be greater than 0")
    
    logger.info(f"action=run_scalability_start algorithm={algorithm} volumes={volumes} seed={seed}")
    
    started_at = datetime.now()
    series_id = f"{algorithm}_scalability_{started_at.strftime('%Y%m%d_%H%M%S_%f')}"
    
    # Executar avaliações individuais para cada volume
    evaluations = []
    evaluation_ids = []
    individual_reports = []
    
    for idx, volume in enumerate(volumes):
        logger.info(f"action=run_volume volume={volume} index={idx+1}/{len(volumes)}")
        
        try:
            # Usar seed incremental para cada volume
            eval_result = run_single(
                algorithm=algorithm,
                volume=volume,
                seed=seed + idx
            )
            
            evaluations.append(eval_result)
            evaluation_ids.append(eval_result["id"])
            individual_reports.append(eval_result["report_path"])
            
        except Exception as e:
            logger.error(f"action=volume_failed volume={volume} error={str(e)}")
            
            # Criar avaliação com status failed
            failed_eval = {
                "id": f"{algorithm}_{volume}_failed_{idx}",
                "algorithm": algorithm,
                "volume": volume,
                "status": "failed",
                "metrics": {},
                "notes": f"Error: {str(e)}",
                "seed": seed + idx
            }
            evaluations.append(failed_eval)
            evaluation_ids.append(failed_eval["id"])
    
    # Agregar métricas de todas as avaliações
    aggregated = aggregate_series(evaluations)
    
    # Determinar status geral
    if aggregated["success_rate"] == 1.0:
        status = "success"
    elif aggregated["success_rate"] > 0.0:
        status = "partial"
    else:
        status = "failed"
    
    # Gerar gráficos comparativos
    comparison_images = _generate_comparison_graphs(algorithm, evaluations, started_at)
    
    # Gerar relatório comparativo
    comparative_report_path = _generate_comparative_report(
        algorithm, volumes, evaluations, aggregated, comparison_images, started_at
    )
    
    ended_at = datetime.now()
    duration_ms = (ended_at - started_at).total_seconds() * 1000
    
    result = {
        "id": series_id,
        "algorithm": algorithm,
        "volumes": volumes,
        "evaluation_ids": evaluation_ids,
        "individual_reports": individual_reports,
        "comparative_report_path": str(comparative_report_path),
        "comparison_images": [str(p) for p in comparison_images],
        "aggregated_metrics": aggregated,
        "status": status,
        "duration_ms": duration_ms
    }
    
    logger.info(f"action=run_scalability_complete id={series_id} status={status} duration_ms={duration_ms:.2f}")
    
    return result


def _generate_comparison_graphs(
    algorithm: str,
    evaluations: List[Dict[str, Any]],
    started_at: datetime
) -> List[Path]:
    """
    Gera gráficos comparativos de escalabilidade.
    
    Returns:
        Lista de paths para imagens geradas
    """
    image_paths = []
    
    # Filtrar apenas avaliações bem-sucedidas
    successful = [e for e in evaluations if e.get("status") == "success"]
    
    if not successful:
        logger.warning("No successful evaluations to plot")
        return image_paths
    
    # Extrair dados
    volumes = [e["volume"] for e in successful]
    cpu_times = [e["metrics"].get("cpu_time_ms", 0.0) for e in successful]
    memory_usage = [e["metrics"].get("memory_mb", 0.0) for e in successful]
    
    timestamp_str = started_at.strftime("%d-%m-%Y_%Hh%Mm%Ss")
    algo_dir = RESULTS_DIR / algorithm
    algo_dir.mkdir(parents=True, exist_ok=True)
    
    # Gráfico 1: CPU Time vs Volume
    try:
        cpu_plot_path = algo_dir / f"{algorithm}_scalability_cpu_{timestamp_str}.png"
        plot_scalability(
            volumes,
            {"CPU Time": cpu_times},
            cpu_plot_path,
            metric_name="CPU Time (ms)"
        )
        image_paths.append(cpu_plot_path)
        logger.info(f"Generated CPU scalability plot: {cpu_plot_path}")
    except Exception as e:
        logger.error(f"Failed to generate CPU plot: {e}")
    
    # Gráfico 2: Memory vs Volume
    try:
        memory_plot_path = algo_dir / f"{algorithm}_scalability_memory_{timestamp_str}.png"
        plot_scalability(
            volumes,
            {"Memory Usage": memory_usage},
            memory_plot_path,
            metric_name="Memory (MB)"
        )
        image_paths.append(memory_plot_path)
        logger.info(f"Generated Memory scalability plot: {memory_plot_path}")
    except Exception as e:
        logger.error(f"Failed to generate memory plot: {e}")
    
    # Gráfico 3: Combined (CPU + Memory)
    try:
        combined_plot_path = algo_dir / f"{algorithm}_scalability_combined_{timestamp_str}.png"
        
        # Normalizar valores para visualização conjunta
        max_cpu = max(cpu_times) if cpu_times else 1.0
        max_mem = max(memory_usage) if memory_usage else 1.0
        
        normalized_cpu = [t / max_cpu * 100 for t in cpu_times]
        normalized_mem = [m / max_mem * 100 for m in memory_usage]
        
        plot_scalability(
            volumes,
            {
                f"CPU Time (norm, max={max_cpu:.0f}ms)": normalized_cpu,
                f"Memory (norm, max={max_mem:.0f}MB)": normalized_mem
            },
            combined_plot_path,
            metric_name="Normalized Performance (%)"
        )
        image_paths.append(combined_plot_path)
        logger.info(f"Generated combined scalability plot: {combined_plot_path}")
    except Exception as e:
        logger.error(f"Failed to generate combined plot: {e}")
    
    return image_paths


def _generate_comparative_report(
    algorithm: str,
    volumes: List[int],
    evaluations: List[Dict[str, Any]],
    aggregated: Dict[str, Any],
    comparison_images: List[Path],
    started_at: datetime
) -> Path:
    """
    Gera relatório comparativo Markdown.
    
    Returns:
        Path do relatório gerado
    """
    timestamp_str = started_at.strftime("%d-%m-%Y %Hh%Mm%Ss.%f")[:-3]
    filename = f"{algorithm} - Escalabilidade - {timestamp_str}.md"
    
    algo_dir = RESULTS_DIR / algorithm
    algo_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = algo_dir / filename
    
    # Criar estrutura de dados para build_series_report
    series_data = {
        "algorithm": algorithm,
        "volumes": volumes,
        "aggregated_metrics": aggregated,
        "evaluations": evaluations,
        "started_at": started_at.isoformat()
    }
    
    build_series_report(series_data, report_path, comparison_images)
    
    logger.info(f"Generated comparative report: {report_path}")
    
    return report_path


if __name__ == "__main__":
    # Configurar logging para execução direta
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )
    
    # Exemplo de execução
    import argparse
    
    parser = argparse.ArgumentParser(description="Execute análise de escalabilidade de algoritmo")
    parser.add_argument("--algorithm", "-a", default="MLKEM_1024", 
                       choices=list(ALGORITHMS.keys()),
                       help="Algoritmo a executar")
    parser.add_argument("--volumes", "-v", nargs="+", type=int,
                       default=[100, 500, 1000],
                       help="Lista de volumes a testar (ex: 100 500 1000)")
    parser.add_argument("--seed", "-s", type=int, default=SEED,
                       help="Seed para reprodutibilidade")
    
    args = parser.parse_args()
    
    print(f"\n{'='*60}")
    print(f"Análise de Escalabilidade: {args.algorithm}")
    print(f"Volumes: {args.volumes}")
    print(f"Seed: {args.seed}")
    print(f"{'='*60}\n")
    
    result = run_scalability(
        algorithm=args.algorithm,
        volumes=args.volumes,
        seed=args.seed
    )
    
    print(f"\n{'='*60}")
    print(f"✓ Análise concluída!")
    print(f"Status: {result['status']}")
    print(f"Volumes testados: {len(result['evaluations'])}")
    if "report_path" in result:
        print(f"Relatório: {result['report_path']}")
    print(f"{'='*60}\n")
