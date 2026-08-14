"""
MLKEM_1024 Key Encapsulation Mechanism usando quantCrypt.
"""

from quantcrypt.kem import MLKEM_1024


def run_kem(volume: int):
    """
    Executa operações de KEM (Key Encapsulation) usando MLKEM_1024.

    Args:
        volume: Número de operações (encapsulation/decapsulation pairs)
    """
    if volume <= 0:
        raise ValueError(f"volume must be greater than 0, got {volume}")

    kem = MLKEM_1024()

    for _ in range(volume):
        public_key, secret_key = kem.keygen()
        cipher_text, shared_secret = kem.encaps(public_key)
        decapsulated_secret = kem.decaps(secret_key, cipher_text)
        assert shared_secret == decapsulated_secret
