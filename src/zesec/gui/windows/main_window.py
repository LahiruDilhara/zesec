"""Main window for Zesec GUI application."""

from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFileDialog, QMessageBox,
    QTabWidget, QCheckBox, QProgressBar, QGroupBox,
    QFormLayout, QLineEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QShortcut, QKeySequence, QIcon

from ...utils.asset_utils import get_asset_path

from ...di.container import ApplicationContainer
from ...core.models.encryption_result import EncryptionResult
from ..controllers.encrypt_controller import EncryptController
from ..controllers.decrypt_controller import DecryptController
from ..controllers.clean_controller import CleanController
from ..controllers.key_controller import KeyController
from ..widgets.file_selector import FileSelectorWidget
from ..widgets.multi_file_selector import MultiFileSelectorWidget
from ..widgets.password_input import PasswordInputWidget
from ..widgets.hover_button import HoverButton
from ..widgets.batch_progress import BatchProgressWidget


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
        
        # State for batch processing
        self._encryption_queue = []
        self._encryption_results = []
        self._decryption_queue = []
        self._decryption_results = []
        
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
        self.resize(900, 800)
        
        # Set Window Icon
        icon_path = get_asset_path("icon/icon.png")
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        self.setMinimumSize(700, 750)
        
        # Ctrl+W shortcut to close
        self._close_shortcut = QShortcut(QKeySequence("Ctrl+W"), self)
        self._close_shortcut.activated.connect(self.close)
        
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
        self._encrypt_file_selector = MultiFileSelectorWidget()
        file_layout.addWidget(self._encrypt_file_selector)
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)  # Stretch factor 1 allows it to expand
        
        # Password input
        self._encrypt_password = PasswordInputWidget(label="Password:")
        layout.addWidget(self._encrypt_password)
        
        self._encrypt_password_confirm = PasswordInputWidget(label="Confirm Password:", is_confirm=True)
        self._encrypt_password_confirm.set_match_target(self._encrypt_password)
        layout.addWidget(self._encrypt_password_confirm)
        
        # Destination Directory
        dest_group = QGroupBox("Destination Directory")
        dest_layout = QVBoxLayout()
        self._encrypt_dest_selector = FileSelectorWidget(is_directory=True)
        dest_layout.addWidget(self._encrypt_dest_selector)
        dest_group.setLayout(dest_layout)
        layout.addWidget(dest_group)
        
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
        self._encrypt_clean_original.setCursor(Qt.PointingHandCursor)
        self._encrypt_clean_original.setChecked(True)
        options_layout.addWidget(self._encrypt_clean_original)
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Progress bar
        self._encrypt_progress = BatchProgressWidget()
        layout.addWidget(self._encrypt_progress)
        
        # Encrypt button
        self._encrypt_btn = HoverButton("Encrypt File")
        self._encrypt_btn.clicked.connect(self._on_encrypt_clicked)
        self._encrypt_btn.setEnabled(False)
        layout.addWidget(self._encrypt_btn)
        
        # Connect signals for dynamic button state
        self._encrypt_file_selector.paths_changed.connect(lambda _: self._update_encrypt_btn_state())
        self._encrypt_file_selector.cancel_clicked.connect(self._on_encrypt_cancel)
        self._encrypt_password.text_changed.connect(lambda _: self._update_encrypt_btn_state())
        self._encrypt_password_confirm.text_changed.connect(lambda _: self._update_encrypt_btn_state())
        self._encrypt_dest_selector.path_changed.connect(lambda _: self._update_encrypt_btn_state())
        self._encrypt_key_file_selector.path_changed.connect(lambda _: self._update_encrypt_btn_state())
        
        layout.addStretch()
        from PySide6.QtWidgets import QScrollArea
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setWidget(widget)
        return scroll
        
    def _create_decrypt_tab(self) -> QWidget:
        """Create decryption tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        
        # File selection group
        file_group = QGroupBox("Encrypted File Selection")
        file_layout = QVBoxLayout()
        self._decrypt_file_selector = MultiFileSelectorWidget(file_filter="Encrypted Files (*.zesec);;All Files (*)")
        file_layout.addWidget(self._decrypt_file_selector)
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)  # Stretch factor 1 allows it to expand
        
        # Password input
        self._decrypt_password = PasswordInputWidget(label="Password:")
        layout.addWidget(self._decrypt_password)
        
        # Destination Directory
        dest_group = QGroupBox("Destination Directory")
        dest_layout = QVBoxLayout()
        self._decrypt_dest_selector = FileSelectorWidget(is_directory=True)
        dest_layout.addWidget(self._decrypt_dest_selector)
        dest_group.setLayout(dest_layout)
        layout.addWidget(dest_group)
        
        # Key file selection (optional)
        key_group = QGroupBox("Key File (If used during encryption)")
        key_layout = QVBoxLayout()
        self._decrypt_key_file_selector = FileSelectorWidget(file_filter="Key Files (*.key);;All Files (*)")
        key_layout.addWidget(self._decrypt_key_file_selector)
        key_group.setLayout(key_layout)
        layout.addWidget(key_group)
        # Options
        options_group = QGroupBox("Options")
        options_layout = QVBoxLayout()
        self._decrypt_clean_original = QCheckBox("Securely delete original encrypted file after decryption")
        self._decrypt_clean_original.setCursor(Qt.PointingHandCursor)
        self._decrypt_clean_original.setChecked(False)
        options_layout.addWidget(self._decrypt_clean_original)
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Progress bar
        self._decrypt_progress = BatchProgressWidget()
        layout.addWidget(self._decrypt_progress)
        
        # Decrypt button
        self._decrypt_btn = HoverButton("Decrypt File")
        self._decrypt_btn.clicked.connect(self._on_decrypt_clicked)
        self._decrypt_btn.setEnabled(False)
        layout.addWidget(self._decrypt_btn)
        
        # Connect signals
        self._decrypt_file_selector.paths_changed.connect(lambda _: self._update_decrypt_btn_state())
        self._decrypt_file_selector.cancel_clicked.connect(self._on_decrypt_cancel)
        self._decrypt_password.text_changed.connect(lambda _: self._update_decrypt_btn_state())
        self._decrypt_dest_selector.path_changed.connect(lambda _: self._update_decrypt_btn_state())
        self._decrypt_key_file_selector.path_changed.connect(lambda _: self._update_decrypt_btn_state())
        
        layout.addStretch()
        from PySide6.QtWidgets import QScrollArea
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setWidget(widget)
        return scroll
        
    def _create_clean_tab(self) -> QWidget:
        """Create cleaning tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        
        # File selection group
        file_group = QGroupBox("File Selection")
        file_layout = QVBoxLayout()
        self._clean_file_selector = MultiFileSelectorWidget()
        file_layout.addWidget(self._clean_file_selector)
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)
        
        # Options
        options_group = QGroupBox("Options")
        options_layout = QVBoxLayout()
        self._clean_delete = QCheckBox("Delete file after cleaning")
        self._clean_delete.setCursor(Qt.PointingHandCursor)
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
        self._clean_progress = BatchProgressWidget()
        layout.addWidget(self._clean_progress)
        
        # Clean button
        self._clean_btn = HoverButton("Clean File")
        self._clean_btn.clicked.connect(self._on_clean_clicked)
        self._clean_btn.setEnabled(False)
        layout.addWidget(self._clean_btn)
        
        # Connect signals
        self._clean_file_selector.paths_changed.connect(lambda _: self._update_clean_btn_state())
        self._clean_file_selector.cancel_clicked.connect(self._on_clean_cancel)
        
        layout.addStretch()
        
        from PySide6.QtWidgets import QScrollArea
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setWidget(widget)
        return scroll
        
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
        
        # Directory selector
        self._key_dir_selector = FileSelectorWidget(is_directory=True)
        key_layout.addWidget(self._key_dir_selector)
        
        # File name input
        name_layout = QHBoxLayout()
        self._key_name_edit = QLineEdit()
        self._key_name_edit.setPlaceholderText("Enter key name...")
        name_layout.addWidget(self._key_name_edit)
        name_layout.addWidget(QLabel(".key"))
        key_layout.addLayout(name_layout)
        
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
        self._generate_btn = HoverButton("Generate Key File")
        self._generate_btn.clicked.connect(self._on_generate_key_clicked)
        self._generate_btn.setEnabled(False)
        layout.addWidget(self._generate_btn)
        
        # Connect signals
        self._key_dir_selector.path_changed.connect(lambda _: self._update_key_btn_state())
        self._key_name_edit.textChanged.connect(lambda _: self._update_key_btn_state())
        
        layout.addStretch()
        
        from PySide6.QtWidgets import QScrollArea
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setWidget(widget)
        return scroll
        
    # Removed _browse_key_file_save since we use directory selector
            
    def _on_encrypt_cancel(self):
        """Handle encryption cancellation."""
        if self._encryption_queue:
            self._encryption_queue.clear()
            QMessageBox.warning(self, "Cancelled", "Batch encryption cancelled! The currently processing file will finish, but no further files will be encrypted.")

    def _on_decrypt_cancel(self):
        """Handle decryption cancellation."""
        if self._decryption_queue:
            self._decryption_queue.clear()
            QMessageBox.warning(self, "Cancelled", "Batch decryption cancelled! The currently processing file will finish, but no further files will be decrypted.")

    def _on_clean_cancel(self):
        """Handle cleaning cancellation."""
        if self._cleaning_queue:
            self._cleaning_queue.clear()
            QMessageBox.warning(self, "Cancelled", "Batch cleaning cancelled! The currently processing file will finish, but no further files will be cleaned.")
            
    def _on_encrypt_clicked(self):
        """Handle encrypt button click."""
        paths = self._encrypt_file_selector.get_paths()
        if not paths:
            self._show_error("Validation Error", "Please select at least one file to encrypt.")
            return
            
        password = self._encrypt_password.get_password()
        if not password:
            self._show_error("Validation Error", "Please enter a password.")
            return
            
        password_confirm = self._encrypt_password_confirm.get_password()
        if password != password_confirm:
            self._show_error("Validation Error", "Passwords do not match.")
            return
            
        # Disable button to prevent concurrent runs
        self._encrypt_btn.setEnabled(False)
        self._encrypt_file_selector.set_processing(True)
        self._encrypt_progress.reset(len(paths))
        
        self._encryption_queue = paths.copy()
        self._encryption_results = []
        self._process_next_encryption()
        
    def _process_next_encryption(self):
        """Process the next file in the encryption queue."""
        if not self._encryption_queue:
            successes = [r for p, r in self._encryption_results if r.success]
            failures = [r for p, r in self._encryption_results if not r.success]
            failed_paths = [p for p, r in self._encryption_results if not r.success]
            
            msg = f"Batch encryption finished.\n\nSuccessfully encrypted: {len(successes)}\nFailed: {len(failures)}"
            if failures:
                msg += "\n\nFirst error:\n" + failures[0].error
                
            QMessageBox.information(self, "Batch Encryption", msg)
            
            # Update form
            if failures:
                self._encrypt_file_selector.retain_failed_files(failed_paths)
            else:
                self._encrypt_file_selector.clear()
                
            self._encrypt_file_selector.set_processing(False)
            self._encrypt_password.clear()
            self._encrypt_password_confirm.clear()
            self._encrypt_key_file_selector.clear()
            self._encrypt_dest_selector.clear()
            self._update_encrypt_btn_state()
            return
            
        next_file = self._encryption_queue.pop(0)
        self._current_encrypt_file = next_file
        
        password = self._encrypt_password.get_password()
        key_file_path = self._encrypt_key_file_selector.get_path()
        clean_original = self._encrypt_clean_original.isChecked()
        dest_dir = self._encrypt_dest_selector.get_path()
        output_path = dest_dir / f"{next_file.name}.zesec" if dest_dir else None
        
        self._encrypt_controller.encrypt_file(
            next_file,
            password,
            output_path,
            key_file_path,
            clean_original
        )
        
    def _on_decrypt_clicked(self):
        """Handle decrypt button click."""
        paths = self._decrypt_file_selector.get_paths()
        if not paths:
            self._show_error("Validation Error", "Please select at least one encrypted file.")
            return
            
        password = self._decrypt_password.get_password()
        if not password:
            self._show_error("Validation Error", "Please enter a password.")
            return
            
        # Disable button
        self._decrypt_btn.setEnabled(False)
        self._decrypt_file_selector.set_processing(True)
        self._decrypt_progress.reset(len(paths))
        
        self._decryption_queue = paths.copy()
        self._decryption_results = []
        self._process_next_decryption()
        
    def _process_next_decryption(self):
        """Process the next file in the decryption queue."""
        if not self._decryption_queue:
            successes = [r for p, r in self._decryption_results if r.success]
            failures = [r for p, r in self._decryption_results if not r.success]
            failed_paths = [p for p, r in self._decryption_results if not r.success]
            
            msg = f"Batch decryption finished.\n\nSuccessfully decrypted: {len(successes)}\nFailed: {len(failures)}"
            if failures:
                msg += "\n\nFirst error:\n" + failures[0].error
                
            QMessageBox.information(self, "Batch Decryption", msg)
            
            # Update form
            if failures:
                self._decrypt_file_selector.retain_failed_files(failed_paths)
            else:
                self._decrypt_file_selector.clear()
                
            self._decrypt_file_selector.set_processing(False)
            self._decrypt_password.clear()
            self._decrypt_key_file_selector.clear()
            self._decrypt_dest_selector.clear()
            self._update_decrypt_btn_state()
            return
            
        next_file = self._decryption_queue.pop(0)
        self._current_decrypt_file = next_file
        
        password = self._decrypt_password.get_password()
        key_file_path = self._decrypt_key_file_selector.get_path()
        dest_dir = self._decrypt_dest_selector.get_path()
        clean_original = self._decrypt_clean_original.isChecked()
        
        orig_name = next_file.name
        if orig_name.endswith('.zesec'):
            orig_name = orig_name[:-6]
        output_path = dest_dir / orig_name if dest_dir else None
        
        self._decrypt_controller.decrypt_file(
            next_file,
            password,
            output_path,
            key_file_path,
            clean_original
        )
        
    def _on_clean_clicked(self):
        """Handle clean button click."""
        paths = self._clean_file_selector.get_paths()
        if not paths:
            self._show_error("Validation Error", "Please select at least one file to clean.")
            return
            
        # Confirm action
        reply = QMessageBox.question(
            self,
            "Confirm Cleaning",
            f"Are you sure you want to securely clean {len(paths)} file(s)?\n\n"
            "This will permanently overwrite the file content and cannot be undone!",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Disable button
            self._clean_btn.setEnabled(False)
            self._clean_file_selector.set_processing(True)
            self._clean_progress.reset(len(paths))
            
            self._cleaning_queue = paths.copy()
            self._cleaning_results = []
            self._process_next_cleaning()
            
    def _process_next_cleaning(self):
        """Process the next file in the cleaning queue."""
        if not self._cleaning_queue:
            successes = [m for p, s, m in self._cleaning_results if s]
            failures = [m for p, s, m in self._cleaning_results if not s]
            failed_paths = [p for p, s, m in self._cleaning_results if not s]
            
            msg = f"Batch cleaning finished.\n\nSuccessfully cleaned: {len(successes)}\nFailed: {len(failures)}"
            if failures:
                msg += "\n\nFirst error:\n" + failures[0]
                
            QMessageBox.information(self, "Batch Cleaning", msg)
            
            # Update form
            if failures:
                self._clean_file_selector.retain_failed_files(failed_paths)
            else:
                self._clean_file_selector.clear()
                
            self._clean_file_selector.set_processing(False)
            self._update_clean_btn_state()
            return
            
        next_file = self._cleaning_queue.pop(0)
        self._current_clean_file = next_file
        
        delete = self._clean_delete.isChecked()
        self._clean_controller.clean_file(next_file, delete)
            
    def _on_generate_key_clicked(self):
        """Handle generate key button click."""
        dir_path = self._key_dir_selector.get_path()
        name = self._key_name_edit.text().strip()
        
        if not dir_path or not name:
            self._show_error("Validation Error", "Please specify location and file name.")
            return
            
        key_file_path = dir_path / f"{name}.key"
            
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
            if hasattr(self, '_current_encrypt_file'):
                self._encrypt_file_selector.update_file_progress(self._current_encrypt_file, value)
            
            # Calculate total progress
            total_files = len(self._encryption_results) + len(self._encryption_queue) + 1
            if total_files > 0:
                completed_files = len(self._encryption_results)
                self._encrypt_progress.update_progress(completed_files, total_files, value)
                
        elif operation == "decrypt":
            if hasattr(self, '_current_decrypt_file'):
                self._decrypt_file_selector.update_file_progress(self._current_decrypt_file, value)
                
            # Calculate total progress
            total_files = len(self._decryption_results) + len(self._decryption_queue) + 1
            if total_files > 0:
                completed_files = len(self._decryption_results)
                self._decrypt_progress.update_progress(completed_files, total_files, value)
                
        elif operation == "clean":
            if hasattr(self, '_current_clean_file'):
                self._clean_file_selector.update_file_progress(self._current_clean_file, value)
                
            # Calculate total progress
            total_files = len(self._cleaning_results) + len(self._cleaning_queue) + 1
            if total_files > 0:
                completed_files = len(self._cleaning_results)
                self._clean_progress.update_progress(completed_files, total_files, value)
        elif operation == "key":
            self._key_progress.setValue(value)
            
    def _on_encrypt_completed(self, result: EncryptionResult):
        """Handle encryption completion."""
        if not result.success:
            self._encrypt_file_selector.mark_file_failed(self._current_encrypt_file)
        self._encryption_results.append((self._current_encrypt_file, result))
        self._process_next_encryption()
            
    def _on_decrypt_completed(self, result: EncryptionResult):
        """Handle decryption completion."""
        if not result.success:
            self._decrypt_file_selector.mark_file_failed(self._current_decrypt_file)
        self._decryption_results.append((self._current_decrypt_file, result))
        self._process_next_decryption()
            
    def _on_clean_completed(self, success: bool, message: str):
        """Handle cleaning completion."""
        if not hasattr(self, '_cleaning_results'):
            self._cleaning_results = []
        if not success:
            self._clean_file_selector.mark_file_failed(self._current_clean_file)
        self._cleaning_results.append((self._current_clean_file, success, message))
        self._process_next_cleaning()
            
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
            self._key_dir_selector.clear()
            self._key_name_edit.clear()
        else:
            QMessageBox.critical(self, "Key Generation Failed", message)
            
    def _show_error(self, title: str, message: str):
        """Show error message."""
        QMessageBox.critical(self, title, message)

    def _update_encrypt_btn_state(self):
        """Update encrypt button state based on fields."""
        paths = self._encrypt_file_selector.get_paths()
        has_file = len(paths) > 0
        has_dest = bool(self._encrypt_dest_selector.get_path())
        has_pw = bool(self._encrypt_password.get_password() and self._encrypt_password.get_password() == self._encrypt_password_confirm.get_password())
        has_key = bool(self._encrypt_key_file_selector.get_path())
        self._encrypt_btn.setEnabled(has_file and has_dest and (has_pw or has_key))
        self._encrypt_progress.set_total(len(paths))
        
    def _update_decrypt_btn_state(self):
        """Update decrypt button state based on fields."""
        paths = self._decrypt_file_selector.get_paths()
        has_file = len(paths) > 0
        has_dest = bool(self._decrypt_dest_selector.get_path())
        has_pw = bool(self._decrypt_password.get_password())
        has_key = bool(self._decrypt_key_file_selector.get_path())
        self._decrypt_btn.setEnabled(has_file and has_dest and (has_pw or has_key))
        self._decrypt_progress.set_total(len(paths))
        
    def _update_clean_btn_state(self):
        """Update clean button state based on fields."""
        paths = self._clean_file_selector.get_paths()
        has_file = len(paths) > 0
        self._clean_btn.setEnabled(has_file)
        self._clean_progress.set_total(len(paths))
        
    def _update_key_btn_state(self):
        """Update generate key button state based on fields."""
        has_dir = bool(self._key_dir_selector.get_path())
        has_name = bool(self._key_name_edit.text().strip())
        self._generate_btn.setEnabled(has_dir and has_name)

