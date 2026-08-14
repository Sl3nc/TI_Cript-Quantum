from logging import INFO, basicConfig
from argparse import ArgumentParser
from sys import path
from pathlib import Path
from algorithms.krypton import run_krypton
from algorithms.dss import run_dss
from algorithms.kem import run_kem
from algorithms.dsa import run_dsa
from algorithms.rsa import run_rsa
from algorithms.dh import run_diffie_hellman

# Diretórios
PROJECT_ROOT = Path().resolve()
DEVELOP_DIR = PROJECT_ROOT / "src"
RESULTS_DIR = PROJECT_ROOT / "output"

# Parâmetros de execução
DEFAULT_ALGORITM = 'KEM'
DEFAULT_VOLUME = 1

# Timestamp format: DD-MM-YYYY HHhMMmSSs.mmm
# Unicidade: milissegundos + sufixo incremental se colisão detectada
# Exemplo: "04-11-2025 15h15m03s.127"
TIMESTAMP_FORMAT = "%d-%m-%Y %Hh%Mm%Ss"  # milliseconds adicionados via código

# Algoritmos suportados
ALGORITHMS = {
    "KEM": run_kem,
    "DSS": run_dss,
    "Krypton": run_krypton,
    "DSA": run_dsa,
    "RSA": run_rsa,
    "Diffie-Hellman": run_diffie_hellman
}

# Métricas obrigatórias
REQUIRED_METRICS = [
    "cpu_time_ms",
    "memory_mb",
    "cpu_cycles",
    "hardware_info"
]

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
    from orchestration.serialization import Serialization
    from orchestration.single import Single

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


    print(f"\n{'='*20}", f"Execução concluída", f"{'='*20}",)
    print(f"Status: {result['status']}")
    print(f"Duração: {result['duration_min']}")
    if "report_path" in result:
        print(f"Relatório: {result['report_path']}")
    print(f"{'='*60}\n")
