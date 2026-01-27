# Grant Money Finder

Find and track agricultural grants, funding opportunities, and financial assistance programs for farmers.

## Purpose

Discover and manage applications for agricultural grants, cost-share programs, low-interest loans, and other funding opportunities that help farmers invest in equipment, conservation, renewable energy, and business development. Reduce the time spent searching for funding and increase success rates through organized tracking and application support.

## Problem Solved

Farmers miss out on thousands of dollars in available funding because:
- Grants are scattered across dozens of websites (USDA, state, nonprofits)
- Application deadlines are missed due to poor tracking
- Complex application requirements are overwhelming
- Eligibility requirements are confusing or misunderstood
- Farmers lack time to research and complete applications
- Matching fund requirements are difficult to navigate
- Past applications are not tracked for learning

Grant Money Finder centralizes grant discovery, eligibility screening, deadline tracking, and application management in one place.

## Capabilities

- **Grant Discovery:** Search federal, state, and private grant databases
- **Eligibility Screening:** Match farm characteristics to grant requirements
- **Deadline Tracking:** Monitor application deadlines and submission requirements
- **Application Management:** Track application status, documents, and follow-up actions
- **Document Templates:** Library of common application documents
- **Cost-Share Calculator:** Calculate matching fund requirements
- **Application Calendar:** View all upcoming deadlines in one place
- **Grant Alerts:** Notifications for new grants matching your profile
- **Application Support:** AI-assisted writing for grant narratives
- **Success Rate Tracking:** Track application outcomes and improve future attempts
- **Collaboration Tools:** Share applications with consultants or partners
- **Document Repository:** Store all grant-related documents in one place
- **Deadline Reminders:** Automated reminders before deadlines

## Instructions

### Usage by AI Agent

1. **Create Farm Profile**
   - Capture farm location, size, type (crop, livestock, mixed)
   - Record business structure (sole proprietor, LLC, corporation)
   - Document current production and revenue levels
   - Note ownership status (owned, rented, tenant)
   - Track certifications (organic, GAP, other)
   - Record conservation practices already implemented
   - Identify equipment needs and improvement projects

2. **Search for Grants**
   - Query grant databases by farm characteristics
   - Filter by eligibility, funding amount, deadline, category
   - Search by keywords (equipment, conservation, energy, research)
   - Filter by organization type (federal, state, nonprofit, private)
   - Prioritize by fit score and likelihood of success

3. **Screen Eligibility**
   - Compare farm profile to grant requirements
   - Identify required certifications or documentation
   - Calculate matching fund requirements and feasibility
   - Check previous award history restrictions
   - Assess application complexity and time required

4. **Track Applications**
   - Create application records for pursued grants
   - Set up deadline reminders and task lists
   - Generate required documents from templates
   - Track submission status and follow-up dates
   - Store all application materials in organized structure

5. **Write Grant Narratives**
   - Generate draft narratives based on farm profile
   - Tailor language to grant agency priorities
   - Incorporate supporting data and statistics
   - Ensure compliance with word counts and formatting
   - Review for completeness and clarity

6. **Monitor and Follow Up**
   - Track award announcement dates
   - Prepare for post-award reporting requirements
   - Track award amounts and disbursement dates
   - Maintain records for future applications

### Grant Categories

**Equipment and Infrastructure:**
- Tractor and equipment purchase assistance
- Irrigation system installation
- Grain storage and handling facilities
- Renewable energy systems (solar, wind, biogas)
- Processing and value-added equipment

**Conservation and Environment:**
- NRCS Conservation Stewardship Program (CSP)
- EQIP - Environmental Quality Incentives Program
- Soil health improvement
- Water quality protection
- Wildlife habitat improvement
- Cover crop cost-share
- Nutrient management planning

**Business Development:**
- USDA Value-Added Producer Grant (VAPG)
- Beginning Farmer and Rancher Development Program
- Business planning assistance
- Marketing and promotion grants
- Cooperative development

**Research and Innovation:**
- Sustainable Agriculture Research and Education (SARE)
- Specialty Crop Block Grants
- Organic research and education
- Precision agriculture technology
- Climate-smart agriculture

**Disaster and Emergency:**
- Emergency Conservation Program (ECP)
- Livestock Forage Disaster Program
- Noninsured Crop Disaster Assistance (NAP)
- Emergency loans from FSA

**Energy Efficiency:**
- Rural Energy for America Program (REAP)
- Energy audit cost-share
- Energy efficiency improvements
- Renewable energy systems

### Application Process

**Preparation:**
1. Complete farm profile
2. Gather financial records (tax returns, balance sheets)
3. Document conservation practices
4. Prepare maps and field information
5. Collect certifications and licenses

**Application:**
1. Register with granting agency (SAM.gov for federal grants)
2. Complete application forms
3. Write grant narrative
4. Prepare budget and cost-share documentation
5. Submit before deadline
6. Follow up on submission confirmation

**Post-Submission:**
1. Track application status
2. Respond to agency questions
3. Prepare for potential site visits
4. Await award decision
5. Complete post-award reporting if awarded

## Tools

- **Python 3.8+** for data management and web scraping
- **SQLite** for grant and application database
- **Requests** for accessing grant APIs
- **BeautifulSoup** for scraping grant websites
- **Dateutil** for deadline calculations and reminders
- **Pandas** for grant data analysis
- **ReportLab** for generating application documents
- **NLTK/TextBlob** for grant writing assistance

## Environment Variables

```bash
# Database Configuration
GRANT_DB_PATH=/opt/grant-finder/grants.db
BACKUP_PATH=/opt/grant-finder/backups
AUTO_BACKUP_ENABLED=true

# Grant Sources
USDA_GRANTS_API_KEY=
GRANTS_GOV_API_KEY=
STATE_GRANT_SOURCES=

# Notification Settings
NOTIFICATION_ENABLED=false
NOTIFICATION_EMAIL=
NOTIFICATION_DAYS_BEFORE_DEADLINE=14

# Calendar Integration
CALENDAR_TYPE=google  # google, outlook, none
GOOGLE_CALENDAR_API_KEY=
GOOGLE_CALENDAR_ID=

# Document Storage
DOCUMENT_PATH=/opt/grant-finder/documents
TEMPLATE_PATH=/opt/grant-finder/templates

# Logging
LOG_LEVEL=info
LOG_FILE=/var/log/grant-money-finder.log
```

## Database Schema

### Grants Table
```sql
CREATE TABLE grants (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  organization TEXT NOT NULL,
  type TEXT,  -- federal, state, nonprofit, private
  category TEXT NOT NULL,
  description TEXT,
  funding_min REAL,
  funding_max REAL,
  application_deadline DATE,
  award_date DATE,
  eligibility_requirements TEXT,
  required_documents TEXT,
  match_requirement REAL,
  url TEXT,
  contact_email TEXT,
  contact_phone TEXT,
  status TEXT,  -- open, closed, upcoming
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Applications Table
```sql
CREATE TABLE applications (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  grant_id INTEGER NOT NULL,
  application_name TEXT NOT NULL,
  submission_date DATE,
  status TEXT,  -- planning, drafting, submitted, under_review, awarded, rejected
  award_amount REAL,
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (grant_id) REFERENCES grants(id)
);
```

### Application Tasks Table
```sql
CREATE TABLE application_tasks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  application_id INTEGER NOT NULL,
  task_name TEXT NOT NULL,
  due_date DATE,
  completed BOOLEAN DEFAULT FALSE,
  notes TEXT,
  FOREIGN KEY (application_id) REFERENCES applications(id)
);
```

### Farm Profile Table
```sql
CREATE TABLE farm_profile (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  farm_name TEXT NOT NULL,
  owner_name TEXT NOT NULL,
  business_type TEXT,
  farm_size REAL,
  farm_size_unit TEXT,
  location_city TEXT,
  location_state TEXT,
  location_county TEXT,
  farm_type TEXT,
  annual_revenue REAL,
  years_in_operation INTEGER,
  certifications TEXT,
  conservation_practices TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Application Documents Table
```sql
CREATE TABLE application_documents (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  application_id INTEGER NOT NULL,
  document_type TEXT NOT NULL,
  file_path TEXT,
  description TEXT,
  uploaded_date DATE,
  FOREIGN KEY (application_id) REFERENCES applications(id)
);
```

### Grant Alerts Table
```sql
CREATE TABLE grant_alerts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  grant_id INTEGER NOT NULL,
  alert_type TEXT,  -- deadline, new, updated
  alert_date DATE,
  sent BOOLEAN DEFAULT FALSE,
  FOREIGN KEY (grant_id) REFERENCES grants(id)
);
```

## Key Grant Programs

### Federal Programs

**USDA NRCS:**
- Conservation Stewardship Program (CSP)
- Environmental Quality Incentives Program (EQIP)
- Agricultural Conservation Easement Program (ACEP)

**USDA FSA:**
- Direct Farm Ownership Loan
- Operating Loan
- Emergency Conservation Program
- Noninsured Crop Disaster Assistance (NAP)

**USDA RD:**
- Rural Energy for America Program (REAP)
- Value-Added Producer Grant (VAPG)
- Beginning Farmer and Rancher Development Program

**SARE:**
- Farmer/Rancher Grant
- Partnership Grant
- Research and Education Grant

### State Programs

Check your state's department of agriculture for:
- Conservation cost-share programs
- Beginning farmer programs
- Value-added agriculture grants
- Specialty crop block grants
- Agricultural innovation grants

### Private and Nonprofit

- American Farmland Trust grants
- Sustainable Agriculture Research & Education
- Regional food system grants
- Local foundation grants

## Application Writing Tips

**Narrative Structure:**
1. Introduction and farm background
2. Problem or opportunity description
3. Proposed solution or project
4. Expected outcomes and benefits
5. Qualifications and capacity
6. Budget and timeline
7. Sustainability and long-term impact

**Key Elements to Include:**
- Specific, measurable objectives
- Clear timeline with milestones
- Detailed budget with justification
- Relevant experience and past successes
- Community or environmental benefits
- Partners and collaborators
- Evaluation metrics

**Common Mistakes to Avoid:**
- Missing required sections
- Exceeding word or page limits
- Incomplete budget information
- Vague descriptions
- Not following agency guidelines
- Submitting past deadline
- Missing signatures or required attachments

## Examples

See examples/ directory for:
- Finding relevant grants
- Creating a farm profile
- Managing application deadlines
- Writing grant narratives
- Post-award reporting

## References

### Official Sources
- **Grants.gov:** Federal grant database
- **USDA.gov:** All USDA grant programs
- **State Agriculture Departments:** State-specific programs
- **National Sustainable Agriculture Coalition:** Grant resources

### Application Help
See references/application-help.md for:
- Grant writing resources
- Cost-share program guides
- Application checklists
- Sample successful applications

## Troubleshooting

### Eligibility Confusion

**Check:**
- Are you interpreting requirements correctly?
- Have you reviewed the official guidelines?
- Are there exceptions or special cases?

**Solutions:**
- Contact the granting agency for clarification
- Review FAQs and previous program guidelines
- Consult with extension agent or grant writer

### Application Rejected

**Common Reasons:**
- Incomplete application
- Did not meet eligibility
- Weak narrative or justification
- Budget not well explained
- Missing documentation

**Actions:**
- Request feedback from agency
- Address deficiencies for next cycle
- Consider other grant programs
- Document lessons learned

### Missing Deadlines

**Prevention:**
- Set reminders 2 weeks before deadline
- Track all steps in application process
- Build in buffer time for technical issues

**Recovery:**
- Check if late submissions accepted
- Plan for next funding cycle
- Improve tracking system

## Testing

1. **Unit Testing**
   - Test grant database queries
   - Verify deadline calculations
   - Test eligibility matching logic

2. **Integration Testing**
   - Test grant discovery from APIs
   - Verify email notifications
   - Test document generation

3. **Data Quality Testing**
   - Validate grant data accuracy
   - Check for duplicate entries
   - Test alert system

## Version History

- **1.0.0** - Initial release with grant discovery and tracking

## License

MIT License - Open source, free to use, modify, and distribute.

## Support

For issues, questions, or contributions:
- GitHub Issues: https://github.com/farmfriend-labs/agent-skills-farming/issues
- Email: farmfriend.labs@gmail.com
