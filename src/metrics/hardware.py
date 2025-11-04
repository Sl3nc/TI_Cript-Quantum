"""
Snapshot de informações de hardware usando py-cpuinfo.
"""
import psutil
import cpuinfo
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


def snapshot_hardware() -> Dict[str, Any]:
    """
    Captura informações de hardware do sistema.
    
    Returns:
        Dict com:
            - cpu_brand: str
            - cpu_arch: str
            - cpu_cores: int (físicos)
            - cpu_threads: int (lógicos)
            - cpu_freq_mhz: float (atual)
            - ram_total_gb: float
            - platform: str (OS)
            
    Nota: Se coleta falhar, retorna dict com campos None e warning_logged=True
    """
    try:
        cpu_info = cpuinfo.get_cpu_info()
        
        hw_info = {
            "cpu_brand": cpu_info.get("brand_raw", "Unknown"),
            "cpu_arch": cpu_info.get("arch", "Unknown"),
            "cpu_cores": psutil.cpu_count(logical=False) or 0,
            "cpu_threads": psutil.cpu_count(logical=True) or 0,
            "cpu_freq_mhz": psutil.cpu_freq().current if psutil.cpu_freq() else 0.0,
            "ram_total_gb": psutil.virtual_memory().total / (1024**3),
            "platform": cpu_info.get("python_version", "Unknown"),
            "warning_logged": False
        }
        
        logger.info(f"action=hardware_snapshot status=success cpu_brand={hw_info['cpu_brand']} cores={hw_info['cpu_cores']}")
        return hw_info
        
    except Exception as e:
        # Fallback: retorna estrutura com Nones
        logger.warning(f"action=hardware_snapshot status=failed error={str(e)} fallback=partial_data")
        
        return {
            "cpu_brand": None,
            "cpu_arch": None,
            "cpu_cores": None,
            "cpu_threads": None,
            "cpu_freq_mhz": None,
            "ram_total_gb": None,
            "platform": None,
            "warning_logged": True,
            "error": str(e)
        }
