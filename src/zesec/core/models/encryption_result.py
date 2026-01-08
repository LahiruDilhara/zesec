"""Result model for encryption/decryption operations."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class EncryptionResult:
    """Result of an encryption or decryption operation."""

    success: bool
    output_path: Optional[Path] = None
    error: Optional[str] = None
    file_size: int = 0
    operation: str = "encrypt"  # "encrypt" or "decrypt"

    def __str__(self) -> str:
        """String representation of the result."""
        if self.success:
            return f"{self.operation.capitalize()} successful: {self.output_path}"
        else:
            return f"{self.operation.capitalize()} failed: {self.error}"

