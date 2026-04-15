---
title: "Suspension Analyzer V2 Results"
date: 2026-02-17
status: in-progress
epic: narrowing
tags: [suspension, geometry, software, analysis]
---

This post will hold screenshots and iteration results from the SA V2 analysis. The workflow checklist and rationale behind each check are in the geometry design reference post.

## Required SA V2 inputs

**Vehicle parameters:**
- **A40 wheelbase:** 2350mm (known)
- Estimated curb weight and front/rear distribution
- Estimated COG height (currently ~575mm, pending measurement)
- Sprung mass and unsprung mass split

**Miata suspension geometry (from donor subframe measurement):**
- All pickup point coordinates (upper inner front/rear, lower inner front/rear, upper/lower ball joint)
- Steering arm geometry (tie rod attachment on knuckle)
- Spring/damper mount locations (lower on LCA, upper on shock tower)

**Design choices:**
- Target outer-to-outer (baseline: 1415mm) and tire width (baseline: 185mm), which together set the track width
- Shock tower position (upper coilover mount)
- Rack mount position (height and fore-aft)
- ARB mounting geometry (arm length, end-link spacing, pivot bushing locations)

---

## Expected outputs

These are the values the SA V2 analysis is expected to produce. All are TBD pending measurement of pickup coordinates from the donor.

- **Front roll center height** at ride height (authoritative value for all roll stiffness and jacking calculations)
- **Front roll center migration** per degree of body roll and per mm of dive
- **Camber curve** through full travel (+/-75mm at wheel)
- **Corrective camber gain** per degree of body roll (used to set static camber targets)
- **Anti-dive and anti-squat percentages** at A40 wheelbase (2350mm)
- **Motion ratio** at the planned shock tower position
- **Ackermann error** across full steering lock range at the planned rack mount position
- **Steering ratio** (degrees of steering wheel per degree of outer wheel lock)
- **Required ARB roll stiffness split** (front/rear) to hit 3-4 degree body roll target at A40 CG

---

More to come with screenshots and actual analysis results as I work through the iterations.
