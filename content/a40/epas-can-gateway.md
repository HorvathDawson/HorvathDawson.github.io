---
title: "EPAS CAN Gateway"
date: 2026-05-18
status: in-progress
epic: design
kind: reference
tags: [electronics, can-bus, epas, steering, raspberry-pi, safety]
---

The [digital dash](./digital-dash) is an infotainment job — it reads the Haltech CAN broadcast and renders gauges. This post is a different problem entirely: a **drive-by-wire networking project** that takes the same Pi and turns it into a hardware-isolated CAN gateway between two completely different vehicle networks so a 2010 Toyota Prius EPAS column thinks it's still bolted into a Prius.

Same Pi 5, same enclosure behind the dash. **Different software stack, different HAT, different safety bar.**

---

## Why a gateway exists at all

The [steering post](./steering) locked in a junkyard column-mount EPAS. The default plan was "Prius column in failsafe mode" — power it up with 12 V + ignition and accept the fixed assist curve.

Failsafe works. But it gives you one assist level forever — parking-lot heavy on the highway, twitchy in a parking lot, no speed-sensitive falloff. The Prius column **can** do speed-sensitive assist, but only when it sees the two CAN messages it expects from a Prius powertrain.

So the brain already sitting behind the dash gets a second job: read what the Haltech is broadcasting and rebroadcast the same physical signals on the Toyota wire format the column expects.

---

## Architecture

Two physically separate CAN buses, one Pi sitting between them.

| Bus | Speed | Role | Frames the Pi cares about |
|---|---|---|---|
| `can0` | 1 Mbps | Haltech Nexus S2 broadcast | Dash reads everything; gateway reads RPM + speed |
| `can1` | 500 kbps | Toyota Prius column comms | Pi *writes* spoofed Powertrain + Speed frames |

The buses do **not** see each other electrically. Isolation matters here — Haltech grounds and the Prius column grounds will sit at slightly different potentials once the car is running, and a ground loop between two CAN transceivers is exactly the kind of thing that fries a $40 HAT and leaves the car with no power steering on the highway.

---

## Hardware change vs the current dash stack

The dash post Phase-2 stack uses a single-channel **PiCAN3** with an on-board SMPS that powers the Pi off the GPIO header. That works fine for a UI-only build. For the gateway:

| Component | Was (dash post) | Now (gateway stack) |
|---|---|---|
| CAN HAT | PiCAN3 (single channel, with SMPS) | **PiCAN FD Duo Isolated, non-SMPS** (Copperhill) |
| CAN channels | 1 × 1 Mbps | 2 × independent, galvanically isolated |
| Pi power | From HAT SMPS via GPIO | Direct from Mini-Box DCDC-USB to the Pi (HAT is non-SMPS) |
| Isolation | None | Per-channel galvanic isolation on the HAT |

The PiCAN FD Duo Isolated keeps the Mini-Box DCDC-USB as the clean 12 V source and the safe-shutdown signaller — the swap is only the CAN HAT itself + a small power-routing change (Pi now drinks its 5 V from the DCDC-USB directly instead of the HAT).

---

## What the column actually needs

Out of the entire Prius CAN traffic map, only two frames keep the column alive and out of limp mode:

| Toyota frame | Hz | Source on the Haltech side | Translation |
|---|---|---|---|
| **`0x1C4`** Powertrain (RPM) | 50 | Haltech `0x360`, bytes 0-1 | Raw RPM value, packed into Toyota frame, checksum byte 7 |
| **`0xB4`** Speed | 20 | Haltech `0x370`, bytes 0-1 (km/h × 10) | Convert km/h × 10 → mph, scale by 0.0062 (Toyota DBC), pack into bytes 5-6, checksum byte 7 |

No brake state, no gear, no ignition state, no body-control frames. The column is a relatively dumb actuator — once it sees RPM > 0 it wakes up, and the speed value just modulates the assist curve.

### Toyota rolling checksum

Every Toyota frame ends with an 8-bit checksum in byte 7 calculated across the CAN ID + length + payload:

```
checksum = ( (CAN_ID >> 8)
           + (CAN_ID & 0xFF)
           + DLC
           + byte0 + byte1 + byte2 + byte3 + byte4 + byte5 + byte6 ) & 0xFF
```

Same algorithm applies to both `0x1C4` and `0xB4`. Get this wrong and the column ignores the frame, falls back to its internal failsafe, and you're back to fixed assist.

---

## Software topology

The gateway does **not** live inside the Godot dash app.

The dash is a UI. UIs crash. The day the gauge font update or a config file typo locks up the renderer is **not** the day to also lose power steering at 70 mph.

So the gateway runs as its own thing:

- Lightweight C or Python service.
- Started as a `systemd` unit, `Restart=always`, `WatchdogSec=` configured.
- Subscribes to `can0` via SocketCAN, decodes the two Haltech frames it cares about.
- Recomputes Toyota frames + checksum, writes to `can1`.
- Logs to journald, no UI dependency.

The Godot dash continues to do its own thing on `can0`. If the dash app crashes, the EPAS gateway service keeps running. If the gateway service crashes, systemd restarts it within a second and the Prius column falls back to its own internal failsafe in the meantime — which is the same fixed-assist behaviour you'd have had without the gateway at all. Worst case = stock-Prius-column-in-failsafe. Acceptable.

---

## Current state

- **Architecture:** locked (dual bus, Pi gateway, isolated HAT).
- **Hardware spec:** locked (PiCAN FD Duo Isolated, Mini-Box DCDC-USB, Pi 5 + NVMe — already on hand).
- **Translation math:** locked (frame IDs, byte layout, scale factors, checksum algorithm — see tables above).
- **Donor column:** 2010 Toyota Prius (Gen 3 brushless). Pivoting to Kia Soul would invalidate the entire gateway — different IDs, different bauds, different checksum.
- **Code:** not written.
- **Bench rig:** not built.
- **In-car install:** not done.

Next step is bench: PiCAN FD Duo on the Pi, a benchtop CAN tool playing a recorded Haltech log on `can0`, the column hooked to `can1`, and a torque-sensor input on the column wiggled by hand to confirm assist actually scales with the spoofed speed.

---

## Why split this out of the dash post

The dash and the gateway share a Pi and a power supply. They share nothing else:

| | Dash | Gateway |
|---|---|---|
| Failure mode | Black screen | Lose power assist |
| Criticality | Annoying | Drive-by-wire |
| Stack | Godot, GDScript, sway, plymouth | C/Python, systemd, SocketCAN |
| Bus count | 1 | 2 |
| Isolation | Not required | Required |

Burying drive-by-wire networking inside a UI post would let one set of design concerns leak into the other. They get separate documents.
