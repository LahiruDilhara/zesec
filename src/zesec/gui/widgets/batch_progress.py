"""Batch progress widget for showing total files and percentage."""

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt

class BatchProgressWidget(QWidget):
    """Widget showing files processed count, a progress bar, and percentage."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
        
    def _init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.count_label = QLabel("0/0")
        self.count_label.setMinimumWidth(40)
        self.count_label.setStyleSheet("font-weight: bold; color: #555555;")
        layout.addWidget(self.count_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedHeight(12)
        self.progress_bar.setStyleSheet(
            "QProgressBar::chunk { background-color: #3498db; border-radius: 4px; } "
            "QProgressBar { border: 1px solid #ced4da; border-radius: 4px; background-color: #f8f9fa; }"
        )
        layout.addWidget(self.progress_bar, 1)
        
        self.pct_label = QLabel("0%")
        self.pct_label.setMinimumWidth(40)
        self.pct_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.pct_label.setStyleSheet("font-weight: bold; color: #3498db;")
        layout.addWidget(self.pct_label)
        
    def reset(self, total: int):
        """Reset the progress bar with a new total."""
        self.count_label.setText(f"0/{total}")
        self.progress_bar.setValue(0)
        self.pct_label.setText("0%")
        
    def set_total(self, total: int):
        """Update the total files count dynamically."""
        text = self.count_label.text()
        completed = text.split('/')[0] if '/' in text else '0'
        current_total = int(text.split('/')[1]) if '/' in text else 0
        
        # Auto-reset if we were at 100% and added new files
        if self.progress_bar.value() == 100 and total > current_total:
            self.reset(total)
        elif self.progress_bar.value() == 0 or total == 0:
            # If nothing has started yet or all removed, just reset
            self.reset(total)
        else:
            self.count_label.setText(f"{completed}/{total}")
        
    def update_progress(self, completed: int, total: int, current_file_progress: int):
        """Update the progress bar based on completed files and current file progress."""
        self.count_label.setText(f"{completed}/{total}")
        if total > 0:
            total_progress = int(((completed * 100) + current_file_progress) / total)
        else:
            total_progress = 0
            
        # Ensure it doesn't exceed 100
        total_progress = min(100, max(0, total_progress))
        
        self.progress_bar.setValue(total_progress)
        self.pct_label.setText(f"{total_progress}%")
