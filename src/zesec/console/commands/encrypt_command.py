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
            console.print("[red]Error: encrypt requires a file path[/red]")
            console.print("[dim]Usage: encrypt <file> [--key-file <path>] [--no-clean][/dim]")
            return None
        
        file_path = Path(args[0])
        
        # Parse options
        key_file_path = None
        clean_original = True
        
        i = 1
        while i < len(args):
            if args[i] == "--key-file" and i + 1 < len(args):
                key_file_path = Path(args[i + 1])
                i += 2
            elif args[i] == "--no-clean":
                clean_original = False
                i += 1
            else:
                i += 1
        
        try:
            # Resolve paths
            file_path = file_path.resolve()
            if key_file_path:
                key_file_path = key_file_path.resolve()
            
            if not file_path.exists():
                console.print(f"[red]File does not exist: {file_path}[/red]")
                return None
            
            # Get password
            password = Prompt.ask("Enter password", password=True)
            if not password:
                console.print("[red]Password cannot be empty[/red]")
                return None
            
            # Get encryptor from container
            encryptor = self._container.encryptor()
            
            # Encrypt file
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
            else:
                console.print(f"[red]✗ Encryption failed: {result.error}[/red]")
                
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
        
        return None

    def get_help(self) -> str:
        """Get help text."""
        return """
        encrypt <file> [options]
        
        Encrypt a file using AES-256-GCM encryption.
        
        Arguments:
          file              Path to the file to encrypt
        
        Options:
          --key-file <path> Use a key file in addition to password
          --no-clean        Don't securely clean original file after encryption
        
        Examples:
          encrypt document.txt
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
            console.print("[red]Error: decrypt requires a file path[/red]")
            console.print("[dim]Usage: decrypt <file> [--key-file <path>][/dim]")
            return None
        
        file_path = Path(args[0])
        
        # Parse options
        key_file_path = None
        
        i = 1
        while i < len(args):
            if args[i] == "--key-file" and i + 1 < len(args):
                key_file_path = Path(args[i + 1])
                i += 2
            else:
                i += 1
        
        try:
            # Resolve paths
            file_path = file_path.resolve()
            if key_file_path:
                key_file_path = key_file_path.resolve()
            
            if not file_path.exists():
                console.print(f"[red]File does not exist: {file_path}[/red]")
                return None
            
            # Get password
            password = Prompt.ask("Enter password", password=True)
            if not password:
                console.print("[red]Password cannot be empty[/red]")
                return None
            
            # Get encryptor from container
            encryptor = self._container.encryptor()
            
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
            else:
                console.print(f"[red]✗ Decryption failed: {result.error}[/red]")
                
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
        
        return None

    def get_help(self) -> str:
        """Get help text."""
        return """
        decrypt <file> [options]
        
        Decrypt an encrypted file.
        
        Arguments:
          file              Path to the encrypted file
        
        Options:
          --key-file <path> Key file path (required if used during encryption)
        
        Examples:
          decrypt document.txt.zesec
          decrypt document.txt.zesec --key-file mykey.key
        """

