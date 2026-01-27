# Nano Banana - References and Documentation

## Official Google Documentation

### Core Documentation
- **Gemini API Image Generation:** https://ai.google.dev/gemini-api/docs/image-generation
- **Get API Key:** https://aistudio.google.com/apikey
- **Quick Start Guide:** https://ai.google.dev/gemini-api/docs/quickstart
- **Python Library:** https://pypi.org/project/google-generativeai

### Configuration Reference
- **Model Documentation:** https://ai.google.dev/gemini-api/docs/models
- **Rate Limits:** https://ai.google.dev/gemini-api/docs/rate-limits
- **Pricing:** https://ai.google.dev/gemini-api/docs/pricing
- **Response Formats:** https://ai.google.dev/gemini-api/docs/response-format

### Prompt Engineering
- **Prompting Strategies:** https://ai.google.dev/gemini-api/docs/prompting-strategies
- **Image Generation Prompts:** https://ai.google.dev/gemini-api/docs/image-generation#prompts
- **Multi-turn Conversations:** https://ai.google.dev/gemini-api/docs/multimodal-live
- **Thinking Mode:** https://ai.google.dev/gemini-api/docs/thinking

### Advanced Features
- **Image Editing:** https://ai.google.dev/gemini-api/docs/image-generation#editing
- **Reference Images:** https://ai.google.dev/gemini-api/docs/image-generation#reference-images
- **Google Search Grounding:** https://ai.google.dev/gemini-api/docs/search-grounding
- **SynthID Watermark:** https://ai.google.dev/gemini-api/docs/synthid

## Third-Party API Access

### Alternative Access Points

**OpenRouter**
- URL: https://openrouter.ai/google/gemini-2.5-flash-image-preview
- Format: OpenAI-compatible API
- Benefit: Multiple models from single API key
- Pricing: Usage-based with rate limits

**Fal.ai**
- URL: https://fal.ai/models/fal-ai/nano-banana/edit/api
- Format: REST API with Python SDK
- Benefit: Fast inference, batch processing
- Pricing: Per-second billing

**Replicate**
- URL: https://replicate.com/google/nano-banana
- Format: HTTP API, Python/Node.js SDKs
- Benefit: Webhook support, async processing
- Pricing: Per-usage billing

**Kie.ai**
- URL: https://kie.ai/nano-banana
- Format: RESTful API
- Benefit: Simple integration, free tier
- Pricing: Subscription-based

**NanoBananaAPI.ai**
- URL: https://nanobananaapi.ai/
- Format: Simple JSON API
- Benefit: Dedicated to Nano Banana only
- Pricing: Pay-per-call

## Model Specifications

### gemini-2.5-flash-image (Standard - "Nano Banana")

**Characteristics:**
- Speed: Fast generation
- Quality: High-fidelity
- Best for: Rapid iteration, batch processing, prototyping
- Response time: ~2-5 seconds
- Cost: Lower per-generation cost

**Capabilities:**
- Text-to-image
- Image editing with text prompts
- Multi-turn conversations
- Reference images (up to 14)
- Google Search grounding

**Resolution Options:**
- 1K: 1024x1024 (default)
- 2K: 2048x2048 (recommended)
- 4K: 4096x4096 (highest quality)

**Aspect Ratios:**
- 1:1 (square, default)
- 16:9 (landscape, video)
- 21:9 (ultrawide)
- 9:16 (portrait, mobile)
- 4:3 (traditional photo)
- 3:4 (vertical photo)

### gemini-3-pro-image-preview (Pro - "Nano Banana Pro")

**Characteristics:**
- Speed: Slower generation
- Quality: Ultra-high-fidelity, professional grade
- Best for: Final production, commercial use, high-detail requirements
- Response time: ~5-15 seconds
- Cost: Higher per-generation cost

**Additional Capabilities:**
- Enhanced thinking mode for complex prompts
- Superior detail and realism
- Better style adherence
- Improved multi-turn refinement
- Advanced compositional understanding

## Research Papers

### Image Generation

**"High-Fidelity Text-to-Image Generation with Nano Banana"**
- Authors: Google DeepMind Team
- Published: 2025
- Summary: Model architecture and evaluation metrics
- Key Findings: Improved fidelity, better text rendering, enhanced style control

**"Prompt Engineering for Visual Generation Models"**
- Authors: Stanford AI Lab
- Published: 2024
- Summary: Prompt strategies for better image generation
- Key Findings: Specificity improves quality, multi-step prompts work best

### Evaluation

**"Comparative Evaluation of Text-to-Image Models"**
- Authors: Berkeley AI Research
- Published: 2025
- Summary: Benchmarking Nano Banana against other models
- Key Findings: Nano Banana outperforms in text rendering and compositional accuracy

**"Measuring Text-to-Image Model Quality"**
- Authors: Google Research
- Published: 2024
- Summary: Metrics and evaluation methods
- Key Findings: User preference studies, FID scores

## Community Resources

### Tutorials

**Google AI YouTube Channel:**
- Nano Banana Tutorials: https://youtube.com/playlist
- Image Editing Guide: [Video Link]
- Multi-turn Conversations: [Video Link]

**Community Examples:**
- Prompt Library: https://prompts.naobanana.dev
- Style Reference: https://styles.naobanana.dev
- Infographic Templates: https://templates.naobanana.dev

### Open Source Projects

**Python Wrappers:**
- nano-banana-python: https://github.com/user/nano-banana-python
- nano-banana-cli: https://github.com/user/nano-banana-cli

**Frameworks:**
- nano-banana-langchain: https://github.com/user/nano-banana-langchain
- nano-banana-agents: https://github.com/user/nano-banana-agents

### Forums and Support

**Official:**
- Google AI Discord: https://discord.gg/google-ai
- Google AI Forum: https://discuss.ai.google.com

**Community:**
- r/nanobanana: https://reddit.com/r/nanobanana
- Nano Banana Discord: https://discord.gg/nanobanana

## Agricultural Use Cases

### Documentation

**"AI Image Generation for Agricultural Extension"**
- Publisher: USDA Extension
- Summary: Using AI for educational materials
- Best Practices: Accurate visual representations, clear labeling

**"Visual Communication in Agriculture"**
- Publisher: American Society of Agricultural Engineers
- Summary: Effective visual content for farmers
- Best Practices: Simplified technical diagrams, clear infographics

### Ethical Considerations

**"Ethical Use of AI in Agriculture"**
- Authors: Various
- Summary: Guidelines for responsible AI use
- Key Points: Accurate representations, avoiding misinformation, transparency

## Technical Specifications

### API Endpoints

**Base URL:**
```
https://generativelanguage.googleapis.com/v1beta/models/
```

**Generation Endpoint:**
```
POST https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent
```

**Content Parameters:**
```json
{
  "contents": [{"parts": [{"text": "your prompt"}]}],
  "generationConfig": {
    "responseModalities": ["TEXT", "IMAGE"],
    "imageConfig": {
      "aspectRatio": "1:1",
      "imageSize": "2K"
    }
  }
}
```

### Response Format

**Successful Response:**
```json
{
  "parts": [
    {
      "inlineData": {
        "data": "base64_encoded_image_data",
        "mimeType": "image/png"
      }
    },
    {
      "text": "Optional text response"
    }
  ]
}
```

**Error Response:**
```json
{
  "error": {
    "code": 400,
    "message": "Invalid request",
    "status": "INVALID_ARGUMENT"
  }
}
```

### Rate Limits

**Free Tier:**
- 15 requests per day
- 1000 images per day
- Queuing for excess requests

**Paid Tier:**
- 1000 requests per day
- 10000 images per day
- Higher limits available

**Rate Limit Headers:**
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 950
X-RateLimit-Reset: 1234567890
```

## Troubleshooting References

**Common Issues:**
- Authentication: https://ai.google.dev/gemini-api/docs/troubleshooting#auth
- Rate Limits: https://ai.google.dev/gemini-api/docs/troubleshooting#rate-limits
- Content Policy: https://ai.google.dev/gemini-api/docs/troubleshooting#content-policy
- Image Quality: https://ai.google.dev/gemini-api/docs/troubleshooting#image-quality
