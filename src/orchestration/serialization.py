"""
Orquestração sequencial de múltiplos algoritmos sob o mesmo volume.
"""

from logging import getLogger
from typing import List

from config import DEFAULT_VOLUME
from orchestration.single import Single

logger = getLogger(__name__)


class Serialization:
    def run(
        self,
        algorithms: List[str],
        volume: int = DEFAULT_VOLUME,
    ) -> None:
        """
        Executa vários algoritmos em sequência, cada um com o mesmo volume.

        Args:
            algorithms: Nomes dos algoritmos registrados em ALGORITHMS
            volume: Número de operações por algoritmo

        Raises:
            ValueError: Se algorithms vazio, algorithm inválido ou volume <= 0
        """
        if not algorithms:
            raise ValueError("algorithms list must not be empty")

        single = Single()

        # Valida todos antes de executar qualquer um (fail-fast)
        for algorithm in algorithms:
            single.validate_data(algorithm, volume)

        logger.info(
            f"action=run_serialization: START algorithms={algorithms} volume={volume}"
        )

        for algorithm in algorithms:
            single.run(algorithm=algorithm, volume=volume)

        logger.info(f"action=run_serialization: COMPLETE algorithms={algorithms}")
