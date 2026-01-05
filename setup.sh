#!/bin/bash
set -e

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "uv is not installed. Please install it first."
    exit 1
fi

echo "Setting up Backend..."
cd backend
# Create venv and install deps
uv venv --python 3.12
source .venv/bin/activate
uv pip install -e .
cd ..

echo "Setting up Frontend..."
cd frontend
npm install
cd ..

echo "Setup complete! You can now run ./start.sh to start the development servers."
