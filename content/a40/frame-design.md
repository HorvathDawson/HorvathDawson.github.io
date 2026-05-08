---
title: "Ladder Frame Design"
date: 2026-02-20
status: in-progress
epic: design
kind: log
tags: [frame, cad, fabrication]
---

The frame is being designed from scratch in CAD. It's a ladder frame — two main rails with crossmembers — built around all the suspension and drivetrain mounting points instead of trying to splice modern subframes into the original A40 chassis. Why a custom frame at all is covered in [front suspension options](./suspension-options); this post is about how the frame itself is laid out.

> Numbers in this post pull from the [build constants](./build-constants) reference. Where those drift, the constants page is the source of truth.

## Inputs the frame has to satisfy

The frame is the integration point for everything else. Before any tube is drawn it has to commit to a coherent set of inputs:

- **Wheelbase 2350 mm** — locked, matches the stock A40 body so the wheel openings sit where the original sheet metal expects them.
- **Front track 1230 mm working / rear track 1340 mm locked** — sets where the front pickup brackets and rear axle perches sit relative to centreline. See [narrowing](./narrowing-analysis) for the front-track derivation.
- **Front pickup geometry** — LCA inner mounts 240.5 mm from CL, UCA inner mounts 290.5 mm from CL, with fore/aft span and heights preserved from the donor Miata. Full table in the [geometry design reference](./geometry-design-reference).
- **Rear four-link brackets** — Welder Series 318500 (Horton Hot Rod) kit. Lower bar mounts 5" below axle CL, 27‑1/8" forward; upper bar mounts 2‑1/8" above axle CL. Detail in the [four-link rear post](./four-link-rear).
- **Engine + trans envelope** — SR20DET with the trans tunnel sized to the larger CD009 case so either OEM 5‑speed or CD009 fits without rework.
- **Steering rack mount** — narrowed Miata rack, position drives Ackermann + bump steer (covered in [steering](./steering)). Vertical adjustment of at least ±15 mm built into the rack mount per the geometry reference.
- **Body mount locations** — measured off the original A40 frame so the shell can be set on the new chassis at the correct height and fore/aft position. Whether the body is welded, rubber-mounted, or hybrid is still TBD; the frame is being designed so either approach is possible.

## Layout

Two main rails run the full length, parallel and at constant height for the centre section to make the body land flat. The rails kick up over the rear axle to clear the housing at full bump. Crossmembers tie the rails at:

- Front, just behind the bumper, carrying the radiator core support and the front body mounts.
- Front suspension, integrated with the LCA and UCA pickup brackets and the lower shock-tower base.
- Firewall plane, structural box that ties into the shock towers and carries the upper steering column mount.
- Trans crossmember — removable, so the trans can come out without unbolting body or driveshaft.
- Mid floor, mostly for body support and torsional stiffness.
- Forward four-link upper bar mount, well-triangulated into the rails.
- Rear, behind the axle, carrying the rear body mounts and bumper.

Shock towers are part of the frame (not bolted plates). The front towers tie into both the upper LCA mount and the firewall crossmember so the LCA load path and the shock load path share the same structure rather than splitting through a bolted joint.

## Loads driving tube selection

Headline numbers from [geometry design reference](./geometry-design-reference): ~43% higher peak weight transfer than the donor Miata at 0.8 G, driven mostly by the higher CG (~575 mm vs ~460 mm). That hits the upper LCA mount, the shock tower top, and the four-link upper bar bracket hardest. Tube sizes for the rails and crossmembers are still being sized; the cut list lands in [design finalization](./design-finalization).

## What is still open

- **Body mounting decision** — welded vs rubber vs hybrid. Affects whether the frame needs sprung/damped body bushings or weldable tabs at each body-mount location.
- **Final shock tower position** — sets the front motion ratio (0.58–0.64 across the practical 65–85° shock band, see geometry reference). Locked once the shock supplier and stroke are committed.
- **Trans choice** — tunnel is sized to CD009; if SR20 5‑speed is chosen instead the tunnel is conservative.
- **Body scan** — until the A40 shell is laser-scanned, body-to-frame clearance checks rely on conservative manual measurements off the original frame.

CAD screenshots and final tube/wall callouts will land here as the design firms up. The companion [design overview](./design-overview) is the cross-system integration view; this post is about the frame structure itself.

