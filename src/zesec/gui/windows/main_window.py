"""Main window for Zesec GUI application."""

from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QMessageBox,
    QTabWidget, QCheckBox, QProgressBar, QGroupBox,
    QFormLayout
)
from PySide6.QtCore import Qt

from ...di.container import ApplicationContainer
from ...core.models.encryption_result import EncryptionResult
from ..controllers.encrypt_controller import EncryptController
from ..controllers.decrypt_controller import DecryptController
from ..controllers.clean_controller import CleanController
from ..controllers.key_controller import KeyController
from ..widgets.file_selector import FileSelectorWidget
from ..widgets.password_input import PasswordInputWidget


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self, container: ApplicationContainer):
        """Initialize main window.
        
        Args:
            container: DI container
        """
        super().__init__()
        self._container = container
        
        # Create controllers
        self._encrypt_controller = EncryptController(container)
        self._decrypt_controller = DecryptController(container)
        self._clean_controller = CleanController(container)
        self._key_controller = KeyController(container)
        
        # Connect controller signals
        self._setup_controller_connections()
        
        # Initialize UI
        self._init_ui()
        
    def _setup_controller_connections(self):
        """Setup signal/slot connections for controllers."""
        # Encryption controller
        self._encrypt_controller.progress_updated.connect(
            lambda v: self._update_progress("encrypt", v)
        )
        self._encrypt_controller.operation_completed.connect(
            lambda r: self._on_encrypt_completed(r)
        )
        self._encrypt_controller.error_occurred.connect(
            lambda e: self._show_error("Encryption Error", e)
        )
        
        # Decryption controller
        self._decrypt_controller.progress_updated.connect(
            lambda v: self._update_progress("decrypt", v)
        )
        self._decrypt_controller.operation_completed.connect(
            lambda r: self._on_decrypt_completed(r)
        )
        self._decrypt_controller.error_occurred.connect(
            lambda e: self._show_error("Decryption Error", e)
        )
        
        # Cleaning controller
        self._clean_controller.progress_updated.connect(
            lambda v: self._update_progress("clean", v)
        )
        self._clean_controller.operation_completed.connect(
            lambda s, m: self._on_clean_completed(s, m)
        )
        self._clean_controller.error_occurred.connect(
            lambda e: self._show_error("Cleaning Error", e)
        )
        
        # Key generation controller
        self._key_controller.progress_updated.connect(
            lambda v: self._update_progress("key", v)
        )
        self._key_controller.operation_completed.connect(
            lambda s, m: self._on_key_completed(s, m)
        )
        self._key_controller.error_occurred.connect(
            lambda e: self._show_error("Key Generation Error", e)
        )
        
    def _init_ui(self):
        """Initialize UI components."""
        self.setWindowTitle("Zesec - Secure File Manager")
        self.setMinimumSize(700, 600)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        tabs = QTabWidget()
        main_layout.addWidget(tabs)
        
        # Encryption tab
        encrypt_tab = self._create_encrypt_tab()
        tabs.addTab(encrypt_tab, "Encryption")
        
        # Decryption tab
        decrypt_tab = self._create_decrypt_tab()
        tabs.addTab(decrypt_tab, "Decryption")
        
        # Cleaning tab
        clean_tab = self._create_clean_tab()
        tabs.addTab(clean_tab, "Cleaning")
        
        # Key Management tab
        key_tab = self._create_key_tab()
        tabs.addTab(key_tab, "Key Management")
        
    def _create_encrypt_tab(self) -> QWidget:
        """Create encryption tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        
        # File selection group
        file_group = QGroupBox("File Selection")
        file_layout = QVBoxLayout()
        self._encrypt_file_selector = FileSelectorWidget()
        file_layout.addWidget(self._encrypt_file_selector)
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)
        
        # Password input
        self._encrypt_password = PasswordInputWidget(label="Password:")
        layout.addWidget(self._encrypt_password)
        
        # Key file selection (optional)
        key_group = QGroupBox("Key File (Optional)")
        key_layout = QVBoxLayout()
        self._encrypt_key_file_selector = FileSelectorWidget(file_filter="Key Files (*.key);;All Files (*)")
        key_layout.addWidget(self._encrypt_key_file_selector)
        key_group.setLayout(key_layout)
        layout.addWidget(key_group)
        
        # Options
        options_group = QGroupBox("Options")
        options_layout = QVBoxLayout()
        self._encrypt_clean_original = QCheckBox("Securely clean original file after encryption")
        self._encrypt_clean_original.setChecked(True)
        options_layout.addWidget(self._encrypt_clean_original)
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Progress bar
        self._encrypt_progress = QProgressBar()
        self._encrypt_progress.setVisible(False)
        layout.addWidget(self._encrypt_progress)
        
        # Encrypt button
        encrypt_btn = QPushButton("Encrypt File")
        encrypt_btn.setStyleSheet("font-weight: bold; padding: 8px;")
        encrypt_btn.clicked.connect(self._on_encrypt_clicked)
        layout.addWidget(encrypt_btn)
        
        layout.addStretch()
        return widget
        
    def _create_decrypt_tab(self) -> QWidget:
        """Create decryption tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        
        # File selection group
        file_group = QGroupBox("Encrypted File Selection")
        file_layout = QVBoxLayout()
        self._decrypt_file_selector = FileSelectorWidget()
        file_layout.addWidget(self._decrypt_file_selector)
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)
        
        # Password input
        self._decrypt_password = PasswordInputWidget(label="Password:")
        layout.addWidget(self._decrypt_password)
        
        # Key file selection (optional)
        key_group = QGroupBox("Key File (If used during encryption)")
        key_layout = QVBoxLayout()
        self._decrypt_key_file_selector = FileSelectorWidget(file_filter="Key Files (*.key);;All Files (*)")
        key_layout.addWidget(self._decrypt_key_file_selector)
        key_group.setLayout(key_layout)
        layout.addWidget(key_group)
        
        # Progress bar
        self._decrypt_progress = QProgressBar()
        self._decrypt_progress.setVisible(False)
        layout.addWidget(self._decrypt_progress)
        
        # Decrypt button
        decrypt_btn = QPushButton("Decrypt File")
        decrypt_btn.setStyleSheet("font-weight: bold; padding: 8px;")
        decrypt_btn.clicked.connect(self._on_decrypt_clicked)
        layout.addWidget(decrypt_btn)
        
        layout.addStretch()
        return widget
        
    def _create_clean_tab(self) -> QWidget:
        """Create cleaning tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        
        # File selection group
        file_group = QGroupBox("File Selection")
        file_layout = QVBoxLayout()
        self._clean_file_selector = FileSelectorWidget()
        file_layout.addWidget(self._clean_file_selector)
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)
        
        # Options
        options_group = QGroupBox("Options")
        options_layout = QVBoxLayout()
        self._clean_delete = QCheckBox("Delete file after cleaning")
        self._clean_delete.setChecked(True)
        options_layout.addWidget(self._clean_delete)
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Warning label
        warning_label = QLabel(
            "⚠ Warning: This operation will permanently overwrite the file content. "
            "This action cannot be undone!"
        )
        warning_label.setWordWrap(True)
        warning_label.setStyleSheet("color: red; font-weight: bold;")
        layout.addWidget(warning_label)
        
        # Progress bar
        self._clean_progress = QProgressBar()
        self._clean_progress.setVisible(False)
        layout.addWidget(self._clean_progress)
        
        # Clean button
        clean_btn = QPushButton("Clean File")
        clean_btn.setStyleSheet("font-weight: bold; padding: 8px; background-color: #d32f2f; color: white;")
        clean_btn.clicked.connect(self._on_clean_clicked)
        layout.addWidget(clean_btn)
        
        layout.addStretch()
        return widget
        
    def _create_key_tab(self) -> QWidget:
        """Create key management tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        
        # Info label
        info_label = QLabel(
            "Generate a random encryption key file. This key file can be used "
            "in combination with a password for enhanced security."
        )
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # Key file selection
        key_group = QGroupBox("Key File Location")
        key_layout = QVBoxLayout()
        self._key_file_selector = FileSelectorWidget()
        # Override browse to use save dialog
        self._key_file_selector._browse_btn.clicked.disconnect()
        self._key_file_selector._browse_btn.clicked.connect(self._browse_key_file_save)
        key_layout.addWidget(self._key_file_selector)
        key_group.setLayout(key_layout)
        layout.addWidget(key_group)
        
        # Warning label
        warning_label = QLabel(
            "⚠ Keep your key file secure! Store it in a safe location. "
            "You will need it to decrypt files encrypted with this key."
        )
        warning_label.setWordWrap(True)
        warning_label.setStyleSheet("color: orange; font-weight: bold;")
        layout.addWidget(warning_label)
        
        # Progress bar
        self._key_progress = QProgressBar()
        self._key_progress.setVisible(False)
        layout.addWidget(self._key_progress)
        
        # Generate button
        generate_btn = QPushButton("Generate Key File")
        generate_btn.setStyleSheet("font-weight: bold; padding: 8px;")
        generate_btn.clicked.connect(self._on_generate_key_clicked)
        layout.addWidget(generate_btn)
        
        layout.addStretch()
        return widget
        
    def _browse_key_file_save(self):
        """Open save dialog for key file."""
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Key File", "", "Key Files (*.key);;All Files (*)"
        )
        if path:
            self._key_file_selector.set_path(Path(path))
            
    def _on_encrypt_clicked(self):
        """Handle encrypt button click."""
        file_path = self._encrypt_file_selector.get_path()
        if not file_path:
            self._show_error("Validation Error", "Please select a file to encrypt.")
            return
            
        password = self._encrypt_password.get_password()
        if not password:
            self._show_error("Validation Error", "Please enter a password.")
            return
            
        key_file_path = self._encrypt_key_file_selector.get_path()
        clean_original = self._encrypt_clean_original.isChecked()
        
        # Show progress
        self._encrypt_progress.setVisible(True)
        self._encrypt_progress.setValue(0)
        
        # Start encryption
        self._encrypt_controller.encrypt_file(
            file_path,
            password,
            key_file_path,
            clean_original
        )
        
    def _on_decrypt_clicked(self):
        """Handle decrypt button click."""
        file_path = self._decrypt_file_selector.get_path()
        if not file_path:
            self._show_error("Validation Error", "Please select an encrypted file.")
            return
            
        password = self._decrypt_password.get_password()
        if not password:
            self._show_error("Validation Error", "Please enter a password.")
            return
            
        key_file_path = self._decrypt_key_file_selector.get_path()
        
        # Show progress
        self._decrypt_progress.setVisible(True)
        self._decrypt_progress.setValue(0)
        
        # Start decryption
        self._decrypt_controller.decrypt_file(
            file_path,
            password,
            key_file_path
        )
        
    def _on_clean_clicked(self):
        """Handle clean button click."""
        file_path = self._clean_file_selector.get_path()
        if not file_path:
            self._show_error("Validation Error", "Please select a file to clean.")
            return
            
        # Confirm action
        reply = QMessageBox.question(
            self,
            "Confirm Cleaning",
            "Are you sure you want to securely clean this file?\n\n"
            "This will permanently overwrite the file content and cannot be undone!",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            delete = self._clean_delete.isChecked()
            
            # Show progress
            self._clean_progress.setVisible(True)
            self._clean_progress.setValue(0)
            
            # Start cleaning
            self._clean_controller.clean_file(file_path, delete)
            
    def _on_generate_key_clicked(self):
        """Handle generate key button click."""
        key_file_path = self._key_file_selector.get_path()
        if not key_file_path:
            self._show_error("Validation Error", "Please select a location to save the key file.")
            return
            
        if key_file_path.exists():
            reply = QMessageBox.question(
                self,
                "File Exists",
                f"The file {key_file_path} already exists. Overwrite?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply != QMessageBox.Yes:
                return
                
        # Show progress
        self._key_progress.setVisible(True)
        self._key_progress.setValue(0)
        
        # Start key generation
        self._key_controller.generate_key_file(key_file_path)
        
    def _update_progress(self, operation: str, value: int):
        """Update progress bar for an operation."""
        if operation == "encrypt":
            self._encrypt_progress.setValue(value)
        elif operation == "decrypt":
            self._decrypt_progress.setValue(value)
        elif operation == "clean":
            self._clean_progress.setValue(value)
        elif operation == "key":
            self._key_progress.setValue(value)
            
    def _on_encrypt_completed(self, result: EncryptionResult):
        """Handle encryption completion."""
        self._encrypt_progress.setVisible(False)
        
        if result.success:
            QMessageBox.information(
                self,
                "Encryption Successful",
                f"File encrypted successfully!\n\nOutput: {result.output_path}\n"
                f"File size: {result.file_size:,} bytes"
            )
            # Clear form
            self._encrypt_file_selector.clear()
            self._encrypt_password.clear()
            self._encrypt_key_file_selector.clear()
        else:
            QMessageBox.critical(
                self,
                "Encryption Failed",
                f"Encryption failed:\n{result.error}"
            )
            
    def _on_decrypt_completed(self, result: EncryptionResult):
        """Handle decryption completion."""
        self._decrypt_progress.setVisible(False)
        
        if result.success:
            QMessageBox.information(
                self,
                "Decryption Successful",
                f"File decrypted successfully!\n\nOutput: {result.output_path}\n"
                f"File size: {result.file_size:,} bytes"
            )
            # Clear form
            self._decrypt_file_selector.clear()
            self._decrypt_password.clear()
            self._decrypt_key_file_selector.clear()
        else:
            QMessageBox.critical(
                self,
                "Decryption Failed",
                f"Decryption failed:\n{result.error}"
            )
            
    def _on_clean_completed(self, success: bool, message: str):
        """Handle cleaning completion."""
        self._clean_progress.setVisible(False)
        
        if success:
            QMessageBox.information(self, "Cleaning Successful", message)
            # Clear form
            self._clean_file_selector.clear()
        else:
            QMessageBox.critical(self, "Cleaning Failed", message)
            
    def _on_key_completed(self, success: bool, message: str):
        """Handle key generation completion."""
        self._key_progress.setVisible(False)
        
        if success:
            QMessageBox.information(
                self,
                "Key Generation Successful",
                f"{message}\n\n⚠ Keep this key file secure!"
            )
            # Clear form
            self._key_file_selector.clear()
        else:
            QMessageBox.critical(self, "Key Generation Failed", message)
            
    def _show_error(self, title: str, message: str):
        """Show error message."""
        QMessageBox.critical(self, title, message)

