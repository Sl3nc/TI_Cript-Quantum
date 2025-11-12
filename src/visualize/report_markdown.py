"""
Geração de relatórios Markdown com tabulate.
"""
from typing import Dict, Any, List
from pathlib import Path
import tabulate
from datetime import datetime

class ReportMarkdown:
    def build_report(self, evaluation: Dict[str, Any], output_path: Path, image_paths: List[Path] | None = None) -> None:
        """
        Gera relatório Markdown individual completo.
        
        Args:
            evaluation: Dict AlgorithmEvaluation com métricas
            output_path: Caminho completo para salvar .md
            image_paths: Lista de caminhos para gráficos gerados (opcional)
            
        Estrutura:
            # [Algoritmo] - [Timestamp PT-BR]
            ## Resumo
            ## Hardware
            ## Métricas
            ## Gráficos
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        image_paths = image_paths or []
        
        # Header
        algorithm = evaluation.get("algorithm", "Unknown")
        
        lines = [
            "## Relatório",
            "",
            f"**Algoritmo**: {algorithm}",
            f"**Volume**: {evaluation.get('volume', 0)} operações",
            f"**Duração**: {evaluation.get('duration_min', 'Undefined')}",
            "",
        ]
        
        # Hardware section
        hw = evaluation.get("hardware_profile", {})
        if hw:
            lines.extend([
                "## Hardware",
                "",
                f"**CPU**: {hw.get('cpu_brand', 'N/A')}",
                f"**Arquitetura**: {hw.get('cpu_arch', 'N/A')}",
                f"**Cores Físicos**: {hw.get('cpu_cores', 'N/A')}",
                f"**Cores Lógicos**: {hw.get('cpu_threads', 'N/A')}",
                f"**Frequência**: {hw.get('cpu_freq_mhz', 0):.0f} MHz",
                f"**RAM Total**: {hw.get('ram_total_gb', 0):.2f} GB",
                "",
            ])
        
        # Metrics table
        metrics = evaluation.get("metrics", {})
        if metrics:
            lines.extend([
                "## Métricas Coletadas",
                "",
            ])

            cpu = metrics['cpu_metrics']
            system = metrics['system_metrics']
            memory = metrics['memory_metrics']
            
            # Tabela de métricas com tabulate
            metrics_data = [
                ["CPU Time", f"{cpu.get('cpu_time_total', 0):.2f} ms"],
                ["CPU Usage Avarage", f"{system.get('cpu_percent_avg', 0):.2f}%"],
                ["Memory Peak", f"{memory.get('memory_mb', 0):.2f} MB"],
                ["Memory Usage Maximum", f"{system.get('memory_percent_max', 0):.2f}%"],
            ]
            
            table = tabulate.tabulate(
                metrics_data,
                headers=["Métrica", "Valor"],
                tablefmt="github"
            )
            
            lines.extend([table, ""])
        
        # Gráficos
        if image_paths:
            lines.extend([
                "## Gráficos",
                "",
            ])
            
            for img_path in image_paths:
                lines.append(f"![{img_path.name}]({img_path.name})")
                lines.append("")
        
        content = "\n".join(lines)
        output_path.write_text(content, encoding='utf-8')

    def build_series_report(self, series: Dict[str, Any], output_path: Path, image_paths: List[Path]) -> None:
        """
        Gera relatório comparativo de escalabilidade.
        
        Args:
            series: Dict com:
                - algorithm: str
                - volumes: list[int]
                - aggregated_metrics: dict
                - evaluations: list[dict]
                - started_at: str (ISO timestamp)
            output_path: Caminho para salvar .md
            image_paths: Lista de caminhos para gráficos gerados
            
        Estrutura:
            # [Algoritmo] - Análise de Escalabilidade
            ## Resumo
            ## Volumes Testados
            ## Métricas Agregadas
            ## Resultados por Volume
            ## Gráficos Comparativos
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        algorithm = series.get("algorithm", "Unknown")
        volumes = series.get("volumes", [])
        aggregated = series.get("aggregated_metrics", {})
        evaluations = series.get("evaluations", [])
        
        # Converter timestamp
        timestamp_str = series.get("started_at", "")
        try:
            dt = datetime.fromisoformat(timestamp_str)
            timestamp_br = dt.strftime("%d-%m-%Y %Hh%Mm%Ss")
        except:
            timestamp_br = timestamp_str
        
        lines = [
            f"# {algorithm} - Análise de Escalabilidade",
            "",
            f"**Data**: {timestamp_br}",
            "",
            "## Resumo",
            "",
            f"**Algoritmo**: {algorithm}",
            f"**Volumes Testados**: {', '.join(map(str, volumes))}",
            f"**Total de Avaliações**: {aggregated.get('total_evaluations', 0)}",
            f"**Avaliações Bem-Sucedidas**: {aggregated.get('successful_evaluations', 0)}",
            f"**Taxa de Sucesso**: {aggregated.get('success_rate', 0.0) * 100:.1f}%",
            "",
        ]
        
        # Métricas agregadas
        lines.extend([
            "## Métricas Agregadas",
            "",
        ])
        
        agg_data = [
            ["CPU Time (Média)", f"{aggregated.get('cpu_time_avg_ms', 0):.2f} ms"],
            ["CPU Time (Desvio Padrão)", f"{aggregated.get('cpu_time_std_ms', 0):.2f} ms"],
            ["Memory (Pico)", f"{aggregated.get('memory_peak_mb', 0):.2f} MB"],
        ]
        
        agg_table = tabulate.tabulate(
            agg_data,
            headers=["Métrica", "Valor"],
            tablefmt="github"
        )
        
        lines.extend([agg_table, "", ""])
        
        # Resultados por volume
        successful_evals = [e for e in evaluations if e.get("status") == "success"]
        
        if successful_evals:
            lines.extend([
                "## Resultados por Volume",
                "",
            ])
            
            volume_data = []
            for eval_item in successful_evals:
                volume = eval_item.get("volume", 0)
                metrics = eval_item.get("metrics", {})
                cpu_time = metrics.get("cpu_time_ms", 0.0)
                memory = metrics.get("memory_mb", 0.0)
                duration = eval_item.get("duration_ms", 0.0)
                
                volume_data.append([
                    volume,
                    f"{cpu_time:.2f} ms",
                    f"{memory:.2f} MB",
                    f"{duration:.2f} ms"
                ])
            
            volume_table = tabulate.tabulate(
                volume_data,
                headers=["Volume", "CPU Time", "Memory", "Duração Total"],
                tablefmt="github"
            )
            
            lines.extend([volume_table, "", ""])
        
        # Falhas (se houver)
        failed_evals = [e for e in evaluations if e.get("status") != "success"]
        if failed_evals:
            lines.extend([
                "## Falhas",
                "",
            ])
            
            for eval_item in failed_evals:
                volume = eval_item.get("volume", 0)
                status = eval_item.get("status", "unknown")
                notes = eval_item.get("notes", "No details")
                
                lines.append(f"- **Volume {volume}**: {status} - {notes}")
            
            lines.append("")
        
        # Gráficos comparativos
        if image_paths:
            lines.extend([
                "## Gráficos Comparativos",
                "",
            ])
            
            for img_path in image_paths:
                img_name = img_path.name
                lines.append(f"![{img_name}]({img_name})")
                lines.append("")
        
        # Análise de escalabilidade
        lines.extend([
            "## Análise",
            "",
        ])
        
        if len(successful_evals) >= 2:
            # Calcular taxa de crescimento (CPU time)
            first_eval = successful_evals[0]
            last_eval = successful_evals[-1]
            
            first_cpu = first_eval["metrics"].get("cpu_time_ms", 1.0)
            last_cpu = last_eval["metrics"].get("cpu_time_ms", 1.0)
            
            first_vol = first_eval["volume"]
            last_vol = last_eval["volume"]
            
            volume_ratio = last_vol / first_vol if first_vol > 0 else 1.0
            cpu_ratio = last_cpu / first_cpu if first_cpu > 0 else 1.0
            
            lines.extend([
                f"- Volume aumentou {volume_ratio:.1f}x (de {first_vol} para {last_vol})",
                f"- CPU Time aumentou {cpu_ratio:.1f}x (de {first_cpu:.2f}ms para {last_cpu:.2f}ms)",
                f"- Complexidade aparente: **O({cpu_ratio/volume_ratio:.2f}n)** aproximadamente",
                ""
            ])
        else:
            lines.extend([
                "Dados insuficientes para análise de escalabilidade detalhada.",
                ""
            ])
        
        # Footer
        lines.extend([
            "---",
            f"*Relatório gerado em {datetime.now().strftime('%d-%m-%Y %Hh%Mm%Ss')}*"
        ])
        
        content = "\n".join(lines)
        output_path.write_text(content, encoding='utf-8')
