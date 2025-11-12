"""Testes unitários para AES-GCM Cipher."""
from pytest import raises
from algorithms.aes_gcm import cipher_rounds


def test_cipher_rounds_validates_volume_aes_gcm():
    with raises(ValueError, match="volume.*must be.*greater than 0"):
        cipher_rounds(volume=0)
    with raises(ValueError, match="volume.*must be.*greater than 0"):
        cipher_rounds(volume=-5)


def test_cipher_rounds_returns_structure_aes_gcm():
    result = cipher_rounds(volume=5, seed=123)
    assert isinstance(result, dict)
    assert result.get("algorithm") == "AES-GCM"
    assert result.get("operations_completed") == 5


def test_cipher_rounds_seed_optional_aes_gcm():
    r1 = cipher_rounds(volume=2)
    r2 = cipher_rounds(volume=2, seed=999)
    assert r1["operations_completed"] == r2["operations_completed"] == 2
