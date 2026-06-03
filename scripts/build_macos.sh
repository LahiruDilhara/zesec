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

APP_DIR=$(find build -maxdepth 1 -name "*.app" | head -n 1)
if [ -n "$APP_DIR" ]; then
    # Rename to Zesec.app so the user sees a clean name instead of zesec-gui
    if [ "$APP_DIR" != "build/Zesec.app" ]; then
        mv "$APP_DIR" "build/Zesec.app"
        APP_DIR="build/Zesec.app"
    fi
    APP_NAME=$(basename "$APP_DIR")
    
    # Add a wrapper to launch with --gui by default when double clicked
    EXEC_PATH="$APP_DIR/Contents/MacOS/zesec-gui"
    if [ -f "$EXEC_PATH" ]; then
        EXEC_BASENAME=$(basename "$EXEC_PATH")
        mv "$EXEC_PATH" "${EXEC_PATH}_bin"
        cat > "$EXEC_PATH" << EOF
#!/bin/bash
DIR="\$( cd "\$( dirname "\${BASH_SOURCE[0]}" )" && pwd )"
"\$DIR/${EXEC_BASENAME}_bin" --gui "\$@"
EOF
        chmod +x "$EXEC_PATH"
    fi
    
    # Bundle the console executable inside the App bundle so it is distributed
    mkdir -p "$APP_DIR/Contents/MacOS"
    if [ -f "build/zesec" ]; then
        cp "build/zesec" "$APP_DIR/Contents/MacOS/zesec"
        chmod +x "$APP_DIR/Contents/MacOS/zesec"
    elif [ -f "build/zesec.bin" ]; then
        cp "build/zesec.bin" "$APP_DIR/Contents/MacOS/zesec"
        chmod +x "$APP_DIR/Contents/MacOS/zesec"
    fi
    
    # Inject dynamic Version and static Bundle ID into Info.plist for clean upgrade paths
    PLIST_PATH="$APP_DIR/Contents/Info.plist"
    if [ -f "$PLIST_PATH" ]; then
        plutil -replace CFBundleIdentifier -string "com.lahirudilhara.zesec" "$PLIST_PATH" || true
        plutil -replace CFBundleShortVersionString -string "$VERSION" "$PLIST_PATH" || true
        plutil -replace CFBundleVersion -string "$VERSION" "$PLIST_PATH" || true
        
        # Add file association for .zesec files to macOS Launch Services
        plutil -insert CFBundleDocumentTypes -array "$PLIST_PATH" || true
        plutil -insert CFBundleDocumentTypes.0 -dictionary "$PLIST_PATH" || true
        plutil -insert CFBundleDocumentTypes.0.CFBundleTypeName -string "Zesec Encrypted File" "$PLIST_PATH" || true
        plutil -insert CFBundleDocumentTypes.0.CFBundleTypeExtensions -array "$PLIST_PATH" || true
        plutil -insert CFBundleDocumentTypes.0.CFBundleTypeExtensions.0 -string "zesec" "$PLIST_PATH" || true
        plutil -insert CFBundleDocumentTypes.0.CFBundleTypeRole -string "Editor" "$PLIST_PATH" || true
        plutil -insert CFBundleDocumentTypes.0.LSHandlerRank -string "Owner" "$PLIST_PATH" || true
        plutil -insert CFBundleDocumentTypes.0.CFBundleTypeIconFile -string "icon.icns" "$PLIST_PATH" || true
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
    if [ -f "build/zesec" ] || [ -f "build/zesec-gui" ]; then
        tar -czvf "dist/Zesec_${VERSION}_macOS_${ARCH}.tar.gz" -C build .
    else
        echo "Error: binaries not found in build/"
        exit 1
    fi
fi
