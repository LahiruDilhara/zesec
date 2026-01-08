"""Cross-platform utilities and platform detection."""

import platform
from enum import Enum
from pathlib import Path


class Platform(Enum):
    """Supported platforms."""

    WINDOWS = "windows"
    LINUX = "linux"
    MACOS = "macos"
    UNKNOWN = "unknown"


def get_platform() -> Platform:
    """Detect the current platform.
    
    Returns:
        Platform enum value
    """
    system = platform.system().lower()
    if system == "windows":
        return Platform.WINDOWS
    elif system == "linux":
        return Platform.LINUX
    elif system == "darwin":
        return Platform.MACOS
    else:
        return Platform.UNKNOWN


def get_home_directory() -> Path:
    """Get user home directory in a cross-platform way.
    
    Returns:
        Path to home directory
    """
    return Path.home()


def normalize_path(path: str | Path) -> Path:
    """Normalize a path for cross-platform compatibility.
    
    Args:
        path: Path string or Path object
        
    Returns:
        Normalized Path object
    """
    return Path(path).expanduser().resolve()

