"""Clean command implementation."""

from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.prompt import Confirm
from tqdm import tqdm

from .base import BaseCommand, CommandRegistry

console = Console()


# Factory function for clean-dir command
def _create_clean_dir_command(container):
    """Factory function to create clean-dir command."""
    return CleanCommand(container, is_directory=True)


@CommandRegistry.register(
    name="clean",
    description="Securely clean a file",
    category="Cleaning",
    requires_container=True
)
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
            args: Command arguments (file/directory path and options)
            
        Returns:
            None
        """
        if not args:
            cmd_name = "clean-dir" if self._is_directory else "clean"
            console.print(f"[red]Error: {cmd_name} requires a path[/red]")
            console.print(f"[dim]Usage: {cmd_name} <path> [--no-delete][/dim]")
            return None
        
        files = []
        delete = True  # Default: delete after cleaning
        
        # Parse options
        i = 0
        while i < len(args):
            if args[i] == "--no-delete":
                delete = False
                i += 1
            elif not args[i].startswith("--"):
                files.append(Path(args[i]))
                i += 1
            else:
                console.print(f"[yellow]Warning: Unknown option {args[i]}[/yellow]")
                i += 1
                
        if not files:
            console.print(f"[red]Error: {cmd_name} requires at least one path[/red]")
            return None
        
        try:
            # Get cleaner from container
            cleaner = self._container.cleaner()
            
            if self._is_directory:
                target_path = files[0].resolve()
                # Clean directory
                if not target_path.is_dir():
                    console.print(f"[red]Not a directory: {target_path}[/red]")
                    return None
                
                # Confirm action
                action = "clean" if delete else "overwrite (without deleting)"
                if not Confirm.ask(f"Securely {action} all files in {target_path}?"):
                    console.print("[dim]Cancelled.[/dim]")
                    return None
                
                console.print(f"[cyan]Cleaning directory: {target_path}[/cyan]")
                success = cleaner.clean_directory(target_path, delete=delete)
                if success:
                    if delete:
                        console.print("[green]✓ Cleaning completed successfully[/green]")
                    else:
                        console.print("[green]✓ Directory files overwritten successfully (not deleted)[/green]")
                else:
                    console.print("[red]✗ Cleaning failed[/red]")
                
            else:
                # Clean multiple files
                success_count = 0
                
                action = "clean" if delete else "overwrite (without deleting)"
                if not Confirm.ask(f"Securely {action} {len(files)} files?"):
                    console.print("[dim]Cancelled.[/dim]")
                    return None
                    
                with tqdm(total=len(files), desc="Overall Progress", unit="file") as main_pbar:
                    for target_path in files:
                        target_path = target_path.resolve()
                        if not target_path.is_file():
                            console.print(f"[red]Not a file or does not exist: {target_path}[/red]")
                            main_pbar.update(1)
                            continue
                        
                        success = cleaner.clean_file(target_path, delete=delete)
                        if success:
                            success_count += 1
                        else:
                            console.print(f"[red]✗ Failed to clean {target_path}[/red]")
                        main_pbar.update(1)
                        
                console.print(f"\n[bold]Completed: {success_count}/{len(files)} files cleaned successfully.[/bold]")
                
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
        
        return None

    def get_help(self) -> str:
        """Get help text."""
        if self._is_directory:
            return """
            clean-dir <directory> [options]
            
            Securely clean all files in a directory by overwriting and deleting.
            
            Arguments:
              directory    Path to the directory to clean
            
            Options:
              --no-delete  Overwrite files but don't delete them
            
            Examples:
              clean-dir /tmp/old_files
              clean-dir documents
              clean-dir /tmp/old_files --no-delete
            """
        else:
            return """
            clean <file1> [file2...] [options]
            
            Securely clean files by overwriting with zeros and deleting.
            
            Arguments:
              file    Paths to the files to clean
            
            Options:
              --no-delete  Overwrite file but don't delete it
            
            Examples:
              clean document.txt document2.txt
              clean /path/to/file.txt
              clean document.txt --no-delete
            """


@CommandRegistry.register(
    name="clean-dir",
    description="Securely clean directory",
    category="Cleaning",
    requires_container=True,
    factory=_create_clean_dir_command
)
class CleanDirCommand(CleanCommand):
    """This class exists only for registration - not actually used."""
    pass

