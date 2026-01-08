"""File information model."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class FileInfo:
    """Information about a file."""

    path: Path
    size: int
    exists: bool = True
    is_directory: bool = False
    is_file: bool = True

    @classmethod
    def from_path(cls, path: Path) -> "FileInfo":
        """Create FileInfo from a path.
        
        Args:
            path: Path to analyze
            
        Returns:
            FileInfo instance
        """
        exists = path.exists()
        is_file = path.is_file() if exists else False
        is_directory = path.is_dir() if exists else False
        size = path.stat().st_size if exists and is_file else 0

        return cls(
            path=path,
            size=size,
            exists=exists,
            is_directory=is_directory,
            is_file=is_file,
        )

