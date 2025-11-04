"""
Testes unitários para geração de gráficos.
"""
import pytest
from pathlib import Path
import tempfile


def test_plot_time_series_creates_png():
    """Verifica que plot_time_series gera arquivo PNG válido."""
    from src.metrics.plotting import plot_time_series
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "time_plot.png"
        
        timestamps = [0.0, 100.0, 200.0, 300.0, 400.0]
        values = [10.5, 25.3, 18.7, 30.2, 28.9]
        
        plot_time_series(timestamps, values, output_path, 
                        title="CPU Time", ylabel="ms")
        
        # PNG deve existir
        assert output_path.exists(), "Gráfico PNG deve ser criado"
        
        # Tamanho razoável (não vazio)
        assert output_path.stat().st_size > 1000, "PNG deve ter tamanho > 1KB"
        
        # Header PNG válido (89 50 4E 47)
        with open(output_path, 'rb') as f:
            header = f.read(4)
            assert header == b'\x89PNG', "Deve ter header PNG válido"


def test_plot_memory_series_creates_png():
    """Verifica que plot_memory_series gera PNG."""
    from src.metrics.plotting import plot_memory_series
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "memory_plot.png"
        
        memory_samples = [10.0, 15.5, 20.3, 18.2, 22.7, 25.1]
        
        plot_memory_series(memory_samples, output_path)
        
        assert output_path.exists()
        assert output_path.stat().st_size > 1000


def test_plot_scalability_creates_bar_chart():
    """Verifica que plot_scalability gera gráfico de barras."""
    from src.metrics.plotting import plot_scalability
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "scalability.png"
        
        volumes = [100, 500, 1000, 5000]
        metrics = {
            "CPU Time (ms)": [50.0, 200.0, 400.0, 2000.0],
            "Memory (MB)": [10.0, 40.0, 80.0, 400.0]
        }
        
        plot_scalability(volumes, metrics, output_path, metric_name="Performance")
        
        assert output_path.exists()
        assert output_path.stat().st_size > 1000


def test_plots_handle_empty_data_gracefully():
    """Verifica comportamento com dados vazios."""
    from src.metrics.plotting import plot_time_series
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "empty.png"
        
        # Dados vazios devem lançar erro ou criar gráfico mínimo
        try:
            plot_time_series([], [], output_path)
            # Se não lançar erro, pelo menos não deve crashar
            assert True
        except (ValueError, IndexError):
            # Erro apropriado para dados vazios
            assert True
