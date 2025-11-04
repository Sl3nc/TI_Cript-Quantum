"""
Testes unitários para geração de relatórios.
"""
import pytest
from pathlib import Path
import tempfile


def test_build_report_creates_markdown_file():
    """Verifica que build_report cria arquivo .md."""
    from src.metrics.report_markdown import build_report
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "report.md"
        
        # Avaliação simulada
        evaluation = {
            "id": "MLKEM_1024_20251104_150530_123456",
            "algorithm": "MLKEM_1024",
            "challenge_type": "Key Encapsulation",
            "volume": 1000,
            "started_at": "2025-11-04T15:05:30.123456",
            "ended_at": "2025-11-04T15:05:32.456789",
            "duration_ms": 2333.333,
            "status": "success",
            "metrics": {
                "cpu_time_ms": 2300.5,
                "memory_mb": 45.2,
                "cpu_cycles": 5000000,
                "cache_misses": 1200
            },
            "hardware_profile": {
                "cpu_brand": "Intel i7",
                "cpu_cores": 8,
                "ram_total_gb": 16.0
            },
            "seed": 42
        }
        
        build_report(evaluation, output_path)
        
        # Arquivo deve existir
        assert output_path.exists(), "Relatório Markdown deve ser criado"
        
        # Conteúdo não vazio
        content = output_path.read_text(encoding='utf-8')
        assert len(content) > 100, "Relatório deve ter conteúdo substancial"
        
        # Deve conter informações chave
        assert "MLKEM_1024" in content
        assert "1000" in content  # volume
        assert "Key Encapsulation" in content


def test_build_report_includes_hardware_section():
    """Verifica que relatório inclui seção de hardware."""
    from src.metrics.report_markdown import build_report
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "hw_report.md"
        
        evaluation = {
            "algorithm": "Krypton",
            "volume": 500,
            "metrics": {},
            "hardware_profile": {
                "cpu_brand": "AMD Ryzen 9",
                "cpu_cores": 12,
                "cpu_threads": 24,
                "ram_total_gb": 32.0
            }
        }
        
        build_report(evaluation, output_path)
        
        content = output_path.read_text(encoding='utf-8')
        
        # Hardware info deve estar presente
        assert "Hardware" in content or "CPU" in content
        assert "AMD Ryzen 9" in content or "Ryzen" in content


def test_build_report_formats_metrics_table():
    """Verifica formatação de métricas em tabela."""
    from src.metrics.report_markdown import build_report
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "metrics_report.md"
        
        evaluation = {
            "algorithm": "MLDSA_87",
            "volume": 100,
            "metrics": {
                "cpu_time_ms": 150.75,
                "memory_mb": 22.5,
                "cpu_cycles": 300000,
                "cache_misses": 450
            },
            "hardware_profile": {}
        }
        
        build_report(evaluation, output_path)
        
        content = output_path.read_text(encoding='utf-8')
        
        # Deve conter métricas
        assert "150.75" in content or "150" in content  # CPU time
        assert "22.5" in content or "22" in content  # Memory
        
        # TODO: Validar formato de tabela Markdown (| ... |)
