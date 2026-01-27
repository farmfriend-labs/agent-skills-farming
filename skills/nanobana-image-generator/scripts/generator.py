#!/usr/bin/env python3
"""
Nano Banana Image Generator - Google Gemini 2.5 Flash Image model wrapper
"""
import os
import sys
import logging
import argparse
import json
import base64
import time
from pathlib import Path

try:
    from google import genai
    from google.genai import types
    from PIL import Image
    import io
except ImportError:
    print("Error: Required libraries not installed.")
    print("Run: pip install google-generativeai Pillow")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('NanoBananaGenerator')


class NanoBananaGenerator:
    """Nano Banana Image Generator - Google Gemini 2.5 Flash Image wrapper"""

    def __init__(self):
        """Initialize generator with API key and configuration"""
        self.api_key = os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")

        self.default_model = os.getenv('DEFAULT_MODEL', 'gemini-2.5-flash-image')
        self.default_aspect_ratio = os.getenv('DEFAULT_ASPECT_RATIO', '1:1')
        self.default_resolution = os.getenv('DEFAULT_RESOLUTION', '2K')
        self.output_dir = Path(os.getenv('OUTPUT_DIR', 'outputs/images'))
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize client
        self.client = genai.Client(api_key=self.api_key)
        logger.info(f"NanoBananaGenerator initialized with model: {self.default_model}")

    def generate_image(self, prompt, aspect_ratio=None, resolution=None, model=None, use_search=False):
        """Generate image from text description"""
        model = model or self.default_model
        aspect_ratio = aspect_ratio or self.default_aspect_ratio
        resolution = resolution or self.default_resolution

        logger.info(f"Generating image with model: {model}")
        logger.info(f"Aspect ratio: {aspect_ratio}, Resolution: {resolution}")

        try:
            # Build generation config
            generation_config = types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio=aspect_ratio,
                    image_size=resolution
                )
            )

            # Add search tool if enabled
            if use_search:
                generation_config.tools = [{"google_search": {}}]

            # Generate content
            response = self.client.models.generate_content(
                model=model,
                contents=prompt,
                config=generation_config
            )

            # Extract image from response
            for part in response.parts:
                if part.inline_data:
                    image_data = part.inline_data.data
                    image_bytes = base64.b64decode(image_data)

                    # Save image
                    filename = f"generated_{int(time.time())}.png"
                    filepath = self.output_dir / filename
                    filepath.write_bytes(image_bytes)

                    logger.info(f"Image saved: {filepath}")

                    return {
                        'file_path': str(filepath),
                        'resolution': resolution,
                        'aspect_ratio': aspect_ratio,
                        'model': model,
                        'prompt': prompt
                    }

            return None

        except Exception as e:
            logger.error(f"Generation failed: {e}")
            return None

    def edit_image(self, image_path, prompt, preserve_style=True):
        """Edit existing image using text prompts"""
        logger.info(f"Editing image: {image_path}")

        try:
            # Load reference image
            ref_image = Image.open(image_path)

            # Edit image
            response = self.client.models.generate_content(
                model=self.default_model,
                contents=[prompt, ref_image],
                config=types.GenerateContentConfig(
                    response_modalities=['TEXT', 'IMAGE']
                )
            )

            # Extract edited image
            for part in response.parts:
                if part.inline_data:
                    image_data = part.inline_data.data
                    image_bytes = base64.b64decode(image_data)

                    # Save edited image
                    filename = f"edited_{int(time.time())}.png"
                    filepath = self.output_dir / filename
                    filepath.write_bytes(image_bytes)

                    logger.info(f"Edited image saved: {filepath}")

                    return {
                        'file_path': str(filepath),
                        'original': image_path,
                        'prompt': prompt,
                        'preserve_style': preserve_style
                    }

            return None

        except Exception as e:
            logger.error(f"Edit failed: {e}")
            return None

    def multi_turn_chat(self, initial_prompt, iterations=3):
        """Create multi-turn conversation for iterative image refinement"""
        logger.info(f"Starting multi-turn chat with {iterations} iterations")

        try:
            # Create chat session
            chat = self.client.chats.create(
                model=self.default_model,
                config=types.GenerateContentConfig(
                    response_modalities=['TEXT', 'IMAGE']
                )
            )

            conversation = {
                'initial_prompt': initial_prompt,
                'iterations': iterations,
                'history': []
            }

            # Send initial message
            response = chat.send_message(initial_prompt)
            self._extract_and_save_response(response, 1, conversation['history'])

            # Continue conversation
            for i in range(2, iterations + 1):
                response = chat.send_message("Continue or refine as needed")
                self._extract_and_save_response(response, i, conversation['history'])

            return conversation

        except Exception as e:
            logger.error(f"Multi-turn chat failed: {e}")
            return None

    def _extract_and_save_response(self, response, turn_number, history):
        """Extract and save response from multi-turn chat"""
        turn_data = {'turn': turn_number}

        for part in response.parts:
            if part.text:
                turn_data['message'] = part.text

            elif part.inline_data:
                image_data = part.inline_data.data
                image_bytes = base64.b64decode(image_data)

                filename = f"chat_turn_{turn_number}_{int(time.time())}.png"
                filepath = self.output_dir / filename
                filepath.write_bytes(image_bytes)

                turn_data['image_path'] = str(filepath)
                logger.info(f"Turn {turn_number} image saved: {filepath}")

        history.append(turn_data)

    def batch_generate(self, prompts, common_config=None):
        """Generate multiple images in batch"""
        logger.info(f"Batch generating {len(prompts)} images")

        results = []

        for i, prompt in enumerate(prompts, 1):
            logger.info(f"Generating image {i}/{len(prompts)}")

            result = self.generate_image(
                prompt=prompt,
                aspect_ratio=common_config.get('aspect_ratio') if common_config else None,
                resolution=common_config.get('resolution') if common_config else None,
                model=common_config.get('model') if common_config else None
            )

            if result:
                results.append(result)

        return {
            'total_generated': len(results),
            'images': results
        }


def main():
    parser = argparse.ArgumentParser(description="Nano Banana Image Generator")
    parser.add_argument("--prompt", "-p", required=True, help="Text prompt for image generation")
    parser.add_argument("--aspect-ratio", "-a", help="Aspect ratio (1:1, 16:9, 21:9, etc.)")
    parser.add_argument("--resolution", "-r", help="Resolution (1K, 2K, 4K)")
    parser.add_argument("--model", "-m", help="Model (gemini-2.5-flash-image, gemini-3-pro-image-preview)")
    parser.add_argument("--use-search", "-s", action="store_true", help="Enable Google Search grounding")
    parser.add_argument("--edit", "-e", help="Edit existing image at this path")
    parser.add_argument("--batch", "-b", help="Generate batch from JSON file with prompts array")
    parser.add_argument("--multi-turn", "-t", type=int, help="Multi-turn conversation iterations")
    parser.add_argument("--output", "-o", help="Output directory")

    args = parser.parse_args()

    try:
        generator = NanoBananaGenerator()

        # Batch generation
        if args.batch:
            with open(args.batch, 'r') as f:
                prompts = json.load(f)
            result = generator.batch_generate(prompts)
            print(f"Batch complete: {result['total_generated']} images generated")
            return

        # Multi-turn chat
        if args.multi_turn:
            conversation = generator.multi_turn_chat(args.prompt, args.multi_turn)
            print(f"Multi-turn chat complete: {len(conversation['history'])} turns")
            return

        # Edit existing image
        if args.edit:
            result = generator.edit_image(args.edit, args.prompt)
            if result:
                print(f"Image edited: {result['file_path']}")
            return

        # Simple generation (default)
        result = generator.generate_image(
            prompt=args.prompt,
            aspect_ratio=args.aspect_ratio,
            resolution=args.resolution,
            model=args.model,
            use_search=args.use_search
        )

        if result:
            print(f"Image generated: {result['file_path']}")
            print(f"Model: {result['model']}")
            print(f"Resolution: {result['resolution']}, Aspect: {result['aspect_ratio']}")
        else:
            print("Image generation failed")
            sys.exit(1)

    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
