#!/bin/bash
set -e

echo "Installing Nuitka and dependencies..."
pip install nuitka zstandard imageio

echo "Compiling Zesec with Nuitka..."
# Create the build directory if it doesn't exist
mkdir -p build

echo "Compiling Zesec Console edition..."
PYTHONPATH=src python -m nuitka \
    --assume-yes-for-downloads \
    --include-package=zesec \
    --output-dir=build \
    --output-filename=zesec \
    src/zesec_console.py

echo "Compiling Zesec GUI edition..."
PYTHONPATH=src python -m nuitka \
    --assume-yes-for-downloads \
    --include-package=zesec \
    --windows-console-mode=disable \
    --macos-disable-console \
    --output-dir=build \
    --output-filename=zesec-gui \
    src/zesec_gui.py

echo "Build complete! Executables are located in the ./build directory"