"""Centralized logging configuration."""

import sys
from pathlib import Path
from typing import Optional

from loguru import logger

from ..config.settings import Settings


def setup_logging() -> None:
    """Configure logging once at application startup.
    
    This function should be called once at the beginning of the application.
    It configures both console and file logging based on settings.
    Colors: INFO=green, WARNING=yellow, ERROR=red
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

    # Console handler with colorization
    logger.add(
        sys.stderr,
        format=format_console,
        level=settings.LOG_LEVEL,
        colorize=True,
    )

    # File handler (if configured) - no colors in file
    log_file = settings.get_log_file_path()
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        logger.add(
            log_file,
            format=settings.LOG_FORMAT,
            level=settings.LOG_LEVEL,
            rotation="10 MB",
            retention="7 days",
            compression="zip",
            colorize=False,  # No colors in file
        )


def get_logger(name: str):
    """Get logger instance for a module.
    
    Args:
        name: Module name (typically __name__)
        
    Returns:
        Logger instance bound to the module name
    """
    return logger.bind(name=name)

