"""Dependency Injection container."""

from dependency_injector import containers, providers

from ..config.settings import Settings
from ..core.encryption import EncryptorService, KeyManager
from ..core.file_operations import CleanerService, FileHandler


class ApplicationContainer(containers.DeclarativeContainer):
    """Dependency Injection Container - wires all dependencies."""

    # Configuration
    config = providers.Configuration()

    # Settings (singleton)
    settings = providers.Singleton(Settings.get_instance)

    # Core services (singletons)
    file_handler = providers.Singleton(FileHandler)
    key_manager = providers.Factory(
        KeyManager,
        file_handler=file_handler,
    )

    # Business logic services
    cleaner = providers.Factory(
        CleanerService,
        file_handler=file_handler,
    )

    encryptor = providers.Factory(
        EncryptorService,
        key_manager=key_manager,
        file_handler=file_handler,
        cleaner=cleaner,
    )

