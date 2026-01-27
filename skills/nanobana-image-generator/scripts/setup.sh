#!/bin/bash
# Setup script for Nano Banana Image Generator

set -e

echo "Setting up Nano Banana Image Generator..."

# Check for API key
if [ ! -f .env ]; then
    echo "Creating .env from .env.example"
    cp .env.example .env
    echo ""
    echo "IMPORTANT: Please set your Google API key in .env file"
    echo "1. Get API key from: https://aistudio.google.com/apikey"
    echo "2. Edit .env and add: GOOGLE_API_KEY=your_api_key_here"
    echo ""
    echo "Then run: source .env"
else
    echo ".env file already exists"
fi

# Create Python virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install google-generativeai Pillow

# Create output directories
mkdir -p outputs/images
mkdir -p logs

# Check API key after setup
if [ -f .env ]; then
    source .env
    if [ -z "$GOOGLE_API_KEY" ]; then
        echo ""
        echo "WARNING: GOOGLE_API_KEY not set in .env"
        echo "Please edit .env file and add your API key"
    else
        echo "GOOGLE_API_KEY is set"
    fi
fi

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. If not set, edit .env and add your Google API key"
echo "2. Run: source venv/bin/activate"
echo "3. Test: python scripts/generator.py --prompt 'A farm sunset over wheat fields'"
