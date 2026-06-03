#!/bin/bash
set -e

mkdir -p dist

if [ -z "$VERSION" ]; then
    echo "VERSION environment variable is not set."
    exit 1
fi
if [ -z "$ARCH" ]; then
    echo "ARCH environment variable is not set."
    exit 1
fi

echo "Packaging for macOS (ARCH: $ARCH, VERSION: $VERSION)"

# Ensure create-dmg is installed
if ! command -v create-dmg &> /dev/null; then
    brew install create-dmg
fi

APP_DIR=$(find . -maxdepth 1 -name "*.app" | head -n 1)
if [ -n "$APP_DIR" ]; then
    # We found the app bundle
    APP_NAME=$(basename "$APP_DIR")
    
    # Add a wrapper to launch with --gui by default when double clicked
    EXEC_PATH="$APP_DIR/Contents/MacOS/main"
    if [ -f "$EXEC_PATH" ]; then
        mv "$EXEC_PATH" "${EXEC_PATH}_bin"
        cat > "$EXEC_PATH" << 'EOF'
#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
"$DIR/main_bin" --gui "$@"
EOF
        chmod +x "$EXEC_PATH"
    fi
    
    # Inject dynamic Version and static Bundle ID into Info.plist for clean upgrade paths
    PLIST_PATH="$APP_DIR/Contents/Info.plist"
    if [ -f "$PLIST_PATH" ]; then
        plutil -replace CFBundleIdentifier -string "com.lahirudilhara.zesec" "$PLIST_PATH" || true
        plutil -replace CFBundleShortVersionString -string "$VERSION" "$PLIST_PATH" || true
        plutil -replace CFBundleVersion -string "$VERSION" "$PLIST_PATH" || true
    fi
    
    # Zip the app bundle
    zip -r "dist/Zesec_${VERSION}_macOS_${ARCH}.zip" "$APP_DIR"
    
    # Create DMG
    create-dmg \
        --volname "Zesec Installer" \
        --window-pos 200 120 \
        --window-size 600 400 \
        --icon-size 100 \
        --icon "$APP_NAME" 200 190 \
        --hide-extension "$APP_NAME" \
        --app-drop-link 400 190 \
        "dist/Zesec_${VERSION}_macOS_${ARCH}.dmg" "$APP_DIR" || true
else
    # Fallback if no .app
    tar -czvf "dist/Zesec_${VERSION}_macOS_${ARCH}.tar.gz" main.dist main.bin
fi
