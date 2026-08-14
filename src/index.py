from argparse import ArgumentParser
from logging import INFO, basicConfig, getLogger
from sys import path

from config import ALGORITHMS, DEFAULT_ALGORITM, DEFAULT_VOLUME, DEVELOP_DIR
from orchestration.serialization import Serialization
from orchestration.single import Single


def cli():
    basicConfig(level=INFO, format="[%(levelname)s] %(message)s")

    parser = ArgumentParser(description="Execute uma avaliação única de algoritmo")
    parser.add_argument(
        "--algorithm",
        "-a",
        default=[DEFAULT_ALGORITM],
        nargs="+",
        choices=list(ALGORITHMS.keys()),
        help="Algoritmos a executar",
    )

    parser.add_argument(
        "--volume", "-v", type=int, default=DEFAULT_VOLUME, help="Número de operações"
    )

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    if str(DEVELOP_DIR) not in path:
        path.insert(0, str(DEVELOP_DIR))

    args = cli()

    print(f"\n{'=' * 60}")
    print("Executando:", *args.algorithm)
    print(f"Volume: {args.volume}")
    print(f"{'=' * 60}\n")

    try:
        if len(args.algorithm) > 1:
            Serialization().run(
                algorithms=args.algorithm,
                volume=args.volume,
            )
        else:
            Single().run(
                algorithm=args.algorithm[0],
                volume=args.volume,
            )
    except Exception as e:
        getLogger(__name__).error(f"action=cli: FAILED error={e}")
        raise SystemExit(1)

    print(
        f"\n{'=' * 20}",
        "Execução concluída",
        f"{'=' * 20}",
    )
    print(f"{'=' * 60}\n")
