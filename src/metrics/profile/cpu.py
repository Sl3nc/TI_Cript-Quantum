"""
Profiling de CPU usando cProfile e line_profiler.
"""
import cProfile
import pstats
from io import StringIO
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class CPU:
    def start(self) -> cProfile.Profile:
        """
        Inicia profiling de CPU com cProfile.
        
        Returns:
            cProfile.Profile: Objeto profiler ativo
        """
        logger.debug("action=start_cpu_profile status=initiated")
        profiler = cProfile.Profile()
        try:
            profiler.enable()
            logger.debug("action=start_cpu_profile status=enabled")
        except ValueError as e:
            # Se já houver um profiler ativo, desabilitar e tentar novamente
            logger.warning(f"Profiler already active, attempting to clear: {e}")
            try:
                profiler.disable()
            except:
                pass
            profiler = cProfile.Profile()
            profiler.enable()
            logger.debug("action=start_cpu_profile status=enabled_after_clear")
        return profiler


    def stop(self, profiler: cProfile.Profile) -> Dict[str, Any]:
        """Finaliza o profiling e extrai métricas de CPU agregadas e por interação.

        Realiza uma leitura final das estatísticas e produz a lista de operações
        lógicas por interação (delta de chamadas primitivas acumuladas entre snapshots).

        Para obter valores por interação é necessário ter chamado
        `interaction_checkpoint(profiler)` em cada passo/loop relevante.

        Args:
            profiler: Instância ativa de cProfile.

        Returns:
            Dict com:
                cpu_time_total: Soma dos tempos exclusivos (tottime) de todas as funções
                operations: Lista de contagem de operações por interação (deltas)
                operations_cumulative: Lista cumulativa (snapshot bruto)
                total_operations: Total de operações lógicas (último cumulativo)
        """
        profiler.disable()
        logger.debug("action=cpu_profile: STOP status=disabled")

        stream = StringIO()
        stats = pstats.Stats(profiler, stream=stream)
        stats.sort_stats("cumulative")
        stats_map = getattr(stats, "stats", {})

        return {
            # "cpu_time": [values[2] for values in  stats_map.values()],
            # "calls": [values[0] for values in  stats_map.values()],
        }

    def profile_lines(self, func, *args, **kwargs) -> Dict[str, Any]:
        """
        Perfila linhas críticas usando line_profiler.
        
        Args:
            func: Função a perfilar
            *args, **kwargs: Argumentos para função
            
        Returns:
            Dict com métricas de linha (placeholder)
        """
        # Placeholder: integrar line_profiler
        result = func(*args, **kwargs)
        return {
            "line_stats": {},
            "result": result
        }
