"""
Testes unitários para Diffie-Hellman (baseline clássico).
"""

from pytest import raises

from algorithms.dh import run_diffie_hellman


def test_run_diffie_hellman_validates_volume():
    """Verifica que run_diffie_hellman rejeita volume <= 0."""
    with raises(ValueError, match="volume.*must be.*greater than 0"):
        run_diffie_hellman(volume=0)

    with raises(ValueError, match="volume.*must be.*greater than 0"):
        run_diffie_hellman(volume=-100)


def test_run_diffie_hellman_executes_cycle():
    """Verifica que um ciclo completo executa sem erro."""
    run_diffie_hellman(volume=1)
