"""Worker thread for encryption operations."""

from pathlib import Path
from typing import Optional

from PySide6.QtCore import QThread, Signal

from ...interfaces.encryptor_interface import IEncryptor
from ...core.models.encryption_result import EncryptionResult


class EncryptWorker(QThread):
    """Worker thread for encryption operations."""
    
    progress = Signal(int)  # 0-100
    finished = Signal(EncryptionResult)
    error = Signal(str)
    
    def __init__(
        self,
        encryptor: IEncryptor,
        file_path: Path,
        password: str,
        key_file_path: Optional[Path] = None,
        clean_original: bool = True,
        parent=None
    ):
        """Initialize encryption worker.
        
        Args:
            encryptor: Encryption service
            file_path: Path to file to encrypt
            password: Encryption password
            key_file_path: Optional key file path
            clean_original: Whether to clean original file
            parent: Parent QObject
        """
        super().__init__(parent)
        self._encryptor = encryptor
        self._file_path = file_path
        self._password = password
        self._key_file_path = key_file_path
        self._clean_original = clean_original
        
    def run(self):
        """Execute encryption in background thread."""
        try:
            self.progress.emit(10)
            
            result = self._encryptor.encrypt_file(
                self._file_path,
                self._password,
                key_file_path=self._key_file_path,
                clean_original=self._clean_original
            )
            
            self.progress.emit(100)
            self.finished.emit(result)
            
        except Exception as e:
            self.error.emit(str(e))

