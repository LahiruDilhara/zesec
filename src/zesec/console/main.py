"""Interactive console application entry point."""

import sys
from pathlib import Path
from typing import Optional

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from rich.console import Console
from rich.panel import Panel

from ..config.settings import Settings
from ..utils.logging_config import get_logger, setup_logging
from .command_parser import CommandParser
from .commands.base import BaseCommand

# Initialize rich console for output
rich_console = Console()


def print_banner() -> None:
    """Print application banner."""
    banner = """
    ╔═══════════════════════════════════════════╗
    ║         ZESEC - Secure File Manager       ║
    ║     Encryption & Secure File Cleaning      ║
    ╚═══════════════════════════════════════════╝
    """
    rich_console.print(Panel(banner, style="bold cyan"))


def print_help() -> None:
    """Print help information."""
    help_text = """
    Available Commands:
    
    [bold cyan]File Operations:[/bold cyan]
      ls [path]              - List files and directories
      cat <file>             - Display file contents
      pwd                     - Print current working directory
      cd [path]               - Change directory
      
    [bold cyan]Encryption:[/bold cyan]
      encrypt <file> [options] - Encrypt a file
      decrypt <file> [options] - Decrypt a file
      generate-key <path>     - Generate encryption key file
      
    [bold cyan]Cleaning:[/bold cyan]
      clean <file>            - Securely clean a file
      clean-dir <dir>         - Securely clean directory
      
    [bold cyan]System:[/bold cyan]
      help                    - Show this help message
      exit, quit              - Exit the application
      clear                   - Clear the screen
    
    Type 'help <command>' for detailed command information.
    """
    rich_console.print(Panel(help_text, title="Help", border_style="cyan"))


def main() -> int:
    """Main entry point for console application.
    
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    # Setup logging
    setup_logging()
    logger = get_logger(__name__)
    
    # Load settings
    settings = Settings.get_instance()
    
    # Initialize command parser
    command_parser = CommandParser()
    
    # Create command completer for autocomplete
    commands = [
        "ls", "cat", "pwd", "cd",
        "encrypt", "decrypt", "generate-key",
        "clean", "clean-dir",
        "help", "exit", "quit", "clear",
    ]
    completer = WordCompleter(commands, ignore_case=True)
    
    # Setup history
    history_file = Path.home() / ".zesec_history"
    history = FileHistory(str(history_file))
    
    # Create prompt session
    session = PromptSession(
        history=history,
        completer=completer,
        complete_while_typing=True,
    )
    
    # Print banner
    print_banner()
    rich_console.print("[dim]Type 'help' for available commands. Type 'exit' to quit.[/dim]\n")
    
    # Main loop
    try:
        while True:
            try:
                # Get user input
                user_input = session.prompt("zesec> ")
                
                if not user_input.strip():
                    continue
                
                # Parse and execute command
                result = command_parser.parse_and_execute(user_input)
                
                # Handle exit
                if result == "exit":
                    rich_console.print("[green]Goodbye![/green]")
                    break
                    
            except KeyboardInterrupt:
                rich_console.print("\n[yellow]Use 'exit' or 'quit' to exit the application.[/yellow]")
                continue
            except EOFError:
                rich_console.print("\n[green]Goodbye![/green]")
                break
            except Exception as e:
                logger.error(f"Error in console: {e}")
                rich_console.print(f"[red]Error: {e}[/red]")
                
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        rich_console.print(f"[red]Fatal error: {e}[/red]")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

