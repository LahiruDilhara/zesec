#!/bin/bash
set -e

echo "Installing Nuitka and dependencies..."
pip install nuitka zstandard imageio

echo "Compiling Zesec with Nuitka..."
# Create the build directory if it doesn't exist
mkdir -p build

PYTHONPATH=src python -m nuitka \
    --assume-yes-for-downloads \
    --include-package=zesec \
    --output-dir=build \
    --output-filename=zesec \
    main.py

echo "Build complete! Executable is located at ./build/zesec"