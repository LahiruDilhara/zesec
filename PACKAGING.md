# Packaging Guide for Zesec

This guide explains how Zesec is packaged for distribution across Linux, Windows, and macOS platforms.

## Overview

Zesec uses **PyInstaller** to create standalone executables that include:
- Python interpreter
- All dependencies
- Application code
- Application icon

## Files Created

### Build Configuration
- `zesec.spec` - PyInstaller specification file
- `zesec_console.py` - Console entry point for PyInstaller
- `zesec_gui.py` - GUI entry point for PyInstaller

### GitHub Actions
- `.github/workflows/build-release.yml` - Automated build workflow

## Build Process

### Local Build

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install pyinstaller
   ```

2. **Build executables:**
   ```bash
   pyinstaller zesec.spec --clean --noconfirm
   ```

3. **Output location:**
   - `dist/zesec` (Linux/macOS) or `dist/zesec.exe` (Windows)
   - `dist/zesec-gui` (Linux/macOS) or `dist/zesec-gui.exe` (Windows)
   - `dist/zesec-gui.app` (macOS only)

### Automated Build (GitHub Actions)

The GitHub Actions workflow automatically builds for all platforms when:

1. **Creating a Release:**
   - Go to GitHub → Releases → Draft a new release
   - Create a new tag (e.g., `v1.0.0`)
   - Publish the release
   - GitHub Actions will automatically build and attach executables

2. **Manual Trigger:**
   - Go to Actions tab
   - Select "Build and Release" workflow
   - Click "Run workflow"
   - Optionally specify a version

## Platform-Specific Notes

### Linux
- Creates standalone executables
- No additional dependencies required
- Icon: Uses PNG format directly

### Windows
- Creates `.exe` files
- May trigger Windows Defender (false positive - can be reported)
- Icon: PNG works, but `.ico` format is recommended for better integration

### macOS
- Creates `.app` bundle for GUI
- Console executable as standalone binary
- May need code signing for distribution outside App Store
- Icon: PNG works, but `.icns` format is recommended

## Icon Handling

The build process uses `img/icon.png` as the application icon. For best results:

- **Windows**: Convert to `.ico` format (optional)
- **macOS**: Convert to `.icns` format (optional)  
- **Linux**: PNG works directly

### Converting Icons

**Windows (ICO):**
```bash
# Using ImageMagick
convert img/icon.png -define icon:auto-resize=256,128,64,48,32,16 img/icon.ico
```

**macOS (ICNS):**
```bash
# Create iconset directory
mkdir icon.iconset
sips -z 16 16     img/icon.png --out icon.iconset/icon_16x16.png
sips -z 32 32     img/icon.png --out icon.iconset/icon_16x16@2x.png
sips -z 32 32     img/icon.png --out icon.iconset/icon_32x32.png
sips -z 64 64     img/icon.png --out icon.iconset/icon_32x32@2x.png
sips -z 128 128   img/icon.png --out icon.iconset/icon_128x128.png
sips -z 256 256   img/icon.png --out icon.iconset/icon_128x128@2x.png
sips -z 256 256   img/icon.png --out icon.iconset/icon_256x256.png
sips -z 512 512   img/icon.png --out icon.iconset/icon_256x256@2x.png
sips -z 512 512   img/icon.png --out icon.iconset/icon_512x512.png
sips -z 1024 1024 img/icon.png --out icon.iconset/icon_512x512@2x.png
iconutil -c icns icon.iconset -o img/icon.icns
```

## Distribution

### GitHub Releases

When a release is created, the workflow automatically:
1. Builds executables for all platforms
2. Creates compressed archives (tar.gz for Linux/macOS, zip for Windows)
3. Uploads all files to the release page
4. Makes them available for download

### File Structure on Release

```
Release v1.0.0
├── zesec-linux-console.tar.gz
├── zesec-linux-gui.tar.gz
├── zesec-windows-console.zip
├── zesec-windows-gui.zip
├── zesec-macos-console.tar.gz
├── zesec-macos-gui.tar.gz
└── RELEASE_NOTES.txt
```

## Troubleshooting

### Import Errors
If PyInstaller misses some imports, add them to `hiddenimports` in `zesec.spec`.

### Large File Size
Executables are large (50-200MB) because they include Python and all dependencies. This is normal for PyInstaller.

### Antivirus False Positives
Windows Defender may flag PyInstaller executables. This is a known issue. You can:
- Report false positives to Microsoft
- Code sign the executable (requires certificate)
- Use alternative packaging methods

### macOS Gatekeeper
macOS may block unsigned apps. To allow:
1. Right-click the app
2. Select "Open"
3. Click "Open" in the dialog

Or code sign the app for automatic approval.

## Testing Builds

Before releasing, test the executables:

1. **Linux:**
   ```bash
   ./dist/zesec --help
   ./dist/zesec-gui
   ```

2. **Windows:**
   ```cmd
   dist\zesec.exe --help
   dist\zesec-gui.exe
   ```

3. **macOS:**
   ```bash
   ./dist/zesec --help
   open dist/zesec-gui.app
   ```

## Next Steps

1. Test local builds on your development machine
2. Push code to GitHub
3. Create a release tag
4. GitHub Actions will automatically build and publish
5. Download and test the executables from the release page

