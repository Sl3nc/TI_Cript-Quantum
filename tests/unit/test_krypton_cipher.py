"""
Testes unitários para Krypton Cipher.
"""
from pytest import raises
from algorithms.krypton import run_krypton

def test_cipher_rounds_validates_volume():
    """Verifica que cipher_rounds rejeita volume <= 0."""
    from algorithms.krypton import run_krypton
    
    # Volume zero deve lançar erro
    with raises(ValueError, match="volume.*must be.*greater than 0"):
        run_krypton(volume=0)
    
    # Volume negativo deve lançar erro
    with raises(ValueError, match="volume.*must be.*greater than 0"):
        run_krypton(volume=-1)


def test_cipher_rounds_returns_structure():
    """Verifica estrutura básica de retorno."""
    result = run_krypton(volume=10, seed=42)
    
    # Estrutura mínima esperada
    assert isinstance(result, dict), "Deve retornar dict"
    
    # TODO: Placeholder pode retornar vazio


def test_cipher_rounds_accepts_seed():
    """Verifica que cipher_rounds aceita seed."""
    result = run_krypton(volume=10, seed=777)
    
    assert result is not None
