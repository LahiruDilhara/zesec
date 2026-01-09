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

### 🔐 Encryption & Decryption
- **AES-256-GCM encryption** - Industry-standard encryption algorithm
- **Password-based encryption** - Secure key derivation using PBKDF2
- **Optional key file support** - Enhanced security with key file + password combination
- **Automatic file extension** - Encrypted files use `.zesec` extension
- **Secure original file deletion** - Optionally clean original files after encryption

### 🧹 Secure File Cleaning
- **Multi-pass overwriting** - Securely overwrite files before deletion
- **Forensic-grade deletion** - Makes file recovery extremely difficult
- **Directory cleaning** - Clean entire directories recursively
- **Configurable passes** - Customize the number of overwrite passes

### 💻 Dual Interface
- **Graphical User Interface (GUI)** - Modern PySide6-based interface with tabbed layout
- **Command-Line Interface (CLI)** - Interactive console with command autocomplete
- **Unified functionality** - Same features available in both interfaces

### 🎯 Additional Features
- **Key file generation** - Generate secure random encryption keys
- **Progress tracking** - Real-time progress indicators for long operations
- **Error handling** - Comprehensive error messages and validation
- **Cross-platform** - Works on Windows, macOS, and Linux

## 📋 Requirements

- Python 3.8 or higher
- PySide6 (for GUI mode)
- cryptography
- Other dependencies listed in `requirements.txt`

## 🔧 Installation

### From Source

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

## 🎮 Usage

### GUI Mode

Launch the graphical user interface:

```bash
python3 main.py --gui
```

The GUI provides a tabbed interface with:
- **Encryption Tab** - Encrypt files with password and optional key file
- **Decryption Tab** - Decrypt encrypted files
- **Cleaning Tab** - Securely clean files
- **Key Management Tab** - Generate encryption key files

### Console Mode

Launch the interactive console:

```bash
python3 main.py
```

#### Available Commands

**File Operations:**
- `ls [path]` - List files and directories
- `cat <file>` - Display file contents
- `pwd` - Print current working directory
- `cd [path]` - Change directory

**Encryption:**
- `encrypt <file> [options]` - Encrypt a file
  - Options:
    - `--key-file <path>` - Use a key file in addition to password
    - `--no-clean` - Don't securely clean original file after encryption
- `decrypt <file> [options]` - Decrypt a file
  - Options:
    - `--key-file <path>` - Key file path (required if used during encryption)
- `generate-key <path>` - Generate encryption key file

**Cleaning:**
- `clean <file> [options]` - Securely clean a file
  - Options:
    - `--no-delete` - Overwrite file but don't delete it
- `clean-dir <dir> [options]` - Securely clean directory
  - Options:
    - `--no-delete` - Overwrite files but don't delete them

**System:**
- `help` - Show help message
- `help <command>` - Show detailed help for a command
- `exit` or `quit` - Exit the application
- `clear` - Clear the screen

#### Example Usage

```bash
# Encrypt a file
zesec> encrypt document.txt
Enter password: ********
✓ Encrypted successfully: document.txt.zesec

# Decrypt a file
zesec> decrypt document.txt.zesec
Enter password: ********
✓ Decrypted successfully: document.txt

# Encrypt with key file
zesec> encrypt document.txt --key-file mykey.key
Enter password: ********
✓ Encrypted successfully: document.txt.zesec

# Generate a key file
zesec> generate-key mykey.key
✓ Key file generated successfully: mykey.key

# Securely clean a file
zesec> clean sensitive_file.txt
Securely clean sensitive_file.txt? [y/N]: y
✓ Cleaning completed successfully
```

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

