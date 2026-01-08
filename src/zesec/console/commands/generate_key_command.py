"""Generate key command implementation."""

from pathlib import Path
from typing import Optional

from rich.console import Console

from ...core.encryption import KeyManager
from ...core.file_operations import FileHandler
from .base import BaseCommand

console = Console()


class GenerateKeyCommand(BaseCommand):
    """Generate encryption key file command."""

    def __init__(self, container):
        """Initialize generate key command.
        
        Args:
            container: DI container
        """
        self._container = container

    def execute(self, args: list[str]) -> Optional[str]:
        """Execute generate-key command.
        
        Args:
            args: Command arguments (key file path)
            
        Returns:
            None
        """
        if not args:
            console.print("[red]Error: generate-key requires a file path[/red]")
            console.print("[dim]Usage: generate-key <path>[/dim]")
            return None
        
        key_file_path = Path(args[0])
        
        try:
            # Resolve path
            key_file_path = key_file_path.resolve()
            
            # Check if file already exists
            if key_file_path.exists():
                console.print(f"[yellow]Warning: File already exists: {key_file_path}[/yellow]")
                response = console.input("Overwrite? (y/N): ")
                if response.lower() != "y":
                    console.print("[dim]Cancelled.[/dim]")
                    return None
            
            # Get key manager and file handler from container
            file_handler = self._container.file_handler()
            key_manager = KeyManager(file_handler=file_handler)
            
            # Generate key file
            console.print(f"[cyan]Generating key file: {key_file_path}[/cyan]")
            success = key_manager.generate_key_file(key_file_path)
            
            if success:
                console.print(f"[green]✓ Key file generated successfully: {key_file_path}[/green]")
                console.print("[yellow]⚠ Keep this key file secure! You'll need it for decryption.[/yellow]")
            else:
                console.print("[red]✗ Failed to generate key file[/red]")
                
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
        
        return None

    def get_help(self) -> str:
        """Get help text."""
        return """
        generate-key <path>
        
        Generate a random encryption key file.
        
        Arguments:
          path    Path where the key file should be saved
        
        Examples:
          generate-key mykey.key
          generate-key /path/to/keyfile.key
        """

