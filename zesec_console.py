#!/usr/bin/env python3
"""Zesec Console Entry Point - for PyInstaller."""

import sys
from pathlib import Path

# Get the project root directory
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    project_root = Path(sys._MEIPASS)
    src_path = project_root / "src"
else:
    # Running as script
    project_root = Path(__file__).parent.resolve()
    src_path = project_root / "src"

# Add src to Python path so 'zesec' package can be imported
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Import and run console
from zesec.console import main
sys.exit(main())

