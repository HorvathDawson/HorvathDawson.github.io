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

## Hardware

The dash Pi was already speced for a **PiCAN FD Duo Isolated (non-SMPS)** HAT from the start — see the [digital dash post](./digital-dash) for the full stack. Two design choices on that HAT make the gateway possible:

| HAT feature | Why it matters |
|---|---|
| **Galvanic isolation per channel** | Haltech grounds and Prius column grounds sit at slightly different potentials once the car is running. A ground loop between two non-isolated CAN transceivers is exactly the kind of thing that fries a $40 HAT and leaves the car with no power steering on the highway. Isolation is the primary reason this HAT is in the build. |
| **Two independent channels** | `can0` at 1 Mbps for the Haltech broadcast, `can1` at 500 kbps for the Toyota column. Independent controllers, independent transceivers — the two buses do not see each other electrically. |

The non-SMPS variant intentionally trades the on-HAT 5 V converter for the isolation. The Pi instead drinks its 5 V directly from the Mini-Box DCDC-USB — same DCDC-USB the dash already uses for clean power + safe-shutdown signalling.

---

## How the frame spec was found: opendbc

Reverse-engineering a stranger's CAN bus from scratch is a project of its own. Toyota does not publish their DBC files, but the open-source self-driving community has — over years of cars-on-bench reverse engineering — done the work for them.

[opendbc](https://github.com/commaai/opendbc) is the comma.ai-maintained repository of community-reverse-engineered DBC files. **DBC** is the de-facto file format for describing a CAN database: which frame IDs exist on a given vehicle, what bytes inside each frame mean, the scale factor and offset for each signal, the broadcast rate, and — critically for Toyota — which byte holds the checksum and how it is computed.

The relevant files for this build live in [`opendbc/dbc/`](https://github.com/commaai/opendbc/tree/master/opendbc/dbc) under names like `toyota_prius_2010_pt_generated.dbc`. Cracking one open gives signal definitions like:

```text
BO_ 452 SPEED: 8 XXX                 ; frame ID 0xB4 = 452 decimal, 8 bytes
 SG_ ENCODER : 7|8@0+ (1,0) [0|255] "" XXX
 SG_ SPEED : 47|16@0+ (0.01,0) [0|250] "kph" XXX   ; bytes 5–6, scale 0.01
 SG_ CHECKSUM : 63|8@0+ (1,0) [0|255] "" XXX        ; byte 7 = rolling checksum
```

That one block tells the gateway exactly where to write the speed value, what scale to apply, and where the checksum goes. The Powertrain frame (`0x1C4`) is described the same way in the same file, and the checksum algorithm is documented in the comma.ai source under `opendbc/can/can_define.py` and the various Toyota safety files in [openpilot](https://github.com/commaai/openpilot).

### Finding signals for a different donor column

The workflow generalises. To evaluate any other OEM column-mount EPAS donor:

1. Look up the donor's powertrain DBC in `opendbc/dbc/` (e.g. `honda_civic_*`, `gm_global_a_powertrain.dbc`, `hyundai_*`).
2. Find the steering / EPS file for the same chassis (commonly `*_eps.dbc` or `*_steering.dbc`).
3. Identify which broadcast frames the EPS controller *listens for* (RPM + speed are the universal pair; some manufacturers also want a brake or ignition frame).
4. Read off the byte positions, scale factors, and checksum strategy. Anything not documented in opendbc is usually documented in [openpilot](https://github.com/commaai/openpilot) under the same OEM's safety folder.
5. Confirm the bus speed: most Toyota powertrain buses are 500 kbps, but some GM and FCA platforms run 125/250 kbps and that has to match `can1` config on the Pi.

### 2010 vs 2011 Prius interchangeability

The 2010 and 2011 Toyota Prius (Gen 3) share the same powertrain CAN architecture — same IDs, same bauds, same checksum scheme. Practically that means a **2011 column** can be driven by the **2010 Prius DBC** without modification, which broadens the junkyard hunt: any 2010–2015 Gen 3 Prius column is fair game, and the gateway code stays identical. Pivoting to a *different* generation (Gen 2 2004–2009, or Gen 4 2016+) or a *different OEM* would require re-walking the opendbc workflow above.

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
- **Donor column:** 2010–2015 Toyota Prius (Gen 3) — the entire Gen 3 run shares the same powertrain CAN architecture, so any year in that range is interchangeable for the gateway. Pivoting to a different generation or OEM would require re-walking the opendbc workflow.
- **Code:** not written.
- **Bench rig:** not built.
- **In-car install:** not done.

Next step is bench: FD Duo on the Pi, a benchtop CAN tool playing a recorded Haltech log on `can0`, the column hooked to `can1`, and a torque-sensor input on the column wiggled by hand to confirm assist actually scales with the spoofed speed.

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
