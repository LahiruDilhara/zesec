"""Secure file cleaning service."""

import os
import random
from pathlib import Path
from typing import Optional

from ...config.settings import Settings
from ...interfaces.cleaner_interface import ICleaner
from ...interfaces.file_handler_interface import IFileHandler
from ...utils.exceptions import CleanerError
from ...utils.logging_config import get_logger


class CleanerService:
    """Secure file cleaning service.
    
    Securely deletes files by overwriting their content with zeros
    or random data before deletion. This removes residual data that
    might be recoverable with forensic tools.
    """

    def __init__(
        self,
        file_handler: IFileHandler,
        settings: Optional[Settings] = None,
        logger=None,
    ):
        """Initialize CleanerService.
        
        Args:
            file_handler: File handler for I/O operations
            settings: Application settings (defaults to singleton)
            logger: Logger instance (defaults to module logger)
        """
        self._file_handler = file_handler
        self._settings = settings or Settings.get_instance()
        self._logger = logger or get_logger(__name__)

    def clean_file(self, file_path: Path, passes: int = 3) -> bool:
        """Securely clean a file by overwriting and deleting.
        
        Args:
            file_path: Path to the file to clean
            passes: Number of overwrite passes (default: 3)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self._file_handler.file_exists(file_path):
                self._logger.warning(f"File does not exist: {file_path}")
                return False

            self._logger.info(f"Cleaning file: {file_path} ({passes} passes)")

            # Overwrite file multiple times
            for pass_num in range(1, passes + 1):
                self._logger.debug(f"Overwrite pass {pass_num}/{passes}")
                if not self.overwrite_file(file_path, passes=1):
                    self._logger.error(f"Failed on pass {pass_num}")
                    return False

            # Delete file
            try:
                file_path.unlink()
                self._logger.success(f"File cleaned and deleted: {file_path}")
                return True
            except Exception as e:
                self._logger.error(f"Failed to delete file {file_path}: {e}")
                return False

        except Exception as e:
            self._logger.error(f"File cleaning failed: {e}")
            return False

    def clean_directory(
        self,
        dir_path: Path,
        passes: int = 3,
        recursive: bool = True,
    ) -> bool:
        """Securely clean all files in a directory.
        
        Args:
            dir_path: Path to the directory
            passes: Number of overwrite passes per file
            recursive: If True, process subdirectories
            
        Returns:
            True if all files cleaned successfully, False otherwise
        """
        if not dir_path.is_dir():
            self._logger.error(f"Not a directory: {dir_path}")
            return False

        # Find all files
        pattern = "**/*" if recursive else "*"
        files = [f for f in dir_path.glob(pattern) if f.is_file()]

        self._logger.info(f"Cleaning {len(files)} files in {dir_path}")

        all_success = True
        for file_path in files:
            if not self.clean_file(file_path, passes):
                all_success = False

        return all_success

    def overwrite_file(
        self,
        file_path: Path,
        data: Optional[bytes] = None,
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
        try:
            if not self._file_handler.file_exists(file_path):
                return False

            file_size = self._file_handler.get_file_size(file_path)

            for pass_num in range(passes):
                # Open file in read-write mode
                with open(file_path, "r+b") as f:
                    # Write zeros or provided data
                    if data is None:
                        # Write zeros
                        buffer_size = self._settings.BUFFER_SIZE
                        remaining = file_size
                        while remaining > 0:
                            write_size = min(buffer_size, remaining)
                            f.write(b"\x00" * write_size)
                            remaining -= write_size
                    else:
                        # Write provided data (repeat if needed)
                        f.seek(0)
                        remaining = file_size
                        data_len = len(data)
                        while remaining > 0:
                            write_size = min(data_len, remaining)
                            f.write(data[:write_size])
                            remaining -= write_size

                    # Flush to disk
                    f.flush()
                    os.fsync(f.fileno())  # Force write to disk

                # On last pass, optionally write random data
                if pass_num == passes - 1 and data is None:
                    with open(file_path, "r+b") as f:
                        remaining = file_size
                        buffer_size = self._settings.BUFFER_SIZE
                        while remaining > 0:
                            write_size = min(buffer_size, remaining)
                            random_data = os.urandom(write_size)
                            f.write(random_data)
                            remaining -= write_size
                        f.flush()
                        os.fsync(f.fileno())

            return True

        except Exception as e:
            self._logger.error(f"Failed to overwrite file {file_path}: {e}")
            return False

