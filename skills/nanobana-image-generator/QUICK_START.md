# Quick Start Guide - Nano Banana Image Generator

## For TD: How to Generate Images

You can now ask me to generate any type of image, and I'll use the Nano Banana skill to create it.

## Example Requests

### Simple Images
```
"Generate an image of a red barn in a wheat field"
"Create a photo of heirloom tomatoes"
"Make a picture of a tractor working in the fields"
```

### Infographics
```
"Generate a 3-panel infographic explaining crop rotation"
"Create a weather dashboard for Cedar Creek, TX"
"Make a diagram showing how worm composting works"
```

### Product Photography
```
"Generate a professional product photo of seed packets"
"Create a studio shot of organic fertilizer bags"
"Make an e-commerce image of gardening tools"
```

### Custom Sizes
```
"Generate a wide infographic about soil health, 21:9 aspect ratio"
"Create a vertical Instagram image of sunflowers, 9:16 aspect ratio"
"Make a square photo of the farm, 1:1 aspect ratio"
```

## Options You Can Specify

- **Aspect Ratios:** 1:1 (square), 16:9 (landscape), 21:9 (ultrawide), 9:16 (vertical), 4:3 (photo), 3:4 (portrait)
- **Resolution:** 1K (fast), 2K (recommended), 4K (highest quality)

## How It Works

1. You tell me what image you want
2. I call the Nano Banana generator
3. Image is saved to: `/home/scrimwiggins/clawd/skills/nanobana-image-generator/outputs/images/`
4. I tell you the file path and size

## Example Session

You: "Generate an image of a beautiful farm at sunset with a red barn and golden wheat field, wide aspect ratio"

Me:
```
Generating image...
  Model: models/gemini-2.5-flash-image
  Prompt: Generate an image of a beautiful farm at sunset...
  Saved: /home/scrimwiggins/clawd/skills/nanobana-image-generator/outputs/images/generated_1234567890.png
  Size: 2.3 MB

Success! Image created at: /home/scrimwiggins/clawd/skills/nanobana-image-generator/outputs/images/generated_1234567890.png
```

## Technical Details

- Uses Google Gemini 2.5 Flash Image model
- Generates PNG format
- Supports text-to-image, image editing
- API key is local (not shared)
- Images are saved automatically
