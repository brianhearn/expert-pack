---
title: "Decision: Inverter Topology (String vs Optimizer vs Microinverter)"
type: "decision"
tags: [component-selection, decision-inverter-topology, inverter-types, nec-rapid-shutdown, process, system-design]
pack: "solar-diy-process"
retrieval_strategy: "standard"
id: solar-diy/process/decisions/inverter-topology
verified_at: "2026-04-21"
verified_by: agent
schema_version: "4.1"
concept_scope: single
---

# Decision: Inverter Topology (String vs Optimizer vs Microinverter)

<!-- context: section=process, topic=decision-inverter-topology, related=inverter-types,nec-rapid-shutdown,component-selection,system-design -->

> **Lead summary:** The inverter topology choice affects shading tolerance, monitoring granularity, installation complexity, cost, and future expandability. In 2026, microinverters (Enphase) dominate the residential market for good reason: they're the most installer-friendly and the most resilient to partial shading. String inverters with optimizers (SolarEdge) remain competitive for large, unshaded arrays. Plain string inverters are lowest cost but least flexible.

## The Three Architectures

### Architecture 1: String Inverter (Central Inverter)

**How it works:** Panels are wired in series strings; all panels in a string feed a single DC input on the central inverter, which does all DC-to-AC conversion.

```
[Panel] → [Panel] → [Panel] → [Panel] → [String Inverter] → Grid
(all in series: voltages add, same current through all)
```

**Strengths:**
- Lowest cost (one large inverter vs many small ones)
- Simpler wiring (fewer components)
- High efficiency at rated power
- Easy inverter replacement (one unit, widely available)
- Familiar to electricians

**Weaknesses:**
- Shading kills the whole string — one shaded panel reduces the entire string to that panel's current
- No per-panel monitoring — you see total string production, not individual panels
- Requires string sizing calculations (see `../../product/concepts/system-design-fundamentals.md`)
- Rapid shutdown requires additional devices for NEC 2017+ compliance
- Difficult to expand (adding panels must fit into existing string configuration)

**Best for:**
- Large, completely unshaded arrays (ground mounts, south-facing roofs with no obstructions)
- Cost-sensitive installs willing to accept some production loss
- Commercial/utility scale (where string inverters are nearly universal)

**Major brands:** SMA, Fronius, Growatt, Solis, Schneider

### Architecture 2: String Inverter + Power Optimizers

**How it works:** Each panel has a DC power optimizer that enables individual Maximum Power Point Tracking (MPPT). The optimizers connect to a string inverter; the string carries a fixed voltage (safe DC) rather than the variable Vmp of a plain string.

```
[Panel+Optimizer] → [Panel+Optimizer] → [Panel+Optimizer] → [String Inverter] → Grid
(fixed DC bus voltage; each optimizer maximizes its panel independently)
```

**Strengths:**
- Per-panel MPPT eliminates most string shading losses
- Per-panel monitoring (via cloud platform)
- SolarEdge "SafeDC" reduces string voltage to <1V when AC is off — built-in rapid shutdown
- Good efficiency (97–99% optimizer, 98–99% inverter)
- Single inverter still means simpler AC wiring

**Weaknesses:**
- Higher cost than plain string (each panel needs an optimizer, ~$50–$100/panel)
- More components = more potential failure points
- Still requires one inverter (but the inverter is simpler and cheaper than without optimizers)
- SolarEdge ecosystem: SolarEdge inverters work best with SolarEdge optimizers (mixing brands is problematic)

**Best for:**
- Moderate shading (trees, chimneys, complex roof planes)
- Installers who want per-panel monitoring without microinverter cost premium
- Large arrays where per-panel MPPT value is high

**Major brands:** SolarEdge (dominant), Tigo (can be used with other inverters as an add-on)

### Architecture 3: Microinverters

**How it works:** Each panel has its own small inverter that converts DC to AC at the panel. There is no string — panels are wired in parallel at AC, which sums currents rather than voltages.

```
[Panel + Microinverter] ─┐
[Panel + Microinverter] ─┤→ AC Trunk Cable → Combiner → Service Panel
[Panel + Microinverter] ─┘
(each panel is independently AC; no DC strings)
```

**Strengths:**
- Best shading tolerance — each panel is fully independent
- Best per-panel monitoring — individual production visible in real time
- No string sizing calculations required
- Easiest to expand — adding panels is as simple as adding another microinverter and trunk cable segment
- Inherent rapid shutdown compliance (no DC strings above module level)
- No high-voltage DC on the roof — safer to work around post-installation
- 25-year product warranty (Enphase) matches panel lifespan

**Weaknesses:**
- Highest component cost (one inverter per panel)
- More failure points per installation (though Enphase microinverter reliability is excellent in practice)
- Trunk cable routing can be complex on irregular roof layouts
- AC trunk cable requires its own conduit run to service panel
- Per-unit replacement: a failed microinverter means accessing the panel to swap it

**Best for:**
- Shaded roofs (even partial shading benefits significantly from microinverters)
- Complex roof shapes with multiple orientations
- Homeowners who value monitoring data and future expandability
- DIY installs (simpler wiring, no dangerous high-voltage DC)

**Major brands:** Enphase (dominant; IQ8 series in 2026), APSystems, Hoymiles (less common in US residential)

## Cost Comparison (2026 Estimates, 10-Panel System)

| Architecture | Inverter/Optimizer Cost | Notes |
|-------------|------------------------|-------|
| String inverter only | $1,500–$2,500 (single unit) | Add $500–$1,000 for external rapid shutdown devices |
| String + optimizers | $2,500–$4,000 (inverter + 10 optimizers) | Optimizer + inverter as package |
| Microinverters | $3,500–$5,500 (10 microinverters + trunk cable) | Higher upfront, no central inverter to fail |

For a 20-panel system, multiply roughly proportionally.

## Shading Sensitivity Analysis

This is the most important factor in the topology decision.

| Shading Scenario | String Inverter | Optimizers | Microinverters |
|-----------------|-----------------|------------|----------------|
| No shading | Best efficiency | Slight loss to optimizer overhead | Slight loss to optimizer overhead |
| Single panel partially shaded 1hr/day | Entire string impacted | Only affected panel impacted | Only affected panel impacted |
| One panel fully shaded midday | String may produce 50–70% of potential | 90–95% of potential | 90–95% of potential |
| Multiple panels shaded by tree | Catastrophic string loss | Near-normal production on unshaded panels | Near-normal on unshaded panels |
| East-west split roof (two orientations) | Requires two strings, two MPPT inputs | Handles naturally | Handles naturally |

**Rule of thumb:** If any panel is shaded for more than 30 minutes during peak hours (10am–2pm) on a typical day, avoid a plain string inverter.

## Monitoring Comparison

| Capability | String Only | Optimizers | Microinverters |
|------------|-------------|------------|----------------|
| System-level production | ✓ | ✓ | ✓ |
| String-level production | Some (per MPPT input) | ✓ | n/a |
| Panel-level production | ✗ | ✓ | ✓ |
| Panel-level fault detection | ✗ | ✓ | ✓ |
| Diagnosing shading vs. failure | Difficult | Easy | Easy |

**If monitoring granularity matters to you** — optimizers and microinverters both deliver it.

## Expandability Comparison

Future expansion (adding panels):
- **String inverter**: Must fit within existing string voltage/current limits; may require redesigning strings
- **Optimizers**: Adding panels is relatively easy but may require inverter upgrade if pushing capacity limits
- **Microinverters**: Add any number of panels independently — just extend the trunk cable

If you plan to add panels later (common when EV arrives), microinverters make future expansion trivial.

## The 2026 Decision Framework

**Choose microinverters (Enphase IQ8+) if:**
- Your roof has any shading from trees, chimneys, or neighboring structures
- You have multiple roof orientations (east + west, or south + east)
- You want per-panel monitoring and easy fault diagnosis
- You may want to add panels in the future
- You're doing DIY (no dangerous high-voltage DC)

**Choose string + optimizers (SolarEdge) if:**
- You have moderate shading and want per-panel MPPT
- You're price-sensitive vs. microinverters but want shading tolerance
- You're doing a large array (>20 panels) where single-inverter AC is simpler to wire

**Choose plain string inverter if:**
- Your array is large and completely unshaded (no trees, no chimneys, perfect orientation)
- Budget is the primary constraint and you accept the trade-offs
- You're doing a ground mount in an open field

## Hybrid Inverter Consideration

If you're adding or plan to add batteries, consider a hybrid inverter:
- **Enphase IQ Battery**: Fully AC-coupled; works with any inverter system
- **SolarEdge Home Hub**: DC-coupled hybrid; requires SolarEdge optimizers
- **Sol-Ark, Schneider XW+, Victron**: Hybrid inverters for off-grid or whole-home battery backup

If using microinverters and you plan to add battery later, the Enphase ecosystem (IQ microinverters + IQ Battery + IQ System Controller) is the cleanest integration.

## Related

- String sizing math (for string inverter selection): `../../product/concepts/system-design-fundamentals.md`
- Inverter types deep dive: `../../product/concepts/inverter-types.md`
- Grid-tied vs hybrid decision: `grid-tied-vs-hybrid.md`
