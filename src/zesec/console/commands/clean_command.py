"""Clean command implementation."""

from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.prompt import Confirm

from .base import BaseCommand

console = Console()


class CleanCommand(BaseCommand):
    """Secure file cleaning command."""

    def __init__(self, container, is_directory: bool = False):
        """Initialize clean command.
        
        Args:
            container: DI container
            is_directory: If True, this is clean-dir command
        """
        self._container = container
        self._is_directory = is_directory

    def execute(self, args: list[str]) -> Optional[str]:
        """Execute clean command.
        
        Args:
            args: Command arguments (file/directory path)
            
        Returns:
            None
        """
        if not args:
            cmd_name = "clean-dir" if self._is_directory else "clean"
            console.print(f"[red]Error: {cmd_name} requires a path[/red]")
            console.print(f"[dim]Usage: {cmd_name} <path>[/dim]")
            return None
        
        target_path = Path(args[0])
        
        try:
            # Resolve path
            target_path = target_path.resolve()
            
            if not target_path.exists():
                console.print(f"[red]Path does not exist: {target_path}[/red]")
                return None
            
            # Get cleaner from container
            cleaner = self._container.cleaner()
            
            if self._is_directory:
                # Clean directory
                if not target_path.is_dir():
                    console.print(f"[red]Not a directory: {target_path}[/red]")
                    return None
                
                # Confirm action
                if not Confirm.ask(f"Securely clean all files in {target_path}?"):
                    console.print("[dim]Cancelled.[/dim]")
                    return None
                
                console.print(f"[cyan]Cleaning directory: {target_path}[/cyan]")
                success = cleaner.clean_directory(target_path)
                
            else:
                # Clean single file
                if not target_path.is_file():
                    console.print(f"[red]Not a file: {target_path}[/red]")
                    return None
                
                # Confirm action
                if not Confirm.ask(f"Securely clean {target_path}?"):
                    console.print("[dim]Cancelled.[/dim]")
                    return None
                
                console.print(f"[cyan]Cleaning file: {target_path}[/cyan]")
                success = cleaner.clean_file(target_path)
            
            if success:
                console.print("[green]✓ Cleaning completed successfully[/green]")
            else:
                console.print("[red]✗ Cleaning failed[/red]")
                
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
        
        return None

    def get_help(self) -> str:
        """Get help text."""
        if self._is_directory:
            return """
            clean-dir <directory>
            
            Securely clean all files in a directory by overwriting and deleting.
            
            Arguments:
              directory    Path to the directory to clean
            
            Examples:
              clean-dir /tmp/old_files
              clean-dir documents
            """
        else:
            return """
            clean <file>
            
            Securely clean a file by overwriting with zeros and deleting.
            
            Arguments:
              file    Path to the file to clean
            
            Examples:
              clean document.txt
              clean /path/to/file.txt
            """

