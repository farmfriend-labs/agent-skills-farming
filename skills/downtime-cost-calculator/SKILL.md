# Downtime Cost Calculator

Calculate and analyze the true cost of equipment downtime, enabling farmers to make informed decisions about repair, replacement, and preventive maintenance investments.

## Purpose

Provide farmers with accurate calculations of equipment downtime costs, including direct costs (lost production, labor costs) and indirect costs (yield impacts, equipment degradation, missed opportunities). This enables data-driven decisions about repair urgency, replacement timing, and preventive maintenance investments.

## Problem Solved

Equipment downtime during critical operations is devastating but hard to quantify accurately. Farmers must make split-second decisions: repair immediately (expensive but necessary) or wait (risky). Traditional cost estimates miss critical factors: yield loss from delayed harvest, soil compaction from working wet fields, quality degradation from delayed planting, equipment damage from continued operation, and opportunity costs of missed optimal windows. This skill provides comprehensive, accurate cost calculations.

## Capabilities

- Calculate hourly downtime costs for specific equipment and operations
- Include direct costs (lost production, labor, rental, depreciation)
- Include indirect costs (yield impacts, quality degradation, soil damage)
- Calculate opportunity costs for optimal windows missed
- Analyze cumulative downtime over seasons
- Compare repair costs vs downtime costs
- Generate cost-benefit analysis for preventive maintenance
- Track downtime patterns and identify problematic equipment
- Calculate ROI of preventive maintenance investments
- Generate downtime reports for insurance or warranty claims
- Analyze seasonal downtime patterns
- Identify critical failure points and high-risk equipment
- Calculate penalty costs for missed delivery windows
- Analyze overtime costs from delayed operations

## Instructions

### Usage by AI Agent

1. **Define Equipment and Operation**
   - Identify equipment experiencing downtime
   - Determine operation type (planting, harvest, spraying, etc.)
   - Define acreage affected by downtime
   - Identify time constraints (weather windows, delivery deadlines)
   - Determine labor costs and availability

2. **Calculate Direct Costs**
   - Calculate lost production per hour
   - Calculate labor costs per hour
   - Include rental equipment costs if applicable
   - Calculate depreciation costs
   - Include fuel and input costs

3. **Calculate Indirect Costs**
   - Estimate yield loss from delayed operations
   - Calculate quality degradation impacts
   - Estimate soil compaction costs
   - Include equipment damage risks
   - Calculate penalty costs for missed deadlines

4. **Calculate Opportunity Costs**
   - Identify missed optimal windows
   - Calculate yield difference from optimal timing
   - Include weather-related opportunity costs
   - Calculate market timing impacts

5. **Generate Analysis**
   - Sum total downtime costs
   - Compare to repair costs
   - Generate cost-benefit analysis
   - Provide recommendations
   - Create report for decision-making

### Usage by Farmer

1. **Quick Downtime Assessment**
   - Input equipment and operation details
   - Review calculated downtime costs
   - Compare to repair quotes
   - Make immediate decision

2. **Comprehensive Analysis**
   - Define full context of downtime
   - Include all cost factors
   - Review detailed breakdown
   - Make informed strategic decision

3. **Historical Analysis**
   - Track downtime over seasons
   - Identify problematic equipment
   - Calculate total downtime costs
   - Plan preventive maintenance

4. **Maintenance Planning**
   - Calculate ROI of preventive maintenance
   - Compare downtime costs to maintenance costs
   - Plan maintenance schedules
   - Optimize equipment replacement timing

## Tools

### calculate-downtime-cost

**Description:** Calculate comprehensive downtime cost for equipment.

**Parameters:**
- `equipment` (object, required): Equipment details (type, age, value)
- `operation` (object, required): Operation details (type, acreage, crop)
- `downtime_hours` (number, required): Hours of downtime
- `include_indirect` (boolean, optional): Include indirect costs (default: true)
- `include_opportunity` (boolean, optional): Include opportunity costs (default: true)

**Returns:** Detailed cost breakdown with totals

### compare-repair-options

**Description:** Compare repair costs to downtime costs.

**Parameters:**
- `downtime_cost` (number, required): Total downtime cost calculation
- `repair_cost` (number, required): Repair cost estimate
- `repair_time_hours` (number, required): Time required for repair
- `replacement_cost` (number, optional): Replacement cost for comparison

**Returns:** Comparison with recommendations

### analyze-downtime-history

**Description:** Analyze historical downtime patterns.

**Parameters:**
- `equipment_id` (string, optional): Specific equipment to analyze
- `time_period` (string, optional): Time period to analyze (season, year, all)
- `include_indirect` (boolean, optional): Include indirect costs in analysis

**Returns:** Historical analysis with patterns and recommendations

### calculate-maintenance-roi

**Description:** Calculate ROI of preventive maintenance investment.

**Parameters:**
- `maintenance_cost` (number, required): Cost of preventive maintenance
- `expected_downtime_reduction` (number, required): Expected reduction in downtime hours
- `downtime_cost_per_hour` (number, required): Cost per hour of downtime
- `maintenance_frequency_months` (number, optional): Frequency in months

**Returns:** ROI calculation with recommendation

## Environment Variables

```
# Cost Defaults
DEFAULT_LABOR_COST_PER_HOUR=25.00
DEFAULT_RENTAL_COST_PER_HOUR=150.00
DEFAULT_DEPRECIATION_RATE=0.15

# Yield Impact Defaults
YIELD_LOSS_PER_DELAY_DAY_PERCENTAGE=1.5
QUALITY_DEGRADATION_PERCENTAGE=2.0

# Opportunity Cost Defaults
OPTIMAL_WINDOW_YIELD_BONUS_PERCENTAGE=5.0
MARKET_TIMING_IMPACT_PERCENTAGE=3.0

# Soil Impact Defaults
SOIL_COMPACTION_COST_PER_ACRE=25.00

# Penalty Costs
DELIVERY_PENALTY_PER_DAY=1000.00

# Database
DOWNTIME_DB_PATH=/data/downtime.db
```

## Real-World Examples

### Example 1: Quick Downtime Calculation

```python
from downtime_calculator import DowntimeCalculator

calculator = DowntimeCalculator()

# Calculate downtime cost for combine
result = calculator.calculate_downtime_cost(
    equipment={
        'type': 'combine',
        'value': 350000,
        'age': 5
    },
    operation={
        'type': 'harvest',
        'acreage': 500,
        'crop': 'corn',
        'yield_bushels_per_acre': 200,
        'price_per_bushel': 4.50
    },
    downtime_hours=8
)

print(f"Total Downtime Cost: ${result['total_cost']}")
print(f"  Direct Costs: ${result['direct_cost']}")
print(f"  Indirect Costs: ${result['indirect_cost']}")
print(f"  Opportunity Costs: ${result['opportunity_cost']}")
```

### Example 2: Repair vs Replace Decision

```python
from downtime_calculator import DowntimeCalculator

calculator = DowntimeCalculator()

# Calculate downtime cost
downtime_cost = calculator.calculate_downtime_cost(
    equipment={'type': 'combine', 'value': 350000, 'age': 5},
    operation={'type': 'harvest', 'acreage': 500, 'crop': 'corn'},
    downtime_hours=48
)['total_cost']

# Compare to repair
comparison = calculator.compare_repair_options(
    downtime_cost=downtime_cost,
    repair_cost=5000,
    repair_time_hours=8,
    replacement_cost=350000
)

print(f"Repair vs Replace Analysis:")
print(f"  Downtime Cost (48 hours): ${downtime_cost}")
print(f"  Repair Cost: $5000 (8 hours)")
print(f"  Recommendation: {comparison['recommendation']}")
```

### Example 3: Maintenance ROI

```python
from downtime_calculator import DowntimeCalculator

calculator = DowntimeCalculator()

# Calculate ROI of preventive maintenance
result = calculator.calculate_maintenance_roi(
    maintenance_cost=2000,
    expected_downtime_reduction=24,
    downtime_cost_per_hour=500,
    maintenance_frequency_months=6
)

print(f"Preventive Maintenance ROI:")
print(f"  Maintenance Cost: ${result['maintenance_cost']}")
print(f"  Downtime Cost Avoided: ${result['downtime_cost_saved']}")
print(f"  ROI: {result['roi_percentage']}%")
print(f"  Recommendation: {result['recommendation']}")
```

## Safety Considerations

- Use conservative estimates for yield impacts
- Verify downtime cost calculations with actual losses
- Include safety margins in calculations
- Consider weather forecasts in timing decisions
- Include operator safety in repair decisions
- Consider operator fatigue risks from overtime

## Troubleshooting

### Inaccurate Cost Estimates

**Problem:** Calculated costs don't match actual losses

**Solutions:**
- Verify yield and price inputs are current
- Include all indirect cost factors
- Update equipment value and age
- Consider seasonal variations
- Validate against historical data

### Missing Cost Factors

**Problem:** Calculation missing important cost factors

**Solutions:**
- Review all cost categories
- Include yield quality impacts
- Add soil damage estimates
- Include market timing impacts
- Consider penalty costs

### Uncertain Repair Time

**Problem:** Repair time estimate uncertain

**Solutions:**
- Get multiple repair quotes
- Use conservative time estimates
- Include parts availability lead time
- Consider backup equipment options
- Plan for delays and complications

### Complex Decision Context

**Problem:** Multiple factors make decision complex

**Solutions:**
- Break decision into multiple scenarios
- Calculate best and worst case scenarios
- Get professional repair assessment
- Consider equipment age and condition
- Evaluate replacement options

## Manufacturer and Research References

### Research Papers
- "The Economics of Farm Equipment Downtime" - Agricultural Economics
- "Cost-Benefit Analysis of Preventive Maintenance" - Computers and Electronics in Agriculture
- "Downtime Cost Analysis in Agriculture" - Journal of Agricultural Engineering

### Industry Data
- John Deere Equipment Cost Calculators
- Case IH Downtime Analysis Tools
- Equipment Manufacturers Association Cost Studies

### Standards
- ASABE Standards for Equipment Cost Analysis
- ISO Agricultural Machinery Cost Standards

## Legal Considerations

- Document downtime for insurance claims
- Calculate damages for warranty claims
- Include legal costs in downtime calculations
- Document all factors for contract disputes
