# Changelog

## [v2.0.1]
### 🌟 Enhancements & Fixes
- **Cancellation Feature:** Added a cancel button to the GUI to safely abort ongoing batch file processing.
- **Performance Fix:** Resolved a GUI freezing issue that occurred when processing a large number of files.
- **Bug Fix:** Fixed an issue where Linux application icons were not loading correctly.

## [v2.0.0] - Architecture & Build System Upgrade

This major release overhauls the core architecture, transitioning to native compilation and introducing robust distribution packages.

### 🌟 Major Upgrades
- **Nuitka Compiler Migration:** Upgraded the entire build system from PyInstaller to Nuitka for optimized, native application compilation, resulting in faster startup times and more stable standalone binaries.
- **Dual Binary Architecture:** Separated the CLI and GUI into independent, pure entry points. This natively prevents background terminal flashes for GUI users on Windows (`CREATE_NO_WINDOW`) while preserving standard console behavior for CLI usage.
- **Cross-Platform Native Installers:** Implemented robust, automated build pipelines for generating complete distribution packages, including Windows MSI (via WiX), Windows EXE (via Inno Setup), and macOS `.app` bundles.
- **File Type Associations:** Implemented native OS file associations globally across Windows, Linux, and macOS, allowing double-click functionality for `.zesec` encrypted files.
- **UI & Layout Refinements:** Extracted modern icon buttons with precise styling, improved MultiFileSelector layouts with fixed scrollable lists, and resolved tooltip and icon rendering issues.

## [v1.2.0] - Advanced Workflow & CLI Update

This update significantly enhances the batch processing workflows, command-line user experience, and GUI data management capabilities of Zesec.

### 🌟 New Features & Enhancements

#### 1. Workflow & Data Management
- **Destination Targeting:** Both the GUI and CLI now natively enforce Destination Directory selection, strictly routing processed output away from your source files for a cleaner workflow.
- **Secure Original Wiper:** You can now instantly toggle a "Securely delete original encrypted file after decryption" option (added `--clean` flag to CLI). The app will securely wipe the source file immediately upon successful decryption.
- **Dynamic File Management:** The GUI multi-file selector lists now feature custom red background SVG bin icons for intuitive single-item removal, along with a convenient "Clear All" button.
- **Window Scaling Adjustments:** Increased the default minimum height of the application to comfortably fit the new destination directory selectors and options checkboxes without immediate scrolling.

#### 2. Advanced CLI & Console Experience
- **Smart Path Autocompletion:** Developed a custom `ZesecCompleter` that contextually switches behavior. It autocompletes CLI commands natively, and smartly transitions to full system directory/file path autocompletion the moment a space is typed.
- **Global Help Routing:** Revamped the command parser to globally intercept `--help` and `-h` flags, instantly printing rich, formatted help menus for any command along with their respective sub-flags.
- **Unified Progress Bars:** Cleaned up the CLI execution visual flow by replacing individual, nested file progress bars with a single, perfectly smooth overall progress bar spanning all batch operations. Failed operations are now summarized silently at the end.
- **Silent Mode (Logging):** Introduced `.env` support (`ENABLE_LOGS`) to toggle internal debug traces. PyInstaller production builds and default executions are now entirely silent, ensuring a pristine console output.

#### 3. GUI Usability Fixes
- **Visual Password Validation:** Password confirmation fields now feature real-time color-coded indicator circles (turning green when passwords match) and descriptive text feedback for maximum confidence before encrypting.

---
*Generated for Zesec version update.*
