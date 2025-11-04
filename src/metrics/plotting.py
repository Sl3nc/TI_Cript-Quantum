"""
Geração de gráficos com matplotlib.
"""
import matplotlib.pyplot as plt
from pathlib import Path
from typing import List, Dict, Any


def plot_time_series(timestamps: List[float], values: List[float], output_path: Path, 
                     title: str = "Time Series", ylabel: str = "Value") -> None:
    """
    Gera gráfico de linha para série temporal.
    
    Args:
        timestamps: Lista de timestamps
        values: Lista de valores correspondentes
        output_path: Caminho para salvar .png
        title: Título do gráfico
        ylabel: Label do eixo Y
    """
    # Placeholder: implementar gráfico real
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(timestamps, values, marker='o')
    ax.set_title(title)
    ax.set_xlabel("Time")
    ax.set_ylabel(ylabel)
    ax.grid(True)
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close(fig)


def plot_memory_series(memory_samples: List[float], output_path: Path) -> None:
    """
    Gera gráfico de linha para consumo de memória.
    
    Args:
        memory_samples: Lista de amostras de memória (MB)
        output_path: Caminho para salvar .png
    """
    # Placeholder: implementar gráfico de memória
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(range(len(memory_samples)), memory_samples, marker='x', color='red')
    ax.set_title("Memory Usage")
    ax.set_xlabel("Sample")
    ax.set_ylabel("Memory (MB)")
    ax.grid(True)
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close(fig)


def plot_scalability(volumes: List[int], metrics: Dict[str, List[float]], 
                     output_path: Path, metric_name: str = "Metric") -> None:
    """
    Gera gráfico de barras comparativo para escalabilidade.
    
    Args:
        volumes: Lista de volumes testados
        metrics: Dict com nome_metrica -> lista de valores
        output_path: Caminho para salvar .png
        metric_name: Nome da métrica principal
    """
    # Placeholder: implementar gráfico de barras
    fig, ax = plt.subplots(figsize=(12, 6))
    
    for metric_label, values in metrics.items():
        ax.bar(range(len(volumes)), values, label=metric_label, alpha=0.7)
    
    ax.set_xticks(range(len(volumes)))
    ax.set_xticklabels([str(v) for v in volumes])
    ax.set_title(f"{metric_name} - Scalability Analysis")
    ax.set_xlabel("Volume")
    ax.set_ylabel(metric_name)
    ax.legend()
    ax.grid(True, axis='y')
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
