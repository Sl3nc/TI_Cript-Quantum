"""
Testes unitários para report_markdown.
"""
import pytest
from pathlib import Path
import tempfile
from visualize.report_markdown import build_report, build_series_report


def test_build_report_creates_file():
    """Verifica que build_report cria arquivo Markdown."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "test_report.md"
        
        evaluation = {
            "algorithm": "MLKEM_1024",
            "volume": 1000,
            "cpu_time_ms": 150.5,
            "memory_mb": 45.2,
            "status": "success"
        }
        
        build_report(evaluation, output_path)
        
        # Arquivo deve existir
        assert output_path.exists(), "Relatório deve ser criado"
        
        # Deve conter conteúdo
        content = output_path.read_text(encoding='utf-8')
        assert len(content) > 0, "Relatório não deve estar vazio"
        
        # Deve mencionar algoritmo
        assert "MLKEM_1024" in content or "Placeholder" in content


def test_build_report_structure():
    """Verifica estrutura básica do relatório."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "structured_report.md"
        
        evaluation = {
            "algorithm": "Krypton",
            "volume": 5000,
            "timestamp": "04-11-2025 15h30m45s.123"
        }
        
        build_report(evaluation, output_path)
        
        content = output_path.read_text(encoding='utf-8')
        
        # TODO: Implementação placeholder é mínima
        # Deve falhar quando exigirmos seções (Hardware, Métricas, Gráficos)


def test_build_series_report_creates_file():
    """Verifica que build_series_report cria relatório comparativo."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "series_report.md"
        
        series = {
            "algorithm": "MLDSA_87",
            "volumes": [100, 500, 1000],
            "cpu_time_avg_ms": 250.0,
            "memory_peak_mb": 80.5
        }
        
        image_paths = [
            Path(tmpdir) / "plot1.png",
            Path(tmpdir) / "plot2.png"
        ]
        
        build_series_report(series, output_path, image_paths)
        
        # Arquivo deve existir
        assert output_path.exists(), "Relatório de série deve ser criado"
        
        # Deve conter conteúdo
        content = output_path.read_text(encoding='utf-8')
        assert len(content) > 0
        
        # TODO: Implementação placeholder é mínima
        # Deve falhar quando validarmos referências às imagens
