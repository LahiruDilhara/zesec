#!/usr/bin/env python3
"""Zesec - Secure file encryption and cleaning tool.

Console entry point for the application.
"""

# ==============================================================================
# NUITKA BUILD CONFIGURATION MANIFEST
# ==============================================================================
# nuitka-project: --standalone
# nuitka-project: --onefile
# nuitka-project: --disable-plugin=pyside6
# nuitka-project: --include-data-dir={MAIN_DIRECTORY}/../assets=assets
# nuitka-project: --company-name="Lahiru Dilhara"
# nuitka-project: --product-name="Zesec Console"
# nuitka-project: --copyright="Copyright (c) 2026 Lahiru Dilhara. All rights reserved."

# nuitka-project-if: {OS} == "Windows":
#    nuitka-project: --windows-icon-from-ico={MAIN_DIRECTORY}/../assets/icon/icon.ico

# nuitka-project-if: {OS} == "Darwin":
#    nuitka-project: --macos-app-icon={MAIN_DIRECTORY}/../assets/icon/icon.icns
# ==============================================================================
import os
import sys
from pathlib import Path

if "__compiled__" in globals():
    # In Nuitka standalone mode, the executable directory is the root
    project_root = Path(sys.argv[0]).parent.resolve()
    # For onefile mode, sys.argv[0] is the temp dir where assets are unpacked? No, sys.argv[0] is the exe.
    # Nuitka onefile actually sets os.path.dirname(__file__) to the temp dir!
    project_root = Path(__file__).parent.resolve()
else:
    # Running as script - project root is one level up from src
    project_root = Path(__file__).parent.parent.resolve()

src_path = project_root / "src"

# Set ZESEC_ROOT so all modules know where the data files are
os.environ["ZESEC_ROOT"] = str(project_root)

# Add src to Python path so 'zesec' package can be imported
if not ("__compiled__" in globals()):
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

# Import and run console mode
try:
    from zesec.console import main as console_main
except ImportError as e:
    print(f"Import error: {e}", file=sys.stderr)
    print(f"Python path: {sys.path}", file=sys.stderr)
    print(f"Looking for package in: {src_path}", file=sys.stderr)
    sys.exit(1)


def main() -> int:
    """Main entry point for console mode."""
    return console_main()


if __name__ == "__main__":
    sys.exit(main())
