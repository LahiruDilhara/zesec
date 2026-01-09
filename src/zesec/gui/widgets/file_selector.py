"""File selector widget."""

from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QLineEdit, QPushButton, QFileDialog
)


class FileSelectorWidget(QWidget):
    """Widget for selecting files with a browse button."""
    
    def __init__(self, parent=None, is_directory: bool = False, file_filter: str = "All Files (*)"):
        """Initialize file selector.
        
        Args:
            parent: Parent widget
            is_directory: If True, select directory instead of file
            file_filter: File filter string for file dialog
        """
        super().__init__(parent)
        self._is_directory = is_directory
        self._file_filter = file_filter
        self._init_ui()
        
    def _init_ui(self):
        """Initialize UI components."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self._path_edit = QLineEdit()
        self._path_edit.setPlaceholderText("No file selected")
        self._path_edit.setReadOnly(True)
        layout.addWidget(self._path_edit)
        
        self._browse_btn = QPushButton("Browse...")
        self._browse_btn.clicked.connect(self._browse_file)
        layout.addWidget(self._browse_btn)
        
    def _browse_file(self):
        """Open file dialog."""
        if self._is_directory:
            path = QFileDialog.getExistingDirectory(self, "Select Directory")
        else:
            path, _ = QFileDialog.getOpenFileName(
                self, "Select File", "", self._file_filter
            )
        
        if path:
            self.set_path(Path(path))
            
    def set_path(self, path: Path):
        """Set the selected path."""
        self._path_edit.setText(str(path))
        
    def get_path(self) -> Optional[Path]:
        """Get the selected path."""
        text = self._path_edit.text()
        if text:
            return Path(text)
        return None
        
    def clear(self):
        """Clear the selected path."""
        self._path_edit.clear()

