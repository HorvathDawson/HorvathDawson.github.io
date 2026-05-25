---
title: "Dimensions, Tire Choice & Narrowing"
date: 2026-02-15
status: in-progress
epic: narrowing
kind: tutorial
tags: [suspension, geometry, analysis, miata, research]
---

How much the Miata front suspension has to narrow to fit inside the A40 fenders, and what tire/wheel goes on the corner. Geometry consequences (RC, camber, scrub, anti-dive) are worked out in the [geometry design reference](./geometry-design-reference); this post sets the dimensional inputs.

---

## Inputs

| | A40 Devon | Miata NA | Δ (A40 − Miata) |
|---|---|---|---|
| Wheelbase | 2350 mm | 2265 mm | +85 mm |
| Front track | 1232 mm | 1420 mm | −188 mm |
| Stock tire | 5.25-16 (133 × 646 mm) | 185/60R14 (185 × 577 mm) | width −52 mm, OD +69 mm |
| Stock outer-to-outer | 1365 mm | 1525 mm | −160 mm |
| Stock wheel | 16 in steel, no offset | 14×6, ET40 | — |
| Bolt pattern | 4-stud | 4×100 | converting to 4×100 |
| Curb weight | ~1010 kg (build target ~950 kg, [build constants](./build-constants)) | — | — |

A40 numbers from [automobile-catalog](https://www.automobile-catalog.com/car/1950/1767110/austin_a40_deluxe_devon.html) and [classiccarportraits](https://www.classiccarportraits.co.uk/pages/Austin_A40_Devon_4752.htm).

**Starting point** for the narrowed track is the original A40 front track (**1232 mm**). The actual fender envelope comes from the body scan; final track gets adjusted within that envelope. Standard clearance budget for a build like this is 25-50 mm per side between sidewall and fender lip — accounts for full bump, steering lock, and tire growth.

---

## Wheel and tire

Same size all four corners, 4×100 hubs (Miata), steel wheel so the original A40 hubcaps fit. Tire diameter has two paths:

| Path | Tire example | OD | Trade-off |
|---|---|---|---|
| **Match A40 stock height** | 205/65R15 | 648 mm | Period-correct ride height; entire suspension assembly translates up with the tire on a custom frame, so local geometry is preserved (camber curve, KPI, scrub all unchanged). |
| Stay near Miata stock | 185/60R15 | 603 mm | Suspension closer to factory; car sits low and wheels look small in the A40 fenders. |

**Decision: 205/65R15 on 15×6 ET+38** (see [build constants](./build-constants)). Near-perfect match to the original 646 mm OD. 205 mm width is wider than stock but the 15 in sidewall keeps the period look, and the bigger contact patch helps put the SR20DET's power down.

---

## Tire width × ET vs A40 envelope

For a fixed narrowed track (1230 mm hub-to-hub), the outer edge of the tire is set by tire width and wheel ET only — track itself doesn't depend on ET. The table gives outer-to-outer delta vs the stock A40 outer-to-outer (1365 mm). Negative = tucks inside the stock A40 envelope; positive = pokes outboard of it.

$$\text{outer-to-outer} = T_{narrowed} + w_{tire} - 2\,\text{ET} \qquad \Delta = \text{outer-to-outer} - 1365$$

| Tire width | ET25 | ET30 | ET38 | ET45 |
|---|---|---|---|---|
| 175 mm | +15 | +5 | −11 | −25 |
| 185 mm | +25 | +15 | −1 | −15 |
| 195 mm | +35 | +25 | +9 | −5 |
| **205 mm (chosen)** | +45 | +35 | **+19** | +5 |

All values in mm of outer-to-outer delta vs A40 stock (1365 mm). Lower ET pushes the tire outboard; every 10 mm of ET reduction grows outer-to-outer by 20 mm (10 per side).

The chosen 205/ET+38 sits 19 mm outboard of stock A40 outer-to-outer (≈10 mm per side). The body scan gives the actual fender envelope to confirm this fits with the clearance budget; if it's tight, options are higher ET (ET+45 lands +5 mm), narrower tire, or a small fender flare.

---

## Narrowing target

**1230 mm front track, 95 mm narrowing per side — locked.** Within 2 mm of the stock A40 front track, with the chosen 205/ET+38 wheel/tire landing within the body-scan envelope. Pickup-point coordinates and donor-side dimensions are in the [geometry design reference](./geometry-design-reference#numbers).

### Geometry implications of the scanned donor

The donor front subframe was photogrammetrically scanned (Einstar 2). The values that follow come from that scan and drive every downstream kinematic plot. Two consequences of the scanned geometry change how the narrowing has to be executed compared with a naive "translate the LCA inboard 95 mm" approach:

- **UCA pivot sits inboard of LCA pivot, not outboard.** UCA inner pivot is at 368 mm from CL; LCA inner pivot is at 329.5 mm from CL. After narrowing, UCA lands at 273 mm from CL and LCA at 234.5 mm. Frame UCA-bracket clearance against the SR20 valve cover and the inner fender both want a check at this new inboard position.
- **Arm-length ratio is 1.34 : 1, not the textbook ~1.9 : 1.** LCA effective length (BJ → pivot) is 336.25 mm; UCA effective length is 250 mm. Closer-to-equal arms give a longer FVSA, a lower roll centre, and less negative camber gain per millimetre of bump than the more-unequal arm ratio commonly assumed for a Miata. The build's static negative camber needs to come from knuckle offset / shim packs, not from the camber curve.
- **UCA bushing axis is canted in plan and tilted in side view.** Side view: front pivot sits 13.56 mm higher than the rear over a 220 mm fa span ≈ 3.5° nose-up. Plan: the bushing axis is not parallel to car fa — the UCA arm is symmetric ±110 mm in its own frame, but its inboard pivot centre projects ~54 mm forward of UBJ in car-frame fa. Frame UCA brackets must replicate both rotations, not just position. The ±1 mm pickup tolerance below applies to the pivot **centre**; orientation error compounds with arm length and is just as important.
- **Caster is real (3.62°) and mechanical trail is +7.57 mm.** That gives the steering meaningful self-centring without relying on the EPAS column to manufacture all of the on-centre feel through torque overlay.

The lower arm itself — fa span between front and rear pivots (322.5 mm c-to-c), BJ offset relative to the front pivot (+25 mm fwd), z-rise from BJ to pivot line (+25 mm) — matches what the published Miata drawings show, so the donor LCA stays as-is. The UCA, the UCA bracket geometry, and the LCA inner-pivot position in the frame are the new fabrication inputs.

### Fabrication notes

- **UCA bracket orientation matters.** Holding the position to ±1 mm is necessary but not sufficient. The bracket bore axis has to be canted to match the scanned side-view tilt (3.5° nose-up) and the plan-view cant inferred from the symmetric-arm reconciliation. Fixture the brackets off the actual UCA arm + a scanned bushing axis, not off generic centerlines.
- **LCA inner-pivot lateral is 234.5 mm from CL.** This is the narrowed value (329.5 − 95). Both LCA pivots share that lateral; fa positions track the scanned 322.5 mm span at the BJ-+25 mm reference.
- **UCA inner-pivot lateral is 273 mm from CL.** This places the UCA bracket inboard of the LCA bracket by 38.5 mm — opposite of what published Miata drawings imply. Verify clearance against the SR20 valve cover, exhaust manifold side, and the inner fender wheel-well before committing to the bracket position.
- **Hub-face position references the wheel-CL, not the LBJ.** Hub face sits at half-track + wheel offset = 615 + ET mm from CL. With ET+38 wheels that puts hub face at 653 mm; with ET+45 at 660 mm. The scanned LBJ-to-hub offset (84.25 mm inboard, 3.75 mm aft, 86 mm down) is taken from the hub face plane and is invariant under narrowing.

### Full-lock-and-full-bump caveat

The envelope check above is done at ride height. Sweeping the tire through the steering arc at ride height clears the body; sweeping it through the bump travel with the wheels pointed straight also clears. The one combination that doesn't quite clear is **simultaneous full steering lock + full suspension compression** — the inboard front corner of the tire kisses the inner fender / wheel arch by a few millimetres.

It's not enough to justify another 5–10 mm of narrowing per side (which would compound back into the rack-narrowing, the inboard pickup geometry, and the front RC height). Three options for handling it, in order of preference:

1. **Steering-lock stops.** Add adjustable hard stops on the rack (or on the knuckle) that pull a couple degrees off maximum lock. Loses some low-speed turning-circle, costs nothing in suspension geometry. Easy to dial in once the car is together.
2. **Bump-stop progression.** A slightly stiffer bump stop limits how much travel is actually available at full lock — the car would have to be cornering *and* hit a bump big enough to use all of bump travel at the same time, which is a vanishingly rare load case for a street car.
3. **Local inner-fender massage.** Roll or trim the few millimetres of inner fender at the contact point. Cheapest fix if the interference shows up worse than predicted at mock-up.

Decision deferred until the front subframe is on the jig and a real steering knuckle + tire can be swept against the actual body. The expected outcome is option 1 (lock stops). Not changing the 1230 mm number over a few millimetres in the worst-case corner of the envelope.
