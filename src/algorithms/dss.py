"""
MLDSA_87 Digital Signature Scheme usando quantCrypt.
"""

from quantcrypt.dss import MLDSA_87


def run_dss(volume: int):
    """
    Executa operações de assinatura digital usando MLDSA_87.

    Args:
        volume: Número de operações (sign/verify pairs)
    """

    dss = MLDSA_87()
    message = b"Hello World"

    for _ in range(volume):
        public_key, secret_key = dss.keygen()
        signature = dss.sign(secret_key, message)
        is_valid = dss.verify(public_key, message, signature)
        assert is_valid
