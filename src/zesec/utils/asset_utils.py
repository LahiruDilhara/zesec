"""Asset utility functions for resolving application resources."""

import os
from pathlib import Path
from typing import Union

def get_asset_path(relative_path: Union[str, Path]) -> Path:
    """Get the absolute path to a file inside the assets directory.
    
    Uses ZESEC_ROOT environment variable (set by main.py during runtime)
    to locate the project root, ensuring paths resolve correctly in both
    development and Nuitka compiled environments.
    
    Args:
        relative_path: The path relative to the 'assets' directory
                       (e.g., 'icon/icon.png')
                       
    Returns:
        Path: Absolute path to the asset.
    """
    root_dir = Path(os.environ.get("ZESEC_ROOT", "."))
    return root_dir / "assets" / relative_path
