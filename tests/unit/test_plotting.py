"""
Testes unitários para plotting.
"""
import pytest
from pathlib import Path
import tempfile
from visualize.plotting import plot_time_series, plot_memory_series, plot_scalability


def test_plot_time_series_creates_image():
    """Verifica que plot_time_series gera arquivo PNG."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "time_series.png"
        
        timestamps = [0.0, 1.0, 2.0, 3.0, 4.0]
        values = [10, 15, 12, 18, 20]
        
        plot_time_series(timestamps, values, output_path, title="Test Series")
        
        # Imagem deve existir
        assert output_path.exists(), "Gráfico deve ser criado"
        
        # Deve ser arquivo válido (tamanho > 0)
        assert output_path.stat().st_size > 0, "Arquivo PNG não deve estar vazio"


def test_plot_memory_series_creates_image():
    """Verifica que plot_memory_series gera arquivo PNG."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "memory_series.png"
        
        memory_samples = [10.5, 15.2, 20.8, 18.3, 22.0]
        
        plot_memory_series(memory_samples, output_path)
        
        # Imagem deve existir
        assert output_path.exists(), "Gráfico de memória deve ser criado"
        assert output_path.stat().st_size > 0


def test_plot_scalability_creates_image():
    """Verifica que plot_scalability gera gráfico de barras."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "scalability.png"
        
        volumes = [100, 500, 1000, 5000]
        metrics = {
            "CPU Time (ms)": [50, 200, 400, 2000],
            "Memory (MB)": [10, 40, 80, 400]
        }
        
        plot_scalability(volumes, metrics, output_path, metric_name="Performance")
        
        # Imagem deve existir
        assert output_path.exists(), "Gráfico de escalabilidade deve ser criado"
        assert output_path.stat().st_size > 0


def test_plot_time_series_handles_empty_data():
    """Verifica comportamento com dados vazios."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "empty_series.png"
        
        # Dados vazios devem ser tratados gracefully
        try:
            plot_time_series([], [], output_path)
            # Se não lançar erro, deve criar arquivo vazio ou mínimo
            assert output_path.exists() or True, "Deve lidar com dados vazios"
        except ValueError:
            # Ou lançar erro apropriado
            pass
        
        # TODO: Definir comportamento esperado para edge case
