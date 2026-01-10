"""Centralized logging configuration."""

import sys

from loguru import logger

from ..config.settings import Settings


def setup_logging() -> None:
    """Configure logging once at application startup.
    
    This function should be called once at the beginning of the application.
    It configures console logging only (no file logging).
    Colors: INFO=green, WARNING=yellow, ERROR=red
    
    On Windows GUI apps (PyInstaller), sys.stderr may be None, so we
    check for availability before adding the handler.
    """
    settings = Settings.get_instance()

    # Remove default handler
    logger.remove()

    def format_console(record: dict) -> str:
        """Format log record with custom colors.
        
        Colors:
        - INFO: green
        - WARNING: yellow
        - ERROR: red
        """
        # Color mapping based on level
        level_colors = {
            "INFO": ("<green>", "</green>"),
            "WARNING": ("<yellow>", "</yellow>"),
            "ERROR": ("<red>", "</red>"),
            "CRITICAL": ("<red><bold>", "</bold></red>"),
            "SUCCESS": ("<green>", "</green>"),
            "DEBUG": ("<blue>", "</blue>"),
        }
        
        level_name = record["level"].name
        color_tags = level_colors.get(level_name, ("", ""))
        color_open, color_close = color_tags
        
        time_str = record["time"].strftime("%Y-%m-%d %H:%M:%S")
        name = record["name"]
        function = record["function"]
        message = record["message"]
        
        # Build formatted string
        formatted = f"<green>{time_str}</green> | "
        
        # Colorize level
        if color_open:
            formatted += f"{color_open}{level_name: <8}{color_close} | "
        else:
            formatted += f"{level_name: <8} | "
        
        # Module and function names
        formatted += f"<cyan>{name}</cyan>:<cyan>{function}</cyan> | "
        
        # Colorize message
        if color_open:
            formatted += f"{color_open}{message}{color_close}"
        else:
            formatted += message
        
        return formatted + "\n"

    # Console handler with colorization (only if stderr is available)
    # On Windows GUI apps, sys.stderr may be None
    if sys.stderr is not None and hasattr(sys.stderr, 'write'):
        try:
            logger.add(
                sys.stderr,
                format=format_console,
                level=settings.LOG_LEVEL,
                colorize=True,
            )
        except (AttributeError, OSError):
            # stderr exists but may not be writable (e.g., in some GUI contexts)
            pass


def get_logger(name: str):
    """Get logger instance for a module.
    
    Args:
        name: Module name (typically __name__)
        
    Returns:
        Logger instance bound to the module name
    """
    return logger.bind(name=name)

