# Finding Local Restaurant Buyers

This example shows how to find and connect with local restaurants that source ingredients from local farms.

## Scenario

You're a vegetable farmer with excess capacity and want to sell directly to restaurants instead of selling all through commodity channels. You need to find restaurants in your area that value local sourcing and establish direct relationships.

## Prerequisites

- Database initialized: `python3 scripts/init_database.py`
- Farm location and product information ready
- Email configured for outreach (optional)

## Steps

### 1. Identify Your Value Proposition

Before searching for buyers, identify what makes your farm's products special:
- Specialty products (heirloom tomatoes, unique peppers, etc.)
- Consistent quality and availability
- Fresh harvest guarantee
- Sustainable farming practices
- Competitive pricing vs. distributors

### 2. Find Potential Buyers

Use web scraping to find local restaurants:
```bash
python3 scripts/scrape_buyers.py \
  --type restaurant \
  --location "Chicago, IL" \
  --radius 25
```

Manually add known restaurants:
```bash
python3 scripts/add_buyer.py \
  --name "Farm-to-Table Bistro" \
  --type restaurant \
  --contact "Chef Johnson" \
  --email "chef@farmtotablebistro.com" \
  --phone "555-123-4567" \
  --address "123 Main St, Chicago, IL" \
  --products "tomatoes, peppers, greens, herbs"
```

### 3. Search for Matching Buyers

Query the database for buyers matching your products:
```bash
python3 scripts/search_buyers.py \
  --products tomatoes,peppers \
  --type restaurant \
  --distance 30
```

Output:
```
Found 12 matching buyers:

1. Farm-to-Table Bistro
   Type: Restaurant
   Distance: 8.2 miles
   Products: tomatoes, peppers, greens, herbs
   Contact: Chef Johnson (chef@farmtotablebistro.com)

2. The Local Kitchen
   Type: Restaurant
   Distance: 12.5 miles
   Products: seasonal vegetables, herbs
   Contact: Chef Maria (maria@localkitchen.com)

...
```

### 4. Analyze Opportunities

Compare local market prices to commodity prices:
```bash
python3 scripts/compare_prices.py \
  --product "heirloom_tomatoes" \
  --location "Chicago"
```

Output:
```
Price Comparison - Heirloom Tomatoes

Commodity Price: $2.50/lb
Local Restaurant Price: $4.50-6.00/lb
Direct-to-Consumer Price: $6.00/lb

Revenue Opportunity:
  Selling 500 lbs at commodity: $1,250
  Selling 500 lbs to restaurant (avg): $2,625
  Revenue increase: $1,375 (110% increase)

Logistics Cost Estimate:
  Delivery: $50
  Packaging: $25
  Net increase: $1,300
```

### 5. Generate Outreach Materials

Create personalized outreach email:
```bash
python3 scripts/generate_outreach.py \
  --buyer-id 1 \
  --template restaurant_intro \
  --products "heirloom_tomatoes, peppers"
```

This generates a personalized email with:
- Farm information
- Available products
- Value proposition
- Call to action

### 6. Track Communications

Log outreach efforts in the database:
```bash
python3 scripts/log_communication.py \
  --buyer-id 1 \
  --type email \
  --date "2024-01-15" \
  --summary "Sent initial outreach email"
  --follow-up-date "2024-01-22"
```

### 7. Manage Sales Pipeline

Check pipeline status:
```bash
python3 scripts/generate_report.py \
  --type pipeline \
  --format markdown
```

Output:
```
Sales Pipeline Summary

New Prospects: 12
Contacted: 8
Interested: 3
Negotiating: 2
Active Customers: 1

Next Actions:
- Follow up with Farm-to-Table Bistro (scheduled 1/22)
- Send samples to The Local Kitchen
- Schedule meeting with Green Plate Cafe

Conversion Rate: 25% (3/12 contacted converted to interested)
```

### 8. Create First Order

When you secure a customer, create an order:
```bash
python3 scripts/create_order.py \
  --buyer-id 1 \
  --delivery-date "2024-01-20" \
  --item "heirloom_tomatoes" 50 lbs 5.00 \
  --item "bell_peppers" 25 lbs 4.50
```

## Best Practices

**Prioritize Buyers:**
1. Those already sourcing locally (easier conversion)
2. Close to farm (lower delivery costs)
3. Match your production schedule
4. Have appropriate volume needs

**Value-Based Pricing:**
- Price based on quality, not just commodity
- Offer volume discounts for regular commitments
- Consider bundled offerings for multiple products

**Relationship Building:**
- Visit restaurants to see their operation
- Understand their menu and seasonal needs
- Be responsive to special requests
- Maintain consistent communication

**Start Small:**
- Begin with one or two products
- Prove reliability and quality
- Expand relationship over time
- Ask for referrals to other restaurants

## Sample Products List

Create a products list to share with buyers:
```markdown
# Available Products - 2024 Season

## Tomatoes
- Heirloom varieties: $5.00/lb
- Roma: $3.50/lb
- Cherry: $4.00/pint
- Available: July-October

## Peppers
- Bell peppers (various colors): $4.50/lb
- Jalapeño: $3.00/lb
- Specialty hot peppers: $6.00/lb
- Available: July-September

## Greens
- Mixed salad greens: $6.00/lb
- Arugula: $8.00/lb
- Kale: $4.00/bunch
- Available: May-November

**Delivery:**
- Minimum order: $50
- Delivery within 25 miles: Free
- Delivery 25-50 miles: $15

**Contact:**
  Farm Name
  Phone: 555-123-4567
  Email: farmer@farm.com
```

## References

- SKILL.md - Full documentation
- examples/csa-setup.md - Setting up CSA programs
- examples/outreach.md - Outreach strategies
