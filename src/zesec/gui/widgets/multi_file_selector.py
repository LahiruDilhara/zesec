"""Multi-file selector widget."""

from pathlib import Path
from typing import List

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFileDialog,
    QListWidget, QListWidgetItem, QLabel, QStackedWidget, QProgressBar
)
from .hover_button import HoverButton
from PySide6.QtCore import Qt, Signal, QSize

class FileItemWidget(QWidget):
    """Custom widget for a file item in the list."""
    
    delete_clicked = Signal(Path)
    
    def __init__(self, path: Path, parent=None):
        super().__init__(parent)
        self.path = path
        self._init_ui()
        
    def _init_ui(self):
        self.setMinimumHeight(40)
        self.setStyleSheet("FileItemWidget { background: transparent; }")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Circle indicator
        self.status_circle = QLabel()
        self.status_circle.setFixedSize(12, 12)
        self._set_circle_color("#bdc3c7") # Grey initially
        layout.addWidget(self.status_circle, 0)
        
        self.name_label = QLabel(self.path.name)
        self.name_label.setToolTip(str(self.path))
        self.name_label.setStyleSheet("background: transparent;")
        layout.addWidget(self.name_label, 2)
        
        self.progress = QProgressBar()
        self.progress.setFixedHeight(12)
        self.progress.setTextVisible(True)
        self.progress.setFormat("%p%")
        self.progress.setValue(0)
        self.progress.setStyleSheet(
            "QProgressBar::chunk { background-color: #2ecc71; border-radius: 4px; } "
            "QProgressBar { border: 1px solid #ced4da; border-radius: 4px; text-align: center; font-size: 9px; color: #333333; }"
        )
        self.progress.setVisible(False)
        layout.addWidget(self.progress, 3)
        
        self.delete_btn = HoverButton("Remove", base_color="#e74c3c")
        self.delete_btn.set_padding("2px 10px")
        self.delete_btn.clicked.connect(lambda: self.delete_clicked.emit(self.path))
        layout.addWidget(self.delete_btn, 0)
        
    def _set_circle_color(self, color: str):
        self.status_circle.setStyleSheet(f"background-color: {color}; border-radius: 6px;")
        
    def update_progress(self, value: int):
        self.progress.setValue(value)
        if value < 100:
            if not self.progress.isVisible():
                self.progress.setVisible(True)
                self._set_circle_color("#f39c12") # Orange while processing
        else:
            self.progress.setVisible(False)
            self._set_circle_color("#2ecc71") # Green when finished


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
        self._add_btn = HoverButton("Add Files...")
        self._add_btn.clicked.connect(self._add_files)
        
        btn_layout.addWidget(self._add_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        # Stacked widget to switch between "No files" and the list
        self._stack = QStackedWidget()
        self._stack.setMinimumHeight(150)  # Expandable
        
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
                item = QListWidgetItem()
                item.setData(Qt.UserRole, path)
                self._list_widget.addItem(item)
                
                widget = FileItemWidget(path)
                widget.delete_clicked.connect(self._remove_item)
                item.setSizeHint(QSize(0, 45))
                self._list_widget.setItemWidget(item, widget)
                
                added = True
                
        if added:
            self._update_ui_state()
            self.paths_changed.emit(self.get_paths())
            
    def _remove_item(self, path: Path):
        """Remove an item from the list by path."""
        if path in self._paths:
            self._paths.remove(path)
            
        for i in range(self._list_widget.count()):
            item = self._list_widget.item(i)
            if item.data(Qt.UserRole) == path:
                self._list_widget.takeItem(i)
                break
                
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

    def update_file_progress(self, path: Path, value: int):
        """Update progress for a specific file."""
        for i in range(self._list_widget.count()):
            item = self._list_widget.item(i)
            if item.data(Qt.UserRole) == path:
                widget = self._list_widget.itemWidget(item)
                if isinstance(widget, FileItemWidget):
                    widget.update_progress(value)
                break
