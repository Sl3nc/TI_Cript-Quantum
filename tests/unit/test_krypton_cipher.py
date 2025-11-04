"""
Testes unitários para Krypton Cipher.
"""
import pytest


def test_cipher_rounds_validates_volume():
    """Verifica que cipher_rounds rejeita volume <= 0."""
    from src.algorithms.krypton_cipher import cipher_rounds
    
    # Volume zero deve lançar erro
    with pytest.raises(ValueError, match="volume.*must be.*greater than 0"):
        cipher_rounds(volume=0)
    
    # Volume negativo deve lançar erro
    with pytest.raises(ValueError, match="volume.*must be.*greater than 0"):
        cipher_rounds(volume=-1)


def test_cipher_rounds_returns_structure():
    """Verifica estrutura básica de retorno."""
    from src.algorithms.krypton_cipher import cipher_rounds
    
    result = cipher_rounds(volume=10, seed=42)
    
    # Estrutura mínima esperada
    assert isinstance(result, dict), "Deve retornar dict"
    
    # TODO: Placeholder pode retornar vazio


def test_cipher_rounds_accepts_seed():
    """Verifica que cipher_rounds aceita seed."""
    from src.algorithms.krypton_cipher import cipher_rounds
    
    result = cipher_rounds(volume=10, seed=777)
    
    assert result is not None
