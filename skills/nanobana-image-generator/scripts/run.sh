#!/bin/bash
# Run script for Nano Banana Image Generator

set -e

# Activate virtual environment if exists
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "Virtual environment activated"
else
    echo "Warning: Virtual environment not found"
    echo "Run ./scripts/setup.sh first"
fi

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | xargs)
    echo "Environment variables loaded from .env"
else
    echo "Warning: .env file not found"
    echo "Copy .env.example to .env and add your Google API key"
fi

# Check API key
if [ -z "$GOOGLE_API_KEY" ]; then
    echo "Error: GOOGLE_API_KEY not set"
    echo "Get API key from: https://aistudio.google.com/apikey"
    exit 1
fi

# Run generator with all arguments
echo "Starting Nano Banana Image Generator..."
python scripts/generator.py "$@"
