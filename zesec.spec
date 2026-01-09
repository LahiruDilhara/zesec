# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Zesec application.
Builds both console and GUI executables.
"""

import sys
from pathlib import Path

block_cipher = None

# Get project root
project_root = Path(SPECPATH).parent
icon_path = project_root / "img" / "icon.png"

# Convert icon path based on platform
if sys.platform == 'win32':
    # Windows needs .ico format - PyInstaller will handle PNG if .ico not found
    icon_file = str(icon_path.with_suffix('.ico')) if (project_root / "img" / "icon.ico").exists() else str(icon_path)
elif sys.platform == 'darwin':
    # macOS needs .icns format - PyInstaller will handle PNG if .icns not found
    icon_file = str(icon_path.with_suffix('.icns')) if (project_root / "img" / "icon.icns").exists() else str(icon_path)
else:
    # Linux can use PNG directly
    icon_file = str(icon_path)

# Hidden imports needed by the application
hidden_imports = [
    'zesec',
    'zesec.console',
    'zesec.console.commands',
    'zesec.console.commands.base',
    'zesec.console.commands.encrypt_command',
    'zesec.console.commands.decrypt_command',
    'zesec.console.commands.clean_command',
    'zesec.console.commands.file_commands',
    'zesec.console.commands.generate_key_command',
    'zesec.console.commands.help_command',
    'zesec.console.commands.system_commands',
    'zesec.console.commands.loader',
    'zesec.gui',
    'zesec.gui.main',
    'zesec.gui.windows',
    'zesec.gui.windows.main_window',
    'zesec.gui.controllers',
    'zesec.gui.controllers.encrypt_controller',
    'zesec.gui.controllers.decrypt_controller',
    'zesec.gui.controllers.clean_controller',
    'zesec.gui.controllers.key_controller',
    'zesec.gui.workers',
    'zesec.gui.workers.encrypt_worker',
    'zesec.gui.workers.decrypt_worker',
    'zesec.gui.workers.clean_worker',
    'zesec.gui.workers.key_generation_worker',
    'zesec.gui.widgets',
    'zesec.gui.widgets.file_selector',
    'zesec.gui.widgets.password_input',
    'zesec.core',
    'zesec.core.encryption',
    'zesec.core.encryption.encryptor',
    'zesec.core.encryption.key_manager',
    'zesec.core.encryption.algorithms',
    'zesec.core.file_operations',
    'zesec.core.file_operations.cleaner',
    'zesec.core.file_operations.file_handler',
    'zesec.core.models',
    'zesec.core.models.encryption_result',
    'zesec.di',
    'zesec.di.container',
    'zesec.config',
    'zesec.config.settings',
    'zesec.interfaces',
    'zesec.utils',
    'cryptography',
    'cryptography.hazmat',
    'cryptography.hazmat.primitives',
    'cryptography.hazmat.primitives.ciphers',
    'cryptography.hazmat.primitives.ciphers.aead',
    'cryptography.hazmat.primitives.kdf',
    'cryptography.hazmat.primitives.kdf.pbkdf2',
    'cryptography.hazmat.primitives.kdf.hkdf',
    'PySide6',
    'PySide6.QtCore',
    'PySide6.QtWidgets',
    'PySide6.QtGui',
    'rich',
    'rich.console',
    'rich.prompt',
    'prompt_toolkit',
    'prompt_toolkit.history',
    'prompt_toolkit.completion',
    'loguru',
    'pydantic',
    'pydantic_settings',
    'dependency_injector',
    'dependency_injector.containers',
    'dependency_injector.providers',
]

# Collect all data files - include the src directory
datas = [
    (str(project_root / "src" / "zesec"), "zesec"),
]

# Analysis for console executable
a_console = Analysis(
    ['zesec_console.py'],
    pathex=[str(project_root / "src")],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Analysis for GUI executable
a_gui = Analysis(
    ['zesec_gui.py'],
    pathex=[str(project_root / "src")],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz_console = PYZ(a_console.pure, a_console.zipped_data, cipher=block_cipher)
pyz_gui = PYZ(a_gui.pure, a_gui.zipped_data, cipher=block_cipher)

# Console executable
exe_console = EXE(
    pyz_console,
    a_console.scripts,
    a_console.binaries,
    a_console.zipfiles,
    a_console.datas,
    [],
    name='zesec',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_file if sys.platform != 'darwin' else None,  # macOS handles icon differently
)

# GUI executable
exe_gui = EXE(
    pyz_gui,
    a_gui.scripts,
    a_gui.binaries,
    a_gui.zipfiles,
    a_gui.datas,
    [],
    name='zesec-gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_file if sys.platform != 'darwin' else None,  # macOS handles icon differently
)

# macOS app bundle (only on macOS)
if sys.platform == 'darwin':
    app_gui = BUNDLE(
        exe_gui,
        name='zesec-gui.app',
        icon=icon_file,
        bundle_identifier='com.zesec.app',
    )

