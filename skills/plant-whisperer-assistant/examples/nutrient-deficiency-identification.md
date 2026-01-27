# Nutrient Deficiency Identification Workflow

This example shows how to identify and correct nutrient deficiencies in your plants using Plant Whisperer Assistant.

## Scenario

Your pepper plants have been growing well for 6 weeks, but suddenly the lower leaves are turning yellow while the upper leaves remain green. You need to identify the deficiency and correct it.

## Quick Reference: Mobile vs Immobile Nutrients

**Mobile Nutrients** (deficiency shows in older leaves first):
- Nitrogen (N)
- Phosphorus (P)
- Potassium (K)
- Magnesium (Mg)

**Immobile Nutrients** (deficiency shows in new growth first):
- Iron (Fe)
- Manganese (Mn)
- Zinc (Zn)
- Copper (Cu)
- Boron (B)

**Pattern Recognition:**
- Lower leaves yellowing → Mobile nutrient deficiency (N, P, K, Mg)
- Upper leaves yellowing → Immobile nutrient deficiency (Fe, Mn, etc.)
- Interveinal chlorosis → Fe, Mn, Mg deficiency
- Uniform yellowing → Nitrogen deficiency
- Purpling → Phosphorus deficiency

## Step 1: Document Symptoms

**Observed Pattern:**
- Yellowing starts at lower leaves
- Yellowing progresses upward over time
- Upper leaves remain green and healthy
- No spots or visible damage
- Growth has slowed slightly
- Plant is in container, 8 weeks old

**Environmental Context:**
- Regular watering schedule (water when soil dry to 2 inches)
- Last fertilized 3 weeks ago with balanced fertilizer
- Full sun (6-8 hours daily)
- Good drainage (container has drainage holes)
- No recent environmental stress

## Step 2: Capture Images

```bash
cd /opt/plant-whisperer/images
mkdir -p plant_5

# Capture images:
# - Overall plant showing pattern
# - Close-up of affected lower leaf
# - Close-up of healthy upper leaf
# - Container and soil surface
```

**Image Naming Convention:**
```
plant_5_overview_2024-07-20.jpg
plant_5_lower_leaf_affected_2024-07-20.jpg
plant_5_upper_leaf_healthy_2024-07-20.jpg
plant_5_container_soil_2024-07-20.jpg
```

## Step 3: Register Plant (If Not Already Done)

```bash
python3 scripts/add_plant.py \
  --name "Bell Pepper" \
  --species "Capsicum annuum" \
  --variety "California Wonder" \
  --location "Container deck, south facing" \
  --planting-date "2024-05-25" \
  --container-size "5 gallon" \
  --soil-type "Potting mix with compost" \
  --light-requirements "Full sun" \
  --water-requirements "Moist, not waterlogged" \
  --notes "First time growing peppers in container"
```

## Step 4: Run Analysis

```bash
python3 scripts/analyze_plant.py \
  --image /opt/plant-whisperer/images/plant_5/lower_leaf_affected_2024-07-20.jpg \
  --plant-id 5 \
  --mode comprehensive
```

**Expected Results:**

```
============================================================
PLANT HEALTH ANALYSIS RESULTS
============================================================
Overall Health Score: 65/100

Primary Issue: Chlorosis (yellowing) - possible nutrient deficiency

Issues Detected:
  - Chlorosis
  - Color deviation from healthy

Nutrient Analysis Results:
  Nitrogen Status: DEFICIENT
  Phosphorus Status: ADEQUATE
  Potassium Status: ADEQUATE
  Magnesium Status: ADEQUATE
  Iron Status: ADEQUATE

Recommendations:

1. [NUTRIENT] HIGH
   Apply nitrogen source immediately. Lower leaf chlorosis indicates nitrogen deficiency.
   Recommended organic sources: Fish emulsion (2-3 tbsp per gallon), blood meal (1-2 tbsp per gallon), or compost tea.
   Apply to soil and water in well.
   (Organic method)

2. [GENERAL] MEDIUM
   Resume regular fertilization schedule. Container plants need more frequent fertilizing than in-ground plants.
   Use balanced liquid fertilizer every 2-3 weeks.
   (Organic method)

3. [GENERAL] LOW
   Monitor plant response. Expect visible improvement in 3-7 days as nitrogen is mobile and moves quickly to deficient areas.
   (Organic method)

============================================================
```

## Step 5: Interpret Diagnosis

**Diagnosis: Nitrogen Deficiency**

**Why Nitrogen:**
- Yellowing starts on older leaves (characteristic of mobile nutrient)
- Uniform yellowing (not interveinal chlorosis)
- Pattern consistent with nitrogen deficiency
- Other nutrients (P, K, Mg, Fe) test adequate

**Root Cause Analysis:**
- Container plants have limited soil volume
- Nitrogen leaches with regular watering
- Last fertilization was 3 weeks ago
- Container peppers need more frequent feeding than in-ground

**Severity: Moderate** (Health score 65/100, not critical yet)

## Step 6: Treatment Options

### Option 1: Fish Emulsion (Recommended for Immediate Action)

**Pros:**
- Quick-acting nitrogen source
- Organic and safe
- Also provides some phosphorus and potassium
- Easy to apply

**Application:**
```bash
# Mix fish emulsion at 2-3 tbsp per gallon of water
# Apply to soil around base of plant
# Water in thoroughly
# Repeat in 7 days if needed
```

**Expected Results:**
- Improvement visible in 3-5 days
- New growth will be green
- Lower leaves may remain yellow (won't recover)

### Option 2: Blood Meal (Slower but Longer-Lasting)

**Pros:**
- High nitrogen content (12-13%)
- Longer-lasting effect
- Organic
- Improves soil structure

**Application:**
```bash
# Sprinkle 1-2 tbsp per gallon soil
# Work gently into top inch of soil
# Water in thoroughly
# Effects last 4-6 weeks
```

**Expected Results:**
- Improvement visible in 5-7 days
- Longer effect than fish emulsion
- May not need re-fertilizing for 3-4 weeks

### Option 3: Compost Tea (Gentle Option)

**Pros:**
- Gentle, won't burn plants
- Provides beneficial microbes
- Improves overall soil health
- Free if you have compost

**Application:**
```bash
# Steve finished compost in water for 24-48 hours
# Strain and apply liquid to soil
# Can apply weekly without risk of burning
# Best as preventive or for mild deficiencies
```

**Expected Results:**
- Slow improvement (7-14 days)
- Best for mild deficiencies or prevention
- Use with other methods for quicker results

### Option 4: Synthetic Fertilizer (Fastest Acting)

**Pros:**
- Fastest results
- Precise nutrient ratios
- Inexpensive
- Consistent formulation

**Application:**
```bash
# Use balanced liquid fertilizer (e.g., 20-20-20)
# Mix according to label instructions
# Apply to soil, water in thoroughly
# Repeat every 2-3 weeks during growing season
```

**Expected Results:**
- Improvement visible in 2-3 days
- Strong growth response
- Monitor for salt buildup in container

## Step 7: Implement Treatment

### Immediate Action (Choose One Method)

**For Fish Emulsion (Recommended):**
```bash
# Mix 2 tbsp fish emulsion in 1 gallon water
# Apply evenly to soil around base
# Water in lightly
# Note: Fish emulsion has strong odor
```

**For Blood Meal:**
```bash
# Sprinkle 1.5 tbsp blood meal on soil surface
# Gently work into top 1 inch with fingers
# Water in thoroughly
# Avoid contact with plant stems
```

**For Synthetic Fertilizer:**
```bash
# Mix 1 tbsp 20-20-20 fertilizer per gallon water
# Apply to soil until water runs from drainage holes
# Discard drainage water (don't let sit in saucer)
```

### Follow-up Care

**Day 1:**
- Observe plant (no immediate change expected)
- Ensure good drainage

**Day 3:**
- Check for new green growth at growing tips
- Old leaves won't recover (that's normal)

**Day 7:**
- Capture new image for comparison
- Re-analyze if desired
- Significant improvement should be visible

**Ongoing:**
- Resume regular fertilization schedule
- Container plants: fertilize every 2-3 weeks
- Use balanced fertilizer with nitrogen

## Step 8: Monitor Progress

### Follow-up Analysis

```bash
# After 7 days, capture new image
python3 scripts/analyze_plant.py \
  --image /opt/plant-whisperer/images/plant_5/lower_leaf_2024-07-27.jpg \
  --plant-id 5 \
  --mode standard
```

**Expected Improvement:**
- Health score: 65 → 80-85
- New growth appears green and healthy
- Growth rate increases
- No further yellowing

**Timeline Expectations:**

| Time | Expected Improvement |
|------|-------------------|
| Day 1-2 | No visible change (nutrient uptake) |
| Day 3-4 | Slight greening of new growth tips |
| Day 5-7 | Clear improvement, new green leaves |
| Day 7-10 | Significant improvement, vigorous growth |
| Day 14+ | Full recovery, normal growth resumes |

## Step 9: Prevent Future Deficiencies

### Container Plant Care Best Practices

**Fertilization Schedule:**
- In-ground: Every 4-6 weeks during growing season
- Container: Every 2-3 weeks during growing season
- Small containers (< 3 gallon): Every 2 weeks
- Large containers (> 5 gallon): Every 3-4 weeks

**Fertilizer Selection:**
- **Seedlings to 4 weeks**: Balanced or lower nitrogen (5-10-5, 10-10-10)
- **Active growth (4-8 weeks)**: Balanced (10-10-10, 20-20-20)
- **Flowering/fruiting**: Higher phosphorus (5-15-10, 10-30-20)

**Watering Considerations:**
- Regular watering leaches nutrients from containers
- Water until drainage from bottom
- Don't let sit in standing water
- Adjust watering based on weather (more when hot, less when cool)

### Soil Amendments

**Annual Refresh:**
```bash
# At start of growing season:
# Remove top 2 inches of soil
# Replace with fresh potting mix + compost
# Mix in slow-release fertilizer
# Top with mulch to retain moisture
```

**For Long-Term Plantings (perennials):**
```bash
# Top dress annually with compost
# Apply slow-release fertilizer in spring
# Refresh soil every 2-3 years by repotting
```

## Nutrient Deficiency Quick Reference

### Nitrogen (N) - Mobile
**Symptoms:** Uniform yellowing of older leaves, stunted growth, pale color
**Correction:** Fish emulsion, blood meal, compost tea, balanced fertilizer

### Phosphorus (P) - Immobile
**Symptoms:** Purpling of leaves (especially older), poor root development, dark green color
**Correction:** Bone meal, rock phosphate, fish bone meal

### Potassium (K) - Mobile
**Symptoms:** Yellow/brown leaf margins, weak stems, poor disease resistance
**Correction:** Greensand, kelp meal, wood ash, sulfate of potash

### Magnesium (Mg) - Mobile
**Symptoms:** Interveinal chlorosis (green veins, yellow between), on older leaves
**Correction:** Epsom salts (magnesium sulfate), dolomite lime

### Iron (Fe) - Immobile
**Symptoms:** Interveinal chlorosis on NEW growth, leaves can turn almost white
**Correction:** Chelated iron, iron sulfate, compost, sulfur (if pH too high)

### Calcium (Ca) - Immobile
**Symptoms:** Blossom end rot, tip burn, distorted new growth
**Correction:** Gypsum, lime (if pH low), eggshells, avoid calcium deficiency from inconsistent watering

## Troubleshooting

**No Improvement After 7 Days:**
1. Verify treatment was applied correctly
2. Check pH (nutrients unavailable at wrong pH)
3. Possible multiple deficiencies
4. Re-run analysis with new image

**Plant Stress After Fertilizing:**
- Possible fertilizer burn (too much fertilizer)
- Flush soil with water to remove excess
- Reduce fertilizer concentration next time

**Yellowing Continues:**
- May be combination of deficiencies
- Check for other symptoms (spots, curling, wilting)
- Could be pest or disease issue
- Consider soil test for comprehensive analysis

## Success Criteria

**Treatment Successful:**
- New growth appears green within 5-7 days
- No further yellowing of existing leaves
- Growth rate returns to normal
- Plant sets fruit/flowers normally

**Additional Notes:**
- Old yellow leaves will not recover (normal)
- Remove severely damaged leaves to improve appearance
- Maintain consistent fertilization schedule going forward
- Document for future reference

## Example Treatment Log

```
Date: 2024-07-20
Plant: Bell Pepper (ID: 5)
Issue: Nitrogen deficiency
Treatment: 2 tbsp fish emulsion per gallon water
Notes: Applied to soil, watered in

Date: 2024-07-22
Observation: New growth tips showing slight greening

Date: 2024-07-24
Observation: Clear improvement, new leaves green

Date: 2024-07-27
Observation: Full recovery, vigorous growth
Next fertilization: 2024-08-10 (2 weeks)
```
