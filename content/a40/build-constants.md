---
title: "Build Constants Reference"
date: 2026-02-15
status: in-progress
epic: design
kind: reference
tags: [reference, constants, geometry, mass]
---

A single source of truth for the headline numbers used across the rest of the build log. If a value is contested or being refined, it is flagged here. Where a more detailed analysis exists, a link is provided.

> Numbers marked **(target)** are design intent. Numbers marked **(working)** are current best estimates that may shift as fabrication progresses. Numbers marked **(locked)** are committed and used to drive other dimensions.

---

## Vehicle and chassis

| Parameter | Value | Notes |
|---|---|---|
| Total mass (curb) | ~950 kg **(working)** | Estimate. Will be re-measured after frame and drivetrain are in. |
| Sprung mass | ~850 kg **(working)** | Total minus wheels, hubs, brakes, half of arms and axle. |
| Centre of gravity height | ~575 mm ±50 **(working)** | Used for roll-stiffness math. Will be refined once the build is rolling. |
| Wheelbase | 2350 mm **(locked)** | Frame is being designed around this. |
| Front track | 1230 mm **(locked)** | Falls out of 95 mm/side narrowing on a 205/65R15 ET+38 wheel. Nearly matches the stock A40 front track of 1232 mm. Minor tire-to-body interference at simultaneous full steering lock + full bump is a known caveat — see [narrowing analysis](./narrowing-analysis#full-lock-and-full-bump-caveat). |
| Rear track | 1340 mm **(locked)** | Drives the Ford 9" narrowing target. |

## Wheels and tires

| Parameter | Value | Notes |
|---|---|---|
| Tire | 205/65R15 **(locked)** | Same size front and rear. |
| Wheel diameter | 15" **(locked)** | |
| Bolt pattern | 4x100 **(locked)** | Unified across front and rear. Drives Moser axle flange spec on the Ford 9". |
| Wheel offset (purchased) | ET+38 **(locked)** | Wheels on hand. All current geometry math uses this number. |
| Wheel offset (reference baseline) | ET+45 | Earlier analysis used this; legacy text in the geometry reference may still cite it. ET+38 is the working value. |

## Suspension geometry

| Parameter | Value | Notes |
|---|---|---|
| Front narrowing per side | 95 mm **(working)** | 190 mm total off the rack, sets the new outer-to-outer of the lower control arm pickups. |
| Front motion ratio (spring/wheel) | ~0.63 **(working)** | Used in spring-rate sizing. |
| Rear coilover spring base | ~950 mm **(working)** | Lateral spacing between the two rear coilovers on the axle housing (near the bearing caps on the narrowed 9"). Sets the lever arm for rear roll stiffness. |

## Drivetrain

| Parameter | Value | Notes |
|---|---|---|
| Engine | SR20DET **(locked)** | |
| Transmission | CD009 (350Z 6-speed) **(leaning)** | Adapter plate to SR20 bellhousing pattern. OEM SR20 5-speed is the fallback. Tunnel sized to the larger CD009 envelope so either fits. |
| Rear axle | Ford 9", 31-spline **(locked)** | Stock-width housing on hand, narrowing to the 1340 mm rear track. Custom Moser axles, 4x100 flanges machined to spec (not a redrill). |

---

## Refining the CG estimate from CAD

The 575 mm CG height above is a top-down estimate (Miata 460 mm + ~115 mm for the taller body and higher seating position) with a ±50 mm uncertainty band. Roll, weight transfer, and ARB sizing are all linear in $h_{CG}$, so tightening that number meaningfully tightens the whole downstream geometry math.

The bottom-up version is a weighted average over the major mass items, $h_{CG} = \sum m_i z_i / \sum m_i$. The list below is the minimum set of items to locate in CAD — modeled at their actual mounted position — to get an estimate within ~30 mm of the true value once the build is rolling.

| Item | Mass (kg, est.) | Why it matters | Where the CoG comes from |
|---|---|---|---|
| Engine (SR20DET, dressed) | 165–185 | Single largest mass; sits low and far forward. Dominates front-axle weight bias. | Nissan service data lists CoG offset from front face / crank centerline; verify against a CAD bare block + accessory pack. |
| Transmission (CD009 or SR20 5-spd) | 50–70 | Long lever arm rearward of engine; sits low in tunnel. | Service data or measured from a known reference on the case; CAD block model is fine. |
| Body shell (stripped, painted) | 200–260 | Largest single contributor to CG **height** because it sits high. ±10 mm in the body's vertical centroid moves the whole-car CG by ~3 mm. | Volumetric centroid of the laser scan, weighted uniformly (acceptable approximation since sheet metal thickness is roughly constant). |
| Ladder frame (welded) | 70–110 | Sits low; pulls CG down. Important to model since it's a custom part with no published number. | Volumetric centroid of the CAD frame model (uniform tube wall density). |
| Fuel (full tank) | 45–55 | Sits low and rearward; pulls CG down and aft. Worth modeling at both full and empty to bracket the operating range. | Geometric centroid of the tank's wetted volume at the chosen fill level. |
| Driver (+ passenger if relevant) | 75 each | Sits high (~450–550 mm above floor). One occupant raises CG noticeably; two raises it more and shifts the balance. | Standard automotive 75 kg occupant model; CoG roughly at sternum height in the seated H-point reference. |
| Rear axle assembly (housing + diff + brakes + wheels) | 80–110 | Sits low at axle centerline. Mostly unsprung but still part of the total-vehicle CG. | CAD axle model + published Ford 9" diff weight + measured wheel/tire/brake corner. |
| Front suspension corners (×2) | 25–30 each | Unsprung mass at hub centerline height. | Sum of wheel/tire + hub + brake + half of arms; measure off the bench. |
| Battery | 15–20 | Small mass but easy to relocate; moving it from front engine bay to rear (boot floor) shifts F/R balance ~1–2%. Height effect is small. | Geometric centroid of the case at the chosen mounting location. |
| Seats (×1 or ×2) | 12–18 each | Sits at floor pan height; pulls CG down slightly relative to occupant. | Geometric centroid of the seat shell in CAD. |
| Radiator + coolant (full) | 8–12 | Sits at front of car, low. Small but worth including for F/R balance. | Geometric centroid of the core at its mounted position. |
| Exhaust system (header to tailpipe) | 12–18 | Long, thin, low. Negligible height effect; small rearward bias contribution. | Centerline of the exhaust path, treated as a uniform line mass in CAD. |
| Driveshaft | 8–12 | Centerline at floor height, mid-car. Negligible effect; include for completeness. | Geometric centroid (midpoint) of the shaft. |

Items deliberately left off the major-mass list because their combined contribution is below the existing ±50 mm CG uncertainty: wiring harness, brake/fuel lines, interior trim, glass, bumpers, lights, hardware. Those get rolled into a "miscellaneous" lump (~30–50 kg) at the body shell's CoG and revisited only if a tight CG target is needed.

**CAD workflow to produce an estimated CG:**

1. Place each item from the table at its actual mounted position in the assembly.
2. Assign each part its estimated mass (or measured mass once available).
3. Use the CAD package's mass-properties tool on the full assembly; it returns the weighted CoG directly.
4. Re-run with the fuel tank empty and with/without passenger to bracket the operating range.

This gets the estimate from "Miata + 115 mm" (current basis) to a CAD-derived number with traceable inputs. Worth doing once the body scan, frame CAD, and engine model are all in the same assembly.

---

This page is the canonical source. Any other post that contradicts it is out of date — please update either this file or the offending post when you spot a mismatch.
