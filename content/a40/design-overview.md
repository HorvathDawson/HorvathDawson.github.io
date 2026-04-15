---
title: "Design Overview"
date: 2026-04-12
status: in-progress
epic: design
tags: [design, cad, clearance, planning]
---

This is the pre-build design phase. Everything gets modeled in CAD before any metal is cut. The goal is to find every clearance issue, packaging conflict, and structural concern in the model so the fabrication phase goes as smoothly as possible.

The narrowing analysis set the geometry targets. The research posts locked in the component choices. This phase takes all of that and fits it together in 3D, checking that everything actually works as a system.

---

## Systems to integrate

### Frame and suspension

The ladder frame is the backbone. It holds:

- **Miata double wishbone front suspension.** Pickup points positioned per the narrowing analysis (LCA inner pivots at 240.5mm from CL, UCA at 290.5mm). Shock towers integrated into the frame structure. The frame must provide the correct geometry at ride height and allow full bump/droop travel without interference.
- **Triangulated four-link rear.** Welder Series 318500 kit. Lower bar mounts 5" below axle CL and 27-1/8" forward. Upper bar mounts 2-1/8" above axle CL. Bar angles and lengths set the anti-squat percentage and pinion angle change through travel.
- **Narrowed Ford 8" rear axle.** Already cut down to fit the A40 body width. Redrilled to 4x100 to match the Miata hubs up front. Spring base ~950mm for coilover mounting.

### Engine and transmission

The SR20DET drops in with one of two transmission options:

- **OEM SR20 5-speed.** The stock pairing. Proven, cheap, readily available. The combined engine-to-shifter length is the issue: the SR20DET is already a long motor, and the 5-speed adds significant length behind the bellhousing. The shifter ends up well behind the firewall in a car this short.
- **CD009 (350Z 6-speed).** Stronger gearbox, better ratios for highway cruising, shorter than the OEM 5-speed. Requires an adapter plate (SR20 to CD009 bellhousing pattern). Still long, just less so.

Either way the motor sits at ~3 degrees nose-down, following the driveshaft angle established in the rear axle post.

### Body

The A40 body goes onto the frame. For now, reference images and design sketches stand in for a body scan. A proper 3D scan of the body shell is planned, which will allow precise clearance checking against the frame, engine, and suspension at all travel positions. Until the scan is in, clearance checking uses manual measurements and conservative estimates.

### Ancillaries

- **Radiator.** Custom aluminum, mounts in the stock location ahead of the engine. The A40's grille opening is small, so airflow is a concern. An electric fan behind the rad is required.
- **Intercooler.** Front-mount intercooler (FMIC) in front of or below the radiator, depending on what fits within the grille opening and bumper area. Charge pipe routing from the turbo outlet, through the intercooler, and back to the intake manifold needs to clear the frame rails and steering linkage on both sides.
- **Steering rack.** Narrowed Miata rack mounted to the frame. Rack mount height and fore-aft position drive Ackermann geometry and bump steer. Oil pan clearance below the rack is critical.
- **Driveshaft.** Single-piece, custom length. 3.5" drop over 37" horizontal run. Both U-joints at 2.4 degrees (detailed in the rear axle post).
- **Shock mounts.** Front: integrated into the frame as a shock tower. Rear: coilovers mount directly to the axle housing near the bearing caps and to the frame above.
- **Gas tank.** Target is the OEM location under the trunk floor. Fitment depends on the body scan, the four-link bar routing underneath, and the fuel line path to the engine bay.
- **Shifter.** Both transmission options put the shifter well behind the firewall. A remote shifter (cable-operated, low-profile) is required to get the shift lever into a usable position on the transmission tunnel. Lokar-style cable shifters are the most common solution for this. The CD009 is shorter, so its shifter position is slightly better, but still needs a remote setup.

---

## Known issues and clearance checks

These are the problems that need to be solved in CAD before fabrication. Each one gets its own section with images as the design progresses.

### Engine and transmission length

The SR20DET with either transmission is a long package for a car with a 2350mm wheelbase. The engine bay is not deep, and the transmission tunnel through the cabin is narrow. The firewall position, tunnel width, and floor height all need to accommodate the bellhousing and transmission case. This is the single biggest packaging constraint in the build.

With the OEM 5-speed, the shifter location falls roughly under the rear seat area. With the CD009, it's somewhat better but still behind the driver's hip point. The remote shifter cable routing needs a straight, low-friction path from the transmission to wherever the shift lever mounts on the tunnel.

### Oil pan vs steering rack

The SR20DET's oil pan hangs below the block. The steering rack mounts to the frame crossmember below and behind the engine. Depending on the exact engine position (height and fore-aft), the oil pan sump can interfere with the rack housing or the tie rod ends. This is checked by overlaying the engine model with the rack at its mounting height. A custom baffled oil pan or a modified sump shape may be needed.

### Brake, clutch, and throttle pedal placement

The A40 cabin is compact and the firewall is close to the front axle line. The stock pedal box doesn't exist anymore, so the pedals need a new mounting solution. Three options:

- **Engine bay side of firewall.** Conventional placement. The master cylinders and pedal assembly hang on the engine bay face of the firewall. The problem is that the SR20DET is long and sits close to the firewall, so there may not be room for a hanging pedal box between the engine and the firewall. The brake booster alone is a bulky item.
- **Underfloor.** Floor-mounted pedals with the master cylinders below the floor or tucked against the bottom of the firewall. This keeps the engine bay clear but requires cutting into the floor pan and building a sealed enclosure. The master cylinder pushrods end up at a steep angle unless the pedals are set well forward.
- **Dash-mounted / bulkhead-recessed.** Tuck the pedal assembly up high into the dash area, using a compact pedal box (Wilwood or similar aftermarket hanging pedal set). The master cylinders poke through the firewall into the engine bay at a higher position, above the steering rack. This avoids the floor cutting and keeps the pedals in a natural ergonomic position, but the bulkhead needs to be strong enough to take braking loads.

The clutch hydraulic line runs from whichever master cylinder location is chosen back to the slave cylinder on the transmission bellhousing. A long run with tight bends will feel spongy. The throttle is electronic (SR20DET DBW) so it only needs a wiring path, not a cable.

### Shock selection and compatibility

The Miata front suspension uses a specific shock length, stroke, and mounting style (lower fork mount on the LCA, upper stud into the shock tower). The four-link rear coilovers are a different size entirely: they mount between the axle housing and the frame, with shorter travel and different valving needs for a solid axle.

Finding a matched set that works for both ends is not straightforward. Off-the-shelf Miata coilovers have the right front geometry but the rear units are designed for the Miata's independent rear, not a four-link. Options:

- **Bilstein or similar monotube fronts, separate rear coilovers.** Run quality Bilstein Sport or equivalent inserts in custom front coilover sleeves sized to the Miata's shock length and stroke. Pick separate rear coilovers sized for the four-link travel. This means two different spring rates, two different shock valving specs, and no matched "kit" to fall back on. Tuning is harder but the parts fit their respective applications properly.
- **Full custom coilovers.** Have a shock builder (QA1, Viking, etc.) build matched front and rear units to the exact lengths, strokes, and valving needed. More expensive, but everything is purpose-built. The front units get the correct Miata mounting geometry and the rears get the correct four-link travel.
- **Miata coilover kit, swap rear shocks only.** Buy a Miata coilover kit for the fronts and source separate four-link-compatible rears. The fronts bolt in with the right geometry. The rears are standalone. Spring rate matching between front and rear is done manually.

The front shock tower geometry (built into the frame) locks in the shock length and upper mount style early. This decision needs to be made before the frame design is finalized.

### Exhaust routing

The turbo outlet and downpipe route down from the exhaust manifold on the passenger side, through or around the frame rail, and back under the floor. The frame crossmembers and the steering rack both sit in the path. The downpipe needs to clear the rack with enough margin for heat shielding. Header wrap or a heat shield on the rack side is likely required regardless of routing.

A 3" exhaust is the target for an SR20DET making any real power. A 3" OD tube is roughly 76mm, and once you add the flange thickness at joints and the clearance needed for hangers and heat shielding, the total envelope is closer to 90-100mm. That is a lot of space to route through a narrow ladder frame. The exhaust needs to pass between or alongside the frame rails without contacting them, and every crossmember in its path either needs a notch (weakening the crossmember) or the exhaust needs to route around it with bends that don't kill flow. Tight bends in 3" pipe also have a larger centerline radius than smaller pipe, so each bend eats more space. The alternative is dropping to 2.5" for packaging and accepting the flow compromise, but that limits the top-end power ceiling.

### Intercooler and charge piping

The FMIC sits in front of the radiator. Charge pipes run from the turbo compressor outlet (driver side), across the front of the engine bay to the intercooler, back across to the intake manifold (passenger side). The pipes need to clear the frame rails, radiator hoses, and any accessories on both sides. Silicone couplers at each joint add length and require clearance for the clamps.

### Radiator and airflow

The A40's grille opening is small compared to modern cars. The radiator core area is limited by the opening width and the space between the grille and the engine. An SR20DET under boost generates significant heat. The radiator needs to be as large as the opening allows, with a properly shrouded electric fan pulling air through the core. If the FMIC sits in front of the radiator, it blocks some airflow. The FMIC core thickness and fin density need to balance charge cooling against radiator heat rejection.

### Driveshaft and axle clearance

The driveshaft runs through the transmission tunnel. At full droop, the driveshaft angle increases and the shaft moves relative to the tunnel. At full bump, the slip yoke shortens and the angles change in the opposite direction. The tunnel needs to clear the shaft at all positions with margin for vibration. The rear axle housing width, including the disc brake calipers, needs to clear the inside of the body at full bump and full droop. The four-link bar paths must not interfere with the axle housing, brake lines, or parking brake cables.

### Steering linkage routing

The tie rods run from the rack ends outboard to the knuckle steering arms. With the narrowed rack, the tie rods angle outward more steeply than stock. At full lock, the tie rod path sweeps through an arc that must clear the frame rail, the lower control arm, and any bracketry in the area. The steering shaft from the column to the rack runs through the firewall and needs clearance from the exhaust manifold and any engine accessories on that side.

### Shock and spring clearance

Front coilovers sit between the upper and lower control arms, mounted to the LCA and the shock tower. The shock tower is a structural part of the frame. At full bump, the shock compresses to its minimum length and the spring/shock body must clear the frame rail, the upper arm, and the inner fender. At full lock combined with bump, the tire sweeps inboard and forward. Budget 12-18mm of lock loss from the narrowing, and check that the tire clears the shock body at the worst-case combined position.

### Body-to-frame clearance

The A40 body mounts to the frame at the original body mount locations (measured off the stock frame). At full suspension travel, combined with body roll, the body panels must clear the tires, suspension arms, and shock bodies. This is the check that needs the body scan the most. Until then, conservative clearance estimates based on the original body mount measurements and fender opening dimensions are used.

### Remote shifter packaging

Cable-operated remote shifters (Lokar, B&M, etc.) use two cables: one for fore-aft (gear selection), one for side-to-side (gate position). The cables need a smooth routing path with gentle bends from the transmission tailshaft area up to the shift lever mount. Sharp bends in the cable housing increase friction and make the shift feel heavy and imprecise. The shift lever mount position on the tunnel needs to be ergonomically reachable from the driver's seat, which in the A40's cabin means roughly centered on the tunnel between the front seats. The CD009's shorter length helps here since the cables originate closer to the cabin.

### Brake line routing

Four-wheel disc brakes with braided stainless lines at each corner. The hard lines run along the frame rails. The front lines need to route around or through the engine bay without contacting exhaust components. The rear lines run to a "T" fitting on the axle housing, with flex lines bridging from the frame to the axle (the axle moves on the four-link). The flex line length must accommodate full droop without tension and full bump without kinking.

### Wiring harness routing

The SR20DET runs a standalone ECU. The engine harness routes from the ECU (likely mounted inside the cabin or on the firewall) through a bulkhead connector to the engine bay. Keep the harness away from exhaust heat, moving suspension components, and steering linkage. The body harness (lights, gauges, switches) is separate and runs along the frame rails under the body. Grounding is critical: run a dedicated ground bus on the frame with individual grounds for each system returning to the same point.

---

*This post is updated as issues are identified and resolved in CAD. Each section will get annotated images showing the problem and the solution once the model reaches that point.*
