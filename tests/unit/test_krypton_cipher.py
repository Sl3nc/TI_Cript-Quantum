"""
Testes unitários para o cipher Krypton.
"""

from pytest import raises

from algorithms.krypton import run_krypton


def test_run_krypton_validates_volume():
    """Verifica que run_krypton rejeita volume <= 0."""
    with raises(ValueError, match="volume.*must be.*greater than 0"):
        run_krypton(volume=0)

    with raises(ValueError, match="volume.*must be.*greater than 0"):
        run_krypton(volume=-100)


def test_run_krypton_executes_cycle():
    """Verifica que um ciclo completo executa sem erro."""
    run_krypton(volume=1)
