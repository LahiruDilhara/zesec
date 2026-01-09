"""Base command class for all console commands."""

from abc import ABC, abstractmethod
from typing import Any, Optional, Dict, List, Callable, Type


class CommandRegistry:
    """Global registry for auto-discovered commands."""
    
    _registered_commands: Dict[str, Dict[str, Any]] = {}
    
    @classmethod
    def register(
        cls,
        name: str,
        description: str = "",
        category: str = "System",
        aliases: Optional[List[str]] = None,
        requires_container: bool = False,
        factory: Optional[Callable] = None
    ):
        """Decorator to register a command class.
        
        Args:
            name: Command name (e.g., "ls", "encrypt")
            description: Short description for help
            category: Category for help grouping
            aliases: Optional list of aliases (e.g., ["quit"] for "exit")
            requires_container: Whether command needs DI container
            factory: Optional factory function for creating instances with custom params
        """
        def decorator(command_class: Type):
            # Verify it extends BaseCommand
            if not issubclass(command_class, BaseCommand):
                raise TypeError(f"{command_class.__name__} must extend BaseCommand")
            
            # Store metadata
            cls._registered_commands[name] = {
                "class": command_class,
                "description": description,
                "category": category,
                "aliases": aliases or [],
                "requires_container": requires_container,
                "factory": factory,
            }
            
            # Also register aliases
            if aliases:
                for alias in aliases:
                    cls._registered_commands[alias] = cls._registered_commands[name]
            
            return command_class
        return decorator
    
    @classmethod
    def get_all_commands(cls) -> Dict[str, Dict[str, Any]]:
        """Get all registered commands."""
        return cls._registered_commands.copy()
    
    @classmethod
    def get_command_info(cls, name: str) -> Optional[Dict[str, Any]]:
        """Get command info by name."""
        return cls._registered_commands.get(name)
    
    @classmethod
    def clear(cls):
        """Clear registry (mainly for testing)."""
        cls._registered_commands.clear()


class BaseCommand(ABC):
    """Base class for all console commands."""

    @abstractmethod
    def execute(self, args: list[str]) -> Optional[str]:
        """Execute the command.
        
        Args:
            args: Command arguments
            
        Returns:
            Command result (may be "exit" to signal application exit)
        """
        pass

    def get_help(self) -> str:
        """Get help text for this command.
        
        Returns:
            Help text string
        """
        return "No help available for this command."

