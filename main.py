#!/usr/bin/env python3
"""Zesec - Secure file encryption and cleaning tool.

Main entry point for the application.
"""

import argparse
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
    from zesec.console import main as console_main
except ImportError as e:
    print(f"Import error: {e}", file=sys.stderr)
    print(f"Python path: {sys.path}", file=sys.stderr)
    print(f"Looking for package in: {src_path}", file=sys.stderr)
    sys.exit(1)


def main() -> int:
    """Main entry point that routes to console or GUI mode."""
    parser = argparse.ArgumentParser(
        description="Zesec - Secure file encryption and cleaning tool"
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Launch the graphical user interface"
    )
    
    args = parser.parse_args()
    
    if args.gui:
        # Import and run GUI
        try:
            from zesec.gui import main as gui_main
            return gui_main()
        except ImportError as e:
            print(f"GUI import error: {e}", file=sys.stderr)
            print("Make sure PySide6 is installed: pip install PySide6", file=sys.stderr)
            return 1
    else:
        # Run console mode
        return console_main()


if __name__ == "__main__":
    sys.exit(main())

