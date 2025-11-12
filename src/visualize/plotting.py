"""
Geração de gráficos com matplotlib.
"""
import matplotlib.pyplot as plt
from pathlib import Path
from typing import List, Dict

class Plotting:
    def __init__(self) -> None:
        pass

    def cpu_time(self, memory_increments: List[float], output_path: Path) -> None:
        """Gera gráfico detalhado para a coluna "CPU Time".

        Ajusta o eixo Y para maior proximidade dos valores observados e adiciona
        referências estatísticas (mínimo, média, máximo, p95 e último valor),
        além de uma caixa resumo para facilitar a análise no relatório.

        Args:
            memory_increments: Lista de valores de tempo de CPU (ms)
            output_path: Caminho onde o PNG será salvo

        Raises:
            ValueError: Se a lista estiver vazia
        """
        if not memory_increments:
            raise ValueError("memory_increments (CPU Time values) must not be empty")

        timestamps = list(range(len(memory_increments)))
        title = "CPU Time"
        ylabel = "CPU Time (ms)"

        # Estatísticas principais
        min_val = min(memory_increments)
        max_val = max(memory_increments)
        mean_val = sum(memory_increments) / len(memory_increments)
        sorted_vals = sorted(memory_increments)
        p95_idx = int(0.95 * (len(sorted_vals) - 1))
        p95_val = sorted_vals[p95_idx]
        last_val = memory_increments[-1]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(
            timestamps,
            memory_increments,
            marker='o',
            linewidth=2,
            markersize=5,
            color='#2563eb',
            label='CPU Time'
        )
        ax.fill_between(timestamps, memory_increments, alpha=0.15, color='#2563eb')

        # Linhas de referência
        ax.axhline(mean_val, color='#1e3a8a', linestyle='--', linewidth=1.1, label=f'Mean {mean_val:.2f} ms')
        ax.axhline(min_val, color='#16a34a', linestyle=':', linewidth=1, label=f'Min {min_val:.2f} ms')
        ax.axhline(max_val, color='#9333ea', linestyle=':', linewidth=1, label=f'Max {max_val:.2f} ms')
        ax.axhline(p95_val, color='#dc2626', linestyle='-.', linewidth=1, label=f'P95 {p95_val:.2f} ms')

        # Destaque último valor
        ax.scatter([timestamps[-1]], [last_val], color='#dc2626', s=55, zorder=5, label=f'Last {last_val:.2f} ms')

        # Ajuste de limites próximos (5% de margem)
        span = max_val - min_val
        margin = span * 0.05 if span > 0 else max_val * 0.05 if max_val != 0 else 1
        ax.set_ylim(min_val - margin, max_val + margin)

        # Caixa resumo
        stats_text = (
            f"Samples: {len(memory_increments)}\n"
            f"Min: {min_val:.2f} ms\n"
            f"Mean: {mean_val:.2f} ms\n"
            f"Max: {max_val:.2f} ms\n"
            f"P95: {p95_val:.2f} ms\n"
            f"Last: {last_val:.2f} ms"
        )
        ax.text(
            0.99,
            0.02,
            stats_text,
            transform=ax.transAxes,
            fontsize=9,
            va='bottom',
            ha='right',
            bbox=dict(boxstyle='round,pad=0.35', facecolor='white', alpha=0.85, edgecolor='#2563eb')
        )

        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel("Sample Index", fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=9)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close(fig)


    def memory_series(self, memory_samples: List[float], output_path: Path) -> None:
        """Gera gráfico detalhado de consumo de memória aproximando-se da coluna "Memory MB".

        Adiciona referências estatísticas (mínimo, média, máximo) e ajusta os limites
        do eixo Y para ficar mais "colado" aos valores observados, evitando grande
        faixa vazia. Também inclui anotações para facilitar leitura do relatório.

        Args:
            memory_samples: Lista de amostras de memória (MB)
            output_path: Caminho para salvar .png

        Raises:
            ValueError: Se lista vazia
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        sample_indices = list(range(len(memory_samples)))

        # Série principal
        ax.plot(
            sample_indices,
            memory_samples,
            marker='x',
            linewidth=2,
            markersize=6,
            color='#dc2626',
            label='Memory Usage'
        )
        ax.fill_between(sample_indices, memory_samples, alpha=0.18, color='#dc2626')

        # Estatísticas
        min_val = min(memory_samples)
        max_val = max(memory_samples)
        mean_val = sum(memory_samples) / len(memory_samples)

        # Linhas de referência
        ax.axhline(mean_val, color='#1e3a8a', linestyle='--', linewidth=1.2, label=f'Mean {mean_val:.2f} MB')
        ax.axhline(min_val, color='#16a34a', linestyle=':', linewidth=1, label=f'Min {min_val:.2f} MB')
        ax.axhline(max_val, color='#9333ea', linestyle=':', linewidth=1, label=f'Max {max_val:.2f} MB')

        # Ajuste de limites próximos aos valores (5% de margem)
        span = max_val - min_val
        margin = span * 0.05 if span > 0 else max_val * 0.05 if max_val != 0 else 1
        ax.set_ylim(min_val - margin, max_val + margin)

        # Caixa resumo
        stats_text = (
            f"Samples: {len(memory_samples)}\n"
            f"Min: {min_val:.2f} MB\n"
            f"Mean: {mean_val:.2f} MB\n"
            f"Max: {max_val:.2f} MB"
        )
        ax.text(
            0.99,
            0.02,
            stats_text,
            transform=ax.transAxes,
            fontsize=9,
            va='bottom',
            ha='right',
            bbox=dict(boxstyle='round,pad=0.35', facecolor='white', alpha=0.85, edgecolor='#dc2626')
        )

        ax.set_title("Memory Usage Over Time", fontsize=14, fontweight='bold')
        ax.set_xlabel("Sample Index", fontsize=12)
        ax.set_ylabel("Memory (MB)", fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=9)

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
