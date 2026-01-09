"""Secure password input widget."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QLabel, QCheckBox
)


class PasswordInputWidget(QWidget):
    """Widget for secure password input with show/hide toggle."""
    
    def __init__(self, parent=None, label: str = "Password:"):
        """Initialize password input.
        
        Args:
            parent: Parent widget
            label: Label text for the password field
        """
        super().__init__(parent)
        self._init_ui(label)
        
    def _init_ui(self, label: str):
        """Initialize UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        label_widget = QLabel(label)
        layout.addWidget(label_widget)
        
        self._password_edit = QLineEdit()
        self._password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self._password_edit)
        
        self._show_password_check = QCheckBox("Show password")
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

