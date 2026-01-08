"""Base command class for all console commands."""

from abc import ABC, abstractmethod
from typing import Any, Optional


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

