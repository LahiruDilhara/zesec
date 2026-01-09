#!/usr/bin/env python3
"""Zesec GUI Entry Point - for PyInstaller."""

import sys
from pathlib import Path

# Get the project root directory
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    # PyInstaller bundles packages, so zesec should be importable directly
    # No need to modify sys.path
    pass
else:
    # Running as script - add src to Python path
    project_root = Path(__file__).parent.resolve()
    src_path = project_root / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

# Import and run GUI
from zesec.gui import main
sys.exit(main())

