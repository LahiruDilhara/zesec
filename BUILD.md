# Building Zesec Executables

This document explains how to build Zesec executables for different platforms.

## Prerequisites

1. Python 3.8 or higher
2. All dependencies from `requirements.txt`
3. PyInstaller: `pip install pyinstaller`

## Local Build

### Build all executables

```bash
pyinstaller zesec.spec --clean --noconfirm
```

This will create:
- `dist/zesec` (Linux/macOS) or `dist/zesec.exe` (Windows) - Console executable
- `dist/zesec-gui` (Linux/macOS) or `dist/zesec-gui.exe` (Windows) - GUI executable
- `dist/zesec-gui.app` (macOS only) - macOS app bundle

### Build console only

```bash
pyinstaller --name=zesec --onefile --console --icon=img/icon.png zesec_console.py
```

### Build GUI only

```bash
pyinstaller --name=zesec-gui --onefile --windowed --icon=img/icon.png zesec_gui.py
```

## Icon Format

The build process uses `img/icon.png` as the application icon. For best results:

- **Windows**: Convert PNG to ICO format (optional, PNG works)
- **macOS**: Convert PNG to ICNS format (optional, PNG works)
- **Linux**: PNG works directly

You can use online converters or tools like:
- `png2ico` (Windows)
- `iconutil` (macOS, built-in)
- `imagemagick` (cross-platform)

## GitHub Actions

The project includes a GitHub Actions workflow (`.github/workflows/build-release.yml`) that automatically builds executables for all platforms when:

1. A new release is created
2. The workflow is manually triggered

### Manual Trigger

1. Go to Actions tab in GitHub
2. Select "Build and Release" workflow
3. Click "Run workflow"
4. Optionally specify a version tag

### Release Process

1. Create a new release in GitHub (tag format: `v1.0.0`)
2. GitHub Actions will automatically:
   - Build executables for Linux, Windows, and macOS
   - Upload them to the release page
   - Create compressed archives

## Troubleshooting

### Import Errors

If you encounter import errors, add missing modules to `hiddenimports` in `zesec.spec`.

### Icon Not Showing

- Ensure `img/icon.png` exists
- For Windows, try converting to `.ico` format
- For macOS, try converting to `.icns` format

### Large Executable Size

This is normal for PyInstaller executables. They include Python interpreter and all dependencies. Use UPX compression (already enabled in spec file) to reduce size.

### macOS Code Signing

For distribution outside the App Store, you may need to code sign the macOS app:

```bash
codesign --deep --force --verify --verbose --sign "Developer ID Application: Your Name" dist/zesec-gui.app
```

