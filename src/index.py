from config import DEFAULT_VOLUME, ALGORITHMS, DEFAULT_ALGORITM, DEVELOP_DIR
from orchestration.serialization import Serialization
from orchestration.single import Single
from logging import INFO, basicConfig
from argparse import ArgumentParser
from sys import path

def cli():
    basicConfig(
        level= INFO,
        format="[%(levelname)s] %(message)s"
    )
    
    parser = ArgumentParser(description="Execute uma avaliação única de algoritmo")
    parser.add_argument(
        "--algorithm", "-a",
        default=[DEFAULT_ALGORITM], nargs="+",
        choices=list(ALGORITHMS.keys()),
        help="Algoritmos a executar"
    )

    parser.add_argument(
        "--volume", "-v", type=int, default=DEFAULT_VOLUME,
        help="Número de operações"
    )
    
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    if str(DEVELOP_DIR) not in path:
        path.insert(0, str(DEVELOP_DIR))

    args = cli()
    
    print(f"\n{'='*60}")
    print(f"Executando:", *args.algorithm)
    print(f"Volume: {args.volume}")
    print(f"{'='*60}\n")
    
    result = Serialization().run(
            algorithm=args.algorithm,
            volumes=args.volume,
        ) if len(args.algorithm) > 1 else Single().run(
            algorithm=args.algorithm[0],
            volume=args.volume,
        )

    
    print(f"\n{'='*60}")
    print(f"✓ Execução concluída!")
    print(f"Status: {result['status']}")
    print(f"Duração: {result['duration_min']:.2f} ms")
    if "report_path" in result:
        print(f"Relatório: {result['report_path']}")
    print(f"{'='*60}\n")
