"""Worker thread for key generation operations."""

from pathlib import Path

from PySide6.QtCore import QThread, Signal

from ...core.encryption import KeyManager


class KeyGenerationWorker(QThread):
    """Worker thread for key generation operations."""
    
    progress = Signal(int)  # 0-100
    finished = Signal(bool, str)  # success, message
    error = Signal(str)
    
    def __init__(
        self,
        key_manager: KeyManager,
        key_file_path: Path,
        parent=None
    ):
        """Initialize key generation worker.
        
        Args:
            key_manager: Key manager service
            key_file_path: Path where key file should be saved
            parent: Parent QObject
        """
        super().__init__(parent)
        self._key_manager = key_manager
        self._key_file_path = key_file_path
        
    def run(self):
        """Execute key generation in background thread."""
        try:
            self.progress.emit(10)
            
            success = self._key_manager.generate_key_file(self._key_file_path)
            
            self.progress.emit(100)
            
            if success:
                self.finished.emit(True, f"Key file generated: {self._key_file_path}")
            else:
                self.finished.emit(False, "Failed to generate key file")
                
        except Exception as e:
            self.error.emit(str(e))

