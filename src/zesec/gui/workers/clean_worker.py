"""Worker thread for file cleaning operations."""

from pathlib import Path

from PySide6.QtCore import QThread, Signal

from ...interfaces.cleaner_interface import ICleaner


class CleanWorker(QThread):
    """Worker thread for file cleaning operations."""
    
    progress = Signal(int)  # 0-100
    finished = Signal(bool, str)  # success, message
    error = Signal(str)
    
    def __init__(
        self,
        cleaner: ICleaner,
        file_path: Path,
        delete: bool = True,
        parent=None
    ):
        """Initialize cleaning worker.
        
        Args:
            cleaner: Cleaning service
            file_path: Path to file to clean
            delete: Whether to delete file after cleaning
            parent: Parent QObject
        """
        super().__init__(parent)
        self._cleaner = cleaner
        self._file_path = file_path
        self._delete = delete
        
    def run(self):
        """Execute cleaning in background thread."""
        try:
            self.progress.emit(10)
            
            success = self._cleaner.clean_file(
                self._file_path,
                delete=self._delete
            )
            
            self.progress.emit(100)
            
            if success:
                action = "cleaned and deleted" if self._delete else "cleaned"
                self.finished.emit(True, f"File {action} successfully")
            else:
                self.finished.emit(False, "Cleaning failed")
                
        except Exception as e:
            self.error.emit(str(e))

