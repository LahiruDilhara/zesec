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

class IconButton(QPushButton):
    """Custom icon button with hand cursor and modern hover styling."""
    
    def __init__(self, icon_path: str, size: int = 26, icon_size: int = 16, hover_bg: str = "rgba(149, 165, 166, 0.2)", parent=None):
        super().__init__(parent)
        self.setIcon(QIcon(icon_path))
        self.setIconSize(QSize(icon_size, icon_size))
        self.setFixedSize(size, size)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(f"""
            IconButton {{ 
                background: transparent; 
                border: none; 
                border-radius: 4px;
            }}
            IconButton:hover {{ 
                background: {hover_bg}; 
            }}
            IconButton:pressed {{
                background: rgba(149, 165, 166, 0.4); 
            }}
            IconButton:disabled {{ 
                background: transparent;
            }}
        """)


class FileItemWidget(QWidget):
    """Custom widget for a file item in the list."""
    
    delete_clicked = Signal(Path)
    move_up_clicked = Signal(Path)
    move_down_clicked = Signal(Path)
    
    _zesec_pixmap = None
    _svg_paths = {}
    
    @classmethod
    def _get_cached_pixmap(cls):
        if cls._zesec_pixmap is None:
            icon_path = get_asset_path("icon/icon.png")
            if icon_path.exists():
                cls._zesec_pixmap = QPixmap(str(icon_path)).scaled(18, 18, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            else:
                cls._zesec_pixmap = QPixmap()
        return cls._zesec_pixmap

    @classmethod
    def _get_cached_svg_path(cls, filename: str) -> str:
        """Get the absolute path to an SVG asset with caching."""
        if filename not in cls._svg_paths:
            cls._svg_paths[filename] = str(get_asset_path(f"svg/{filename}"))
        return cls._svg_paths[filename]
    
    def __init__(self, path: Path, parent=None):
        super().__init__(parent)
        self.path = path
        self._init_ui()
        
    def _get_svg_path(self, filename: str) -> str:
        """Get the absolute path to an SVG asset."""
        return self._get_cached_svg_path(filename)
        
    def _init_ui(self):
        self.setMinimumHeight(44)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
            FileItemWidget { 
                background: rgba(127, 140, 141, 0.05); 
                border-radius: 6px; 
                border: 1px solid rgba(127, 140, 141, 0.1);
            }
            FileItemWidget:hover {
                background: rgba(127, 140, 141, 0.1);
            }
            QLabel { background: transparent; border: none; }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 8, 15, 8)
        layout.setSpacing(15)  # Global spacing between elements
        layout.setAlignment(Qt.AlignVCenter)
        
        # Number indicator
        self.number_label = QLabel("1.")
        self.number_label.setAlignment(Qt.AlignVCenter)
        self.number_label.setStyleSheet("font-weight: bold; color: #7f8c8d; font-size: 13px;")
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
            pixmap = self._get_cached_pixmap()
            if not pixmap.isNull():
                self.logo_label.setPixmap(pixmap)
        layout.addWidget(self.logo_label, 0)
        
        self.name_label = QLabel(self.path.name)
        self.name_label.setAlignment(Qt.AlignVCenter)
        self.name_label.setStyleSheet("color: #2c3e50; font-size: 13px; font-weight: 500;")
        self.name_label.setMinimumWidth(100)
        layout.addWidget(self.name_label, 1) # 1 stretch factor
        
        up_svg_path = self._get_svg_path("up.svg")
        self.up_btn = IconButton(up_svg_path)
        self.up_btn.clicked.connect(lambda: self.move_up_clicked.emit(self.path))
        layout.addWidget(self.up_btn, 0)
        
        down_svg_path = self._get_svg_path("down.svg")
        self.down_btn = IconButton(down_svg_path)
        self.down_btn.clicked.connect(lambda: self.move_down_clicked.emit(self.path))
        layout.addWidget(self.down_btn, 0)
        
        bin_svg_path = self._get_svg_path("bin.svg")
        self.delete_btn = IconButton(bin_svg_path, size=30, icon_size=18, hover_bg="rgba(231, 76, 60, 0.2)")
        self.delete_btn.clicked.connect(lambda: self.delete_clicked.emit(self.path))
        layout.addWidget(self.delete_btn, 0)
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if not hasattr(self, 'name_label') or not hasattr(self, 'path'):
            return
            
        # Cache width to prevent expensive font metrics calculation on every minor event
        current_width = self.name_label.width()
        if hasattr(self, '_last_width') and self._last_width == current_width:
            return
        self._last_width = current_width
            
        from PySide6.QtGui import QFontMetrics
        metrics = QFontMetrics(self.name_label.font())
        width = current_width - 5
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


class MultiFileSelectorWidget(QWidget):
    """Widget for selecting multiple files with a list view."""
    
    paths_changed = Signal(list)
    cancel_clicked = Signal()
    
    def __init__(self, parent=None, file_filter: str = "All Files (*)"):
        """Initialize multi-file selector.
        
        Args:
            parent: Parent widget
            file_filter: File filter string for file dialog
        """
        super().__init__(parent)
        self._file_filter = file_filter
        self._paths: List[Path] = []
        self._paths_set = set()
        self._path_to_widget = {}
        self._current_progress_widget = None
        self._shared_progress = QProgressBar(self)
        self._shared_progress.hide()
        self._shared_progress.setFixedHeight(12)
        self._shared_progress.setTextVisible(True)
        self._shared_progress.setFormat("%p%")
        self._shared_progress.setStyleSheet(
            "QProgressBar::chunk { background-color: #2ecc71; border-radius: 4px; } "
            "QProgressBar { border: 1px solid #ced4da; border-radius: 4px; text-align: center; font-size: 9px; color: #333333; }"
        )
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
        
        self._cancel_btn = HoverButton("Cancel", base_color="#e74c3c")
        self._cancel_btn.clicked.connect(self._on_cancel_clicked)
        self._cancel_btn.setEnabled(False)
        
        btn_layout.addWidget(self._add_btn)
        btn_layout.addWidget(self._clear_btn)
        btn_layout.addWidget(self._cancel_btn)
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
        self._list_widget.setSelectionMode(QListWidget.NoSelection)
        self._list_widget.setUniformItemSizes(True)  # CRITICAL for scroll performance with large lists
        self._list_widget.setStyleSheet("QListWidget { border: none; background: transparent; outline: none; } QListWidget::item { border: none; outline: none; }")
        self._list_widget.setSpacing(5) # Give spacing between rows
        self._stack.addWidget(self._list_widget)
        
        layout.addWidget(self._stack)
        
        self._update_ui_state()
        
    def set_processing(self, processing: bool):
        """Disable UI elements during processing in batches to prevent UI freezing."""
        self._processing_state = processing
        self._add_btn.setEnabled(not processing)
        self._clear_btn.setEnabled(not processing)
        self._cancel_btn.setEnabled(processing)
        
        def disable_chunk(start_idx):
            if getattr(self, '_processing_state', None) != processing:
                return
            count = self._list_widget.count()
            end_idx = min(start_idx + 100, count)
            for i in range(start_idx, end_idx):
                item = self._list_widget.item(i)
                widget = self._list_widget.itemWidget(item)
                if isinstance(widget, FileItemWidget):
                    widget.set_processing(processing)
            
            if end_idx < count:
                from PySide6.QtCore import QTimer
                QTimer.singleShot(2, lambda: disable_chunk(end_idx))
                
        disable_chunk(0)
                
    def _add_files(self):
        """Open file dialog and add files."""
        paths, _ = QFileDialog.getOpenFileNames(
            self, "Select Files", "", self._file_filter
        )
        
        if not paths:
            return
            
        self._pending_paths = [Path(p) for p in paths]
        self._added_any = False
        
        # Change add and clear buttons to disabled while processing
        self._add_btn.setEnabled(False)
        self._clear_btn.setEnabled(False)
        
        self._process_pending_paths()

    def _process_pending_paths(self):
        if not hasattr(self, '_pending_paths') or not self._pending_paths:
            self._add_btn.setEnabled(True)
            self._clear_btn.setEnabled(True)
            if hasattr(self, '_added_any') and self._added_any:
                self._update_ui_state()
                self.paths_changed.emit(self.get_paths())
                self._added_any = False
            return
            
        # Process a chunk of files to keep UI responsive
        chunk_size = 50
        chunk = self._pending_paths[:chunk_size]
        self._pending_paths = self._pending_paths[chunk_size:]
        
        self._list_widget.setUpdatesEnabled(False)
        try:
            for path in chunk:
                if path not in self._paths_set:
                    self._paths.append(path)
                    self._paths_set.add(path)
                    
                    item = QListWidgetItem()
                    item.setData(Qt.UserRole, path)
                    self._list_widget.addItem(item)
                    
                    widget = FileItemWidget(path)
                    self._path_to_widget[path] = widget
                    widget.set_number(self._list_widget.count())
                    widget.delete_clicked.connect(self._remove_item)
                    widget.move_up_clicked.connect(self._move_item_up)
                    widget.move_down_clicked.connect(self._move_item_down)
                    item.setSizeHint(QSize(0, 45))
                    self._list_widget.setItemWidget(item, widget)
                    
                    self._added_any = True
        finally:
            self._list_widget.setUpdatesEnabled(True)
            
        # Emit partial update so user can see progress (optional, but let's just wait until end or emit after chunk)
        if self._added_any:
            self._update_ui_state()
            
        # Schedule next chunk
        from PySide6.QtCore import QTimer
        QTimer.singleShot(10, self._process_pending_paths)
            
    def _redraw_list(self):
        """Redraw the entire list based on self._paths."""
        self._list_widget.clear()
        self._path_to_widget.clear()
        self._list_widget.setUpdatesEnabled(False)
        try:
            for i, path in enumerate(self._paths):
                item = QListWidgetItem()
                item.setData(Qt.UserRole, path)
                self._list_widget.addItem(item)
                
                widget = FileItemWidget(path)
                self._path_to_widget[path] = widget
                widget.set_number(i + 1)
                widget.delete_clicked.connect(self._remove_item)
                widget.move_up_clicked.connect(self._move_item_up)
                widget.move_down_clicked.connect(self._move_item_down)
                item.setSizeHint(QSize(0, 45))
                self._list_widget.setItemWidget(item, widget)
        finally:
            self._list_widget.setUpdatesEnabled(True)
            
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
        if path in self._paths_set:
            self._paths.remove(path)
            self._paths_set.remove(path)
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
        if self._current_progress_widget:
            self._current_progress_widget.layout().removeWidget(self._shared_progress)
            self._shared_progress.setParent(self)
            self._shared_progress.hide()
            self._current_progress_widget = None
        self._paths.clear()
        self._paths_set.clear()
        self._path_to_widget.clear()
        self._list_widget.clear()
        self._update_ui_state()
        self.paths_changed.emit([])

    def update_file_progress(self, path: Path, value: int):
        """Update progress for a specific file."""
        if path not in self._path_to_widget:
            return
            
        widget = self._path_to_widget[path]
        
        if self._current_progress_widget != widget:
            if self._current_progress_widget:
                self._current_progress_widget.layout().removeWidget(self._shared_progress)
                self._shared_progress.setParent(self)
                self._current_progress_widget._set_circle_color("#2ecc71")
                
            # Insert before up, down, delete buttons
            insert_idx = widget.layout().count() - 3
            widget.layout().insertWidget(insert_idx, self._shared_progress, 1)
            self._shared_progress.show()
            widget._set_circle_color("#f39c12")
            self._current_progress_widget = widget
            
        self._shared_progress.setValue(value)
        
        if value >= 100:
            widget.layout().removeWidget(self._shared_progress)
            self._shared_progress.setParent(self)
            self._shared_progress.hide()
            widget._set_circle_color("#2ecc71")
            self._current_progress_widget = None

    def _on_cancel_clicked(self):
        """Handle cancel button click."""
        self._cancel_btn.setEnabled(False)
        self.cancel_clicked.emit()

    def mark_file_failed(self, path: Path):
        """Mark a specific file as failed."""
        if path in self._path_to_widget:
            widget = self._path_to_widget[path]
            if self._current_progress_widget == widget:
                widget.layout().removeWidget(self._shared_progress)
                self._shared_progress.setParent(self)
                self._shared_progress.hide()
                self._current_progress_widget = None
            widget._set_circle_color("#e74c3c") # Red

    def retain_failed_files(self, failed_paths: List[Path]):
        """Clear successful files and retain failed ones."""
        if not failed_paths:
            self.clear()
            return
            
        self._list_widget.clear()
        self._path_to_widget.clear()
        
        self._paths = [p for p in self._paths if p in failed_paths]
        self._paths_set = set(self._paths)
        
        self._list_widget.setUpdatesEnabled(False)
        try:
            for i, path in enumerate(self._paths):
                item = QListWidgetItem()
                item.setData(Qt.UserRole, path)
                self._list_widget.addItem(item)
                
                widget = FileItemWidget(path)
                self._path_to_widget[path] = widget
                widget.set_number(i + 1)
                widget._set_circle_color("#e74c3c") # Red
                widget.delete_clicked.connect(self._remove_item)
                widget.move_up_clicked.connect(self._move_item_up)
                widget.move_down_clicked.connect(self._move_item_down)
                item.setSizeHint(QSize(0, 45))
                self._list_widget.setItemWidget(item, widget)
        finally:
            self._list_widget.setUpdatesEnabled(True)
            
        self._update_ui_state()
        self.paths_changed.emit(self.get_paths())
