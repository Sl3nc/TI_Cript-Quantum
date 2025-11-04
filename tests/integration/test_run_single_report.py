"""
Teste de integração para run_single com geração de relatório (US2).
"""
import pytest
from pathlib import Path
import tempfile
import shutil


def test_run_single_generates_complete_report():
    """
    Testa que run_single gera relatório Markdown + gráficos.
    
    Este teste valida integração completa US1 + US2.
    """
    from src.orchestration.run_single import run_single
    from src.orchestration.config import RESULTS_DIR
    
    # Executar avaliação
    result = run_single(algorithm="MLKEM_1024", volume=50, seed=42)
    
    # Deve ter path do relatório
    assert "report_path" in result, "Resultado deve incluir caminho do relatório"
    
    report_path = Path(result["report_path"])
    
    # Relatório deve existir
    assert report_path.exists(), f"Relatório deve existir em {report_path}"
    
    # Conteúdo não vazio
    content = report_path.read_text(encoding='utf-8')
    assert len(content) > 200, "Relatório deve ter conteúdo substancial"
    
    # Deve conter informações chave
    assert "MLKEM_1024" in content
    assert "50" in content  # volume
    
    # Deve ter gráficos referenciados
    assert "report_images" in result, "Resultado deve listar imagens geradas"
    images = result["report_images"]
    
    # Pelo menos 1 imagem gerada
    assert len(images) > 0, "Deve gerar pelo menos 1 gráfico"
    
    # Imagens devem existir
    for img_path_str in images:
        img_path = Path(img_path_str)
        assert img_path.exists(), f"Imagem {img_path} deve existir"
        assert img_path.suffix == ".png", "Imagens devem ser PNG"


def test_report_naming_includes_timestamp():
    """Verifica que nome do relatório inclui timestamp PT-BR."""
    from src.orchestration.run_single import run_single
    
    result = run_single(algorithm="Krypton", volume=10, seed=99)
    
    report_path = Path(result["report_path"])
    filename = report_path.name
    
    # Formato: Krypton - DD-MM-YYYY HHhMMmSSs.mmm.md
    assert "Krypton" in filename
    assert ".md" in filename
    
    # Deve ter padrão de timestamp (contém 'h' e 'm')
    assert "h" in filename and "m" in filename


def test_report_uniqueness_on_rapid_execution():
    """
    Valida unicidade: 3 execuções rápidas geram 3 relatórios distintos.
    
    Testa constraint de milissegundos para unicidade (Research decision #6).
    """
    from src.orchestration.run_single import run_single
    import time
    
    results = []
    for i in range(3):
        result = run_single(algorithm="MLDSA_87", volume=5, seed=i)
        results.append(result)
        time.sleep(0.01)  # 10ms entre execuções
    
    # 3 relatórios distintos
    report_paths = [r["report_path"] for r in results]
    
    assert len(set(report_paths)) == 3, "3 execuções devem gerar 3 relatórios únicos"
    
    # Todos devem existir
    for path_str in report_paths:
        assert Path(path_str).exists()


def test_report_includes_hardware_metadata():
    """Verifica que relatório inclui metadados de hardware."""
    from src.orchestration.run_single import run_single
    
    result = run_single(algorithm="MLKEM_1024", volume=20, seed=42)
    
    report_path = Path(result["report_path"])
    content = report_path.read_text(encoding='utf-8')
    
    # Deve conter seção de hardware
    assert "Hardware" in content or "CPU" in content
    
    # Hardware profile deve estar no resultado
    assert "hardware_profile" in result
    hw = result["hardware_profile"]
    
    # Informações básicas devem estar presentes
    assert "cpu_brand" in hw or "cpu_cores" in hw
