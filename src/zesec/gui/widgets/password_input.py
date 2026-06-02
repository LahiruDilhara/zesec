"""Secure password input widget."""

# pyrefly: ignore [missing-import]
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QCheckBox
)
from PySide6.QtCore import Signal, Qt

class PasswordInputWidget(QWidget):
    """Widget for secure password input with show/hide toggle."""
    
    text_changed = Signal(str)
    
    def __init__(self, parent=None, label: str = "Password:", is_confirm: bool = False):
        """Initialize password input.
        
        Args:
            parent: Parent widget
            label: Label text for the password field
            is_confirm: Whether this is a confirm password field with matching indicator
        """
        super().__init__(parent)
        self.is_confirm = is_confirm
        self._target_widget = None
        self._init_ui(label)
        
    def _init_ui(self, label: str):
        """Initialize UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        label_layout = QHBoxLayout()
        label_layout.setContentsMargins(0, 0, 0, 0)
        
        if self.is_confirm:
            self.status_circle = QLabel()
            self.status_circle.setFixedSize(12, 12)
            self._set_circle_color("#bdc3c7")
            label_layout.addWidget(self.status_circle)
            
        self.label_widget = QLabel(label)
        label_layout.addWidget(self.label_widget)
        
        if self.is_confirm:
            self.match_label = QLabel("")
            self.match_label.setStyleSheet("color: #e74c3c; font-size: 11px; margin-left: 10px;")
            label_layout.addWidget(self.match_label)
            
        label_layout.addStretch()
        layout.addLayout(label_layout)
        
        self._password_edit = QLineEdit()
        self._password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self._password_edit.textChanged.connect(self.text_changed.emit)
        layout.addWidget(self._password_edit)
        
        self._show_password_check = QCheckBox("Show password")
        self._show_password_check.setCursor(Qt.PointingHandCursor)
        self._show_password_check.toggled.connect(self._toggle_password_visibility)
        layout.addWidget(self._show_password_check)
        
    def _toggle_password_visibility(self, checked: bool):
        """Toggle password visibility."""
        if checked:
            self._password_edit.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self._password_edit.setEchoMode(QLineEdit.EchoMode.Password)
            
    def get_password(self) -> str:
        """Get the entered password."""
        return self._password_edit.text()
        
    def set_password(self, password: str):
        """Set the password (for testing purposes)."""
        self._password_edit.setText(password)
        
    def clear(self):
        """Clear the password field."""
        self._password_edit.clear()
        self._show_password_check.setChecked(False)
        if self.is_confirm:
            self._check_match()
            
    def set_match_target(self, target_widget):
        """Set the target password widget to compare against."""
        self._target_widget = target_widget
        target_widget.text_changed.connect(self._check_match)
        self.text_changed.connect(self._check_match)
        
    def _check_match(self, _=""):
        if not self.is_confirm or not self._target_widget:
            return
            
        p1 = self._target_widget.get_password()
        p2 = self.get_password()
        
        if not p1 and not p2:
            self._set_circle_color("#bdc3c7")
            self.match_label.setText("")
        elif p1 == p2:
            self._set_circle_color("#2ecc71")
            self.match_label.setText("Passwords match")
            self.match_label.setStyleSheet("color: #2ecc71; font-size: 11px; margin-left: 10px;")
        else:
            self._set_circle_color("#e74c3c")
            self.match_label.setText("Passwords do not match")
            self.match_label.setStyleSheet("color: #e74c3c; font-size: 11px; margin-left: 10px;")
            
    def _set_circle_color(self, color: str):
        if hasattr(self, 'status_circle'):
            self.status_circle.setStyleSheet(f"background-color: {color}; border-radius: 6px;")

