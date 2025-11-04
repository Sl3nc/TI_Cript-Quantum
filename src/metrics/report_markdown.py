"""
Geração de relatórios Markdown com tabulate.
"""
from typing import Dict, Any, List
from pathlib import Path
import tabulate
from datetime import datetime


def build_report(evaluation: Dict[str, Any], output_path: Path, image_paths: List[Path] = None) -> None:
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
    timestamp = evaluation.get("started_at", "")
    
    # Converter ISO timestamp para PT-BR se disponível
    try:
        dt = datetime.fromisoformat(timestamp)
        timestamp_br = dt.strftime("%d-%m-%Y %Hh%Mm%Ss.%f")[:-3]  # Milissegundos
    except:
        timestamp_br = timestamp
    
    lines = [
        f"# {algorithm} - {timestamp_br}",
        "",
        "## Resumo",
        "",
        f"**Algoritmo**: {algorithm}",
        f"**Tipo de Desafio**: {evaluation.get('challenge_type', 'N/A')}",
        f"**Volume**: {evaluation.get('volume', 0)} operações",
        f"**Status**: {evaluation.get('status', 'unknown')}",
        f"**Duração**: {evaluation.get('duration_ms', 0):.2f} ms",
        f"**Seed**: {evaluation.get('seed', 'N/A')}",
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
        
        # Tabela de métricas com tabulate
        metrics_data = [
            ["CPU Time", f"{metrics.get('cpu_time_ms', 0):.2f} ms"],
            ["Memory Peak", f"{metrics.get('memory_mb', 0):.2f} MB"],
            ["CPU Cycles", _format_metric(metrics.get('cpu_cycles'))],
            ["Cache Misses", _format_metric(metrics.get('cache_misses'))],
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
            img_name = img_path.name
            # Caminho relativo ao relatório
            rel_path = img_path.name  # Assumindo imagens no mesmo diretório
            lines.append(f"![{img_name}]({rel_path})")
            lines.append("")
    
    # Notas
    notes = evaluation.get("notes", "")
    if notes:
        lines.extend([
            "## Observações",
            "",
            notes,
            ""
        ])
    
    # Footer
    lines.extend([
        "---",
        f"*Relatório gerado em {datetime.now().strftime('%d-%m-%Y %Hh%Mm%Ss')}*"
    ])
    
    content = "\n".join(lines)
    output_path.write_text(content, encoding='utf-8')


def _format_metric(value) -> str:
    """Formata métrica, tratando None."""
    if value is None:
        return "N/A (indisponível)"
    if isinstance(value, (int, float)):
        return f"{value:,}"
    return str(value)


def build_series_report(series: Dict[str, Any], output_path: Path, image_paths: List[Path]) -> None:
    """
    Gera relatório comparativo de escalabilidade.
    
    Args:
        series: Dict ScalabilitySeries com agregados
        output_path: Caminho para salvar .md
        image_paths: Lista de caminhos para gráficos gerados
        
    Estrutura:
        # [Algoritmo] - Análise de Escalabilidade
        ## Volumes Testados
        ## Agregados
        ## Gráficos Comparativos
    """
    # Placeholder: implementar formatação comparativa
    content = f"# Placeholder Scalability Report\n\nVolumes: {series.get('volumes', [])}\n"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding='utf-8')
