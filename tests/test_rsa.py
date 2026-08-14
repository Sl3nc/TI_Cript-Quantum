"""
Testes unitários para RSA (baseline clássico).
"""

from pytest import raises

from algorithms.rsa import run_rsa


def test_run_rsa_validates_volume():
    """Verifica que run_rsa rejeita volume <= 0."""
    with raises(ValueError, match="volume.*must be.*greater than 0"):
        run_rsa(volume=0)

    with raises(ValueError, match="volume.*must be.*greater than 0"):
        run_rsa(volume=-100)


def test_run_rsa_executes_cycle():
    """Verifica que um ciclo completo executa sem erro."""
    run_rsa(volume=1)
