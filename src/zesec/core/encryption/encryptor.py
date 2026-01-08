"""Core encryption service implementation."""

import struct
from pathlib import Path
from typing import Optional

from ...config.settings import Settings
from ...core.models.encryption_result import EncryptionResult
from ...interfaces.cleaner_interface import ICleaner
from ...interfaces.encryptor_interface import IEncryptor
from ...interfaces.file_handler_interface import IFileHandler
from ...utils.exceptions import DecryptionError, EncryptionError
from ...utils.logging_config import get_logger
from .algorithms import EncryptionAlgorithm, get_algorithm
from .key_manager import KeyManager


class EncryptorService:
    """Core encryption service - pure business logic.
    
    This service handles encryption and decryption operations without
    any UI dependencies. It uses dependency injection for file operations
    and cleaning services.
    """

    # File format:
    # [Header: 16 bytes]
    # - Version: 1 byte
    # - Algorithm ID: 1 byte
    # - Salt length: 1 byte
    # - Nonce length: 1 byte
    # - Key file flag: 1 byte (0 = no key file, 1 = key file used)
    # - Reserved: 11 bytes
    # [Salt: variable (typically 16 bytes)]
    # [Nonce: variable (typically 12 bytes)]
    # [Ciphertext + Tag: variable]

    FILE_FORMAT_VERSION = 1
    ALGORITHM_ID_AES_256_GCM = 1
    KEY_FILE_FLAG_NO_KEY = 0
    KEY_FILE_FLAG_WITH_KEY = 1

    def __init__(
        self,
        key_manager: KeyManager,
        file_handler: IFileHandler,
        cleaner: Optional[ICleaner] = None,
        settings: Optional[Settings] = None,
        logger=None,
    ):
        """Initialize EncryptorService.
        
        Args:
            key_manager: Key manager for key generation/derivation
            file_handler: File handler for I/O operations
            cleaner: Optional cleaner for secure file deletion
            settings: Application settings (defaults to singleton)
            logger: Logger instance (defaults to module logger)
        """
        self._key_manager = key_manager
        self._file_handler = file_handler
        self._cleaner = cleaner
        self._settings = settings or Settings.get_instance()
        self._logger = logger or get_logger(__name__)

        # Get algorithm provider
        algorithm = EncryptionAlgorithm(self._settings.ENCRYPTION_ALGORITHM)
        self._algorithm = get_algorithm(algorithm)

    def encrypt_file(
        self,
        file_path: Path,
        password: str,
        output_path: Optional[Path] = None,
        clean_original: bool = True,
        key_file_path: Optional[Path] = None,
    ) -> EncryptionResult:
        """Encrypt a file.
        
        Args:
            file_path: Path to the file to encrypt
            password: Password for encryption
            output_path: Optional output path. If None, uses file_path with .enc extension
            clean_original: If True, securely clean original file after encryption
            key_file_path: Optional path to key file. If provided, combines with password
            
        Returns:
            EncryptionResult with success status and output path
        """
        try:
            self._logger.info(f"Starting encryption: {file_path}")

            # Validate input
            if not self._file_handler.file_exists(file_path):
                raise EncryptionError(f"File not found: {file_path}")

            # Determine output path
            if output_path is None:
                output_path = self._settings.get_encrypted_path(file_path)
            else:
                self._file_handler.ensure_directory(output_path.parent)

            # Read file
            plaintext = self._file_handler.read_file(file_path)
            file_size = len(plaintext)

            # Derive key from password
            password_key, salt = self._key_manager.derive_key_from_password(password)
            nonce = self._key_manager.generate_nonce()

            # Load key file if provided
            key_file = None
            if key_file_path is not None:
                self._logger.info(f"Using key file: {key_file_path}")
                key_file = self._key_manager.load_key_file(key_file_path)

            # Combine keys (key file + password)
            encryption_key = self._key_manager.combine_keys(key_file, password_key, salt)

            # Encrypt data
            ciphertext = self._algorithm.encrypt(plaintext, encryption_key, nonce)

            # Build encrypted file format
            has_key_file = key_file is not None
            encrypted_data = self._build_encrypted_file(salt, nonce, ciphertext, has_key_file)

            # Write encrypted file
            if not self._file_handler.write_file(output_path, encrypted_data):
                raise EncryptionError(f"Failed to write encrypted file: {output_path}")

            # Clean original file if requested
            if clean_original and self._cleaner:
                self._logger.info(f"Cleaning original file: {file_path}")
                if not self._cleaner.clean_file(file_path):
                    self._logger.warning(f"Failed to clean original file: {file_path}")

            self._logger.success(f"Encryption completed: {output_path}")

            return EncryptionResult(
                success=True,
                output_path=output_path,
                file_size=file_size,
                operation="encrypt",
            )

        except Exception as e:
            self._logger.error(f"Encryption failed: {e}")
            return EncryptionResult(
                success=False,
                error=str(e),
                operation="encrypt",
            )

    def decrypt_file(
        self,
        file_path: Path,
        password: str,
        output_path: Optional[Path] = None,
        key_file_path: Optional[Path] = None,
    ) -> EncryptionResult:
        """Decrypt a file.
        
        Args:
            file_path: Path to the encrypted file
            password: Password used for encryption
            output_path: Optional output path. If None, removes .enc extension
            key_file_path: Optional path to key file. Required if used during encryption
            
        Returns:
            EncryptionResult with success status and output path
        """
        try:
            self._logger.info(f"Starting decryption: {file_path}")

            # Validate input
            if not self._file_handler.file_exists(file_path):
                raise DecryptionError(f"File not found: {file_path}")

            # Read encrypted file
            encrypted_data = self._file_handler.read_file(file_path)

            # Parse file format
            salt, nonce, ciphertext, has_key_file = self._parse_encrypted_file(encrypted_data)

            # Check if key file is required
            if has_key_file and key_file_path is None:
                raise DecryptionError(
                    "Key file is required for decryption but not provided. "
                    "This file was encrypted with a key file."
                )

            # Derive key from password
            password_key, _ = self._key_manager.derive_key_from_password(password, salt)

            # Load key file if required
            key_file = None
            if has_key_file:
                if key_file_path is None:
                    raise DecryptionError("Key file path required but not provided")
                self._logger.info(f"Loading key file: {key_file_path}")
                key_file = self._key_manager.load_key_file(key_file_path)

            # Combine keys (same as encryption)
            decryption_key = self._key_manager.combine_keys(key_file, password_key, salt)

            # Decrypt data
            plaintext = self._algorithm.decrypt(ciphertext, decryption_key, nonce)
            file_size = len(plaintext)

            # Determine output path
            if output_path is None:
                output_path = self._settings.get_decrypted_path(file_path)
            else:
                self._file_handler.ensure_directory(output_path.parent)

            # Write decrypted file
            if not self._file_handler.write_file(output_path, plaintext):
                raise DecryptionError(f"Failed to write decrypted file: {output_path}")

            self._logger.success(f"Decryption completed: {output_path}")

            return EncryptionResult(
                success=True,
                output_path=output_path,
                file_size=file_size,
                operation="decrypt",
            )

        except Exception as e:
            self._logger.error(f"Decryption failed: {e}")
            return EncryptionResult(
                success=False,
                error=str(e),
                operation="decrypt",
            )

    def encrypt_directory(
        self,
        dir_path: Path,
        password: str,
        clean_originals: bool = True,
        recursive: bool = True,
        key_file_path: Optional[Path] = None,
    ) -> list[EncryptionResult]:
        """Encrypt all files in a directory.
        
        Args:
            dir_path: Path to the directory
            password: Password for encryption
            clean_originals: If True, securely clean original files
            recursive: If True, process subdirectories
            key_file_path: Optional path to key file. If provided, combines with password
            
        Returns:
            List of EncryptionResult for each file processed
        """
        results = []

        if not dir_path.is_dir():
            self._logger.error(f"Not a directory: {dir_path}")
            return results

        # Find all files
        pattern = "**/*" if recursive else "*"
        files = [f for f in dir_path.glob(pattern) if f.is_file()]

        self._logger.info(f"Found {len(files)} files to encrypt in {dir_path}")

        for file_path in files:
            result = self.encrypt_file(
                file_path,
                password,
                clean_original=clean_originals,
                key_file_path=key_file_path,
            )
            results.append(result)

        return results

    def _build_encrypted_file(
        self,
        salt: bytes,
        nonce: bytes,
        ciphertext: bytes,
        has_key_file: bool = False,
    ) -> bytes:
        """Build encrypted file format.
        
        Args:
            salt: Salt used for key derivation
            nonce: Nonce used for encryption
            ciphertext: Encrypted data (includes tag for GCM)
            has_key_file: Whether a key file was used in encryption
            
        Returns:
            Complete encrypted file as bytes
        """
        # Header: version(1) + algorithm(1) + salt_len(1) + nonce_len(1) + key_file_flag(1) + reserved(11)
        key_file_flag = (
            self.KEY_FILE_FLAG_WITH_KEY if has_key_file else self.KEY_FILE_FLAG_NO_KEY
        )
        header = struct.pack(
            "!BBBBB11s",
            self.FILE_FORMAT_VERSION,
            self.ALGORITHM_ID_AES_256_GCM,
            len(salt),
            len(nonce),
            key_file_flag,
            b"\x00" * 11,  # Reserved
        )

        return header + salt + nonce + ciphertext

    def _parse_encrypted_file(
        self,
        data: bytes,
    ) -> tuple[bytes, bytes, bytes, bool]:
        """Parse encrypted file format.
        
        Args:
            data: Complete encrypted file data
            
        Returns:
            Tuple of (salt, nonce, ciphertext, has_key_file)
            
        Raises:
            DecryptionError: If file format is invalid
        """
        if len(data) < 16:
            raise DecryptionError("Encrypted file too short (missing header)")

        # Parse header
        header = data[:16]
        version, algorithm_id, salt_len, nonce_len, key_file_flag = struct.unpack(
            "!BBBBB", header[:5]
        )

        if version != self.FILE_FORMAT_VERSION:
            raise DecryptionError(f"Unsupported file format version: {version}")

        if algorithm_id != self.ALGORITHM_ID_AES_256_GCM:
            raise DecryptionError(f"Unsupported algorithm ID: {algorithm_id}")

        has_key_file = key_file_flag == self.KEY_FILE_FLAG_WITH_KEY

        # Extract components
        offset = 16
        salt = data[offset : offset + salt_len]
        offset += salt_len
        nonce = data[offset : offset + nonce_len]
        offset += nonce_len
        ciphertext = data[offset:]

        if len(salt) != salt_len or len(nonce) != nonce_len:
            raise DecryptionError("Invalid file format: component length mismatch")

        return salt, nonce, ciphertext, has_key_file

