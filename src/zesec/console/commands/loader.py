"""Command loader for auto-discovering commands."""

import importlib
import pkgutil
from pathlib import Path
from typing import Dict, Optional, Type

from ...di.container import ApplicationContainer
from .base import BaseCommand, CommandRegistry


def discover_commands(commands_package_path: str = "zesec.console.commands") -> None:
    """Auto-discover and register all commands from a package.
    
    This function imports all Python modules in the commands package,
    which triggers the @CommandRegistry.register decorators.
    
    Args:
        commands_package_path: Full path to commands package
    """
    try:
        # Import the commands package
        commands_package = importlib.import_module(commands_package_path)
        package_path = Path(commands_package.__file__).parent
        
        # Find all Python files in the commands directory
        for finder, name, ispkg in pkgutil.iter_modules([str(package_path)]):
            # Skip packages and special files
            if ispkg or name.startswith("_") or name == "__pycache__":
                continue
            
            # Import the module (this triggers decorator registration)
            module_name = f"{commands_package_path}.{name}"
            try:
                importlib.import_module(module_name)
            except Exception as e:
                # Log error but continue loading other commands
                # In production, you might want to use proper logging
                print(f"Warning: Failed to load command module {name}: {e}")
                continue
                
    except Exception as e:
        print(f"Error discovering commands: {e}")
        raise


def create_command_instance(
    command_name: str,
    container: Optional[ApplicationContainer] = None
) -> Optional[BaseCommand]:
    """Create an instance of a registered command.
    
    Args:
        command_name: Name of the command
        container: Optional DI container
        
    Returns:
        Command instance or None if not found
    """
    command_info = CommandRegistry.get_command_info(command_name)
    if not command_info:
        return None
    
    command_class: Type[BaseCommand] = command_info["class"]
    requires_container = command_info.get("requires_container", False)
    factory = command_info.get("factory")
    
    # Use factory if provided (for special cases like clean-dir)
    if factory:
        if requires_container and container:
            return factory(container)
        elif requires_container:
            return factory(ApplicationContainer())
        else:
            return factory()
    
    # Instantiate with container if needed
    if requires_container:
        if container:
            return command_class(container)
        else:
            return command_class(ApplicationContainer())
    else:
        return command_class()

