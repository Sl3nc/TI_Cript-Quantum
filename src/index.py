from logging import INFO, basicConfig
from argparse import ArgumentParser
from config import DEFAULT_VOLUME, SEED, ALGORITHMS, DEFAULT_ALGORITM
from orchestration.single import Single
from orchestration.serialization import Serialization

def cli():
    basicConfig(
        level= INFO,
        format="[%(levelname)s] %(message)s"
    )
    
    parser = ArgumentParser(description="Execute uma avaliação única de algoritmo")
    parser.add_argument(
        "--algorithm", "-a",
        default=DEFAULT_ALGORITM,                
        choices=list(ALGORITHMS.keys()),
        help="Algoritmo a executar"
    )

    parser.add_argument(
        "--volume", "-v", nargs="+",
        type=list, default=DEFAULT_VOLUME,
        help="Número de operações"
    )

    parser.add_argument(
        "--seed", "-s",
        type=int, default=SEED,
        help="Seed para reprodutibilidade"
    )   
    
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = cli()
    
    print(f"\n{'='*60}")
    print(f"Executando: {args.algorithm}")
    print(f"Volume: {args.volume}")
    print(f"Seed: {args.seed}")
    print(f"{'='*60}\n")
    
    result = Serialization().run(
            algorithm=args.algorithm,
            volumes=args.volume,
            seed=args.seed
        ) if len(args.volume) > 1 else Single().run(
            algorithm=args.algorithm,
            volume=args.volume,
            seed=args.seed
        )

    
    print(f"\n{'='*60}")
    print(f"✓ Execução concluída!")
    print(f"Status: {result['status']}")
    print(f"Duração: {result['duration_ms']:.2f} ms")
    print(f"Volumes testados: {len(result['evaluations'])}")
    if "report_path" in result:
        print(f"Relatório: {result['report_path']}")
    print(f"{'='*60}\n")
