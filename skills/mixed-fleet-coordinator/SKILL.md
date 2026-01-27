# Mixed Fleet Coordinator

Coordinate mixed-brand smaller equipment for mid-size farms (100-2,000 acres) with different tractor and implement brands.

## Purpose

Enable mid-size farms to operate mixed-brand equipment efficiently without the complexity and cost of enterprise fleet management systems. Provide coordination capabilities that work across John Deere, Case IH, AGCO, Kubota, and other equipment brands.

## Problem Solved

Mid-size farms often have:
- Mixed equipment brands due to acquisitions, dealer availability, or budget constraints
- Difficulty scheduling operations across different equipment
- Incompatibility between brand-specific systems
- Lack of unified fleet visibility
- Inefficient equipment utilization

Farmers need:
- Single view of all equipment regardless of brand
- Cross-brand operation scheduling
- Equipment availability tracking
- Maintenance coordination
- Cost analysis by equipment piece

## Capabilities

### Equipment Inventory Management

**Equipment Registration**
- Register all equipment regardless of brand
- Store manufacturer, model, serial number
- Capture specifications (horsepower, PTO, hydraulics)
- Track equipment location and status
- Assign equipment to fields/operations

**Equipment Classification**
- Tractors (compact, utility, row crop)
- Implements (planters, drills, sprayers, combines)
- Support equipment (tillage, hay, harvest)
- Utility equipment (skid steers, loaders)

**Status Tracking**
- Available, In Use, Maintenance, Idle
- Location tracking (field, shop, storage)
- Fuel/fuel level monitoring
- Operating hours tracking
- Utilization metrics

### Operation Scheduling

**Cross-Brand Scheduling**
- Schedule operations across all equipment
- Assign equipment based on availability and capability
- Prevent double-booking of equipment
- Prioritize critical operations
- Adjust for weather and delays

**Field Operation Planning**
- Create operation sequences for each field
- Assign optimal equipment per operation
- Estimate operation duration
- Track progress in real-time
- Alert on schedule conflicts

**Resource Allocation**
- Match equipment to field requirements
- Consider equipment size vs field size
- Account for equipment capabilities
- Balance workload across equipment
- Optimize for efficiency

### Maintenance Coordination

**Maintenance Scheduling**
- Track maintenance schedules by equipment
- Alert based on hours, days, or usage
- Coordinate with operation schedules
- Schedule around critical operations
- Track maintenance history

**Service Provider Integration**
- Maintain list of service providers
- Schedule service appointments
- Track service costs
- Coordinate parts ordering
- Document service results

**Breakdown Management**
- Rapid breakdown logging
- Identify backup equipment options
- Reassign operations if needed
- Track downtime and costs
- Generate breakdown reports

### Performance Analytics

**Equipment Utilization**
- Track hours by equipment piece
- Calculate utilization percentage
- Compare actual vs planned usage
- Identify underutilized equipment
- Generate utilization reports

**Cost Analysis**
- Track costs by equipment piece
- Calculate cost per hour of operation
- Compare costs across equipment
- Identify high-cost equipment
- Generate cost optimization reports

**Efficiency Metrics**
- Work rate (acres/hour, tons/hour)
- Fuel efficiency (acres/gallon)
- Downtime percentage
- On-time completion rate
- Overall fleet efficiency

### Communication and Alerts

**Status Notifications**
- Equipment status changes
- Operation completion alerts
- Maintenance due reminders
- Breakdown notifications
- Schedule conflict alerts

**Operator Communication**
- Assign operators to equipment
- Send operation assignments
- Receive status updates
- Track operator hours
- Generate operator reports

**Integration Options**
- SMS/text notifications
- Email alerts
- Mobile app notifications
- Web dashboard access
- API integration

## Instructions

### Usage by AI Agent

#### 1. Initial Setup

**Register Equipment:**
```python
def register_equipment(equipment_data):
    """
    Register a new piece of equipment

    Args:
        equipment_data: Dictionary with equipment details
    Returns:
        equipment_id: ID of registered equipment
    """
    fields = [
        'name', 'manufacturer', 'model', 'serial_number',
        'equipment_type', 'horsepower', 'pto_hp', 'hydraulics',
        'fuel_type', 'year', 'purchase_date', 'purchase_price'
    ]

    # Validate required fields
    for field in ['name', 'manufacturer', 'model', 'equipment_type']:
        if field not in equipment_data:
            raise ValueError(f"Missing required field: {field}")

    # Insert into database
    equipment_id = db.insert('equipment', equipment_data)

    # Log registration
    log_event('equipment_registered', equipment_id, equipment_data)

    return equipment_id
```

**Import Equipment from Files:**
- CSV import from existing inventories
- JSON import from other systems
- Manual entry for individual pieces
- Bulk import for large fleets

**Configure Equipment Capabilities:**
- Compatible implements
- Field size limitations
- Operation types supported
- Attachment capabilities
- GPS/precision compatibility

#### 2. Operation Planning

**Create Operation Plan:**
1. Select field(s) for operation
2. Define operation type (planting, spraying, harvest, etc.)
3. Set operation window (start/end dates)
4. Assign priority level
5. Select required equipment
6. Estimate duration based on field size
7. Check equipment availability
8. Assign operators if needed
9. Save operation plan

**Validate Operation Plan:**
```python
def validate_operation_plan(operation_plan):
    """
    Validate operation plan for conflicts and feasibility

    Returns:
        dict: Validation results with warnings/errors
    """
    issues = []

    # Check equipment availability
    for equipment_id in operation_plan['equipment_ids']:
        if not is_equipment_available(
            equipment_id,
            operation_plan['start_date'],
            operation_plan['end_date']
        ):
            issues.append({
                'type': 'conflict',
                'equipment_id': equipment_id,
                'message': 'Equipment not available'
            })

    # Check operator availability
    for operator_id in operation_plan['operator_ids']:
        if not is_operator_available(
            operator_id,
            operation_plan['start_date'],
            operation_plan['end_date']
        ):
            issues.append({
                'type': 'conflict',
                'operator_id': operator_id,
                'message': 'Operator not available'
            })

    # Check equipment compatibility with field
    field = get_field(operation_plan['field_id'])
    for equipment_id in operation_plan['equipment_ids']:
        equipment = get_equipment(equipment_id)
        if not is_equipment_compatible(equipment, field):
            issues.append({
                'type': 'warning',
                'equipment_id': equipment_id,
                'message': 'Equipment may not be optimal for field size'
            })

    return {
        'valid': len([i for i in issues if i['type'] == 'error']) == 0,
        'issues': issues
    }
```

#### 3. Scheduling and Coordination

**Generate Schedule:**
1. Load all pending operations
2. Sort by priority and dependencies
3. Check equipment availability
4. Resolve conflicts
5. Assign dates and times
6. Generate schedule view
7. Send notifications to operators

**Monitor Operations:**
- Track operation progress
- Update equipment status
- Log completion times
- Record any issues
- Update inventory usage

**Handle Schedule Changes:**
```python
def reschedule_operation(operation_id, new_start_date, new_end_date, reason):
    """
    Reschedule an operation and handle dependent operations

    Args:
        operation_id: ID of operation to reschedule
        new_start_date: New start date/time
        new_end_date: New end date/time
        reason: Reason for rescheduling
    """
    # Get operation details
    operation = get_operation(operation_id)

    # Check for conflicts with new dates
    conflicts = check_schedule_conflicts(
        operation['equipment_ids'],
        operation['operator_ids'],
        new_start_date,
        new_end_date
    )

    if conflicts:
        raise ScheduleConflictError(conflicts)

    # Reschedule the operation
    update_operation(operation_id, {
        'start_date': new_start_date,
        'end_date': new_end_date,
        'status': 'rescheduled',
        'reschedule_reason': reason
    })

    # Check for dependent operations
    dependencies = get_dependent_operations(operation_id)
    for dep_op in dependencies:
        # Propagate reschedule to dependent operations
        shift_operation(
            dep_op['id'],
            new_end_date - operation['end_date'],
            f"Dependent operation rescheduled: {reason}"
        )

    # Send notifications
    notify_stakeholders(
        'operation_rescheduled',
        operation_id,
        {'new_dates': (new_start_date, new_end_date), 'reason': reason}
    )
```

#### 4. Maintenance Management

**Track Maintenance Needs:**
```python
def check_maintenance_due():
    """
    Check for equipment requiring maintenance

    Returns:
        list: Equipment IDs requiring maintenance
    """
    due_for_maintenance = []

    equipment_list = get_all_equipment()

    for equipment in equipment_list:
        # Check hour-based maintenance
        if equipment['current_hours'] >= equipment['maintenance_hours']:
            due_for_maintenance.append({
                'equipment_id': equipment['id'],
                'type': 'hour_based',
                'current_hours': equipment['current_hours'],
                'maintenance_hours': equipment['maintenance_hours']
            })

        # Check time-based maintenance
        days_since_service = (
            datetime.now() - equipment['last_service_date']
        ).days
        if days_since_service >= equipment['maintenance_days']:
            due_for_maintenance.append({
                'equipment_id': equipment['id'],
                'type': 'time_based',
                'days_since': days_since_service,
                'maintenance_days': equipment['maintenance_days']
            })

        # Check usage-based maintenance
        if equipment['usage_count'] >= equipment['maintenance_usage']:
            due_for_maintenance.append({
                'equipment_id': equipment['id'],
                'type': 'usage_based',
                'current_usage': equipment['usage_count'],
                'maintenance_usage': equipment['maintenance_usage']
            })

    return due_for_maintenance
```

**Schedule Maintenance:**
1. Identify equipment needing maintenance
2. Find optimal maintenance window
3. Check for conflicts with operations
4. Schedule maintenance appointment
5. Notify operator and mechanic
6. Track maintenance completion
7. Update equipment status

#### 5. Performance Analysis

**Generate Utilization Report:**
```python
def generate_utilization_report(start_date, end_date, equipment_ids=None):
    """
    Generate equipment utilization report

    Args:
        start_date: Report start date
        end_date: Report end date
        equipment_ids: Optional list of equipment IDs

    Returns:
        dict: Utilization data by equipment
    """
    report = {}

    # Get equipment to report on
    if equipment_ids:
        equipment_list = [get_equipment(id) for id in equipment_ids]
    else:
        equipment_list = get_all_equipment()

    for equipment in equipment_list:
        # Calculate total available hours
        total_days = (end_date - start_date).days
        available_hours = total_days * 24  # Simplified

        # Get operations for this equipment
        operations = get_operations_for_equipment(
            equipment['id'],
            start_date,
            end_date
        )

        # Calculate used hours
        used_hours = sum(
            (op['end_time'] - op['start_time']).total_seconds() / 3600
            for op in operations
        )

        # Calculate utilization
        utilization = (used_hours / available_hours) * 100 if available_hours > 0 else 0

        report[equipment['id']] = {
            'name': equipment['name'],
            'manufacturer': equipment['manufacturer'],
            'model': equipment['model'],
            'available_hours': available_hours,
            'used_hours': used_hours,
            'utilization_percent': utilization,
            'operation_count': len(operations)
        }

    return report
```

**Calculate Cost Per Hour:**
```python
def calculate_cost_per_hour(equipment_id, period_start, period_end):
    """
    Calculate operating cost per hour for equipment

    Args:
        equipment_id: Equipment ID
        period_start: Period start date
        period_end: Period end date

    Returns:
        float: Cost per hour
    """
    equipment = get_equipment(equipment_id)

    # Get operating hours for period
    operations = get_operations_for_equipment(
        equipment_id,
        period_start,
        period_end
    )
    operating_hours = sum(
        (op['end_time'] - op['start_time']).total_seconds() / 3600
        for op in operations
    )

    # Get costs for period
    costs = {
        'fuel': get_fuel_costs(equipment_id, period_start, period_end),
        'maintenance': get_maintenance_costs(equipment_id, period_start, period_end),
        'repairs': get_repair_costs(equipment_id, period_start, period_end),
        'depreciation': calculate_depreciation(equipment, period_start, period_end)
    }

    total_cost = sum(costs.values())

    if operating_hours > 0:
        cost_per_hour = total_cost / operating_hours
    else:
        cost_per_hour = 0

    return {
        'equipment_id': equipment_id,
        'period': (period_start, period_end),
        'operating_hours': operating_hours,
        'costs': costs,
        'total_cost': total_cost,
        'cost_per_hour': cost_per_hour
    }
```

### Implementation Checklist

**Data Collection:**
- [ ] List all equipment (brand, model, serial)
- [ ] Capture equipment specifications
- [ ] Record current hours/usage
- [ ] Note maintenance history
- [ ] Document service providers

**System Setup:**
- [ ] Register all equipment in system
- [ ] Import field boundaries
- [ ] Define operation types
- [ ] Configure notification settings
- [ ] Set up user accounts

**Integration:**
- [ ] Connect to GPS systems (if available)
- [ ] Import maintenance schedules
- [ ] Configure alert thresholds
- [ ] Set up report schedules
- [ ] Train operators on system

**Testing:**
- [ ] Test equipment registration
- [ ] Validate operation scheduling
- [ ] Test conflict detection
- [ ] Verify maintenance alerts
- [ ] Check report generation

## Tools

### Software Tools

- **Python 3.8+** for data processing and automation
- **SQLite** for local data storage
- **PostgreSQL** (optional) for advanced multi-user setups
- **Pandas** for data analysis and reporting
- **Matplotlib** for visualization

### Hardware Tools

- **Tablets/laptops** for operator interfaces
- **GPS receivers** (optional) for location tracking
- **CAN interfaces** (optional) for equipment communication

### APIs and Data Sources

- Weather APIs for schedule optimization
- Equipment manufacturer APIs (if available)
- SMS/email services for notifications

## Environment Variables

```bash
# ============================================
# Database Configuration
# ============================================

# Database type: sqlite, postgresql
DB_TYPE=sqlite

# SQLite database path
DB_PATH=/var/lib/mixed-fleet/fleet.db

# PostgreSQL configuration (if using)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mixed_fleet
DB_USER=fleet_user
DB_PASSWORD=secure_password

# ============================================
# Notification Settings
# ============================================

# Enable SMS notifications
SMS_ENABLED=false

# SMS service provider: twilio, plivo, nexmo
SMS_PROVIDER=twilio

# SMS credentials
SMS_ACCOUNT_SID=
SMS_AUTH_TOKEN=
SMS_PHONE_NUMBER=

# Email notifications
EMAIL_ENABLED=true
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_USERNAME=
EMAIL_PASSWORD=
EMAIL_FROM=Fleet Coordinator <fleet@farm.com>

# ============================================
# Scheduling Configuration
# ============================================

# Default operation priority
DEFAULT_PRIORITY=medium

# Schedule conflict resolution strategy
# Options: prioritize_priority, prioritize_first, manual
CONFLICT_RESOLUTION=prioritize_priority

# Auto-reschedule operations
AUTO_RESCHEDULE=false

# Notify operators of assignments
NOTIFY_OPERATORS=true

# ============================================
# Maintenance Configuration
# ============================================

# Maintenance reminder lead time (in days)
MAINTENANCE_REMINDER_DAYS=7

# Maintenance scheduling buffer (in days)
MAINTENANCE_BUFFER_DAYS=2

# Track utilization
TRACK_UTILIZATION=true

# Utilization calculation period (in days)
UTILIZATION_PERIOD=30

# ============================================
# Reporting Configuration
# ============================================

# Default report format
# Options: pdf, html, csv, json
DEFAULT_REPORT_FORMAT=pdf

# Report output directory
REPORT_OUTPUT_DIR=/var/lib/mixed-fleet/reports

# Schedule automatic reports
AUTO_REPORTS=false

# Report generation schedule (cron format)
REPORT_SCHEDULE="0 8 * * 1"  # 8 AM every Monday

# ============================================
# GPS and Location Tracking
# ============================================

# Enable GPS tracking
GPS_TRACKING_ENABLED=false

# GPS update interval (in seconds)
GPS_UPDATE_INTERVAL=300

# GPS accuracy threshold (in meters)
GPS_ACCURACY_THRESHOLD=10

# ============================================
# Logging Configuration
# ============================================

# Log level: debug, info, warn, error
LOG_LEVEL=info

# Log file path
LOG_FILE=/var/log/mixed-fleet/fleet.log

# Maximum log file size (in MB)
LOG_MAX_SIZE=100

# Number of log files to rotate
LOG_ROTATION=5

# ============================================
# Backup and Recovery
# ============================================

# Enable automatic backups
AUTO_BACKUP_ENABLED=true

# Backup interval (in hours)
BACKUP_INTERVAL=24

# Backup location
BACKUP_PATH=/var/backups/mixed-fleet

# Number of backups to keep
BACKUP_RETENTION=30

# ============================================
# API Configuration (Optional)
# ============================================

# Weather API
WEATHER_API_PROVIDER=openmeteo
WEATHER_API_KEY=

# Equipment manufacturer APIs
JOHN_DEERE_API_KEY=
CASE_IH_API_KEY=
AGCO_API_KEY=

# ============================================
# Security Settings
# ============================================

# Enable user authentication
AUTH_ENABLED=true

# Session timeout (in minutes)
SESSION_TIMEOUT=60

# Password requirements
PASSWORD_MIN_LENGTH=8
PASSWORD_REQUIRE_SPECIAL=true

# ============================================
# Development Settings
# ============================================

# Enable debug mode
DEBUG_MODE=false

# Offline mode (no external API calls)
OFFLINE_MODE=true

# Development/test mode
DEV_MODE=false
```

## Common Implementations

### Scenario 1: Grain Operation (1,200 acres)

**Equipment:**
- 3 tractors (2 JD, 1 Case IH)
- Planter (16-row)
- Drill (20-foot)
- Sprayer (40-foot)
- Combine (2 units, different brands)
- Tillage equipment (multiple brands)

**Coordination Needs:**
- Schedule planting across 6 fields
- Coordinate sprayer and planter
- Manage combine fleet during harvest
- Track equipment hours
- Schedule maintenance around planting/harvest

**Implementation:**
- Register all 15+ equipment pieces
- Create operation schedules for each field
- Set up maintenance alerts
- Generate utilization reports monthly
- Track costs by equipment

### Scenario 2: Vegetable Operation (150 acres)

**Equipment:**
- 2 compact tractors (different brands)
- Transplanter
- Small sprayer
- Small combine
- Utility equipment

**Coordination Needs:**
- Tight planting windows for succession planting
- Frequent equipment changes
- Maintenance coordination
- Utilization tracking

**Implementation:**
- Focus on schedule flexibility
- Quick reassignment of equipment
- Maintenance between plantings
- Detailed cost tracking

### Scenario 3: Mixed Crop/Dairy (500 acres)

**Equipment:**
- 4 tractors (3 different brands)
- Planter, drill, sprayer
- Hay equipment
- Manure spreader
- TMR mixer
- Utility equipment

**Coordination Needs:**
- Coordinate crops and hay operations
- Balance dairy and crop work
- Track equipment sharing
- Manage maintenance

**Implementation:**
- Separate crop and dairy schedules
- Shared equipment allocation
- Prevent conflicts
- Track utilization

## Best Practices

### Equipment Registration

1. **Be thorough with specifications:**
   - Record all relevant specs
   - Include limitations
   - Note compatibility issues
   - Add custom equipment capabilities

2. **Standardize naming:**
   - Use consistent naming convention
   - Include manufacturer and model
   - Add distinguishing features
   - Example: "JD 8370R - Row Crop"

3. **Track from day one:**
   - Register immediately on acquisition
   - Document purchase details
   - Start tracking hours
   - Note initial condition

### Scheduling

1. **Plan for contingencies:**
   - Build in buffer time
   - Have backup equipment options
   - Consider weather delays
   - Allow for breakdowns

2. **Prioritize wisely:**
   - Critical operations get priority
   - Weather-sensitive operations first
   - Time-sensitive operations flagged
   - Balance across equipment

3. **Communicate clearly:**
   - Notify operators early
   - Provide clear instructions
   - Confirm assignments
   - Follow up on completion

### Maintenance

1. **Stay ahead of issues:**
   - Schedule preventive maintenance
   - Monitor for warning signs
   - Track recurring problems
   - Plan for major services

2. **Document everything:**
   - Log all maintenance
   - Track costs
   - Record parts used
   - Note technician observations

3. **Coordinate with operations:**
   - Schedule maintenance during downtime
   - Avoid critical operation windows
   - Plan backup equipment
   - Communicate with operators

### Analysis

1. **Review regularly:**
   - Monthly utilization reports
   - Quarterly cost analysis
   - Annual efficiency review
   - Equipment replacement planning

2. **Look for patterns:**
   - Underutilized equipment
   - High-cost equipment
   - Frequent breakdowns
   - Maintenance trends

3. **Take action:**
   - Sell or repurpose underutilized equipment
   - Repair or replace high-cost equipment
   - Address recurring maintenance issues
   - Adjust practices based on data

## Troubleshooting

### Common Issues

**Problem: Schedule conflicts**

Possible causes:
- Equipment double-booked
- Operator assigned to multiple operations
- Inadequate time estimates
- Unexpected delays

Solutions:
1. Use conflict detection feature
2. Adjust operation priorities
3. Add buffer time between operations
4. Have backup equipment ready

**Problem: Low equipment utilization**

Possible causes:
- Too much equipment for operation size
- Equipment not suited to available work
- Poor scheduling
- Seasonal variations

Solutions:
1. Analyze utilization reports
2. Consider selling underutilized equipment
3. Improve scheduling efficiency
4. Look for custom work opportunities

**Problem: Unexpected breakdowns**

Possible causes:
- Inadequate maintenance
- Equipment age
- Operator error
- Unexpected failures

Solutions:
1. Improve preventive maintenance
2. Track breakdown patterns
3. Provide operator training
4. Plan for quick repairs

## Examples

See examples/ directory for:
- Equipment registration walkthrough
- Operation scheduling example
- Maintenance coordination workflow
- Utilization report example
- Cost analysis example

## References

### Manufacturer Documentation

See references/ directory for:
- Equipment specifications by manufacturer
- Maintenance schedule recommendations
- Cost data resources
- Best practices guides

## Version History

- **1.0.0** - Initial release with core coordination features

## License

MIT License - Open source, free to use, modify, and distribute.

## Support

For issues, questions, or contributions:
- GitHub Issues: https://github.com/farmfriend-labs/agent-skills-farming/issues
- Email: farmfriend.labs@gmail.com
