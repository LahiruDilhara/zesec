"""Command parser for interactive console."""

import shlex
from typing import Optional

from rich.console import Console

from ..di.container import ApplicationContainer
from .commands.base import BaseCommand
from .commands.clean_command import CleanCommand
from .commands.encrypt_command import DecryptCommand, EncryptCommand
from .commands.file_commands import (
    CatCommand,
    CdCommand,
    LsCommand,
    PwdCommand,
)
from .commands.generate_key_command import GenerateKeyCommand
from .commands.help_command import HelpCommand
from .commands.system_commands import ClearCommand, ExitCommand

console = Console()


class CommandParser:
    """Parses and executes console commands."""

    def __init__(self, container: Optional[ApplicationContainer] = None):
        """Initialize command parser.
        
        Args:
            container: Optional DI container. If None, creates a new one.
        """
        self._container = container or ApplicationContainer()
        
        # Register all commands
        # Note: HelpCommand needs commands registry, so we create it after
        self._commands: dict[str, BaseCommand] = {
            # File operations
            "ls": LsCommand(),
            "cat": CatCommand(),
            "pwd": PwdCommand(),
            "cd": CdCommand(),
            
            # Encryption
            "encrypt": EncryptCommand(self._container),
            "decrypt": DecryptCommand(self._container),
            "generate-key": GenerateKeyCommand(self._container),
            
            # Cleaning
            "clean": CleanCommand(self._container),
            "clean-dir": CleanCommand(self._container, is_directory=True),
            
            # System
            "exit": ExitCommand(),
            "quit": ExitCommand(),
            "clear": ClearCommand(),
        }
        
        # Create HelpCommand with commands registry to avoid circular import
        self._commands["help"] = HelpCommand(commands_registry=self._commands)

    def parse_and_execute(self, user_input: str) -> Optional[str]:
        """Parse user input and execute command.
        
        Args:
            user_input: Raw user input string
            
        Returns:
            Command result (may be "exit" to signal application exit)
        """
        if not user_input.strip():
            return None
        
        # Parse command and arguments
        try:
            parts = shlex.split(user_input)
        except ValueError as e:
            console.print(f"[red]Error parsing command: {e}[/red]")
            return None
        
        if not parts:
            return None
        
        command_name = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        # Find and execute command
        command = self._commands.get(command_name)
        if command is None:
            console.print(f"[red]Unknown command: {command_name}[/red]")
            console.print(f"[dim]Type 'help' for available commands.[/dim]")
            return None
        
        try:
            return command.execute(args)
        except Exception as e:
            console.print(f"[red]Error executing command: {e}[/red]")
            return None

    def get_command_suggestions(self, partial: str) -> list[str]:
        """Get command suggestions for partial input.
        
        Args:
            partial: Partial command name
            
        Returns:
            List of matching command names
        """
        partial_lower = partial.lower()
        return [
            cmd for cmd in self._commands.keys()
            if cmd.startswith(partial_lower)
        ]

