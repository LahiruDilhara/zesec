"""File operation commands (ls, cat, pwd, cd) - cross-platform."""

import os
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.table import Table
from rich.tree import Tree

from ...utils.platform import get_platform
from .base import BaseCommand

console = Console()


class LsCommand(BaseCommand):
    """List files and directories command."""

    def execute(self, args: list[str]) -> Optional[str]:
        """Execute ls command.
        
        Args:
            args: Command arguments (optional path)
            
        Returns:
            None
        """
        # Get target path (default to current directory)
        target_path = Path(args[0]) if args else Path.cwd()
        
        try:
            # Resolve path
            target_path = target_path.resolve()
            
            if not target_path.exists():
                console.print(f"[red]Path does not exist: {target_path}[/red]")
                return None
            
            if target_path.is_file():
                # Single file
                self._print_file_info(target_path)
            else:
                # Directory listing
                self._print_directory(target_path)
                
        except Exception as e:
            console.print(f"[red]Error listing directory: {e}[/red]")
        
        return None

    def _print_file_info(self, file_path: Path) -> None:
        """Print information about a single file."""
        try:
            stat = file_path.stat()
            size = stat.st_size
            size_str = self._format_size(size)
            
            console.print(f"[cyan]{file_path.name}[/cyan]")
            console.print(f"  Size: {size_str}")
            console.print(f"  Path: {file_path}")
        except Exception as e:
            console.print(f"[red]Error reading file info: {e}[/red]")

    def _print_directory(self, dir_path: Path) -> None:
        """Print directory contents."""
        try:
            items = sorted(dir_path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
            
            if not items:
                console.print(f"[dim]Directory is empty: {dir_path}[/dim]")
                return
            
            # Create table for directory listing
            table = Table(show_header=True, header_style="bold cyan")
            table.add_column("Type", style="dim", width=6)
            table.add_column("Name", style="cyan")
            table.add_column("Size", justify="right", style="green")
            
            for item in items:
                item_type = "[DIR]" if item.is_dir() else "[FILE]"
                name = item.name
                
                if item.is_file():
                    try:
                        size = item.stat().st_size
                        size_str = self._format_size(size)
                    except:
                        size_str = "?"
                else:
                    size_str = "-"
                
                table.add_row(item_type, name, size_str)
            
            console.print(f"\n[bold]Contents of: {dir_path}[/bold]")
            console.print(table)
            
        except PermissionError:
            console.print(f"[red]Permission denied: {dir_path}[/red]")
        except Exception as e:
            console.print(f"[red]Error reading directory: {e}[/red]")

    def _format_size(self, size: int) -> str:
        """Format file size in human-readable format."""
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"

    def get_help(self) -> str:
        """Get help text."""
        return """
        ls [path]
        
        List files and directories.
        
        Arguments:
          path    Optional path to list (default: current directory)
        
        Examples:
          ls
          ls /home/user
          ls documents
        """


class CatCommand(BaseCommand):
    """Display file contents command."""

    def execute(self, args: list[str]) -> Optional[str]:
        """Execute cat command.
        
        Args:
            args: Command arguments (file path)
            
        Returns:
            None
        """
        if not args:
            console.print("[red]Error: cat requires a file path[/red]")
            console.print("[dim]Usage: cat <file>[/dim]")
            return None
        
        file_path = Path(args[0])
        
        try:
            # Resolve path
            file_path = file_path.resolve()
            
            if not file_path.exists():
                console.print(f"[red]File does not exist: {file_path}[/red]")
                return None
            
            if not file_path.is_file():
                console.print(f"[red]Not a file: {file_path}[/red]")
                return None
            
            # Read and display file
            try:
                with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
                    
                console.print(f"[bold cyan]Contents of: {file_path}[/bold cyan]")
                console.print("─" * 60)
                console.print(content)
                console.print("─" * 60)
                
            except UnicodeDecodeError:
                # Try binary mode for non-text files
                with open(file_path, "rb") as f:
                    content = f.read()
                    size = len(content)
                    console.print(f"[yellow]Binary file ({size} bytes)[/yellow]")
                    console.print("[dim]Use a hex viewer for binary files.[/dim]")
            except PermissionError:
                console.print(f"[red]Permission denied: {file_path}[/red]")
                
        except Exception as e:
            console.print(f"[red]Error reading file: {e}[/red]")
        
        return None

    def get_help(self) -> str:
        """Get help text."""
        return """
        cat <file>
        
        Display file contents.
        
        Arguments:
          file    Path to the file to display
        
        Examples:
          cat document.txt
          cat /path/to/file.txt
        """


class PwdCommand(BaseCommand):
    """Print current working directory command."""

    def execute(self, args: list[str]) -> Optional[str]:
        """Execute pwd command.
        
        Args:
            args: Command arguments (ignored)
            
        Returns:
            None
        """
        try:
            cwd = Path.cwd().resolve()
            console.print(f"[cyan]{cwd}[/cyan]")
        except Exception as e:
            console.print(f"[red]Error getting current directory: {e}[/red]")
        
        return None

    def get_help(self) -> str:
        """Get help text."""
        return """
        pwd
        
        Print the current working directory.
        
        Examples:
          pwd
        """


class CdCommand(BaseCommand):
    """Change directory command."""

    def execute(self, args: list[str]) -> Optional[str]:
        """Execute cd command.
        
        Args:
            args: Command arguments (directory path)
            
        Returns:
            None
        """
        if not args:
            # Go to home directory
            target = Path.home()
        else:
            target = Path(args[0])
        
        try:
            # Resolve path
            target = target.resolve()
            
            if not target.exists():
                console.print(f"[red]Directory does not exist: {target}[/red]")
                return None
            
            if not target.is_dir():
                console.print(f"[red]Not a directory: {target}[/red]")
                return None
            
            # Change directory
            os.chdir(target)
            console.print(f"[green]Changed to: {target}[/green]")
            
        except PermissionError:
            console.print(f"[red]Permission denied: {target}[/red]")
        except Exception as e:
            console.print(f"[red]Error changing directory: {e}[/red]")
        
        return None

    def get_help(self) -> str:
        """Get help text."""
        return """
        cd [path]
        
        Change the current working directory.
        
        Arguments:
          path    Optional directory path (default: home directory)
        
        Examples:
          cd
          cd /home/user
          cd documents
          cd ..
        """

