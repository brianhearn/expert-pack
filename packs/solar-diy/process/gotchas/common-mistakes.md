---
title: "Common Mistakes in Residential Solar Projects"
type: "gotcha"
tags: [common-mistakes, installation, nec-rapid-shutdown, permitting, process, string-sizing, system-design]
pack: "solar-diy-process"
retrieval_strategy: "atomic"
id: solar-diy/process/gotchas/common-mistakes
verified_at: "2026-04-21"
verified_by: agent
schema_version: "4.1"
concept_scope: single
---

# Common Mistakes in Residential Solar Projects

<!-- context: section=process, topic=common-mistakes, related=system-design,permitting,installation,nec-rapid-shutdown,string-sizing -->

> **Lead summary:** Most solar project failures are preventable. The most costly mistakes happen at three points: string sizing errors (Phase 2), skipping or rushing the permit process (Phase 4), and incorrect service panel work (Phase 5). This file documents the most common mistakes organized by project phase, with prevention patterns.

## Design Mistakes

### 1. Installing on a Roof That Needs Replacing
**Mistake:** Mounting solar on a 15-year-old roof without assessing remaining life.
**What happens:** Roof fails in year 8; removing and reinstalling panels costs $2,000–$6,000.
**Prevention:** If roof is 15+ years old or showing wear, re-roof first. Solar has a 25–30 year lifespan — the roof needs to match it.

### 2. Underestimating Shading
**Mistake:** Designing for an "mostly clear" roof without doing a shading analysis.
**What happens:** A chimney shadow, dormers, or tree branches that seemed minor turn out to kill production 2–4 hours/day.
**Prevention:** Do a proper shade analysis at solar noon for the worst shading months (November-January). Use a shading tool or the Solmetric SunEye app.

### 3. Sizing to Current Consumption, Not Future
**Mistake:** Sizing the array for today's electricity bill, forgetting about the EV you're buying next year.
**What happens:** System is immediately undersized; adding panels later is possible but more expensive (permits, labor).
**Prevention:** Model expected future loads — EV, heat pump, pool heat, etc. — and size for the 5-year future load.

### 4. String Sizing Math Errors
**Mistake:** Using nominal voltage instead of temperature-corrected voltage for string sizing.
**What happens:** Maximum string voltage exceeds inverter's rated input voltage on cold mornings → inverter trips on overvoltage or sustains damage over time.
**Prevention:** Use actual Voc temperature coefficients and ASHRAE design temperatures. Run both max and min string calculations. When in doubt, reduce string length by one panel.

### 5. Ignoring the 120% Rule
**Mistake:** Designing a system that requires a solar breaker larger than 20% of your panel bus bar rating.
**What happens:** Permit rejection; must redesign with supply-side connection or panel upgrade.
**Prevention:** Calculate service panel capacity before finalizing system size: solar breaker ≤ 20% of bus bar rating.

## Permit & Utility Gotchas

### 6. Waiting to Start the Interconnection Application
**Mistake:** Submitting the interconnection application after the building permit is approved.
**What happens:** Building permit takes 3 weeks; utility interconnection takes 10 weeks. You're waiting an extra 7 weeks for no reason.
**Prevention:** Submit both applications the same week. They run in parallel. The utility process is often the critical path.

### 7. Net Metering Enrollment Mixup
**Mistake:** Assuming you're automatically enrolled in net metering when you interconnect.
**What happens:** System goes live; you're billing on a non-NEM tariff for months before someone notices.
**Prevention:** Confirm your net metering tariff enrollment separately from the interconnection agreement. Many utilities treat them as separate processes.

### 8. Layout Doesn't Match Permit Drawings
**Mistake:** Minor field adjustments (shifting a row a foot north, removing one panel for a vent) not reflected in permit drawings.
**What happens:** Inspector compares actual layout to permit drawings — if they don't match, failed inspection.
**Prevention:** Permit drawings are the legal document. If you make any changes, revise and re-submit. Even small changes need as-built documentation.

### 9. Assuming Your AHJ Is on the Latest NEC
**Mistake:** Designing rapid shutdown to NEC 2023 requirements when your jurisdiction adopted NEC 2017.
**What happens:** Over-engineering isn't a failure, but under-engineering (designing for 2023 where 2023 is actually more strict than 2017 was for your specific case) can cause issues.
**Prevention:** Call your AHJ and confirm exactly which NEC edition they're enforcing. "Latest NEC" is not universal — many jurisdictions are 1–2 versions behind.

### 10. HOA Surprise
**Mistake:** Not checking HOA requirements before ordering equipment.
**What happens:** HOA requires black-on-black panels only; you ordered silver-framed panels.
**Prevention:** Submit to HOA before ordering. In most states with solar rights laws, HOAs cannot prohibit solar but may impose aesthetic restrictions.

## Installation Mistakes

### 11. Missing or Wrong Labels
**Mistake:** Skipping NEC-required labels or using incorrect wording.
**What happens:** Inspection failure — inspectors check every label.
**Prevention:** Use a comprehensive label checklist (see Phase 5). Buy a label kit designed for NEC 690 compliance — available from solar distributors.

### 12. MC4 Connector Brand Mixing
**Mistake:** Using MC4 connectors from different manufacturers in the same connection.
**What happens:** Mixed-brand MC4 connections are a code violation and a known fire cause — they can arc internally due to dimensional differences.
**Prevention:** Use the same brand MC4 connectors throughout. If your panels have Stäubli connectors, use Stäubli mating connectors.

### 13. Crossing DC Conductors
**Mistake:** Allowing the positive and negative DC conductors from the same string to contact each other or run in the same conduit without separation.
**What happens:** A fault creates a direct short at high voltage — fire hazard.
**Prevention:** Route positive and negative conductors separately where possible. Where they must run together, use separate conduit or NEC-compliant bundling. Never nick the insulation.

### 14. Roof Mount Not on Rafter
**Mistake:** Installing an L-foot mount between rafters, into sheathing only.
**What happens:** The mount can pull out under wind load — potentially catastrophic in high wind events.
**Prevention:** Use a stud finder from the attic or eave end to locate every rafter. Every mount must have minimum 2.5" embedment into rafter wood.

### 15. Incorrect Flashing
**Mistake:** Using non-approved flashing methods or improper shingle integration.
**What happens:** Roof leak at penetration point — often doesn't manifest until the first heavy rain.
**Prevention:** Use ICC ESR-listed flashing hardware (QuickBOLT, IronRidge Flashkit, QuickMount PV). Follow the exact installation sequence: remove shingle → seal → bolt → seal → reinstall shingle over flashing foot, under shingle above.

### 16. Working Alone on the Roof
**Mistake:** Solo roof work to save time.
**What happens:** Falls from residential roofs are frequently fatal. No one to call for help, no one to supervise.
**Prevention:** Never work alone on a roof. Always have a second person present.

## Electrical Gotchas

### 17. Forgetting Torque Requirements
**Mistake:** Not torquing wire terminations to manufacturer specifications.
**What happens:** Loose terminations create resistance → heat → fire over time.
**Prevention:** Use a calibrated torque screwdriver for all inverter terminal connections. Record that you torqued them (some inspectors ask).

### 18. Battery in Unconditioned Space
**Mistake:** Installing an LFP battery in a garage or storage space where temperatures exceed manufacturer limits.
**What happens:** Batteries outside their temperature operating range can fail prematurely, have reduced capacity, or (in extreme cases) thermal events.
**Prevention:** Check manufacturer's operating temperature spec: Tesla Powerwall 3 (32°F–122°F / 0°C–50°C), Enphase IQ Battery similar. In hot climates, a south-facing garage can exceed 120°F in summer — check ambient temps.

### 19. AC Coupling Incompatibility
**Mistake:** Buying a battery system without verifying it's compatible with your inverter.
**What happens:** Incompatible inverter/battery combinations can create AC frequency shifting issues during backup mode — one system may not play nicely with the other's islanding behavior.
**Prevention:** Verify inverter and battery compatibility explicitly with both manufacturers before purchasing. Stick to proven combinations (Enphase IQ Battery + Enphase inverters; Tesla Powerwall with compatible gateway).

## Post-Commissioning Mistakes

### 20. Not Setting Up Monitoring Alerts
**Mistake:** Commissioning the system and then just assuming it works.
**What happens:** A microinverter fails, a string goes offline, or production drops 20% — you don't notice for months.
**Prevention:** Set up production alerts in your monitoring platform on day one. A "no production" or "low production" alert should notify you within 24 hours.

### 21. Ignoring the First-Year Warranty Window
**Mistake:** Noticing a panel hotspot or microinverter failure but not reporting it promptly.
**What happens:** Many product warranties require claims within specific timeframes; delayed reporting can complicate claims.
**Prevention:** Do a detailed visual inspection at 3 months and 12 months. Check monitoring data monthly. File warranty claims promptly — document with photos and monitoring data.

## Related

- Phase 5 installation detail: `../phases/05-installation.md`
- Phase 4 permit detail: `../phases/04-permitting.md`
- Phase 2 string sizing: `../phases/02-system-design.md`
- NEC rapid shutdown requirements: `../../product/concepts/nec-rapid-shutdown.md`
