from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dsa
from logging import getLogger

logger = getLogger(__name__)

def run_dsa(volume: int):

    if volume <= 0:
        raise ValueError(f"volume must be greater than 0, got {volume}")
    
    logger.info(f"action=DSA: START volume={volume}")

    message = b'Hello World'
    
    for _ in range(volume):
        private_key = dsa.generate_private_key(1024)
        signature = private_key.sign(
            message, hashes.SHA256()
        )

        public_key = private_key.public_key()
        public_key.verify(
            signature, message, hashes.SHA256()
        )


    logger.info(f"action=DSA: COMPLETE operations={volume}")