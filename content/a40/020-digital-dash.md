---
title: "Digital Dash"
date: 2026-04-16
status: in-progress
epic: fabrication
tags: [electronics, dash, raspberry-pi, haltech, can-bus]
---

The A40's original gauge cluster is a simple oval bezel with speedo and a handful of idiot lights. It's not going back in. A modified SR20DET needs real instrumentation, and the stock cluster doesn't have room for half of what matters. The plan is a custom React-based digital dashboard running on a Raspberry Pi, mounted behind the original bezel opening.

<figure>
  <img src="/assets/projects/a40-austin/blog/dash-reference.jpeg" alt="A40 Austin Devon dash bezel with dimension reference" />
  <figcaption>A40 dash bezel opening. The Waveshare 12.3" screen's active area (10.5" x 3.5" minimum) needs to fill this space cleanly behind the original trim ring.</figcaption>
</figure>

---

## What the dash needs to show

An SR20DET on a standalone ECU broadcasts everything over CAN bus. The dashboard reads that stream and displays what matters, organized by priority.

**Primary (always visible):** Tachometer and speedometer. Big, readable, OEM-style sweep needles.

**Vital (front and center):** Oil pressure, coolant temperature, and air/fuel ratio (wideband lambda). If oil pressure drops on an SR20, you need to see it before 
anything else. These get prominent numeric readouts or warning-state indicators that change color at threshold values.

**Secondary (smaller, but always present):** Manifold pressure (boost/vacuum gauge), oil temperature, intake air temperature, and battery voltage.

---

## Bill of materials

| Component | Part | Role |
|-----------|------|------|
| ECU | Haltech Nexus S2 | Engine management, DBW throttle, CAN bus broadcast |
| Computer | Raspberry Pi 5 (4GB) | Runs the dashboard UI |
| Storage | Pimoroni NVMe Base + 256GB M.2 SSD | Fast boot (~8 seconds cold start) |
| CAN interface | PiCAN3 HAT | Translates Haltech CAN to Linux SocketCAN |
| Power supply | Mini-Box DCDC-USB (100W) | Clean 5V/12V from car's dirty 12V, handles ignition-off shutdown |
| Display | Waveshare 12.3" 1920x720 DSI | Wide format, DSI ribbon (no HDMI cable). Active area must be at least 10.5" x 3.5" to fill the bezel |

---

## Assembly plan

### Step 1: Base plate and screen integration

Everything mounts to a single ABS or 3D-printed plate that bolts to the back of the Waveshare screen. The DSI ribbon cable runs directly from the screen into the Pi 5's MIPI port, eliminating a bulky HDMI cable.

### Step 2: Hardware stack

Two assemblies mount side by side on the backplate:

- **Computer stack:** Pimoroni NVMe Base (bottom), Raspberry Pi 5 (middle), PiCAN3 HAT (top), connected with brass standoffs.
- **Power supply:** Mini-Box DCDC-USB mounted adjacent to the Pi stack on the same plate.

### Step 3: Wiring

A single connector from the car carries raw 12V battery, 12V ignition, ground, CAN-H, and CAN-L to the back of the cluster. The DCDC-USB takes the car's power and routes clean 5V and 12V locally to the PiCAN3, Pi, and screen.

The DCDC-USB's shutdown pins wire directly to the Pi 5's J2 power header with a short jumper. When the ignition turns off, the Mini-Box triggers a safe OS shutdown and cuts power ~45 seconds later.

### Step 4: Software

- **OS:** Raspberry Pi OS Lite, booting straight into Chromium kiosk mode.
- **Backend:** A local Node.js process starts on boot. It reads the Haltech CAN bus via the PiCAN3 (SocketCAN), decodes the hex frames using Haltech's public protocol, and converts them into a JSON stream.
- **Frontend:** React app consuming the JSON stream over WebSockets. Gauge needles rendered as animated SVGs using framer-motion at 60 FPS. The UI is styled to look period-appropriate behind the A40's bezel.
