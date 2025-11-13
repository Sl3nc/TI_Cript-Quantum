"""
Configuração centralizada para execuções.
"""
from pathlib import Path
from algorithms.krypton import cipher_rounds
from algorithms.dss import generate_and_sign
from algorithms.kem import run_mlkem
from algorithms.aes_gcm import cipher_aes
from algorithms.dsa import run_dsa

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
    "KEM": run_mlkem,
    "DSS": generate_and_sign,
    "Krypton": cipher_aes,
    "AES-GCM": cipher_rounds,
    "DSA": run_dsa
}

# Métricas obrigatórias
REQUIRED_METRICS = [
    "cpu_time_ms",
    "memory_mb",
    "cpu_cycles",
    "hardware_info"
]
