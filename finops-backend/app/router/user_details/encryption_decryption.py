import base64
import logging
import logging.config

from cryptography.fernet import Fernet
from fastapi import HTTPException, status

from router.user_details.dev_details import get_developer_secret_value

logger = logging.getLogger(__name__)

def get_encryption_key() -> bytes:
    """Fetch the encryption key from the key vault."""
    encryption_key = get_developer_secret_value("ENCRYPTION-KEY")
    if encryption_key:
        return encryption_key.encode()
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Encryption key not found")


def encrypt_and_encode(value: str) -> str:
    """Encrypt and encode the value."""
    key = get_encryption_key()
    encrypted = Fernet(key).encrypt(value.encode("utf-8")).decode("utf-8")
    logger.debug("Encrypted Value: %s", encrypted)
    to_encode = ("true" + encrypted).encode("utf-8")
    logger.debug("Value to encode: %s", to_encode)
    encoded = base64.b64encode(to_encode).decode("utf-8")
    logger.debug("Encoded Value: %s", encoded)
    return encoded


def decode_and_decrypt(value: str) -> str:
    """Decode and decrypt the value."""
    logger.debug("Value to decode: %s", value)
    decoded = base64.b64decode(value.encode()).decode("utf-8")
    logger.debug("Decoded Value: %s", decoded)
    if decoded[:4] != "true":
        return decoded
    key = get_encryption_key()
    to_decrypt= decoded[4:].encode("utf-8")
    logger.debug("Value to decrypt: %s", to_decrypt)
    decrypted = Fernet(key).decrypt(to_decrypt).decode("utf-8")
    logger.debug("Decrypted Value: %s", decrypted)
    return decrypted