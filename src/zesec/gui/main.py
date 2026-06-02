"""GUI application entry point."""

import sys
import signal
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QTimer

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
    
    # Handle Ctrl+C properly in terminal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    # Load settings
    settings = Settings.get_instance()
    
    # Create QApplication
    app = QApplication(sys.argv)
    app.setApplicationName("Zesec")
    app.setOrganizationName("Zesec")
    
    # Load and apply modern dark theme QSS
    style_path = Path(__file__).parent / "style.qss"
    if style_path.exists():
        try:
            with open(style_path, "r", encoding="utf-8") as f:
                stylesheet = f.read()
                
            # Fix SVG paths to be absolute for QSS
            if getattr(sys, 'frozen', False):
                base_dir = Path(sys._MEIPASS)
            else:
                base_dir = Path(__file__).parent.parent.parent.parent
                
            base_dir_str = base_dir.as_posix()
            stylesheet = stylesheet.replace("url(public/svg/", f"url({base_dir_str}/public/svg/")
            
            app.setStyleSheet(stylesheet)
        except Exception as e:
            logger.warning(f"Failed to load stylesheet: {e}")
    
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

