"""Interface for encryption operations."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Protocol, runtime_checkable

from ..core.models.encryption_result import EncryptionResult


@runtime_checkable
class IEncryptor(Protocol):
    """Protocol defining encryption contract.
    
    This interface allows loose coupling between core encryption logic
    and presentation layers (console/GUI).
    """

    @abstractmethod
    def encrypt_file(
        self,
        file_path: Path,
        password: str,
        output_path: Path | None = None,
        clean_original: bool = True,
        key_file_path: Path | None = None,
    ) -> EncryptionResult:
        """Encrypt a file.
        
        Args:
            file_path: Path to the file to encrypt
            password: Password for encryption
            output_path: Optional output path. If None, uses file_path with .zesec extension
            clean_original: If True, securely clean original file after encryption
            key_file_path: Optional path to key file. If provided, combines with password
            
        Returns:
            EncryptionResult with success status and output path
        """
        ...

    @abstractmethod
    def decrypt_file(
        self,
        file_path: Path,
        password: str,
        output_path: Path | None = None,
        key_file_path: Path | None = None,
    ) -> EncryptionResult:
        """Decrypt a file.
        
        Args:
            file_path: Path to the encrypted file
            password: Password used for encryption
            output_path: Optional output path. If None, removes .zesec extension
            key_file_path: Optional path to key file. Required if used during encryption
            
        Returns:
            EncryptionResult with success status and output path
        """
        ...

    @abstractmethod
    def encrypt_directory(
        self,
        dir_path: Path,
        password: str,
        clean_originals: bool = True,
        recursive: bool = True,
        key_file_path: Path | None = None,
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
        ...

