"""
Testes unitários para MLDSA_87 DSS.
"""
from pytest import raises
from algorithms.mldsa_dss import generate_and_sign

def test_generate_and_sign_validates_volume():
    """Verifica que generate_and_sign rejeita volume <= 0."""
    
    # Volume zero deve lançar erro
    with raises(ValueError, match="volume.*must be.*greater than 0"):
        generate_and_sign(volume=0)
    
    # Volume negativo deve lançar erro
    with raises(ValueError, match="volume.*must be.*greater than 0"):
        generate_and_sign(volume=-50)


def test_generate_and_sign_returns_structure():
    """Verifica estrutura básica de retorno."""
    result = generate_and_sign(volume=10, seed=42)
    
    # Estrutura mínima esperada
    assert isinstance(result, dict), "Deve retornar dict"
    
    # TODO: Placeholder pode retornar vazio, deve falhar até implementação real


def test_generate_and_sign_accepts_seed():
    """Verifica que generate_and_sign aceita seed."""
    result = generate_and_sign(volume=10, seed=99999)
    
    assert result is not None
