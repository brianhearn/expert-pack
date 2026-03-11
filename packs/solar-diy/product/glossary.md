# Solar & Battery — Glossary

Quick-reference definitions for residential solar terminology. Maps technical terms to how homeowners and DIYers actually talk about them.

## Panel & Cell Technology

| Term | Definition | Common User Language |
|------|-----------|---------------------|
| **N-type cell** | Modern silicon cell type with superior efficiency and lower degradation than older P-type cells. Most 2024+ panels use N-type. | "newer cell type", "better panels" |
| **TOPCon** | Tunnel Oxide Passivated Contact — mainstream N-type cell technology balancing high efficiency (~23-24%) with cost-effective manufacturing | "standard good panels" |
| **Back-contact (IBC/ABC)** | Cell design where all electrical contacts are on the rear, maximizing light absorption. Highest efficiency (~24-25%) but more expensive | "premium panels", "most efficient" |
| **HJT** | Heterojunction — N-type cell combining crystalline and amorphous silicon. Excellent temperature coefficient but less common now than TOPCon | "hetero panels" |
| **Voc** | Open Circuit Voltage — maximum voltage a panel produces with no load, at standard test conditions (25°C). Critical for string sizing calculations | "panel voltage" |
| **Vmp** | Voltage at Maximum Power — the voltage where the panel produces its rated wattage. Used for minimum string size calculations | "operating voltage" |
| **Temperature coefficient** | How much panel voltage (or power) changes per degree above/below 25°C. Always negative for voltage — panels produce MORE voltage in cold weather | "cold weather voltage boost" |
| **Degradation rate** | Annual percentage loss of panel output over time. Quality panels degrade 0.25-0.5% per year | "how fast panels wear out" |
| **STC** | Standard Test Conditions — lab conditions (25°C cell temp, 1000 W/m² irradiance) used for rating panels. Real-world output is typically lower | "rated conditions", "lab specs" |

## Inverter Terms

| Term | Definition | Common User Language |
|------|-----------|---------------------|
| **Microinverter** | Small inverter mounted behind each panel, converting DC to AC at the panel level. Each panel operates independently | "per-panel inverter", "Enphase" |
| **String inverter** | Single central inverter that converts DC from a series-connected string of panels to AC. More efficient but single point of failure | "central inverter", "one big box" |
| **Power optimizer** | Module-level DC-DC converter paired with a string inverter. Optimizes each panel individually while using a central inverter for DC-AC conversion | "SolarEdge optimizer", "panel optimizer" |
| **MPPT** | Maximum Power Point Tracking — algorithm that continuously adjusts voltage/current to extract maximum power from panels | "power optimization" |
| **MLPE** | Module-Level Power Electronics — umbrella term for microinverters, power optimizers, and rapid shutdown devices | "per-panel electronics" |
| **AC-coupled** | Battery connected on the AC side of the system (after the inverter). Can be added to any existing solar system | "add-on battery" |
| **DC-coupled** | Battery connected on the DC side, sharing an inverter with the solar panels. More efficient but requires compatible hybrid inverter | "integrated battery" |
| **Hybrid inverter** | Inverter that handles both solar panels (DC input) and battery (DC charge/discharge) in one unit | "combo inverter", "all-in-one inverter" |

## Battery Terms

| Term | Definition | Common User Language |
|------|-----------|---------------------|
| **LFP** | Lithium Iron Phosphate (LiFePO4) — dominant battery chemistry for home storage. Safer, longer-lasting, but lower energy density than NMC | "safe battery chemistry" |
| **NMC** | Nickel Manganese Cobalt — older battery chemistry with higher energy density but shorter cycle life and more thermal risk | "older battery type" |
| **Depth of discharge (DoD)** | How much of the battery's capacity can actually be used. Modern LFP batteries typically allow 100% DoD | "usable capacity" |
| **Round-trip efficiency** | Percentage of energy you get back out vs what you put in. Typically 90-96% for modern home batteries | "how much energy is lost" |
| **LRA** | Locked Rotor Amps — peak current draw when a motor starts (A/C compressor, well pump). Batteries must handle this surge | "startup surge", "A/C starting power" |
| **Continuous output** | Sustained power the battery can deliver. Different from surge/peak power | "running power" |

## Code & Compliance

| Term | Definition | Common User Language |
|------|-----------|---------------------|
| **NEC** | National Electrical Code (NFPA 70) — US electrical safety standard. Updated every 3 years (2017, 2020, 2023). States adopt different editions | "electrical code" |
| **Rapid shutdown** | NEC 690.12 requirement to reduce voltage within the array boundary within 30 seconds of initiation, to protect firefighters | "safety shutdown", "fire code for solar" |
| **UL 3741** | Standard for PV Hazard Control Systems — alternative compliance path for rapid shutdown that can eliminate need for MLPE | "hazard control standard" |
| **AHJ** | Authority Having Jurisdiction — the local building department or inspector who approves your installation | "building inspector", "permit office" |
| **Interconnection agreement** | Contract between homeowner and utility allowing the solar system to connect to the grid. Required before system activation | "utility agreement", "grid connection paperwork" |
| **Net metering** | Billing arrangement where excess solar energy sent to the grid earns credits on your electric bill | "selling power back", "grid credits" |
| **NEM 3.0** | California's updated net metering policy (2023+) with significantly reduced export rates. Other states may follow similar patterns | "new California solar rules" |

## System Design

| Term | Definition | Common User Language |
|------|-----------|---------------------|
| **String** | Series-connected group of solar panels wired together. String voltage = sum of individual panel voltages | "row of panels wired together" |
| **String sizing** | Calculating the minimum and maximum number of panels per string based on temperature extremes and inverter voltage limits | "how many panels per row" |
| **Array** | The complete set of solar panels in a system, which may contain one or more strings | "all the panels" |
| **Azimuth** | Compass direction a roof face or panel array points. Due south (180°) is ideal in the Northern Hemisphere | "which way the roof faces" |
| **Tilt** | Angle of panels from horizontal. Optimal tilt roughly equals site latitude for annual production | "panel angle" |
| **Irradiance** | Amount of solar energy hitting a surface, measured in W/m² or kWh/m²/day. Varies by location and season | "how much sun you get" |
| **Peak sun hours** | Equivalent hours of 1000 W/m² irradiance per day. Used to estimate daily production. Ranges from ~3 (cloudy) to ~6+ (desert) in the US | "usable sun hours" |
