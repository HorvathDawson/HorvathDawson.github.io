---
title: "Wiring & ECU Overview"
date: 2026-05-11
status: planning
epic: fabrication
kind: log
tags: [electronics, wiring, ecu, haltech, harness]
---

The engine bay is going to live or die on the wiring. A clean harness is the difference between a car you can debug in a parking lot and a car that sits on jackstands for a season because nobody can find the short. This post is the starting point for the wiring thread — ECU choice, the decisions upstream of the harness, and the two big meta-questions (build from scratch vs. start from a universal, and how to loom it).

The CAN-side consumer (Pi dash) is already covered in the [digital dash post](./digital-dash). This post is everything *before* CAN — the engine harness itself.

## ECU: Haltech Nexus S2

Going with the **Haltech Nexus S2**. Short version of why:

- All-in-one ECU + PDM + CAN keypad-ready controller in a single sealed box. Fewer relays and fuses bolted to the firewall, fewer crimps that can fail.
- Native CAN broadcast that the Godot dash already speaks (see [digital dash](./digital-dash)) — no second translation layer.
- Drive-by-wire support out of the box. The SR20DET path I want to leave open is a DBW throttle body swap (Z33/350Z or similar), and the Nexus handles pedal + TB without an external module.
- Built-in wideband controller. One less standalone gauge controller, one less harness branch.
- High-current outputs on the PDM side mean injectors, coils, fuel pump, fans, and starter solenoid all land on the same connector family — no separate relay panel to fabricate.

The Elite 2500 was the obvious alternative but it punts power distribution to a separate fuse/relay block, which means a second mini-harness I have to design and loom. The Nexus collapses that.

## Decisions that drive the wiring

Before pin one of the harness gets crimped, these have to be locked. Each one changes the connector list, the wire count, or both.

### Injectors

- High-impedance, top-feed, EV14 / Bosch-style. Sized for the target boost level (~550 cc/min as a starting point for ~350 whp on E85-capable pump gas; will revisit when the fuel system is locked).
- Connector family: **EV1** or **EV14/USCAR**. EV14 is the modern default — locks the injector connector choice from Wiring Specialties.

### Ignition / coils

- Smart coils (built-in igniter), most likely **LS-style truck coils** on a remote bracket, or **R35 GT-R coils** if I want to stay closer to a Nissan-flavoured engine bay aesthetic.
- Smart coils mean the Nexus drives them with a low-current logic signal — no separate ignitor module, no high-current coil wiring running through the cabin side of the harness.
- Either way: 4 individual coil sub-harnesses, ~3 wires each (12V, ground, trigger).

### Throttle: DBW

- Yes. Going drive-by-wire. The Nexus supports it natively, and DBW unlocks cruise control, idle control without an IAC valve, and cleaner pedal mapping.
- Adds: TB connector (6-pin), pedal connector (6-pin), and a routing decision — pedal wiring runs from the firewall pass-through down to the pedal box, so the bulkhead connector needs to budget for those pins.

### Air metering: MAP, no MAF

- **Removing the MAF.** Speed-density only, off the Nexus's onboard MAP + IAT.
- Why: MAF restricts the intake tract, complicates the piping layout (has to be straight pipe for X diameters before the sensor), and a properly tuned speed-density map is more than enough resolution for this engine. The Nexus's onboard MAP handles up to 4 bar, which covers anything I'll realistically run.
- Wiring impact: deletes the MAF connector entirely. Adds an IAT sensor in the intake manifold / charge pipe (single 2-pin connector).

### Wideband O2

- Bosch **LSU 4.9** sensor, driven by the **Nexus's built-in wideband controller**.
- No standalone AEM / Innovate controller. One less box, one less power/ground/CAN tap.
- Connector: Bosch 6-pin to the sensor, plus an EGT thermocouple branch later if I add one downstream.

### Other branches that need to be on the diagram now

- Crank trigger (CAS or trigger wheel + sensor — needs deciding when the front cover is opened up)
- Cam trigger (single sensor on the exhaust cam for the SR20)
- Coolant temp (1-pin, sensor in thermostat housing)
- Oil pressure (3-pin sensor, ratiometric, for both ECU protection and dash display)
- Fuel pressure (3-pin, same family as oil)
- Knock sensor (1 or 2, depending on Nexus channel allocation)
- Fuel pump (Nexus PDM channel, possibly PWM-controlled for low-noise idle)
- Fans (two PDM channels, staged)
- Starter / ignition switch / cranking signal
- Reverse light + neutral safety switch (from the CD009 if I run one)
- Steering EPAS (covered separately, but the harness needs to budget for a CAN tap or a switched-12V feed depending on how that lands — see the [EPAS notes in the roadmap](./overview))

## Dash-driven sensor adds

The [digital dash](./digital-dash) post enumerates every signal the cluster needs to display. A factory SR20DET only provides about half of them over the Haltech CAN broadcast — the rest are sensors I have to *add* during the swap, and the harness needs to budget for them now (not after the dash lights up and something is missing).

What the ECU gives the dash for free over CAN — **no extra wiring**:

- RPM, throttle position
- Coolant temp (factory CTS)
- IAT (the new manifold IAT noted above, once it's in)
- Battery voltage (Nexus measures its own supply)
- Boost / MAP (Nexus's onboard 3.5 bar sensor — covers anything I'll run, no external MAP needed)
- Wideband AFR (Nexus's built-in WB controller, LSU 4.9 already in the branch list above)

What needs adding for the dash to be complete (each one is a harness branch):

| Dash signal | Sensor | Wiring impact |
|---|---|---|
| Oil pressure | 0–150 psi 3-wire transducer (AEM 30-2130-150 or Honeywell PX3) — **not** the OEM idiot-light switch | Already in the branch list above. 3-pin: 5V, signal, ground. Tee at the block oil-pressure boss. |
| Oil temp | 1/8 NPT thermistor (Haltech HT-010-300 or equivalent) | New 2-pin branch. Pan bung or sandwich plate at the filter. |
| Fuel level | A40 tank sender — keep the OEM resistive sender if it survives the tank rebuild, otherwise a custom resistive sender sized to the new in-tank pump hat | 2-pin (signal + ground) back to a Nexus analog input. Scale curve programmed in the ECU. |
| Vehicle speed | GPS first (Haltech RACEPAK GPS module on CAN) — driveshaft Hall-effect sensor as backup | GPS = pure CAN, no harness branch. Hall sensor = 3-pin branch (12V, signal, ground) routed to the gearbox tail. **Decision deferred** — start with GPS, add the Hall only if GPS dropouts become a problem. |
| Gear position | None — derived in software from `vehicle_speed / engine_rpm` against a per-gear ratio table | **No wiring.** |
| Fuel pressure (for dash + ECU protection) | Already in the branch list above (3-pin ratiometric sensor on the rail) | — |

Net new branches the dash adds beyond what engine management alone would need: **oil temp**, **fuel level**, and (eventually, maybe) **driveshaft VSS**. Everything else either piggybacks on a sensor that's already going in for the ECU's sake, or comes over CAN.

## The two big meta-decisions

### 1. Custom harness from scratch vs. Haltech universal

Two paths:

**A. Full custom.** Order Raychem DR-25 loom, TXL / TefzelTM wire, all the connectors individually from Wiring Specialties, and build the harness pin-by-pin against the Nexus pinout PDF. Maximum control over wire lengths, branch routing, and bulkhead connector layout. Maximum time investment.

**B. Start from the Haltech Nexus universal harness.** Haltech sells a pre-built universal harness for the Nexus with the ECU-side connector already terminated and labelled flying leads on the other end. I terminate the engine side with my own connectors and route/loom it myself. Faster, still clean, but I inherit Haltech's wire colour and length choices.

Leaning toward **B (universal harness)** for the ECU-side trunk, and **full custom for the engine-side sub-harnesses** (injectors, coils, sensors). That's the split most pro shops actually run — buy the hard part (the ECU connector with 70+ pins terminated correctly), build the easy/repetitive part yourself. Decision is not final yet; want to price out both first.

### 2. Connectors

Either path needs the **engine-side connectors** sourced individually. Plan is **Wiring Specialties** for:

- EV14 injector connectors (×4)
- Smart coil connectors (×4, type depends on the coil choice above)
- Bosch sensor connectors (CTS, IAT, oil pressure, fuel pressure)
- DBW TB + pedal connectors
- LSU 4.9 wideband connector
- Bulkhead connector (Deutsch Autosport or similar — TBD, this is its own sub-decision)

Wiring Specialties sells the OEM-spec connectors with the right terminals and seals already kitted, which beats hunting individual part numbers on TE Connectivity.

### 3. Looming

Goal: **race-car clean, not show-car polished**. Specifically:

- **DR-25 heat-shrink loom** on every trunk run. No split-loom, no fabric wrap, no zip-tie spaghetti.
- **Raychem SCL adhesive boots** at every branch and at every connector backshell.
- All branches at 90° to the trunk, kept short, supported back to the trunk with P-clips.
- Bulkhead connector mounted on the firewall, not on the inner fender. Single pass-through, sealed.
- Labels at every terminal end during build (Brady heat-shrink) — removed or covered before final loom.

This is the part where time and patience pay off more than money does.

## What comes next

Roughly in this order, each one its own post:

1. **Pinout & branch map** — full Nexus pinout reduced to a single one-page wiring diagram showing every branch and where it terminates.
2. **Universal vs. custom — final decision** — pricing both paths and committing.
3. **Connector order list** — final BOM going to Wiring Specialties.
4. **Engine-side sub-harnesses** — build log for the injector, coil, and sensor sub-harnesses.
5. **Trunk + bulkhead** — main loom and firewall pass-through.
6. **First power-up** — bench-power the ECU with nothing connected, verify PDM channels with a test load, then start adding sensors one at a time.

The dash side ([digital dash](./digital-dash)) can keep developing in parallel against synthetic CAN data — it doesn't have to wait on the harness.
