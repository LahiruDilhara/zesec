"""Command parser for interactive console."""

import shlex
from typing import Optional

from rich.console import Console

from ..di.container import ApplicationContainer
from .commands.base import BaseCommand, CommandRegistry
from .commands.loader import discover_commands, create_command_instance

console = Console()


class CommandParser:
    """Parses and executes console commands."""

    def __init__(self, container: Optional[ApplicationContainer] = None):
        """Initialize command parser.
        
        Args:
            container: Optional DI container. If None, creates a new one.
        """
        self._container = container or ApplicationContainer()
        
        # Auto-discover all commands
        discover_commands()
        
        # Build command instances from registry
        self._commands: dict[str, BaseCommand] = {}
        all_commands = CommandRegistry.get_all_commands()
        
        # Track which command classes we've already instantiated
        # (to avoid creating multiple instances for aliases)
        instantiated_classes = {}
        processed_names = set()
        
        for name, info in all_commands.items():
            # Skip if we've already processed this command (could be an alias entry)
            if name in processed_names:
                continue
            
            command_class = info["class"]
            
            # If we've already instantiated this class, reuse the instance
            if command_class in instantiated_classes:
                instance = instantiated_classes[command_class]
            else:
                # Create new instance
                instance = create_command_instance(name, self._container)
                if instance:
                    instantiated_classes[command_class] = instance
                else:
                    continue
            
            # Register this name and all its aliases
            self._commands[name] = instance
            processed_names.add(name)
            
            for alias in info.get("aliases", []):
                self._commands[alias] = instance
                processed_names.add(alias)
        
        # Special case: HelpCommand needs the registry after all commands are loaded
        # Re-instantiate it with the commands registry
        if "help" in self._commands:
            from .commands.help_command import HelpCommand
            help_instance = HelpCommand(commands_registry=self._commands)
            self._commands["help"] = help_instance

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

