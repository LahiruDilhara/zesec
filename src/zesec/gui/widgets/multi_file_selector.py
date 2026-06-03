"""Multi-file selector widget."""

import os
import sys
from pathlib import Path
from typing import List

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFileDialog,
    QListWidget, QListWidgetItem, QLabel, QStackedWidget, QProgressBar,
    QPushButton
)
from PySide6.QtGui import QIcon
from .hover_button import HoverButton
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QPixmap
import sys

from ...utils.asset_utils import get_asset_path

class FileItemWidget(QWidget):
    """Custom widget for a file item in the list."""
    
    delete_clicked = Signal(Path)
    move_up_clicked = Signal(Path)
    move_down_clicked = Signal(Path)
    
    def __init__(self, path: Path, parent=None):
        super().__init__(parent)
        self.path = path
        self._init_ui()
        
    def _get_svg_path(self, filename: str) -> str:
        """Get the absolute path to an SVG asset."""
        return str(get_asset_path(f"svg/{filename}"))
        
    def _init_ui(self):
        self.setMinimumHeight(40)
        self.setStyleSheet("FileItemWidget { background: transparent; }")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(15)  # Global spacing between elements
        
        # Number indicator
        self.number_label = QLabel("1.")
        self.number_label.setStyleSheet("background: transparent; font-weight: bold; color: #7f8c8d;")
        self.number_label.setFixedWidth(25)
        layout.addWidget(self.number_label, 0)
        
        # Circle indicator
        self.status_circle = QLabel()
        self.status_circle.setFixedSize(12, 12)
        self._set_circle_color("#bdc3c7") # Grey initially
        layout.addWidget(self.status_circle, 0)
        
        # Logo indicator for .zesec files
        self.logo_label = QLabel()
        self.logo_label.setFixedSize(18, 18)
        if self.path.name.endswith(".zesec"):
            icon_path = get_asset_path("icon/icon.png")
            if icon_path.exists():
                pixmap = QPixmap(str(icon_path)).scaled(18, 18, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.logo_label.setPixmap(pixmap)
        layout.addWidget(self.logo_label, 0)
        
        self.name_label = QLabel(self.path.name)
        self.name_label.setStyleSheet("background: transparent;")
        self.name_label.setToolTip(self.path.name)
        self.name_label.setMinimumWidth(100)
        layout.addWidget(self.name_label, 1) # 1 stretch factor
        
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
        layout.addWidget(self.progress, 1)
        
        up_svg_path = self._get_svg_path("up.svg")
        self.up_btn = QPushButton("")
        self.up_btn.setIcon(QIcon(up_svg_path))
        self.up_btn.setIconSize(QSize(16, 16))
        self.up_btn.setFixedSize(26, 26)
        self.up_btn.setStyleSheet(
            "QPushButton { background: transparent; border: none; }"
            "QPushButton:hover { background: rgba(0, 0, 0, 10%); border-radius: 4px; }"
            "QPushButton:disabled { opacity: 0.5; }"
        )
        self.up_btn.clicked.connect(lambda: self.move_up_clicked.emit(self.path))
        layout.addWidget(self.up_btn, 0)
        
        down_svg_path = self._get_svg_path("down.svg")
        self.down_btn = QPushButton("")
        self.down_btn.setIcon(QIcon(down_svg_path))
        self.down_btn.setIconSize(QSize(16, 16))
        self.down_btn.setFixedSize(26, 26)
        self.down_btn.setStyleSheet(
            "QPushButton { background: transparent; border: none; }"
            "QPushButton:hover { background: rgba(0, 0, 0, 10%); border-radius: 4px; }"
            "QPushButton:disabled { opacity: 0.5; }"
        )
        self.down_btn.clicked.connect(lambda: self.move_down_clicked.emit(self.path))
        layout.addWidget(self.down_btn, 0)
        
        bin_svg_path = self._get_svg_path("bin.svg")
        self.delete_btn = QPushButton("")
        self.delete_btn.setIcon(QIcon(bin_svg_path))
        self.delete_btn.setIconSize(QSize(18, 18))
        self.delete_btn.setFixedSize(30, 30)
        self.delete_btn.setStyleSheet(
            "QPushButton { background: transparent; border: none; }"
            "QPushButton:hover { background: rgba(0, 0, 0, 10%); border-radius: 4px; }"
            "QPushButton:disabled { opacity: 0.5; }"
        )
        self.delete_btn.clicked.connect(lambda: self.delete_clicked.emit(self.path))
        layout.addWidget(self.delete_btn, 0)
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'name_label') and hasattr(self, 'path'):
            from PySide6.QtGui import QFontMetrics
            metrics = QFontMetrics(self.name_label.font())
            width = self.name_label.width() - 5
            if width > 0:
                elided = metrics.elidedText(self.path.name, Qt.ElideMiddle, width)
                self.name_label.setText(elided)
        
    def _set_circle_color(self, color: str):
        self.status_circle.setStyleSheet(f"background-color: {color}; border-radius: 6px;")
        
    def set_number(self, num: int):
        self.number_label.setText(f"{num}.")
        
    def set_processing(self, processing: bool):
        """Disable or enable buttons during processing."""
        self.delete_btn.setEnabled(not processing)
        self.up_btn.setEnabled(not processing)
        self.down_btn.setEnabled(not processing)
        
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
        
        self._clear_btn = HoverButton("Clear All", base_color="#95a5a6")
        self._clear_btn.clicked.connect(self.clear)
        
        btn_layout.addWidget(self._add_btn)
        btn_layout.addWidget(self._clear_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        # Stacked widget to switch between "No files" and the list
        self._stack = QStackedWidget()
        self._stack.setFixedHeight(280)  # Fixed height for list
        
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
        
    def set_processing(self, processing: bool):
        """Disable UI elements during processing."""
        self._add_btn.setEnabled(not processing)
        self._clear_btn.setEnabled(not processing)
        for i in range(self._list_widget.count()):
            item = self._list_widget.item(i)
            widget = self._list_widget.itemWidget(item)
            if isinstance(widget, FileItemWidget):
                widget.set_processing(processing)
                
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
                widget.set_number(self._list_widget.count())
                widget.delete_clicked.connect(self._remove_item)
                widget.move_up_clicked.connect(self._move_item_up)
                widget.move_down_clicked.connect(self._move_item_down)
                item.setSizeHint(QSize(0, 45))
                self._list_widget.setItemWidget(item, widget)
                
                added = True
                
        if added:
            self._update_ui_state()
            self.paths_changed.emit(self.get_paths())
            
    def _redraw_list(self):
        """Redraw the entire list based on self._paths."""
        self._list_widget.clear()
        for i, path in enumerate(self._paths):
            item = QListWidgetItem()
            item.setData(Qt.UserRole, path)
            self._list_widget.addItem(item)
            
            widget = FileItemWidget(path)
            widget.set_number(i + 1)
            widget.delete_clicked.connect(self._remove_item)
            widget.move_up_clicked.connect(self._move_item_up)
            widget.move_down_clicked.connect(self._move_item_down)
            item.setSizeHint(QSize(0, 45))
            self._list_widget.setItemWidget(item, widget)
            
        self._update_ui_state()
        self.paths_changed.emit(self.get_paths())
            
    def _move_item_up(self, path: Path):
        """Move an item up in the list."""
        if path not in self._paths:
            return
        idx = self._paths.index(path)
        if idx > 0:
            self._paths[idx], self._paths[idx - 1] = self._paths[idx - 1], self._paths[idx]
            self._redraw_list()

    def _move_item_down(self, path: Path):
        """Move an item down in the list."""
        if path not in self._paths:
            return
        idx = self._paths.index(path)
        if idx < len(self._paths) - 1:
            self._paths[idx], self._paths[idx + 1] = self._paths[idx + 1], self._paths[idx]
            self._redraw_list()

    def _remove_item(self, path: Path):
        """Remove an item from the list by path."""
        if path in self._paths:
            self._paths.remove(path)
            self._redraw_list()
            
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
