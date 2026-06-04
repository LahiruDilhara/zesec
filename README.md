# Zesec

<div align="center">

**Zesec - Secure File Encryption and Cleaning Tool**

A modern, cross-platform application for secure file encryption, decryption, and secure file deletion.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

</div>

---

## 🚀 Features

### 🔐 Encryption & Decryption (Batch Processing Supported)
- **AES-256-GCM encryption** - Industry-standard encryption algorithm
- **Password-based encryption** - Secure key derivation using PBKDF2
- **Optional key file support** - Enhanced security with key file + password combination
- **Automatic file extension** - Encrypted files use `.zesec` extension
- **Custom File Type Association** - Native OS file associations for `.zesec` files
- **Secure original file deletion** - Optionally clean original files after encryption
- **Batch Processing** - Encrypt or decrypt hundreds of files at once flawlessly in both GUI and CLI without freezes

### 🧹 Deep Cleaning
- **Multi-pass overwriting** - Securely overwrite sensitive files with zero-byte buffers before deletion, ensuring files are deeply cleaned and never exist for recovery
- **Forensic-grade deletion** - Removes recovery options completely, making file recovery virtually impossible
- **Directory cleaning** - Clean entire directories recursively
- **Batch Cleaning** - Process multiple files or folders simultaneously

### 💻 Dual Interface
- **Graphical User Interface (GUI)** - Modern PySide6-based interface with tabbed layout, custom lists, and batch progress tracking
- **Command-Line Interface (CLI)** - Interactive console with smart path and command autocomplete (`prompt_toolkit`) and unified `tqdm` progress bars
- **Unified functionality** - Same features available natively across both interfaces

### 🎯 Additional Features
- **Key file generation** - Generate secure random encryption keys
- **Process Cancellation** - Real-time progress tracking with safe interruption capabilities
- **Cross-platform** - Works and natively compiles on Windows, macOS, and Linux

## 📋 Requirements

- Python 3.8 or higher
- PySide6 (for GUI mode)
- cryptography
- Other dependencies listed in `requirements.txt`

## 🔧 Installation

### 📦 Pre-compiled Installers (Recommended)
Zesec provides native, ready-to-use installers for all major operating systems. You can download the latest release directly from the GitHub Releases page.

- **Windows:** Download the `.msi` (Windows Installer) or `.exe` setup file.
- **Linux:** Download the `.deb` (Debian/Ubuntu) or `.rpm` (Fedora/RHEL/CentOS) packages.
- **macOS:** Download the `.dmg` or `.app` bundle.

*(Installing via these packages automatically configures your system paths and native OS file associations for `.zesec` files!)*

### 🛠️ From Source

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/zesec.git
   cd zesec
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 Usage Journey

Zesec is designed to adapt to your workflow, whether you prefer a polished visual interface or a rapid, robust command-line experience.

### 🎨 The Visual Experience (GUI)

Launch the graphical user interface via your terminal, or simply double-click the compiled application executable. Thanks to our **Native OS File Associations**, you can even double-click any `.zesec` file directly from your file manager to instantly launch the decryption flow!

![File Type Integration](docs/images/zesec-encryption-custom-file-type.png)

#### Securing Your Files
Imagine you have a directory filled with sensitive financial records. You open the **Encryption** tab and drag-and-drop hundreds of files at once into the multi-file selector. Zesec intelligently validates your destinations and strictly enforces password confirmation to prevent accidental lockouts.

![Encryption Interface](docs/images/zesec-gui-encryption-start.png)

As you initiate the encryption, you aren't left in the dark. Zesec smoothly processes the batch, providing real-time visual progress indicators for every single file alongside a global progress bar. Need to abort? The process cancellation feature lets you safely halt operations without corrupting data.

![Encryption Ongoing](docs/images/zesec-gui-encryption-ongoing.png)

#### Retrieving Your Data
When it's time to access your files, the **Decryption** tab offers the exact same robust batch processing. Once finished, a satisfying completion screen summarizes the successful decryptions, letting you get right back to work.

![Decryption Start](docs/images/zesec-gui-decryption-start.png)
![Decryption Complete](docs/images/zesec-gui-decryption-complete.png)

#### Erasing Traces Forever (Deep Cleaning)
Simply deleting a file or moving it to the trash bin leaves the raw data sitting on your hard drive, completely vulnerable to basic data recovery tools. The **Deep Cleaning** tab is built for forensic-grade data destruction. When you initiate a deep clean, Zesec doesn't just delete the file pointer. It actively opens the file and aggressively overwrites the underlying physical disk sectors with multi-pass zero-byte buffers.

![Deep Cleaning Start](docs/images/zesec-gui-deep-cleaning-start.png)

Whether you are wiping a single password document or recursively destroying an entire directory of financial logs, you can watch Zesec securely erase each file one by one. Once the process is complete, the original data is permanently shredded. You have the absolute guarantee that the sensitive information has been eradicated and forensic data recovery is mathematically impossible.

![Deep Cleaning Ongoing](docs/images/zesec-gui-deep-cleaning-ongoing.png)
![Deep Cleaning Complete](docs/images/zesec-gui-deep-cleaning-complete.png)

#### Key Management & Multi-Factor Security
A strong password is great, but relying solely on human memory can sometimes be a vulnerability. For advanced users requiring an enterprise-grade layer of security, Zesec features a dedicated **Key Management** system. This allows you to generate highly secure, cryptographically random key files (`.key`).

When encrypting a file, you can choose to use a Key File *in addition* to your standard text password. This effectively creates a multi-factor encryption lock: an attacker would not only need to guess your secret password, but they would also need to possess the physical key file (which you can store on an external USB drive) to ever decrypt the data.

![Key Management](docs/images/zesec-gui-key-management.png)

---

### 💻 The Power User Experience (CLI)

For those who live in the terminal, Zesec offers a completely unified experience without sacrificing a single feature. Launch the interactive console by simply running `zesec` or `python3 main.py`.

Immediately, you're greeted by a smart, interactive shell powered by `prompt_toolkit`. It intuitively autocompletes commands, and the moment you press space, it transitions into system path autocompletion—drastically speeding up your workflow.

![CLI Interactive Terminal](docs/images/zesec-cli-help-and-interactive-terminal.png)

#### Massive Batch Operations
When you issue a command like `encrypt folder/* -d safe_vault/`, the console springs to life. Instead of cluttering your terminal with hundreds of lines, Zesec groups the entire batch into a unified, perfectly smooth `tqdm` progress bar. 

![CLI Encryption Ongoing](docs/images/zesec-cli-encryption-ongoing.png)

Upon finishing, it provides a clean, silent summary of exactly how many files were successfully encrypted.

![CLI Encryption Complete](docs/images/zesec-cli-encryption-complete.png)

The same unified elegance applies to **Decryption**, restoring your files efficiently and cleanly.

![CLI Decryption Complete](docs/images/zesec-cli-decryption-complete.png)

#### Forensic Cleaning from the Terminal
Need to securely wipe a sensitive server directory? The `clean` command operates identically to the GUI, executing multi-pass overwrites across the entire batch while visualizing the overarching progress.

![CLI Deep Cleaning](docs/images/zesec-cli-deep-cleaning-ongoing.png)

#### Available Commands

**File Operations:**
- `ls [path]` - List files and directories
- `cat <file>` - Display file contents
- `pwd` - Print current working directory
- `cd [path]` - Change directory

**Encryption:**
- `encrypt <file1> [file2...] -d <dir> [options]` - Encrypt files
  - Options:
    - `--key-file <path>` - Use a key file in addition to password
    - `--no-clean` - Don't securely clean original file after encryption
- `decrypt <file1> [file2...] -d <dir> [options]` - Decrypt files
  - Options:
    - `--key-file <path>` - Key file path (required if used during encryption)
    - `--clean` - Securely delete original encrypted file after decryption
- `generate-key <path>` - Generate encryption key file

**Cleaning:**
- `clean <file1> [file2...] [options]` - Securely deep clean files
  - Options:
    - `--no-delete` - Overwrite file but don't delete it
- `clean-dir <dir> [options]` - Securely deep clean directory
  - Options:
    - `--no-delete` - Overwrite files but don't delete them

**System:**
- `help` - Show help message
- `help <command>` - Show detailed help for a command
- `exit` or `quit` - Exit the application
- `clear` - Clear the screen

## 🏗️ Architecture

Zesec follows a clean architecture pattern with clear separation of concerns:

### Project Structure

```
zesec/
├── src/zesec/
│   ├── core/              # Business logic (Model)
│   │   ├── encryption/    # Encryption services
│   │   └── file_operations/ # File handling and cleaning
│   ├── interfaces/        # Protocol definitions
│   ├── di/                # Dependency injection container
│   ├── config/            # Configuration and settings
│   ├── console/           # CLI interface
│   │   └── commands/      # Command implementations
│   ├── gui/               # GUI interface (MVP pattern)
│   │   ├── windows/       # Views
│   │   ├── controllers/   # Presenters
│   │   ├── workers/       # Background threads
│   │   └── widgets/       # Reusable UI components
│   └── utils/             # Utilities and helpers
├── tests/                 # Test suite
├── docs/                  # Documentation
└── main.py               # Application entry point
```

### Design Patterns

- **MVP (Model-View-Presenter)** - GUI architecture
- **Dependency Injection** - Loose coupling and testability
- **Command Pattern** - Console command handling
- **Service Layer** - Business logic encapsulation

## 🔒 Security

- **Encryption Algorithm**: AES-256-GCM (Galois/Counter Mode)
- **Key Derivation**: PBKDF2 with 100,000 iterations (SHA-256)
- **Key Size**: 256 bits (32 bytes)
- **Nonce**: 12 bytes (random per encryption)
- **Salt**: 16 bytes (random per encryption)
- **Authentication**: Built-in GCM authentication tag

### Security Best Practices

1. **Strong Passwords**: Use long, complex passwords for encryption
2. **Key File Security**: Store key files in secure locations
3. **File Cleaning**: Use secure cleaning before deleting sensitive files
4. **Key File Backup**: Keep secure backups of key files

## 🧪 Testing

Run the test suite:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=src/zesec --cov-report=html
```

## 📝 Configuration

Zesec can be configured via environment variables or a `.env` file:

```env
# Encryption settings
ENCRYPTION_ALGORITHM=AES-256-GCM
KEY_DERIVATION_ITERATIONS=100000
KEY_SIZE=32
NONCE_SIZE=12

# File operations
CLEAN_PASSES=3
BUFFER_SIZE=1048576

# Logging
LOG_LEVEL=INFO
LOG_FILE=zesec.log
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

1. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Install pre-commit hooks (optional):
   ```bash
   pre-commit install
   ```

3. Run linting:
   ```bash
   flake8 src/
   black src/
   mypy src/
   ```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [PySide6](https://www.qt.io/qt-for-python) for the GUI
- Encryption powered by [cryptography](https://cryptography.io/)
- Console interface uses [Rich](https://github.com/Textualize/rich) and [prompt_toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit)

## ⚠️ Disclaimer

This software is provided "as is" without warranty of any kind. Use at your own risk. The authors are not responsible for any data loss or security breaches resulting from the use of this software.

## 📧 Contact

For questions, issues, or contributions, please open an issue on GitHub.

---

<div align="center">

**Made with ❤️ for secure file management**

[Report Bug](https://github.com/yourusername/zesec/issues) · [Request Feature](https://github.com/yourusername/zesec/issues) · [Documentation](docs/)

</div>

