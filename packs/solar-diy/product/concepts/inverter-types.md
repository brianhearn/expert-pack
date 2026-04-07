---
title: Inverter Types — Microinverters vs String Inverters vs Optimizers
type: concept
tags:
- component-selection
- inverter-topology
- inverter-types
- nec-rapid-shutdown
- product
- system-design-fundamentals
pack: solar-diy-product
retrieval_strategy: standard
---
# Inverter Types — Microinverters vs String Inverters vs Optimizers

<!-- context: section=product, topic=inverter-types, related=system-design-fundamentals,nec-rapid-shutdown,inverter-topology,component-selection -->

> **Lead summary:** There are three main residential inverter architectures: microinverters (one per panel, best for shading/complex roofs, Enphase dominates), string inverters (one central unit, most cost-effective for simple unshaded roofs, SMA/Fronius), and string inverters with power optimizers (SolarEdge's approach — central inverter + per-panel DC optimizers). Microinverters and optimizers are both MLPE and satisfy rapid shutdown requirements. String inverters alone require additional rapid shutdown devices unless using UL 3741 compliant systems.

## The Three Architectures

### Microinverters

Each solar panel gets its own small inverter that converts DC to AC right at the panel.

**How it works:** Panel produces DC → microinverter converts to AC immediately → AC power flows to your electrical panel. Each panel operates completely independently.

**Key brands:** Enphase (dominant market leader — IQ8 and IQ8+ series), AP Systems

<!-- refresh
  decay: fast-moving
  as_of: 2026-Q1
  fields: [enphase_model_series, market_leadership]
  source: https://enphase.com/homeowners/microinverters
  method: "Check Enphase product page for current model series. IQ8 may be superseded by IQ9 or later. Check Solar Power World for market share shifts."
-->

**Pros:**
- Panel-level independence — shading on one panel doesn't affect others
- No single point of failure — if one microinverter fails, all other panels keep producing
- Panel-level monitoring — see exactly how each panel performs
- Inherently satisfies rapid shutdown requirements (MLPE)
- Easy to expand — add panels one at a time
- Safer — no high-voltage DC on the roof (each panel converts to ~240V AC)

**Cons:**
- Higher cost per watt than string inverters
- More components on the roof = more potential failure points over 25 years
- Slightly lower peak efficiency than best string inverters (~96-97% vs ~97-98%)
- Harder to access for replacement (under panels on roof)

**Best for:** Complex roof layouts, partial shading, systems that may expand over time, safety-conscious installations.

### String Inverters

All panels wire together in series (a "string"), and one central inverter handles DC-to-AC conversion.

**How it works:** Panels produce DC → DC flows through series-connected string → central inverter converts to AC. All panels in a string share the same current.

**Key brands:** SMA (Sunny Boy), Fronius (Primo/Symo), SolarEdge (when used without optimizers, rare)

<!-- refresh
  decay: fast-moving
  as_of: 2026-Q1
  fields: [string_inverter_brand_models]
  source: manufacturer product pages (sma.de, fronius.com, solaredge.com)
  method: "Check manufacturer sites for current model lines. Model names change but the architecture concepts above are permanent."
-->

**Pros:**
- Lowest cost per watt
- Fewer total components = simpler system
- Highest peak efficiency (~97-98%)
- Easy to service (inverter is ground-level, accessible)
- Proven technology — decades of track record

**Cons:**
- String-level performance — weakest panel in the string limits the whole string
- Single point of failure — if the inverter fails, entire system goes down
- **Does NOT satisfy rapid shutdown alone** — must add rapid shutdown devices or use UL 3741 compliant installation
- Less granular monitoring (string-level, not panel-level)
- String sizing calculations required (voltage limits based on temperature extremes)

**Best for:** Simple roofs with uniform orientation, no shading, budget-focused installations, ground-mount systems.

### String Inverters + Power Optimizers (SolarEdge)

Hybrid approach: each panel gets a DC-DC power optimizer, but a central string inverter still handles DC-to-AC conversion.

**How it works:** Panel produces DC → optimizer adjusts voltage/current for maximum power (MPPT) at each panel → optimized DC flows to central inverter → inverter converts to AC.

**Key brand:** SolarEdge (this is essentially their entire product strategy)

**Pros:**
- Panel-level optimization — each panel produces its maximum regardless of neighbors
- Panel-level monitoring
- Satisfies rapid shutdown requirements (optimizers are MLPE)
- Central inverter is more cost-effective than microinverters
- Fixed-voltage string output simplifies inverter design

**Cons:**
- SolarEdge optimizers are proprietary — locked into their ecosystem
- Still has single-point-of-failure at the central inverter
- More components than pure string, but fewer than microinverters
- SolarEdge has faced reliability concerns in recent years (higher warranty claim rates reported in the field, as of 2025-2026)

<!-- refresh
  decay: fast-moving
  as_of: 2026-Q1
  fields: [solaredge_reliability_status]
  source: r/solar, Solar Power World, SolarEdge investor relations
  method: "SolarEdge reliability concerns may improve or worsen. Check r/solar for installer sentiment and SolarEdge announcements for product revisions."
-->
- Optimizer failure diagnosis can be confusing — monitoring shows which panel underperforms but physical access is still on-roof

**Best for:** Moderate shading situations, wanting panel-level monitoring without full microinverter cost, mid-range budgets.

## Quick Decision Matrix

| Factor | Microinverter | String | String + Optimizer |
|--------|:---:|:---:|:---:|
| Complex/multi-orientation roof | ✅ Best | ❌ Poor | ✅ Good |
| Partial shading | ✅ Best | ❌ Poor | ✅ Good |
| Lowest cost | ❌ Highest | ✅ Lowest | ⚠️ Middle |
| Rapid shutdown compliance | ✅ Built-in | ❌ Needs addition | ✅ Built-in |
| Expandability | ✅ Easy | ❌ Harder | ⚠️ Medium |
| Monitoring granularity | ✅ Panel-level | ❌ String-level | ✅ Panel-level |
| Single point of failure | ✅ None | ❌ Yes | ❌ Yes (inverter) |

## The UL 3741 Alternative

A newer compliance path allows string inverter systems to meet rapid shutdown without MLPE by using UL 3741-listed PV Hazard Control Systems. These systems use wire management and fault protection instead of per-module electronics. This can reduce component count and long-term maintenance, but adoption is still early and not all AHJs accept it yet. See [[nec-rapid-shutdown.md|NEC Rapid Shutdown]] for details.
