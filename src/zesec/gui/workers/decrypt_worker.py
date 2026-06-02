"""Worker thread for decryption operations."""

from pathlib import Path
from typing import Optional

from PySide6.QtCore import QThread, Signal

from ...interfaces.encryptor_interface import IEncryptor
from ...core.models.encryption_result import EncryptionResult


class DecryptWorker(QThread):
    """Worker thread for decryption operations."""
    
    progress = Signal(int)  # 0-100
    finished = Signal(EncryptionResult)
    error = Signal(str)
    
    def __init__(
        self,
        encryptor: IEncryptor,
        file_path: Path,
        password: str,
        output_path: Optional[Path] = None,
        clean_original: bool = False,
        key_file_path: Optional[Path] = None,
        parent=None
    ):
        """Initialize decryption worker.
        
        Args:
            encryptor: Encryption service
            file_path: Path to encrypted file
            password: Decryption password
            key_file_path: Optional key file path
            parent: Parent QObject
        """
        super().__init__(parent)
        self._encryptor = encryptor
        self._file_path = file_path
        self._password = password
        self._output_path = output_path
        self._clean_original = clean_original
        self._key_file_path = key_file_path
        
    def run(self):
        """Execute decryption in background thread."""
        try:
            self.progress.emit(10)
            
            result = self._encryptor.decrypt_file(
                self._file_path,
                self._password,
                output_path=self._output_path,
                clean_original=self._clean_original,
                key_file_path=self._key_file_path,
                progress_callback=self.progress.emit
            )
            
            self.progress.emit(100)
            self.finished.emit(result)
            
        except Exception as e:
            self.error.emit(str(e))

