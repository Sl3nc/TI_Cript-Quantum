from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from typing import Dict, Any
from logging import getLogger

logger = getLogger(__name__)

def run_diffie_hellman(volume: int) -> Dict[str, Any]:
    if volume <= 0:
        raise ValueError(f"volume must be greater than 0, got {volume}")
    
    logger.info(f"action=Diffie-Hellman: START volume={volume}")
    message = b'handshake data'

    for _ in range(volume):
        parameters = dh.generate_parameters(generator=2, key_size=2048)
        server_private_key = parameters.generate_private_key()

        peer_private_key = parameters.generate_private_key()
        shared_key = server_private_key.exchange(peer_private_key.public_key())

        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info= message,
        ).derive(shared_key)

        same_shared_key = peer_private_key.exchange(
            server_private_key.public_key()
        )
        same_derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info= message,
        ).derive(same_shared_key)

        assert derived_key == same_derived_key
    logger.info(f"action=Diffie-Hellman: COMPLETE operations={volume}")