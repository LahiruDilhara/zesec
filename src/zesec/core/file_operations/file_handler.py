"""File I/O operations handler."""

from pathlib import Path
from typing import Optional

from ...config.settings import Settings
from ...interfaces.file_handler_interface import IFileHandler
from ...utils.exceptions import FileOperationError
from ...utils.logging_config import get_logger


class FileHandler:
    """Cross-platform file I/O operations handler.
    
    Provides a clean interface for file operations that works
    consistently across Windows, Linux, and macOS.
    """

    def __init__(
        self,
        settings: Optional[Settings] = None,
        logger=None,
    ):
        """Initialize FileHandler.
        
        Args:
            settings: Application settings (defaults to singleton)
            logger: Logger instance (defaults to module logger)
        """
        self._settings = settings or Settings.get_instance()
        self._logger = logger or get_logger(__name__)

    def read_file(self, file_path: Path) -> bytes:
        """Read file contents as bytes.
        
        Args:
            file_path: Path to the file
            
        Returns:
            File contents as bytes
            
        Raises:
            FileNotFoundError: If file doesn't exist
            FileOperationError: If file cannot be read
        """
        try:
            self._logger.debug(f"Reading file: {file_path}")
            with open(file_path, "rb") as f:
                return f.read()
        except FileNotFoundError:
            self._logger.error(f"File not found: {file_path}")
            raise
        except Exception as e:
            self._logger.error(f"Failed to read file {file_path}: {e}")
            raise FileOperationError(f"Failed to read file: {e}") from e

    def write_file(self, file_path: Path, data: bytes) -> bool:
        """Write bytes to a file.
        
        Args:
            file_path: Path to the file
            data: Data to write
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self._logger.debug(f"Writing file: {file_path} ({len(data)} bytes)")

            # Ensure directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Write file
            with open(file_path, "wb") as f:
                f.write(data)

            self._logger.debug(f"File written successfully: {file_path}")
            return True

        except Exception as e:
            self._logger.error(f"Failed to write file {file_path}: {e}")
            return False

    def file_exists(self, file_path: Path) -> bool:
        """Check if file exists.
        
        Args:
            file_path: Path to check
            
        Returns:
            True if file exists, False otherwise
        """
        return file_path.exists() and file_path.is_file()

    def get_file_size(self, file_path: Path) -> int:
        """Get file size in bytes.
        
        Args:
            file_path: Path to the file
            
        Returns:
            File size in bytes
            
        Raises:
            FileNotFoundError: If file doesn't exist
        """
        if not self.file_exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        return file_path.stat().st_size

    def ensure_directory(self, dir_path: Path) -> bool:
        """Ensure directory exists, create if needed.
        
        Args:
            dir_path: Path to the directory
            
        Returns:
            True if directory exists or was created, False otherwise
        """
        try:
            dir_path.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            self._logger.error(f"Failed to create directory {dir_path}: {e}")
            return False

