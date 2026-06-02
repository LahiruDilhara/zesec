"""Encrypt command implementation."""

from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.prompt import Prompt

from ...interfaces.encryptor_interface import IEncryptor
from .base import BaseCommand, CommandRegistry

console = Console()


@CommandRegistry.register(
    name="encrypt",
    description="Encrypt a file",
    category="Encryption",
    requires_container=True
)
class EncryptCommand(BaseCommand):
    """Encrypt file command."""

    def __init__(self, container):
        """Initialize encrypt command.
        
        Args:
            container: DI container
        """
        self._container = container

    def execute(self, args: list[str]) -> Optional[str]:
        """Execute encrypt command.
        
        Args:
            args: Command arguments (file path and options)
            
        Returns:
            None
        """
        if not args:
            console.print("[red]Error: encrypt requires at least one file path[/red]")
            console.print("[dim]Usage: encrypt <file1> [file2...] [--key-file <path>] [--no-clean][/dim]")
            return None
        
        # Parse options and files
        files = []
        key_file_path = None
        clean_original = True
        
        i = 0
        while i < len(args):
            if args[i] == "--key-file" and i + 1 < len(args):
                key_file_path = Path(args[i + 1])
                i += 2
            elif args[i] == "--no-clean":
                clean_original = False
                i += 1
            elif not args[i].startswith("--"):
                files.append(Path(args[i]))
                i += 1
            else:
                console.print(f"[yellow]Warning: Unknown option {args[i]}[/yellow]")
                i += 1
                
        if not files:
            console.print("[red]Error: No input files provided[/red]")
            return None
        
        try:
            if key_file_path:
                key_file_path = key_file_path.resolve()
                if not key_file_path.exists():
                    console.print(f"[red]Key file does not exist: {key_file_path}[/red]")
                    return None
                
            
            # Get password
            password = Prompt.ask("Enter password", password=True)
            if not password:
                console.print("[red]Password cannot be empty[/red]")
                return None
                
            confirm_password = Prompt.ask("Confirm password", password=True)
            if password != confirm_password:
                console.print("[red]Passwords do not match[/red]")
                return None
            
            # Get encryptor from container
            encryptor = self._container.encryptor()
            
            success_count = 0
            for file_path in files:
                file_path = file_path.resolve()
                if not file_path.exists():
                    console.print(f"[red]File does not exist: {file_path}[/red]")
                    continue
                    
                console.print(f"[cyan]Encrypting: {file_path}[/cyan]")
                result = encryptor.encrypt_file(
                    file_path,
                    password,
                    clean_original=clean_original,
                    key_file_path=key_file_path,
                )
                
                if result.success:
                    console.print(f"[green]✓ Encrypted successfully: {result.output_path}[/green]")
                    console.print(f"[dim]File size: {result.file_size} bytes[/dim]")
                    success_count += 1
                else:
                    console.print(f"[red]✗ Encryption failed: {result.error}[/red]")
                    
            console.print(f"\n[bold]Completed: {success_count}/{len(files)} files encrypted successfully.[/bold]")
                
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
        
        return None

    def get_help(self) -> str:
        """Get help text."""
        return """
        encrypt <file1> [file2...] [options]
        
        Encrypt one or more files using AES-256-GCM encryption.
        
        Arguments:
          file              Paths to the files to encrypt
        
        Options:
          --key-file <path> Use a key file in addition to password
          --no-clean        Don't securely clean original file after encryption
        
        Examples:
          encrypt document1.txt document2.txt
          encrypt document.txt --key-file mykey.key
          encrypt document.txt --no-clean
        """


@CommandRegistry.register(
    name="decrypt",
    description="Decrypt a file",
    category="Encryption",
    requires_container=True
)
class DecryptCommand(BaseCommand):
    """Decrypt file command."""

    def __init__(self, container):
        """Initialize decrypt command.
        
        Args:
            container: DI container
        """
        self._container = container

    def execute(self, args: list[str]) -> Optional[str]:
        """Execute decrypt command.
        
        Args:
            args: Command arguments (file path and options)
            
        Returns:
            None
        """
        if not args:
            console.print("[red]Error: decrypt requires at least one file path[/red]")
            console.print("[dim]Usage: decrypt <file1> [file2...] [--key-file <path>][/dim]")
            return None
        
        # Parse options
        files = []
        key_file_path = None
        
        i = 0
        while i < len(args):
            if args[i] == "--key-file" and i + 1 < len(args):
                key_file_path = Path(args[i + 1])
                i += 2
            elif not args[i].startswith("--"):
                files.append(Path(args[i]))
                i += 1
            else:
                console.print(f"[yellow]Warning: Unknown option {args[i]}[/yellow]")
                i += 1
                
        if not files:
            console.print("[red]Error: No input files provided[/red]")
            return None
        
        try:
            if key_file_path:
                key_file_path = key_file_path.resolve()
                if not key_file_path.exists():
                    console.print(f"[red]Key file does not exist: {key_file_path}[/red]")
                    return None
            
            # Get password
            password = Prompt.ask("Enter password", password=True)
            if not password:
                console.print("[red]Password cannot be empty[/red]")
                return None
            
            # Get encryptor from container
            encryptor = self._container.encryptor()
            
            success_count = 0
            for file_path in files:
                file_path = file_path.resolve()
                if not file_path.exists():
                    console.print(f"[red]File does not exist: {file_path}[/red]")
                    continue
                
                # Decrypt file
                console.print(f"[cyan]Decrypting: {file_path}[/cyan]")
                result = encryptor.decrypt_file(
                    file_path,
                    password,
                    key_file_path=key_file_path,
                )
                
                if result.success:
                    console.print(f"[green]✓ Decrypted successfully: {result.output_path}[/green]")
                    console.print(f"[dim]File size: {result.file_size} bytes[/dim]")
                    success_count += 1
                else:
                    console.print(f"[red]✗ Decryption failed: {result.error}[/red]")
                    
            console.print(f"\n[bold]Completed: {success_count}/{len(files)} files decrypted successfully.[/bold]")
                
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
        
        return None

    def get_help(self) -> str:
        """Get help text."""
        return """
        decrypt <file1> [file2...] [options]
        
        Decrypt one or more encrypted files.
        
        Arguments:
          file              Paths to the encrypted files
        
        Options:
          --key-file <path> Key file path (required if used during encryption)
        
        Examples:
          decrypt document1.txt.zesec document2.txt.zesec
          decrypt document.txt.zesec --key-file mykey.key
        """

