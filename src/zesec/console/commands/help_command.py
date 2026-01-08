"""Help command implementation."""

from typing import Optional

from rich.console import Console
from rich.panel import Panel

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
        help_text = """
        [bold cyan]Available Commands:[/bold cyan]
        
        [bold]File Operations:[/bold]
          ls [path]              - List files and directories
          cat <file>             - Display file contents
          pwd                     - Print current working directory
          cd [path]               - Change directory
        
        [bold]Encryption:[/bold]
          encrypt <file>         - Encrypt a file
          decrypt <file>         - Decrypt a file
          generate-key <path>    - Generate encryption key file
        
        [bold]Cleaning:[/bold]
          clean <file>           - Securely clean a file
          clean-dir <dir>        - Securely clean directory
        
        [bold]System:[/bold]
          help [command]         - Show help (this message)
          exit, quit             - Exit the application
          clear                   - Clear the screen
        
        Type 'help <command>' for detailed information about a specific command.
        """
        console.print(Panel(help_text, title="Zesec Help", border_style="cyan"))

    def _show_command_help(self, command_name: str) -> None:
        """Show help for a specific command.
        
        Args:
            command_name: Name of the command
        """
        if self._commands_registry:
            command = self._commands_registry.get(command_name)
            if command:
                help_text = command.get_help()
                console.print(Panel(help_text, title=f"Help: {command_name}", border_style="cyan"))
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

