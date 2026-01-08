"""Interface definitions for dependency injection and loose coupling."""

from .encryptor_interface import IEncryptor
from .cleaner_interface import ICleaner
from .file_handler_interface import IFileHandler

__all__ = [
    "IEncryptor",
    "ICleaner",
    "IFileHandler",
]

