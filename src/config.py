"""
Configuração centralizada para execuções.
"""
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

# Parâmetros de execução
DEFAULT_ALGORITM = 'KEM'
DEFAULT_VOLUME = 1

# Algoritmos suportados
ALGORITHMS = {
    "KEM": run_kem,
    "DSS": run_dss,
    "Krypton": run_krypton,
    "DSA": run_dsa,
    "RSA": run_rsa,
    "Diffie-Hellman": run_diffie_hellman
}
