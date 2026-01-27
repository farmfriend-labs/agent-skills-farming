#!/usr/bin/env python3
"""
Simple image generation interface - can be called directly from Python
"""
import sys
import os
import base64
import time
import google.generativeai as genai
from pathlib import Path

# Configuration
API_KEY = os.getenv('GOOGLE_API_KEY', 'AIzaSyC2Og7JDCG2jl8Gd_uNaiBpcD8mFZ_aANs')
OUTPUT_DIR = Path('/home/scrimwiggins/clawd/skills/nanobana-image-generator/outputs/images')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Configure API
genai.configure(api_key=API_KEY)


def generate_image(prompt, aspect_ratio='1:1', resolution='2K', model='models/gemini-2.5-flash-image'):
    """
    Generate an image from text prompt.

    Args:
        prompt: Description of image to generate
        aspect_ratio: Aspect ratio (1:1, 16:9, 21:9, 9:16, 4:3, 3:4)
        resolution: Resolution (1K, 2K, 4K)
        model: Model name

    Returns:
        dict: {'file_path': str, 'prompt': str} or None on error
    """
    try:
        print(f"Generating image...")
        print(f"  Model: {model}")
        print(f"  Prompt: {prompt[:100]}...")

        # Create model
        gen_model = genai.GenerativeModel(model)

        # Generate content
        response = gen_model.generate_content(prompt)

        # Extract image from response
        for part in response.parts:
            if hasattr(part, 'inline_data') and part.inline_data:
                if part.inline_data.mime_type and 'image' in part.inline_data.mime_type:
                    # Data is already decoded bytes
                    image_bytes = part.inline_data.data

                    # Save image
                    filename = f"generated_{int(time.time())}.png"
                    filepath = OUTPUT_DIR / filename
                    filepath.write_bytes(image_bytes)

                    file_size_mb = len(image_bytes) / (1024 * 1024)
                    print(f"  Saved: {filepath}")
                    print(f"  Size: {file_size_mb:.2f} MB")

                    return {
                        'file_path': str(filepath),
                        'prompt': prompt,
                        'model': model,
                        'aspect_ratio': aspect_ratio,
                        'resolution': resolution
                    }

        print(f"  Error: No image data in response")
        return None

    except Exception as e:
        print(f"  Error: {e}")
        return None


def edit_image(image_path, edit_prompt):
    """
    Edit an existing image with text prompt.

    Args:
        image_path: Path to image to edit
        edit_prompt: Description of edits to make

    Returns:
        dict: {'file_path': str} or None on error
    """
    try:
        print(f"Editing image: {image_path}")

        # Load reference image
        from PIL import Image
        ref_image = Image.open(image_path)

        # Create model
        gen_model = genai.GenerativeModel('models/gemini-2.5-flash-image')

        # Edit image
        response = gen_model.generate_content([edit_prompt, ref_image])

        # Extract edited image
        for part in response.parts:
            if hasattr(part, 'inline_data') and part.inline_data:
                if part.inline_data.mime_type and 'image' in part.inline_data.mime_type:
                    # Data is already decoded bytes
                    image_bytes = part.inline_data.data

                    # Save edited image
                    filename = f"edited_{int(time.time())}.png"
                    filepath = OUTPUT_DIR / filename
                    filepath.write_bytes(image_bytes)

                    print(f"  Saved: {filepath}")
                    return {
                        'file_path': str(filepath),
                        'original': image_path,
                        'edit_prompt': edit_prompt
                    }

        print(f"  Error: No image data in response")
        return None

    except Exception as e:
        print(f"  Error: {e}")
        return None


if __name__ == "__main__":
    # Command line interface
    import argparse

    parser = argparse.ArgumentParser(description="Simple Image Generation")
    parser.add_argument("--prompt", "-p", required=True, help="Image description")
    parser.add_argument("--aspect-ratio", "-a", default="1:1", help="Aspect ratio")
    parser.add_argument("--resolution", "-r", default="2K", help="Resolution")
    parser.add_argument("--edit", "-e", help="Path to image to edit")
    parser.add_argument("--edit-prompt", help="Edit instruction")

    args = parser.parse_args()

    if args.edit and args.edit_prompt:
        result = edit_image(args.edit, args.edit_prompt)
    else:
        result = generate_image(
            prompt=args.prompt,
            aspect_ratio=args.aspect_ratio,
            resolution=args.resolution
        )

    if result:
        print(f"\nSuccess: {result['file_path']}")
    else:
        print("\nFailed")
        sys.exit(1)
