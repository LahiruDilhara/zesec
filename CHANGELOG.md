# Changelog

## [v2.0.1] - Stability and Concurrency Fixes
### 🌟 Enhancements & Fixes
- **Process Cancellation:** Implemented robust GUI process cancellation by adding a dedicated cancel button to the batch operation flows, allowing immediate and safe interruption of running encryption/decryption loops.
- **Asynchronous UI Throttling:** Addressed UI freezing during large file operations by processing pending file paths in the `MultiFileSelectorWidget` using asynchronous chunks (using `QTimer.singleShot`), decoupling heavy file path parsing from the main UI thread.
- **Linux Icon Resolution:** Fixed a rendering bug causing application icons to missing on Linux systems by accurately standardizing Nuitka asset paths.

## [v2.0.0] - Architecture Refactoring & Nuitka Migration

This release involves a deep architectural rewrite of the build system and entry points, moving from PyInstaller to Nuitka for compiled application delivery.

### 🌟 Deep Architectural Changes
- **Nuitka Manifest Configuration:** Completely transitioned build pipelines in `.github/workflows/build-release.yml` and `build.sh`. Migrated configuration directly into `nuitka-project` manifests inside Python entry scripts for native cross-platform compilation.
- **Pure Entry Points (Dual Binary):** Deleted the monolith `main.py` and decoupled the system into `src/zesec_console.py` and `src/zesec_gui.py`. This guarantees Windows GUI execution without hidden terminal allocation (`--windows-console-mode=disable`) while preserving strict console attachment for CLI operations.
- **MacOS App Bundle Improvements:** Modified `scripts/build_macos.sh` to package both the GUI (`zesec-gui`) and the pure CLI binary (`zesec`) side-by-side within the final `.app/Contents/MacOS` directory.
- **Windows WiX Integration:** Injected a `WixUI_InstallDir` GUI installer workflow with the MIT License EULA, and patched WiX's `ProgId` icon resolution to reference `ZesecGUIEXE` directly instead of raw `.ico` files. Added Native OS File Association (`.zesec`) capabilities.

### ✨ GUI Redesign & Optimizations
- **IconButton Extraction:** Created a custom `IconButton` (extending `QPushButton`) with a hand cursor and modern hover/pressed styling (`rgba(149, 165, 166, 0.2)`) and integrated new SVG action icons (Up, Down, Bin).
- **MultiFileSelector Refinements:**
  - Applied robust global styling to list rows: `#2c3e50` text colors, `6px` border-radiuses, and transparent `QListWidget` backgrounds.
  - Implemented `Qt.ElideMiddle` filename clipping on resize events via `QFontMetrics` to maintain grid structure on long file names.
  - Removed standard `QToolTip` tooltips entirely to prevent rendering glitches on Linux Wayland compositors.

## [v1.2.0] - Advanced Workflow & CLI Improvements

A massive overhaul to batch operation routing, CLI experience, and file tracking.

### 🌟 New Features & Enhancements

#### 1. Advanced CLI Tooling (`prompt_toolkit` & `tqdm`)
- **Smart Completion Engine:** Built `ZesecCompleter` leveraging `prompt_toolkit`. It natively autocompletes CLI keywords/subcommands while dynamically switching to a `PathCompleter` the moment a space is typed, ensuring rapid directory targeting.
- **Unified Batch Progress:** Refactored `EncryptCommand` and `DecryptCommand` to ingest multiple file paths via arguments (e.g. `encrypt file1 file2 -d out_dir`). Added a unified `tqdm` progress bar calculating total chunk percentages rather than stacking individual file bars. Failed files are gracefully summarized at the end of the batch process.
- **Global Help Support:** Updated `CommandParser` to natively intercept `-h` and `--help` universally, ensuring proper formatting via `rich` console instead of crashing into unparsed args.
- **Silent Logging Mode:** Added `ENABLE_LOGS` flag to `.env` (via `pydantic-settings`). The `setup_logging` utility now cleanly exits and disables output traces unless explicitly enabled, keeping standard CLI output flawless.

#### 2. Workflow Overhauls
- **Destination Targeting Requirement:** Added the `--dest` (`-d`) flag to `encrypt` and `decrypt` CLI commands as a hard requirement to isolate encrypted data from original source data.
- **Secure File Wiping:** Refactored `EncryptorService` to support a `clean_original` flag. Integrated `--clean` into the CLI to overwrite source files with zero-byte buffers prior to physical deletion. `clean` command now successfully loops over multiple files.
- **GUI Checkboxes & Layouts:** Styled checkboxes and list items to follow modern visual paradigms, shifting from standard dull toggles to custom-drawn SVGs. Expanded the minimum UI height (`40` to `44` px per row) to improve visual breathing room for multi-file batches.

---
*Generated for Zesec version update.*
