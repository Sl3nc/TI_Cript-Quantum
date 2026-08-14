"""
Testes unitários para MLDSA_87 DSS.
"""

from pytest import raises

from algorithms.dss import run_dss


def test_run_dss_validates_volume():
    """Verifica que run_dss rejeita volume <= 0."""
    with raises(ValueError, match="volume.*must be.*greater than 0"):
        run_dss(volume=0)

    with raises(ValueError, match="volume.*must be.*greater than 0"):
        run_dss(volume=-100)


def test_run_dss_executes_cycle():
    """Verifica que um ciclo completo executa sem erro."""
    run_dss(volume=1)
