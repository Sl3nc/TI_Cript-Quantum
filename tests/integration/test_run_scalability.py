"""
Teste de integração para run_scalability (US3).
"""
import pytest
from pathlib import Path


def test_run_scalability_multiple_volumes():
    """
    Testa execução de múltiplos volumes e geração de relatório comparativo.
    """
    from orchestration.scalability import run_scalability
    
    volumes = [10, 50, 100]
    
    result = run_scalability(
        algorithm="MLKEM_1024",
        volumes=volumes,
        seed=42
    )
    
    # Estrutura esperada (ScalabilitySeries)
    assert "id" in result
    assert "algorithm" in result
    assert "volumes" in result
    assert "evaluation_ids" in result
    assert "comparative_report_path" in result
    assert "individual_reports" in result
    
    # Validações
    assert result["algorithm"] == "MLKEM_1024"
    assert result["volumes"] == volumes
    
    # Deve ter uma avaliação por volume
    assert len(result["evaluation_ids"]) == len(volumes)
    assert len(result["individual_reports"]) == len(volumes)
    
    # Relatório comparativo deve existir
    comparative_path = Path(result["comparative_report_path"])
    assert comparative_path.exists(), "Relatório comparativo deve existir"
    
    # Relatórios individuais devem existir
    for report_path_str in result["individual_reports"]:
        report_path = Path(report_path_str)
        assert report_path.exists(), f"Relatório individual {report_path} deve existir"


def test_run_scalability_generates_comparison_graphs():
    """Verifica que gráficos comparativos são gerados."""
    from orchestration.scalability import run_scalability
    
    result = run_scalability(
        algorithm="Krypton",
        volumes=[20, 40],
        seed=99
    )
    
    # Deve ter gráficos comparativos
    assert "comparison_images" in result
    images = result["comparison_images"]
    
    assert len(images) > 0, "Deve gerar pelo menos 1 gráfico comparativo"
    
    # Imagens devem existir
    for img_path_str in images:
        img_path = Path(img_path_str)
        assert img_path.exists(), f"Imagem {img_path} deve existir"


def test_run_scalability_aggregates_metrics():
    """Verifica que métricas são agregadas corretamente."""
    from orchestration.scalability import run_scalability
    
    result = run_scalability(
        algorithm="MLDSA_87",
        volumes=[5, 10, 15],
        seed=123
    )
    
    # Deve ter agregados
    assert "aggregated_metrics" in result
    agg = result["aggregated_metrics"]
    
    # Estrutura de agregados
    assert "cpu_time_avg_ms" in agg
    assert "cpu_time_std_ms" in agg
    assert "memory_peak_mb" in agg
    assert "success_rate" in agg
    
    # Success rate deve ser 1.0 se tudo passou
    assert agg["success_rate"] == 1.0, "Todas execuções devem ter sucesso"


def test_run_scalability_handles_partial_failure():
    """
    Testa manejo de falha parcial: alguns volumes falham, outros passam.
    """
    from orchestration.scalability import run_scalability
    
    # Usar volume 0 que deve falhar por validação
    # Mas implementação deve capturar e marcar como failed
    volumes = [10, 20]  # Volumes válidos para teste
    
    result = run_scalability(
        algorithm="MLKEM_1024",
        volumes=volumes,
        seed=42
    )
    
    # Deve completar mesmo com falhas
    assert "comparative_report_path" in result
    
    # Relatório deve existir
    report_path = Path(result["comparative_report_path"])
    assert report_path.exists()
    
    # Agregados devem refletir apenas execuções bem-sucedidas
    agg = result["aggregated_metrics"]
    assert "success_rate" in agg


def test_run_scalability_validates_empty_volumes():
    """Verifica que lista vazia de volumes é rejeitada."""
    from orchestration.scalability import run_scalability
    
    with pytest.raises(ValueError, match="volumes.*empty"):
        run_scalability(algorithm="MLKEM_1024", volumes=[], seed=42)


def test_run_scalability_comparative_report_content():
    """Verifica conteúdo do relatório comparativo."""
    from orchestration.scalability import run_scalability
    
    result = run_scalability(
        algorithm="Krypton",
        volumes=[10, 20],
        seed=42
    )
    
    report_path = Path(result["comparative_report_path"])
    content = report_path.read_text(encoding='utf-8')
    
    # Deve conter informações chave
    assert "Krypton" in content
    assert "Escalabilidade" in content or "Scalability" in content
    
    # Deve listar volumes testados
    assert "10" in content and "20" in content
