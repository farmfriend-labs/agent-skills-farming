# Example: Tracking Seed Viability Over Multiple Seasons

This example demonstrates how to track seed viability, make informed decisions about seed replacement, and maintain a healthy seed inventory.

## Scenario

You've been saving seeds for 3 years and have accumulated various varieties. Some seeds are getting old, and you need to determine which need replacement.

## Current Inventory

| ID | Variety | Crop | Year | Qty | Germ% | Last Tested |
|----|---------|------|------|-----|-------|-------------|
| 1 | Cherokee Purple | tomato | 2023 | 3g | 85% | 2024-03-15 |
| 2 | Kentucky Wonder | beans | 2024 | 5g | 92% | 2024-06-20 |
| 3 | Golden Bantam | corn | 2023 | 2g | 45% | 2024-04-10 |
| 4 | Waltham Butternut | squash | 2024 | 4g | 88% | 2024-08-25 |
| 5 | Boston Pickling | cucumber | 2022 | 3g | 60% | 2023-05-12 |
| 6 | Red Salad Bowl | lettuce | 2023 | 1g | 78% | 2023-09-01 |
| 7 | California Wonder | pepper | 2024 | 2g | 90% | 2024-07-30 |
| 8 | Detroit Dark Red | beets | 2022 | 3g | 55% | 2023-06-18 |

## Step 1: Run Viability Checker

```bash
python3 scripts/viability_checker.py
```

**Output:**

```
=== Seed Viability Check ===

Found 7 potential issues:

✗ Boston Pickling (cucumber)
   Year: 2022 | Germination: 60%
   Issue: Seed is 3 years old (max viability: 5 years)

✗ Detroit Dark Red (beets)
   Year: 2022 | Germination: 55%
   Issue: Low germination rate: 55%

✗ Golden Bantam (corn)
   Year: 2023 | Germination: 45%
   Issue: Low germination rate: 45%

⚠ Cherokee Purple (tomato)
   Year: 2023 | Germination: 85%
   Issue: Seed is 2 years old (approaching end of viability)

⚠ Red Salad Bowl (lettuce)
   Year: 2023 | Germination: 78%
   Issue: Last tested 511 days ago

ℹ Kentucky Wonder (beans)
   Year: 2024 | Germination: 92%
   Issue: Last tested 220 days ago

ℹ Waltham Butternut (squash)
   Year: 2024 | Germination: 88%
   Issue: Last tested 154 days ago

Summary: 3 high priority, 2 medium priority, 2 low priority

Recommendations:
  • Test germination for all high-priority seeds
  • Consider replacing seeds with low germination rates
  • Plan to save fresh seeds this season
```

## Step 2: Prioritize Action Items

### High Priority (Replace)

1. **Golden Bantam Corn (2023)**
   - Problem: 45% germination
   - Age: 2 years old (corn viability: 1 year)
   - Action: Replace immediately
   - Plan: Plant fresh seed this season, save new seed

2. **Boston Pickling Cucumber (2022)**
   - Problem: 60% germination
   - Age: 3 years old (approaching 5-year limit)
   - Action: Test again, likely replace
   - Plan: Grow fresh seed this season

3. **Detroit Dark Red Beets (2022)**
   - Problem: 55% germination
   - Age: 3 years old (viability: 4 years)
   - Action: Test again, consider replacement
   - Plan: Biennial - need to overwinter roots

### Medium Priority (Test or Plan)

4. **Cherokee Purple Tomato (2023)**
   - Problem: Approaching 2 years (viability: 4 years)
   - Germination: 85% - still good
   - Action: Test again, still viable
   - Plan: Save fresh seed this season

5. **Red Salad Bowl Lettuce (2023)**
   - Problem: Last tested >1 year ago
   - Germination: 78% - marginal
   - Action: Test germination now
   - Plan: May need replacement if below 70%

### Low Priority (Monitor)

6. **Kentucky Wonder Beans (2024)**
   - Germination: 92% - excellent
   - Last tested: 220 days ago
   - Action: No immediate action needed
   - Plan: Save fresh seed this season

7. **Waltham Butternut Squash (2024)**
   - Germination: 88% - excellent
   - Last tested: 154 days ago
   - Action: No immediate action needed
   - Plan: Save fresh seed this season

## Step 3: Conduct Germination Tests

### Test Golden Bantam Corn

```bash
python3 scripts/germination_test.py
```

**Input:**
- Seed ID: 3
- Seeds tested: 25
- Seeds germinated: 11

**Result:**
```
=== Test Results ===

Seeds tested: 25
Seeds germinated: 11
Germination rate: 44.0%

✗ Poor germination - consider replacing seed
```

**Decision:** Replace - germination too low for reliable planting

### Test Boston Pickling Cucumber

**Input:**
- Seed ID: 5
- Seeds tested: 20
- Seeds germinated: 10

**Result:**
```
Seeds tested: 20
Seeds germinated: 10
Germination rate: 50.0%

✗ Poor germination - consider replacing seed
```

**Decision:** Replace - marginal at best, age getting up there

### Test Red Salad Bowl Lettuce

**Input:**
- Seed ID: 6
- Seeds tested: 25
- Seeds germinated: 15

**Result:**
```
Seeds tested: 25
Seeds germinated: 15
Germination rate: 60.0%

✗ Poor germination - consider replacing seed
```

**Decision:** Replace - below 70% minimum threshold

## Step 4: Create Replacement Plan

### Seeds to Replace This Season

| Variety | Current Germ% | Age | Viability Limit | Action |
|---------|---------------|-----|-----------------|--------|
| Golden Bantam (corn) | 44% | 2 years | 1 year | Replace immediately |
| Boston Pickling (cucumber) | 50% | 3 years | 5 years | Replace this season |
| Detroit Dark Red (beets) | 55% | 3 years | 4 years | Replace this season (2-year cycle) |
| Red Salad Bowl (lettuce) | 60% | 2 years | 2 years | Replace this season |

### Seeds to Save Fresh

| Variety | Priority | Notes |
|---------|----------|-------|
| Cherokee Purple (tomato) | High | Current 85%, getting old |
| Kentucky Wonder (beans) | Medium | Current 92%, but 1 year old |
| Waltham Butternut (squash) | Medium | Current 88%, but 1 year old |

### Seeds to Source Externally

If can't save seed this season:

| Variety | Source Options |
|---------|---------------|
| Golden Bantam corn | Seed Savers Exchange, Baker Creek, local seed swap |
| Boston Pickling cucumber | Local garden center, seed swap, online |
| Detroit Dark Red beets | Biennial - need 2 years, may be easier to purchase |
| Red Salad Bowl lettuce | Quick to mature, easy to find |

## Step 5: Track Seed Saving Progress

### 2025 Planting Plan

| Month | Action |
|-------|--------|
| March | Plant Golden Bantam corn (purchased seed) |
| March | Test Cherokee Purple germination before planting |
| April | Plant Boston Pickling cucumber (purchased seed) |
| April | Plant Kentucky Wonder beans (existing seed) |
| May | Plant Waltham Butternut squash (existing seed) |
| May | Plant Red Salad Bowl lettuce (purchased seed) |
| September | Harvest and save Cherokee Purple tomatoes |
| October | Harvest and save Kentucky Wonder beans |
| October | Harvest and save Waltham Butternut squash |

### 2025-2026 Seed Saving Timeline

| Date | Variety | Action |
|------|---------|--------|
| Sep 2025 | Cherokee Purple | Harvest fruits, ferment seeds |
| Sep 2025 | Cherokee Purple | Dry seeds 10-14 days |
| Oct 2025 | Kentucky Wonder | Harvest dry pods, thresh |
| Oct 2025 | Waltham Butternut | Harvest overripe fruits, ferment |
| Oct 2025 | All varieties | Test germination |
| Nov 2025 | All varieties | Store in refrigerator |
| Nov 2025 | All varieties | Record in database |
| Nov 2025 | Detroit Dark Red | Harvest roots, overwinter (biennial) |
| Apr 2026 | Detroit Dark Red | Replant roots for seed |
| Jul 2026 | Detroit Dark Red | Harvest seeds, process |
| Jul 2026 | Detroit Dark Red | Test germination, store |

## Step 6: Update Database After New Harvests

After 2025 harvest:

```bash
python3 scripts/seed_manager.py add
```

**New entries:**

| Variety | Crop | Year | Qty | Notes |
|---------|------|------|-----|-------|
| Cherokee Purple | tomato | 2025 | 4g | Saved from my garden, 91% germination |
| Kentucky Wonder | beans | 2025 | 6g | Saved from my garden, 94% germination |
| Waltham Butternut | squash | 2025 | 5g | Saved from my garden, 89% germination |
| Golden Bantam | corn | 2025 | 3g | Purchased seed, first season |
| Boston Pickling | cucumber | 2025 | 2g | Purchased seed, first season |
| Red Salad Bowl | lettuce | 2025 | 1g | Purchased seed, first season |

## Step 7: Regular Viability Monitoring

### Weekly Tasks

- Check storage temperature and humidity
- Note any environmental changes
- Ensure refrigerator temperature stable

### Monthly Tasks

- Review seed inventory
- Check which seeds are approaching replacement age
- Plan seed saving for upcoming season

### Quarterly Tasks

- Run viability checker
- Test germination for seeds >1 year old
- Update replacement plan

### Annual Tasks

- Record complete seed saving season
- Evaluate seed performance
- Update database with new harvests
- Participate in seed exchanges

## Long-Term Seed Viability Strategy

### Maintain 3-Year Rotation

Each variety should have seeds from 3 different years:
- **Year 1 (fresh)** - For planting this season
- **Year 2 (good)** - Backup, still high germination
- **Year 3 (marginal)** - Last resort, may need replacement

### Example Rotation Timeline

**Cherokee Purple Tomato:**
- 2025 seed: 91% germination (plant 2025, 2026)
- 2024 seed: 85% germination (backup, plant 2026 if needed)
- 2023 seed: 80% germination (last resort, likely replace)

**Decision for 2026:**
- Plant 2025 seed primarily
- Keep 2024 as backup
- Save fresh 2026 seed
- Remove 2023 seed from active inventory

### Track Seed Quality Over Time

Create seed performance log:

```
Variety: Cherokee Purple Tomato

2023 Seed:
  Year saved: 2023
  Germination: 85% (tested 2024-03-15)
  Plantings:
    2024 spring: 10 plants, good vigor
    2024 fall: 5 plants, minor disease issues
  Notes: Good variety, maintain in inventory

2025 Seed:
  Year saved: 2025
  Germination: 91% (tested 2025-09-20)
  Plantings: TBD
  Notes: Excellent germination, expect good performance

Replacement due: 2027 (after 2026 harvest)
```

## Benefits of Regular Viability Tracking

1. **Reliable Planting** - Know exactly which seeds will germinate well
2. **Cost Savings** - Only replace seeds when necessary
3. **Time Savings** - Don't waste time on low-germination seeds
4. **Yield Improvement** - Plant only high-viability seeds
5. **Inventory Management** - Keep organized, up-to-date records
6. **Planning** - Anticipate replacement needs in advance
7. **Data Collection** - Track variety performance over years

## Automated Viability Alerts

Set up automated checks (optional):

```bash
# Run viability checker weekly
0 9 * * 1 python3 /opt/seed-sovereignty/scripts/viability_checker.py >> /var/log/seed-sovereignty/viability.log 2>&1

# Monitor storage conditions daily
0 */6 * * * python3 /opt/seed-sovereignty/scripts/storage_monitor.py check >> /var/log/seed-sovereignty/storage.log 2>&1
```

This ensures you're always aware of seed viability status.
