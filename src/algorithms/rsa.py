from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa


def run_rsa(volume: int):
    if volume <= 0:
        raise ValueError(f"volume must be greater than 0, got {volume}")

    message = b"Hello World!"

    for _ in range(volume):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=1024,
        )
        signature = private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256(),
        )

        public_key = private_key.public_key()
        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256(),
        )
