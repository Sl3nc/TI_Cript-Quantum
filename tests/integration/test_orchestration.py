"""
Testes de integração da orquestração: validação + execução, sem coleta de métricas.
"""

from pytest import raises

from orchestration.serialization import Serialization
from orchestration.single import Single


def test_single_runs_algorithm():
    """Single executa a carga de trabalho de um algoritmo registrado."""
    Single().run(algorithm="Krypton", volume=1)


def test_single_rejects_unknown_algorithm():
    """Single rejeita algoritmo fora de ALGORITHMS."""
    with raises(ValueError, match="Unknown algorithm"):
        Single().run(algorithm="Inexistente", volume=1)


def test_single_rejects_invalid_volume():
    """Single rejeita volume <= 0."""
    with raises(ValueError, match="Volume must be greater than 0"):
        Single().run(algorithm="Krypton", volume=0)


def test_serialization_runs_all_algorithms():
    """Serialization executa cada algoritmo da lista sob o mesmo volume."""
    Serialization().run(algorithms=["Krypton", "KEM"], volume=1)


def test_serialization_rejects_empty_list():
    """Serialization rejeita lista vazia de algoritmos."""
    with raises(ValueError, match="algorithms list must not be empty"):
        Serialization().run(algorithms=[], volume=1)


def test_serialization_validates_before_running():
    """Um nome inválido na lista aborta antes de executar qualquer algoritmo."""
    with raises(ValueError, match="Unknown algorithm"):
        Serialization().run(algorithms=["Krypton", "Inexistente"], volume=1)
