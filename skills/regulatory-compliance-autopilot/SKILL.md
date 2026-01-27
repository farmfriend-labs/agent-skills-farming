# Regulatory Compliance Autopilot

Automate compliance reporting and tracking for agricultural operations, including environmental regulations, worker safety, chemical application records, equipment certifications, and government program requirements.

## Purpose

Eliminate manual compliance paperwork and reduce regulatory risk by automating the tracking, reporting, and documentation required for agricultural operations. Provide a unified system for managing all compliance requirements across federal, state, and local jurisdictions.

## Problem Solved

Modern agricultural operations face a complex web of regulatory requirements that create significant administrative burden and risk:

- **Environmental Regulations:** EPA regulations on pesticide application, nutrient management, water quality, air quality, and waste management
- **Worker Safety:** OSHA requirements for training, protective equipment, hazard communication, and incident reporting
- **Chemical Application:** Detailed record-keeping for pesticide/herbicide/fungicide applications (application rates, locations, weather conditions, re-entry intervals)
- **Equipment Compliance:** Annual inspections, emissions certifications, weight limits, and operational permits
- **Food Safety:** FSMA (Food Safety Modernization Act) requirements for traceability, sanitation, and contamination prevention
- **Government Programs:** NRCS/USDA program requirements for cost-share programs, conservation practices, and farm bill compliance
- **Record-Keeping:** Multiple overlapping requirements with different reporting periods, formats, and deadlines

Manual compliance management leads to:
- Missed deadlines resulting in fines ($1,000-$50,000 per violation)
- Incomplete records during audits
- Inconsistent data across systems
- Hours wasted on duplicate data entry
- Risk of losing program payments (NRCS cost-share can be $10,000-$100,000+)
- Operational disruption during audits
- Compliance gaps and liability exposure

Regulatory Compliance Autopilot automates the entire compliance lifecycle from data collection to report generation, ensuring farmers stay compliant while focusing on operations.

## Capabilities

### Core Functions

**Automated Regulatory Tracking:**
- Centralized repository for all regulatory requirements
- Deadline tracking with automated reminders
- Jurisdiction filtering (federal, state, county, local)
- Requirement categorization (environmental, safety, reporting, certification)
- Compliance status dashboard (compliant, at-risk, non-compliant)
- Regulatory change alerts and impact analysis

**Chemical Application Record-Keeping:**
- Automatic capture from application equipment (ISOBUS/ISO 11783)
- Record required data fields for EPA compliance:
  - Product name and EPA registration number
  - Application rate and total quantity applied
  - Location and field boundaries
  - Date and time of application
  - Weather conditions (wind speed, direction, temperature, humidity)
  - Applicator certification and license number
  - Re-entry interval (REI) and pre-harvest interval (PHI)
  - Target pest and crop
- Drift documentation and mitigation measures
- Spray drift modeling and buffer zone calculations
- Restricted-use pesticide (RUP) tracking
- Generate EPA-compliant application reports on demand

**Worker Safety Compliance (OSHA):**
- Track required training for all workers:
  - Pesticide handler training (Worker Protection Standard)
  - Equipment operation safety training
  - Hazard communication (HazCom) training
  - Emergency response training
  - First aid/CPR certification
- Training expiration tracking with automated reminders
- Personal Protective Equipment (PPE) inventory and assignment
- Hazardous Chemical Inventory (HazCom Standard)
- Safety data sheet (SDS) management and accessibility
- Incident and near-miss reporting and tracking
- OSHA 300 log maintenance (work-related injuries and illnesses)
- Annual training summaries for audits

**Equipment Compliance:**
- Track annual inspection requirements
- Emissions certification monitoring (Tier 4, CARB, etc.)
- Equipment weight and dimension limits for road transport
- Permit tracking (oversized/overweight permits, seasonal permits)
- Maintenance compliance logs
- GPS/RTK calibration records
- Generate inspection readiness reports

**Environmental Compliance:**
- Nutrient Management Plan (NMP) tracking
- Manure application records (timing, rates, setbacks)
- Cover crop reporting and compliance
- Conservation practice documentation
- Water quality monitoring data aggregation
- Air quality emissions tracking (dust, sprays, equipment)
- Wetland conservation compliance
- Endangered Species Act consultation tracking
- Generate EPA/State environmental compliance reports

**Food Safety Compliance (FSMA):**
- Produce Safety Rule compliance tracking
- Traceability records (field to distribution)
- Water quality testing records
- Soil amendments and manure application tracking
- Domesticated animal presence documentation
- Worker health and hygiene training
- Equipment sanitation and cleaning logs
- Recall planning and mock recall exercises
- Generate FSMA-compliance reports

**Government Program Compliance:**
- NRCS program requirements tracking (EQIP, CSP, ACEP, etc.)
- USDA Farm Bill program compliance
- Conservation practice documentation and verification
- Payment eligibility tracking
- Cost-share program documentation
- Crop insurance requirements
- Generate program compliance documentation

**Automated Reporting:**
- Pre-built report templates for major regulatory requirements
- Scheduled report generation and delivery (email, webhook)
- Custom report builder for unique requirements
- Report archival and retention management
- Audit trail for all report submissions
- Regulatory submission integrations (EPA e-filing, state portals)
- Generate annual compliance summary

**Audit Preparation:**
- One-click audit package generation
- Organized document repository by regulation
- Pre-audit compliance checks and gap identification
- Historical data retrieval for multi-year audits
- Digital signature and document authentication
- Export to PDF for official submissions

### Advanced Features

**AI-Powered Compliance Prediction:**
- Predict compliance gaps before deadlines
- Identify at-risk areas based on historical patterns
- Suggest corrective actions for non-compliance
- Model impact of operational changes on compliance
- Forecast resource needs for compliance activities

**Integration with Farm Systems:**
- Pull data from equipment ISOBUS/ISO 11783 messages
- Import from precision ag software (Climate FieldView, John Deere Ops Center, etc.)
- Sync with accounting systems for payment documentation
- Connect with HR systems for worker training records
- Integrate with weather services for application records

**Multi-Language Support:**
- Generate reports in multiple languages for diverse workforce
- Spanish-language worker safety materials and training records
- H2A visa program compliance tracking

**Mobile Worker Compliance:**
- Mobile app for field data capture
- Offline capability for areas with poor connectivity
- Photo documentation of compliance activities
- Signature capture for training and acknowledgments
- Barcode/QR code scanning for equipment and chemical tracking

## Instructions

### Usage by AI Agent

#### 1. Initial Compliance Setup

**Step 1: Identify Applicable Regulations**

```bash
cd /path/to/regulatory-compliance-autopilot
python3 scripts/setup_regulations.py --location "41.8776, -87.6346" --acres 5000
```

The system will:
- Determine state and county based on GPS location
- Identify federal regulations (EPA, OSHA, USDA, FSMA)
- Identify state-specific regulations (nutrient management, pesticide regulations)
- Identify county/local requirements (zoning, setbacks, permits)
- Generate applicable regulatory checklist

**Step 2: Configure Farm Profile**

Create detailed farm profile for jurisdiction determination:

```bash
python3 scripts/farm_profile.py \
  --name "Green Valley Farms" \
  --location "41.8776, -87.6346" \
  --state "Illinois" \
  --county "Cook" \
  --acres 5000 \
  --crops ["corn", "soybeans", "wheat"] \
  --livestock ["cattle", "hogs"] \
  --employees 25 \
  --seasonal-workers 15
```

**Step 3: Load Regulatory Requirements**

```bash
python3 scripts/load_regulations.py --source "epa,osha,usda,state"
```

This loads:
- EPA pesticide application requirements
- EPA nutrient management requirements
- OSHA worker safety requirements
- FSMA produce safety requirements
- State-specific agricultural regulations
- Reporting deadlines and frequency

**Step 4: Create Compliance Calendar**

```bash
python3 scripts/compliance_calendar.py --generate --year 2026
```

Generates calendar with:
- Monthly compliance tasks
- Quarterly reporting deadlines
- Annual certifications and inspections
- Training expiration dates
- Permit renewal dates
- Program application windows

#### 2. Chemical Application Compliance

**Step 1: Capture Application Data**

Automatic capture from equipment:

```bash
# Start application data capture
python3 scripts/capture_application.py \
  --interface can0 \
  --monitor
```

Manual entry for applications not captured automatically:

```bash
python3 scripts/log_application.py \
  --date "2026-01-27" \
  --time "14:30" \
  --field "North-40" \
  --crop "corn" \
  --product "Roundup PowerMAX" \
  --epa-number "524-528" \
  --epa-registered "true" \
  --rate "32" \
  --units "oz/acre" \
  --total-acres 240 \
  --total-quantity "480" \
  --total-units "gal" \
  --weather-temp 72 \
  --weather-humidity 45 \
  --weather-wind-speed 5 \
  --weather-wind-direction "NW" \
  --applicator "John Smith" \
  --license-number "IL-PEST-12345" \
  --certification-expiry "2026-12-31" \
  --rei "12" \
  --phi "45" \
  --restraint-zone "30" \
  --notes "Applied with drift reduction nozzle"
```

**Step 2: Validate Compliance**

The system automatically validates:
- Product is EPA registered and current
- Applicator holds valid certification
- Application rate is within label limits
- Weather conditions met label requirements
- Buffer zones maintained from sensitive areas
- Re-entry interval (REI) documented for workers
- Pre-harvest interval (PHI) tracked for crop

**Step 3: Generate EPA-Compliant Report**

```bash
# Generate EPA application report
python3 scripts/gen_application_report.py \
  --start-date "2026-01-01" \
  --end-date "2026-01-31" \
  --format epa \
  --output /tmp/epa-report-jan2026.pdf
```

Report includes all required fields for EPA audits and state pesticide reporting.

#### 3. Worker Safety Compliance (OSHA)

**Step 1: Register Workers**

```bash
python3 scripts/register_worker.py \
  --name "Maria Garcia" \
  --employee-id "EMP-001" \
  --role "field-worker" \
  --hire-date "2025-03-15" \
  --h2a-visa "false"
```

**Step 2: Track Required Training**

For each worker, track required training:

```bash
# Add training record
python3 scripts/add_training.py \
  --worker-id "EMP-001" \
  --training-type "pesticide-handler" \
  --training-date "2025-03-20" \
  --trainer "Safety Coordinator" \
  --certificate-number "WPS-IL-001234" \
  --expiry-date "2026-03-20" \
  --hours 8
```

Training types tracked:
- Pesticide Handler Training (Worker Protection Standard)
- Pesticide Worker Training (Worker Protection Standard)
- Equipment Operation Safety
- Hazard Communication (HazCom)
- Emergency Response and Evacuation
- First Aid and CPR
- Heat Stress Prevention
- Machine Guarding and Lockout/Tagout

**Step 3: Monitor Training Expirations**

The system automatically:
- Tracks training expiration dates
- Sends reminders 30 days before expiration
- Flags workers with expired training for work restrictions
- Generates training schedule for upcoming month

```bash
# Get training status for all workers
python3 scripts/training_status.py --all

# Get expiring training for next 30 days
python3 scripts/training_status.py --expiring 30
```

**Step 4: Manage PPE Inventory**

```bash
# Add PPE to inventory
python3 scripts/add_ppe.py \
  --type "respirator" \
  --model "3M 7502" \
  --quantity 25 \
  --cost 45.00 \
  --expiration "2027-01-01"

# Assign PPE to worker
python3 scripts/assign_ppe.py \
  --worker-id "EMP-001" \
  --ppe-id "PPE-001" \
  --date "2025-03-20"
```

**Step 5: Maintain OSHA 300 Log**

```bash
# Record workplace injury
python3 scripts/osha300_log.py \
  --record-type "injury" \
  --date "2026-01-15" \
  --worker-id "EMP-005" \
  --description "Laceration to hand from equipment maintenance" \
  --injury-location "right-hand" \
  --days-away-from-work 2 \
  --days-job-transfer 0 \
  --days-restriction 3
```

Generate annual OSHA 300A summary for posting:

```bash
python3 scripts/gen_osha300a.py --year 2026
```

#### 4. Equipment Compliance

**Step 1: Register Equipment**

```bash
python3 scripts/register_equipment.py \
  --equipment-id "EQ-001" \
  --type "tractor" \
  --manufacturer "John Deere" \
  --model "8R 410" \
  --year 2023 \
  --serial-number "JD8R410-2023-00123"
```

**Step 2: Track Inspections and Certifications**

```bash
# Log annual inspection
python3 scripts/log_inspection.py \
  --equipment-id "EQ-001" \
  --inspection-type "annual" \
  --date "2026-01-15" \
  --inspector "Third-Party Inspection Service" \
  --result "pass" \
  --next-inspection "2027-01-15"

# Track emissions certification
python3/scripts/log_certification.py \
  --equipment-id "EQ-001" \
  --cert-type "emissions-tier4" \
  --cert-number "EPA-2023-00123" \
  --issue-date "2023-01-15" \
  --expiry-date "2033-01-15"
```

**Step 3: Monitor Permits**

```bash
# Add permit
python3 scripts/add_permit.py \
  --permit-id "PERMIT-001" \
  --type "overweight-load" \
  --equipment-id "EQ-001" \
  --issue-date "2026-01-01" \
  --expiry-date "2026-12-31" \
  --issuing-authority "IDOT" \
  --permit-number "IL-OW-2026-12345"
```

The system monitors:
- Permit expiration dates with reminders
- Weight and dimension limits
- Seasonal permit validity
- Route restrictions

**Step 4: Generate Equipment Compliance Report**

```bash
python3 scripts/gen_equipment_report.py \
  --equipment-id "EQ-001" \
  --compliance-check
```

Report includes:
- All current certifications and their expiry
- Upcoming inspection requirements
- Permit status and validity
- Maintenance compliance
- Outstanding compliance items

#### 5. Environmental Compliance

**Step 1: Nutrient Management Plan (NMP)**

```bash
# Define NMP parameters
python3 scripts/nutrient_plan.py \
  --plan-id "NMP-2026" \
  --acres 5000 \
  --total-nitrogen "150" \
  --units "lbs/acre" \
  --total-phosphorus "60" \
  --total-potassium "120" \
  --manure-source "swine" \
  --manure-application-limit "50" \
  --setbacks-from-water "100" \
  --setbacks-from-residences "300"
```

**Step 2: Track Manure and Nutrient Applications**

```bash
# Log manure application
python3 scripts/log_nutrient_application.py \
  --date "2026-01-20" \
  --field "South-80" \
  --crop "corn" \
  --source "swine-manure" \
  --application-rate "30" \
  --units "tons/acre" \
  --total-acres 80 \
  --method "injection" \
  --setbacks-maintained "true" \
  --buffer-zone "100"
```

**Step 3: Cover Crop and Conservation Tracking**

```bash
# Log cover crop planting
python3 scripts/log_cover_crop.py \
  --field "North-40" \
  --crop-type "winter-rye" \
  --planting-date "2025-10-15" \
  --target-date "2026-04-15" \
  --purpose "erosion-control" \
  --program-participation "EQIP-CSP"
```

**Step 4: Generate Environmental Compliance Report**

```bash
python3 scripts/gen_env_report.py \
  --start-date "2026-01-01" \
  --end-date "2026-01-31" \
  --format epa
```

Report includes:
- All nutrient applications (rates, locations, timing)
- Cover crop documentation
- Water quality monitoring data
- Buffer zone compliance
- Conservation practice verification

#### 6. Food Safety Compliance (FSMA)

**Step 1: Implement Traceability System**

```bash
# Create traceability lot
python3 scripts/create_lot.py \
  --lot-id "LOT-2026-CORN-001" \
  --field "North-40" \
  --crop "corn" \
  --planting-date "2026-05-01" \
  --variety "Dekalb DKC66-40"
```

**Step 2: Track Harvest and Distribution**

```bash
# Log harvest
python3 scripts/log_harvest.py \
  --lot-id "LOT-2026-CORN-001" \
  --harvest-date "2026-10-15" \
  --yield 240 \
  --units "bushels/acre" \
  --total-yield 9600 \
  --storage-location "Bin-1"

# Log distribution
python3 scripts/log_distribution.py \
  --lot-id "LOT-2026-CORN-001" \
  --recipient "ABC Grain Co-op" \
  --distribution-date "2026-10-20" \
  --quantity 5000 \
  --units "bushels" \
  --transport-method "truck"
```

**Step 3: Water Quality Testing**

```bash
# Add water test result
python3 scripts/add_water_test.py \
  --test-date "2026-01-15" \
  --source "irrigation-well-1" \
  --e-coli-result "negative" \
  --generic-e-coli "<10" \
  --ph 7.2 \
  --conductivity 450 \
  --test-lab "State Water Lab" \
  --result "pass"
```

FSMA requires:
- Generic E. coli testing for irrigation water
- Water quality documentation
- Treatment records if contamination detected
- Microbial water quality profiles

**Step 4: Generate FSMA Compliance Report**

```bash
python3 scripts/gen_fsma_report.py \
  --start-date "2026-01-01" \
  --end-date "2026-01-31"
```

Report includes:
- Traceability records from field to distribution
- Water quality test results
- Soil amendment and manure applications
- Equipment sanitation logs
- Worker health and hygiene training
- Recall planning documentation

#### 7. Government Program Compliance

**Step 1: Track NRCS Programs**

```bash
# Add program participation
python3 scripts/add_program.py \
  --program-id "EQIP-2026-001" \
  --program-name "EQIP" \
  --practice-code "329" \
  --practice-name "Irrigation Water Management" \
  --contract-start "2026-01-01" \
  --contract-end "2028-12-31" \
  --payment-amount 50000
```

**Step 2: Track Conservation Practices**

```bash
# Log practice implementation
python3 scripts/log_practice.py \
  --program-id "EQIP-2026-001" \
  --date "2026-05-01" \
  --description "Installed soil moisture sensors in North-40 field" \
  --equipment "soil-moisture-sensor-array" \
  --cost 15000
```

**Step 3: Generate Program Compliance Documentation**

```bash
python3 scripts/gen_program_report.py \
  --program-id "EQIP-2026-001" \
  --report-type "annual"
```

Report includes:
- Practice implementation verification
- Cost documentation
- Photos and documentation
- Practice maintenance records
- Payment eligibility verification

#### 8. Automated Reporting

**Step 1: Schedule Regular Reports**

```bash
# Schedule weekly compliance report
python3 scripts/schedule_report.py \
  --report-type "compliance-summary" \
  --frequency "weekly" \
  --day "friday" \
  --time "17:00" \
  --recipients "farm@valleyfarms.com,office@valleyfarms.com"
```

**Step 2: Generate Ad-Hoc Reports**

```bash
# Generate custom report
python3 scripts/gen_report.py \
  --type "chemical-applications" \
  --start-date "2026-01-01" \
  --end-date "2026-01-31" \
  --fields "North-40,South-80" \
  --products "Roundup PowerMAX,Liberty" \
  --format pdf \
  --output /tmp/chemical-report-jan2026.pdf
```

**Step 3: One-Click Audit Package**

```bash
# Generate complete audit package
python3 scripts/gen_audit_package.py \
  --year 2026 \
  --include "chemical-applications,training,equipment,environmental" \
  --output /tmp/audit-package-2026.zip
```

Audit package includes:
- All chemical application records
- Worker training documentation
- Equipment inspection and certification records
- Environmental compliance documentation
- FSMA traceability records
- Government program documentation
- Index and table of contents

## Tools

### Software Tools

**Core System:**
- **Python 3.8+** for compliance tracking engine
- **SQLite** for compliance database
- **PostgreSQL** (optional) for large-scale deployments
- **SQLite** for document storage

**Document Generation:**
- **ReportLab** for PDF generation
- **Jinja2** for report templates
- **Pandas** for data aggregation and analysis
- **NumPy** for calculations

**Data Processing:**
- **Pandas** for compliance data analysis
- **NumPy** for numerical calculations
- **Dateutil** for date and time calculations
- **Pytz** for timezone handling

**API Integrations:**
- **Requests** for API calls to regulatory systems
- **BeautifulSoup4** for web scraping (where allowed)
- **Selenium** (optional) for web-based submissions

**Email and Notifications:**
- **SMTPlib** for email alerts
- **APScheduler** for scheduled tasks
- **Twilio Python SDK** (optional) for SMS alerts

**Mapping and Geospatial:**
- **GeoPandas** for spatial data
- **Shapely** for geometric operations
- **Folium** for map generation (buffer zones, application areas)

### Hardware Requirements

**For On-Premise Deployment:**
- **Server:** Minimum 4 CPU cores, 16GB RAM (recommended 8 cores, 32GB)
- **Storage:** 1TB SSD for document storage and database
- **Network:** Gigabit Ethernet connection
- **UPS:** Uninterruptible power supply for data protection

**Optional Hardware:**
- **Document Scanner:** For digitizing paper records
- **Label Printer:** For chemical and equipment labeling
- **Mobile Devices:** Tablets/smartphones for field data capture

## Environment Variables

```bash
# ============================================
# Database Configuration
# ============================================

# Database type (sqlite, postgresql)
DB_TYPE=sqlite

# SQLite database path
DB_PATH=/opt/compliance-autopilot/compliance.db

# PostgreSQL connection (if using PostgreSQL)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=compliance_autopilot
DB_USER=compliance_user
DB_PASSWORD=change_me

# Document storage path
DOCUMENT_STORAGE=/opt/compliance-autopilot/documents

# ============================================
# Regulatory Data Sources
# ============================================

# Enable EPA database integration
EPA_INTEGRATION_ENABLED=true

# EPA API key (if available)
EPA_API_KEY=

# Enable state regulatory integration
STATE_INTEGRATION_ENABLED=true

# State abbreviation (for state-specific regulations)
STATE_ABBREVIATION=IL

# County name (for county-specific requirements)
COUNTY=Cook

# ============================================
# Weather Integration (for Application Records)
# ============================================

# Weather API provider (openweathermap, noaa, weatherbit)
WEATHER_PROVIDER=openweathermap

# OpenWeatherMap API key (free tier available)
WEATHER_API_KEY=

# Weather history provider (for past application records)
WEATHER_HISTORY_PROVIDER=noaa

# ============================================
# Chemical Application Tracking
# ============================================

# Enable ISOBUS/ISO 11783 automatic capture
ISOBUS_CAPTURE_ENABLED=true

# CAN interface for equipment data
CAN_INTERFACE=can0

# Application rate tolerance (percentage)
APPLICATION_RATE_TOLERANCE=5

# Weather condition enforcement (warn or block)
WEATHER_ENFORCEMENT=warn

# Maximum wind speed for spraying (MPH)
MAX_WIND_SPEED=10

# Minimum temperature for spraying (F)
MIN_TEMP_SPRAYING=40

# Maximum temperature for spraying (F)
MAX_TEMP_SPRAYING=95

# ============================================
# Worker Safety (OSHA)
# ============================================

# Training reminder days before expiration
TRAINING_REMINDER_DAYS=30

# Block work for expired training (true/false)
BLOCK_EXPIRED_TRAINING=false

# OSHA 300 log retention (years)
OSHA300_RETENTION_YEARS=5

# Incident report required for (all, lost-time, hospitalization)
INCIDENT_REPORTING=all

# ============================================
# Equipment Compliance
# ============================================

# Inspection reminder days before due
INSPECTION_REMINDER_DAYS=60

# Permit reminder days before expiration
PERMIT_REMINDER_DAYS=90

# Certification tracking (tier4, carb, local)
CERTIFICATION_TYPES=tier4,carb

# ============================================
# Environmental Compliance
# ============================================

# Nutrient Management Plan enabled
NMP_ENABLED=true

# Cover crop tracking enabled
COVER_CROP_ENABLED=true

# Water quality testing schedule (weekly, monthly, quarterly)
WATER_TEST_SCHEDULE=monthly

# Buffer zone enforcement (warn or block)
BUFFER_ENFORCEMENT=warn

# Minimum buffer zone (feet)
MINIMUM_BUFFER_ZONE=100

# ============================================
# FSMA Compliance
# ============================================

# Traceability system enabled
TRACEABILITY_ENABLED=true

# Lot tracking enabled
LOT_TRACKING_ENABLED=true

# Water testing interval (days)
WATER_TEST_INTERVAL_DAYS=30

# Mock recall frequency (per year)
MOCK_RECALL_FREQUENCY=1

# ============================================
# Government Programs
# ============================================

# NRCS program tracking enabled
NRCS_TRACKING_ENABLED=true

# USDA program tracking enabled
USDA_TRACKING_ENABLED=true

# State program tracking enabled
STATE_PROGRAM_TRACKING_ENABLED=true

# Cost-share documentation requirements
COST_SHARE_DOCUMENTATION=photos,receipts,implementation

# ============================================
# Reporting and Alerts
# ============================================

# Default report format (pdf, html, csv)
DEFAULT_REPORT_FORMAT=pdf

# Enable email alerts
ALERTS_EMAIL_ENABLED=false
ALERTS_EMAIL_SMTP=smtp.gmail.com
ALERTS_EMAIL_PORT=587
ALERTS_EMAIL_USERNAME=
ALERTS_EMAIL_PASSWORD=
ALERTS_EMAIL_FROM=Compliance Autopilot <compliance@farm.com>

# Enable SMS alerts (via Twilio)
ALERTS_SMS_ENABLED=false
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=
ALERTS_SMS_TO=+15551234567

# Enable webhook alerts
ALERTS_WEBHOOK_ENABLED=false
ALERTS_WEBHOOK_URL=https://hooks.slack.com/services/...

# ============================================
# Logging Configuration
# ============================================

# Log level (debug, info, warn, error)
LOG_LEVEL=info

# Log file path
LOG_FILE=/var/log/compliance-autopilot.log

# Maximum log file size (MB)
LOG_MAX_SIZE=100

# Number of log files to rotate
LOG_ROTATION=5

# ============================================
# Backup and Archive
# ============================================

# Automatic backup enabled
AUTO_BACKUP_ENABLED=true

# Backup interval (hours)
BACKUP_INTERVAL=24

# Backup directory
BACKUP_DIR=/opt/compliance-autopilot/backups

# Retention period (years)
DOCUMENT_RETENTION_YEARS=7

# Archive format (zip, tar.gz)
ARCHIVE_FORMAT=zip

# ============================================
# Advanced Configuration
# ============================================

# Timezone for reporting and deadlines
TIMEZONE=America/Chicago

# Date format for reports
DATE_FORMAT=%Y-%m-%d

# Enable multi-language support
MULTI_LANGUAGE_ENABLED=false

# Default language
DEFAULT_LANGUAGE=en

# Additional languages (comma-separated)
ADDITIONAL_LANGUAGES=es

# Debug mode
DEBUG=false
```

## Regulatory Requirements Summary

### EPA Regulations

**Federal Insecticide, Fungicide, and Rodenticide Act (FIFRA):**
- Restricted-use pesticides (RUP) require certified applicator
- All applications must be recorded within 14 days
- Records must be kept for 2 years
- Records must include: product name, EPA registration number, amount applied, location, date, time, applicator

**Clean Water Act:**
- Nutrient management for operations with 1000+ animal units
- Discharge permits for concentrated animal feeding operations (CAFOs)
- Stormwater management
- Spill Prevention, Control, and Countermeasure (SPCC) plans

**Clean Air Act:**
- Agricultural equipment emissions (Tier 4 compliance)
- Dust control for arid regions
- Pesticide drift regulations
- Air quality permits for large operations

### OSHA Regulations

**Worker Protection Standard (WPS):**
- Pesticide handler training (every 5 years)
- Pesticide worker training (every 5 years)
- PPE requirements and provision
- Decontamination facilities
- Notification of pesticide applications
- Restricted-entry intervals (REI)

**Hazard Communication Standard (HazCom):**
- Safety data sheets (SDS) accessible
- Chemical hazard labeling
- Training on chemical hazards
- Written hazard communication program

**Recordkeeping:**
- OSHA 300 log for injuries and illnesses
- Training records maintained
- PPE inspection records
- Exposure records (if applicable)

### FSMA (Food Safety Modernization Act)

**Produce Safety Rule:**
- Microbial water quality standards
- Soil amendments and manure application
- Worker health and hygiene
- Domesticated animals
- Equipment, tools, buildings, and sanitation
- Sprout production (if applicable)
- Traceability

**Records:**
- Water quality test results
- Soil amendment applications (manure, compost)
- Worker training records
- Equipment cleaning and sanitization
- Traceability from field to distribution

### State-Specific Regulations

**Illinois (Example):**
- Illinois Pesticide Act
- Nutrient Loss Reduction Strategy
- Illinois Environmental Protection Act
- Worker protection requirements may exceed federal

**California (Example - CARB):**
- Stricter pesticide regulations
- Air quality emissions
- Worker protection exceeds federal

**Iowa (Example):**
- Nutrient reduction strategy
- Water quality trading
- Conservation compliance requirements

### USDA Programs

**NRCS (Natural Resources Conservation Service):**
- EQIP (Environmental Quality Incentives Program)
- CSP (Conservation Stewardship Program)
- ACEP (Agricultural Conservation Easement Program)
- CRP (Conservation Reserve Program)
- Conservation practice compliance

**FSA (Farm Service Agency):**
- Crop insurance requirements
- Farm Bill program compliance
- Conservation compliance
- Payment eligibility

## Troubleshooting

### Common Issues

**Chemical Application Not Recorded:**
1. Check ISOBUS/ISO 11783 capture is enabled
2. Verify CAN interface is configured and working
3. Review equipment ISOBUS support and configuration
4. Check application data validation rules (rate limits, weather conditions)
5. Review logs for data capture errors

**Training Expirations Not Detected:**
1. Verify training records have valid expiry dates
2. Check training reminder settings in configuration
3. Review alert notification settings (email/SMS enabled)
4. Test alert delivery (send test alert)
5. Check calendar integration for reminders

**Reports Not Generating:**
1. Verify report templates exist and are valid
2. Check data availability for report period
3. Review report permissions (user has access)
4. Check storage location has sufficient disk space
5. Review error logs for template processing errors

**Audit Package Missing Documents:**
1. Verify documents are stored in correct directory
2. Check document indexing is up to date
3. Review document metadata for correct dates and categories
4. Verify document file formats are supported
5. Rebuild document index if necessary

**Weather Data Not Populating:**
1. Check weather API key is valid and not expired
2. Verify API quota not exceeded
3. Check network connectivity to weather service
4. Test API endpoint manually
5. Review weather provider settings for correct location

### Debug Mode

Enable debug mode for detailed logging:

```bash
# Set in .env
DEBUG=true
LOG_LEVEL=debug

# Or enable temporarily
python3 scripts/gen_report.py --debug
```

Debug logs include:
- Detailed compliance validation steps
- API request/response data
- Database query results
- Template processing details
- Error stack traces

## Testing

### Unit Testing

```bash
cd scripts
./test.sh --unit
```

Tests include:
- Compliance validation logic
- Report generation templates
- Deadline calculation accuracy
- Data validation rules
- Notification delivery

### Integration Testing

```bash
cd scripts
./test.sh --integration
```

Tests include:
- Regulatory API connectivity
- Weather service integration
- Email/SMS notification delivery
- Database operations
- Document storage and retrieval

### End-to-End Testing

```bash
cd scripts
./test.sh --e2e
```

Simulated compliance workflow:
- Chemical application logging and validation
- Training tracking and expiration alerts
- Equipment compliance monitoring
- Report generation and delivery
- Audit package creation
- Multi-regulation compliance

## Security and Data Privacy

### Data Protection

- Encrypt sensitive worker information at rest
- Use TLS for all API communications
- Implement access control based on roles
- Regular security audits and penetration testing
- Secure backup and restore procedures

### Compliance with Data Privacy Laws

- Comply with GDPR if processing EU worker data
- Comply with state privacy laws (CCPA, etc.)
- Implement data retention policies
- Provide data subject access requests
- Secure disposal of expired records

### Audit Trail

- Log all access to compliance data
- Track changes to compliance records
- Maintain immutable audit logs
- Provide tamper-evident record keeping
- Support forensic analysis for incidents

## References

### Regulatory Agencies

**Federal:**
- EPA: https://www.epa.gov/agriculture
- OSHA: https://www.osha.gov/agriculture
- USDA: https://www.usda.gov
- FSMA: https://www.fda.gov/food/food-safety-modernization-act-fsma

**State:**
- Illinois Department of Agriculture: https://agr.illinois.gov
- California Department of Pesticide Regulation: https://www.cdpr.ca.gov
- Iowa Department of Agriculture: https://www.iowaagriculture.gov

### Standards and Regulations

**EPA:**
- 40 CFR Part 170 (Worker Protection Standard)
- 40 CFR Part 112 (SPCC)
- 40 CFR Part 122 (NPDES)

**OSHA:**
- 29 CFR Part 1910 (General Industry)
- 29 CFR Part 1928 (Agriculture)

**FSMA:**
- 21 CFR Part 112 (Produce Safety Rule)
- 21 CFR Part 11 (Traceability)

**ISO Standards:**
- ISO 14001 (Environmental Management)
- ISO 45001 (Occupational Health and Safety)
- ISO 22000 (Food Safety)

### Academic Research

- "Compliance Costs in Agriculture: An Analysis of Regulatory Burden" (Agricultural Economics Review, 2022)
- "Digital Compliance Systems for Modern Farming" (Computers and Electronics in Agriculture, 2023)
- "Automated Compliance Tracking in Precision Agriculture" (Journal of Agricultural Systems, 2021)

### Industry Resources

- Agricultural Safety and Health Council
- National Association of State Departments of Agriculture (NASDA)
- American Farm Bureau Federation (regulatory resources)
- National Sustainable Agriculture Coalition (NSAC)

## Version History

- **1.0.0** - Initial release with EPA, OSHA, and FSMA compliance tracking

## License

MIT License - Open source, free to use, modify, and distribute.

## Support

For issues, questions, or contributions:
- GitHub Issues: https://github.com/farmfriend-labs/agent-skills-farming/issues
- Email: farmfriend.labs@gmail.com
