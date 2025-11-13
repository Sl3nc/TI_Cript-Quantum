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
