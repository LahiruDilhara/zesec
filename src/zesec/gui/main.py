"""GUI application entry point."""

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from ..config.settings import Settings
from ..utils.logging_config import get_logger, setup_logging
from ..di.container import ApplicationContainer
from .windows.main_window import MainWindow


def main() -> int:
    """Main entry point for GUI application.
    
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    # Setup logging
    setup_logging()
    logger = get_logger(__name__)
    
    # Load settings
    settings = Settings.get_instance()
    
    # Create QApplication
    app = QApplication(sys.argv)
    app.setApplicationName("Zesec")
    app.setOrganizationName("Zesec")
    
    # Enable high DPI scaling
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    try:
        # Create DI container
        container = ApplicationContainer()
        
        # Create and show main window
        window = MainWindow(container)
        window.show()
        
        # Run event loop
        return app.exec()
        
    except Exception as e:
        logger.error(f"Fatal error in GUI: {e}")
        # Try to print to stderr as fallback (may not be available on Windows GUI apps)
        if sys.stderr is not None:
            try:
                print(f"Fatal error: {e}", file=sys.stderr)
            except (AttributeError, OSError):
                pass  # stderr not available or not writable
        return 1

