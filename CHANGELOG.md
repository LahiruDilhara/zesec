# Release Notes: Zesec Advanced Workflow & CLI Update

This update significantly enhances the batch processing workflows, command-line user experience, and GUI data management capabilities of Zesec.

## 🌟 New Features & Enhancements

### 1. Workflow & Data Management
- **Destination Targeting:** Both the GUI and CLI now natively enforce Destination Directory selection, strictly routing processed output away from your source files for a cleaner workflow.
- **Secure Original Wiper:** You can now instantly toggle a "Securely delete original encrypted file after decryption" option (added `--clean` flag to CLI). The app will securely wipe the source file immediately upon successful decryption.
- **Dynamic File Management:** The GUI multi-file selector lists now feature custom red background SVG bin icons for intuitive single-item removal, along with a convenient "Clear All" button.
- **Window Scaling Adjustments:** Increased the default minimum height of the application to comfortably fit the new destination directory selectors and options checkboxes without immediate scrolling.

### 2. Advanced CLI & Console Experience
- **Smart Path Autocompletion:** Developed a custom `ZesecCompleter` that contextually switches behavior. It autocompletes CLI commands natively, and smartly transitions to full system directory/file path autocompletion the moment a space is typed.
- **Global Help Routing:** Revamped the command parser to globally intercept `--help` and `-h` flags, instantly printing rich, formatted help menus for any command along with their respective sub-flags.
- **Unified Progress Bars:** Cleaned up the CLI execution visual flow by replacing individual, nested file progress bars with a single, perfectly smooth overall progress bar spanning all batch operations. Failed operations are now summarized silently at the end.
- **Silent Mode (Logging):** Introduced `.env` support (`ENABLE_LOGS`) to toggle internal debug traces. PyInstaller production builds and default executions are now entirely silent, ensuring a pristine console output.

### 3. GUI Usability Fixes
- **Visual Password Validation:** Password confirmation fields now feature real-time color-coded indicator circles (turning green when passwords match) and descriptive text feedback for maximum confidence before encrypting.

---
*Generated for Zesec version update.*
