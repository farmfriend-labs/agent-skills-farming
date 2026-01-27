# Basic Emergency Diagnostics Workflow

This example demonstrates the basic emergency diagnostics workflow for diagnosing equipment problems during critical operations.

## Scenario

You're in the middle of harvest when your combine throws a warning light. The dealer is 2 hours away and won't be able to get to you today. You need to diagnose the problem yourself to decide whether to attempt a repair, continue operation, or wait for the dealer.

## Prerequisites

- OBD-II/CAN adapter connected to equipment
- Emergency Diagnostics Liberator installed
- Equipment with diagnostic port access
- Code database initialized

## Step 1: Connect to Equipment

1. Locate the diagnostic port on your combine:
   - Usually located in the cab near the operator station
   - May be under a cover or panel
   - Consult your equipment manual if unsure

2. Connect your OBD-II adapter:
   ```bash
   # Connect USB adapter
   ls /dev/ttyUSB*
   # Should see /dev/ttyUSB0 or similar
   ```

3. Verify connection:
   ```bash
   # Start diagnostics
   cd scripts
   sudo ./run.sh
   ```

## Step 2: Identify Equipment Information

Before reading codes, identify your equipment:

```
Manufacturer: Case IH
Model: Axial-Flow 8240
Year: 2020
VIN: [equipment VIN]
```

This information helps the diagnostics skill select the correct protocol and code database.

## Step 3: Read Diagnostic Trouble Codes

Start the diagnostic session and read codes:

```
diag> read

Reading codes from OBD-II...
Found 3 code(s):
  91_1
  245_1
  1572_1
```

The diagnostics skill displays codes in SPN_FMI format.

## Step 4: Interpret Each Code

### Code 91_1: Engine Coolant Temperature Below Normal

**Display Output:**
```
============================================================
SPN 91 FMI 1
============================================================
Severity: WARNING [ADDRESS SOON]

Description: Engine Coolant Temperature Below Normal

Manufacturer: Case IH

Common Causes:
  - Thermostat stuck open
  - Sensor failure

Suggested Tests:
  - Check thermostat
  - Verify sensor reading with manual temperature gauge

Repair Complexity: Low
============================================================
```

**Interpretation:** Your engine is running too cool. This won't cause immediate damage but reduces efficiency. The thermostat is likely stuck open.

### Code 245_1: DPF Differential Pressure Elevated

**Display Output:**
```
============================================================
SPN 245 FMI 1
============================================================
Severity: WARNING [ADDRESS SOON]

Description: DPF Differential Pressure Elevated

Manufacturer: Case IH

Common Causes:
  - DPF requiring regeneration
  - Soot accumulation

Suggested Tests:
  - Perform DPF regeneration
  - Check for operating conditions preventing regeneration

Repair Complexity: Medium

============================================================
```

**Interpretation:** Your diesel particulate filter is starting to clog and needs regeneration. This is a common issue and can be addressed.

### Code 1572_1: Battery Voltage Below Normal

**Display Output:**
```
============================================================
SPN 1572 FMI 1
============================================================
Severity: ADVISORY [MONITOR]

Description: Battery Voltage Below Normal

Manufacturer: Case IH

Common Causes:
  - Battery weak
  - Alternator not charging
  - Excessive electrical load

Suggested Tests:
  - Check battery condition
  - Test alternator output
  - Reduce electrical load

Repair Complexity: Low
============================================================
```

**Interpretation:** Your electrical system voltage is slightly low. This could be a weak battery or the alternator not charging properly.

## Step 5: Analyze the Overall Picture

Now analyze all codes together:

**Severity Assessment:**
- No CRITICAL codes - Equipment can continue operation
- 2 WARNING codes - Address soon, but not immediate danger
- 1 ADVISORY code - Monitor, repair when convenient

**Root Cause Analysis:**
- Code 91_1 (cool temp) and 1572_1 (low voltage) may be related
- A failing alternator can cause low voltage, which can affect sensor readings
- Code 245_1 (DPF) is likely independent and just due to extended operation

**Decision Matrix:**

| Code | Severity | Action | Complexity |
|------|----------|--------|------------|
| 91_1 | Warning | Replace thermostat | Low |
| 245_1 | Warning | Force DPF regeneration | Low |
| 1572_1 | Advisory | Test charging system | Medium |

## Step 6: Develop Action Plan

Based on the diagnostics:

### Immediate Actions (Can do now):
1. **Force DPF regeneration:**
   - Most equipment has a manual regeneration option
   - Requires the combine to be in a safe, open area
   - Takes 20-30 minutes
   - Should clear code 245_1

2. **Test alternator output:**
   - Use multimeter at battery terminals
   - Should read 13.8-14.4V at idle
   - If below 13V, alternator may be failing

### Deferred Repairs (After harvest):
1. **Replace thermostat:**
   - Inexpensive part ($20-50)
   - Medium complexity repair
   - Can wait until harvest is complete

2. **Address battery/alternator:**
   - Test battery load capacity
   - Replace alternator if needed
   - Critical for reliable operation

## Step 7: Decide on Operation

**Can you continue harvesting?**

**YES** - Here's why:
- No critical codes that require immediate shutdown
- All issues can be managed safely
- DPF can be regenerated during a break
- Low voltage is being monitored and not critical

**Monitoring plan:**
- Watch battery voltage on display
- Note any new warning lights
- Stop if temperature or pressure warnings increase
- Perform DPF regeneration during lunch break

**Expected outcome:**
- You can finish today's field
- DPF regeneration will clear that code
- Thermostat replacement can wait
- Charging system needs testing soon

## Step 8: Generate Diagnostic Report

Save the diagnostic session for record-keeping:

```
diag> report

============================================================
DIAGNOSTIC REPORT
============================================================
Session ID: 123
Timestamp: 2026-01-27 13:45:00

Equipment: Case IH Axial-Flow 8240
Interface: OBD-II
Protocol: J1939

Codes Found:
  SPN 91 FMI 1: Engine Coolant Temperature Below Normal [Warning]
  SPN 245 FMI 1: DPF Differential Pressure Elevated [Warning]
  SPN 1572 FMI 1: Battery Voltage Below Normal [Advisory]

Recommendations:
  - Continue operation with monitoring
  - Force DPF regeneration when convenient
  - Test charging system within 24 hours
  - Replace thermostat after harvest season

============================================================
```

Save this report for:
- Warranty documentation if needed
- Your own records
- Sharing with dealer or independent mechanic
- Future reference

## Step 9: Clear Codes (After Repairs)

After you've completed repairs and verified they're working:

1. **Never clear critical codes** without proper repairs
2. **Confirm the repair worked** before clearing
3. **Monitor for code recurrence** after clearing

```
diag> clear

Are you sure you want to clear codes? (yes/no): yes

Clearing codes...
Codes cleared successfully.

Monitor for recurrence over next 24 hours.
```

## Step 10: Continue Operation

You've now:
- Diagnosed the problem yourself
- Saved hours waiting for dealer
- Made an informed decision to continue
- Have a plan to address issues
- Documented everything for your records

**Result:** You finish harvesting today's field instead of losing it to waiting for dealer service.

## Troubleshooting

### No Codes Found

If you see "No codes found" but equipment has problems:

1. **Check connection:**
   ```bash
   diag> info
   ```
   Verify you're connected and protocol is correct

2. **Try different protocol:**
   - Auto-detect may have selected wrong protocol
   - Try manual protocol selection in .env

3. **Check if codes were recently cleared:**
   - Codes may have been cleared by previous diagnostic session
   - Some codes take time to reappear after being cleared

### Cannot Connect

If connection fails:

1. **Check adapter:**
   ```bash
   ls /dev/ttyUSB*
   ```
   Make sure your adapter is detected

2. **Check permissions:**
   ```bash
   sudo chmod 666 /dev/ttyUSB0
   ```
   May need to adjust permissions

3. **Try different USB port** or cable

### Codes Keep Returning

If codes return immediately after clearing:

1. **Root cause not fixed** - The diagnostic guidance was incomplete or repair was insufficient
2. **Intermittent issue** - Wiring problem or failing component
3. **ECU issue** - May require dealer reprogramming

## Best Practices

1. **Always document** diagnostic sessions
2. **Never clear codes** without understanding the problem
3. **Prioritize by severity** - Critical codes first
4. **Consider relationships** between codes
5. **Use professional service** for complex issues
6. **Keep safety first** - Stop if critical codes appear
7. **Maintain records** for warranty and troubleshooting

## Next Steps

- Monitor equipment throughout the day
- Perform recommended tests and repairs
- Update diagnostic reports after repairs
- Share findings with your service network

## References

- SKILL.md - Complete documentation
- references/safety-guidelines.md - Safety procedures
- references/manufacturer-codes.md - Manufacturer-specific codes
