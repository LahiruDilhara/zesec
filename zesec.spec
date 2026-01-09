# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Zesec application.
Builds both console and GUI executables.
"""

import sys
from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

# Get project root
project_root = Path(SPECPATH).parent
icon_path = project_root / "img" / "icon.png"

# Convert icon path based on platform
# Use icon only if it exists, otherwise PyInstaller will skip it
if icon_path.exists():
    if sys.platform == 'win32':
        # Windows prefers .ico format - PyInstaller will handle PNG if .ico not found
        icon_ico = project_root / "img" / "icon.ico"
        icon_file = str(icon_ico) if icon_ico.exists() else str(icon_path)
    elif sys.platform == 'darwin':
        # macOS prefers .icns format - PyInstaller will handle PNG if .icns not found
        icon_icns = project_root / "img" / "icon.icns"
        icon_file = str(icon_icns) if icon_icns.exists() else str(icon_path)
    else:
        # Linux can use PNG directly
        icon_file = str(icon_path)
else:
    # No icon file found - PyInstaller will use default
    icon_file = None

# Hidden imports needed by the application

hidden_imports = [
    'zesec',
    'zesec.console',
    'zesec.console.commands',
    'zesec.gui',
    'zesec.core',
    'zesec.di',
    'zesec.config',
    'zesec.utils',
    'PySide6',
    'rich',
    'prompt_toolkit',
    'loguru',
    'pydantic',
]

# Add all submodules from dependency_injector and zesec
hidden_imports += collect_submodules("dependency_injector")
hidden_imports += collect_submodules("zesec")
hidden_imports += collect_submodules("zesec.console.commands")

# Collect all data files
# Note: We don't need to include the source directory as data files
# PyInstaller will automatically bundle Python modules from the pathex
datas = []

# Analysis for console executable
a_console = Analysis(
    ['src/zesec_console.py'],
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
    ['src/zesec_gui.py'],
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
    icon=icon_file,  # None if icon not found
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
    icon=icon_file,  # None if icon not found
)

# macOS app bundle (only on macOS)
if sys.platform == 'darwin':
    app_gui = BUNDLE(
        exe_gui,
        name='zesec-gui.app',
        icon=icon_file,
        bundle_identifier='com.zesec.app',
    )

