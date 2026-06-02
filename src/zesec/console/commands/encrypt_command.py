"""Encrypt command implementation."""

from pathlib import Path
from typing import Optional

from tqdm import tqdm
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
            console.print("[dim]Usage: encrypt <file1> [file2...] --dest <dir> [--key-file <path>] [--no-clean][/dim]")
            return None
        
        # Parse options and files
        files = []
        key_file_path = None
        dest_dir = None
        clean_original = True
        
        i = 0
        while i < len(args):
            if args[i] == "--key-file" and i + 1 < len(args):
                key_file_path = Path(args[i + 1])
                i += 2
            elif args[i] in ("--dest", "-d") and i + 1 < len(args):
                dest_dir = Path(args[i + 1])
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
            
        if not dest_dir:
            console.print("[red]Error: Destination directory (--dest) is required.[/red]")
            return None
            
        dest_dir = dest_dir.resolve()
        if not dest_dir.exists():
            dest_dir.mkdir(parents=True, exist_ok=True)
        
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
            failed_files = []
            
            with tqdm(total=len(files) * 100, desc="Overall Progress", unit="%") as main_pbar:
                for file_path in files:
                    file_path = file_path.resolve()
                    if not file_path.exists():
                        failed_files.append((file_path, "File does not exist"))
                        main_pbar.update(100)
                        continue
                        
                    output_path = dest_dir / f"{file_path.name}.zesec"
                    
                    last_pct = [0]
                    def progress_cb(pct: int):
                        delta = pct - last_pct[0]
                        if delta > 0:
                            main_pbar.update(delta)
                            last_pct[0] = pct
                            
                    result = encryptor.encrypt_file(
                        file_path,
                        password,
                        output_path=output_path,
                        clean_original=clean_original,
                        key_file_path=key_file_path,
                        progress_callback=progress_cb
                    )
                
                    if result.success:
                        success_count += 1
                    else:
                        failed_files.append((file_path, result.error))
                        
                    # Make sure it reaches 100 for this file
                    remaining = 100 - last_pct[0]
                    if remaining > 0:
                        main_pbar.update(remaining)
                    
            console.print(f"\n[bold]Completed: {success_count}/{len(files)} files encrypted successfully.[/bold]")
            if failed_files:
                console.print("\n[red]Failed files:[/red]")
                for f, err in failed_files:
                    console.print(f"[red] - {f.name}: {err}[/red]")
                
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
          --dest, -d <dir>  Destination directory (required)
          --key-file <path> Use a key file in addition to password
          --no-clean        Don't securely clean original file after encryption
        
        Examples:
          encrypt document1.txt document2.txt --dest /path/to/output
          encrypt document.txt -d output/ --key-file mykey.key
          encrypt document.txt -d . --no-clean
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
            console.print("[dim]Usage: decrypt <file1> [file2...] --dest <dir> [--key-file <path>][/dim]")
            return None
        
        # Parse options
        files = []
        key_file_path = None
        dest_dir = None
        clean_original = False
        
        i = 0
        while i < len(args):
            if args[i] == "--key-file" and i + 1 < len(args):
                key_file_path = Path(args[i + 1])
                i += 2
            elif args[i] in ("--dest", "-d") and i + 1 < len(args):
                dest_dir = Path(args[i + 1])
                i += 2
            elif args[i] == "--clean":
                clean_original = True
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
            
        if not dest_dir:
            console.print("[red]Error: Destination directory (--dest) is required.[/red]")
            return None
            
        dest_dir = dest_dir.resolve()
        if not dest_dir.exists():
            dest_dir.mkdir(parents=True, exist_ok=True)
        
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
            failed_files = []
            
            with tqdm(total=len(files) * 100, desc="Overall Progress", unit="%") as main_pbar:
                for file_path in files:
                    file_path = file_path.resolve()
                    if not file_path.exists():
                        failed_files.append((file_path, "File does not exist"))
                        main_pbar.update(100)
                        continue
                    
                    orig_name = file_path.name
                    if orig_name.endswith('.zesec'):
                        orig_name = orig_name[:-6]
                    output_path = dest_dir / orig_name
                    
                    last_pct = [0]
                    def progress_cb(pct: int):
                        delta = pct - last_pct[0]
                        if delta > 0:
                            main_pbar.update(delta)
                            last_pct[0] = pct
                            
                    result = encryptor.decrypt_file(
                        file_path,
                        password,
                        output_path=output_path,
                        clean_original=clean_original,
                        key_file_path=key_file_path,
                        progress_callback=progress_cb
                    )
                
                    if result.success:
                        success_count += 1
                    else:
                        failed_files.append((file_path, result.error))
                        
                    # Make sure it reaches 100 for this file
                    remaining = 100 - last_pct[0]
                    if remaining > 0:
                        main_pbar.update(remaining)
                    
            console.print(f"\n[bold]Completed: {success_count}/{len(files)} files decrypted successfully.[/bold]")
            if failed_files:
                console.print("\n[red]Failed files:[/red]")
                for f, err in failed_files:
                    console.print(f"[red] - {f.name}: {err}[/red]")
                
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
          --dest, -d <dir>  Destination directory (required)
          --key-file <path> Key file path (required if used during encryption)
          --clean           Securely delete original encrypted file after decryption
        
        Examples:
          decrypt document1.txt.zesec document2.txt.zesec -d /path/to/output
          decrypt document.txt.zesec -d . --key-file mykey.key
        """

