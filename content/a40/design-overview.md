---
title: "Design Overview"
date: 2026-04-12
status: in-progress
epic: design
kind: reference
tags: [design, cad, clearance, planning, integration]
---

The pre-build design phase. Everything gets modeled in CAD before any metal is cut, so every clearance issue, packaging conflict, and structural concern lives in the model — not in the welded-up frame.

This post is the integration view: a one-paragraph summary of each system and a link to the post that goes deep on it. The [build constants](./build-constants) page is the source of truth for any number that appears in more than one place.

---

## Systems index

| System | Summary | Detail |
|---|---|---|
| **Frame** | Custom ladder, two main rails + crossmembers, built around the suspension and drivetrain pickup points. Body mounts measured off the original A40 frame. | [frame design](./frame-design) · [finalization & cut list](./design-finalization) · [jig build](./frame-jig) |
| **Front suspension** | Narrowed Miata NA double wishbone. Inner pickups moved 95 mm inboard per side; donor LCA geometry retained, scanned UCA pickups used for the upper arm. | [options](./suspension-options) · [narrowing analysis](./narrowing-analysis) · [geometry reference](./geometry-design-reference) · [tuning](./suspension-tuning) |
| **Rear suspension** | Triangulated four-link, Welder Series 318500 (Horton Hot Rod) kit. Rear track locked at 1340 mm. | [four-link rear](./four-link-rear) |
| **Rear axle** | 31-spline Ford 9", stock-width housing on hand. Narrowing to 1340 mm; custom Moser axles with 4×100 flanges machined to spec (no redrill). | [rear axle & driveshaft](./rear-axle) |
| **Engine + trans** | SR20DET, leaning CD009 6-speed (350Z) on a Driftworks Superfly adapter; OEM SR20 5-speed fallback. Tunnel sized to CD009. Motor ~3° nose-down. | [motor selection](./motor-selection) |
| **Steering** | Narrowed Miata NA rack (190 mm total / 95 mm per side), Toyota Prius Gen 3 EPAS column over a Pi CAN gateway. | [steering](./steering) |
| **Body** | Original A40 shell. Mount style (welded / rubber / hybrid) TBD. Laser scan planned for clearance checks against frame, engine, suspension across full travel. | this post |
| **Dash + electronics** | Custom Godot/GDScript digital dash on a Raspberry Pi behind the original A40 bezel, fed by Haltech ECU over CAN. | [digital dash](./digital-dash) |

### Ancillaries

| Item | Plan |
|---|---|
| Radiator | Custom aluminum, stock location ahead of engine. Electric fan (small grille opening). |
| Intercooler | FMIC, in front of or below the radiator depending on grille fit. |
| Driveshaft | Single-piece custom length. 3.5" drop over 37" run; both U-joints at 2.4°. Detail in [rear axle](./rear-axle). |
| Shock mounts | Front shock towers integrated into the frame (not bolted plates). Rear coilovers between axle housing and frame. |
| Gas tank | Target OEM location under trunk floor; pending body scan and four-link routing. |
| Shifter | Remote linkage — trans length puts the native shifter location behind the driver's hip either way. Linkage style (solid rod vs short-throw kit) still TBD. |

---

## Known issues and clearance checks

Problems to solve in CAD before fabrication. Each gets annotated images as the design progresses.

| Issue | Constraint | Approach |
|---|---|---|
| **Engine + trans length** | SR20DET + either trans is long for a 2350 mm wheelbase. Single biggest packaging constraint. | Firewall, tunnel width, and floor designed around the bellhousing. CD009 puts the lever behind the driver's hip; OEM 5-speed worse — remote shifter linkage required either way. |
| **Oil pan vs steering rack** | Sump hangs below the block; rack mounts to the crossmember below/behind the engine. Risk of interference with rack housing or tie rod ends. | CAD overlay of engine + rack at mounting height. Custom baffled pan or modified sump may be needed. |
| **Pedal box placement** | Compact cabin, firewall close to front axle. Manual brakes (no booster) — locked decision. | Three options on the table: engine-bay side of firewall (tight against the SR20DET), underfloor (cuts the floor pan, sealed enclosure), or dash-mounted / bulkhead-recessed (Wilwood-style, masters poking through above the rack). Throttle is DBW — wiring path only. |
| **Shock selection** | No off-the-shelf "kit" covers both ends. Front locks the shock-tower geometry early. | Options: monotube fronts in custom sleeves + separate rears; full custom (QA1, Viking) both ends; or Miata coilover front kit + four-link-spec rears. Decision must land before frame design is final. |
| **Exhaust routing** | 3" target for SR20DET; ~90-100 mm envelope with hangers + heat shielding. Crossmembers in the path either get notched or routed around. | Header wrap or rack-side heat shield expected regardless. 2.5" is the packaging fallback at top-end power cost. |
| **Intercooler + charge piping** | Pipes run turbo (driver) → across front of bay → IC → back across to intake (passenger). Must clear frame rails, hoses, accessories. | Silicone couplers at each joint; clamp clearance budgeted in CAD. |
| **Radiator + airflow** | Small A40 grille opening, SR20DET under boost rejects significant heat, FMIC ahead of radiator blocks some flow. | Radiator as large as opening allows, properly shrouded electric fan. FMIC core thickness/fin density balanced against radiator rejection. |
| **Driveshaft + axle clearance** | Shaft moves through the trans tunnel (angle changes with travel; slip yoke shortens at bump). Rear axle + calipers must clear body interior. | Tunnel sized for full travel + vibration margin. Four-link bar paths cleared against housing, brake lines, parking brake cables. |
| **Steering linkage routing** | Narrowed rack ⇒ steeper outboard tie rod angle. At full lock, tie rod arc must clear frame rail / LCA / brackets. | Steering shaft column-to-rack routed to clear exhaust manifold and accessories on that side of the engine. |
| **Shock + spring clearance** | At full bump shock body must clear frame rail, upper arm, inner fender. Tire sweeps inboard + forward at bump-and-lock. | Budget 12-18 mm of lock loss from narrowing; check tire-to-shock at the worst-case combined position. |
| **Body-to-frame clearance** | Mount style still TBD. At full travel + body roll the panels must clear tires, arms, shock bodies. | Needs the [body laser scan](#body) most. Until then, conservative estimates from original body-mount measurements + fender opening dimensions. |
| **Remote shifter packaging** | Solid linkage from the native trans shifter location forward to the lever. Sharp bends or excess length add slop and load up the bushings. | Linkage routed with minimal joints from tailshaft to lever (centred on tunnel between seats). CD009's shorter length helps. |
| **Brake line routing** | 4-wheel disc, braided flex at each corner, hard lines along frame rails. Rear flex must accommodate full droop without tension and full bump without kinking. | Front lines routed around exhaust. Rear flex bridges frame to axle "T" with travel margin. |
| **Wiring harness routing** | Standalone Haltech ECU. Engine harness through a bulkhead connector; body harness separate along frame rails. | Harness kept away from exhaust heat, moving suspension, steering linkage. Dedicated frame ground bus, individual returns to a common point. |

---

### Downpipe routing reference

![SR20DET assembly with forward top-mount turbo and downpipe routing down the driver side between cylinders 3 and 4](/assets/projects/a40-austin/blog/reference/sr20-downpipe-routing.png)

Forward top-mount manifold with the turbo high and ahead of the head. The downpipe drops down the driver side between cylinders 3 and 4, runs under the pedal box, then along the driver-side frame rail to the rear exit. Crossmembers are unaffected — no relief notches required.

---

*Updated as issues are identified and resolved in CAD. Each row gets annotated images showing the problem and the solution as the model reaches that point.*
