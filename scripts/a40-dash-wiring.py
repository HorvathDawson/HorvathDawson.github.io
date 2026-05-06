"""
A40 Austin — digital dash wiring harness (WireViz).

Emits a YAML harness description and renders it via WireViz to SVG + PNG.
WireViz is purpose-built for wiring-harness diagrams: connectors with
labeled pins, cables with per-conductor colors and gauges.

Run:
  conda run -n a40-gauge python scripts/a40-dash-wiring.py
"""
from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "public" / "assets" / "projects" / "a40-austin" / "blog"
OUT_DIR.mkdir(parents=True, exist_ok=True)

YAML = r"""
metadata:
  title: A40 Austin — Digital Dash Wiring Harness
  description: |
    12 V switched power tree, CAN bus, and DSI display wiring.
    Headline path: DCDC-USB PSW → Pi 5 J2 for safe shutdown
    when ignition drops (HARDOFF 1 min after OFFDELAY 1 min).

options:
  bgcolor: WH
  color_mode: full
  fontname: Helvetica

connectors:
  PWR:
    type: Vehicle 12 V (fused)
    subtype: switched + ignition
    pinlabels: ['+12V', GND, IGN]
    bgcolor: '#ffe5e5'
    notes: Upstream battery / kill / fuse / ignition not shown
  DCDC:
    type: Mini-Box DCDC-USB
    subtype: 6–34 V in / 100 W
    notes: Automotive mode — OFFDELAY 1 min, HARDOFF 1 min
    pinlabels:
      - V(in)
      - GND
      - IGN
      - V(out) +12V
      - GND
      - PSW+
      - PSW−
    bgcolor: '#fff3d6'
  PICAN:
    type: PiCAN3 (Pi 5)
    subtype: 4-pos screw terminal + DB9
    pinlabels:
      - 1 CAN_H
      - 2 CAN_L
      - 3 GND
      - 4 +12V in
    notes: 120 Ω term at JP1 · 3 A SMPS powers Pi · IRQ on GPIO25
  ECU:
    type: Engine ECU / CAN node
    pinlabels: [CAN_H, CAN_L, GND]
  PI:
    type: Raspberry Pi 5
    subtype: 8 GB
    pinlabels:
      - GPIO 5V (pin 2/4)
      - GPIO GND (pin 6)
      - J2 GLOBAL_EN
      - J2 GND
      - DSI1
      - PCIe (M.2 HAT)
    notes: J2 momentary short → boot or clean shutdown
    bgcolor: '#e3f0ff'
  NVME:
    type: NVMe SSD
    subtype: M.2 2230/2242 via HAT
    pinlabels: [PCIe]
  DISP:
    type: Waveshare 12.3-DSI-TOUCH-A
    subtype: 1920×720 portrait, capacitive
    pinlabels: [DSI in, +5V, GND]

cables:
  W3:
    category: bundle
    gauge: 14 AWG
    length: 0.4
    colors: [RD, BK, WH]
  W4:
    category: bundle
    gauge: 14 AWG
    length: 0.25
    colors: [YE, BK]
  W_PSW:
    category: bundle
    gauge: 22 AWG
    length: 0.25
    colors: [BU, BK]
    notes: HEADLINE — soft shutdown trigger
  W_CAN:
    category: bundle
    gauge: 20 AWG
    length: 1.5
    colors: [GN, GN, BK]
    notes: Twisted pair, terminated 120 Ω each end
  W_PI5V:
    category: bundle
    gauge: 22 AWG
    length: 0.15
    colors: [RD, BK]
    notes: 5 V from PiCAN SMPS via GPIO header
  W_DSI:
    category: bundle
    length: 0.3
    colors: [VT]
    notes: 22-pin DSI FFC ribbon
  W_DISP_PWR:
    category: bundle
    gauge: 22 AWG
    length: 0.3
    colors: [RD, BK]
    notes: 5 V/GND tap from Pi GPIO header
  W_PCIE:
    category: bundle
    length: 0.1
    colors: [VT]
    notes: PCIe ribbon (M.2 HAT)

connections:
  - - PWR: [1, 2, 3]
    - W3: [1, 2, 3]
    - DCDC: [1, 2, 3]

  - - DCDC: [4, 5]
    - W4: [1, 2]
    - PICAN: [4, 3]

  - - DCDC: [6, 7]
    - W_PSW: [1, 2]
    - PI: [3, 4]

  - - PICAN: [1, 2, 3]
    - W_CAN: [1, 2, 3]
    - ECU: [1, 2, 3]

  - - PICAN: [4, 3]
    - W_PI5V: [1, 2]
    - PI: [1, 2]

  - - PI: [5]
    - W_DSI: [1]
    - DISP: [1]
  - - PI: [1, 2]
    - W_DISP_PWR: [1, 2]
    - DISP: [2, 3]

  - - PI: [6]
    - W_PCIE: [1]
    - NVME: [1]
"""


def main() -> None:
    if shutil.which("wireviz") is None:
        raise SystemExit("wireviz CLI not found in PATH (run inside the a40-gauge env).")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        yml = tmp_path / "dash-wiring.yml"
        yml.write_text(YAML.lstrip())
        subprocess.run(
            [
                "wireviz",
                "-f", "sp",  # SVG + PNG
                "-o", str(OUT_DIR),
                "-O", "dash-wiring",
                str(yml),
            ],
            check=True,
        )

    for ext in ("svg", "png"):
        f = OUT_DIR / f"dash-wiring.{ext}"
        print("wrote", f, f"({f.stat().st_size:,} B)")


if __name__ == "__main__":
    main()
