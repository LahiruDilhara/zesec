"""Controller for key generation operations."""

from pathlib import Path

from PySide6.QtCore import QObject, Signal

from ...di.container import ApplicationContainer
from typing import Optional

from ...core.encryption import KeyManager
from ..workers.key_generation_worker import KeyGenerationWorker


class KeyController(QObject):
    """Presenter for key generation operations."""
    
    # Signals to communicate with View
    progress_updated = Signal(int)  # 0-100
    operation_completed = Signal(bool, str)  # success, message
    error_occurred = Signal(str)
    
    def __init__(self, container: ApplicationContainer):
        """Initialize key generation controller.
        
        Args:
            container: DI container
        """
        super().__init__()
        self._container = container
        self._key_manager = container.key_manager()
        self._current_worker: Optional[KeyGenerationWorker] = None
        
    def generate_key_file(self, key_file_path: Path):
        """Initiate key generation operation.
        
        Args:
            key_file_path: Path where key file should be saved
        """
        # Validation
        if key_file_path.exists():
            self.error_occurred.emit("File already exists. Please choose a different path.")
            return
            
        # Cancel any existing operation
        if self._current_worker and self._current_worker.isRunning():
            self._current_worker.terminate()
            self._current_worker.wait()
        
        # Create worker for async operation
        worker = KeyGenerationWorker(
            self._key_manager,
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
        """Cancel current key generation operation."""
        if self._current_worker and self._current_worker.isRunning():
            self._current_worker.terminate()
            self._current_worker.wait()

