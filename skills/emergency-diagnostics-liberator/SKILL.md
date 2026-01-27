# Emergency Diagnostics Liberator

Emergency equipment diagnostics without dealer tools, providing farmers with immediate access to diagnostic information, error code interpretation, and repair guidance when equipment fails during critical operations.

## Purpose

Provide immediate, on-farm diagnostic capabilities for agricultural equipment when dealer diagnostic tools are unavailable, too expensive, or inaccessible. This skill empowers farmers to read error codes, interpret them, and make informed repair decisions during time-sensitive operations like harvest or planting.

## Problem Solved

When agricultural equipment breaks down during critical operations, farmers face an impossible choice: wait hours or days for dealer technicians with proprietary diagnostic tools, or attempt blind repairs that may cause further damage. Dealer diagnostic software costs $3,000-$15,000 and often requires subscription fees. Emergency service calls cost $200-$500 per hour plus travel. Every hour of downtime during harvest can cost $1,000-$5,000 in lost production. This skill provides immediate diagnostic access using open-source tools and standard OBD-II/CAN interfaces.

## Capabilities

- Read and clear diagnostic trouble codes (DTCs) from equipment ECUs
- Interpret manufacturer-specific and generic OBD-II codes
- Provide code descriptions, severity levels, and common causes
- Suggest potential repairs based on code analysis
- Monitor real-time sensor data and ECU parameters
- Perform basic system tests and actuator tests
- Generate diagnostic reports for record-keeping
- Support multiple manufacturers through protocol adapters
- Work with standard OBD-II adapters and CAN interfaces
- Provide offline operation with cached code database
- Identify safety-critical codes requiring professional service
- Track code history and recurrence patterns
- Export data for sharing with dealers or independent mechanics
- Create maintenance schedules based on diagnostic patterns

## Instructions

### Usage by AI Agent

1. **Assess Emergency Situation**
   - Determine equipment type (tractor, combine, sprayer, etc.)
   - Identify symptoms and failure mode
   - Check operator-reported warning lights or messages
   - Document time of failure and operating conditions

2. **Connect Diagnostic Interface**
   - Locate OBD-II or diagnostic port on equipment
   - Connect compatible CAN/OBD adapter
   - Verify communication with vehicle network
   - Check for power and ground connections

3. **Identify Equipment Protocol**
   - Scan available ECUs on the network
   - Determine manufacturer (John Deere, Case IH, AGCO, etc.)
   - Select appropriate protocol profile
   - Load manufacturer-specific code definitions

4. **Read Diagnostic Trouble Codes**
   - Query all ECUs for stored codes
   - Capture pending and confirmed codes
   - Check for historical/cleared codes
   - Document code counts and severity

5. **Analyze Codes**
   - Look up code definitions from database
   - Cross-reference manufacturer-specific codes
   - Identify related systems and components
   - Determine safety-critical vs. non-critical codes

6. **Check Sensor Data**
   - Read live data from affected systems
   - Compare values to normal ranges
   - Identify out-of-spec parameters
   - Look for sensor drift or failure patterns

7. **Provide Diagnostic Guidance**
   - Explain code meaning in plain language
   - Identify most likely causes ranked by probability
   - Suggest safe diagnostic tests the operator can perform
   - Recommend immediate actions vs. deferred repairs

8. **Generate Report**
   - Create comprehensive diagnostic report
   - Include codes, definitions, and recommendations
   - Capture sensor snapshots and test results
   - Save timestamp and equipment information

9. **Clear Codes (If Appropriate)**
   - Verify repairs are complete
   - Confirm no safety concerns exist
   - Clear codes and verify they don't return
   - Monitor for code recurrence

### Safety Considerations

- Never clear safety-critical codes without proper repairs
- Do not override ECU safety limits or fault conditions
- Provide clear warnings when professional service is required
- Do not suggest repairs beyond operator capability level
- Always document diagnostic sessions for liability protection
- Verify equipment is in safe state before clearing codes
- Respect manufacturer warranty requirements

## Tools

- **Python 3.8+** for diagnostic communication and analysis
- **CAN/OBD-II interface hardware** (ELM327, OBDLink, CANUSB, etc.)
- **python-obd** library for OBD-II communication
- **python-can** library for direct CAN bus access
- **SQLite** for code database and diagnostic history
- **pyserial** for serial port communication with adapters
- **pandas** for data analysis and pattern detection
- **matplotlib** for diagnostic visualization

## Environment Variables

```bash
# Diagnostic Interface Configuration
DIAG_INTERFACE_TYPE=obd2  # obd2 | can | custom
DIAG_INTERFACE_PORT=/dev/ttyUSB0
DIAG_CAN_INTERFACE=can0
DIAG_BAUDRATE=250000

# Diagnostic Protocol
DIAG_PROTOCOL=auto  # auto | j1939 | iso15765 | iso14230
DIAG_MANUFACTURER=auto  # auto | johndeere | caseih | agco | kubota

# Code Database
CODE_DB_PATH=/opt/emergency-diagnostics/codes.db
OFFLINE_MODE=true
UPDATE_CHECK_INTERVAL=168  # hours

# Logging
DIAG_LOG_LEVEL=info
DIAG_LOG_FILE=/var/log/emergency-diagnostics.log
DIAG_REPORT_DIR=/var/log/emergency-diagnostics/reports

# Safety
SAFETY_OVERRIDE_DISABLED=true
REQUIRE_CONFIRMATION=true
WARN_BEFORE_CLEAR=true

# Reporting
ENABLE_PDF_REPORTS=true
ENABLE_JSON_EXPORT=true
REPORT_INCLUDE_SENSORS=true
REPORT_HISTORY_DAYS=30
```

## Equipment Protocols and Standards

### OBD-II Standards

**SAE J1939** (Heavy Vehicle CAN Protocol):
- Standard for agricultural and heavy equipment
- 29-bit CAN identifiers
- PGN-based message structure
- Supports multiple ECUs on single bus

**ISO 14230** (KWP2000):
- Keyword Protocol 2000
- Serial diagnostic protocol
- Used by some manufacturers for diagnostics

**ISO 15765** (CAN Diagnostic):
- Unified Diagnostic Services (UDS)
- Modern diagnostic protocol over CAN
- Used by most newer equipment

### Manufacturer-Specific Protocols

#### John Deere

**Protocol:** JDLink Connect / CAN bus

**Diagnostic Port:** 9-pin Deutsch connector (typically)

**Key Characteristics:**
- Proprietary diagnostic codes (SPN/FMI format)
- Extended data beyond standard OBD-II
- Integration with JDLink cloud services
- Security handshake for some functions

**Common Code Format:**
```
SPN 91 FMI 3 (Engine Coolant Temperature High)
SPN = Suspect Parameter Number
FMI = Failure Mode Identifier
```

**Code Ranges:**
- Engine: SPN 91-250
- Transmission: SPN 500-650
- Hydraulics: SPN 1000-1200
- Electrical: SPN 1500-1700

**Access Notes:**
- Some codes require dealer-level access
- Security features may block certain functions
- JDLink Connect provides remote diagnostics (subscription)

#### Case IH

**Protocol:** AFS Connect / ISO 11783

**Diagnostic Port:** OBD-II style or 9-pin

**Key Characteristics:**
- Good ISO 11783 compliance
- Standard J1939 codes where possible
- AFS Pro terminal integration
- More open than John Deere

**Code Format:**
```
SPN 91 FMI 3 - Coolant Temperature High
```

**Access Notes:**
- Generally more accessible
- Standard OBD-II adapters often work
- AFS Connect optional subscription

#### AGCO

**Protocol:** AGCOMMAND / ISO 11783

**Diagnostic Port:** Varies by brand (Challenger, Massey Ferguson, Fendt)

**Key Characteristics:**
- Mixed approach across brands
- Some proprietary, some standard
- Fuse platform integration
- Varies by equipment age

**Access Notes:**
- Check specific brand documentation
- Newer equipment more open
- Older equipment may require dealer tools

#### Kubota

**Protocol:** K-Communicator / J1939

**Diagnostic Port:** OBD-II or proprietary

**Key Characteristics:**
- Compact equipment focused
- Simpler diagnostic structure
- J1939 standard codes
- Less proprietary extensions

**Access Notes:**
- Often accessible with standard tools
- Compact tractors may have limited OBD-II
- Consult service manual for port location

## Diagnostic Trouble Codes (DTCs)

### Code Structure (J1939/SAE Format)

**SPN (Suspect Parameter Number):**
- Identifies the specific component or parameter
- 19-bit number (1-524287)
- Common SPNs defined in J1939 standard

**FMI (Failure Mode Identifier):**
- Describes the type of failure
- 5-bit number (0-31)
- Common FMIs defined in J1939 standard

**OC (Occurrence Count):**
- Number of times the fault has occurred
- Used to track recurrence

### Common FMI Definitions

- **FMI 0:** Data valid but above normal operational range (most severe)
- **FMI 1:** Data valid but below normal operational range
- **FMI 2:** Erratic, intermittent, or incorrect
- **FMI 3:** Voltage above normal or open circuit
- **FMI 4:** Voltage below normal or open circuit
- **FMI 5:** Current below normal or open circuit
- **FMI 6:** Current above normal or open circuit
- **FMI 7:** Mechanical system not responding properly
- **FMI 8:** Abnormal frequency, pulse width, or period
- **FMI 9:** Abnormal update rate
- **FMI 10:** Abnormal rate of change
- **FMI 11:** Failure mode not identifiable
- **FMI 12:** Bad intelligent device or component
- **FMI 13:** Out of calibration
- **FMI 14:** Special instructions
- **FMI 15:** Data not available
- **FMI 16:** Parameter not supported
- **FMI 17:** Calibration not performed
- **FMI 18:** Sensor supply failure
- **FMI 19:** Not used
- **FMI 31:** Condition exists (general fault)

### Common SPN Categories

**Engine System:**
- **SPN 91:** Engine Coolant Temperature
- **SPN 100:** Engine Oil Pressure
- **SPN 105:** Engine Speed (RPM)
- **SPN 110:** Fuel Temperature
- **SPN 111:** Fuel Pressure
- **SPN 172:** Exhaust Gas Temperature
- **SPN 245:** Diesel Particulate Filter (DPF) differential pressure
- **SPN 246:** DPF regeneration status
- **SPN 3226:** DEF (AdBlue) quality/level

**Transmission System:**
- **SPN 523:** Transmission Oil Temperature
- **SPN 527:** Transmission Range
- **SPN 529:** Transmission Input Speed
- **SPN 530:** Transmission Output Speed

**Hydraulic System:**
- **SPN 949:** Hydraulic Oil Temperature
- **SPN 989:** Hydraulic System Pressure
- **SPN 1026:** Three-point hitch position
- **SPN 1028:** Remote valve status

**Electrical System:**
- **SPN 1572:** Battery voltage
- **SPN 1574:** Alternator voltage
- **SPN 610:** Engine control module supply voltage

**Brake System:**
- **SPN 597:** Brake system pressure
- **SPN 598:** Parking brake status
- **SPN 599:** Brake application status

**PTO System:**
- **SPN 963:** PTO speed
- **SPN 964:** PTO engagement status
- **SPN 1578:** PTO control module voltage

## Code Severity Levels

### Level 1: Critical (Immediate Action Required)
- Equipment must be stopped immediately
- Risk of catastrophic damage or injury
- Examples:
  - SPN 91 FMI 0 - Engine coolant temperature critically high
  - SPN 100 FMI 0 - Engine oil pressure critically low
  - SPN 597 FMI 0 - Brake system failure

**Action:** Stop operation immediately, do not clear codes, professional service required

### Level 2: Warning (Stop Operation Soon)
- Equipment should be stopped within reasonable time
- Risk of damage if operation continues
- Examples:
  - SPN 91 FMI 1 - Engine coolant temperature elevated
  - SPN 245 FMI 1 - DPF near regeneration required

**Action:** Complete current operation cycle, then investigate and repair

### Level 3: Advisory (Monitor Closely)
- Operation can continue but monitor condition
- Possible performance degradation
- Examples:
  - SPN 3226 FMI 1 - DEF level low
  - SPN 1572 FMI 1 - Battery voltage slightly low

**Action:** Continue operation, schedule repair when convenient

### Level 4: Informational (Historical)
- Fault has occurred but is no longer active
- Indicates past issue or intermittent condition
- Examples:
  - Any code marked as "stored" or "historical"
  - Codes cleared during previous session

**Action:** Document for trend analysis, investigate if recurring

## Diagnostic Process

### Initial Assessment

1. **Capture Operator Information**
   - What was the equipment doing when the problem occurred?
   - What warning lights or messages appeared?
   - Were there any unusual sounds, smells, or vibrations?
   - Has this happened before?

2. **Visual Inspection**
   - Check for obvious problems: leaks, loose connections, damage
   - Inspect belts, hoses, wiring
   - Check fluid levels (oil, coolant, fuel, hydraulic)
   - Look for evidence of previous repairs

3. **Connect Diagnostic Tool**
   - Locate diagnostic port
   - Connect CAN/OBD adapter
   - Verify connection (LED indicators, software detection)
   - Check for communication errors

### Code Reading and Analysis

1. **Read All Codes**
   - Scan all ECUs on network
   - Capture confirmed and pending codes
   - Check for historical codes
   - Note code count per ECU

2. **Prioritize by Severity**
   - Identify Level 1 (Critical) codes first
   - Address Level 2 (Warning) codes next
   - Note Level 3-4 codes for later review

3. **Analyze Code Relationships**
   - Multiple codes may indicate single root cause
   - Example: Low voltage causing multiple sensor faults
   - Check for cascading failures

4. **Cross-Reference Systems**
   - Check related systems and sensors
   - Verify data values make sense
   - Look for common ground/power issues

### Live Data Monitoring

1. **Select Relevant Parameters**
   - Monitor sensors related to fault codes
   - Include supporting parameters
   - Compare to normal operating ranges

2. **Capture Baseline**
   - Record values at idle
   - Record values under load
   - Record values at different operating conditions

3. **Identify Anomalies**
   - Look for values outside normal ranges
   - Check for sensor drift or inconsistency
   - Note erratic or unstable readings

4. **Perform Tests**
   - Actuate components (if supported)
   - Monitor response to known inputs
   - Check sensor response to changes

### Interpretation and Recommendations

1. **Translate Codes to Meaning**
   - Use code database for definitions
   - Cross-reference manufacturer documentation
   - Provide plain-language explanation

2. **Identify Possible Causes**
   - Rank causes by probability (high, medium, low)
   - Consider environmental factors (temperature, contamination)
   - Factor in equipment age and maintenance history

3. **Recommend Diagnostic Steps**
   - Suggest tests operator can perform safely
   - Identify tests requiring professional equipment
   - Prioritize steps from least to most invasive

4. **Provide Repair Guidance**
   - Estimate repair complexity and cost
   - Identify parts that may be needed
   - Recommend DIY vs. professional service

5. **Clearing Codes**
   - Only clear after repairs are verified complete
   - Verify no safety concerns exist
   - Monitor for code recurrence
   - Document clearing action

## Code Database Structure

The emergency diagnostics skill uses a comprehensive code database to interpret diagnostic trouble codes. The database includes:

### Manufacturer Codes
- John Deere specific codes
- Case IH specific codes
- AGCO specific codes
- Kubota specific codes
- Generic J1939 codes

### Code Information
- SPN and FMI definitions
- Plain-language descriptions
- Severity levels
- Common causes
- Suggested tests
- Repair complexity ratings
- Parts frequently involved

### Cross-References
- Related codes and systems
- Similar symptoms across manufacturers
- Standard vs. proprietary code mappings
- Known manufacturer service bulletins

## Offline Operation

The skill is designed to work offline when internet connectivity is unavailable or unreliable in the field:

### Offline Capabilities
- Complete code database stored locally
- Diagnostic interpretation without external lookup
- Report generation with PDF export
- Historical data analysis and trend detection

### Online Capabilities (when available)
- Code database updates
- Manufacturer service bulletin access
- Community forum queries
- Remote dealer communication

## Legal and Warranty Considerations

### Right to Repair

**Legal Basis:**
- **Federal Magnesson-Moss Warranty Act:** Manufacturers cannot void warranty for using third-party parts or services
- **DMCA Exemptions:** Farmers are allowed to bypass software locks for diagnostic purposes
- **State Right to Repair Laws:** Many states have enacted or proposed right-to-repair legislation

**What This Means for Farmers:**
- You have the legal right to diagnose your own equipment
- Using this diagnostic skill does not void manufacturer warranty
- Dealers must honor warranty regardless of who performs diagnostics
- Document all diagnostic sessions for warranty protection

### Documentation Best Practices
- Always timestamp diagnostic sessions
- Record codes found, sensor data, and actions taken
- Save diagnostic reports with equipment identification
- Maintain log of all maintenance and repairs

### Warranty Claims
- Provide diagnostic reports to dealer with warranty claims
- Include timestamped evidence of proper maintenance
- Document any dealer-performed repairs
- Keep records of all parts used

## Troubleshooting

### Connection Issues

**Problem: Cannot connect to equipment**

**Possible Causes:**
- Wrong port selected
- Driver not installed for adapter
- Bad cable or adapter
- Equipment port not powered

**Solutions:**
- Check adapter compatibility with equipment protocol
- Verify port device (/dev/ttyUSB0, /dev/ttyUSB1, etc.)
- Test adapter on known-good vehicle
- Check power supply to diagnostic port
- Try different baud rate settings

### No Codes Found

**Problem: Scanner shows "No Codes" but equipment has problems**

**Possible Causes:**
- Wrong protocol selected
- ECU not responding
- Codes cleared previously
- Non-emission-related faults not on OBD-II bus
- Pre-OBD-II equipment

**Solutions:**
- Try different protocol settings (J1939, ISO15765, etc.)
- Check individual ECUs (engine, transmission, hydraulics)
- Check for communication errors
- Consult equipment service manual for bus architecture
- Consider proprietary diagnostic software may be needed

### Codes Keep Returning

**Problem: Codes cleared but return immediately or shortly after**

**Possible Causes:**
- Underlying problem not fixed
- Intermittent connection or wiring issue
- Sensor not actually faulty
- ECU calibration issue

**Solutions:**
- Review code interpretation and common causes
- Check wiring and connections thoroughly
- Perform live data monitoring to identify issue
- Consider replacing suspect components
- Check for software updates or ECU reflashing

### Incorrect Code Interpretation

**Problem: Code database missing or has wrong definition**

**Possible Causes:**
- Manufacturer-specific code not in database
- Code meaning changed by manufacturer update
- Database outdated

**Solutions:**
- Report missing codes for database update
- Check manufacturer service manual
- Search online forums for code meanings
- Contact dealer or manufacturer for clarification
- Use generic J1939 code interpretation as fallback

## Examples

See examples/ directory for:
- Basic code reading and interpretation
- Live data monitoring workflow
- Generating diagnostic reports
- Clearing codes safely
- Multi-ECU diagnostics
- Code analysis and recommendations

## References

### Standards and Specifications

See references/ directory for:
- SAE J1939 standard documentation
- ISO 14230 (KWP2000) specification
- ISO 15765 (UDS on CAN) specification
- OBD-II standard codes

### Manufacturer Documentation

- John Deere Technical Information System (TIS)
- Case IH AFS documentation
- AGCO service manuals
- Kubota technical publications

### Research and Standards

- Agricultural Equipment Diagnostics Research Papers
- Right to Repair legal resources
- Manufacturer service bulletins

## Testing

1. **Unit Testing**
   - Test code reading functions
   - Verify code interpretation accuracy
   - Validate database queries

2. **Integration Testing**
   - Test with actual equipment
   - Verify connection protocols
   - Test report generation

3. **Stress Testing**
   - Test with multiple codes
   - Test with intermittent faults
   - Test offline operation

## Version History

- **1.0.0** - Initial release with major manufacturer support and offline operation

## License

MIT License - Open source, free to use, modify, and distribute.

## Support

For issues, questions, or contributions:
- GitHub Issues: https://github.com/farmfriend-labs/agent-skills-farming/issues
- Email: farmfriend.labs@gmail.com

---

**Emergency Diagnostics Liberator - Because downtime during harvest costs more than this entire skill.**
