"""
Geração de gráficos com matplotlib.
"""
import matplotlib.pyplot as plt
from pathlib import Path
from typing import List, Dict, Any

class Plotting:
    def __init__(self) -> None:
        pass

    def plot_time_series(self, timestamps: List[int], values: List[float], output_path: Path, 
                        title: str = "Time Series", ylabel: str = "Value") -> None:
        """
        Gera gráfico de linha para série temporal.
        
        Args:
            timestamps: Lista de timestamps
            values: Lista de valores correspondentes
            output_path: Caminho para salvar .png
            title: Título do gráfico
            ylabel: Label do eixo Y
            
        Raises:
            ValueError: Se listas vazias ou tamanhos incompatíveis
        """
        if not timestamps or not values:
            raise ValueError("timestamps and values must not be empty")
        
        if len(timestamps) != len(values):
            raise ValueError(f"timestamps ({len(timestamps)}) and values ({len(values)}) must have same length")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(timestamps, values, marker='o', linewidth=2, markersize=6, color='#2563eb')
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel("Time (ms)", fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.grid(True, alpha=0.3)
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close(fig)


    def plot_memory_series(self, memory_samples: List[float], output_path: Path) -> None:
        """
        Gera gráfico de linha para consumo de memória.
        
        Args:
            memory_samples: Lista de amostras de memória (MB)
            output_path: Caminho para salvar .png
            
        Raises:
            ValueError: Se lista vazia
        """
        if not memory_samples:
            raise ValueError("memory_samples must not be empty")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sample_indices = list(range(len(memory_samples)))
        
        ax.plot(sample_indices, memory_samples, marker='x', linewidth=2, 
                markersize=8, color='#dc2626', label='Memory Usage')
        ax.fill_between(sample_indices, memory_samples, alpha=0.2, color='#dc2626')
        
        ax.set_title("Memory Usage Over Time", fontsize=14, fontweight='bold')
        ax.set_xlabel("Sample Index", fontsize=12)
        ax.set_ylabel("Memory (MB)", fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close(fig)


    def plot_scalability(self, volumes: List[int], metrics: Dict[str, List[float]], 
                        output_path: Path, metric_name: str = "Metric") -> None:
        """
        Gera gráfico de barras comparativo para escalabilidade.
        
        Args:
            volumes: Lista de volumes testados
            metrics: Dict com nome_metrica -> lista de valores
            output_path: Caminho para salvar .png
            metric_name: Nome da métrica principal
            
        Raises:
            ValueError: Se volumes vazio ou métricas incompatíveis
        """
        if not volumes:
            raise ValueError("volumes must not be empty")
        
        if not metrics:
            raise ValueError("metrics dict must not be empty")
        
        # Validar que todas as métricas têm mesmo tamanho que volumes
        for metric_label, values in metrics.items():
            if len(values) != len(volumes):
                raise ValueError(f"Metric '{metric_label}' has {len(values)} values but {len(volumes)} volumes")
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Cores distintas para cada métrica
        colors = ['#2563eb', '#dc2626', '#16a34a', '#9333ea']
        
        x_pos = list(range(len(volumes)))
        bar_width = 0.8 / len(metrics)
        
        for idx, (metric_label, values) in enumerate(metrics.items()):
            offset = (idx - len(metrics) / 2) * bar_width + bar_width / 2
            positions = [x + offset for x in x_pos]
            
            ax.bar(positions, values, bar_width, 
                label=metric_label, 
                alpha=0.8, 
                color=colors[idx % len(colors)])
        
        ax.set_xticks(x_pos)
        ax.set_xticklabels([str(v) for v in volumes], fontsize=11)
        ax.set_title(f"{metric_name} - Scalability Analysis", fontsize=14, fontweight='bold')
        ax.set_xlabel("Volume (operations)", fontsize=12)
        ax.set_ylabel(metric_name, fontsize=12)
        ax.legend(fontsize=10)
        ax.grid(True, axis='y', alpha=0.3)
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
