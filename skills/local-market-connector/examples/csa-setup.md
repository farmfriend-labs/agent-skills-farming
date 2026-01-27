# Setting Up CSA Member Management

This example demonstrates setting up a Community Supported Agriculture (CSA) program using Local Market Connector.

## Scenario

You're starting a 50-member CSA program for your vegetable farm. You need to:
- Track member subscriptions
- Manage weekly box contents
- Coordinate deliveries/pickups
- Handle member communications

## Setup

### 1. Add CSA as Buyer Category

CSA members are direct-to-consumer buyers:

```bash
python3 scripts/add_buyer.py \
  --name "CSA Program 2024" \
  --type direct \
  --sub_type csa \
  --notes "50-member vegetable CSA, 20-week season"
```

### 2. Add CSA Members

Add each member as an individual buyer:

```bash
python3 scripts/add_buyer.py \
  --name "John Smith" \
  --type direct \
  --sub_type csa_member \
  --contact "John Smith" \
  --email "john.smith@email.com" \
  --phone "555-111-2222" \
  --address "123 Oak St, Anytown, IL" \
  --notes "Full share, Friday pickup at farm"
```

### 3. Create Weekly Box Plan

Track what goes into each week's CSA boxes:

```sql
INSERT INTO orders (
  buyer_id,
  order_date,
  delivery_date,
  status,
  notes
) VALUES (
  1,  -- CSA Program ID
  '2024-06-01',
  '2024-06-07',
  'confirmed',
  'Week 1 CSA boxes'
);

-- Add box contents
INSERT INTO order_items (
  order_id,
  product_name,
  variety,
  quantity,
  unit,
  unit_price,
  total_price
) VALUES (
  1,
  'Head lettuce',
  'Romaine',
  1,
  'head',
  3.00,
  3.00
);
```

### 4. Generate Weekly CSA Newsletter

Create communication to members about box contents:

```bash
python3 scripts/generate_outreach.py \
  --type csa_newsletter \
  --week 1 \
  --date "2024-06-07"
```

Output includes:
- Box contents list
- Farm news and updates
- Recipe suggestions
- Storage tips for produce

### 5. Track Member Payments

Record subscription payments:

```sql
INSERT INTO financial_records (
  buyer_id,
  record_date,
  category,
  description,
  amount,
  payment_method
) VALUES (
  2,  -- John Smith member ID
  '2024-05-01',
  'csa_subscription',
  'Full share 20-week subscription',
  600.00,
  'check'
);
```

### 6. Manage Pickup/Delivery Schedule

For member pickups at farm:

```bash
python3 scripts/schedule_pickups.py \
  --date "2024-06-07" \
  --time "14:00-18:00" \
  --location "Farm Stand"
```

## Member Communication

### Weekly CSA Email Template

Subject: Your CSA Box - Week 1 - June 7, 2024

```
Hello [Member Name],

Welcome to your first CSA box of the 2024 season! Here's what's in this week's box:

**This Week's Harvest:**
- Head lettuce (Romaine) - 1 head
- Spinach - 1 bag
- Radishes - 1 bunch
- Green onions - 1 bunch
- Strawberries - 1 quart

**Farm News:**
It's finally here! The 2024 CSA season kicks off this Friday. We're excited to
share the harvest with you. This spring has been challenging with the wet weather,
but the crops are looking great now that things have dried out.

The strawberries are just coming into peak production - enjoy them fresh or
save for shortcake!

**Storage Tips:**
- Lettuce and spinach: Store in plastic bag in refrigerator crisper
- Radishes: Remove tops, store roots in bag in refrigerator
- Strawberries: Store unwashed in refrigerator, wash just before eating
- Green onions: Store in bag in refrigerator

**Recipe Idea:**
Simple Strawberry Salad
- Fresh strawberries, sliced
- Spring greens
- Goat cheese crumbles
- Balsamic vinaigrette

**Pickup Details:**
- Date: Friday, June 7, 2024
- Time: 2:00 PM - 6:00 PM
- Location: Farm Stand (123 Farm Road)
- Please bring your own bags if possible

See you Friday!
[Your Farm Name]
```

## Managing Special Situations

### Vacation Weeks

When members will be away and can't pick up:

```bash
python3 scripts/vacation_hold.py \
  --member-id 2 \
  --start-date "2024-07-01" \
  --end-date "2024-07-07" \
  --option "credit"  # options: credit, donate, double_up
```

Options:
- **credit:** Member gets credit for future boxes
- **donate:** Box is donated to food bank
- **double_up:** Member gets double box following week

### Substitutions

When a crop fails and substitution is needed:

```sql
INSERT INTO substitutions (
  member_id,
  week,
  original_item,
  substituted_item,
  quantity,
  note
) VALUES (
  2,
  1,
  'Strawberries',
  'Raspberries',
  1,
  'quart',
  'Strawberries damaged by rain'
);
```

### Member Feedback

Collect and track member feedback:

```sql
INSERT INTO member_feedback (
  member_id,
  week,
  rating,  -- 1-5 scale
  comments,
  category  -- quantity, quality, variety
) VALUES (
  2,
  1,
  4,
  'Loved everything, but wish there were more strawberries',
  'quantity'
);
```

## CSA Business Analytics

Track member retention:

```sql
SELECT
  year,
  COUNT(*) as total_members,
  SUM(CASE WHEN returning = 1 THEN 1 ELSE 0 END) as returning_members,
  ROUND(100.0 * SUM(CASE WHEN returning = 1 THEN 1 ELSE 0 END) / COUNT(*), 1) as retention_rate
FROM csa_members
GROUP BY year;
```

Analyze box content value:

```sql
SELECT
  week,
  COUNT(*) as member_count,
  SUM(total_box_value) as total_value,
  AVG(total_box_value) as avg_value_per_box
FROM csa_boxes
JOIN order_items ON csa_boxes.id = order_items.order_id
WHERE year = 2024
GROUP BY week;
```

## Best Practices

**Member Communication:**
- Send weekly email with box contents and farm news
- Include recipe ideas and storage tips
- Share photos from the farm
- Communicate problems early and honestly

**Box Assembly:**
- Standardize box contents where possible
- Provide options when available (swap items)
- Include farm newsletter in box
- Quality check every box

**Pickup Logistics:**
- Clear pickup times and location
- Have backup plan for weather
- Track who picked up each week
- Follow up on missed pickups

**Member Satisfaction:**
- Survey members mid-season and end of season
- Address concerns promptly
- Celebrate successes with members
- Create community around the CSA

## References

- SKILL.md - Full documentation
- examples/find-buyers.md - Finding other buyer types
- examples/outreach.md - Communication strategies
