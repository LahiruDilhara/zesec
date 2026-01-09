"""Controller for decryption operations."""

from pathlib import Path
from typing import Optional

from PySide6.QtCore import QObject, Signal

from ...di.container import ApplicationContainer
from ...interfaces.encryptor_interface import IEncryptor
from ...core.models.encryption_result import EncryptionResult
from ..workers.decrypt_worker import DecryptWorker


class DecryptController(QObject):
    """Presenter for decryption operations."""
    
    # Signals to communicate with View
    progress_updated = Signal(int)  # 0-100
    operation_completed = Signal(EncryptionResult)
    error_occurred = Signal(str)
    
    def __init__(self, container: ApplicationContainer):
        """Initialize decryption controller.
        
        Args:
            container: DI container
        """
        super().__init__()
        self._container = container
        self._encryptor: IEncryptor = container.encryptor()
        self._current_worker: Optional[DecryptWorker] = None
        
    def decrypt_file(
        self,
        file_path: Path,
        password: str,
        key_file_path: Optional[Path] = None
    ):
        """Initiate decryption operation.
        
        Args:
            file_path: Path to encrypted file
            password: Decryption password
            key_file_path: Optional key file path
        """
        # Validation
        if not file_path.exists():
            self.error_occurred.emit("File does not exist")
            return
            
        if not password:
            self.error_occurred.emit("Password cannot be empty")
            return
            
        # Cancel any existing operation
        if self._current_worker and self._current_worker.isRunning():
            self._current_worker.terminate()
            self._current_worker.wait()
        
        # Create worker for async operation
        worker = DecryptWorker(
            self._encryptor,
            file_path,
            password,
            key_file_path
        )
        
        # Connect worker signals
        worker.progress.connect(self.progress_updated)
        worker.finished.connect(self.operation_completed)
        worker.error.connect(self.error_occurred)
        
        # Store reference and start worker
        self._current_worker = worker
        worker.start()
        
    def cancel_operation(self):
        """Cancel current decryption operation."""
        if self._current_worker and self._current_worker.isRunning():
            self._current_worker.terminate()
            self._current_worker.wait()

