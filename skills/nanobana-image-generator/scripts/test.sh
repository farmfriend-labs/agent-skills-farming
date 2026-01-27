#!/bin/bash
# Test script for Nano Banana Image Generator

set -e

echo "Testing Nano Banana Image Generator..."
echo ""

# Activate virtual environment if exists
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "Virtual environment activated"
else
    echo "Error: Virtual environment not found"
    echo "Run ./scripts/setup.sh first"
    exit 1
fi

# Check API key
if [ ! -f .env ]; then
    echo "Error: .env file not found"
    echo "Copy .env.example to .env and add your Google API key"
    exit 1
fi

# Load environment variables
export $(cat .env | xargs)

if [ -z "$GOOGLE_API_KEY" ]; then
    echo "Error: GOOGLE_API_KEY not set in .env"
    exit 1
fi

echo "API key found"
echo ""

# Test 1: Simple image generation
echo "Test 1: Simple image generation"
python scripts/generator.py \
    --prompt "A red barn in a green wheat field at sunset" \
    --aspect-ratio "16:9" \
    --resolution "1K"

if [ $? -eq 0 ]; then
    echo "Test 1: PASSED"
else
    echo "Test 1: FAILED"
fi

echo ""

# Test 2: Square image
echo "Test 2: Square aspect ratio"
python scripts/generator.py \
    --prompt "Organic heirloom tomatoes on rustic wooden surface" \
    --aspect-ratio "1:1" \
    --resolution "2K"

if [ $? -eq 0 ]; then
    echo "Test 2: PASSED"
else
    echo "Test 2: FAILED"
fi

echo ""

# Test 3: Vertical image
echo "Test 3: Vertical aspect ratio for social media"
python scripts/generator.py \
    --prompt "Vertical smartphone photo of field of sunflowers" \
    --aspect-ratio "9:16" \
    --resolution "2K"

if [ $? -eq 0 ]; then
    echo "Test 3: PASSED"
else
    echo "Test 3: FAILED"
fi

echo ""
echo "All tests complete!"
echo ""
echo "Generated images in outputs/images/"
