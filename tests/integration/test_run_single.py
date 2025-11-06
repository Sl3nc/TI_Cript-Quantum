"""
Teste de integração para run_single (US1).
"""
import pytest
from pathlib import Path


def test_run_single_end_to_end():
    """
    Testa execução completa: algoritmo → métricas → resultado.
    """
    from src.orchestration.run_single import run_single
    
    result = run_single(algorithm="MLKEM_1024", volume=100, seed=42)
    
    # Estrutura esperada (AlgorithmEvaluation)
    assert "algorithm" in result
    assert "volume" in result
    assert "metrics" in result
    assert "status" in result
    assert "started_at" in result
    assert "ended_at" in result
    
    # Valores corretos
    assert result["algorithm"] == "MLKEM_1024"
    assert result["volume"] == 100
    assert result["seed"] == 42
    
    # Status deve ser success
    assert result["status"] == "success"


def test_run_single_collects_minimum_metrics():
    """
    Valida que métricas mínimas são coletadas (Princípio II).
    
    Métricas obrigatórias: cpu_time, memory, cpu_cycles, hardware_info
    """
    from src.orchestration.run_single import run_single
    
    result = run_single(algorithm="Krypton", volume=50, seed=99)
    
    # Deve ter métricas
    assert "metrics" in result
    metrics = result["metrics"]
    
    # CPU time presente
    assert "cpu_time_ms" in metrics, "CPU time é métrica obrigatória"
    
    # Memória presente
    assert "memory_mb" in metrics, "Memory é métrica obrigatória"
    
    # CPU cycles (pode ser None se fallback)
    assert "cpu_cycles" in metrics, "CPU cycles deve estar presente (None se unavailable)"
    
    # Hardware info
    assert "hardware_profile" in result, "Hardware profile é obrigatório"
    hw = result["hardware_profile"]
    assert isinstance(hw, dict), "Hardware profile deve ser dict"


def test_run_single_validates_algorithm():
    """Verifica que run_single rejeita algoritmo inválido."""
    from src.orchestration.run_single import run_single
    
    with pytest.raises(ValueError, match="Unknown algorithm"):
        run_single(algorithm="INVALID_ALGO", volume=100)


def test_run_single_validates_volume():
    """Verifica que run_single propaga validação de volume."""
    from src.orchestration.run_single import run_single
    
    with pytest.raises(ValueError, match="volume.*must be.*greater than 0"):
        run_single(algorithm="MLKEM_1024", volume=0)


def test_run_single_different_algorithms():
    """Testa que os 3 algoritmos podem ser executados."""
    from src.orchestration.run_single import run_single
    
    algorithms = ["MLKEM_1024", "MLDSA_87", "Krypton"]
    
    for algo in algorithms:
        result = run_single(algorithm=algo, volume=10, seed=42)
        
        assert result["status"] == "success", f"{algo} deve executar com sucesso"
        assert result["algorithm"] == algo
        assert "metrics" in result
