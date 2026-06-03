#!/bin/bash
set -e

mkdir -p dist

# Ensure VERSION and ARCH are set
if [ -z "$VERSION" ]; then
    echo "VERSION environment variable is not set."
    exit 1
fi
if [ -z "$ARCH" ]; then
    echo "ARCH environment variable is not set."
    exit 1
fi

echo "Packaging for Linux (ARCH: $ARCH, VERSION: $VERSION)"

# Install nfpm if not installed
if ! command -v nfpm &> /dev/null; then
    echo 'deb [trusted=yes] https://repo.goreleaser.com/apt/ /' | sudo tee /etc/apt/sources.list.d/goreleaser.list
    sudo apt-get update
    sudo apt-get install -y nfpm
fi

# Create nfpm packages
cd package/linux
nfpm pkg --packager deb --target ../../dist/zesec_${VERSION}_${ARCH}.deb
nfpm pkg --packager rpm --target ../../dist/zesec_${VERSION}_${ARCH}.rpm
cd ../..

# Create standalone tar.gz
if [ -f main.bin ]; then
    tar -czvf dist/zesec-linux-${ARCH}.tar.gz main.dist main.bin
else
    tar -czvf dist/zesec-linux-${ARCH}.tar.gz main.dist main
fi
