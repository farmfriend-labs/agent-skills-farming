# Basic Field History Import and Analysis

This example demonstrates how to import field data and analyze yield trends using Field History Intelligence.

## Scenario

You have 5 years of corn and soybean data scattered across:
- Paper notebooks (planting dates, variety choices)
- Combine yield monitor files (yield data)
- Receipts and invoices (input costs)
- Soil test reports from lab (soil health data)

You want to centralize this data and identify patterns to improve decision-making.

## Prerequisites

- Database initialized: `python3 scripts/init_database.py`
- Historical data in CSV or JSON format
- Python 3.8+ with required dependencies

## Setup

1. Initialize database (if not already done):
   ```bash
   cd /tmp/agent-skills-farming/skills/field-history-intelligence
   python3 scripts/init_database.py
   ```

2. Create field records in database:
   ```sql
   sqlite3 /opt/field-history/field-data.db

   INSERT INTO fields (name, farm_name, acres, soil_type, drainage_rating)
   VALUES
     ('North 40', 'My Farm', 40.5, 'Silt Loam', 'Good'),
     ('East 80', 'My Farm', 82.3, 'Clay Loam', 'Fair'),
     ('South 25', 'My Farm', 25.8, 'Sandy Loam', 'Excellent');
   ```

3. Create season records:
   ```sql
   INSERT INTO seasons (name, year, crop_type, planting_date, harvest_date)
   VALUES
     ('2024 Corn', 2024, 'corn', '2024-04-15', '2024-10-15'),
     ('2024 Soybeans', 2024, 'soybeans', '2024-05-10', '2024-10-01'),
     ('2023 Corn', 2023, 'corn', '2023-04-20', '2023-10-20'),
     ('2023 Soybeans', 2023, 'soybeans', '2023-05-15', '2023-10-05');
   ```

## Import Planting Data

Create a CSV file `planting_data.csv`:
```csv
field_name,season,variety,planting_date,seeding_rate,row_spacing,depth,method
North 40,2024 Corn,Pioneer P1234,2024-04-15,32000,30,2.5,no-till
North 40,2023 Corn,DeKalb DKC45-65,2023-04-20,31500,30,2.5,no-till
East 80,2024 Soybeans,Asgrow A2632,2024-05-10,140000,15,1.5,conventional
East 80,2023 Soybeans,Pioneer P22A05,2023-05-15,138000,15,1.5,conventional
```

Import the data:
```bash
python3 scripts/import_csv.py \
  --database /opt/field-history/field-data.db \
  planting_data.csv planting
```

Output:
```
Import Summary:
  Imported: 4 records
  Errors: 0
  Total: 4 rows
```

## Import Harvest Data

Create a CSV file `harvest_data.csv`:
```csv
field_name,season,harvest_date,variety,yield,moisture,test_weight
North 40,2024 Corn,2024-10-15,Pioneer P1234,215,16.5,58.2
North 40,2023 Corn,2023-10-20,DeKalb DKC45-65,198,17.2,57.8
East 80,2024 Soybeans,2024-10-01,Asgrow A2632,55,13.0,55.0
East 80,2023 Soybeans,2023-10-05,Pioneer P22A05,48,13.5,54.5
```

Import the data:
```bash
python3 scripts/import_csv.py \
  --database /opt/field-history/field-data.db \
  harvest_data.csv harvest
```

## Import Input Data

Create a CSV file `input_data.csv`:
```csv
field_name,season,application_date,input_type,product_name,rate,rate_unit,method,total_cost
North 40,2024 Corn,2024-04-10,fertilizer,28-0-0,30,gal/acre,injected,45.00
North 40,2024 Corn,2024-04-12,fertilizer,MAP,150,lbs/acre,broadcast,67.50
East 80,2024 Soybeans,2024-05-08,fertilizer,10-34-0,5,gal/acre,in-row,12.00
```

Import the data:
```bash
python3 scripts/import_csv.py \
  --database /opt/field-history/field-data.db \
  input_data.csv inputs
```

## Analyze Yields

Analyze yields across all fields and years:
```bash
python3 scripts/analyze_yields.py \
  --database /opt/field-history/field-data.db
```

Output:
```
====================================================================================================================
YIELD ANALYSIS REPORT
====================================================================================================================
Field                 Year   Variety              Yield       Moisture    Planting     Harvest
--------------------------------------------------------------------------------------------------------------------
North 40              2024   Pioneer P1234        215.0       16.5        2024-04-15   2024-10-15
North 40              2023   DeKalb DKC45-65     198.0       17.2        2023-04-20   2023-10-20
East 80               2024   Asgrow A2632        55.0        13.0        2024-05-10   2024-10-01
East 80               2023   Pioneer P22A05      48.0        13.5        2023-05-15   2023-10-05
--------------------------------------------------------------------------------------------------------------------
Average Yield: 129.0 bu/ac (4 records)
====================================================================================================================
```

Analyze specific field:
```bash
python3 scripts/analyze_yields.py \
  --database /opt/field-history/field-data.db \
  --field "North 40"
```

Output includes trend analysis showing whether yields are improving, declining, or stable over time.

## Query Database Directly

Find cost per bushel:
```sql
SELECT
  s.year,
  f.name AS field_name,
  s.crop_type,
  SUM(i.total_cost) AS total_input_cost,
  h.yield,
  CASE
    WHEN h.yield > 0 THEN SUM(i.total_cost) / h.yield
    ELSE 0
  END AS cost_per_bushel
FROM inputs i
JOIN fields f ON i.field_id = f.id
JOIN seasons s ON i.season_id = s.id
LEFT JOIN harvest h ON h.field_id = f.id AND h.season_id = s.id
GROUP BY s.year, f.name, s.crop_type, h.yield
ORDER BY s.year DESC, f.name;
```

## Advanced: AI Analysis

Use the AI agent to analyze patterns:

```
Analyze the North 40 field for the last 5 years and identify:
- Best performing corn variety
- Optimal planting window based on historical yield
- Input efficiency trends (cost per bushel)
- Any recurring issues or patterns
```

The AI will query the database, analyze the data, and provide comprehensive insights.

## Next Steps

- Import more historical years of data
- Add soil test data for trend analysis
- Import weather data for correlation analysis
- Generate comprehensive reports
- Create visualizations of trends and patterns

## References

- SKILL.md - Complete documentation
- examples/yield-analysis.md - Yield trend analysis examples
- examples/input-optimization.md - Input efficiency examples
