# Soil Health Assessment References

## NRCS Soil Health Assessment Protocols

### Indicators of Soil Health

**Physical Indicators:**
1. **Aggregate Stability**
   - Measurement: Slake test or wet aggregate stability
   - Target: >60% stable aggregates
   - Improvement: Cover crops, reduced tillage

2. **Infiltration Rate**
   - Measurement: Single-ring infiltrometer test
   - Target: >3 inches/hour
   - Improvement: No-till, organic matter, reduced compaction

3. **Bulk Density**
   - Measurement: Soil core sample
   - Target: 1.2-1.5 g/cm³ (varies by texture)
   - Improvement: Reduce compaction, increase organic matter

4. **Soil Structure**
   - Assessment: Visual soil assessment (VSA)
   - Target: Granular structure, good porosity
   - Improvement: Cover crops, diverse rotations

**Chemical Indicators:**
1. **Organic Matter**
   - Measurement: Loss on ignition test
   - Target: >3% in temperate climates
   - Improvement: Cover crops, reduced tillage, compost

2. **pH**
   - Measurement: Soil test
   - Target: 6.0-7.0 for most crops
   - Improvement: Lime (low pH), sulfur (high pH)

3. **CEC (Cation Exchange Capacity)**
   - Measurement: Soil test
   - Target: Varies by texture (10-25 meq/100g)
   - Improvement: Increase organic matter

4. **Phosphorus and Potassium**
   - Measurement: Soil test
   - Target: Sufficiency levels vary by crop
   - Improvement: Targeted fertilization

**Biological Indicators:**
1. **Earthworm Count**
   - Assessment: Visual assessment during soil sampling
   - Target: >5 earthworms per cubic foot
   - Improvement: Organic matter, reduce pesticides

2. **Soil Respiration**
   - Measurement: CO2 evolution test
   - Target: Varies by management
   - Improvement: Organic amendments, cover crops

3. **Active Carbon**
   - Measurement: Permanganate oxidizable carbon
   - Target: >300 ppm
   - Improvement: Cover crops, reduced tillage

4. **Potentially Mineralizable Nitrogen**
   - Measurement: Anaerobic incubation
   - Target: Varies by crop needs
   - Improvement: Diverse rotations, legume cover crops

## Visual Soil Assessment (VSA)

### Procedure

1. **Soil Sampling**
   - Sample to depth of interest (usually 0-6 inches)
   - Avoid field edges and unusual areas
   - Collect 10-15 cores per assessment area
   - Sample when soil is moist but not wet

2. **Field Assessment**
   Score each indicator on a scale:
   - 1: Poor (severe limitation)
   - 2: Moderate limitation
   - 3: Good (minor limitation)
   - 4: Very good (no limitation)

3. **Indicators to Score:**

   **Structure and Porosity**
   - Look at soil clods when broken
   - Score: 1 = massive, platy; 4 = granular, crumbly

   **Earthworms**
   - Count earthworms in soil sample
   - Score: 1 = 0-1; 2 = 2-3; 3 = 4-5; 4 = 6+

   **Root Development**
   - Look at root branching and penetration
   - Score: 1 = restricted; 4 = extensive, deep

   **Soil Smell**
   - Healthy soil has earthy smell
   - Score: 1 = chemical, sour; 4 = earthy, pleasant

   **Residue Breakdown**
   - Look for partially decomposed residue
   - Score: 1 = no breakdown; 4 = good breakdown

   **Color**
   - Darker color indicates more organic matter
   - Score: 1 = light; 4 = dark

   **Compaction**
   - Test penetrometer resistance or visual assessment
   - Score: 1 = severely compacted; 4 = no compaction

   **Erosion**
   - Look for signs of soil loss
   - Score: 1 = severe erosion; 4 = no erosion

### Scoring and Interpretation

**Total Score:**
- 8-12: Poor soil health
- 13-18: Moderate soil health
- 19-24: Good soil health
- 25-32: Very good soil health

## Laboratory Tests

### Standard Soil Test Package

1. **pH** - Soil acidity/alkalinity
2. **Buffer pH** - Amount of lime needed
3. **Phosphorus** - Bray P1 or Mehlich-3 extraction
4. **Potassium** - Exchangeable K
5. **Magnesium** - Exchangeable Mg
6. **Calcium** - Exchangeable Ca
7. **CEC** - Cation exchange capacity
8. **Organic Matter** - Loss on ignition

### Advanced Soil Health Tests

1. **Permanganate Oxidizable Carbon (POXC)**
   - Active organic matter pool
   - Good indicator of biological activity
   - More responsive to management than total organic matter

2. **Soil Respiration**
   - CO2 evolution over 24 hours
   - Measures microbial activity
   - Higher = more active biology

3. **Potentially Mineralizable Nitrogen**
   - Anaerobic incubation
   - Predicts nitrogen release during season
   - Helps fine-tune fertilizer rates

4. **Wet Aggregate Stability**
   - Measures aggregate resistance to water
   - Indicator of erosion resistance
   - Higher = more stable aggregates

## Soil Health Trends

### Tracking Over Time

Establish baseline and retest every 3-5 years:

**Key Trends to Monitor:**
1. **Organic Matter**
   - Increasing: Good
   - Stable: Acceptable if at target
   - Decreasing: Concern - review management

2. **Aggregate Stability**
   - Improving: Reduced erosion risk
   - Declining: Increased erosion, infiltration problems

3. **Infiltration Rate**
   - Increasing: Better water management
   - Decreasing: Compaction, structure degradation

4. **Biological Activity**
   - Improving: Better nutrient cycling
   - Declining: Reduced residue, pesticide use

### Management Impact on Trends

**Practices that Improve Soil Health:**
- No-till or reduced tillage
- Cover crops (especially diverse mixtures)
- Diverse crop rotations (including small grains and legumes)
- Manure and compost application
- Reduced chemical inputs
- Prevent plant-feeding periods

**Practices that Reduce Soil Health:**
- Excessive tillage
- Monoculture cropping
- Lack of cover crops
- Excessive nitrogen fertilization
- Heavy equipment on wet soils
- Failure to address compaction

## Field History Integration

### Using Field History Intelligence

1. **Track Soil Test Results**
   - Import all soil tests into database
   - Include lab name, test date, sample depth
   - Attach PDF reports if available

2. **Analyze Trends**
   ```sql
   SELECT
     test_date,
     ph,
     organic_matter,
     nitrogen,
     phosphorus,
     potassium
   FROM soil_tests
   WHERE field_id = (SELECT id FROM fields WHERE name = 'North 40')
   ORDER BY test_date DESC
   LIMIT 10;
   ```

3. **Correlate with Yields**
   - Compare soil parameters to yield data
   - Identify limiting factors
   - Track improvement over time

4. **Link to Management**
   - Record cover crops planted
   - Track tillage operations
   - Document organic amendments
   - Compare to soil test trends

### AI Analysis Prompts

"Analyze 5 years of soil test data for [FIELD NAME] and:
- Identify trends in organic matter, pH, and nutrients
- Correlate soil changes with management practices
- Identify any declining parameters
- Recommend actions to improve soil health
- Predict next soil test expectations based on management"

## Laboratory Recommendations

### Choosing a Soil Test Lab

**Consider:**
- Turnaround time (1-2 weeks is typical)
- Test methods used (ensure consistency)
- Experience with agricultural soils
- Cost and package options
- Interpretation support

**Recommended Labs:**
- University extension labs (often lower cost, good support)
- Private commercial labs (faster turnaround, more options)
- State soil testing programs (sometimes subsidized)

### Sample Handling

1. **Sampling Equipment**
   - Use clean soil probe or auger
   - Plastic bucket (avoid metal contamination)
   - Sample bags from lab

2. **Sampling Procedure**
   - Zig-zag pattern across field
   - 10-15 cores per 20-40 acres
   - Consistent sampling depth (usually 0-6 inches)
   - Mix cores thoroughly
   - Subsample to fill bag

3. **Sample Timing**
   - Test same time each year (fall or early spring)
   - Avoid testing immediately after fertilization
   - Sample when soil is not too wet or dry
   - Allow 3-6 months between management change and testing

## References

- **USDA NRCS:** Soil Health Assessment protocols
- **Soil Science Society of America:** Standard testing methods
- **University Extension:** Local soil testing recommendations
- **Cornell Soil Health Assessment:** Comprehensive testing procedures

For specific recommendations, contact your local NRCS office or university extension service.
