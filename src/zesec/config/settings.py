"""Application settings loaded from environment variables."""

from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings - loaded once from .env file.
    
    This is a singleton pattern to ensure settings are loaded once
    and accessed consistently throughout the application.
    """

    # Encryption settings
    ENCRYPTION_ALGORITHM: str = "AES-256-GCM"
    KEY_DERIVATION_ITERATIONS: int = 100000
    NONCE_SIZE: int = 12
    KEY_SIZE: int = 32  # 256 bits for AES-256
    TAG_SIZE: int = 16  # GCM authentication tag size

    # File operations
    CLEAN_PASSES: int = 3  # Number of overwrite passes for secure deletion
    BUFFER_SIZE: int = 1024 * 1024  # 1MB buffer for file operations

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Optional[str] = None
    LOG_FORMAT: str = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function} | {message}"

    # Application
    APP_NAME: str = "Zesec"
    APP_VERSION: str = "1.0.0"

    # File extensions
    ENCRYPTED_EXTENSION: str = ".zesec"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # Ignore extra env vars
    )

    @classmethod
    @lru_cache(maxsize=1)
    def get_instance(cls) -> "Settings":
        """Get singleton instance of settings.
        
        Returns:
            Settings instance (cached after first call)
        """
        return cls()

    def get_log_file_path(self) -> Optional[Path]:
        """Get log file path if configured.
        
        Returns:
            Path to log file or None if not configured
        """
        if self.LOG_FILE:
            return Path(self.LOG_FILE)
        return None

    def get_encrypted_path(self, original_path: Path) -> Path:
        """Get encrypted file path from original path.
        
        Args:
            original_path: Original file path
            
        Returns:
            Path with encrypted extension
        """
        return original_path.with_suffix(original_path.suffix + self.ENCRYPTED_EXTENSION)

    def get_decrypted_path(self, encrypted_path: Path) -> Path:
        """Get decrypted file path from encrypted path.
        
        Args:
            encrypted_path: Encrypted file path
            
        Returns:
            Path with encrypted extension removed
        """
        if encrypted_path.suffix == self.ENCRYPTED_EXTENSION:
            # Remove encrypted extension
            return encrypted_path.with_suffix("")
        # If no encrypted extension, try removing it from the end
        name = encrypted_path.name
        if name.endswith(self.ENCRYPTED_EXTENSION):
            new_name = name[: -len(self.ENCRYPTED_EXTENSION)]
            return encrypted_path.parent / new_name
        return encrypted_path.with_suffix("")

