from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dsa


def run_dsa(volume: int):
    message = b"Hello World"

    for _ in range(volume):
        private_key = dsa.generate_private_key(1024)
        signature = private_key.sign(message, hashes.SHA256())

        public_key = private_key.public_key()
        public_key.verify(signature, message, hashes.SHA256())
