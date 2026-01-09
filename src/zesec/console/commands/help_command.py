"""Help command implementation."""

from typing import Optional

from rich.console import Console
from rich.table import Table

from .base import BaseCommand

console = Console()


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
        # Create a table for better alignment
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Command", style="cyan", width=20)
        table.add_column("Description", style="white")
        
        # File Operations
        table.add_row("[bold]File Operations:[/bold]", "")
        table.add_row("  ls [path]", "List files and directories")
        table.add_row("  cat <file>", "Display file contents")
        table.add_row("  pwd", "Print current working directory")
        table.add_row("  cd [path]", "Change directory")
        table.add_row("", "")  # Empty row for spacing
        
        # Encryption
        table.add_row("[bold]Encryption:[/bold]", "")
        table.add_row("  encrypt <file>", "Encrypt a file")
        table.add_row("  decrypt <file>", "Decrypt a file")
        table.add_row("  generate-key <path>", "Generate encryption key file")
        table.add_row("", "")  # Empty row for spacing
        
        # Cleaning
        table.add_row("[bold]Cleaning:[/bold]", "")
        table.add_row("  clean <file>", "Securely clean a file")
        table.add_row("  clean-dir <dir>", "Securely clean directory")
        table.add_row("", "")  # Empty row for spacing
        
        # System
        table.add_row("[bold]System:[/bold]", "")
        table.add_row("  help [command]", "Show help (this message)")
        table.add_row("  exit, quit", "Exit the application")
        table.add_row("  clear", "Clear the screen")
        
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

