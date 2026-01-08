"""Path utility functions for cross-platform compatibility."""

from pathlib import Path
from typing import Union

from ...utils.platform import normalize_path as _normalize_path


def normalize_path(path: Union[str, Path]) -> Path:
    """Normalize a path for cross-platform compatibility.
    
    Args:
        path: Path string or Path object
        
    Returns:
        Normalized Path object
    """
    return _normalize_path(path)

