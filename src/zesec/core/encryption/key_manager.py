"""Key generation and derivation management."""

import base64
import os
from pathlib import Path
from typing import Optional

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from ...config.settings import Settings
from ...interfaces.file_handler_interface import IFileHandler
from ...utils.exceptions import KeyDerivationError
from ...utils.logging_config import get_logger


class KeyManager:
    """Manages encryption key generation and derivation from passwords and key files."""

    def __init__(
        self,
        file_handler: Optional[IFileHandler] = None,
        settings: Optional[Settings] = None,
        logger=None,
    ):
        """Initialize KeyManager.
        
        Args:
            file_handler: File handler for key file operations (optional)
            settings: Application settings (defaults to singleton instance)
            logger: Logger instance (defaults to module logger)
        """
        self._file_handler = file_handler
        self._settings = settings or Settings.get_instance()
        self._logger = logger or get_logger(__name__)

    def generate_key(self) -> bytes:
        """Generate a random encryption key.
        
        Returns:
            Random key bytes (32 bytes for AES-256)
        """
        return os.urandom(self._settings.KEY_SIZE)

    def derive_key_from_password(
        self,
        password: str,
        salt: Optional[bytes] = None,
    ) -> tuple[bytes, bytes]:
        """Derive encryption key from password using PBKDF2.
        
        Args:
            password: User password
            salt: Optional salt. If None, generates a random salt
            
        Returns:
            Tuple of (key, salt) where key is derived key and salt is used salt
        """
        if salt is None:
            salt = os.urandom(16)  # 16 bytes salt

        try:
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=self._settings.KEY_SIZE,
                salt=salt,
                iterations=self._settings.KEY_DERIVATION_ITERATIONS,
            )
            key = kdf.derive(password.encode("utf-8"))
            return key, salt
        except Exception as e:
            self._logger.error(f"Key derivation failed: {e}")
            raise KeyDerivationError(f"Failed to derive key from password: {e}") from e

    def generate_nonce(self) -> bytes:
        """Generate a random nonce for encryption.
        
        Returns:
            Random nonce bytes (12 bytes for GCM)
        """
        return os.urandom(self._settings.NONCE_SIZE)

    def generate_key_file(self, key_file_path: Path) -> bool:
        """Generate and save a random encryption key to a file.
        
        The key is saved as base64-encoded text (UTF-8) for human readability.
        
        Args:
            key_file_path: Path where the key file should be saved
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if self._file_handler is None:
                raise KeyDerivationError("File handler not available for key file operations")

            # Generate random key
            key = self.generate_key()

            # Encode key as base64 for human readability (UTF-8)
            key_base64 = base64.b64encode(key).decode('utf-8')
            
            # Save key to file as UTF-8 encoded bytes
            key_bytes = key_base64.encode('utf-8')
            if not self._file_handler.write_file(key_file_path, key_bytes):
                raise KeyDerivationError(f"Failed to write key file: {key_file_path}")

            self._logger.info(f"Key file generated: {key_file_path}")
            return True

        except Exception as e:
            self._logger.error(f"Failed to generate key file: {e}")
            return False

    def load_key_file(self, key_file_path: Path) -> bytes:
        """Load encryption key from a file.
        
        The key file is expected to be base64-encoded text (UTF-8).
        
        Args:
            key_file_path: Path to the key file
            
        Returns:
            Key bytes from the file
            
        Raises:
            KeyDerivationError: If key file cannot be loaded or is invalid
        """
        try:
            if self._file_handler is None:
                raise KeyDerivationError("File handler not available for key file operations")

            if not self._file_handler.file_exists(key_file_path):
                raise KeyDerivationError(f"Key file not found: {key_file_path}")

            # Read key from file (as bytes)
            key_data = self._file_handler.read_file(key_file_path)
            
            # Decode from UTF-8 to get base64 string
            try:
                key_base64 = key_data.decode('utf-8').strip()
            except UnicodeDecodeError as e:
                raise KeyDerivationError(f"Key file is not valid UTF-8: {e}") from e
            
            # Decode from base64 to get key bytes
            try:
                key = base64.b64decode(key_base64)
            except Exception as e:
                raise KeyDerivationError(f"Key file is not valid base64: {e}") from e

            # Validate key size
            if len(key) != self._settings.KEY_SIZE:
                raise KeyDerivationError(
                    f"Invalid key size: expected {self._settings.KEY_SIZE} bytes, "
                    f"got {len(key)} bytes"
                )

            self._logger.debug(f"Key file loaded: {key_file_path}")
            return key

        except KeyDerivationError:
            raise
        except Exception as e:
            self._logger.error(f"Failed to load key file: {e}")
            raise KeyDerivationError(f"Failed to load key file: {e}") from e

    def combine_keys(
        self,
        key_file: Optional[bytes],
        password_key: bytes,
        salt: bytes,
    ) -> bytes:
        """Combine key file and password-derived key using HKDF.
        
        This securely combines both keys so that both are required for decryption.
        
        Args:
            key_file: Key from file (optional)
            password_key: Key derived from password
            salt: Salt to use for HKDF
            
        Returns:
            Combined key (32 bytes for AES-256)
        """
        if key_file is None:
            # If no key file, just use password key
            return password_key

        # Combine both keys using HKDF
        # Use the key file as the input key material and password key as salt/context
        combined_input = key_file + password_key

        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=self._settings.KEY_SIZE,
            salt=salt,
            info=b"zesec-key-combination",
        )

        combined_key = hkdf.derive(combined_input)
        self._logger.debug("Keys combined using HKDF")
        return combined_key

