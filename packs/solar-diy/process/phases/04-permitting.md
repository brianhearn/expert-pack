# Phase 4: Permitting & Utility Interconnection

> **Lead summary:** Permitting is the longest phase for most projects — not because the work is hard, but because of queue times. A building permit typically takes 1–4 weeks; utility interconnection approval takes 4–12 weeks (and up to 6 months in congested areas). You'll need both before you can legally operate your system. Start both applications as early as possible and run them in parallel.

## Overview of What's Required

Most residential solar projects require three approvals:
1. **Building permit** — from your local jurisdiction (city, county, or AHJ — Authority Having Jurisdiction)
2. **Utility interconnection agreement** — from your electric utility (may involve both distribution and metering departments)
3. **HOA approval** (if applicable) — from your homeowners association

These are entirely independent processes. Don't wait for one before starting the others.

## 1. Building Permit

### Who Issues It
Your local building department — could be a city building department, county development services, or a regional fire authority for rapid shutdown review. Look up your AHJ at the NABCEP website or simply search "[your city/county] solar permit."

### What They Review
- **Structural**: That the racking system, roof structure, and panel loading are code-compliant. Many jurisdictions accept manufacturer structural engineering letters for standard residential installs.
- **Electrical**: That the system wiring, overcurrent protection, grounding, and disconnects comply with NEC (local adoption — verify whether your AHJ is on NEC 2017, 2020, or 2023).
- **Rapid shutdown compliance**: Per your jurisdiction's NEC version — this is closely reviewed.
- **Fire setbacks**: Confirm required ridge setback (3 feet NEC; 18" edges is common but some jurisdictions require 36" for pathways).

### What You'll Submit
Typical permit package includes:
- **Site plan**: Aerial view showing roof with panel layout, setbacks, and obstructions (can be from Google Maps or satellite with annotations)
- **Electrical single-line diagram (SLD)**: Shows the complete electrical path from panels to utility meter. Most component manufacturers provide templates; many AHJs have their own fillable forms.
- **Roof plan/structural details**: Panel layout on roof with rafter locations, racking specs, and mount details
- **Equipment cut sheets**: One-page datasheets for panels, inverter, batteries, and racking (from manufacturer websites)
- **Equipment specifications / listings**: UL 1703, UL 1741, UL 9540 confirmations; some AHJs require ICC ESR listing for penetration hardware
- **Load calculation** (sometimes): Showing your service panel has capacity under NEC 705.12

### The 120% Rule (NEC 705.12)
NEC 705.12(B)(2) governs how solar connects to your main service panel. The key calculation:
```
(Panel bus bar rating + Solar breaker size) ≤ 120% of panel bus bar rating
```
Or equivalently:
```
Solar breaker size ≤ 20% of panel bus bar rating
```
**Example**: 200A panel bus, solar breaker can be max 40A. A 40A breaker serves a 7.6 kW AC system (240V × 40A ÷ 1.25).

If your solar output requires a larger breaker, you have options:
- **Load-side solar: use a supply-side connection** (above the main breaker, requires utility permission and different equipment)
- **Bus bar tap**: Connect at the far end of the bus bar opposite the main breaker (NEC 705.12(B)(2)(b))
- **Upgrade service panel**: Expensive but sometimes necessary

### Self-Permitting vs Permit Service
- Most jurisdictions allow homeowners to pull their own permits ("homeowner-builder" exemption)
- Some jurisdictions require a licensed electrical contractor
- Third-party permit services (ExpressSolarPermit, PermitFlow, SolarPermitServices) can handle the package prep and submission for $200–$500 — worth it for DIYers who haven't done this before
- Solar-specific software (Aurora, OpenSolar, Solargraf) generates permit packages automatically from your design

### Permit Fees
- Typically $200–$800 for residential solar
- Some jurisdictions have adopted flat-fee or streamlined solar permits (SolarAPP+ — check if your jurisdiction participates)
- Inspection fees are usually separate ($75–$200)

## 2. Utility Interconnection

### Process Overview
The interconnection process authorizes your system to connect to and export power to the grid.

1. **Submit application**: Online portal or paper form. Requires your system specs (size, equipment, single-line diagram).
2. **Application review**: Utility engineering reviews for technical compliance. For systems <10 kW, this is often an expedited "fast track" review.
3. **Approval**: You receive a Permission to Install (PTI) or similar letter. This does NOT mean you can energize — it's permission to install.
4. **Installation**: Complete your installation and pass building inspection.
5. **Interconnection inspection**: Utility may send a technician to inspect your equipment (not all utilities require this).
6. **Permission to Operate (PTO)**: After inspections pass, utility issues PTO. The utility installs a net meter (bidirectional meter). Now you can flip the switch.

### Timeline Reality
- Fast-track (small systems, simple feeders): 4–8 weeks
- Standard review: 8–16 weeks
- Congested feeders or high-solar-penetration areas: 6–18 months (not a typo)
- Some utilities in California, Arizona, and other high-solar states have significant backlogs
- **Submit your interconnection application the same week you submit your building permit application — don't wait**

### Net Metering and Billing
- **Net metering (NEM 1.0/2.0)**: Excess solar production credited at full retail rate. Most favorable economics.
- **Net billing (CA NEM 3.0 style)**: Credits calculated at avoided-cost rate (much lower than retail). Makes battery storage much more valuable.
- **Buy-all/sell-all**: Some utilities require you to sell all production at wholesale rate and buy all consumption at retail — very unfavorable; rare in residential.
- Verify your specific utility and rate class — these policies vary enormously and change frequently.

### Utility-Required Equipment
Many utilities have specific equipment requirements:
- **Interconnection switch**: External AC disconnect visible and accessible from the utility meter (lockable)
- **Production meter socket**: Some utilities require a separate production meter (CT-based or separate socket)
- **Anti-islanding**: All grid-tied inverters must have anti-islanding protection (standard in UL 1741-listed equipment)
- **Inverter settings**: Some utilities require specific voltage/frequency trip settings; provide to your electrician

### Net Metering Application
Separate from the interconnection application at some utilities. Enrolling in the correct net metering program can be easy to miss — it determines how your credits are calculated. Confirm you're enrolled correctly before your system goes live.

## 3. HOA Approval (If Applicable)

Many states have "solar rights" laws that limit HOA authority to ban solar panels. Check your state's solar rights legislation before assuming you need approval.

- **Strong solar rights states**: California, Florida, Texas, Colorado, Arizona — HOAs cannot prohibit solar, may only impose reasonable aesthetic restrictions
- **Weaker protections**: Some states allow HOAs to prohibit solar on certain surfaces; check your CC&Rs
- Even with solar rights protection, your HOA may require a design review submission
- Submit early — HOA review boards often meet monthly

**HOA submission typically includes:**
- Photo of planned panel location on roof
- Product images showing panel appearance
- Brief description of system
- Equipment color: black-on-black panels and black racking hardware typically pass HOA review more easily than silver frames and racking

## Permit Phase Checklist

- [ ] Building permit application submitted with complete package
- [ ] Utility interconnection application submitted
- [ ] HOA pre-approval submitted (if applicable)
- [ ] Equipment ordered (or holding for permit approval)
- [ ] Contractor scheduled (if applicable)
- [ ] Building permit approved
- [ ] Utility Permission to Install (PTI) received (or confirmed not required in your jurisdiction)
- [ ] HOA approval received (if applicable)

## What Can Go Wrong

- **Permit rejection**: Missing documentation is the most common cause; resubmit promptly with complete package
- **Utility interconnection delay**: Nothing you can do but follow up. Keep notes of every contact.
- **NEC version mismatch**: Your jurisdiction may be on an older NEC version; verify before designing rapid shutdown
- **Service panel bus bar capacity**: 120% rule may require panel upgrade or supply-side connection — budget for this

## Related

- NEC rapid shutdown requirements: `../../product/concepts/nec-rapid-shutdown.md`
- Phase 5 (Installation): `05-installation.md`
- Common permit gotchas: `../gotchas/common-mistakes.md`
