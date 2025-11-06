"""
Configuração centralizada para execuções.
"""
from pathlib import Path
from sys import path

# Diretórios
PROJECT_ROOT = Path().resolve()
RESULTS_DIR = PROJECT_ROOT / "docs" / "results"

if str(PROJECT_ROOT) not in path:
    path.insert(0, str(PROJECT_ROOT))

from src.algorithms.mlkem_kem import run_mlkem
from src.algorithms.mldsa_dss import generate_and_sign
from src.algorithms.krypton_cipher import cipher_rounds

# Parâmetros de execução
DEFAULT_ALGORITM = 'KEM'
DEFAULT_VOLUME = 1000
SEED = 42

# Timestamp format: DD-MM-YYYY HHhMMmSSs.mmm
# Unicidade: milissegundos + sufixo incremental se colisão detectada
# Exemplo: "04-11-2025 15h15m03s.127"
TIMESTAMP_FORMAT = "%d-%m-%Y %Hh%Mm%Ss"  # milliseconds adicionados via código

# Algoritmos suportados
ALGORITHMS = {
    "KEM": "Key Encapsulation Mechanisms",
    "DSS": "Digital Signature Shemes",
    "Krypton": "Cipher"
}

ALGORITHMS_FUNCTIONS = {
    "KEM": run_mlkem,
    "DSS": generate_and_sign,
    "Krypton": cipher_rounds
}

# Métricas obrigatórias
REQUIRED_METRICS = [
    "cpu_time_ms",
    "memory_mb",
    "cpu_cycles",
    "cache_misses",
    "hardware_info"
]
