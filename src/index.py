from argparse import ArgumentParser
from datetime import UTC, datetime
from logging import INFO, basicConfig, getLogger
from pathlib import Path

from algorithms.dh import run_diffie_hellman
from algorithms.dsa import run_dsa
from algorithms.dss import run_dss
from algorithms.kem import run_kem
from algorithms.krypton import run_krypton
from algorithms.rsa import run_rsa

PROJECT_ROOT = Path().cwd()

DEFAULT_ALGORITM = "KEM"
DEFAULT_VOLUME = 1

ALGORITHMS = {
    "KEM": run_kem,
    "DSS": run_dss,
    "Krypton": run_krypton,
    "DSA": run_dsa,
    "RSA": run_rsa,
    "Diffie-Hellman": run_diffie_hellman,
}

basicConfig(level=INFO, format="[%(levelname)s] %(message)s")
logger = getLogger(__name__)


def cli() -> tuple[str, int]:

    parser = ArgumentParser(description="Execute a single algorithm evaluation")
    _ = parser.add_argument(
        "--algorithm",
        "-a",
        type=str,
        default=DEFAULT_ALGORITM,
        choices=list(ALGORITHMS.keys()),
        help="Algorithms to run",
    )

    _ = parser.add_argument(
        "--volume", "-v", type=int, default=DEFAULT_VOLUME, help="Number of operations"
    )

    args = parser.parse_args()
    return (args.algorithm, args.volume)


def is_input_valid(algorithm: str, volume: int) -> None:
    if volume <= 0:
        raise ValueError(f"Volume must be greater than 0, got {volume}")

    if algorithm not in ALGORITHMS:
        raise ValueError(
            f"Unknown algorithm '{algorithm}'. Valid options: {', '.join(ALGORITHMS.keys())}"
        )


if __name__ == "__main__":
    algorithm, volume = cli()

    print(
        f"{'=' * 60}",
        f"Running: {algorithm} - Volume: {volume}",
        f"{'=' * 60}",
        sep="\n",
    )

    try:
        is_input_valid(algorithm, volume)
        logger.info(f"START - {datetime.now(UTC).strftime('%H:%M:%S')}")
        ALGORITHMS[algorithm](volume)
        logger.info(f"COMPLETE - {datetime.now(UTC).strftime('%H:%M:%S')}")
    except ValueError as e:
        logger.error(f"FAILED error={e}")
        raise SystemExit(1)
