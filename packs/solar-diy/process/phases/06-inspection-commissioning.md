---
title: "Phase 6: Inspection & Commissioning"
type: "phase"
tags: [federal-tax-credit, installation, net-metering, operations-maintenance, permitting, phase-6-inspection-commissioning, process]
pack: "solar-diy-process"
retrieval_strategy: "atomic"
id: solar-diy/process/phases/06-inspection-commissioning
verified_at: "2026-04-21"
verified_by: agent
schema_version: "4.1"
concept_scope: single
---

# Phase 6: Inspection & Commissioning

<!-- context: section=process, topic=phase-6-inspection-commissioning, related=permitting,installation,operations-maintenance,net-metering,federal-tax-credit -->

> **Lead summary:** Two inspections gate your ability to legally operate your solar system: the building/electrical inspection (from your AHJ) and the utility inspection (sometimes). After both pass, the utility issues Permission to Operate (PTO), swaps your meter for a net meter, and you can flip the inverter on. The inspection process typically takes 2–8 weeks; commissioning itself (the day you turn it on) takes a few hours.

## The Two-Gate Model

You need two green lights before operating:

| Gate | Who | What They Check | What You Get |
|------|-----|-----------------|-------------|
| Building/Electrical Inspection | AHJ (city/county building department) | Code compliance: wiring, grounding, labeling, rapid shutdown, structural | Signed permit card or final inspection approval |
| Utility Approval | Your electric utility | Interconnection agreement compliance, meter swap | Permission to Operate (PTO) letter |

Some utilities require their own field inspection before issuing PTO; others issue PTO after receiving the signed permit card from your AHJ. Know which process your utility uses — ask when you submitted your interconnection application.

## Part 1: Building/Electrical Inspection

### Scheduling
- Call your building department to schedule — don't wait until you're 100% done; schedule as soon as you can confirm a completion date
- Some jurisdictions do online scheduling; some require phone calls
- Wait times vary: same-week scheduling is common in rural areas; 2–3 week waits are common in busy urban areas

### What the Inspector Will Check

**On the roof:**
- Panel layout matches permit drawings (count, placement, setbacks)
- Racking hardware installed per specs
- No evidence of damaged panels
- Rapid shutdown device properly installed and accessible
- Conduit properly supported and weatherproofed

**At the inverter and battery:**
- Equipment matches permit drawings
- Proper clearances maintained
- Wiring neat and organized (inspectors notice)
- All labels present and correctly worded
- Disconnect accessible and properly labeled

**At the service panel:**
- Solar breaker in correct location per permit
- Wiring properly landed and sized
- All labels present (NEC 705.10 interconnection label)
- AC disconnect visible and accessible

**Grounding:**
- Equipment grounding conductors properly sized and connected
- No missing grounds

### Common Inspection Failures
- Missing labels (the #1 cause of failures — see Phase 5 labeling checklist)
- Panel layout doesn't match permit drawings exactly (even small field modifications require permit revision)
- Exposed wiring where conduit was required
- Rapid shutdown device not properly labeled or accessible
- Incorrect wire gauge

### If You Fail
- Get a detailed list of corrections from the inspector
- Make all corrections before re-scheduling
- Don't argue during the inspection — note the issue, fix it, reschedule
- Most jurisdictions allow one free re-inspection; additional inspections may incur fees

## Part 2: Utility Interconnection Inspection

### Process Varies by Utility
- Some utilities require a field inspection by their technician
- Some utilities only require your signed/approved building permit card
- Some utilities do everything remotely via submitted photos
- Confirm your utility's specific process when you receive your PTI letter

### If the Utility Sends an Inspector
They typically verify:
- External AC disconnect is installed, labeled, and accessible
- Interconnection label at utility meter
- Production meter (if required) is installed
- System matches interconnection application (size, equipment)

### Meter Swap
After PTO is issued, the utility will:
- Schedule a meter swap appointment (or just swap it without notice — utilities vary)
- Install a bidirectional net meter that records export and import separately
- Some utilities install a separate production meter in addition to the net meter

**Wait for the net meter before turning on the system for export.** Running a grid-tied system without a net meter in place may result in an unmetered export credit dispute.

## Part 3: System Commissioning

Commissioning is the step-by-step startup of your system after both inspections are complete.

### Pre-Commissioning Verification

Before energizing, verify:
- [ ] All DC wiring complete and correct polarity
- [ ] AC disconnect(s) in the OFF position
- [ ] Inverter DC disconnect in the OFF position
- [ ] Battery in the OFF or standby mode
- [ ] Main panel solar breaker in the OFF position
- [ ] Net meter installed by utility

### String Inverter Commissioning Sequence

1. **Measure open-circuit voltage at the inverter DC input** before connecting
   - Set your multimeter to DC volts (1000V+ range)
   - Measure across each string's positive and negative conductors
   - Calculated Voc × number of panels should roughly match (within 5%)
   - Verify polarity (positive is positive)
   - If voltage is 0 or reversed: stop and troubleshoot before proceeding

2. **Connect DC inputs** to inverter
3. **Turn on AC breaker** in service panel
4. **Turn on AC disconnect**
5. **Turn on inverter** per manufacturer startup procedure
6. **Wait for inverter initialization** (typically 1–5 minutes for grid synchronization)
7. **Verify production** — inverter display or monitoring app should show production

### Microinverter Commissioning
1. Connect trunk cable to service panel (through AC disconnect)
2. Turn on solar breaker in service panel
3. Microinverters power up automatically as sunlight hits panels
4. Wait 5–10 minutes for all units to come online
5. Check monitoring app — all microinverters should report

### Battery Commissioning
Battery systems have their own commissioning sequence — follow the manufacturer's specific procedure exactly. Generally:

1. Verify AC input power is present at battery
2. Enable battery via app or physical control
3. Complete any required firmware updates before first use
4. Set operating mode (backup only, self-consumption, time-of-use, etc.)
5. Verify backup gateway function (if present) by testing brief outage simulation
6. Configure monitoring integration

### Monitoring Setup

Set up monitoring before or during commissioning:
- **Enphase**: Envoy gateway connects to home Wi-Fi; Enlighten app shows per-panel production
- **SolarEdge**: Inverter connects directly to Wi-Fi or via inverter display; monitoring portal at monitoring.solaredge.com
- **String inverters (generic)**: Many support Modbus or proprietary protocols; third-party monitoring (Solar-Log, Solarman, manufacturer cloud)
- **Tesla Powerwall**: Tesla app handles all monitoring; also shows home energy flow

Monitoring baseline: Check production on your first sunny day and compare to your PVWatts estimate. It won't match exactly (day 1 is not representative) but should be in the right ballpark.

## Post-Commissioning Actions

### Tax Credits and Incentives
- **Federal Investment Tax Credit (ITC)**: 30% of total system cost as of 2024–2026. Includes equipment, labor, permitting, and battery (if storage meets threshold). File IRS Form 5695 with your taxes.
- **State and local incentives**: Vary by state; check DSIRE (dsireusa.org) for your state's current programs
- **Utility rebates**: Some utilities offer rebates; most have phased these out as costs dropped
- **SREC markets**: Some states (NJ, MA, PA, MD, DC) have solar renewable energy certificate markets — register your system

### Document and Store
- Permit (keep the final approved permit package)
- Warranty documentation for all equipment
- Interconnection agreement
- Net metering enrollment confirmation
- System monitoring login credentials
- Manufacturer installation manuals (for reference during maintenance)
- As-built single-line diagram (update if any field changes were made)

## Related

- Operations & Maintenance (ongoing): `07-operations-maintenance.md`
- Troubleshooting if system doesn't perform as expected: `../../product/troubleshooting/`
