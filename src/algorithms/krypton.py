"""
Krypton Cipher usando quantCrypt.
"""

from secrets import token_bytes

from quantcrypt.cipher import Krypton


def run_krypton(volume: int):
    """
    Executa rodadas de cifração/decifração usando Krypton.

    Args:
        volume: Número de operações (encrypt/decrypt pairs)
    """
    plaintext = b"Hello World"

    for _ in range(volume):
        secret_key = token_bytes(64)
        krypton = Krypton(secret_key)

        krypton.begin_encryption()
        ciphertext = krypton.encrypt(plaintext)
        verif_dp = krypton.finish_encryption()

        krypton.begin_decryption(verif_dp)
        plaintext_copy = krypton.decrypt(ciphertext)
        krypton.finish_decryption()

        assert plaintext_copy == plaintext
