"""System commands (exit, clear, etc.)."""

import os
from typing import Optional

from rich.console import Console

from .base import BaseCommand, CommandRegistry

console = Console()


@CommandRegistry.register(
    name="exit",
    description="Exit the application",
    category="System",
    aliases=["quit"]
)
class ExitCommand(BaseCommand):
    """Exit application command."""

    def execute(self, args: list[str]) -> Optional[str]:
        """Execute exit command.
        
        Args:
            args: Command arguments (ignored)
            
        Returns:
            "exit" to signal application exit
        """
        return "exit"

    def get_help(self) -> str:
        """Get help text."""
        return """
        exit, quit
        
        Exit the Zesec application.
        
        Examples:
          exit
          quit
        """


@CommandRegistry.register(
    name="clear",
    description="Clear the screen",
    category="System"
)
class ClearCommand(BaseCommand):
    """Clear screen command."""

    def execute(self, args: list[str]) -> Optional[str]:
        """Execute clear command.
        
        Args:
            args: Command arguments (ignored)
            
        Returns:
            None
        """
        # Clear screen (cross-platform)
        os.system("cls" if os.name == "nt" else "clear")
        return None

    def get_help(self) -> str:
        """Get help text."""
        return """
        clear
        
        Clear the terminal screen.
        
        Examples:
          clear
        """

