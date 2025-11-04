"""
Geração de relatórios Markdown com tabulate.
"""
from typing import Dict, Any, List
from pathlib import Path
import tabulate


def build_report(evaluation: Dict[str, Any], output_path: Path) -> None:
    """
    Gera relatório Markdown individual.
    
    Args:
        evaluation: Dict AlgorithmEvaluation com métricas
        output_path: Caminho completo para salvar .md
        
    Estrutura:
        # [Algoritmo] - [Timestamp]
        ## Hardware
        ## Métricas
        ## Gráficos
    """
    # Placeholder: implementar formatação completa
    content = f"# Placeholder Report\n\nAlgorithm: {evaluation.get('algorithm', 'Unknown')}\n"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding='utf-8')


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
