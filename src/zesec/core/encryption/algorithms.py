"""Encryption algorithm definitions and utilities."""

from enum import Enum
from typing import Protocol

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class EncryptionAlgorithm(Enum):
    """Supported encryption algorithms."""

    AES_256_GCM = "AES-256-GCM"


class AlgorithmProvider(Protocol):
    """Protocol for encryption algorithm providers."""

    def encrypt(self, data: bytes, key: bytes, nonce: bytes) -> bytes:
        """Encrypt data."""
        ...

    def decrypt(self, data: bytes, key: bytes, nonce: bytes) -> bytes:
        """Decrypt data."""
        ...


class AES256GCMProvider:
    """AES-256-GCM encryption provider."""

    def __init__(self):
        self._cipher = None

    def encrypt(self, data: bytes, key: bytes, nonce: bytes) -> bytes:
        """Encrypt data using AES-256-GCM.
        
        Args:
            data: Plaintext data
            key: Encryption key (32 bytes for AES-256)
            nonce: Nonce/IV (12 bytes for GCM)
            
        Returns:
            Encrypted data (ciphertext + tag)
        """
        cipher = AESGCM(key)
        return cipher.encrypt(nonce, data, None)

    def decrypt(self, data: bytes, key: bytes, nonce: bytes) -> bytes:
        """Decrypt data using AES-256-GCM.
        
        Args:
            data: Encrypted data (ciphertext + tag)
            key: Decryption key (32 bytes for AES-256)
            nonce: Nonce/IV (12 bytes for GCM)
            
        Returns:
            Decrypted plaintext data
        """
        cipher = AESGCM(key)
        return cipher.decrypt(nonce, data, None)


def get_algorithm(algorithm: EncryptionAlgorithm | str) -> AlgorithmProvider:
    """Get algorithm provider for the specified algorithm.
    
    Args:
        algorithm: Algorithm enum or string name
        
    Returns:
        Algorithm provider instance
        
    Raises:
        ValueError: If algorithm is not supported
    """
    if isinstance(algorithm, str):
        try:
            algorithm = EncryptionAlgorithm(algorithm)
        except ValueError:
            raise ValueError(f"Unsupported algorithm: {algorithm}")

    if algorithm == EncryptionAlgorithm.AES_256_GCM:
        return AES256GCMProvider()
    else:
        raise ValueError(f"Algorithm provider not implemented: {algorithm}")

