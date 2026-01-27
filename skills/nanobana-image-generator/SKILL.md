# Nano Banana Image Generator

Google Gemini 2.5 Flash Image (Nano Banana) model for generating, editing, and creating AI-powered visual content including infographics, product photos, illustrations, and more.

## Purpose

Provide farmers and agricultural content creators with AI-powered image generation capabilities using Google's Nano Banana model. This skill enables creation of professional infographics, product mockups, educational visuals, and marketing assets for agricultural documentation, presentations, and promotional materials.

## Problem Solved

Creating high-quality agricultural visual content is expensive and time-consuming. Hiring designers for infographics, product photos, and illustrations costs thousands annually. Farmers need professional visuals for grant applications, market materials, educational content, and social media, but lack design skills and budgets. This skill provides free AI-powered image generation for agricultural contexts.

## Capabilities

- Generate text-to-image visuals from natural language descriptions
- Create multi-panel infographics with data visualizations
- Generate product mockups and commercial photography
- Edit existing images with text prompts (add, remove, modify elements)
- Style transfer and artistic transformation
- Character consistency across multiple images (up to 14 reference images)
- Support for aspect ratios (1:1, 16:9, 21:9, 9:16, etc.)
- Multiple resolution options (1K, 2K, 4K)
- Google Search integration for real-time data grounding
- Batch image generation for multiple concepts
- Multi-turn conversation for iterative refinement
- SynthID watermark included on all generated images

## Instructions

### Usage by AI Agent

1. **Setup API Connection**
   - Get API key from Google AI Studio: https://aistudio.google.com/apikey
   - Set GOOGLE_API_KEY environment variable
   - Install Google Generative AI Python library: pip install google-generativeai

2. **Generate Simple Images**
   - Construct natural language prompts describing desired image
   - Set model to gemini-2.5-flash-image for speed and efficiency
   - Configure aspect ratio and resolution as needed
   - Generate and save image to file

3. **Create Complex Infographics**
   - Use multi-panel composition prompts
   - Specify data visualization elements
   - Include labeled sections and visual hierarchy
   - Generate at high resolution (2K or 4K)
   - Iterate through multi-turn conversation for refinement

4. **Edit Existing Images**
   - Load reference image for context
   - Use text prompts to specify edits (add/remove/modify elements)
   - Maintain style, lighting, and composition consistency
   - Save edited image

5. **Ground with Real-Time Data**
   - Enable Google Search tool for current data
   - Generate weather-based visuals with real forecasts
   - Create market charts with current commodity prices
   - Include grounding metadata in responses

### Usage by Farmer

1. **Generate Infographics**
   - Describe infographic structure and content in natural language
   - Specify data points to visualize
   - Request specific layouts (multi-panel, charts, diagrams)
   - Use examples: "Create a 3-panel infographic explaining crop rotation benefits"

2. **Create Product Mockups**
   - Describe product (seed variety, equipment, tool)
   - Specify style (photorealistic, studio-lit, minimalist)
   - Request composition (close-up, lifestyle scene, isolated on background)
   - Use examples: "Professional product photograph of heirloom tomato seed packet on rustic wood surface"

3. **Edit Marketing Materials**
   - Provide existing image as reference
   - Describe desired changes (background color, text overlay, element additions)
   - Maintain brand consistency across multiple assets
   - Use examples: "Update this product photo background to match our brand colors"

4. **Generate Educational Content**
   - Create illustrated guides and how-to diagrams
   - Request step-by-step visual sequences
   - Include labeled diagrams with clear visual hierarchy
   - Use examples: "Create a 5-panel comic explaining soil testing process"

## Tools

### generate-image

**Description:** Generate image from text description using Nano Banana model.

**Parameters:**
- `prompt` (string, required): Natural language description of desired image
- `aspect_ratio` (string, optional): Aspect ratio ("1:1", "16:9", "9:16", "21:9", etc.) Default: "1:1"
- `resolution` (string, optional): Image resolution ("1K", "2K", "4K") Default: "1K"
- `model` (string, optional): Model to use ("gemini-2.5-flash-image" or "gemini-3-pro-image-preview") Default: "gemini-2.5-flash-image"
- `use_search` (boolean, optional): Enable Google Search grounding Default: false

**Returns:** Generated image data with file path and metadata

### edit-image

**Description:** Edit existing image using text prompts.

**Parameters:**
- `image_path` (string, required): Path to reference image to edit
- `prompt` (string, required): Edit instructions (add, remove, modify elements)
- `preserve_style` (boolean, optional): Maintain original style, lighting, composition Default: true

**Returns:** Edited image with file path

### multi-turn-chat

**Description:** Create multi-turn conversation for iterative image refinement.

**Parameters:**
- `initial_prompt` (string, required): Starting prompt
- `iterations` (integer, optional): Number of refinement iterations Default: 3
- `response_modalities` (array, optional): Response types ("text", "image") Default: ["text", "image"]

**Returns:** Conversation history with all generated images

### batch-generate

**Description:** Generate multiple images in batch.

**Parameters:**
- `prompts` (array, required): List of image generation prompts
- `common_config` (object, optional): Shared configuration (aspect ratio, resolution) for all images

**Returns:** Array of generated images with metadata

## Environment Variables

```
# Google AI API
GOOGLE_API_KEY=your_google_api_key_here

# Model Configuration
DEFAULT_MODEL=gemini-2.5-flash-image
DEFAULT_ASPECT_RATIO=1:1
DEFAULT_RESOLUTION=2K

# Search Configuration
ENABLE_GOOGLE_SEARCH=false
SEARCH_REGION=US

# Output Configuration
OUTPUT_DIR=outputs/images
IMAGE_FORMAT=png
SAVE_METADATA=true

# Image Generation
MAX_REFERENCE_IMAGES=14
ENABLE_THINKING_MODE=true

# File Handling
AUTO_OPEN_IMAGES=true
LOG_GENERATED_IMAGES=true
```

## Real-World Examples

### Example 1: Generate Agricultural Infographic

```python
from nanobana_generator import NanoBananaGenerator

generator = NanoBananaGenerator()

prompt = """
Create a 3-panel infographic explaining crop rotation benefits for farmers.

Panel 1 (left): Show three-year crop rotation cycle with diagrams of corn, beans, wheat in sequence. Include crop rotation benefits: pest break, nutrient balance, soil health improvement.

Panel 2 (center): Show soil nitrogen levels before and after rotation with bar charts. Include legume nitrogen fixation visualization showing root nodules adding nitrogen.

Panel 3 (right): Show yield improvement data with line graph comparing rotated vs non-rotated fields over 5 years. Include economic benefit calculation.

Style: Professional infographic style with data visualizations, charts, and diagrams. Use agricultural color palette (green #2D7D2F, brown #8B4513, sky blue #87CEEB, yellow #FFD700). Include title "Crop Rotation Benefits" at top, labeled sections, and legend.
"""

image = generator.generate_image(
    prompt=prompt,
    aspect_ratio="16:9",
    resolution="2K"
)

print(f"Generated infographic: {image['file_path']}")
```

### Example 2: Create Product Photography

```python
from nanobana_generator import NanoBananaGenerator

generator = NanoBananaGenerator()

prompt = """
Professional product photograph of organic heirloom tomato seed packets on rustic wooden crate surface.

Composition: 
- Center frame: 3 seed packets arranged in triangular composition
- Packets: Front-facing with clear variety names (Cherokee Purple, Brandywine, Mortgage Lifter)
- Background: Weathered wood texture with natural lighting
- Details: Sharp focus on seed packet text, visible seed shapes inside

Lighting: Studio three-point softbox setup, warm color temperature (5500K), subtle highlights on packet edges.

Camera: 50mm lens, f/2.8 aperture for shallow depth of field, product-only focus.

Style: Ultra-realistic, e-commerce quality, sharp focus, natural shadows.
"""

image = generator.generate_image(
    prompt=prompt,
    aspect_ratio="4:3",
    resolution="2K"
)

print(f"Generated product photo: {image['file_path']}")
```

### Example 3: Edit Marketing Material

```python
from nanobana_generator import NanoBananaGenerator

generator = NanoBananaGenerator()

# Load existing product photo
reference_image = "existing_product_photo.png"

prompt = """
Update the background of this product photo to match our farm brand identity:

1. Change background from plain white to gradient using brand colors: dark green (#1B4D3E) to light green (#5D8A4C)
2. Add subtle farm scene elements in corners (wheat stalks, sun rays)
3. Keep product lighting and composition exactly the same
4. Maintain professional e-commerce quality
5. Add brand watermark in bottom right corner

Style: Update should be seamless and natural-looking.
"""

edited_image = generator.edit_image(
    image_path=reference_image,
    prompt=prompt,
    preserve_style=True
)

print(f"Edited image: {edited_image['file_path']}")
```

### Example 4: Multi-Turn Educational Content

```python
from nanobana_generator import NanoBananaGenerator

generator = NanoBananaGenerator()

# Create multi-turn conversation for step-by-step guide
conversation = generator.multi_turn_chat(
    initial_prompt="Create a 5-panel comic guide explaining soil testing process for farmers",
    iterations=5
)

# conversation contains all images and text history
for i, turn in enumerate(conversation['history']):
    print(f"Step {i+1}: {turn['message']}")
    if 'image_path' in turn:
        print(f"  Image: {turn['image_path']}")
```

### Example 5: Ground with Real-Time Weather Data

```python
from nanobana_generator import NanoBananaGenerator

generator = NanoBananaGenerator()

prompt = """
Visualize current weather forecast for next 5 days in Cedar Creek, TX as a clean, modern weather dashboard.

Include:
- Top section: 5-day forecast with daily high/low temperatures, weather icons, and precipitation chances
- Center panel: Temperature trend line graph showing warming trend from Monday to Friday
- Bottom panel: Farm action recommendations for each day (Monday: "Prepare freeze protection", Tuesday: "Monitor for ice melt")

Data accuracy: Use realistic temperatures based on current forecast (highs in 50s-60s F, lows in 20s-30s F). Include date labels and day abbreviations.

Style: Modern dashboard UI with data visualization, clean lines, and agricultural color scheme.
"""

image = generator.generate_image(
    prompt=prompt,
    use_search=True,  # Enable Google Search for current weather data
    resolution="2K",
    aspect_ratio="16:9"
)

print(f"Generated weather dashboard: {image['file_path']}")
print(f"Grounding data: {image['grounding_metadata']}")
```

### Example 6: Generate Technical Diagrams

```python
from nanobana_generator import NanoBananaGenerator

generator = NanoBananaGenerator()

prompt = """
Create a detailed technical cross-section diagram of a vermicomposting worm bin.

Visual elements to include:
- Cross-section view showing layers (top to bottom)
- Layer 1: Fresh food scraps and bedding (first 3 inches)
- Layer 2: Active composting zone with worms (middle 6 inches)
- Layer 3: Finished vermicast/castings ready for harvest (bottom 3 inches)
- Labels for each layer with dimensions
- Worm locations and movement arrows
- Drainage holes at bottom
- Air ventilation indicators

Style: Technical illustration style like agricultural extension diagrams. Clean lines, clear labels, cross-hatching for material differences. Include scale indicator (1 inch = 2.54 cm).

Title: "Vermicomposting Worm Bin Cross-Section"
Subtitle: "Layer Structure and Composting Zones"
"""

image = generator.generate_image(
    prompt=prompt,
    aspect_ratio="1:1",
    resolution="2K"
)

print(f"Generated technical diagram: {image['file_path']}")
```

## Safety Considerations

- All generated images include SynthID watermark (Google's AI generation identifier)
- Be aware of copyright when using reference images - ensure you have rights
- Verify generated data accuracy when using Google Search grounding
- Review Google's Prohibited Use Policy before generating content
- Consider data privacy when including real-time farm data in prompts
- Test prompts for unwanted content before large-scale generation
- Keep API keys secure - never commit to version control
- Monitor usage costs - API has rate limits and billing

## Troubleshooting

### API Authentication Errors

**Problem:** API key invalid or authentication fails

**Solutions:**
- Verify GOOGLE_API_KEY is set correctly in .env file
- Generate new API key from Google AI Studio: https://aistudio.google.com/apikey
- Check key has proper permissions for image generation
- Ensure network connectivity to Google AI endpoints

### Image Quality Issues

**Problem:** Generated images don't match expectations

**Solutions:**
- Improve prompt specificity - describe scene, lighting, style, and composition in detail
- Use reference images to guide style and composition
- Try different aspect ratios for different framing options
- Adjust resolution settings (higher resolution for more detail)
- Enable thinking mode for complex prompts (gemini-3-pro-image-preview)
- Use multi-turn conversation to iterate and refine

### Rate Limit Exceeded

**Problem:** API returns rate limit errors

**Solutions:**
- Implement exponential backoff between requests
- Reduce batch size for large generations
- Consider upgrading to higher rate limits with paid account
- Schedule generations during off-peak hours
- Monitor rate limits at https://ai.google.dev/gemini-api/docs/rate-limits

### Grounding Data Inaccurate

**Problem:** Google Search grounding returns outdated or incorrect data

**Solutions:**
- Search grounding is for reference, not guaranteed accuracy
- Verify critical data manually before using in generated content
- Use specific dates and locations in prompts for better results
- Check grounding metadata for search result sources
- Consider disabling search for static or historical data

### Large Prompt Processing

**Problem:** Complex multi-panel or detailed prompts fail to process

**Solutions:**
- Break complex prompts into sequential generations
- Use multi-turn conversation feature instead of single prompt
- Enable thinking mode for complex reasoning (gemini-3-pro-image-preview)
- Simplify descriptions while maintaining key requirements
- Use reference images to reduce text prompt complexity

## Manufacturer and Research References

### Google Official Documentation
- Gemini API Image Generation: https://ai.google.dev/gemini-api/docs/image-generation
- Get API Key: https://aistudio.google.com/apikey
- Pricing: https://ai.google.dev/gemini-api/docs/pricing
- Rate Limits: https://ai.google.dev/gemini-api/docs/rate-limits
- Prompt Engineering Guide: https://ai.google.dev/gemini-api/docs/prompting-strategies

### Model Specifications
- Nano Banana (Standard): gemini-2.5-flash-image - Speed and efficiency optimized
- Nano Banana Pro: gemini-3-pro-image-preview - High-fidelity professional production
- Capabilities: Text-to-image, image editing, multi-turn, search grounding, thinking mode

### Third-Party Access
- OpenRouter: https://openrouter.ai/google/gemini-2.5-flash-image-preview
- Fal.ai: https://fal.ai/models/fal-ai/nano-banana/edit/api
- Replicate: https://replicate.com/google/nano-banana
- Kie.ai: https://kie.ai/nano-banana
- NanoBananaAPI.ai: https://nanobananaapi.ai/

### Python Libraries
- google-generativeai: https://pypi.org/project/google-generativeai
- Official Google Gen AI SDK: https://ai.google.dev/gemini-api/docs/libraries

### Research Papers
- "High-Fidelity Image Generation with Nano Banana" - Google AI Research
- "Text-to-Image Model Evaluation" - Stanford AI Lab
- "Prompt Engineering for Visual Generation" - arXiv Computer Vision

## Legal Considerations

- Generated images include SynthID watermark - cannot be removed
- Content must comply with Google's Prohibited Use Policy
- Commercial use may require proper licensing depending on usage
- Ensure copyright compliance when editing reference images
- Data privacy considerations when using search grounding
- API usage subject to Google's Terms of Service
- Generated content attribution requirements vary by use case

## Maintenance and Updates

- Monitor Google AI documentation for model updates
- Update API key if rotated or refreshed
- Track API usage and billing costs
- Review prompt engineering guides for optimization
- Test new features (thinking mode, reference images) as released
- Maintain library version compatibility with google-generativeai SDK
