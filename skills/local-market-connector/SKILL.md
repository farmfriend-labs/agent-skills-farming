# Local Market Connector

Connect farmers with local markets, buyers, and direct sales opportunities to maximize revenue and reduce dependence on commodity markets.

## Purpose

Establish direct connections between farmers and local buyers including restaurants, grocery stores, farmers markets, CSAs, food co-ops, and institutional buyers. Enable farmers to find and negotiate direct sales opportunities, bypassing commodity market middlemen and capturing more value for their products.

## Problem Solved

Farmers are often disconnected from local market opportunities, relying on commodity markets that offer lower prices and less control. This creates several problems:
- Receiving commodity prices far below retail value
- Lack of knowledge about local buyer needs and preferences
- Inability to match production to local demand
- Missed opportunities for premium pricing through direct sales
- No visibility into seasonal price trends in local markets
- Difficulty aggregating small quantities for institutional buyers
- Time-consuming manual outreach and relationship building
- Limited access to market intelligence beyond commodity reports

Local Market Connector solves these issues by providing access to local market data, buyer directories, and direct sales tools.

## Capabilities

- **Local Buyer Discovery:** Database of local restaurants, grocers, and institutions seeking farm products
- **Market Price Tracking:** Monitor local market prices vs. commodity prices
- **Demand Forecasting:** Predict local market demand by season and product
- **Connection Facilitation:** Tools to reach out to potential buyers
- **Order Management:** Track orders, deliveries, and payments from direct sales
- **Seasonal Planning:** Align production planning with local market demand patterns
- **Price Negotiation Support:** Data-driven negotiation tools for direct sales
- **Market Opportunity Alerts:** Notifications of new market opportunities
- **CSA Management:** Tools to manage Community Supported Agriculture programs
- **Farmers Market Integration:** Optimize farmers market participation
- **Wholesale Matching:** Connect with wholesale buyers for larger quantities
- **Local Food Hub Integration:** Interface with regional food hub networks
- **Marketing Materials:** Generate product lists, availability calendars, and price sheets
- **Compliance Tracking:** Maintain requirements for different buyer types (FSMA, GAP, organic)
- **Delivery Logistics:** Plan and track deliveries to multiple buyers

## Instructions

### Usage by AI Agent

1. **Build Buyer Database**
   - Import local buyer directories (restaurants, grocers, institutions)
   - Scrape online buyer databases (localharvest.org, state agriculture directories)
   - Manually add buyer contacts from networking and recommendations
   - Categorize buyers by type: retail, wholesale, institutional, CSA
   - Tag buyers by product preferences, seasonal needs, delivery requirements
   - Track buyer requirements (certifications, insurance, packaging)

2. **Analyze Market Opportunities**
   - Query database for buyers matching farm's production
   - Analyze seasonal demand patterns by buyer type
   - Compare commodity prices vs. local market prices
   - Identify premium pricing opportunities
   - Calculate potential revenue increase from direct sales
   - Assess logistics requirements for different buyer relationships

3. **Generate Target Lists**
   - Create prioritized lists of potential buyers
   - Score buyers by fit (product match, quantity, location, requirements)
   - Generate outreach materials tailored to each buyer type
   - Create availability calendars matching production to buyer needs
   - Prepare price sheets reflecting value-added pricing

4. **Facilitate Connections**
   - Draft personalized outreach emails or calls
   - Generate product listings with photos and descriptions
   - Create sample order forms and agreements
   - Prepare compliance documentation (GAP, organic, insurance certificates)
   - Schedule and track follow-up communications

5. **Manage Sales Pipeline**
   - Track buyer interest and progress through pipeline stages
   - Record meetings, calls, and communications
   - Schedule product availability and delivery windows
   - Generate orders from interested buyers
   - Manage inventory allocation across multiple buyers

6. **Support Operations**
   - Generate delivery schedules and route optimization
   - Track invoices and payments from direct sales
   - Maintain buyer relationships through regular communication
   - Collect and analyze feedback on product quality
   - Adjust production based on buyer feedback and market trends

7. **Market Intelligence**
   - Monitor local market price trends
   - Track competitor pricing and offerings
   - Identify emerging buyer needs and opportunities
   - Analyze seasonality in local demand
   - Provide recommendations for production planning

### Buyer Categories

**Retail Buyers:**
- Independent grocery stores
- Natural food co-ops
- Farmers markets (vendor relationships)
- Farm stands (if operating multiple)
- Online local food platforms

**Wholesale Buyers:**
- Restaurant distributors
- Small regional food hubs
- Grocery chain local procurement programs
- Institutional food service distributors

**Institutional Buyers:**
- School districts (farm-to-school programs)
- Hospitals and healthcare facilities
- Universities and colleges
- Corporate cafeterias
- Government agencies (local, state)

**Direct-to-Consumer:**
- CSA members
- Restaurant direct purchasing
- Farm subscription programs
- Online marketplace sales

### Data to Track per Buyer

**Contact Information:**
- Business name and type
- Contact person and role
- Phone, email, website
- Physical address and delivery locations
- Preferred contact method and hours

**Product Requirements:**
- Products of interest (with varieties preferred)
- Quantity needed (weekly, seasonal, annual)
- Quality standards and specifications
- Packaging requirements (bulk, individual, branded)
- Delivery frequency and timing
- Price sensitivity and budget range

**Compliance Requirements:**
- Food safety certifications needed (GAP, FSMA, organic)
- Insurance requirements
- License and permit requirements
- Traceability and labeling requirements
- Audit and inspection needs

**Business Terms:**
- Payment terms (Net 30, COD, etc.)
- Contract preferences (seasonal, annual, spot)
- Price negotiation flexibility
- Delivery arrangements and costs
- Minimum order quantities

**Relationship Status:**
- Contact history (calls, emails, meetings)
- Interest level and fit assessment
- Pipeline stage (prospect, active, customer, inactive)
- Last communication date
- Next action needed

## Tools

- **Python 3.8+** for data management and analysis
- **SQLite** for buyer and market data storage
- **Pandas** for market data analysis
- **Requests/BeautifulSoup** for web scraping buyer directories
- **ReportLab** for generating marketing materials
- **Geopy** for distance calculations and route planning
- **SMTPLib/Email** for outreach automation
- **CSV/JSON** for data import/export

## Environment Variables

```bash
# Database Configuration
BUYER_DB_PATH=/opt/local-market/buyers.db
MARKET_DATA_PATH=/opt/local-market/market-data.db
BACKUP_PATH=/opt/local-market/backups
AUTO_BACKUP_ENABLED=true

# Buyer Discovery
ENABLE_WEB_SCRAPING=true
SCRAPE_INTERVAL=weekly
BUYER_SOURCE_URLS=
USER_AGENT=LocalMarketConnector/1.0

# Email Configuration
SMTP_SERVER=
SMTP_PORT=587
SMTP_USERNAME=
SMTP_PASSWORD=
SMTP_FROM=YourFarm <contact@yourfarm.com>
EMAIL_TEMPLATES_DIR=/opt/local-market/templates

# Maps and Logistics
MAPS_API_KEY=  # Google Maps API for routing
DEFAULT_FARM_ADDRESS=
MAX_DELIVERY_DISTANCE=50  # miles

# Market Data
COMMODITY_PRICE_API=
LOCAL_PRICE_TRACKING=true
PRICE_UPDATE_INTERVAL=daily

# Notifications
NOTIFICATION_ENABLED=false
NOTIFICATION_EMAIL=
WEBHOOK_URL=

# Logging
LOG_LEVEL=info
LOG_FILE=/var/log/local-market-connector.log

# API Access
API_ENABLED=false
API_PORT=8080
API_TOKEN=

# Business Info
FARM_NAME=
FARM_ADDRESS=
FARM_PHONE=
FARM_EMAIL=
FARM_WEBSITE=
```

## Database Schema

### Buyers Table
```sql
CREATE TABLE buyers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  buyer_type TEXT NOT NULL,  -- retail, wholesale, institutional, direct
  sub_type TEXT,  -- restaurant, grocery, school, hospital, etc.
  contact_person TEXT,
  email TEXT,
  phone TEXT,
  website TEXT,
  address TEXT,
  city TEXT,
  state TEXT,
  zip TEXT,
  latitude REAL,
  longitude REAL,
  distance_miles REAL,
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Buyer Requirements Table
```sql
CREATE TABLE buyer_requirements (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  buyer_id INTEGER NOT NULL,
  product_type TEXT,
  product_variety TEXT,
  quantity_min REAL,
  quantity_max REAL,
  quantity_unit TEXT,
  quality_standards TEXT,
  packaging_requirements TEXT,
  delivery_frequency TEXT,
  price_min REAL,
  price_max REAL,
  price_unit TEXT,
  FOREIGN KEY (buyer_id) REFERENCES buyers(id)
);
```

### Buyer Compliance Table
```sql
CREATE TABLE buyer_compliance (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  buyer_id INTEGER NOT NULL,
  certification_type TEXT,  -- GAP, FSMA, organic, etc.
  certification_level TEXT,
  insurance_required BOOLEAN DEFAULT FALSE,
  insurance_amount REAL,
  license_required BOOLEAN DEFAULT FALSE,
  audit_required BOOLEAN DEFAULT FALSE,
  notes TEXT,
  FOREIGN KEY (buyer_id) REFERENCES buyers(id)
);
```

### Communications Table
```sql
CREATE TABLE communications (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  buyer_id INTEGER NOT NULL,
  contact_date DATE NOT NULL,
  contact_type TEXT,  -- email, phone, meeting, site_visit
  summary TEXT,
  follow_up_required BOOLEAN DEFAULT FALSE,
  follow_up_date DATE,
  next_action TEXT,
  FOREIGN KEY (buyer_id) REFERENCES buyers(id)
);
```

### Orders Table
```sql
CREATE TABLE orders (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  buyer_id INTEGER NOT NULL,
  order_date DATE NOT NULL,
  delivery_date DATE,
  status TEXT,  -- pending, confirmed, delivered, paid, cancelled
  total_amount REAL,
  payment_terms TEXT,
  notes TEXT,
  FOREIGN KEY (buyer_id) REFERENCES buyers(id)
);
```

### Order Items Table
```sql
CREATE TABLE order_items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  order_id INTEGER NOT NULL,
  product_name TEXT NOT NULL,
  variety TEXT,
  quantity REAL,
  unit TEXT,
  unit_price REAL,
  total_price REAL,
  FOREIGN KEY (order_id) REFERENCES orders(id)
);
```

### Market Prices Table
```sql
CREATE TABLE market_prices (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  product_type TEXT NOT NULL,
  variety TEXT,
  price REAL NOT NULL,
  unit TEXT NOT NULL,
  source TEXT,  -- commodity, local, wholesale, retail
  location TEXT,
  date DATE NOT NULL,
  notes TEXT
);
```

### Seasonal Demand Table
```sql
CREATE TABLE seasonal_demand (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  buyer_type TEXT NOT NULL,
  product_type TEXT NOT NULL,
  month INTEGER NOT NULL,
  demand_level TEXT,  -- low, medium, high
  notes TEXT
);
```

## Data Sources

### Online Buyer Directories

**LocalHarvest.org:**
- Farmers market listings
- CSA directories
- Local farm directories

**State Agriculture Departments:**
- Farm-to-school programs
- Local food directories
- Seasonal availability guides

**Chamber of Commerce Directories:**
- Restaurant listings
- Grocery stores
- Food service businesses

**Specialty Food Associations:**
- Natural food co-ops
- Organic food retailers
- Farm-to-table restaurants

### Government Programs

**USDA Farm-to-School:**
- School district contacts
- Seasonal demand information

**USDA Local Food Directories:**
- Regional food hub listings
- Buyer-seller matching programs

**State Farm-to-Institution:**
- Hospital food service contacts
- University procurement

## Outreach Strategies

### Email Outreach Templates

**Initial Contact:**
```
Subject: Local [Product] Available - [Farm Name]

Dear [Buyer Contact],

I'm reaching out from [Farm Name], a local farm in [Location] that has been
growing high-quality [Products] for [Number] years.

We currently have [Product] available and would love to explore the possibility
of supplying [Business Name]. Our [Product] features:
- [Key feature 1]
- [Key feature 2]
- [Key feature 3]

We pride ourselves on:
- Fresh harvest, usually within 24-48 hours of delivery
- Sustainable farming practices
- Consistent quality and availability

I'd welcome the opportunity to discuss how we might work together. Would you be
available for a brief call next week to learn more about your needs?

Best regards,
[Your Name]
[Your Title]
[Contact Information]
```

**Follow-up After Meeting:**
```
Subject: Great meeting - [Business Name] & [Farm Name]

Dear [Buyer Contact],

Thank you for taking the time to meet with me today. I appreciated learning about
[Business Name]'s commitment to [specific value mentioned - local sourcing, quality, etc.].

Based on our conversation, here's what I understand your needs to be:
- [Product 1]: [Quantity], [Frequency]
- [Product 2]: [Quantity], [Frequency]

I believe [Farm Name] can be a great fit for these needs. Here are our current
prices and availability:

[Product 1]: $[Price]/[Unit], [Availability]
[Product 2]: $[Price]/[Unit], [Availability]

Next steps from our discussion:
- [Action item 1]
- [Action item 2]

Please let me know if I've captured everything correctly, and when you'd like
to proceed.

Best regards,
[Your Name]
```

### Cold Call Script

**Opening:**
"Hi, this is [Name] from [Farm Name] in [Location]. I'm a local farmer growing
[Products] and I'm calling to learn if [Business Name] sources locally and if
you might have interest in our products."

**If interested:**
"That's great to hear. We specialize in [specialty] and can provide [key benefit
- consistent supply, superior quality, competitive pricing]. What types of
[products] are you currently using and from what sources?"

**Closing:**
"Would it be possible to schedule a 15-minute call next week to discuss further?
Or would you prefer I send over some information first?"

## Market Analysis

### Price Comparison

Calculate the opportunity cost of selling to commodity markets vs. direct sales:

**Revenue Impact Formula:**
```
Direct Sales Revenue = Quantity × Local Price
Commodity Revenue = Quantity × Commodity Price
Revenue Increase = Direct Sales Revenue - Commodity Revenue
Percentage Increase = (Revenue Increase / Commodity Revenue) × 100
```

**Logistics Cost Consideration:**
```
Net Revenue Increase = Revenue Increase - Delivery Cost - Packaging Cost -
                      Marketing Cost - Administrative Cost
```

### Demand Forecasting

Analyze historical seasonal patterns:
```sql
SELECT
  product_type,
  month,
  AVG(demand_score) as avg_demand
FROM seasonal_demand
WHERE buyer_type = 'restaurant'
GROUP BY product_type, month
ORDER BY product_type, month;
```

## Examples

See examples/ directory for:
- Finding local restaurant buyers
- Setting up CSA member database
- Comparing market prices
- Generating outreach materials
- Managing orders and deliveries

## References

### Industry Standards
- **Local Food Systems:** USDA local food procurement guides
- **Food Safety:** FSMA compliance requirements for direct sales
- **Farm-to-School:** USDA farm-to-school program guidelines
- **Organic Certification:** USDA organic standards for direct marketing

### Marketing Resources
See references/marketing-resources.md for:
- Email marketing templates
- Product photography guidelines
- Social media strategies
- Pricing strategy frameworks

### Legal Considerations
- Direct sales regulations by state
- Food licensing requirements
- Labeling requirements for direct sales
- Contract templates for buyer agreements

## Troubleshooting

### Buyer Not Responding

**Check:**
- Is contact information current?
- Is timing appropriate (not busy season)?
- Is value proposition clear and relevant?

**Solutions:**
- Try alternative contact method
- Find mutual connection for introduction
- Attend industry events for networking
- Send relevant information before calling

### Price Negotiations Stalled

**Check:**
- Is price realistic for market and quality?
- Are volume commitments clear?
- Are delivery terms acceptable?

**Solutions:**
- Offer tiered pricing based on volume
- Suggest trial period
- Highlight quality and consistency benefits
- Offer flexible terms (seasonal contract, etc.)

### Delivery Logistics Challenging

**Check:**
- Are delivery locations reasonable distance?
- Is delivery frequency workable?
- Are time windows feasible?

**Solutions:**
- Consolidate deliveries by geographic area
- Explore third-party delivery services
- Offer pickup option at farm or farmers market
- Coordinate with other farmers for joint delivery

## Testing

1. **Unit Testing**
   - Test buyer database queries
   - Verify price calculations
   - Test distance calculations
   - Validate email template generation

2. **Integration Testing**
   - Test buyer discovery from web sources
   - Verify email sending functionality
   - Test order creation and tracking
   - Validate report generation

3. **Data Quality Testing**
   - Validate buyer contact data
   - Check for duplicate entries
   - Verify price data accuracy
   - Test seasonal demand patterns

## Version History

- **1.0.0** - Initial release with buyer database and outreach tools

## License

MIT License - Open source, free to use, modify, and distribute.

## Support

For issues, questions, or contributions:
- GitHub Issues: https://github.com/farmfriend-labs/agent-skills-farming/issues
- Email: farmfriend.labs@gmail.com
