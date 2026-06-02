#!/bin/bash
set -e

echo "Installing Nuitka and dependencies..."
pip install nuitka zstandard imageio

echo "Compiling Zesec with Nuitka..."
# Create the build directory if it doesn't exist
mkdir -p build

PYTHONPATH=src python -m nuitka \
    --standalone \
    --onefile \
    --assume-yes-for-downloads \
    --plugin-enable=pyside6 \
    --include-package=zesec \
    --include-data-file=src/zesec/gui/style.qss=zesec/gui/style.qss \
    --include-data-dir=public/svg=public/svg \
    --output-dir=build \
    --output-filename=zesec \
    main.py

echo "Build complete! Executable is located at ./build/zesec"