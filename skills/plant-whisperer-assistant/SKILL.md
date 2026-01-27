# Plant Whisperer Assistant

AI-powered plant health monitoring, diagnosis, and personalized care recommendations for home gardens and small farms.

## Purpose

Empower gardeners and small-scale farmers with expert-level plant knowledge that would normally require decades of horticultural experience. Detect plant stress, diseases, and nutrient deficiencies before they become visible to the naked eye. Receive personalized care recommendations based on your specific plants, growing conditions, and climate zone.

## Problem Solved

Most plant problems are discovered too late—when leaves are yellowing, plants are wilting, or diseases have already spread. Traditional methods rely on reactive observation after damage has occurred. Gardeners without extensive horticultural knowledge struggle with:
- Identifying subtle early warning signs of plant stress
- Differentiating between similar-looking symptoms (nutrient deficiency vs disease vs environmental stress)
- Knowing the right intervention at the right time
- Understanding how environmental factors interact with plant health
- Tracking plant health over time to prevent recurring issues

Plant Whisperer Assistant uses computer vision, pattern recognition, and expert horticultural knowledge bases to proactively identify issues and recommend precise interventions.

## Capabilities

### Visual Analysis
- Leaf color analysis (chlorosis, necrosis, purpling, bronzing)
- Leaf spot identification (size, shape, color, borders)
- Growth pattern analysis (stunting, etiolation, abnormal growth)
- Stem and branch health assessment
- Root system analysis (when visible)
- Flower and fruit development tracking
- Pest damage pattern recognition

### Environmental Monitoring
- Soil moisture recommendations
- Temperature stress detection
- Light requirement matching
- Humidity impact assessment
- Air circulation issues
- Seasonal timing recommendations

### Nutrient Management
- Nitrogen deficiency/excess identification
- Phosphorus deficiency symptoms
- Potassium imbalance detection
- Micronutrient deficiency diagnosis (iron, magnesium, calcium, etc.)
- Fertilizer timing recommendations
- Soil amendment suggestions

### Disease & Pest Detection
- Fungal infection identification (powdery mildew, blight, rust)
- Bacterial disease recognition
- Viral symptom patterns
- Insect damage analysis
- Beneficial insect identification
- Organic treatment recommendations

### Growth Tracking
- Stage-of-growth identification
- Expected development milestones
- Harvest timing predictions
- Pruning recommendations
- Propagation readiness assessment

### Personalized Recommendations
- Species-specific care schedules
- Climate zone adjustments
- Container vs in-ground differences
- Microclimate considerations
- Companion planting suggestions
- Succession planting timing

## Instructions

### Usage by AI Agent

#### 1. Plant Identification and Setup

**Initial Plant Registry:**
- Collect plant data: species, variety, age, location, container size, soil type
- Document planting date, source, and any known issues
- Photograph initial state as baseline
- Determine plant's native habitat and preferred conditions
- Identify climate zone and microclimate factors

**Image Capture Guidelines:**
- Use good lighting (natural daylight preferred)
- Include reference scale (ruler or coin) if possible
- Capture multiple angles: top, underside of leaves, stems
- Include overall plant view and close-up of concerning areas
- Use consistent resolution (minimum 1080p recommended)
- Date and timestamp all images

#### 2. Routine Health Monitoring

**Weekly Checkups:**
1. Capture standardized images from fixed angles
2. Record environmental data (temperature, humidity, soil moisture)
3. Note any visible changes or concerns
4. Compare against baseline images
5. Run diagnostic analysis
6. Document observations and recommendations

**Stress Detection Protocol:**
1. Analyze leaf color for chlorosis patterns
2. Check leaf spots for characteristic patterns
3. Inspect stem and branch integrity
4. Assess growth rate against expectations
5. Evaluate environmental stress factors
6. Cross-reference with known disease/pest patterns
7. Generate severity score and action plan

#### 3. Diagnostic Analysis

**Step-by-Step Diagnosis:**

**A. Symptom Analysis**
- Identify primary symptoms (most obvious issues)
- Note secondary symptoms (related effects)
- Document progression timeline
- Correlate with environmental changes
- Check for pattern consistency across plant

**B. Pattern Recognition**
- Match visual patterns against 50,000+ symptom database
- Compare nutrient deficiency signatures
- Cross-reference disease progression models
- Evaluate pest damage characteristics
- Assess environmental stress indicators

**C. Differential Diagnosis**
- Generate list of potential causes ranked by probability
- Rule out unlikely causes based on context
- Test hypotheses with targeted observations
- Consider comorbidity (multiple issues simultaneously)
- Prioritize acute issues over chronic concerns

**D. Intervention Planning**
- Rank interventions by effectiveness and urgency
- Provide organic and conventional options
- Calculate resource requirements and costs
- Outline expected timeline for improvement
- Set up monitoring checkpoints

#### 4. Treatment Implementation

**Organic-First Approach:**
1. Start with least invasive methods
2. Gradually escalate if needed
3. Document all interventions and outcomes
4. Adjust based on plant response
5. Learn from effectiveness for future cases

**Intervention Categories:**
- Cultural practices (watering, light, temperature adjustment)
- Soil amendments (compost, organic fertilizers)
- Biological controls (beneficial insects, microbes)
- Organic sprays (neem oil, insecticidal soap, copper)
- Last resort: targeted synthetic treatments

#### 5. Long-Term Plant Health Strategy

**Seasonal Planning:**
- Pre-season preparation checklist
- In-season monitoring schedule
- Post-season cleanup and storage
- Overwintering protection
- Dormant season planning

**Preventive Maintenance:**
- Disease prevention protocols
- Pest barrier establishment
- Soil health monitoring
- Nutrient management schedules
- Environmental optimization

**Knowledge Building:**
- Track what works for your specific microclimate
- Document successful interventions
- Build plant history database
- Share learnings with community

## Tools

### Hardware
- **Camera/Smartphone:** Minimum 1080p with good lighting (preferably 4K)
- **Optional Microscope:** For detailed pest/disease examination (60x-200x recommended)
- **Soil Moisture Sensor:** For precise watering recommendations
- **pH Meter:** For soil acidity monitoring
- **Light Meter:** For measuring PAR (photosynthetically active radiation)
- **Weather Station:** Local microclimate monitoring (optional but valuable)

### Software
- **Python 3.8+**: Core analysis engine
- **OpenCV**: Image processing and analysis
- **TensorFlow/PyTorch**: Machine learning models for pattern recognition
- **PlantNet API**: Plant identification verification
- **Trefle API**: Comprehensive plant database
- **OpenWeatherMap API**: Weather data and forecasts
- **USDA Hardiness Zone Database**: Climate zone information
- **SQLite**: Plant health database storage

### Python Libraries
```
opencv-python>=4.8.0
numpy>=1.24.0
pandas>=2.0.0
pillow>=10.0.0
scikit-learn>=1.3.0
scikit-image>=0.21.0
requests>=2.31.0
matplotlib>=3.7.0
seaborn>=0.12.0
tensorflow>=2.13.0  # or torch>=2.0.0
plantnet-client>=0.1.0  # Optional
pyyaml>=6.0
```

## Environment Variables

```bash
# ============================================
# Image Analysis Configuration
# ============================================

# Minimum image resolution for analysis
MIN_IMAGE_WIDTH=1920
MIN_IMAGE_HEIGHT=1080

# Image quality threshold (0-100)
IMAGE_QUALITY_THRESHOLD=70

# Enable AI-powered disease detection
AI_DETECTION_ENABLED=true

# AI model selection (tensorflow, pytorch, local, cloud)
AI_MODEL_TYPE=tensorflow

# Confidence threshold for AI predictions (0.0-1.0)
AI_CONFIDENCE_THRESHOLD=0.75

# ============================================
# Plant Database APIs
# ============================================

# PlantNet API (optional, for plant identification)
PLANTNET_API_KEY=
PLANTNET_API_URL=https://my.api.plantnet.org/v1/identify

# Trefle API (optional, comprehensive plant database)
TREFLE_API_KEY=
TREFLE_API_URL=https://trefle.io/api/v1

# ============================================
# Weather Data
# ============================================

# OpenWeatherMap API for weather data
OPENWEATHER_API_KEY=
OPENWEATHER_API_URL=https://api.openweathermap.org/data/2.5

# Enable weather-based recommendations
WEATHER_INTEGRATION_ENABLED=true

# Default latitude/longitude for weather (optional)
DEFAULT_LATITUDE=
DEFAULT_LONGITUDE=

# ============================================
# Storage and Database
# ============================================

# Plant health database path
PLANT_DB_PATH=/opt/plant-whisperer/plants.db

# Image storage directory
IMAGE_STORAGE_PATH=/opt/plant-whisperer/images

# Maximum image storage size (in GB)
MAX_IMAGE_STORAGE_GB=50

# Database backup interval (in hours)
DB_BACKUP_INTERVAL=24

# ============================================
# Analysis Settings
# ============================================

# Analysis mode: basic, standard, comprehensive
ANALYSIS_MODE=standard

# Include growth stage analysis
GROWTH_STAGE_ANALYSIS=true

# Include nutrient deficiency detection
NUTRIENT_ANALYSIS=true

# Include pest and disease detection
PEST_DISEASE_ANALYSIS=true

# Include environmental stress analysis
ENV_STRESS_ANALYSIS=true

# ============================================
# Alert Configuration
# ============================================

# Enable email alerts
ALERT_EMAIL_ENABLED=false

# Email address for alerts
ALERT_EMAIL=

# SMTP server for email alerts
SMTP_SERVER=
SMTP_PORT=587
SMTP_USERNAME=
SMTP_PASSWORD=

# Alert severity threshold: info, warning, critical
ALERT_SEVERITY_THRESHOLD=warning

# ============================================
# Logging
# ============================================

# Log level: debug, info, warn, error
LOG_LEVEL=info

# Log file path
LOG_FILE=/var/log/plant-whisperer.log

# ============================================
# Recommendation Preferences
# ============================================

# Preferred approach: organic, conventional, balanced
PREFERRED_APPROACH=organic

# Include cost estimates for recommendations
INCLUDE_COST_ESTIMATES=true

# Include difficulty ratings
INCLUDE_DIFFICULTY_RATING=true

# ============================================
# Development and Testing
# ============================================

# Enable debug mode
DEBUG_MODE=false

# Test data directory (for development)
TEST_DATA_DIR=/opt/plant-whisperer/test-data

# Mock API responses for testing
MOCK_API_RESPONSES=false
```

## Plant Health Indicators

### Visual Symptoms Reference

#### Leaf Color Changes

**Chlorosis (Yellowing):**
- General chlorosis: Nitrogen deficiency
- Interveinal chlorosis: Iron, magnesium, manganese deficiency
- Lower leaf chlorosis: Mobile nutrient deficiency (N, P, K, Mg)
- Upper leaf chlorosis: Immobile nutrient deficiency (Fe, Mn, Zn, Cu)

**Necrosis (Dead Tissue):**
- Tip burn: Potassium deficiency, salt stress
- Marginal burn: Potassium deficiency, drought stress
- Intervenal necrosis: Magnesium deficiency
- Spot necrosis: Bacterial/fungal infection, nutrient toxicity

**Purpling:**
- Red/purple leaves: Phosphorus deficiency, cold stress
- Purple undersides: Phosphorus deficiency, anthocyanin accumulation
- Vein purpling: Phosphorus or magnesium deficiency

**Bronzing:**
- Bronze/metallic sheen: Boron toxicity
- Leaf bronzing: Light stress, heat stress

#### Leaf Abnormalities

**Curling and Cupping:**
- Upward curling: Herbicide damage, excessive heat
- Downward curling: Aphids, excessive watering
- Cupping: Herbicide drift, growth regulator exposure

**Wilting:**
- Temporary wilting: Underwatering, heat stress
- Permanent wilting: Overwatering, root rot, vascular wilt
- One-sided wilting: Root damage, stem blockage

**Spotting Patterns:**
- Circular spots with halos: Bacterial spot
- Angular spots: Bacterial infection (limited by veins)
- Irregular brown spots: Fungal leaf spot
- Yellow halo spots: Early fungal infection
- Water-soaked spots: Bacterial soft rot

**Molds and Coatings:**
- White powdery coating: Powdery mildew
- Gray fuzzy growth: Botrytis (gray mold)
- Black sooty coating: Sooty mold (honeydew from insects)
- Downy white growth: Downy mildew
- Rust-colored pustules: Rust fungi

#### Stem and Branch Issues

**Stem Symptoms:**
- Cankers: Dead sections on stems (fungal/bacterial)
- Galls: Swollen growths (insect activity, bacterial crown gall)
- Lesions: Sunken or raised areas (fungal/bacterial)
- Exudation: Sap oozing (bacterial infection, borers)
- Splitting: Rapid growth, freeze damage, mechanical injury

**Growth Patterns:**
- Stunting: Chronic nutrient deficiency, root damage
- Etiolation: Leggy growth, insufficient light
- Abnormal branching: Hormone imbalance, pruning damage
- Witches' broom: Excessive branching (phytoplasma infection)

#### Root Issues (When Visible)

**Root Symptoms:**
- Brown/black roots: Root rot, overwatering
- Stunted roots: Soil compaction, nutrient deficiency
- Knobby roots: Root-knot nematodes
- Swollen roots: Clubroot disease
- Sparse root system: Container-bound, poor soil structure

### Nutrient Deficiency Guide

#### Primary Nutrients

**Nitrogen (N) Deficiency:**
- **Symptoms:** Overall pale green to yellow leaves, starting with older leaves
- **Pattern:** Uniform chlorosis progressing from leaf tips inward
- **Growth Impact:** Stunted growth, reduced leaf size
- **Correction:** Fish emulsion, blood meal, alfalfa meal, compost tea
- **Timeline:** Improvement visible in 3-7 days with soluble nitrogen

**Phosphorus (P) Deficiency:**
- **Symptoms:** Dark green or purple leaves, especially older leaves
- **Pattern:** Purpling of leaf undersides and stems
- **Growth Impact:** Poor root development, delayed maturity
- **Correction:** Bone meal, rock phosphate, fish bone meal
- **Timeline:** Slow improvement (2-4 weeks)

**Potassium (K) Deficiency:**
- **Symptoms:** Yellow/brown leaf margins (scorch), weak stems
- **Pattern:** Marginal chlorosis and necrosis starting on older leaves
- **Growth Impact:** Poor disease resistance, weak stems, reduced fruit quality
- **Correction:** Greensand, kelp meal, wood ash, sulfate of potash
- **Timeline:** Improvement in 1-2 weeks

#### Secondary Nutrients

**Calcium (Ca) Deficiency:**
- **Symptoms:** Blossom end rot (tomatoes), tip burn (lettuce), curled leaves
- **Pattern:** Distortion of new growth, death of growing points
- **Growth Impact:** Poor cell wall structure, reduced fruit quality
- **Correction:** Gypsum, lime (if pH is low), eggshell powder
- **Timeline:** Improvement in new growth within 1-2 weeks

**Magnesium (Mg) Deficiency:**
- **Symptoms:** Interveinal chlorosis on older leaves
- **Pattern:** Green veins with yellow tissue between
- **Growth Impact:** Reduced photosynthesis, poor fruit quality
- **Correction:** Epsom salts (magnesium sulfate), dolomite lime
- **Timeline:** Improvement in 5-10 days

**Sulfur (S) Deficiency:**
- **Symptoms:** Uniform yellowing of new growth (similar to nitrogen but starts on new leaves)
- **Pattern:** Light green leaves, sometimes reddish tint
- **Growth Impact:** Stunted growth, reduced protein synthesis
- **Correction:** Elemental sulfur, gypsum, compost
- **Timeline:** Improvement in 1-2 weeks

#### Micronutrients

**Iron (Fe) Deficiency:**
- **Symptoms:** Interveinal chlorosis on new growth
- **Pattern:** Veins remain green, tissue between turns yellow/white
- **Growth Impact:** Severe stunting in extreme cases
- **Correction:** Chelated iron, iron sulfate, compost
- **Timeline:** Improvement in new growth within 3-7 days

**Manganese (Mn) Deficiency:**
- **Symptoms:** Interveinal chlorosis with dark green spots
- **Pattern:** Yellow areas between veins with necrotic spots
- **Growth Impact:** Reduced growth, poor fruit set
- **Correction:** Manganese sulfate, compost
- **Timeline:** Improvement in 1-2 weeks

**Zinc (Zn) Deficiency:**
- **Symptoms:** Stunted growth, small leaves (little leaf)
- **Pattern:** Short internodes, rosetting of leaves
- **Growth Impact:** Severe growth reduction
- **Correction:** Zinc sulfate, zinc chelate
- **Timeline:** Improvement in new growth within 1-2 weeks

**Boron (B) Deficiency:**
- **Symptoms:** Heart rot (celery), hollow stems (cauliflower), cracked fruit
- **Pattern:** Death of growing points, distorted new growth
- **Growth Impact:** Poor reproductive development
- **Correction:** Borax (use sparingly - toxicity risk), kelp
- **Timeline:** Improvement in new growth within 1-2 weeks

**Copper (Cu) Deficiency:**
- **Symptoms:** Young leaves wilt and die back
- **Pattern:** Bleached or pale green new growth
- **Growth Impact:** Poor fruit set, reduced disease resistance
- **Correction:** Copper sulfate (use sparingly - toxicity risk)
- **Timeline:** Improvement in 1-2 weeks

**Molybdenum (Mo) Deficiency:**
- **Symptoms:** Yellowing between veins, similar to nitrogen
- **Pattern:** Cupping and scorching of leaves
- **Growth Impact:** Poor nitrogen utilization
- **Correction:** Sodium molybdate
- **Timeline:** Improvement in 1-2 weeks

### Disease Identification Guide

#### Fungal Diseases

**Powdery Mildew:**
- **Symptoms:** White powdery coating on leaves, stems, flowers
- **Conditions:** High humidity, moderate temperatures (60-80°F)
- **Susceptible Plants:** Squash, cucumbers, roses, phlox
- **Prevention:** Good air circulation, resistant varieties, neem oil
- **Treatment:** Sulfur spray, neem oil, milk spray (1:10), baking soda solution

**Downy Mildew:**
- **Symptoms:** Yellow patches on leaf tops, gray fuzzy growth underneath
- **Conditions:** Cool, wet weather, high humidity
- **Susceptible Plants:** Lettuce, grapes, basil, impatiens
- **Prevention:** Avoid overhead watering, good drainage, resistant varieties
- **Treatment:** Copper-based fungicides, biofungicides (Bacillus subtilis)

**Early Blight:**
- **Symptoms:** Dark concentric rings on leaves, starting from bottom
- **Conditions:** Warm, wet weather, poor air circulation
- **Susceptible Plants:** Tomatoes, potatoes, peppers
- **Prevention:** Crop rotation, mulching, resistant varieties
- **Treatment:** Copper fungicide, sulfur, biofungicides

**Late Blight:**
- **Symptoms:** Water-soaked lesions, white moldy growth, rapid plant death
- **Conditions:** Cool, wet weather (55-75°F)
- **Susceptible Plants:** Tomatoes, potatoes
- **Prevention:** Resistant varieties, good drainage, avoid overhead watering
- **Treatment:** Copper fungicide (must catch early), destroy infected plants

**Rust:**
- **Symptoms:** Orange/brown rust-colored pustules on leaves
- **Conditions:** Moderate temperatures, high humidity
- **Susceptible Plants:** Beans, roses, hollyhocks, corn
- **Prevention:** Resistant varieties, good air circulation
- **Treatment:** Sulfur spray, neem oil, remove infected leaves

**Root Rot:**
- **Symptoms:** Yellowing, wilting, brown/black mushy roots
- **Conditions:** Overwatering, poor drainage, cool soil
- **Susceptible Plants:** Most container plants, sensitive species
- **Prevention:** Well-draining soil, proper watering, avoid waterlogged conditions
- **Treatment:** Improve drainage, reduce watering, apply beneficial microbes

#### Bacterial Diseases

**Bacterial Leaf Spot:**
- **Symptoms:** Water-soaked spots that turn brown/black, yellow halos
- **Conditions:** Warm, wet weather, overhead watering
- **Susceptible Plants:** Tomatoes, peppers, lettuce, stone fruits
- **Prevention:** Crop rotation, resistant varieties, avoid overhead watering
- **Treatment:** Copper bactericide, remove infected leaves, improve air circulation

**Bacterial Wilt:**
- **Symptoms:** Sudden wilting despite adequate moisture, brown discoloration in stems
- **Conditions:** Warm weather, spread by cucumber beetles
- **Susceptible Plants:** Cucumbers, melons, squash
- **Prevention:** Row covers, control cucumber beetles, resistant varieties
- **Treatment:** No cure - remove and destroy infected plants

**Fire Blight:**
- **Symptoms:** Blackened, curled shoots that look burned
- **Conditions:** Warm, wet weather during bloom
- **Susceptible Plants:** Apples, pears, roses
- **Prevention:** Resistant varieties, avoid excessive nitrogen
- **Treatment:** Prune infected branches 12 inches below symptoms, disinfect tools

**Crown Gall:**
- **Symptoms:** Swollen, tumor-like growths at crown of plant
- **Conditions:** Soil-borne bacteria enters through wounds
- **Susceptible Plants:** Many woody plants, tomatoes, roses
- **Prevention:** Avoid wounding roots, use clean soil, resistant rootstocks
- **Treatment:** Remove affected plants, solarize soil

#### Viral Diseases

**Mosaic Virus:**
- **Symptoms:** Mottled light/dark green pattern, distorted leaves
- **Conditions:** Spread by aphids, mechanical damage
- **Susceptible Plants:** Tomatoes, peppers, cucumbers, beans
- **Prevention:** Control aphids, resistant varieties, sanitize tools
- **Treatment:** No cure - remove and destroy infected plants

**Tomato Spotted Wilt Virus (TSWV):**
- **Symptoms:** Yellow/brown rings on leaves, stunted growth, dark streaks
- **Conditions:** Spread by thrips
- **Susceptible Plants:** Tomatoes, peppers, lettuce
- **Prevention:** Control thrips, remove infected plants, resistant varieties
- **Treatment:** No cure - remove and destroy infected plants

**Cucumber Mosaic Virus:**
- **Symptoms:** Mottled leaves, stunted growth, distorted fruit
- **Conditions:** Spread by aphids, contaminated tools
- **Susceptible Plants:** Cucumbers, tomatoes, peppers
- **Prevention:** Control aphids, sanitize tools, resistant varieties
- **Treatment:** No cure - remove and destroy infected plants

### Pest Identification Guide

#### Chewing Insects

**Aphids:**
- **Appearance:** Small (1-8mm), pear-shaped, green/black/white/pink
- **Damage:** Curling leaves, sticky honeydew, sooty mold
- **Signs:** Clusters on new growth, ants tending them
- **Control:** Water spray, insecticidal soap, neem oil, ladybugs
- **Prevention:** Beneficial insects, avoid over-fertilizing

**Caterpillars:**
- **Types:** Cabbage loopers, hornworms, cutworms, armyworms
- **Damage:** Chewed leaves, holes, defoliation
- **Signs:** Droppings (frass), webbing, visible larvae
- **Control:** Handpick, Bt (Bacillus thuringiensis), neem oil
- **Prevention:** Row covers, encourage beneficial wasps

**Beetles:**
- **Types:** Japanese beetles, flea beetles, cucumber beetles, Colorado potato beetles
- **Damage:** Skeletonized leaves, holes in foliage, root damage
- **Signs:** Visible beetles, feeding damage patterns
- **Control:** Handpick, diatomaceous earth, neem oil, row covers
- **Prevention:** Trap crops, resistant varieties, beneficial nematodes

**Slugs and Snails:**
- **Appearance:** Soft-bodied, slimy, shell (snails)
- **Damage:** Irregular holes in leaves, slime trails
- **Signs:** Slime trails, nocturnal feeding damage
- **Control:** Beer traps, copper barriers, diatomaceous earth, iron phosphate
- **Prevention:** Reduce hiding places, remove debris, evening watering

#### Sucking Insects

**Spider Mites:**
- **Appearance:** Tiny, red/brown, webbing on plants
- **Damage:** Stippling (tiny dots), yellowing, leaf drop
- **Signs:** Fine webbing, tap test for mites
- **Control:** Water spray (increases humidity), neem oil, predatory mites
- **Prevention:** Adequate humidity, avoid broad-spectrum pesticides

**Whiteflies:**
- **Appearance:** Tiny white moth-like insects, fly when disturbed
- **Damage:** Yellowing leaves, sticky honeydew, sooty mold
- **Signs:** Cloud of whiteflies when shaking plant, sticky leaves
- **Control:** Yellow sticky traps, insecticidal soap, neem oil
- **Prevention:** Avoid over-fertilizing, beneficial insects

**Thrips:**
- **Appearance:** Tiny (1mm), elongated, fringed wings
- **Damage:** Silvery streaks, distorted growth, black frass
- **Signs:** Black specks (frass), distorted new growth
- **Control:** Blue sticky traps, neem oil, predatory mites
- **Prevention:** Remove weeds, beneficial insects

**Scale Insects:**
- **Appearance:** Small, armored bumps on stems/leaves
- **Damage:** Yellowing, stunted growth, sticky honeydew
- **Signs:** Brown/white bumps on plant, sooty mold
- **Control:** Manual removal, horticultural oil, neem oil
- **Prevention:** Inspect new plants, maintain plant health

#### Root and Soil Pests

**Root-Knot Nematodes:**
- **Appearance:** Microscopic worm-like organisms
- **Damage:** Knobby/galled roots, stunted growth, wilting
- **Signs:** Unhealthy appearance despite good care, swollen roots
- **Control:** Solarization, beneficial nematodes, resistant varieties
- **Prevention:** Crop rotation, marigolds, soil solarization

**Fungus Gnats:**
- **Appearance:** Tiny black flies, mosquito-like
- **Damage:** Larvae feed on roots, spread diseases
- **Signs:** Adult flies near soil, poor plant growth
- **Control:** Yellow sticky traps, beneficial nematodes, let soil dry
- **Prevention:** Avoid overwatering, well-draining soil

**Cutworms:**
- **Appearance:** Dark caterpillars, curl when disturbed
- **Damage:** Cut seedlings at soil level
- **Signs:** Severed seedlings, cutworms in soil at night
- **Control:** Collars around seedlings, handpick, Bt
- **Prevention:** Clean garden debris, till soil before planting

### Environmental Stress Factors

#### Water Stress

**Underwatering:**
- **Symptoms:** Drooping leaves, dry soil, leaf curling, crispy leaf edges
- **Progression:** Bottom leaves yellow/die first, overall wilting
- **Recovery:** Perked up within hours after watering if not severe
- **Prevention:** Mulch, consistent watering schedule, drought-resistant varieties

**Overwatering:**
- **Symptoms:** Yellowing leaves, soft/mushy stems, root rot
- **Progression:** Leaves drop, stunted growth, plant death
- **Recovery:** Very difficult once root rot sets in
- **Prevention:** Well-draining soil, check moisture before watering

**Inconsistent Watering:**
- **Symptoms:** Blossom end rot (tomatoes), fruit cracking, leaf drop
- **Progression:** Variable stress, reduced fruit quality
- **Recovery:** Variable depending on duration
- **Prevention:** Consistent watering schedule, mulching

#### Temperature Stress

**Heat Stress:**
- **Symptoms:** Wilting, sunscald, leaf curling, flower/fruit drop
- **Progression:** Accelerated bolting, reduced yields
- **Recovery:** Recovers with cooler temperatures and water
- **Prevention:** Shade cloth, mulch, adequate water

**Cold Stress:**
- **Symptoms:** Purpling leaves, stunted growth, frost damage
- **Progression:** Tissue death in freezing conditions
- **Recovery:** Partial if not frozen, dead tissue won't recover
- **Prevention:** Row covers, cold frames, proper planting timing

**Freezing Damage:**
- **Symptoms:** Water-soaked tissue, black/brown discoloration, mushy texture
- **Progression:** Tissue death, plant collapse
- **Recovery:** Dead tissue won't recover; may regrow from crown
- **Prevention:** Frost protection, hardening off, proper zone selection

#### Light Stress

**Insufficient Light:**
- **Symptoms:** Leggy growth (etiolation), small leaves, pale color
- **Progression:** Weak stems, poor flowering/fruiting
- **Recovery:** Moves plants to brighter location; existing growth won't change
- **Prevention:** Proper plant placement, supplemental grow lights

**Excessive Light:**
- **Symptoms:** Leaf scorch, bleached leaves, sunburn
- **Progression:** Tissue death, reduced photosynthesis
- **Recovery:** Damaged tissue won't recover; new growth will be normal
- **Prevention:** Gradual acclimation, shade during peak sun

#### Nutrient and Soil Issues

**pH Imbalance:**
- **Low pH (< 5.5):** Nutrient lockout (especially phosphorus), aluminum toxicity
- **High pH (> 7.5):** Nutrient lockout (iron, manganese, boron)
- **Symptoms:** Similar to nutrient deficiencies, stunted growth
- **Correction:** Add lime (raise pH) or sulfur (lower pH)
- **Testing:** pH test strips, meter, soil test kit

**Soil Compaction:**
- **Symptoms:** Poor drainage, stunted root growth, surface runoff
- **Progression:** Reduced nutrient uptake, plant stress
- **Correction:** Aeration, adding organic matter, raised beds
- **Prevention:** Avoid walking on soil, no-till methods

**Poor Soil Structure:**
- **Symptoms:** Water runs off or pools, poor root development
- **Progression:** Nutrient deficiencies, plant stress
- **Correction:** Add organic matter, compost, improve drainage
- **Prevention:** Regular compost additions, cover cropping

## Plant Database Integration

### Plant Species Information

For each plant in your garden, track:

**Basic Information:**
- Scientific name and common names
- Variety/cultivar
- Growth habit (annual, perennial, shrub, tree)
- Mature size (height, spread)
- Growth rate

**Environmental Requirements:**
- Hardiness zones
- Light requirements (full sun, partial shade, shade)
- Temperature tolerances (min/max)
- Humidity preferences
- Soil pH preferences

**Water and Nutrient Needs:**
- Watering frequency
- Drought tolerance
- Nutrient requirements (heavy, moderate, light feeder)
- Fertilizer schedule

**Planting and Care:**
- Planting date
- Expected days to maturity/harvest
- Pruning requirements
- Repotting needs (container plants)
- Propagation methods

**Pest and Disease Susceptibility:**
- Common pests
- Disease susceptibility
- Resistant varieties
- Companion plants

## Analysis Algorithms

### Image Processing Pipeline

#### 1. Image Preprocessing
- Color space conversion (RGB to LAB/HSV for better color analysis)
- Contrast enhancement (CLAHE - Contrast Limited Adaptive Histogram Equalization)
- Noise reduction (Gaussian blur or bilateral filter)
- Normalization (standardize lighting conditions)

#### 2. Color Analysis
- Extract color histograms for each leaf
- Compare against healthy leaf color profiles
- Detect chlorosis, necrosis, purpling patterns
- Calculate color deviation scores

#### 3. Texture Analysis
- Gray-Level Co-occurrence Matrix (GLCM) for texture features
- Detect surface abnormalities (powdery, fuzzy, hairy)
- Identify spot patterns (size, distribution, borders)
- Analyze leaf structure integrity

#### 4. Shape and Pattern Analysis
- Contour detection and shape analysis
- Identify leaf curling, cupping, distortion
- Detect spot shapes (circular, angular, irregular)
- Analyze vein patterns and health

#### 5. Feature Extraction
- Extract 500+ visual features per image
- Color features (L*a*b* values, histograms)
- Texture features (entropy, contrast, homogeneity)
- Shape features (aspect ratio, circularity, solidity)
- Spatial features (distribution patterns)

#### 6. Machine Learning Classification
- Trained models for 50+ plant diseases
- Nutrient deficiency pattern recognition
- Pest damage identification
- Environmental stress detection
- Confidence scoring for each prediction

### Multi-Image Analysis

When analyzing multiple images of the same plant:

1. **Temporal Comparison:**
   - Compare current images with baseline
   - Track progression over time
   - Identify worsening or improving conditions
   - Calculate rate of change

2. **Multi-Angle Integration:**
   - Combine analysis from different views
   - Cross-reference symptoms from different plant parts
   - Build comprehensive health profile

3. **Symptom Correlation:**
   - Identify related symptoms across plant parts
   - Differentiate between multiple issues
   - Prioritize interventions based on correlation strength

## Recommendation Engine

### Intervention Scoring System

Each potential intervention is scored on:
- **Effectiveness** (0-100): Expected success rate
- **Urgency** (0-100): Time sensitivity
- **Ease of Implementation** (0-100): Difficulty rating
- **Cost** (0-100): Lower is better
- **Organic Alignment** (0-100): Organic preference match
- **Overall Score**: Weighted average based on user preferences

### Recommendation Categories

**Immediate Actions (Do within 24 hours):**
- Critical disease treatment
- Severe pest outbreaks
- Life-threatening conditions

**Short-term Actions (Within 1 week):**
- Nutrient adjustments
- Environmental modifications
- Preventive measures

**Medium-term Actions (Within 1 month):**
- Soil amendments
- Repotting/transplanting
- Long-term preventive measures

**Long-term Strategy (Ongoing):**
- Soil health improvement
- Pest management program
- Disease prevention protocol

## Examples

See examples/ directory for:
- Tomato disease diagnosis workflow
- Nutrient deficiency identification
- Pest outbreak management
- Seasonal plant care schedule
- Container plant monitoring

## References

### Plant Identification Resources
- **PlantNet:** https://identify.plantnet.org/ - AI plant identification
- **Trefle API:** https://trefle.io/ - Comprehensive plant database
- **iNaturalist:** https://www.inaturalist.org/ - Citizen science identification
- **USDA Plants Database:** https://plants.usda.gov/ - Native plant database

### Disease and Pest Resources
- **Plant Disease Handbook:** Purdue University Extension
- **IPM (Integrated Pest Management):** University Extension resources
- **Cornell Vegetable MD:** https://vegetablemdonline.ppath.cornell.edu/
- **APS (American Phytopathological Society):** Disease resources

### Nutrient Management
- **Nutrient Deficiency Database:** Colorado State University Extension
- **Soil Health Hub:** Natural Resources Conservation Service (NRCS)
- **Plant Nutrient Functions:** University Extension publications

### Climate and Weather
- **USDA Hardiness Zones:** https://planthardiness.ars.usda.gov/
- **NOAA Climate Data:** https://www.ncdc.noaa.gov/
- **Local Extension Offices:** County-specific recommendations

### Research Papers
See references/research-papers.md for:
- Computer vision in plant disease detection
- Machine learning for plant health monitoring
- Nutrient deficiency pattern recognition
- Organic pest management effectiveness

## Troubleshooting

### Common Issues

**Poor Image Quality:**
- Ensure good lighting (natural daylight preferred)
- Use higher resolution camera if available
- Clean camera lens
- Avoid glare and shadows
- Steady camera to prevent blur

**Inaccurate Diagnoses:**
- Provide multiple images from different angles
- Include environmental context (recent weather, care changes)
- Document timeline of symptoms
- Check plant species information is correct
- Verify AI confidence scores

**No Improvement After Treatment:**
- Verify diagnosis accuracy
- Check treatment was applied correctly
- Ensure environmental conditions support recovery
- Consider multiple concurrent issues
- Allow sufficient time for improvement (varies by issue)

**Conflicting Recommendations:**
- Prioritize based on severity and urgency
- Consider compatibility of multiple treatments
- Start with least invasive options
- Monitor plant response and adjust

**Database Errors:**
- Check database file integrity
- Verify database permissions
- Review recent changes to plant records
- Restore from backup if needed

## Testing

### Unit Tests
- Test image preprocessing pipeline
- Verify color analysis accuracy
- Validate machine learning predictions
- Test database operations

### Integration Tests
- Test API integrations (PlantNet, Trefle, weather)
- Verify complete analysis workflow
- Test recommendation generation
- Validate alert system

### Manual Testing
- Test with known plant problems
- Verify recommendations are practical
- Check user interface usability
- Test across different plant types

## Version History

- **1.0.0** - Initial release with core diagnostic capabilities

## License

MIT License - Open source, free to use, modify, and distribute.

## Support

For issues, questions, or contributions:
- GitHub Issues: https://github.com/farmfriend-labs/agent-skills-farming/issues
- Email: farmfriend.labs@gmail.com
