#!/usr/bin/env python3
"""Zesec - Secure file encryption and cleaning tool.

GUI entry point for the application.
"""

# ==============================================================================
# NUITKA BUILD CONFIGURATION MANIFEST
# ==============================================================================
# nuitka-project: --standalone
# nuitka-project: --onefile
# nuitka-project: --enable-plugin=pyside6
# nuitka-project: --include-data-dir={MAIN_DIRECTORY}/src/zesec/gui=zesec/gui
# nuitka-project: --include-data-dir={MAIN_DIRECTORY}/assets=assets
# nuitka-project: --company-name="Lahiru Dilhara"
# nuitka-project: --product-name="Zesec GUI"
# nuitka-project: --file-version=1.4.0
# nuitka-project: --copyright="Copyright (c) 2026 Lahiru Dilhara. All rights reserved."

# nuitka-project-if: {OS} == "Windows":
#    nuitka-project: --windows-icon-from-ico={MAIN_DIRECTORY}/assets/icon/icon.ico
#    nuitka-project: --windows-console-mode=disable

# nuitka-project-if: {OS} == "Darwin":
#    nuitka-project: --macos-create-app-bundle
#    nuitka-project: --macos-app-icon={MAIN_DIRECTORY}/assets/icon/icon.icns
#    nuitka-project: --macos-app-protected-resource="NSMicrophoneUsageDescription:Microphone access"
# ==============================================================================
import os
import sys
import argparse
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).parent.parent.resolve()
src_path = project_root / "src"

# Set ZESEC_ROOT so all modules know where the data files are
os.environ["ZESEC_ROOT"] = str(project_root)

# Add src to Python path so 'zesec' package can be imported
if not (getattr(sys, 'frozen', False) or "__compiled__" in globals()):
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

def main() -> int:
    """Main entry point for GUI mode."""
    # We still accept arguments in case it was launched via association (e.g., File Manager)
    # The --gui arg might be passed by the system integration script
    parser = argparse.ArgumentParser(
        description="Zesec - Secure file encryption and cleaning tool"
    )
    parser.add_argument("--gui", action="store_true", help="Launch the graphical user interface")
    args, unknown = parser.parse_known_args()
    
    # Import and run GUI
    try:
        from zesec.gui import main as gui_main
        return gui_main()
    except ImportError as e:
        print(f"GUI import error: {e}", file=sys.stderr)
        print("Make sure PySide6 is installed: pip install PySide6", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
