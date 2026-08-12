"""
Orquestração de execução de um único algoritmo.

Executa a carga de trabalho e nada mais: a coleta de métricas é responsabilidade
de programas externos e dedicados.
"""

from logging import getLogger
from typing import Callable

from config import ALGORITHMS, DEFAULT_VOLUME

logger = getLogger(__name__)


class Single:
    def run(
        self,
        algorithm: str,
        volume: int = DEFAULT_VOLUME,
    ) -> None:
        """
        Executa `volume` ciclos completos de um algoritmo.

        Args:
            algorithm: Nome do algoritmo registrado em ALGORITHMS ("KEM", "RSA", ...)
            volume: Número de operações a executar

        Raises:
            ValueError: Se algorithm inválido ou volume <= 0
        """
        algo_func = self.validate_data(algorithm, volume)

        logger.info(f"action=run_single: START algorithm={algorithm} volume={volume}")

        algo_func(volume=volume)

        logger.info(
            f"action=run_single: COMPLETE algorithm={algorithm} volume={volume}"
        )

    def validate_data(self, algorithm: str, volume: int) -> Callable:
        if algorithm not in ALGORITHMS:
            valid_algos = ", ".join(ALGORITHMS.keys())
            raise ValueError(
                f"Unknown algorithm '{algorithm}'. Valid options: {valid_algos}"
            )

        if volume <= 0:
            raise ValueError(f"Volume must be greater than 0, got {volume}")

        return ALGORITHMS[algorithm]
