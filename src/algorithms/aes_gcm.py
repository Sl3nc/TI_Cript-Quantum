"""
AES-GCM Cipher usando biblioteca cryptography.

Implementa operações de cifração/decifração para validação funcional
similar ao fluxo em `krypton.py`.
"""
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from typing import Dict, Any
from logging import getLogger
import secrets

logger = getLogger(__name__)

def cipher_aes(volume: int) -> Dict[str, Any]:
    """Executa pares encrypt/decrypt usando AES-GCM.

    Args:
        volume: Número de operações (encrypt/decrypt pairs) a executar.
        seed: Seed opcional para reprodutibilidade (não garante chave igual
              pois AESGCM.generate_key usa os.urandom; usado apenas para
              debug determinístico em geração de nonce alternativa).

    Returns:
        Dict com metadados da execução:
            - operations_completed: int
            - algorithm: str ("AES-GCM")
            - volume: int
            - seed: int | None

    Raises:
        ValueError: Se volume <= 0.
    """
    if volume <= 0:
        raise ValueError(f"volume must be greater than 0, got {volume}")
    
    logger.info(f"action=AES-GCM: START volume={volume}")
    plaintext = b"Hello World"
    key = AESGCM().generate_key(bit_length=256)
    nonce = secrets.token_bytes(12)

    for _ in range(volume):
        aesgcm = AESGCM(key)
        ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data=None)
        decrypted = aesgcm.decrypt(nonce, ciphertext, associated_data=None)
        assert decrypted == plaintext, "Decrypted plaintext divergence"

    logger.info(f"action=AES-GCM: COMPLETE operations={volume}")