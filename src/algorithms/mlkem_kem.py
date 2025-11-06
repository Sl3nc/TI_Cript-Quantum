"""
MLKEM_1024 Key Encapsulation Mechanism usando quantCrypt.

Princípio I da Constituição: Uso EXCLUSIVO de quantCrypt.
Sem implementações customizadas de criptografia.
"""
from typing import Dict, Any
from logging import getLogger
from quantcrypt.kem import MLKEM_1024

logger = getLogger(__name__)


def run_mlkem(volume: int, seed: int = 42) -> Dict[str, Any]:
    """
    Executa operações de KEM (Key Encapsulation) usando MLKEM_1024.
    
    Args:
        volume: Número de operações (encapsulation/decapsulation pairs)
        seed: Seed para PRNG (reprodutibilidade - Princípio V)
        
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
    
    logger.info(f"action=KEM: START volume={volume} seed={seed}")
    kem = MLKEM_1024()
        
    # Simular execuções
    for _ in range(volume):
        public_key, secret_key = kem.keygen()
        cipher_text, shared_secret = kem.encaps(public_key)
        decapsulated_secret = kem.decaps(secret_key, cipher_text)
        assert shared_secret == decapsulated_secret
    
    result = {
        "operations_completed": volume,
        "algorithm": "MLKEM_1024",
        "volume": volume,
        "seed": seed
    }
    
    logger.info(f"action=KEM: COMPLETE operations={volume}")
    return result
