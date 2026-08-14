"""
Testes unitários para MLKEM_1024 KEM.
"""

from pytest import raises

from algorithms.kem import run_kem


def test_run_kem_validates_volume():
    """Verifica que run_kem rejeita volume <= 0."""
    with raises(ValueError, match="volume.*must be.*greater than 0"):
        run_kem(volume=0)

    with raises(ValueError, match="volume.*must be.*greater than 0"):
        run_kem(volume=-100)


def test_run_kem_executes_cycle():
    """Verifica que um ciclo completo executa sem erro."""
    run_kem(volume=1)
