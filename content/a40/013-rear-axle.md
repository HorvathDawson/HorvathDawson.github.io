---
title: "Rear Axle & Driveshaft"
date:
status: in-progress
epic: research
tags: [axle, driveshaft, ford-8-inch]
---

## The Ford 8-inch

The rear axle is a narrowed Ford 8-inch, picked up with the second A40. The Ford 8" is a removable-carrier design: the entire center section (carrier, ring gear, pinion) drops out as one assembly, same concept as the Ford 9" but with a smaller 8-inch ring gear. Ratio changes and diff rebuilds are straightforward. Pull the third member, swap it, bolt it back in.

Why this axle:
- **Strength.** The Ford 8" handles 250-300hp without issue. The SR20DET at stock turbo power (200-220hp) is well inside the envelope, with room if the power goes up later.
- **Aftermarket.** Ring and pinion sets, limited-slip diffs, custom axle shafts in any length and spline count, all off the shelf from Moser, Strange, Currie, and others.
- **Axle retention.** The Ford 8" uses pressed-on bearings with a four-bolt retainer plate at each housing end. The axle cannot pull out without removing the retainer. This is not a C-clip design. C-clip axles (like the Ford 8.8") can lose a wheel if the clip fails. The retainer plate design is inherently safer.
- **Availability.** It was already narrowed and sitting in the second car.

The differential is offset (the ring gear sits to one side of the carrier, making one axle tube effectively shorter than the other). This affects four-link mockup sequence and bar lengths, covered in the four-link post.

---

## Narrowing the housing

The axle came already narrowed from the second car, cut down to fit within the A40 body. The process for narrowing a Ford 8" housing:

1. **Mark and cut the housing tubes.** The tubes are cut to the target width, removing equal amounts from each side to keep the differential centered (or intentionally offset if the diff is already offset and you want symmetric axle lengths).
2. **Housing ends.** Either re-use the original pressed-in housing ends (if the cut is outboard of them) or press in new ones. The housing ends carry the axle bearings and seals, so they have to be concentric with the tube and square to the axle centerline.
3. **Weld.** The housing tubes are welded back together. This weld carries all the lateral and braking loads from the rear axle, so full penetration and proper technique matter. Drill a small vent hole (3-4mm) in the housing tube away from the weld zone before welding; sealed tubes expand internally and can blow out the weld pool. The housing should be jigged straight during welding to prevent warping. After welding, inspect with dye penetrant to check for cracks or lack of fusion. This is a fatigue-critical joint.
4. **Custom axle shafts.** New shafts are ordered to the shorter length. The shaft manufacturer (Moser, Strange, etc.) needs the spline count, bearing journal diameter, flange bolt pattern, and the length from the differential centerline to the bearing seat.
5. **Post-weld verification.** Check housing straightness by clamping in V-blocks and running a dial indicator along each tube (total indicated runout under 0.5mm). Verify bearing seat concentricity at each housing end. A bent housing causes tire scrub, uneven bearing wear, and inconsistent rear tracking.

The target rear track is approximately 1250mm, set to fit the A40 body and stay close to the front track (1230mm). A slightly wider rear is typical and adds a bit of rear stability. The exact housing width depends on the wheel offset, tire width, and clearance to the four-link brackets and housing.

Stock Ford 8" axle shafts are 28 spline. A 31-spline upgrade is available and worth considering since the shafts are being custom-made anyway. The cost difference is small and the strength increase is meaningful if the power goes up later.

Ensure the axle housing vent (on top of the center section) remains clear and functional after narrowing. Route the vent tube upward and away from road splash. Without a working vent, internal pressure from warming gear oil pushes past the axle seals and onto the brake rotors.

---

## Bolt pattern conversion

The stock Ford bolt pattern is 4x4.25 inches (4x108mm). The Miata is 4x100mm. The axle flanges are being redrilled so all four corners of the car run one bolt pattern, one set of wheels, one set of lug nuts.

The PCD difference is 8mm (108 to 100), so each stud moves 4mm closer to center. On a four-bolt pattern, both patterns have studs at the same angular positions (0, 90, 180, 270 degrees), which means each new hole center is only 4mm from the corresponding old hole. Standard stud holes are 12-13mm diameter, so the holes overlap almost entirely if drilled at the same clocking.

Two approaches:
- **Rotate 45 degrees.** Clock the new 4x100 pattern 45 degrees from the original 4x108 pattern. This places each new stud midway between the old holes with ~40mm clearance, so nothing overlaps. Most 4x100 wheels are symmetric and accommodate either orientation.
- **Order new flanges (preferred).** Since custom axle shafts are being ordered from Moser or Strange anyway, specify flanges machined for 4x100 from the start. This avoids the redrilling entirely and guarantees concentricity. The flanges need to be indicated on a lathe or mill to ensure the new pattern is concentric with the axle centerline. Off-center drilling means the wheel is off-center, which causes a vibration that no amount of balancing can fix.

The center bore (pilot diameter) on the Ford flange also needs to match the rotor. If the Ford flange pilot is larger than the rotor center bore, the rotor needs boring. If smaller, a centering ring works but a machined register is more precise and doesn't add a loose part.

---

## Rear disc brakes

The stock Ford 8" came with drums. Those are being replaced with disc brakes to match the front. The goal: Miata disc brakes at all four corners.

### Caliper brackets

The Miata NA rear brake is a single-piston sliding caliper. On the stock Miata, it bolts to a bracket on the rear knuckle. On a Ford 8" solid axle there is no knuckle, so a custom caliper bracket is needed.

The bracket attaches to the axle housing end (using the bearing retainer bolt holes, or a dedicated bracket welded to the housing tube) and positions the Miata caliper over the rotor. The critical dimensions:

- **Caliper centerline** must align with the rotor mid-plane (radially and axially)
- **Mounting bolt spacing** from bracket to caliper must match the Miata caliper ears
- **Clearance** between the caliper body and the axle flange, and between the caliper and the four-link brackets

These are simple flat-plate brackets, but they resist the full braking torque reaction from the caliper. Use 10mm or thicker mild steel plate and gusset the bracket to resist flexing under hard braking. A thin bracket that flexes causes uneven pad wear and reduced stopping power. Bearing retainer bolt holes on one side, caliper mounting holes on the other, positioned by measurement. Mock up with the actual caliper and rotor before committing to a design. Off-the-shelf adapter kits exist for small import calipers on Ford housings, but most are for 5-lug setups. Custom brackets are the more reliable path for 4x100.

### Rotor fitment

The Miata NA rear rotor is a 231mm solid disc. It fits the 4x100 bolt pattern and the Miata caliper. Whether it sits correctly on the Ford axle flange depends on the center bore, the mounting surface, and the flange-to-caliper offset. If the rotor doesn't sit flush or centered, shim spacers between the rotor and flange can adjust it, but ideally the bracket is designed to the correct offset from the start.

The 231mm solid disc is thermally limited for sustained hard braking. For street use this is adequate. For any track use, consider a 251mm rotor or a vented rotor if one can be found or adapted for the 4x100 pattern. Monitor rear rotor temperature during initial spirited driving with a temp-indicating crayon (Tempilstik) at 400F and 600F marks.

### Brake bias

Miata rear brakes are sized for a ~1000kg car with roughly 50/50 weight distribution. The A40 will be approximately 950kg with a potentially different front/rear split. The hydraulic brake bias (front vs rear line pressure) needs to be adjustable. An adjustable proportioning valve on the rear brake line (Wilwood, Tilton, or similar) is the standard solution. Without it, the rear brakes may lock before the fronts under hard braking, causing instability. The proportioning valve gets dialed in during brake testing on the finished car.

Master cylinder bore, pedal ratio, and dual-circuit hydraulic split (front/rear or diagonal) are coupling dependencies that affect the entire brake system balance. These are addressed during the pedal box and master cylinder selection, which happens alongside the brake bracket fabrication.

---

## Parking brake

The parking brake needs to work independently of the hydraulic system. If the hydraulic brakes fail, the parking brake is the backup.

### Drum-in-hat (preferred)

The Miata NA rear uses a drum-in-hat parking brake: small expanding brake shoes inside the rotor hat, actuated by a cable. This is the cleanest solution if it physically fits. The drum shoes sit inside the rotor hat and the actuation is purely mechanical (cable from the cabin). The constraint is whether the Miata rotor hat section has enough internal clearance over the Ford axle flange and bearing retainer to leave room for the shoes and backing plate.

If it fits, the setup is: Miata rotor, Miata drum shoes and backing plate (mounted to the housing end behind the rotor), Miata caliper on the custom bracket, custom cable routing to the cabin.

### Fallback: mechanical caliper

If the drum-in-hat doesn't package, the next option is a caliper with an integrated mechanical actuator (a screw mechanism inside the piston, driven by a cable). Wilwood and others make these for hot rod applications. They work but don't hold as well as a dedicated drum and can glaze the pads if the parking brake is used frequently.

### Cable routing

The parking brake cables run from a hand lever inside the cabin, through the floor, back to the axle. On a custom frame the routing is all new. Use nylon-lined cable housings and keep the bends gentle to reduce friction. The cable equalizer (the Y-piece that splits one input cable into left and right) should be accessible underneath the car for adjustment. Equal cable tension on both sides matters, otherwise the car pulls to one side when the parking brake is applied.

---

## Pinion angle

Pinion angle is one of the most overlooked and most consequential setup details on a four-link car. Get it wrong and the car vibrates under power, eats U-joints, and develops a driveline whine at highway speed.

### How it works

The driveshaft connects the SR20DET's transmission output to the pinion input on the Ford 8". A U-joint at each end accommodates the angular misalignment between them. For smooth operation, three conditions must be met:

1. **Equal operating angles.** The front U-joint angle and the rear U-joint angle should be equal. When they are, the speed pulsations from each joint cancel out and the driveshaft turns at constant velocity. If they're unequal, the driveshaft speed fluctuates twice per revolution, producing a vibration that the driver feels through the floor and seats.

2. **Same plane.** Both the transmission output and pinion must tilt in the same vertical plane. If the pinion is yawed sideways relative to the transmission, the cancellation doesn't work even if the angles match.

3. **Not zero.** U-joints need a small minimum operating angle (1-2 degrees) to keep the needle bearings rotating inside the caps. At exactly zero degrees, the needles sit still under load and develop flat spots (brinelling). Target 2-3 degrees at each joint at ride height.

### A40 driveshaft geometry

The SR20DET sits at 3 degrees nose-down in the frame. The driveshaft drops 3.5 inches over 37 inches of horizontal run to reach the Ford 8" pinion. The pinion is angled to 3 degrees, parallel to the motor. That gives a driveshaft angle of 5.4 degrees from horizontal.

Each U-joint sees the difference between the shafts it connects:

- **Front U-joint:** 5.4° (driveshaft) minus 3.0° (trans output) = **2.4°**
- **Rear U-joint:** 5.4° (driveshaft) minus 3.0° (pinion input) = **2.4°**

Equal angles, same plane, not zero. All three conditions met.

<figure class="wide" style="margin:1rem 0">
  <img src="/assets/projects/a40-austin/blog/plots/driveshaft_angles.png" alt="Driveshaft angle layout side view showing transmission, driveshaft, and pinion angles with U-joint operating angles" style="width:100%" />
  <figcaption>Driveshaft angle layout at ride height. Trans output at 3° down, driveshaft at 5.4° down (3.5" drop over 37"), pinion at 3° down (parallel to motor). Both U-joints operate at 2.4°.</figcaption>
</figure>

### U-joint life expectancy

A U-joint is rated for a specific continuous operating load at 3000 RPM for 5000 hours with a 3 degree joint angle, assuming proper periodic maintenance. The relationship between angle and life is inversely proportional: double the angle, halve the life. Halve the load, double the life. Because a driveline seldom sees constant load, absolute life numbers are hard to pin down. But 5000 hours is roughly 8 hours a day, 5 days a week for 2.5 years of continuous driving, so even 20% of rated life is a reasonable service interval for a street car.

At 2.4 degrees per joint, the A40 build sits below the rated 3 degree angle. That puts U-joint life above the 5000 hour baseline, comfortably in the "set it and forget it" range for a car that sees weekend use.

<figure class="wide" style="margin:1rem 0">
  <img src="/assets/projects/a40-austin/blog/plots/ujoint_life.png" alt="U-joint life expectancy vs operating angle chart" style="width:100%" />
  <figcaption>U-joint life vs operating angle at constant load and 3000 RPM. Life is inversely proportional to angle. The A40 build at 2.4° per joint exceeds the 5000 hour baseline.</figcaption>
</figure>

### Setting pinion angle at ride height

With the four-link, the pinion angle is controlled by the upper bars. The lower bars set the axle's fore-aft position; the upper bars set its rotational position (nose up or nose down). Both sets of bars are threaded adjusters, so the angles are dialed in after the axle is in the car.

Procedure:
1. Set the frame at ride height on the jig, axle in position
2. Measure the transmission output flange angle with a digital inclinometer (degrees from horizontal)
3. Measure the pinion flange angle the same way
4. The driveline angle is the difference between the transmission output and the pinion input. Each U-joint's operating angle is the difference between the shafts it connects. Adjust until the front U-joint angle equals the rear U-joint angle, targeting 2-3 degrees each. The driveshaft should bisect the total angular change between the transmission output and the pinion.
5. Adjust the upper four-link bar lengths until the pinion angle gives equal angles front and rear, targeting 2-3 degrees each

The SR20DET sits at a slight nose-down angle following the engine's installed tilt. The pinion needs to point slightly upward to match. The exact values depend on the engine/trans mounting angle in the frame, which gets set during frame design.

### Pinion angle through suspension travel

This is where pinion angle stops being a static setup problem and becomes a geometry problem. As the rear axle moves through suspension travel on the four-link, the axle housing rotates. In bump (compression), the pinion nose rotates one direction. In droop (extension), it rotates the other. The amount of rotation per unit of travel depends on the four-link bar lengths, mounting heights, and angles.

At ride height, the pinion angle is dialed to the target. But at full bump or full droop, the angle may be significantly different. The U-joints have to tolerate the full range.

**Operating limits:**
- Most automotive U-joints tolerate up to about 15-18 degrees before binding
- Smooth operation (minimal vibration with proper cancellation) requires staying under about 3-4 degrees per joint for sustained highway driving. The mechanical binding limit is 15-18 degrees, but vibration becomes perceptible well before that because manufacturing tolerances prevent perfect cancellation
- In normal driving, the axle moves through roughly +/-30-50mm of travel (moderate bumps, acceleration squat, braking lift). The pinion angle change through that range should stay within 1-2 degrees of the ride-height target
- At full bump or full droop (60-80mm from ride height), the angle may be 3-5 degrees off target. This is acceptable because those extremes are brief (hitting a bump, hard cornering)
- The problem case is sustained operation at a bad angle: a heavy load in the trunk that compresses the rear springs and shifts the pinion angle 3-4 degrees from target, then highway driving at that angle for extended periods

The four-link geometry controls how fast the pinion angle changes through travel. Longer bars and a smaller angular spread between upper and lower mounting points both reduce the rotation per inch of axle travel. The Welder Series kit's recommended mounting positions (upper bars 2-1/8" above axle centerline, lowers 5" below and 27-1/8" ahead) are chosen to keep pinion rotation within a workable range for typical installations.

**Verification during mockup:** At ride height, full bump, and full droop, measure the pinion angle and the transmission output angle. Calculate the U-joint operating angles at all three positions. If any position exceeds 5-6 degrees at either joint, the bar geometry needs adjustment (change upper bar length, change mounting height) or the ride height target needs to be set so the full range is centered.

### Diagnosing driveline vibration

If the finished car vibrates at highway speed under light throttle, pinion angle is the first suspect. Driveline vibration from U-joint angle mismatch shows up as a buzz that scales with driveshaft RPM. It's often worse under light load because there's less torque to preload the U-joint and take up the needle bearing clearance. Under hard acceleration the vibration may disappear because the torque loads the joint in one direction, eliminating the cyclic speed variation.

This is distinct from wheel balance vibration (scales with road speed regardless of gear) and driveshaft balance vibration (constant at a given RPM regardless of load).

---

## Custom driveshaft

The driveshaft connects the SR20DET's transmission output to the Ford 8" pinion input. It's a one-off piece: the length is set by the custom frame, and the end fittings need to match the specific transmission and axle.

### What the driveshaft shop needs

A driveshaft shop (local or mail-order, places like Denny's Driveshafts or Tom Woods) needs:

1. **Length.** Measured center-to-center of the U-joints with the transmission and axle at ride height. Measure from the transmission seal surface (where the slip yoke enters the tailshaft) to the pinion flange face. The shop accounts for U-joint and yoke lengths; just give them the installed dimension.

2. **Front end fitting.** The SR20DET's 5-speed manual uses a slip yoke that slides into the transmission tailshaft housing. The yoke spline count and diameter must match the transmission output shaft. This is typically a standard Nissan part number that the driveshaft shop will cross-reference.

3. **Rear end fitting.** The Ford 8" pinion accepts a yoke. The yoke U-joint size depends on the specific pinion. Common Ford 8" U-joint sizes are 1310 and 1330 series.

4. **U-joint series.** Both ends should use the same series for consistent strength. 1310 is standard for cars under 300hp. 1330 gives more margin. The SR20DET at stock turbo power is well within 1310 territory, but 1330 is a reasonable choice if the power target may increase.

5. **Tube sizing.** The tube diameter and wall thickness determine the critical speed: the RPM at which the driveshaft's natural resonant frequency causes vibration. Longer shafts need larger diameter or thicker walls to keep the critical speed above max operating RPM. For a single-piece shaft under about 55-60 inches, a 3" x .065" DOM steel tube is typical. The shop calculates the critical speed based on the tube dimensions and length.

6. **Balance.** The shop balances the completed assembly on a balancing machine. This is non-negotiable. An unbalanced driveshaft causes vibration that scales with RPM, distinct from pinion angle vibration.

### Slip yoke and travel

The front of the driveshaft uses a slip yoke because the axle moves on the four-link, changing the distance between the transmission and the pinion. The splined slip yoke slides in and out of the transmission tailshaft as the driveshaft gets shorter (bump) and longer (droop).

**Travel check:** at full droop, the driveshaft is at its longest. At full bump, it's shortest. The slip yoke must have enough spline engagement at full droop (typically 1" minimum remaining in the tailshaft) and must not bottom out at full bump. Measure the driveshaft length at ride height, full bump, and full droop. The difference is the working stroke the slip yoke must accommodate. If the four-link geometry creates more length change than the yoke can handle, a longer tailshaft housing or different yoke may be needed.

### Ordering sequence

The driveshaft is one of the last things ordered. The length measurement requires the engine, transmission, and rear axle to be in their final positions in the frame. Engine mount position, transmission crossmember location, and axle position in the four-link all have to be locked down first. Only then can you measure the installed distance and order the shaft.

---

## Ring and pinion ratio

The final drive ratio hasn't been selected yet. It depends on the SR20DET's transmission gear ratios, the tire diameter, and the desired balance between cruising RPM and acceleration response.

The Ford 8" accepts a wide range of ratios. Common options:

| Ratio | Character |
|-------|-----------|
| 3.55 | Taller gearing, lower highway RPM, relies on being in the boost range for acceleration |
| 3.73 | Middle ground for a turbocharged street car |
| 4.10 | Shorter, more responsive off-boost, higher RPM at highway speed |

A shorter ratio (4.10) keeps the engine closer to the turbo's spool range and makes the car feel more responsive in daily driving. A taller ratio (3.55) is quieter cruising but can feel flat below boost threshold. The choice gets made once the engine tune targets and turbo sizing are clearer.

The removable carrier design means changing the ratio later is a weekend job. Pull the third member, swap in a different ratio carrier (or rebuild the existing one with a new gear set), bolt it back in. It's not a permanent decision. New ring and pinion sets require a break-in period (typically 500 miles of varied driving, no sustained heavy load) with a gear oil change afterward.

### Limited-slip differential

A limited-slip diff is planned. With the power going to a solid axle, an open diff would spin the inside wheel in every corner and on every damp surface.

Options for the Ford 8":

- **Gear-type (Truetrac/Torsen style).** Helical gears provide progressive locking with no clutches to wear. Quiet, smooth, works well on the street. Bias ratio is fixed by the gear design (typically 2.5:1 to 3.5:1). One limitation: if the inside rear wheel lifts off the ground (possible given the limited droop travel and high CG from the front suspension analysis), a gear-type diff sends zero torque to the grounded wheel, behaving like an open diff at the worst moment. If testing shows the inside rear lifting under hard cornering, a clutch-type with initial preload may be the better choice despite the maintenance requirement. For street driving where full wheel lift is unlikely, the gear-type is the preferred option.
- **Clutch-type (Auburn, Eaton posi, etc.).** Adjustable preload, higher locking force available, but clutch packs wear over time and need periodic service. Better suited for dedicated track or autocross use.
- **Full locking (Detroit Locker, mini-spool).** Always locked. Excellent for drag racing, harsh for street driving (tire chirp in turns, reluctance to turn). Not appropriate for this build.

The gear-type is the current plan. It goes in with the ring and pinion set when the ratio is selected.

---

## What's left

The axle housing is narrowed. Remaining work, roughly in order:

1. **Redrill flanges** to 4x100 (machine shop, can be done now)
2. **Axle shafts** ordered to final length once housing width is confirmed in the frame (28 or 31 spline, from Moser or Strange)
3. **Ring and pinion ratio and LSD** selected once engine tune targets are set
4. **Disc brake brackets** fabricated once caliper, rotor, and housing end dimensions are confirmed with parts in hand
5. **Parking brake** mechanism confirmed (drum-in-hat fit check with actual parts)
6. **Pinion angle** set during four-link mockup on the frame jig
7. **Rear coilover mounting** position on the axle housing determined during four-link design (sets rear motion ratio and roll stiffness)
8. **Driveshaft** measured and ordered once motor, trans, and axle are in final positions

Most of this is blocked on the frame design being further along. The redrilling can happen any time. Everything else happens in sequence on the jig once the frame is tacked and the motor/trans is mocked up.
