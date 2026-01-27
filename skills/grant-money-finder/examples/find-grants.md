# Finding Relevant Conservation Grants

This example shows how to find and apply for conservation grants for your farm.

## Scenario

You're a 200-acre corn and soybean farmer interested in improving soil health and reducing erosion. You want to find grants that can help cover costs for cover crops, no-till equipment, and conservation practices.

## Prerequisites

- Farm profile created
- Understand your conservation goals
- Know what practices you're interested in implementing

## Step 1: Create Farm Profile

First, create a detailed farm profile for eligibility matching:

```bash
python3 scripts/create_farm_profile.py \
  --farm-name "Green Acres Farm" \
  --owner "John Farmer" \
  --business-type "sole_proprietorship" \
  --farm-size 200 \
  --farm-size-unit acres \
  --location-county "Dane" \
  --location-state "Wisconsin" \
  --farm-type "row_crop" \
  --annual-revenue 250000 \
  --years-in-operation 15 \
  --certifications "none" \
  --conservation-practices "no-till,crop_rotation"
```

## Step 2: Search for Conservation Grants

Search for grants matching your conservation interests:

```bash
python3 scripts/search_grants.py \
  --category conservation \
  --keywords "cover_crop,no_till,erosion" \
  --max-funding 100000
```

Results:
```
Found 8 matching grants:

1. Environmental Quality Incentives Program (EQIP)
   Organization: USDA NRCS
   Category: Conservation
   Funding: $5,000 - $250,000 per year
   Deadline: Rolling applications
   Match Required: 0% (full cost-share)
   Eligibility: Farmers, Ranchers, Forest landowners
   Description: Provides financial and technical assistance to implement conservation
   practices that improve natural resources.

2. Conservation Stewardship Program (CSP)
   Organization: USDA NRCS
   Category: Conservation
   Funding: $20,000 - $40,000 per year (5-year contract)
   Deadline: Fall enrollment
   Match Required: 0% (full cost-share)
   Eligibility: Farmers and Ranchers
   Description: Reward producers who are already good stewards of natural resources
   for taking additional conservation actions.

3. State Cover Crop Cost-Share Program
   Organization: Wisconsin Department of Agriculture
   Category: Conservation
   Funding: $25/acre for cover crops
   Deadline: December 31, 2024
   Match Required: 25%
   Eligibility: Farmers with 10+ acres
   Description: Cost-share for establishing cover crops.

...
```

## Step 3: Check Eligibility

Check your eligibility for specific grants:

```bash
python3 scripts/check_eligibility.py \
  --grant-id 1 \
  --farm-profile-id 1
```

Output:
```
EQIP Eligibility Assessment for Green Acres Farm

✓ Business Type: Eligible (sole proprietorship)
✓ Farm Size: Eligible (200 acres)
✓ Location: Eligible (Dane County, WI)
✓ Land Ownership: Eligible (owned farmland)
✓ Compliance History: Eligible (no violations)

Recommended Practices for EQIP:
- Cover Crops: 160 acres @ $40/acre = $6,400
- No-Till Equipment: $45,000 cost-share (50%)
- Nutrient Management Plan: $5,000
- Filter Strips: 10 acres @ $250/acre = $2,500

Total Potential Funding: $58,900
Match Requirement: $0
```

## Step 4: Calculate Match Requirements

For grants requiring a match:

```bash
python3 scripts/calculate_match.py \
  --grant-id 3 \
  --practice "cover_crop" \
  --acres 160 \
  --cost-per-acre 35
```

Output:
```
Cover Crop Cost-Share Calculation

Practice: Cover Crops
Area: 160 acres
Total Cost: $5,600 (160 acres × $35/acre)

State Program:
- Cost-Share: $25/acre
- Grant Amount: $4,000
- Your Cost: $1,600
- Match Percentage: 28.6% (above 25% minimum - eligible)

Remaining Match Options:
1. Apply for additional EQIP cover crop funding
2. Use existing budget for 28.6% match
3. Enroll in stacked conservation programs

Recommendation: Apply for EQIP cover crop funding to reduce match to 0%
```

## Step 5: Create Application Tracker

Create application to track your progress:

```bash
python3 scripts/create_application.py \
  --grant-id 1 \
  --grant-name "EQIP 2024" \
  --status planning \
  --deadline "2024-11-01"
```

Add tasks to application:

```sql
INSERT INTO application_tasks (
  application_id,
  task_name,
  due_date,
  completed
) VALUES
  (1, 'Contact NRCS office', '2024-06-01', FALSE),
  (1, 'Complete conservation plan', '2024-06-15', FALSE),
  (1, 'Gather financial records', '2024-06-30', FALSE),
  (1, 'Submit application', '2024-10-01', FALSE);
```

## Step 6: Generate Grant Narrative

Use AI assistance to write grant narrative:

```bash
python3 scripts/generate_narrative.py \
  --grant-id 1 \
  --application-id 1 \
  --practices "cover_crop,no_till,filter_strips"
```

Generated narrative:
```
Project Title: Soil Health Improvement and Erosion Control

Project Description:
Green Acres Farm, operated by John Farmer, has been a cornerstone of Dane County
agriculture for 15 years. Located in Wisconsin's Driftless Area, our 200-acre
row crop operation faces ongoing challenges with soil erosion and nutrient runoff.

We propose implementing a comprehensive soil health improvement program including:
- 160 acres of multi-species cover crops (cereal rye, radishes, and clover mix)
- Transition to 100% no-till across all acres
- 10 acres of vegetative filter strips along waterways

Conservation Need:
The Driftless Area's topography makes our farm particularly susceptible to soil
erosion. Current estimates show we lose 2.5 tons of topsoil per acre annually.
This impacts both farm productivity and downstream water quality. Our long-term
goal is to reduce soil loss to below T (tolerable soil loss) levels.

Project Benefits:
1. Soil Health: Cover crops will increase organic matter, improve soil structure,
   and enhance water infiltration.

2. Water Quality: Filter strips and reduced tillage will decrease nutrient and
   sediment runoff by an estimated 40%.

3. Climate Resilience: Improved soil health will increase water holding capacity
   during drought periods.

4. Economic: No-till reduces fuel and equipment costs by $30-40/acre.
   Cover crops reduce nitrogen fertilizer needs by 50 lbs/acre.

Implementation Timeline:
Year 1:
- Spring: Purchase no-till equipment (John Deere 1590 drill)
- Spring: Plant 80 acres of cover crops after wheat harvest
- Fall: Plant 80 acres of cover crops after corn silage
- Fall: Establish 10 acres of filter strips

Years 2-5:
- Maintain all acres in no-till system
- Cover crops on all acres annually
- Monitor soil health and water quality improvements

Budget Summary:
Equipment (John Deere 1590 No-Till Drill): $90,000
  EQIP Cost-Share (50%): -$45,000
  Net Cost: $45,000

Cover Crop Seed (160 acres × $35/acre): $5,600
  EQIP Cost-Share ($40/acre): -$6,400
  Net Cost: $0 (excess funds for future cover crops)

Filter Strips Establishment (10 acres): $2,500
  EQIP Cost-Share (75%): -$1,875
  Net Cost: $625

Total Project Cost: $98,100
Total EQIP Funding: $53,275
Farm Contribution: $44,825

Qualifications:
John Farmer has 15 years of row crop farming experience and has implemented
no-till on 80 acres for the past 3 years with excellent results. We work
closely with Dane County NRCS District Conservationist Sarah Johnson and have
completed conservation plans for our entire operation.

We are committed to long-term stewardship of our land and look forward to
implementing these additional conservation practices with EQIP support.
```

## Step 7: Track Deadlines

Monitor all upcoming deadlines:

```bash
python3 scripts/track_deadlines.py
```

Output:
```
Upcoming Grant Deadlines

Within 14 days:
✓ None

This month:
- State Cover Crop Cost-Share: Dec 31, 2024 (14 days away)

Next month:
✓ None

Next quarter:
- EQIP Application: Nov 1, 2024 (45 days away)
- CSP Enrollment: Oct 15, 2024 (29 days away)

Action Items:
1. Complete EQIP application by Oct 15 (allow 2 weeks for NRCS review)
2. Submit state program by Dec 1 (early submission improves chances)
3. Schedule CSP pre-application meeting by September
```

## Step 8: Post-Award Reporting

If awarded, track reporting requirements:

```sql
INSERT INTO award_tracking (
  application_id,
  award_date,
  award_amount,
  reporting_deadline,
  report_submitted,
  payment_received,
  payment_date
) VALUES (
  1,
  '2024-12-15',
  53275.00,
  '2025-12-31',
  FALSE,
  FALSE,
  NULL
);
```

## Best Practices

**Applications:**
- Start early - applications take time
- Work with NRCS staff on conservation plans
- Document everything with photos and records
- Be specific about practices and implementation

**Eligibility:**
- Maintain good compliance history
- Know your farm's soil erosion rates
- Document current conservation practices
- Understand land ownership requirements

**Narrative Writing:**
- Be specific about problems and solutions
- Quantify benefits (soil saved, tons of erosion prevented, etc.)
- Show commitment to long-term stewardship
- Include photos of farm and current practices

**Multiple Grants:**
- Look for opportunities to stack programs
- Coordinate applications to avoid conflicts
- Keep track of all reporting requirements
- Document all activities for all programs

## References

- SKILL.md - Full documentation
- examples/application-tracking.md - Managing applications
- examples/eligibility-check.md - Eligibility assessment
