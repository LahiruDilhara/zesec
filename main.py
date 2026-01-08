#!/usr/bin/env python3
"""Zesec - Secure file encryption and cleaning tool.

Main entry point for the application.
"""

import sys
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).parent.resolve()
src_path = project_root / "src"

# Add src to Python path so 'zesec' package can be imported
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Now import from zesec package
try:
    from zesec.console import main
except ImportError as e:
    print(f"Import error: {e}", file=sys.stderr)
    print(f"Python path: {sys.path}", file=sys.stderr)
    print(f"Looking for package in: {src_path}", file=sys.stderr)
    sys.exit(1)

if __name__ == "__main__":
    sys.exit(main())

