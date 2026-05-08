---
title: "Design Finalization & Materials"
date: 2026-03-05
status: planning
epic: design
kind: log
tags: [frame, planning, materials]
---

This post collects the final design pass: the cut list, material spec, tube sizes and wall thicknesses, and the order in which the frame goes onto the [jig](./frame-jig). It runs after [frame design](./frame-design) and the [design overview](./design-overview) integration checks, and lands the inputs needed before any metal is bought.

> Headline values referenced here live in [build constants](./build-constants). If something here disagrees, the constants page wins.

## What "done" means

The trigger to flip this post to complete is a cut list that's signed off and ready to order metal from. There is no separate BOM document — the cut list **is** the BOM. Each line item:

- Material grade (DOM mild steel for rails and crossmembers; 4130 only where it earns its keep, e.g. four-link bar tabs).
- Tube OD and wall thickness.
- Length (cut length, including weld allowance and miter allowance).
- Quantity.
- Cut/notch profile reference (CAD callout number).

## Inputs that must be locked first

The cut list cannot be ordered until each of these has a number, not a placeholder:

- **SA V2 outputs.** Front roll center, camber curve, motion ratio at the chosen shock-tower position, anti-dive/squat at the A40 wheelbase, ARB stiffness split. See [geometry design reference](./geometry-design-reference) for what's expected.
- **Donor Miata measurements.** Pickup coordinates and ball-joint heights confirmed against the actual donor, not just the photogrammetric scan. Anything tagged "verify" in the geometry table needs to flip to "confirmed".
- **Trans choice.** OEM SR20 5-speed vs CD009 6-speed. Tunnel is being sized to CD009 either way, but the trans crossmember position depends on the case length.
- **Tub/fender choice.** Stock A40 fender envelope vs subtle flares. Drives the upper limit on tire width and changes the body-to-frame clearance numbers.
- **Body mounting decision.** Welded, rubber-mounted, or hybrid. Affects which weldable tabs (or sprung bushings) get built into the rails at each body-mount location.

## Material strategy

- **Main rails:** rectangular DOM, large enough to take the bending and torsion loads from the higher-CG package without playing wall-thickness games. Final size waits on the SA V2 numbers and FEA on the upper LCA mount.
- **Crossmembers:** round or rectangular DOM depending on packaging. Round where bend access matters (around the trans tunnel, around the four-link upper bar mount).
- **Suspension brackets:** plate steel, gusseted into the rails. Frame brackets get turned-steel or DOM tube inserts at each pickup location for load distribution per the [geometry design reference](./geometry-design-reference) fabrication notes.
- **Shock towers:** plate, fully tied into the firewall crossmember and the upper LCA mount. No bolted joints in the primary load path.
- **Body mount tabs:** location set by stock body-mount measurements, type (weld-in stud, threaded boss, sprung bushing pocket) deferred until the body-mounting decision is made.

## Engine + trans mounting

The frame includes pads for the **stock SR20 engine mounts** so no custom-mount fabrication is in scope. Trans crossmember is removable, sized for the CD009 envelope. Motor sits at ~3° nose-down per the driveshaft angle established in the [rear axle post](./rear-axle).

## Sequence into fabrication

The cut list and the [frame jig](./frame-jig) together feed straight into the build:

1. Cut list signed off → metal ordered.
2. Tubes cut and notched per the CAD callouts.
3. Rails laid into the jig, tacked.
4. Suspension and four-link brackets bolted to actual control arms / axle on the jig, measured for left/right symmetry, then tacked.
5. Crossmembers fitted, tacked.
6. Full weld-out off the jig in a controlled sequence to manage distortion.

Photos, the actual cut list as it firms up, and any deviations between the CAD and the metal end up in this post.

