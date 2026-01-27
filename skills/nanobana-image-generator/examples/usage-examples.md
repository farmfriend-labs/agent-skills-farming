# Nano Banana Image Generator - Usage Examples

## Example 1: Simple Image Generation

Generate a basic agricultural scene:

```bash
./scripts/run.sh --prompt "A red barn in a green wheat field at sunset" \
  --aspect-ratio "16:9" \
  --resolution "2K"
```

## Example 2: Product Photography

Create professional product photo:

```bash
./scripts/run.sh --prompt "Professional product photograph of organic heirloom tomato seed packets on rustic wooden surface" \
  --aspect-ratio "4:3" \
  --resolution "2K"
```

## Example 3: Educational Infographic

Generate multi-panel infographic:

```bash
./scripts/run.sh --prompt "Create a 3-panel infographic explaining crop rotation benefits:
- Panel 1: Show three-year crop rotation cycle (corn, beans, wheat)
- Panel 2: Show soil nitrogen levels before and after rotation
- Panel 3: Show yield improvement data over 5 years
Style: Professional infographic with charts and diagrams" \
  --aspect-ratio "21:9" \
  --resolution "2K"
```

## Example 4: Vertical Social Media

Generate vertical image for Instagram/Reels:

```bash
./scripts/run.sh --prompt "Vertical smartphone photo of field of sunflowers in golden hour" \
  --aspect-ratio "9:16" \
  --resolution "2K"
```

## Example 5: Technical Diagram

Create technical illustration:

```bash
./scripts/run.sh --prompt "Technical cross-section diagram of vermicomposting worm bin showing:
- Layer 1: Fresh food scraps and bedding (first 3 inches)
- Layer 2: Active composting zone with worms (middle 6 inches)
- Layer 3: Finished vermicast/castings (bottom 3 inches)
Include labels and scale indicator" \
  --aspect-ratio "1:1" \
  --resolution "2K"
```

## Example 6: Batch Generation

Generate multiple images at once:

```bash
# Create prompts.json file
cat > prompts.json << EOF
[
  "Close-up of organic tomato seeds in hand",
  "Field of corn at sunrise with dew",
  "Tractor working in wheat field",
  "Farmer checking soil moisture"
]
EOF

./scripts/run.sh --batch prompts.json
```

## Example 7: Multi-Turn Refinement

Iterative refinement through conversation:

```bash
./scripts/run.sh --prompt "Create a diagram of compost bin with layers" \
  --multi-turn 5
```

This creates 5 turns of refinement, each building on previous output.

## Example 8: Edit Existing Image

Modify an existing image:

```bash
# Edit product photo background
./scripts/run.sh --edit "existing_product.png" \
  --prompt "Change background to brand gradient colors, add subtle wheat stalks in corners, keep product focus sharp"
```

## Example 9: Grounded Weather Dashboard

Generate with real-time search grounding:

```bash
./scripts/run.sh \
  --prompt "Visualize weather forecast for next 5 days in Cedar Creek, TX as modern dashboard with daily temperatures and precipitation chances" \
  --use-search \
  --aspect-ratio "16:9" \
  --resolution "2K"
```

The `--use-search` flag enables Google Search grounding for current weather data.

## Example 10: High-Fidelity Pro Model

Use pro model for professional quality:

```bash
./scripts/run.sh --prompt "Ultra-detailed photorealistic close-up of soil structure showing organic matter, mycelium network, and earthworm tunnels" \
  --model "gemini-3-pro-image-preview" \
  --aspect-ratio "4:3" \
  --resolution "4K"
```

## Prompting Tips

### For Infographics
- Specify panel structure explicitly ("3-panel", "left/right/top/bottom")
- Describe data visualizations ("bar chart", "line graph", "pie chart")
- Include labels and legend requirements
- Specify color palette for consistency
- Request clean, professional style

### For Product Photography
- Describe composition (centered, triangular, rule-of-thirds)
- Specify lighting (studio, softbox, natural, golden-hour)
- Include camera settings (f/2.8, 50mm lens)
- Request style (e-commerce, minimalist, lifestyle)
- Mention background details

### For Technical Diagrams
- Specify all elements to include
- Request clear labels and dimensions
- Include scale indicators
- Request diagram style (technical illustration, cross-section)
- Mention reference style (extension agency diagrams)

### For Multi-Turn
- Start with general concept
- Let model refine in subsequent turns
- Provide feedback after each turn
- Request specific additions in later turns

## Output

Generated images are saved to `outputs/images/` directory with filenames:
- `generated_<timestamp>.png` - Single generation
- `edited_<timestamp>.png` - Edited images
- `chat_turn_<number>_<timestamp>.png` - Multi-turn images
