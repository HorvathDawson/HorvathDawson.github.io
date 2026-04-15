---
title: "Dimensions, Tire Choice & Narrowing"
date: 2026-02-15
status: in-progress
epic: narrowing
tags: [suspension, geometry, analysis, miata, research]
---

This post collects the baseline dimensions for both the A40 body and the Miata NA front suspension, works through the tire and wheel decision, then derives how much narrowing is needed to fit Miata suspension inside the A40 fenders.

---

## Austin A40 Devon stock specs

Stock specs for the 1950 Austin A40 Devon ([automobile-catalog](https://www.automobile-catalog.com/car/1950/1767110/austin_a40_deluxe_devon.html), [classiccarportraits](https://www.classiccarportraits.co.uk/pages/Austin_A40_Devon_4752.htm)):

- **Wheelbase:** 2350mm / 92.5in
- **Stock front track:** 1232mm / 48.5in
- **Stock rear track:** 1257mm / 49.5in
- **Overall length:** 3886mm / 153in
- **Overall width:** 1549mm / 61in
- **Overall height:** 1588mm / 62.5in
- **Ground clearance:** 170mm / 6.7in
- **Curb weight:** 1010kg / 2226lbs
- **Construction:** Pressed steel body on steel chassis
- **Original wheels:** 4-stud, 16in pressed steel
- **Original tire size:** 5.25-16 (133mm width, 90 aspect ratio, 16in rim, 646mm / 25.4in total diameter)
- **Steering:** Worm and peg
- **Front suspension:** Coil spring
- **Rear suspension:** Semi-elliptic leaf
- **Brakes front:** Hydraulic drum
- **Brakes rear:** Mechanical drum
- **Drivetrain:** RWD, 4-speed manual (synchro on 2nd, 3rd, 4th)
- **Engine:** 1200cc inline 4, OHV pushrod, 65.5mm bore x 89mm stroke, 7.2:1 compression, single Zenith carb
- **Power:** 40bhp @ 4300rpm
- **Torque:** 79Nm / 58 ft-lb @ 2400rpm
- **Top speed:** ~65mph / ~105km/h
- **0-60 mph:** ~31 sec
- **Fuel consumption:** ~35 mpg (imp) / ~29 mpg (US)
- **Fuel capacity:** 8.7 imp gal / ~40L
- **Estimated Cd:** 0.55
- **Production:** 456,544 Devons (1947-1952)

### Fender clearance measurements

Measured fender-to-fender clearances (rough numbers off the body):

- **Front of fender opening:** 44.5in between fenders + 4.5in depth on each side = 53.5in (~1359mm)
- **Rear of fender opening:** 47in between fenders + 4in depth on each side = 55in (~1397mm)
- **Fender opening length (front to back):** ~27in (~686mm)
- The fender flares out between the front and rear edges, so the widest usable point is somewhere in the middle of the opening.

Standard fender clearances for a build like this are typically 1 to 2 inches (25-50mm) between the tire sidewall and the fender lip on each side. That has to account for full suspension travel (bump and rebound), steering lock at full turn, and any tire growth at speed. Most builders target around 1.5in (38mm) per side as a minimum.

### Measurement cross-check

The stock A40 front track is 1232mm with 133mm section width tires (5.25-16 bias-ply), giving an outer-to-outer of 1232 + 133 = 1365mm. The measured front fender opening is ~1359mm, which is 6mm narrower than the stock tires. That is impossible for a car that left the factory this way.

The most likely source of error is the tape measurement on a curved surface at the narrowest point of the fender opening. Photos of the car show roughly 40-50mm of clearance per side, and external references confirm 175mm tires fit with "plenty of space" on stock fenders. The fender is wider than the tape measurement suggests. This needs to be re-measured with a laser level or straight edge across the inside of the fender lips at the point where the tire sits at straight-ahead.

Other dimensions:

- Available engine bay width: TBD

---

## Wheel and tire choice

Using the Miata 4x100 bolt pattern. The goal is a common modern steel wheel size close in proportion to the original A40 16in pressed steel wheels. Steel wheels so the original A40 hubcaps can go over them. Same size on all four corners.

The original A40 tire (5.25-16) had a total diameter of about 646mm / 25.4in and a width of only 133mm. The Miata NA stock (185/60R14) is about 578mm diameter. That's a 68mm difference in height, which matters for both looks and suspension geometry.

### Two approaches

There are two ways to think about tire choice here, and they have different trade-offs.

**Stay close to Miata stock diameter (~578mm)**
Keeps the Miata suspension geometry closer to factory. The control arm angles relative to the ground stay near where Mazda designed them, so the roll center height, camber curve, and instant center locations are close to stock. Less rework needed in the suspension model. But the car will sit lower than original and the wheels will look small in the A40's fender openings.

| Tire | Width | Diameter | vs Miata | Availability |
|------|-------|----------|----------|-------------|
| 185/60R15 | 185mm | 603mm | +25mm | Common |
| 195/55R16 | 195mm | 621mm | +43mm | Moderate |
| 185/65R15 | 185mm | 621mm | +43mm | Common |

**Match original A40 diameter (~646mm)**
The car sits at the correct ride height with period-correct proportions. The tall sidewall looks right on a vintage car. But the hub center moves up ~34mm compared to Miata stock, which changes the suspension geometry. Here's what happens if you keep the same control arm pickup point locations but increase the tire diameter:

**Roll center stays similar in height but moves relative to the ground.** If the entire suspension (hub, inner pivots, everything) shifts up with the taller tire, the control arm angles relative to the hub stay the same. The roll center height relative to the axle line is preserved. But the roll center is now higher relative to the ground plane, and the CG also moves up. The distance between the CG and roll center (the roll couple) may stay close to the same, so body roll behavior is similar. The real question is whether the roll center height relative to the ground is where you want it for this car's weight and CG.

**Camber curve is preserved through travel.** Since the control arm angles relative to the hub center haven't changed, the camber gain per unit of travel stays the same. Static camber at ride height is the same as Miata stock. This is the main benefit of moving the pickup points up with the ride height.

**Scrub radius stays the same.** The kingpin axis orientation relative to the hub and contact patch doesn't change if the ball joint locations move up with everything else. The ground intersection point moves up the same amount as the contact patch, so scrub radius is unchanged.

**Anti-dive and anti-squat stay similar.** These depend on the side-view instant center location relative to the CG. If the entire suspension moves up with the ride height, the side-view arm angles relative to the hub are the same. The CG shifts up slightly because of the taller tire, but the effect is small.

**Bump steer is not a concern here.** On a swap into an existing chassis, the steering rack mount is fixed and the knuckle moves up, which changes the tie rod angle and introduces bump steer. In this build the frame is custom, so the rack mount moves up along with all the suspension pickups. The tie rod angle relative to the control arms stays the same as Miata stock.

| Tire | Width | Diameter | vs A40 | Availability |
|------|-------|----------|--------|-------------|
| 185/70R15 | 185mm | 640mm | -6mm | Moderate |
| 195/65R15 | 195mm | 635mm | -11mm | Very common |
| 205/65R15 | 205mm | 648mm | +2mm | Common |

### Decision

Going with a tire close to the original A40 diameter. The car should look right and sit at the right height. Since this is a custom frame, every pickup point and mount (suspension, steering rack, subframe) gets placed to match the chosen tire diameter and ride height. The Miata geometry carries over without compromise. All of this gets verified in the SA V2 analysis with the actual dimensions as inputs.

A 185-195mm width keeps the proportions reasonable on a car that originally wore 133mm tires. 205mm starts to look wide.

### Tire width vs fender space

Wider tires only cost the width difference in fender space. With ~90mm total stock clearance (photo estimate), even 195mm tires fit:

| Tire | Width | Extra vs 133mm stock | Remaining clearance (per side) |
|------|-------|---------------------|-------------------------------|
| 5.25-16 (stock) | 133mm | 0mm | ~45mm |
| 175/80R16 | 175mm | 42mm | ~24mm |
| 185/70R15 | 185mm | 52mm | ~19mm |
| 195/65R15 | 195mm | 62mm | ~14mm |

A Devon owner running 175mm tires noted "plenty of space" on stock fenders. A NZ build ([kilroy.co.nz](http://www.kilroy.co.nz/cars/car02.html)) fitted 178mm rims with only subtle flares. The fender is not the hard constraint. The constraint is how much the Miata suspension needs to narrow.

- **Bolt pattern:** 4x100 (Miata)
- **Wheel diameter:** TBD
- **Wheel width:** TBD
- **Tire size:** TBD
- **Style:** Steel wheel with original A40 hubcaps

---

## Part 1: Two options

**Option 1: Shorten the control arms.** The Miata arms are stamped steel, so you can't just cut and sleeve them like tube arms. You'd need to fabricate entirely new arms, or section and reweld the stamped ones. Either way you end up with shorter arms on the same knuckle. Shorter arms increase camber gain per mm of travel (arm length, angles, and kingpin geometry all interact), and the roll centre height becomes harder to predict because it depends on instant-centre geometry rather than arm length alone. You're also putting structural welds in components that see huge loads every time you hit a bump.

**Option 2: Move the inner pickup points inward on the frame.** Keep the arms at or near stock length, keep the knuckle and spindle stock, but mount everything further inboard. This is only possible if you're building a custom frame, which I am.

I'm going with option 2. The arm geometry stays closer to what Mazda designed. Both arm lengths and their installed angles determine camber gain through travel; keeping the arms near stock length with similar pickup-height ratios keeps behaviour close to stock. Roll-centre migration through travel also stays more predictable because the instant-centre geometry is largely preserved. And you don't have to fabricate or modify the arms themselves.

---

## Part 2: Narrowing target

How much does the Miata suspension need to narrow to fit inside the A40? It comes down to four things: the fender opening width, the tire width, the wheel offset, and the clearance budget. This section walks through the logic in plain English, with formulas and a worked example boxed at the end.

### Miata NA

| Parameter | Value | Source |
|-----------|-------|--------|
| Stock front track | 1405mm | Factory spec |
| Stock tire width | 185mm | 185/60R14 factory tire |
| Stock outer-to-outer | 1590mm | Derived: 1405 + 185 |
| Stock wheel offset | ET40 to ET45 | 14x6 factory wheel (varies by year), aftermarket commonly ET35 |

### A40 Devon

| Parameter | Value | Source |
|-----------|-------|--------|
| Stock front track | 1232mm | Factory spec |
| Stock tire width | 133mm | 5.25-16 bias-ply |
| Stock outer-to-outer | 1365mm | Derived: 1232 + 133 |

Fender tape measurements and the cross-check showing they underread are in the stock specs section above. The working baseline outer-to-outer is 1415mm based on photo evidence.

### Tire width

A 185mm tire is 52mm wider than the stock 133mm. Forum evidence and external builds confirm 175mm tires fit with "plenty of space" inside the A40 Devon fenders; 185mm is 10mm wider than that. Every 10mm of extra tire width costs 5mm more narrowing per side at a fixed outer-to-outer.

### Wheel offset

The original A40 had no ET offset (pressed steel wheels). The new build uses Miata 4x100 hubs with modern wheels, so offset matters.

ET sets how far the wheel centerline sits outboard of the hub flange. For a fixed fender envelope and tire width the track is fixed regardless of ET, so ET does not appear in the narrowing formula. What ET does affect is tuck: lower ET pushes the tire outboard relative to the hub, leaving less clearance to the fender at full compression. Stick with ET45 or higher to keep the tire from kissing the fender lip under load.

### Fender scenarios

The fender sets a hard limit on where the tire's outer edge can sit. Track is just outer-to-outer minus tire width. The stock A40 outer-to-outer (1365mm) is the conservative baseline. Photos suggest the fenders allow more room, so here are three scenarios with 185mm tires:

| Outer-to-outer | Track |
|----------------|-------|
| 1365mm (stock envelope) | 1180mm |
| 1390mm (+25mm) | 1205mm |
| 1415mm (+50mm) | 1230mm |

The +50mm row (1230mm track) nearly matches the stock A40 front track of 1232mm.

Photos suggest the usable envelope is somewhere around 1380-1400mm, but external references confirm 175mm tires (42mm wider than stock A40) fit with "plenty of space," so 1415mm (+50mm) is the working baseline.

### Estimated narrowing

At ET45, the Miata hub sits at 747.5mm from centerline. The build's hub position depends on the track. Narrowing per side is the difference between the two:

| Outer-to-outer | Track | Hub from CL | Narrow/side | Hub-to-hub |
|----------------|-------|-------------|-------------|------------|
| 1365mm (stock envelope) | 1180mm | 635mm | 112.5mm | 1270mm |
| 1390mm (+25mm) | 1205mm | 647.5mm | 100mm | 1295mm |
| 1415mm (+50mm) | 1230mm | 660mm | 87.5mm | 1320mm |

### Working assumptions

Baseline: 185mm tire, ET45, 1415mm outer-to-outer. Track = 1230mm, narrowing = 87.5mm per side. This nearly matches the stock A40 front track of 1232mm. Re-measure the A40 fender with a straight edge before committing to pickup locations.

### Formulas

> **Step 1.** Max tire outer-to-outer (fender width minus clearance):
>
> $$W_{outer} = W_{fender} - 2 \times cl$$
>
> **Step 2.** Track width (outer-to-outer minus tire width):
>
> $$T = W_{outer} - w_{tire}$$
>
> **Step 3.** Hub position from vehicle centerline:
>
> $$d_{hub} = \frac{T}{2}$$
>
> **Step 4.** Narrowing per side:
>
> $$\Delta = \frac{T_{Miata} - T}{2} = \frac{1405 - T}{2}$$

> **Worked example (185mm tire, ET45, +50mm envelope 1415mm):**
>
> 1. $W_{outer} = 1415 \text{ mm}$ (+50mm tire envelope)
> 2. $T = 1415 - 185 = 1230 \text{ mm}$
> 3. $d_{hub} = 1230 / 2 = 615 \text{ mm from CL}$
> 4. $\Delta = (1405 - 1230) / 2 = 87.5 \text{ mm per side}$

---

## Required measurements

Before any of this analysis becomes final numbers, these dimensions need to be measured or confirmed from the actual donor car. The geometry design reference post (005b) uses these as inputs — none of the pickup location math is final until this list is complete.

**From the Miata donor:**
- Upper and lower ball joint heights relative to hub centre (LBJ −93.6 mm, UBJ +139.4 mm from photogrammetric scan, not yet verified against donor car)
- Spring/damper lower mount position along the LCA (to confirm motion ratio)
- ARB arm length (pivot axis to end-link attachment on bar)
- Steering rack housing width and tie rod length
- Tie rod attachment point on the knuckle (steering arm geometry)
- **Pickup point positions relative to vehicle centerline and spindle center (see tables below)**

### Lower control arm (LCA)

**Key dimensions from frontcontrolarms.pdf:**

<figure class="wide" style="margin:1rem 0">
  <img src="/assets/projects/a40-austin/blog/reference/arms-p0.png" alt="Miata front control arm key dimensions technical drawing" style="width:100%;border-radius:4px;display:block;margin-bottom:6px" />
  <figcaption>frontcontrolarms.pdf — control arm key dimensions. Educational reference only; verify all values against the donor car before fabrication.</figcaption>
</figure>

<figure style="margin:1rem 0">
  <img src="/assets/projects/a40-austin/blog/reference/lower-control-arm.png" alt="Miata NA lower control arm photo" style="width:100%;border-radius:4px;display:block;margin-bottom:6px" />
  <figcaption>Lower control arm (LCA) — donor photo. A-arm with front and rear inner bushings. Both inner pivots are 328mm from car CL. BJ is 25mm forward of the front pivot; rear pivot is 323.5mm rearward of the front pivot (348.5mm rearward of BJ). Coilover lower mount and ARB end-link visible along the rear blade.</figcaption>
</figure>

<figure style="margin:1rem 0">
  <img src="/assets/projects/a40-austin/blog/plots/lca_plan.png" alt="LCA plan view schematic" style="width:100%" />
  <figcaption>LCA plan view (top-down). BJ at origin (0, 0). +x = outboard, +y = forward. Both inner pivots are 374.5mm inboard of the BJ (= 702.5 − 328mm). BJ is 25mm forward of the front pivot; rear pivot is 348.5mm rearward of BJ. Fore-aft span = 323.5mm. Coilover mount 240mm outboard of the pivot line, +25mm forward. ARB end-link 185mm outboard, +35mm forward.</figcaption>
</figure>

| Dimension | Value | Notes |
|-----------|-------|-------|
| LCA inner pivots from car CL (both front and rear) | 328mm | Confirmed |
| LCA lateral (inboard from Miata hub = 702.5 − 328mm) | 374.5mm | Confirmed |
| BJ forward of LCA front pivot | 25mm | Confirmed |
| LCA fore-aft span (front to rear, c-t-c) | 323.5mm | Confirmed |
| LCA rear pivot rearward of BJ | 348.5mm | Derived (25 + 323.5) |
| Coilover mount from pivot line (perpendicular toward BJ) | 240mm outboard, +25mm fore-aft | Confirmed |
| ARB end-link attachment from pivot line | 185mm outboard, +35mm fore-aft | Confirmed |

### Upper control arm (UCA)

<figure style="margin:1rem 0">
  <img src="/assets/projects/a40-austin/blog/reference/upper-control-arm.png" alt="Miata NA upper control arm photo" style="width:100%;border-radius:4px;display:block;margin-bottom:6px" />
  <figcaption>Upper control arm (UCA) — donor photo. Shorter wishbone. Lateral arm length is 324.5mm (hub centre to inner pivot line). Front pivot is +113.5mm forward of BJ, rear pivot is −143.5mm rearward of BJ (257mm total span). UCA inner pivots sit 50mm outboard of LCA inner pivots on each side (378mm from CL vs 328mm).</figcaption>
</figure>

<figure style="margin:1rem 0">
  <img src="/assets/projects/a40-austin/blog/plots/uca_plan.png" alt="UCA plan view schematic" style="width:100%" />
  <figcaption>UCA plan view (top-down). BJ at origin, +x outboard, +y forward. Both inner pivots are 324.5mm inboard of hub centre (378mm from car CL). UCA pivots sit 50mm outboard of LCA pivots on each side. Front pivot at +113.5mm, rear pivot at −143.5mm from the BJ. Total fore-aft span = 257.0mm. Pivot bushings shown as 56mm rectangles.</figcaption>
</figure>

| Dimension | Value | Notes |
|-----------|-------|-------|
| UCA inner pivots from car CL (both front and rear) | 378mm | Confirmed (702.5 − 324.5); 50mm outboard of LCA |
| UCA arm lateral (hub centre to inner pivot line) | 324.5mm | Confirmed |
| UCA fore-aft front pivot from BJ | +113.5mm | Confirmed |
| UCA fore-aft rear pivot from BJ | −143.5mm | Confirmed |
| UCA front pivot forward of BJ | +113.5mm | Confirmed |
| UCA rear pivot rearward of BJ | −143.5mm | Confirmed |
| UCA front pivot height above LCA pivot | +192mm | Verify |
| UCA rear pivot height above LCA pivot | +170mm | Verify |
| UCA fore-aft span (front to rear, c-t-c) | 257.0mm | Confirmed (113.5 + 143.5) |

### Knuckle / spindle

<figure style="margin:1rem 0">
  <img src="/assets/projects/a40-austin/blog/reference/miata-spindle.jpg" alt="Miata NA front spindle and knuckle photo" style="width:100%;border-radius:4px;display:block;margin-bottom:6px" />
  <figcaption>Front spindle (knuckle) — donor photo. Upper and lower ball joint seats, hub flange, and steering arm. KPI angle and scrub radius are fixed by this casting and do not change with narrowing.</figcaption>
</figure>

> **Heights from photogrammetric scan, not yet verified against donor car.** LBJ and UBJ positions relative to the hub centre come from a CAD model built from a photogrammetric scan of a Miata NA knuckle. Heights above ground depend on ride height (hub centre estimated at 265 mm). Inner pivot heights are still estimated.

<figure class="wide" style="margin:1rem 0">
  <img src="/assets/projects/a40-austin/blog/plots/knuckle_3view.png" alt="Knuckle 3-view schematic — front, side, and plan views" style="width:100%" />
  <figcaption>Knuckle / spindle 3-view schematic. Front view (top-left): kingpin axis (pink), LBJ (gold) at −94mm below hub, UBJ (blue) at +139mm above hub, steering arm (green) at −76mm. KPI ≈12.1°. Side view (top-right): shows fore-aft positions — LBJ and UBJ share the same fore-aft offset (−8.8mm), caster = 0.0°. Steering arm extends +97mm forward from hub. Plan view (bottom): lateral KPI spread visible (UBJ 50mm more inboard than LBJ); steering arm forward reach. All values from photogrammetric scan CAD model, not yet verified against donor car.</figcaption>
</figure>

| Term | Full name | What it is |
|------|-----------|------------|
| BJ | Ball joint | Spherical pivot connecting a control arm to the knuckle. The lower BJ (LBJ) sits at the bottom of the knuckle; the upper BJ (UBJ) at the top. The line through them is the kingpin axis. |
| LCA | Lower control arm | The A-arm that runs from two inner frame bushings to the lower ball joint. On the Miata it also carries the coilover lower mount and the ARB end-link. |
| UCA | Upper control arm | The shorter wishbone that runs from two inner frame bushings to the upper ball joint. Shorter arm = more camber gain per mm of travel. |
| KPI | Kingpin inclination | The inward lean of the kingpin axis when viewed from the front. Causes the wheel to rise slightly as it steers, giving self-centering feel. |
| ARB | Anti-roll bar | Torsion bar connecting left and right suspension. Resists body roll without changing single-wheel compliance. |
| CL | Centerline | Vehicle longitudinal centerline — the midplane of the car. All lateral dimensions are measured from here. |
| Miata half-track | — | 1405 mm ÷ 2 = 702.5 mm from CL to hub center |
| A40 half-track | — | 1230 mm ÷ 2 = 615.0 mm from CL to hub center |

**Coordinate convention** (for all diagrams and tables below): lateral measured from car CL; fore-aft measured from the LCA front pivot (+forward, −rearward); height measured from the LCA inner pivot height.

### Pickup point geometry

**Pickup point positions relative to spindle center (from frontcontrolpickups.pdf):**

<figure class="wide" style="margin:1rem 0">
  <img src="/assets/projects/a40-austin/blog/reference/pickups-p0.png" alt="Miata front suspension pickup points technical drawing" style="width:100%;border-radius:4px;display:block;margin-bottom:6px" />
  <figcaption>frontcontrolpickups.pdf — front suspension pickup point reference. Educational reference only; verify all values against the donor car before fabrication.</figcaption>
</figure>

<figure class="wide" style="margin:1rem 0">
  <img src="/assets/projects/a40-austin/blog/plots/pickups_3view.png" alt="Pickup point 3-view schematic — front, plan, and side views stacked vertically" style="width:100%" />
  <figcaption>Inner pivot pickup positions — front view (top), plan view / top-down (middle), side view (bottom). Both sides of the car are shown in front and plan views. Gold squares = LCA inner pivots, blue triangles = UCA inner pivots. Lateral from car CL / fore-aft from LCA front pivot / height from LCA pivot. BJ and knuckle positions to be added once knuckle dimensions are confirmed.</figcaption>
</figure>

| Point | Lateral from car CL | Fore-aft from LCA-front pivot | Height from LCA pivot |
|-------|---------------------|-------------------------------|----------------------|
| LCA front pivot | 328mm | 0 (reference) | 0 (reference) |
| LCA rear pivot | 328mm | −323.5mm | 0 |
| UCA front pivot | 378mm | +138.5mm | +192mm |
| UCA rear pivot | 378mm | −118.5mm | +170mm |
| Lower ball joint (LBJ) | — | — | — |
| Upper ball joint (UBJ) | — | — | — |
| Hub / spindle CL | — | — | — |

> **Frame design takeaway.** LCA inner mounts: 328mm from Miata CL, shift 87.5mm inboard to 240.5mm from A40 CL. UCA inner mounts: 378mm from Miata CL, shift to 290.5mm from A40 CL. Fore-aft spacing and heights are unchanged by the narrowing. Verify all values against the actual donor subframe before cutting tube.

**From the A40 body:**
- Fender opening width at the tire centerline (re-measure with laser level or straight edge)
- Available clearance between fender lip and tire at ride height, full bump, and full lock
- Engine bay width at the front crossmember

