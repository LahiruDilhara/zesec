"""Multi-file selector widget."""

from pathlib import Path
from typing import List

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog,
    QListWidget, QListWidgetItem, QLabel, QStackedWidget
)
from PySide6.QtCore import Qt, Signal


class MultiFileSelectorWidget(QWidget):
    """Widget for selecting multiple files with a list view."""
    
    paths_changed = Signal(list)
    
    def __init__(self, parent=None, file_filter: str = "All Files (*)"):
        """Initialize multi-file selector.
        
        Args:
            parent: Parent widget
            file_filter: File filter string for file dialog
        """
        super().__init__(parent)
        self._file_filter = file_filter
        self._paths: List[Path] = []
        self._init_ui()
        
    def _init_ui(self):
        """Initialize UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Buttons layout
        btn_layout = QHBoxLayout()
        self._add_btn = QPushButton("Add Files...")
        self._add_btn.clicked.connect(self._add_files)
        
        self._remove_btn = QPushButton("Remove Selected")
        self._remove_btn.clicked.connect(self._remove_selected)
        
        btn_layout.addWidget(self._add_btn)
        btn_layout.addWidget(self._remove_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        # Stacked widget to switch between "No files" and the list
        self._stack = QStackedWidget()
        self._stack.setFixedHeight(120)  # Specific height requested
        
        # Page 0: No files label
        self._empty_label = QLabel("No files added")
        self._empty_label.setAlignment(Qt.AlignCenter)
        self._empty_label.setStyleSheet("color: #6c757d; font-style: italic;")
        self._stack.addWidget(self._empty_label)
        
        # Page 1: List widget
        self._list_widget = QListWidget()
        self._stack.addWidget(self._list_widget)
        
        layout.addWidget(self._stack)
        
        self._update_ui_state()
        
    def _add_files(self):
        """Open file dialog and add files."""
        paths, _ = QFileDialog.getOpenFileNames(
            self, "Select Files", "", self._file_filter
        )
        
        if not paths:
            return
            
        added = False
        for path_str in paths:
            path = Path(path_str)
            if path not in self._paths:
                self._paths.append(path)
                
                # Add to list widget
                item = QListWidgetItem(path.name)
                item.setToolTip(str(path))
                item.setData(Qt.UserRole, path)
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                item.setCheckState(Qt.Unchecked)
                self._list_widget.addItem(item)
                added = True
                
        if added:
            self._update_ui_state()
            self.paths_changed.emit(self.get_paths())
            
    def _remove_selected(self):
        """Remove checked items from the list."""
        removed = False
        # Iterate backwards to safely remove items
        for i in range(self._list_widget.count() - 1, -1, -1):
            item = self._list_widget.item(i)
            if item.checkState() == Qt.Checked:
                path = item.data(Qt.UserRole)
                if path in self._paths:
                    self._paths.remove(path)
                self._list_widget.takeItem(i)
                removed = True
                
        if removed:
            self._update_ui_state()
            self.paths_changed.emit(self.get_paths())
            
    def _update_ui_state(self):
        """Update visibility of stacked widget pages."""
        if not self._paths:
            self._stack.setCurrentIndex(0)  # Show empty label
        else:
            self._stack.setCurrentIndex(1)  # Show list
            
    def get_paths(self) -> List[Path]:
        """Get the selected paths."""
        return self._paths.copy()
        
    def clear(self):
        """Clear all selected files."""
        self._paths.clear()
        self._list_widget.clear()
        self._update_ui_state()
        self.paths_changed.emit([])
