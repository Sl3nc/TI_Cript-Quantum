"""
Estatísticas de sistema (CPU, processos) usando psutil.
"""
import psutil
from typing import Optional, List
from metrics.system_stat_sample import SystemStatSample
import time
import logging
import threading

logger = logging.getLogger(__name__)

class SystemSampler:
    """Amostrador contínuo de estatísticas de sistema.

    Uso típico:
        sampler = SystemSampler()
        sampler.start(interval=0.05)  # 50ms
        ... executar workload ...
        metrics = sampler.stop()

    Enquanto ativo, uma thread coleta amostras de CPU% e memória% periodicamente.
    """

    def __init__(self):
        self.process = psutil.Process()
        self.samples: List[SystemStatSample] = []
        self._sampling = False
        self._thread: Optional[threading.Thread] = None
        self._stop_event: Optional[threading.Event] = None
        
    def start(self, interval: float = 0.05) -> None:
        """Inicia amostragem assíncrona.

        Args:
            interval: Intervalo entre amostras em segundos (default 50ms).
        """
        if self._sampling:
            logger.debug("SystemSampler already running; ignoring second start().")
            return
        self._sampling = True
        self.samples = []
        self._stop_event = threading.Event()

        def _loop():
            # Primeira chamada de cpu_percent pode retornar 0; fazer uma leitura inicial descartada.
            try:
                self.process.cpu_percent(interval=None)
            except Exception:
                pass
            while not self._stop_event.is_set():
                try:
                    sample = self.sample()
                    self.samples.append(sample)
                except Exception as e:
                    logger.debug(f"Failed to collect system sample: {e}")
                # Intervalo adaptativo simples: dormir período solicitado.
                time.sleep(interval)

        self._thread = threading.Thread(target=_loop, name="SystemSamplerThread", daemon=True)
        self._thread.start()
        logger.debug(f"action=system_sampler START interval={interval}s")

    def sample(self) -> SystemStatSample:
        """Coleta uma única amostra imediata (modo síncrono)."""
        return SystemStatSample(
            timestamp=time.time(),
            cpu_percent=self.process.cpu_percent(interval=None),
            memory_percent=self.process.memory_percent(),
        )

    def stop(self) -> dict:
        """Para amostragem e agrega resultados."""
        if not self._sampling:
            logger.debug("SystemSampler.stop() called but sampler not active.")
        self._sampling = False

        if self._stop_event:
            self._stop_event.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)
        self._thread = None

        if not self.samples:
            logger.warning("SystemSampler.stop() no samples collected.")
            return {
                "cpu_percent_avg": 0.0,
                "memory_percent_max": 0.0,
            }

        avg_cpu = sum(s.cpu_percent for s in self.samples) / len(self.samples)
        max_mem = max(s.memory_percent for s in self.samples) * 100

        logger.info(
            f"action=system_stats_aggregated cpu_avg={avg_cpu:.2f} mem_max={max_mem:.2f}"
        )
        return {
            "cpu_percent_avg": avg_cpu,
            "memory_percent_max": max_mem,
        }
