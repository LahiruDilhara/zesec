"""Controller for file cleaning operations."""

from pathlib import Path
from typing import Optional

from PySide6.QtCore import QObject, Signal

from ...di.container import ApplicationContainer
from ...interfaces.cleaner_interface import ICleaner
from ..workers.clean_worker import CleanWorker


class CleanController(QObject):
    """Presenter for file cleaning operations."""
    
    # Signals to communicate with View
    progress_updated = Signal(int)  # 0-100
    operation_completed = Signal(bool, str)  # success, message
    error_occurred = Signal(str)
    
    def __init__(self, container: ApplicationContainer):
        """Initialize cleaning controller.
        
        Args:
            container: DI container
        """
        super().__init__()
        self._container = container
        self._cleaner: ICleaner = container.cleaner()
        self._current_worker: Optional[CleanWorker] = None
        
    def clean_file(
        self,
        file_path: Path,
        delete: bool = True
    ):
        """Initiate cleaning operation.
        
        Args:
            file_path: Path to file to clean
            delete: Whether to delete file after cleaning
        """
        # Validation
        if not file_path.exists():
            self.error_occurred.emit("File does not exist")
            return
            
        # Cancel any existing operation
        if self._current_worker and self._current_worker.isRunning():
            self._current_worker.terminate()
            self._current_worker.wait()
        
        # Create worker for async operation
        worker = CleanWorker(
            self._cleaner,
            file_path,
            delete
        )
        
        # Connect worker signals
        worker.progress.connect(self.progress_updated)
        worker.finished.connect(self.operation_completed)
        worker.error.connect(self.error_occurred)
        
        # Store reference and start worker
        self._current_worker = worker
        worker.start()
        
    def cancel_operation(self):
        """Cancel current cleaning operation."""
        if self._current_worker and self._current_worker.isRunning():
            self._current_worker.terminate()
            self._current_worker.wait()

