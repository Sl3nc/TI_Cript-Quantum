from logging import INFO, basicConfig
from argparse import ArgumentParser
from config import DEFAULT_VOLUME, SEED, ALGORITHMS, RESULTS_DIR, ALGORITHMS_FUNCTIONS, DEFAULT_ALGORITM
from orchestration.single import Single

if __name__ == "__main__":
    single = Single()
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
        "--volume", "-v",
        type=int, default=DEFAULT_VOLUME,
        help="Número de operações"
    )

    parser.add_argument(
        "--seed", "-s",
        type=int, default=SEED,
        help="Seed para reprodutibilidade"
)
    
    args = parser.parse_args()
    
    print(f"\n{'='*60}")
    print(f"Executando: {args.algorithm}")
    print(f"Volume: {args.volume}")
    print(f"Seed: {args.seed}")
    print(f"{'='*60}\n")
    
    result = single.run(
        algorithm=args.algorithm,
        volume=args.volume,
        seed=args.seed
    )
    
    print(f"\n{'='*60}")
    print(f"✓ Execução concluída!")
    print(f"Status: {result['status']}")
    print(f"Duração: {result['duration_ms']:.2f} ms")
    if "report_path" in result:
        print(f"Relatório: {result['report_path']}")
    print(f"{'='*60}\n")
