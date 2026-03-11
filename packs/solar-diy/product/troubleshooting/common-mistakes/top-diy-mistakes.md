# Top DIY Solar Installation Mistakes

## 1. Wrong String Sizing

### Symptom
Inverter displays overvoltage error on cold winter mornings, or system produces less than expected on hot summer afternoons with no apparent issue.

### The Mistake
Not accounting for temperature effects on panel voltage. Panels produce MORE voltage in cold weather and LESS in hot weather. If you size your strings at room temperature, you'll exceed inverter limits in winter or fall below minimum in summer.

### The Fix
Run proper string sizing calculations using your site's ASHRAE temperature extremes, not average temperatures. See [System Design Fundamentals](../../concepts/system-design-fundamentals.md) for the math.

### How to Avoid
Always use the coldest recorded temperature (or ASHRAE 2% low) for maximum string size and the hottest temperature plus mounting adder for minimum string size. Never guess.

---

## 2. Ignoring Rapid Shutdown Requirements

### Symptom
Inspection fails. Inspector requires rapid shutdown compliance before signing off.

### The Mistake
Installing a string inverter system without MLPE or UL 3741 compliance. This was the most common NEC violation for DIY installs since 2017.

### The Fix
Add compliant rapid shutdown devices, switch to microinverters, or redesign for UL 3741 compliance. Any of these may require significant rework.

### How to Avoid
Check your jurisdiction's adopted NEC edition BEFORE designing the system. If NEC 2017 or later, plan for rapid shutdown from the start. See [NEC Rapid Shutdown](../../concepts/nec-rapid-shutdown.md).

---

## 3. Undersized Wiring

### Symptom
Voltage drop across long wire runs, wires running hot, tripped breakers, or reduced system output.

### The Mistake
Using wire gauges that are too small for the current and distance. Solar panels on roofs can require long wire runs, and voltage drop accumulates.

### The Fix
Recalculate wire sizing using NEC Article 310 ampacity tables and voltage drop formulas. Replace undersized wiring. Target ≤2% voltage drop on DC runs and ≤3% on AC runs.

### How to Avoid
Use a wire sizing calculator that accounts for: current (Isc × 1.56 safety factor per NEC), wire run length (round trip), ambient temperature derating, and conduit fill derating.

---

## 4. Improper Grounding

### Symptom
Failed inspection. In severe cases: equipment damage from lightning or ground faults, shock hazard.

### The Mistake
Missing or improper equipment grounding conductors, missing ground rods, or not bonding the panel frames to the grounding system.

### The Fix
Install proper equipment grounding per NEC 690.41-690.47. This includes grounding each panel frame, the racking system, inverter chassis, and a ground electrode system.

### How to Avoid
Follow NEC Article 690 Part V grounding requirements exactly. Use listed grounding lugs and WEEBs (Washer, Electrical Equipment Bond) for racking. Don't rely on metal-to-metal contact through mounting hardware — it's not reliable long-term.

---

## 5. Not Pulling Permits

### Symptom
No inspection means no interconnection agreement with the utility. Insurance may not cover damage. If you sell the house, unpermitted work is a liability.

### The Mistake
Skipping permits to save money or avoid hassle. Solar is an electrical installation — it requires a permit in virtually every US jurisdiction.

### The Fix
Apply for permits retroactively. You may need to expose wiring for inspection, which can mean partial disassembly.

### How to Avoid
Pull permits before you start. Many jurisdictions have streamlined solar permits. Some accept SolarAPP+ (automated permit processing). Budget $200-500 for permit fees.

---

## 6. Poor Roof Attachment / Water Leaks

### Symptom
Water stains on ceiling below solar panels. Racking loosens over time.

### The Mistake
Improper flashing around roof penetrations, using lag bolts without proper sealant, or penetrating the roof in the wrong locations (missing rafters).

### The Fix
Remove panels from affected areas, properly flash and seal all penetrations, and re-mount. Use a stud finder to locate rafters.

### How to Avoid
Use code-compliant flashing (not just caulk) at every roof penetration. Always lag into rafters, not just sheathing. Consider rail-less mounting systems that minimize penetrations. Some racking systems (S-5! clamps) attach to standing seam metal roofs with zero penetrations.

---

## 7. Mismatching Panel and Inverter Specs

### Symptom
Inverter clipping (producing less than panels could deliver), voided warranties, or outright equipment failure.

### The Mistake
Pairing panels with an incompatible inverter — wrong voltage range, insufficient input channels, or exceeding the inverter's maximum DC input power.

### The Fix
Verify compatibility before purchasing. Check: inverter max input voltage ≥ string Voc at cold temps, inverter MPPT range covers string Vmp at hot temps, inverter max DC input ≥ array nameplate wattage (some oversizing is fine and normal — typically up to 1.3:1 DC:AC ratio).

### How to Avoid
Read both datasheets. Use manufacturer string sizing tools (SolarEdge Designer, Enphase Design Tool, SMA Sunny Design). These catch incompatibilities automatically.

---

## 8. Forgetting About Future Battery Readiness

### Symptom
You want to add a battery later but your inverter doesn't support it, or adding one requires replacing the inverter.

### The Mistake
Installing a solar-only inverter with no path to add storage later.

### The Fix
Options: replace the inverter with a hybrid model, or add an AC-coupled battery (Enphase, Franklin) that works alongside any existing inverter.

### How to Avoid
If battery storage is even a possibility, either install a hybrid inverter now (Tesla, SolarEdge with battery interface) or choose an AC-coupled ecosystem (Enphase) that can be added without changing the solar inverter.
