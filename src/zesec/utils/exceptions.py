"""Custom exceptions for the application."""


class ZesecError(Exception):
    """Base exception for all Zesec errors."""

    pass


class EncryptionError(ZesecError):
    """Raised when encryption operations fail."""

    pass


class DecryptionError(ZesecError):
    """Raised when decryption operations fail."""

    pass


class FileOperationError(ZesecError):
    """Raised when file operations fail."""

    pass


class CleanerError(ZesecError):
    """Raised when secure cleaning operations fail."""

    pass


class KeyDerivationError(ZesecError):
    """Raised when key derivation fails."""

    pass


class ConfigurationError(ZesecError):
    """Raised when configuration is invalid."""

    pass

