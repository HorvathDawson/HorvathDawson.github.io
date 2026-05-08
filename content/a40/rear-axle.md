---
title: "Rear Axle & Driveshaft"
date: 2026-03-26
status: in-progress
epic: fabrication
kind: log
tags: [axle, driveshaft, ford-9-inch]
---

## The Ford 9-inch

The rear axle is a stock-width 31-spline Ford 9-inch on hand. Removable third member (easy ratio swaps), pressed-on bearings with a four-bolt retainer at each end (no C-clip — the axle can't pull out if a clip fails), strong well past anything the SR20DET will throw at it, and a deep aftermarket for shafts and gears. Stock housing measures ~60.5" flange-to-flange (~1537 mm); needs ~136-140 mm of narrowing to land on the locked 1.340 m rear track.

The diff is offset (ring gear sits to one side), which affects four-link bar lengths — covered in the [four-link rear post](./four-link-rear).

---

## Narrowing plan

The plan is in three stages: order custom axle shafts cut to the final length, narrow the housing to match, then weld on all the bracketry (four-link, coilover, brakes).

### 1. Order axle shafts

Custom shafts from Moser (or Strange / Currie) spec'd to the 1.340 m rear track. Order spec:

- **31 spline** (matching the big-bearing housing)
- **4x100 bolt pattern** machined into the flange (no redrill — concentricity guaranteed)
- **Hub register** sized to the Miata rotor centre bore so the rotor pilots on the flange, not the studs
- **Length** from diff centreline to the bearing seat, mirrored on both sides — sets the final housing width

Going custom-flange instead of redrilling the stock 4x108 avoids the geometry problem that the two patterns nearly overlap (8 mm PCD difference, 12-13 mm stud holes — the new holes would land on top of the old ones).

### 2. Narrow the housing

DIY, after the shafts arrive so the housing width can be cut to match exactly:

1. **Cut the tubes.** Equal amounts off each side keeps the diff in its existing offset position relative to the chassis.
2. **Housing ends.** Re-use the original pressed-in ends if the cut is outboard of them, otherwise press in new ones. They carry the bearings and seals, so they have to be concentric with the tube and square to the axle centreline.
3. **Weld.** Drill a small vent hole in the tube before welding (sealed tubes blow out the weld pool when they expand). Jig the housing straight. Full-penetration weld — this joint carries all lateral and braking load.
4. **Verify.** Dye-pen the welds for cracks/lack of fusion. Clamp in V-blocks and dial-indicate each tube — under 0.5 mm TIR. Verify bearing seat concentricity at each end. A bent housing causes tire scrub, uneven bearing wear, and rear tracking that no alignment can fix.

Keep the existing housing vent clear and routed upward — without it, internal pressure pushes oil past the axle seals onto the brake rotors.

### 3. Weld on bracket mounts

With the housing at final width and verified straight, weld on:

- Four-link upper and lower axle brackets (positions from the [four-link rear post](./four-link-rear))
- Coilover lower mounts
- Caliper mounting tabs (see brakes section below)

All of these reference the axle centreline, so they get jigged off the tubes after the narrowing welds are signed off.

---

## Rear disc brakes (Miata)

Stock Ford 9" came with drums; replacing with Miata NA rear discs to match the front and stay on a single bolt pattern. Parts: Miata caliper (single-piston sliding) + Miata 231 mm solid rotor + custom caliper bracket welded to the axle housing.

The bracket is a flat-plate weldment (10 mm+ mild steel, gusseted) that puts the caliper at the right radius and axial position over the rotor. Critical dimensions: caliper centreline aligned with rotor mid-plane (radial and axial), bolt spacing matches the Miata caliper ears, clearance to the axle flange and four-link brackets. Mock up against the actual caliper and rotor before welding the tabs.

The 231 mm solid rotor is fine for street; sustained track use would want a vented or larger rotor on the same 4x100 pattern.

**Brake bias.** Miata rears are sized for a ~1000 kg, ~50/50 car. The A40 is ~950 kg with a different split, so an adjustable proportioning valve (currently leaning Tilton) goes in the rear circuit and gets dialled in during shakedown. System-level decisions already locked: manual brakes (no booster) and a diagonal (X-pattern) dual-circuit split. Master cylinder bore (~7/8" leaning) and pedal ratio are set during pedal-box selection.

**Parking brake.** Preference is Miata drum-in-hat: small expanding shoes inside the rotor hat, pure mechanical cable actuation. The check is whether the rotor hat clears the Ford housing end and bearing retainer with room for the shoes and backing plate. If it doesn't fit, fallback is a caliper with an integrated mechanical actuator (Wilwood-style). Cable routing is custom either way — gentle bends, equalizer accessible underneath for adjustment.

---

## Pinion angle and driveshaft

Both depend on the engine and trans being in their final positions in the frame, so this work happens late, on the jig.

**Pinion angle.** SR20DET sits 3° nose-down. Driveshaft drops 3.5" over a 37" run — 5.4° from horizontal. Pinion is set parallel to the motor (3° down), giving 2.4° at each U-joint. Equal angles + same plane + non-zero — meets all three U-joint operating-life conditions. The upper four-link bars are the adjusters; angle is set at ride height during four-link mockup.

<figure class="wide" style="margin:1rem 0">
  <img src="/assets/projects/a40-austin/blog/plots/driveshaft_angles.png" alt="Driveshaft angle layout side view showing transmission, driveshaft, and pinion angles with U-joint operating angles" style="width:100%" />
  <figcaption>Driveshaft angle layout at ride height. Trans output 3° down, driveshaft 5.4° down (3.5" drop over 37"), pinion 3° down (parallel to motor). Both U-joints operate at 2.4°.</figcaption>
</figure>

U-joint life is inversely proportional to operating angle (rated for 5000 hr at 3°, 3000 RPM, continuous load). At 2.4° per joint the build sits below the rated angle, comfortably in the "set it and forget it" range for a weekend-use car.

<figure class="wide" style="margin:1rem 0">
  <img src="/assets/projects/a40-austin/blog/plots/ujoint_life.png" alt="U-joint life expectancy vs operating angle chart" style="width:100%" />
  <figcaption>U-joint life vs operating angle at constant load and 3000 RPM. Inversely proportional. The A40 build at 2.4° per joint exceeds the 5000 hr baseline.</figcaption>
</figure>

**Pinion angle through travel.** Static pinion angle is only half the story. As the axle moves on the four-link, the housing rotates and the U-joint operating angles change. Targets:

- Normal driving range (±30-50 mm of travel): keep angle within 1-2° of the ride-height target.
- Full bump / full droop (60-80 mm): up to 3-5° off target is acceptable for brief excursions.
- Mechanical binding limit on automotive U-joints is 15-18°; perceptible vibration well before that.

Longer four-link bars and a smaller angular spread between upper and lower mounts both reduce pinion rotation per inch of axle travel. Verify during mockup: measure pinion + trans output angles at ride height, full bump, and full droop, and compute U-joint operating angles at all three. If anything exceeds 5-6°, adjust bar geometry or re-centre the ride-height target.

**Driveshaft.** One-off, single-piece, ordered from a driveshaft shop (Denny's, Tom Woods, etc.) once the engine, trans, and axle are in their final positions. They need installed length at ride height (centre-to-centre of the U-joints), the front yoke spec for the chosen trans (CD009 leaning, OEM SR20 5-speed fallback), and the Ford 9" rear yoke. 1330-series U-joints both ends is the typical street-build cross-spec at this power level. Tube sizing (typical 3" × .065" DOM for a single-piece shaft under ~55-60") is set by the shop's critical-speed calc; shop balances the assembly. Slip yoke must keep ≥1" spline engagement at full droop and not bottom out at full bump — verified during mockup.

---

## Ratio and LSD

Both deferred — final drive ratio depends on the trans choice and the engine tune target, and the carrier is a removable third member so this isn't a permanent decision. Plan is a **gear-type LSD** (Truetrac/Torsen): progressive locking, no clutches to wear, well-suited to the street use this car will see. Common 9" ratios in play: 3.55 (taller, quieter cruise), 3.73 (middle), 4.10 (shorter, keeps the turbo in spool range). Ratio gets selected with the LSD when the engine tune target is firmer.

---

## What's left

1. Order axle shafts from Moser to the 1.340 m rear-track spec.
2. Narrow the housing once the shafts are in hand.
3. Weld on four-link, coilover, and caliper brackets.
4. Fit-check Miata drum-in-hat parking brake against the narrowed housing.
5. Pick ratio + LSD with the engine tune target.
6. Set pinion angle on the jig during four-link mockup.
7. Measure and order the driveshaft once everything is in its final position.
