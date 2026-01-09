"""Interface for secure file cleaning operations."""

from abc import abstractmethod
from pathlib import Path
from typing import Protocol, runtime_checkable


@runtime_checkable
class ICleaner(Protocol):
    """Protocol defining secure file cleaning contract.
    
    Secure cleaning means overwriting file content with zeros or random data
    before deletion to remove residual data.
    """

    @abstractmethod
    def clean_file(self, file_path: Path, passes: int = 3, delete: bool = True) -> bool:
        """Securely clean a file by overwriting and optionally deleting.
        
        Args:
            file_path: Path to the file to clean
            passes: Number of overwrite passes (default: 3)
            delete: If True, delete file after cleaning (default: True)
            
        Returns:
            True if successful, False otherwise
        """
        ...

    @abstractmethod
    def clean_directory(
        self,
        dir_path: Path,
        passes: int = 3,
        recursive: bool = True,
        delete: bool = True,
    ) -> bool:
        """Securely clean all files in a directory.
        
        Args:
            dir_path: Path to the directory
            passes: Number of overwrite passes per file
            recursive: If True, process subdirectories
            delete: If True, delete files after cleaning (default: True)
            
        Returns:
            True if all files cleaned successfully, False otherwise
        """
        ...

    @abstractmethod
    def overwrite_file(
        self,
        file_path: Path,
        data: bytes | None = None,
        passes: int = 1,
    ) -> bool:
        """Overwrite file content without deleting.
        
        Args:
            file_path: Path to the file
            data: Data to write. If None, writes zeros
            passes: Number of overwrite passes
            
        Returns:
            True if successful, False otherwise
        """
        ...

