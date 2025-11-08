from dataclasses import dataclass
from typing import Optional

@dataclass
class SystemStatSample:
    """Amostra de estatísticas de sistema em um ponto no tempo."""
    timestamp: float
    cpu_percent: float
    memory_percent: float
    cpu_cycles: Optional[int] = None