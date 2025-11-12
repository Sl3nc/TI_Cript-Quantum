"""
Orquestração de execução única de algoritmo com profiling.

User Story 1: Executar avaliação única com coleta de métricas completas.
User Story 2: Gerar relatório Markdown individual.
"""
from config import DEFAULT_VOLUME, ALGORITHMS, RESULTS_DIR
from metrics.profile.manager import Profiler
from visualize.report_markdown import ReportMarkdown
from visualize.plotting import Plotting
from logging import getLogger
from datetime import datetime
from typing import Dict, Any
from pathlib import Path

logger = getLogger(__name__)

class Single:
    def __init__(self):
        self.plotting = Plotting()
        pass

    def run(
        self,
        algorithm: str,
        volume: int = DEFAULT_VOLUME,
    ) -> Dict[str, Any]:
        """
        Executa avaliação única de algoritmo com profiling completo.
        
        Args:
            algorithm: Nome do algoritmo ("MLKEM_1024", "MLDSA_87", "Krypton")
            volume: Número de operações a executar
            seed: Seed para PRNG (reprodutibilidade - Princípio V)
            
        Returns:
            Dict AlgorithmEvaluation com:
                - algorithm: str
                - volume: int
                - started_at: str (ISO timestamp)
                - ended_at: str (ISO timestamp)
                - duration_min: float
                - status: str (success|partial|failed)
                - metrics: dict (agregados)
                - hardware_profile: dict
                - notes: str
                
        Raises:
            ValueError: Se algorithm inválido ou volume <= 0
        """
        try:
            algo_func = self.validate_data(algorithm, volume)
            
            started_at = datetime.now()
            
            logger.info(f"action=run_single: START algorithm={algorithm} volume={volume}")
            
            # Executa algoritmo com profiling
            raw_metrics = Profiler().execution(algo_func, volume=volume)
            
            duration_min, duration_seg = self.calculate_duration(started_at)
            
            # Monta resultado final (AlgorithmEvaluation)
            evaluation = {
                "algorithm": algorithm,
                "volume": volume,
                "duration_min": duration_min,
                "duration_seg": duration_seg,
                "metrics": raw_metrics,
                "status": "success",
                "hardware_profile": raw_metrics.get("hardware_info", 'Undefined'),
                "notes": "",
            }
            
            report_path, image_paths = self._generate_report(
                evaluation, started_at
            )
            
            evaluation["report_path"] = str(report_path)
            evaluation["report_images"] = [str(p) for p in image_paths]
            
            logger.info(f"action=run_single: COMPLETE status=success duration_min={duration_min} report={report_path}")
            return evaluation
            
        except Exception as e:
            duration_min, duration_seg =  self.calculate_duration(started_at)
            logger.error(f"action=run_single: FAILED algorithm={algorithm} error={str(e)}")
            
            # Retorna estrutura com status failed
            return {
                "algorithm": algorithm,
                "volume": volume,
                "duration_min": duration_min,
                "duration_seg": duration_seg,
                "status": "failed",
                "metrics": 'Undefined',
                "hardware_profile": 'Undefined',
                "notes": f"Error: {str(e)}",
            }

    def calculate_duration(self, started_at: datetime):
        ended_at = datetime.now()
        duration = (ended_at - started_at).total_seconds()
        duration_format = f'{int(duration // 60):02d} min : {(duration % 60):05.2f} seg'
        return duration_format, duration

    def validate_data(self, algorithm, volume):
        if algorithm not in ALGORITHMS.keys():
            valid_algos = ", ".join(ALGORITHMS.keys())
            raise ValueError(f"Unknown algorithm '{algorithm}'. Valid options: {valid_algos}")
        
        if volume <= 0:
            raise ValueError(f"Volume must be greater than 0, got {volume}")
        
        return ALGORITHMS[algorithm]


    def _generate_report(self, evaluation: Dict[str, Any], started_at: datetime) -> tuple[Path, list[Path]]:
        """
        Gera relatório Markdown e gráficos.
        
        Args:
            evaluation: Dict AlgorithmEvaluation
            raw_metrics: Métricas brutas incluindo séries temporais
            
        Returns:
            tuple: (report_path, image_paths)
        """
        image_paths = []
        algorithm = evaluation["algorithm"]
        timestamp_str = started_at.strftime("%d-%m-%Y_%Hh-%Mm")
        
        # Diretório específico do algoritmo
        algo_dir = RESULTS_DIR / algorithm / timestamp_str
        report_path = algo_dir / f"relatorio.md"
        
        # Verificar colisão (raro mas possível)
        counter = 1
        while algo_dir.exists():
            timestamp_str += f' - {counter}'
            algo_dir = RESULTS_DIR / algorithm / timestamp_str
            counter += 1
        
        algo_dir.mkdir(parents=True, exist_ok=True)

        metrics = evaluation['metrics']
        # calls = metrics.get("cpu_metrics", {}).get("calls", [])
        memory_increments = metrics.get("memory_metrics", {}).get("memory_increments", [])
        
        # Gráfico 1: CPU time (se houver dados de série temporal)
        # self.generate_calls_plot(algo_dir, image_paths, calls)
        
        # Gráfico 2: Memory usage
        self.generate_memory_plot(algo_dir, image_paths, memory_increments)
        
        # Gerar relatório Markdown
        ReportMarkdown().build_report(evaluation, report_path, image_paths)
        
        logger.info(f"action=report_generated path={report_path} images={len(image_paths)}")
        
        return report_path, image_paths

    def generate_memory_plot(self, algo_dir, image_paths, memory_increments):
        memory_plot = algo_dir / f"memory.png"
        try:
            self.plotting.memory_series(
                memory_increments,
                memory_plot
            )
            image_paths.append(memory_plot)
        except Exception as e:
            logger.warning(f"Failed to generate memory plot: {e}")

    def generate_calls_plot(self, algo_dir, image_paths, cpu_time):
        cpu_time_plot = algo_dir / f"cpu_time.png"
        try:
            # Placeholder: usar incrementos de memória como proxy para série temporal
            self.plotting.cpu_time(
                cpu_time,
                cpu_time_plot,
            )
            image_paths.append(cpu_time_plot)
        except Exception as e:
            logger.warning(f"Failed to generate CPU time plot: {e}")