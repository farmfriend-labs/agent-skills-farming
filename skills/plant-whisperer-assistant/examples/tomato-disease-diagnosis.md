# Tomato Disease Diagnosis Workflow

This example demonstrates the complete workflow for diagnosing and managing tomato diseases using Plant Whisperer Assistant.

## Scenario

You have a healthy tomato plant that suddenly shows concerning symptoms. You need to identify the issue and take appropriate action.

## Step 1: Initial Observation

**Symptoms Observed:**
- Small dark spots on lower leaves
- Yellow halos around spots
- Concentric rings forming in larger spots
- Leaves starting to yellow and drop

**Environmental Context:**
- Recent rainfall (3 days of wet weather)
- Temperatures 75-85°F during day, 60-65°F at night
- Moderate air circulation (tomatoes in raised bed, 2 feet apart)

## Step 2: Capture Diagnostic Images

**Best Practices:**
1. Use natural daylight (avoid harsh shadows)
2. Include reference scale (coin or ruler) for size comparison
3. Capture multiple angles:
   - Overall plant view (showing which leaves are affected)
   - Close-up of affected leaf topside
   - Close-up of affected leaf underside
   - View of stem and base of plant
4. Date and timestamp each image

**Example Image Capture:**
```bash
# Navigate to plant directory
cd /opt/plant-whisperer/images

# Create plant-specific directory if not exists
mkdir -p plant_1

# Capture images (using smartphone or camera)
# Save with descriptive names:
# - plant_1_overview_2024-07-15.jpg
# - plant_1_leaf_topside_2024-07-15.jpg
# - plant_1_leaf_underside_2024-07-15.jpg
# - plant_1_stem_base_2024-07-15.jpg
```

## Step 3: Register Plant (If New)

```bash
cd /opt/plant-whisperer/skills/plant-whisperer-assistant

python3 scripts/add_plant.py \
  --name "Roma Tomato" \
  --species "Solanum lycopersicum" \
  --variety "Roma" \
  --location "Raised bed east side" \
  --planting-date "2024-05-15" \
  --container-size "Not applicable" \
  --soil-type "Loamy compost-amended" \
  --light-requirements "Full sun (6-8 hours)" \
  --water-requirements "1-2 inches per week" \
  --notes "First year growing this variety"
```

Expected output:
```
Plant registered successfully!
Plant ID: 1
Name: Roma Tomato
Species: Solanum lycopersicum
Variety: Roma
Planting Date: 2024-05-15
Days since planting: 61
```

## Step 4: Run Analysis

```bash
python3 scripts/analyze_plant.py \
  --image /opt/plant-whisperer/images/plant_1/leaf_topside_2024-07-15.jpg \
  --plant-id 1 \
  --mode comprehensive
```

**Expected Output:**

```
============================================================
PLANT HEALTH ANALYSIS RESULTS
============================================================
Image: /opt/plant-whisperer/images/plant_1/leaf_topside_2024-07-15.jpg
Analysis Date: 2024-07-15T10:30:00
Overall Health Score: 45/100

Primary Issue: Possible early blight

Issues Detected:
  - Chlorosis
  - Necrosis
  - Leaf spots

Recommendations:

1. [DISEASE] HIGH
   Remove severely infected leaves to prevent spread. Apply copper-based fungicide or sulfur spray. Improve air circulation around plants.
   (Organic method)

2. [GENERAL] MEDIUM
   Avoid overhead watering. Water at base of plants early in day so leaves dry quickly. Mulch around base to prevent soil splash.
   (Organic method)

3. [NUTRIENT] LOW
   Continue balanced fertilizer regimen. Early blight is not caused by nutrient deficiency but stressed plants are more susceptible.
   (Organic method)

4. [GENERAL] HIGH
   Monitor closely over next 5-7 days. If spots continue to spread upward, consider removing and destroying severely affected plants.
   (Organic method)

============================================================
```

## Step 5: Interpret Results

**Diagnosis: Early Blight (Alternaria solani)**

**Key Indicators:**
- Concentric ring pattern in spots (bullseye appearance)
- Starting from lower leaves and moving upward
- Yellow halos around spots
- Occurring in warm, wet conditions

**Severity: High** (Health score 45/100)

**Urgency: High** - Disease spreads rapidly in favorable conditions

## Step 6: Implement Treatment Plan

### Immediate Actions (Within 24 Hours)

**1. Remove Infected Leaves:**
```bash
# Remove all leaves with visible spots
# Focus on lower leaves first
# Dispose of infected material (don't compost)
# Sterilize pruning tools between plants (10% bleach solution)
```

**2. Apply Organic Treatment:**

**Option A: Copper Fungicide Spray**
```bash
# Mix copper fungicide according to label
# Spray remaining foliage thoroughly
# Reapply every 7-10 days
# Stop 14 days before harvest
```

**Option B: Sulfur Spray**
```bash
# Apply sulfur powder or spray
# Works best when temperatures are below 85°F
# Reapply every 7-14 days
# Avoid using within 2 weeks of oil-based products
```

**3. Environmental Modifications:**
- Stake or cage plants for better air circulation
- Remove lower leaves touching soil (create 6-8 inch clearance)
- Apply mulch to prevent soil splash
- Water at base of plants, not foliage
- Ensure adequate plant spacing

### Short-term Actions (1 Week)

**4. Continue Monitoring:**
- Check plants daily for new symptoms
- Photograph weekly to track progress
- Re-run analysis if condition worsens

**5. Preventive Measures:**
- Apply mulch (straw or shredded leaves) around base
- Rotate tomato location next year
- Consider resistant varieties for future plantings

### Long-term Strategy (Ongoing)

**6. Crop Rotation:**
- Don't plant tomatoes in same spot for 3 years
- Use family rotation: tomato → pepper/eggplant → legumes → brassicas → back to tomato

**7. Soil Health:**
- Add compost annually
- Maintain pH between 6.2-6.8
- Ensure good drainage

**8. Preventive Spraying:**
- Consider preventive copper spray before disease season
- Apply when conditions are favorable (warm + wet)
- Reapply every 7-10 days during disease season

## Step 7: Follow-up Analysis

After 7 days, capture new images and re-analyze:

```bash
python3 scripts/analyze_plant.py \
  --image /opt/plant-whisperer/images/plant_1/leaf_topside_2024-07-22.jpg \
  --plant-id 1 \
  --mode comprehensive
```

**Expected Improvement:**
- Health score should increase (e.g., 45 → 60-70)
- No new spots forming
- Remaining spots not growing
- Plants producing new healthy growth

**If Condition Worsens:**
- Health score decreases further
- New spots continuing to form
- Spots spreading upward
- Treatment not effective

**Escalation Options:**
1. Remove and destroy severely affected plants
2. Consider more aggressive treatment (consult local extension)
3. Prevent spread to healthy plants

## Step 8: Document and Learn

**Record in Plant Database:**
- Date of infection
- Symptoms observed
- Treatment applied
- Response to treatment
- Final outcome
- Lessons learned for next year

**Future Prevention:**
- Plant disease-resistant varieties (e.g., 'Mountain Merit', 'Defiant')
- Ensure proper spacing (2-3 feet between plants)
- Improve air circulation
- Use drip irrigation instead of overhead
- Apply preventive fungicide in disease-prone areas
- Rotate crops consistently

## Timeline Summary

| Day | Action |
|-----|--------|
| Day 0 | Identify symptoms, capture images, run analysis |
| Day 0-1 | Remove infected leaves, apply first treatment |
| Day 2-3 | Monitor for worsening |
| Day 7 | Re-apply treatment, re-analyze |
| Day 14 | Re-apply treatment if needed |
| Day 21 | Final assessment, document results |

## Success Criteria

**Treatment Successful:**
- No new spots forming after 7-10 days
- Health score improving each week
- Plants continuing to grow and produce
- Harvest unaffected

**Treatment Failed:**
- Disease continues to spread
- Plant health deteriorating
- Yield significantly reduced
- Need to destroy affected plants

## Additional Resources

- **Cornell Vegetable MD**: https://vegetablemdonline.ppath.cornell.edu/
- **Local Extension Office**: Contact for specific regional advice
- **SKILL.md**: Complete plant health documentation
- **references/plant-diseases.md**: Detailed disease information

## Troubleshooting

**No Improvement After 7 Days:**
1. Verify treatment was applied correctly
2. Check environmental conditions (still favorable for disease?)
3. Consider alternative treatment (different product)
4. Remove severely affected plants if disease spreading

**Chemical Burn on Leaves:**
- Stop copper/sulfur applications
- Rinse foliage with water
- Allow plant to recover
- Use lower concentration next time

**Weather Prevents Treatment:**
- Rain washes off fungicide
- Reapply after rain stops
- Apply early morning when foliage can dry
- Consider using sticker-spreader to improve adhesion
