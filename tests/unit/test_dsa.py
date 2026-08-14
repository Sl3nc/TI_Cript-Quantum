"""
Testes unitários para DSA (baseline clássico).
"""

from pytest import raises

from algorithms.dsa import run_dsa


def test_run_dsa_validates_volume():
    """Verifica que run_dsa rejeita volume <= 0."""
    with raises(ValueError, match="volume.*must be.*greater than 0"):
        run_dsa(volume=0)

    with raises(ValueError, match="volume.*must be.*greater than 0"):
        run_dsa(volume=-100)


def test_run_dsa_executes_cycle():
    """Verifica que um ciclo completo executa sem erro."""
    run_dsa(volume=1)
