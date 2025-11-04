"""
Configuração centralizada para execuções.
"""
from pathlib import Path

# Parâmetros de execução
DEFAULT_VOLUME = 1000
SEED = 42

# Diretórios
PROJECT_ROOT = Path(__file__).parent.parent.parent
RESULTS_DIR = PROJECT_ROOT / "docs" / "results"

# Timestamp format: DD-MM-YYYY HHhMMmSSs.mmm
# Unicidade: milissegundos + sufixo incremental se colisão detectada
# Exemplo: "04-11-2025 15h15m03s.127"
TIMESTAMP_FORMAT = "%d-%m-%Y %Hh%Mm%Ss"  # milliseconds adicionados via código

# Algoritmos suportados
ALGORITHMS = {
    "MLKEM_1024": "Key Encapsulation",
    "MLDSA_87": "Digital Signature",
    "Krypton": "Cipher"
}

# Métricas obrigatórias
REQUIRED_METRICS = [
    "cpu_time_ms",
    "memory_mb",
    "cpu_cycles",
    "cache_misses",
    "hardware_info"
]
