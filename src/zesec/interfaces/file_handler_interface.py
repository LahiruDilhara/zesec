"""Interface for file I/O operations."""

from abc import abstractmethod
from pathlib import Path
from typing import Protocol, runtime_checkable


@runtime_checkable
class IFileHandler(Protocol):
    """Protocol defining file I/O contract.
    
    Provides cross-platform file operations abstraction.
    """

    @abstractmethod
    def read_file(self, file_path: Path) -> bytes:
        """Read file contents as bytes.
        
        Args:
            file_path: Path to the file
            
        Returns:
            File contents as bytes
            
        Raises:
            FileNotFoundError: If file doesn't exist
            IOError: If file cannot be read
        """
        ...

    @abstractmethod
    def write_file(self, file_path: Path, data: bytes) -> bool:
        """Write bytes to a file.
        
        Args:
            file_path: Path to the file
            data: Data to write
            
        Returns:
            True if successful, False otherwise
        """
        ...

    @abstractmethod
    def file_exists(self, file_path: Path) -> bool:
        """Check if file exists.
        
        Args:
            file_path: Path to check
            
        Returns:
            True if file exists, False otherwise
        """
        ...

    @abstractmethod
    def get_file_size(self, file_path: Path) -> int:
        """Get file size in bytes.
        
        Args:
            file_path: Path to the file
            
        Returns:
            File size in bytes
            
        Raises:
            FileNotFoundError: If file doesn't exist
        """
        ...

    @abstractmethod
    def ensure_directory(self, dir_path: Path) -> bool:
        """Ensure directory exists, create if needed.
        
        Args:
            dir_path: Path to the directory
            
        Returns:
            True if directory exists or was created, False otherwise
        """
        ...

