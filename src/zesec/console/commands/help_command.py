"""Help command implementation."""

from typing import Optional

from rich.console import Console
from rich.table import Table

from .base import BaseCommand, CommandRegistry

console = Console()


@CommandRegistry.register(
    name="help",
    description="Show help information",
    category="System"
)
class HelpCommand(BaseCommand):
    """Help command."""

    def __init__(self, commands_registry=None):
        """Initialize help command.
        
        Args:
            commands_registry: Optional dict of commands for showing command-specific help
        """
        self._commands_registry = commands_registry

    def execute(self, args: list[str]) -> Optional[str]:
        """Execute help command.
        
        Args:
            args: Command arguments (optional command name)
            
        Returns:
            None
        """
        if not args:
            # Show general help
            self._show_general_help()
        else:
            # Show help for specific command
            command_name = args[0].lower()
            self._show_command_help(command_name)
        
        return None

    def _show_general_help(self) -> None:
        """Show general help information."""
        # Get commands from registry
        all_commands = CommandRegistry.get_all_commands()
        
        # Group commands by category
        commands_by_category: dict[str, list[dict]] = {}
        
        for name, info in all_commands.items():
            # Skip aliases (they point to the same command)
            if name in info.get("aliases", []):
                continue
            
            category = info.get("category", "System")
            if category not in commands_by_category:
                commands_by_category[category] = []
            
            commands_by_category[category].append({
                "name": name,
                "description": info.get("description", ""),
                "aliases": info.get("aliases", [])
            })
        
        # Create a table for better alignment
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Command", style="cyan", width=20)
        table.add_column("Description", style="white")
        
        # Add commands grouped by category
        for category in sorted(commands_by_category.keys()):
            table.add_row(f"[bold]{category}:[/bold]", "")
            for cmd_info in sorted(commands_by_category[category], key=lambda x: x["name"]):
                name = cmd_info["name"]
                if cmd_info["aliases"]:
                    name += f", {', '.join(cmd_info['aliases'])}"
                table.add_row(f"  {name}", cmd_info["description"])
            table.add_row("", "")  # Empty row for spacing
        
        # Print the help content directly without a box
        console.print("[bold cyan]Available Commands:[/bold cyan]")
        console.print()
        console.print(table)
        console.print()
        console.print("[dim]Type 'help <command>' for detailed information about a specific command.[/dim]")

    def _show_command_help(self, command_name: str) -> None:
        """Show help for a specific command.
        
        Args:
            command_name: Name of the command
        """
        if self._commands_registry:
            command = self._commands_registry.get(command_name)
            if command:
                help_text = command.get_help()
                console.print(help_text)
                return
        
        console.print(f"[red]Unknown command: {command_name}[/red]")
        console.print("[dim]Type 'help' for available commands.[/dim]")

    def get_help(self) -> str:
        """Get help text."""
        return """
        help [command]
        
        Show help information.
        
        Arguments:
          command    Optional command name for detailed help
        
        Examples:
          help
          help encrypt
          help ls
        """

