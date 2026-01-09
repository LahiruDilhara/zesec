"""Command loader for loading commands."""

from typing import Dict, Optional, Type

from ...di.container import ApplicationContainer
from .base import BaseCommand, CommandRegistry


def discover_commands(commands_package_path: str = "zesec.console.commands") -> None:
    """Load and register all commands by directly importing command modules.
    
    This function directly imports all command modules, which triggers
    the @CommandRegistry.register decorators.
    
    Args:
        commands_package_path: Full path to commands package (kept for compatibility)
    """
    # Directly import all command modules
    # This ensures they work in both normal Python and PyInstaller frozen executables
    try:
        from . import clean_command
        from . import encrypt_command
        from . import file_commands
        from . import generate_key_command
        from . import help_command
        from . import system_commands
    except ImportError as e:
        print(f"Error importing command modules: {e}")
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

