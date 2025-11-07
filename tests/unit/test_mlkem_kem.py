"""
Testes unitários para MLKEM_1024 KEM.
"""
from pytest import raises
from algorithms.mlkem_kem import run_mlkem

def test_run_mlkem_validates_volume():
    """Verifica que run_mlkem rejeita volume <= 0."""
    # Volume zero deve lançar erro
    with raises(ValueError, match="volume.*must be.*greater than 0"):
        run_mlkem(volume=0)
    
    # Volume negativo deve lançar erro
    with raises(ValueError, match="volume.*must be.*greater than 0"):
        run_mlkem(volume=-100)


def test_run_mlkem_returns_structure():
    """Verifica estrutura básica de retorno antes de implementação completa."""
    
    # Placeholder deve retornar dict com campos esperados
    result = run_mlkem(volume=10, seed=42)
    
    # Estrutura mínima esperada
    assert isinstance(result, dict), "Deve retornar dict"
    
    # TODO: Implementação placeholder pode retornar estrutura vazia
    # Este teste falhará até implementarmos lógica real do quantCrypt


def test_run_mlkem_accepts_seed():
    """Verifica que run_mlkem aceita seed para reprodutibilidade."""
    # Deve aceitar seed sem erro
    result = run_mlkem(volume=10, seed=12345)
    
    assert result is not None
    
    # TODO: Validar que mesmo seed produz mesmos resultados
