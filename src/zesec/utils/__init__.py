"""Utility modules for cross-platform support and shared functionality."""

from .exceptions import (
    EncryptionError,
    DecryptionError,
    FileOperationError,
    CleanerError,
)
from .logging_config import get_logger, setup_logging
from .platform import Platform, get_platform

__all__ = [
    "EncryptionError",
    "DecryptionError",
    "FileOperationError",
    "CleanerError",
    "get_logger",
    "setup_logging",
    "Platform",
    "get_platform",
]

