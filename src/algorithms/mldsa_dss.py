"""
MLDSA_87 Digital Signature Scheme usando quantCrypt.

Princípio I da Constituição: Uso EXCLUSIVO de quantCrypt.
"""
from typing import Dict, Any
from logging import getLogger
from quantcrypt.dss import MLDSA_87

logger = getLogger(__name__)


def generate_and_sign(volume: int) -> Dict[str, Any]:
    """
    Executa operações de assinatura digital usando MLDSA_87.
    
    Args:
        volume: Número de operações (sign/verify pairs)
        seed: Seed para PRNG (reprodutibilidade)
        
    Returns:
        Dict com:
            - operations_completed: int
            - algorithm: str
            - volume: int
            - seed: int
            
    Raises:
        ValueError: Se volume <= 0
    """
    # Validação obrigatória
    if volume <= 0:
        raise ValueError(f"volume must be greater than 0, got {volume}")
    
    logger.info(f"action=DSS: START volume={volume}")

    dss = MLDSA_87()
    message = b'Hello World'
    
    # Simular assinaturas
    for _ in range(volume):
        public_key, secret_key = dss.keygen()
        signature = dss.sign(secret_key, message)
        is_valid = dss.verify(public_key, message, signature)
        assert is_valid
    
    result = {
        "operations_completed": volume,
        "algorithm": "MLDSA_87",
        "volume": volume,
    }
    
    logger.info(f"action=DSS: COMPLETE operations={volume}")
    return result
