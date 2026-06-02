# Release Notes: Zesec Modernization Update

This major update introduces a modernized user interface, enhances security protocols, and dramatically improves workflow efficiency by bringing batch-processing capabilities to both the GUI and the Command Line Interface.

## 🌟 Key Features & Improvements

### 1. Modernized GUI & Theming
- **Brand New UI Theme:** Fully redesigned the application with a highly professional, trustworthy **light blue (`#3498db`) and white** aesthetic.
- **Enhanced Components:** Overhauled QSS styling for all primary elements, including dynamic hover states for table rows, custom-rounded scrollbars without arrows, and unified action buttons.
- **Premium Checkboxes:** Replaced standard dull checkboxes with custom-drawn SVG checkmarks that feature a distinct inner blue fill, white gap, and a solid blue outer border for perfect visibility.
- **Responsive Layout:** The application window is now fully maximizable and stretchable. The multi-file selection lists will automatically scale their height dynamically when the window grows.

### 2. Multi-File Batch Processing
- **GUI Multi-File Support:** Replaced the single-file inputs with a completely custom `MultiFileSelectorWidget`. You can now select as many files as you want for both Encryption and Decryption. Duplicate selections are automatically filtered.
- **CLI Batch Operations:** Upgraded the `encrypt` and `decrypt` terminal commands to accept multiple file paths in a single execution (`zesec.console encrypt file1.txt file2.jpg`). 
- **Sequential Execution:** Batch processes now iterate file-by-file sequentially, maintaining progress feedback and providing a comprehensive summary once all files are successfully processed. 

### 3. Security Enhancements
- **Password Confirmation:** Added strict password confirmation (re-type validation) for the encryption processes in both the Graphical Interface and the Terminal commands, mitigating the risk of accidental lockouts due to typos.
- **Smart Validation Validation:** Action buttons in the GUI intelligently disable until all required inputs (Files + Passwords/Keys) are provided.

### 4. Usability Fixes
- **Ctrl+W Shortcut:** You can now safely and instantly close the GUI window by pressing `Ctrl+W`.
- **Ctrl+C Interrupt:** Fixed a common PySide6 quirk. Pressing `Ctrl+C` in the terminal running the GUI will now smoothly and cleanly close the application.
- **Key File Validation:** CLI scripts now correctly throw descriptive errors if a provided Key File path does not exist.

---
*Generated for Zesec version update.*
