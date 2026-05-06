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

---

## What the dash needs to show

An SR20DET on a standalone ECU broadcasts everything over CAN bus. The dashboard reads that stream and displays what matters, organized by priority — survival data on the outsides where peripheral vision catches it, driving data dead center, admin data at the far right.

| Priority | Signal | Why it matters |
|----------|--------|----------------|
| 1 | Coolant temp | #1 cause of catastrophic SR20 failure in daily driving. |
| 2 | Oil pressure | Drop to zero at RPM and the engine is gone in seconds. |
| 3 | Wideband AFR | Lean under boost = melted ringlands. |
| 4 | Boost (MAP) | Primary feedback for the turbo system. |
| 5 | Tachometer | Shift point and redline. |
| 6 | Speed | Legal + situational awareness. |
| 7 | Oil temp | Hot oil thins out and kills bearings. |
| 8 | Fuel level | Boring, but you'll be stranded without it. |
| 9 | Battery voltage | Early warning for alternator issues. |
| 10 | Intake air temp | Knock risk on hot days. |

---

## Bill of materials

| Component | Part | Role |
|-----------|------|------|
| ECU | Haltech Nexus S2 | Engine management, DBW throttle, CAN bus broadcast |
| Computer | Raspberry Pi 5 (4GB) | Runs the dashboard UI |
| Cooling | Official Raspberry Pi Active Cooler | Required — Pi 5 throttles fast under sustained load, especially in a sealed dash enclosure on a hot engine bay-adjacent firewall |
| Storage | Freenove M.2 Adapter V2 + Crucial 256GB M.2 NVMe SSD | Fast boot (~8 seconds cold start) |
| CAN interface | PiCAN3 HAT (Copperhill Technologies) | Translates Haltech CAN to Linux SocketCAN |
| Power supply | Mini-Box DCDC-USB (100W) | Clean 5V/12V from car's dirty 12V; handles ignition-off shutdown |
| Display | [Waveshare 12.3" 1920×720 DSI](https://www.waveshare.com/wiki/12.3-DSI-TOUCH-A) | Portrait-native panel, DSI ribbon (no HDMI cable). Active area must be at least 10.5" × 3.5" to fill the A40 bezel |
| Bench-only PSU | Official Pi 5 27W USB-C | For desk testing before the car wiring |

---

## Section 1 — Hardware assembly

The build happens in two stages. **Phase 1** is a bench-test stack used to verify the OS, NVMe boot, and the screen. **Phase 2** swaps the bench PSU for the automotive power chain once the UI is ready.

<figure>
  <img src="/assets/projects/a40-austin/blog/dash-hardware-stack.jpg" alt="Full Pi 5 + NVMe + PiCAN3 stack on the bench" />
  <figcaption>Placeholder: full hardware stack laid out for bench testing.</figcaption>
</figure>

### Phase 1 — Bench setup (Pi + NVMe + screen)

1. **Mount the SSD.** Attach the Crucial NVMe SSD to the Freenove adapter board.
2. **Fit the Pi 5 active cooler.** Peel the thermal-pad backings, press the cooler onto the SoC + PMIC, and clip the spring pins through the Pi's mounting holes. Plug the fan lead into the 4-pin JST header next to the GPIO. Without this the Pi 5 throttles within minutes under sustained UI load — in a closed dash pod near the firewall it'll throttle even faster.
3. **Stack the Pi.** Use the supplied brass standoffs to mount the Raspberry Pi 5 (with cooler attached) directly on top of the Freenove adapter. Verify the cooler clears the M.2 ribbon and the standoffs.
4. **Connect the NVMe ribbon.** Connect the tiny PCIe FPC ribbon between the two boards.
5. **Connect the screen.**
   - Route the Waveshare DSI ribbon cable into the **DSI1** port (closest to the outer edge of the Pi).
   - Connect the 2-pin power jumper from the back of the Waveshare screen to the Pi's **5V** and **GND** GPIO pins.
6. **Power up.** Plug the official 27W USB-C PSU into the Pi.

> **Note — ribbon orientation.** The contacts on the PCIe FPC ribbon usually face **inward** toward the Pi's center, but check the Freenove V2 manual to confirm. Make sure it's seated perfectly flush before pushing the locking tab down.

<figure>
  <img src="/assets/projects/a40-austin/blog/dash-phase1-assembly.jpg" alt="Phase 1 bench assembly with NVMe base, Pi 5, and Waveshare DSI screen" />
  <figcaption>Placeholder: Phase 1 desk setup — NVMe base, Pi 5, and DSI display wired up.</figcaption>
</figure>

### Phase 2 — Automotive stack (CAN + DCDC-USB)

Once the desk tests are clean and the dash UI is loading correctly, the stack converts for the car:

1. **Add the CAN HAT.** Mount the PiCAN3 directly on top of the Pi 5, seating it on the GPIO header pins.
2. **Drop the USB-C.** No more wall plug — the PiCAN3's built-in SMPS now powers the Pi (and through it, the SSD) via the GPIO header.
3. **Wire the Mini-Box DCDC-USB** next to the Pi stack:
   - Run car 12V battery / ignition into the Mini-Box input.
   - Run the clean 12V output from the Mini-Box to the PiCAN3 screw terminals, and splice it to power the Waveshare screen's barrel jack.
   - Connect the Mini-Box shutdown pins to the Pi 5's **J2 power header** for a safe OS shutdown when the ignition is cut.

> **Note — shutdown timing.** When the ignition turns off, the Mini-Box triggers a clean OS shutdown and only cuts power ~45 seconds later, so the Pi never gets yanked mid-write.

<figure class="wide">
  <img src="/assets/projects/a40-austin/blog/dash-wiring.svg" alt="Digital dash wiring diagram: battery, kill switch, fused ignition feed, Mini-Box DCDC-USB, PiCAN3 HAT, Raspberry Pi 5, NVMe SSD, Waveshare DSI display, and Haltech Nexus S2 ECU, with the PSW shutdown signal routed to the Pi 5 J2 header" />
  <figcaption>Phase 2 wiring overview. Switched +12 V feeds the Mini-Box DCDC-USB (red trunk) plus its ignition-sense pin (orange dashed). Clean V(out) +12 V drops into the PiCAN3 screw terminal pin 4, which runs the on-HAT 3 A SMPS that powers the Pi 5 (and the Waveshare screen via the GPIO 5 V rail). The blue PSW \u2192 Pi 5 J2 trace is the safe-shutdown pulse: on key-off the DCDC-USB pulses the Pi's power-button header to start a clean OS shutdown before HARDOFF cuts power. CAN_H/L (green) come straight from the Haltech Nexus S2 to the PiCAN3 with the on-board 120 \u03a9 terminator. Diagram source: <code>scripts/a40-dash-wiring.py</code>.</figcaption>
</figure>

<figure>
  <img src="/assets/projects/a40-austin/blog/dash-phase2-assembly.jpg" alt="Phase 2 automotive stack with PiCAN3 HAT and DCDC-USB power manager" />
  <figcaption>Placeholder: Phase 2 automotive stack — PiCAN3 on top, Mini-Box DCDC-USB feeding the rail.</figcaption>
</figure>

---

## Section 2 — Flash the OS (Mac)

Prepare the OS on a temporary MicroSD card before booting the Pi.

1. Insert a MicroSD card into the Mac and open **Raspberry Pi Imager**.
2. Select **Raspberry Pi OS Lite (64-bit)**.
3. Click **Edit Settings** (OS customization) and set:
   - **Hostname:** `dash`
   - **Username / password:** e.g. `sr20` / `password`
   - **Configure wireless LAN:** exact SSID (case-sensitive) and password.
   - **Enable SSH:** password authentication.
4. Flash, drop the card into the Pi, power on, and wait ~90 seconds for it to join Wi-Fi.

> **Note — Wi-Fi country code.** The Imager's Wireless LAN section requires the correct country code, otherwise the Wi-Fi chip stays disabled and the Pi never appears on the network.

<figure>
  <img src="/assets/projects/a40-austin/blog/dash-rpi-imager.png" alt="Raspberry Pi Imager OS customization screen" />
  <figcaption>Placeholder: Raspberry Pi Imager OS customization (hostname, user, Wi-Fi, SSH).</figcaption>
</figure>

---

## Section 3 — Provisioning script (Mac → Pi)

Rather than typing setup commands by hand, this Bash script runs from the Mac. It SSHes in, injects the screen / NVMe / PiCAN3 device-tree overlays into `/boot/firmware/config.txt`, installs `can-utils`, brings up the `can0` interface, and enables a virtual `vcan0` interface for mock testing.

1. On the Mac, create the file: `nano setup_dash.sh`
2. Paste the script:

   ```bash
   #!/bin/bash
   PI_USER="sr20"
   PI_HOST="dash.local"

   cat << 'EOF' > payload.sh
   #!/bin/bash
   sudo apt-get update

   # Driver overlays: Waveshare DSI panel, NVMe boot, PiCAN3
   sudo cp /boot/firmware/config.txt /boot/firmware/config.txt.bak
   for line in \
     'dtoverlay=vc4-kms-dsi-waveshare-panel-v2,12_3_inch_a_4lane' \
     'dtparam=pciex1' \
     'dtparam=nvme' \
     'dtparam=spi=on' \
     'dtoverlay=mcp2515-can0,oscillator=16000000,interrupt=25'
   do
     sudo grep -qxF "$line" /boot/firmware/config.txt || \
       echo "$line" | sudo tee -a /boot/firmware/config.txt
   done

   sudo apt-get -y install can-utils

   sudo bash -c 'cat > /etc/network/interfaces.d/can0 << "NETEOF"
   auto can0
   iface can0 can static
       bitrate 1000000
   NETEOF'

   sudo grep -qxF 'vcan' /etc/modules || echo 'vcan' | sudo tee -a /etc/modules
   sudo reboot
   EOF

   scp payload.sh $PI_USER@$PI_HOST:/home/$PI_USER/payload.sh
   ssh -t $PI_USER@$PI_HOST "chmod +x payload.sh && ./payload.sh"
   rm payload.sh
   ```

3. Make it executable and run it:

   ```bash
   chmod +x setup_dash.sh
   ./setup_dash.sh
   ```

The Pi reboots on its own when the script finishes.

---

## Section 4 — Move the OS onto the NVMe

Once the Pi is back up, clone the SD card to the SSD and switch boot order so subsequent boots come straight off NVMe.

1. SSH in: `ssh sr20@dash.local`
2. Verify the NVMe is on the bus: `lspci` (look for "Non-Volatile memory controller").
3. Clone:

   ```bash
   sudo dd if=/dev/mmcblk0 of=/dev/nvme0n1 bs=4M status=progress
   ```

4. Set the boot order: `sudo raspi-config` → **Advanced Options → Boot Order → NVMe/USB Boot**.
5. `sudo shutdown -h now`, **physically remove the SD card**, then power back on. The Pi now boots natively from the SSD.

---

## Section 5 — Verify the screen (framebuffer test)

Pi OS Lite has no desktop, so the panel will look black except for a tiny blinking cursor. To prove the hardware, drivers, and DSI ribbon are all working, write raw pixels straight to the framebuffer.

```bash
ssh sr20@dash.local
cat /dev/urandom > /dev/fb0   # screen fills with TV-style colored snow
cat /dev/zero    > /dev/fb0   # wipes back to black
```

> **Note — "No space left on device".** Both commands print `cat: write error: No space left on device` and **that is the success signal**. The stream filled every pixel of the framebuffer, hit the physical edge of display memory, and the kernel correctly stopped it.

If the snow appears and then clears cleanly to black, the hardware foundation is bulletproof.

<figure>
  <img src="/assets/projects/a40-austin/blog/dash-snow-test.jpg" alt="Waveshare 12.3 inch DSI display showing colored static from /dev/urandom" />
  <figcaption>Placeholder: the "snow" test — `/dev/urandom` piped straight into the framebuffer.</figcaption>
</figure>

---

## Section 6 — UI framework: Qt vs. Godot

To land the high-end OEM look (think modern Porsche / Audi virtual cluster) — anti-aliased needles, smooth sweeps, subtle glow on warnings — there are two realistic options for a single developer:

- **Qt / QML.** The literal industry standard for OEM clusters. Locks to 60 FPS on bare metal. The catch is a brutal learning curve: custom shaders, glow effects, and complex animations in QML/C++ are hard if you aren't a full-time embedded GUI engineer.
- **Godot Engine.** A lightweight game engine that takes the visual-design problem and makes it trivial. Glowing needle? Drop a Bloom node. Smooth sweep? Use an `AnimationPlayer`. Gauge faces drag in visually, redline warnings can be particle effects, scripting is GDScript (effectively Python). The Pi 5 has plenty of GPU headroom to run a 2D Godot dash at 60 FPS.

**Verdict for this build: Godot.** Shortest path from "Pi with a black screen" to "glowing OEM-style cluster I'm proud of," without spending months learning QML shader pipelines.

<figure>
  <img src="/assets/projects/a40-austin/blog/dash-godot-mockup.png" alt="Mockup of the Godot-based digital cluster UI" />
  <figcaption>Placeholder: Godot UI mockup — gauge faces, glow, and animation done in the editor.</figcaption>
</figure>

---

## Section 7 — A40 gauge layout

The original A40 bezel has **5 mechanical openings**: one large round hole in the center, flanked by two smaller (equal-sized) holes on each side. A turbo SR20 broadcasts more critical signals than five, so the small slots become **composite gauges** — a primary analog with a secondary digital readout layered inside — instead of one signal per hole.

| Slot | Bezel hole | Primary analog | Inner digital |
|------|-----------|----------------|---------------|
| 1 | Far left (small) | Coolant temp | — |
| 2 | Left inner (small) | Oil pressure | Oil temperature |
| 3 | Center (large) | Tachometer | Speed + gear indicator |
| 4 | Right inner (small) | Boost (MAP) | Wideband AFR |
| 5 | Far right (small) | Fuel level | Battery voltage + IAT |

**Warning overlays** (turn signals, high beam, check engine light, low-oil-pressure flash, overheat flash) sit as icons layered above the gauges and don't consume a slot.

The four outer gauges share identical visual sizing so the cluster stays symmetric behind the original A40 trim ring; only the center gauge scales up to match the bigger bezel hole.

<figure>
  <img src="/assets/projects/a40-austin/blog/dash-gauge-layout.png" alt="Five-slot turbo SR20 gauge layout mapped onto the A40 bezel" />
  <figcaption>Placeholder: 5-slot composite gauge layout mapped onto the A40 bezel openings.</figcaption>
</figure>

---

## Section 8 — Generate gauge assets (Mac)

Rather than drawing dial faces by hand, [scripts/a40-gauge-placeholders.py](scripts/a40-gauge-placeholders.py) generates mathematically perfect dial backgrounds and needles, plus a printed log of pivot coordinates for each one.

```bash
source $HOME/miniconda3/etc/profile.d/conda.sh
conda activate a40-gauge
cd scripts
python a40-gauge-placeholders.py
# → public/assets/projects/a40-austin/blog/gauges/   (backgrounds, needle sprites, pivot log)
```

The pivot numbers from the log feed straight into Godot in the next section — no manual measuring, no Photoshop ruler.

<figure>
  <img src="/assets/projects/a40-austin/blog/dash-asset-generation.png" alt="Generated gauge backgrounds and needle sprites from the Python placeholder script" />
  <figcaption>Placeholder: generated dial backgrounds + needle sprites with computed pivot coordinates.</figcaption>
</figure>

---

## Section 9 — Build the UI in Godot (Mac)

### Project setup

1. Create a new Godot project.
2. **Project → Project Settings → Display → Window:**
   - **Width:** `1920`, **Height:** `720`
   - **Mode:** `Windowed`
   - **V-Sync Mode:** `Enabled`
   - **Stretch → Mode:** `canvas_items`, **Aspect:** `keep`
3. Drag the generated `.png` assets from the Mac into Godot's lower-left **FileSystem** dock.

> **Note — why Windowed, not Exclusive Fullscreen.** Exclusive Fullscreen conflicts with the Pi's Wayland graphics driver and produces a black screen on launch. Windowed mode lets Sway (the compositor) handle stretching, and removing window decorations at the OS level (Section 10) gives the same edge-to-edge result.

### Build a single gauge scene (e.g. center tach)

1. **Scene → New Scene → 2D Scene.** Rename the root node `CenterTach`.
2. Drag in the background image (`center_tach.png`); rename it `Background`.
3. Drag in the needle image; rename it `Needle`. It must be a child of the root, not a child of `Background`.
4. **Alignment cheat:** click each of `Background` and `Needle`, expand **Offset** in the Inspector, and **uncheck Centered**. This skips a lot of fiddly pivot math.
5. **Apply the Python pivot data:**
   - Needle hinge: take the pivot coordinates from the script's log, **negate them**, and put them in the needle's **Offset X / Y** (e.g. pivot `(90, 858)` → Offset X `-90`, Y `-858`).
   - Needle dial position: enter the script's reported coordinates directly into the needle's **Transform → Position X / Y**.
6. Set the root `CenterTach` node's **Transform → Scale** to `(0.5, 0.5)` to fit the bar display.
7. Right-click `Needle`, attach a GDScript, and use a `sin()`-driven rotation as a stand-in until real CAN data is wired in.
8. Save as `center_tach.tscn`.

Repeat for each of the five composite gauges (coolant, oil pair, tach/speed/gear, boost+AFR, fuel/admin).

### Assemble the main dashboard

1. **Scene → New Scene → 2D Scene.** Name it `MainDash`.
2. Drag each saved gauge `.tscn` into the `MainDash` viewport and align it with its physical bezel opening.
3. **Project → Project Settings → Application → Run** → set **Main Scene** to `main_dash.tscn`.

### Export for the Pi

1. **Project → Export.** Add a **Linux/X11** preset.
2. Set **Architecture** to `arm64`.
3. **Uncheck "Export With Debug"** in the save dialog. (This is what removes the `(DEBUG)` text that otherwise appears in the title bar at runtime, and it strips out debug overhead for performance.)
4. Click **Export Project** and save to `~/Desktop/dash_app.arm64`.

<figure>
  <img src="/assets/projects/a40-austin/blog/dash-godot-scene.png" alt="Godot 2D scene with composite gauge faces laid out for the A40 cluster" />
  <figcaption>Placeholder: Godot 2D scene with the five composite gauges arranged for the A40 bezel.</figcaption>
</figure>

---

## Section 10 — Sway compositor + autoboot service

The Pi runs **Sway** (a Wayland compositor) with no desktop environment. Sway gives Godot direct hardware-accelerated framebuffer access and, with the right config, strips every scrap of window chrome so the dash looks like dedicated hardware.

### 1. Transfer the exported app

```bash
scp ~/Desktop/dash_app.* sr20@dash.local:~
```

### 2. Install Sway and grant hardware permissions

```bash
ssh sr20@dash.local
sudo apt-get update
sudo apt-get install sway -y
sudo usermod -aG video,render,input,tty sr20
```

### 3. Configure Sway (rotation, cursor, borderless, autostart)

```bash
mkdir -p ~/.config/sway
nano ~/.config/sway/config
```

Paste:

```text
# Force the Waveshare panel to landscape
output * transform 270

# Hide the mouse cursor
seat * hide_cursor 1

# Strip every window border and title bar so the dash is edge-to-edge
default_border none
default_floating_border none
smart_borders on

# Launch the Godot dash natively under Wayland
exec /home/sr20/dash_app.arm64 --display-driver wayland
```

> **Note — borderless production look.** Godot is running in Windowed mode (Section 9), so by default Sway would draw a title bar around it. The three `*_border` lines remove all decorations, producing a 100% edge-to-edge fullscreen result without the driver issues of Exclusive Fullscreen.

### 4. Create the systemd unit (the software ignition switch)

```bash
sudo nano /etc/systemd/system/dash.service
```

```ini
[Unit]
Description=SR20 Digital Dash
After=systemd-user-sessions.service systemd-logind.service
Conflicts=getty@tty1.service

[Service]
User=sr20
PAMName=login
TTYPath=/dev/tty1
StandardInput=tty
Environment="WLR_LIBINPUT_NO_DEVICES=1"
ExecStartPre=-/usr/bin/plymouth quit
ExecStart=/usr/bin/sway
Restart=always
RestartSec=1

[Install]
WantedBy=multi-user.target
```

> **Note — why `ExecStartPre=-/usr/bin/plymouth quit`.** Plymouth (Section 11) holds the GPU after rendering the boot splash, which would block Sway from taking over the screen. This line forces Plymouth to release the framebuffer the instant Sway is about to start. The `-` prefix makes systemd ignore non-zero exit codes, so a missing/already-quit Plymouth doesn't fail the service.

### 5. Enable and start

```bash
sudo systemctl daemon-reload
sudo systemctl enable dash.service
sudo systemctl start dash.service
```

Every power cycle now boots the Pi straight into a borderless, cursor-free, hardware-accelerated digital dashboard — no SSH, no manual login, no desktop in sight.

<figure>
  <img src="/assets/projects/a40-austin/blog/dash-final-boot.jpg" alt="A40 digital dash booted natively on the Waveshare 12.3 inch DSI panel" />
  <figcaption>Placeholder: final native boot — Godot dash running under Sway on the Waveshare bar display.</figcaption>
</figure>

---

## Section 11 — OEM silent boot with a custom splash

A stock Pi boot dumps a wall of kernel text and a blinking cursor. To turn the key and see only black → vintage Austin crest → sweeping gauges, four problems have to be solved together:

1. **Silence the kernel.** Hide the scrolling logs, blinking cursor, and Pi logos via the boot command line.
2. **Add a splash engine.** Pi OS Lite has no boot-time image renderer, so Plymouth has to be installed manually.
3. **Pre-rotate the splash.** The Waveshare panel is portrait-native; doing live matrix rotation in Plymouth is slow, so the splash PNG is rotated 90° on the Mac before it ever hits the Pi.
4. **GPU handoff.** Plymouth holds the framebuffer after the splash; without an explicit `plymouth quit`, Sway never gets the screen. (Already handled in the systemd unit in Section 10.)

### Step 1 — Generate the splash (Mac)

The repo includes [scripts/a40-splash-generator.py](scripts/a40-splash-generator.py) — a Pillow script that renders the Austin A40 crest (oxblood enamel, robin's-egg-blue diagonal band, tall gold "40" numerals, gold "Austin" cursive) and emits **two** files in a single run:

- `scripts/output/a40-dash/a40-boot-splash-portrait.png` — **720×1920**, pre-rotated 90° for Plymouth on the portrait-native panel.
- `public/assets/projects/a40-austin/blog/a40-boot-splash-landscape.png` — **1920×720**, landscape, for the blog frontend.

```bash
source $HOME/miniconda3/etc/profile.d/conda.sh
conda activate a40-gauge
python scripts/a40-splash-generator.py
```

> **Note — rotation.** The Pi output defaults to `--rotate 90` to match Sway's `output * transform 270`. If it boots upside-down, regenerate with `--rotate 270`. The blog output is always landscape and is never rotated. Pass `--blog-out ''` to skip writing the blog copy.

<figure>
  <img src="/assets/projects/a40-austin/blog/a40-boot-splash-landscape.png" alt="Generated Austin A40 boot splash crest with diagonal band and gold lettering" />
  <figcaption>Generated boot splash, shown in landscape for readability. The actual file shipped to the Pi is pre-rotated 90° to match the panel.</figcaption>
</figure>

### Step 2 — Muzzle the kernel (Pi)

```bash
ssh sr20@dash.local
sudo nano /boot/firmware/cmdline.txt
```

The whole file must stay as **one continuous line** — do not press Enter. Find `console=tty1` and change it to `console=tty3`. Then append at the very end (with a leading space):

```text
quiet splash plymouth.ignore-serial-consoles loglevel=0 logo.nologo vt.global_cursor_default=0
```

Save and exit (`Ctrl+O`, `Enter`, `Ctrl+X`).

### Step 3 — Install Plymouth (Pi)

```bash
sudo apt-get update
sudo apt-get install plymouth plymouth-themes pix-plym-splash -y
```

### Step 4 — Inject the splash and bake it in (Mac → Pi)

```bash
# From the Mac
scp scripts/output/a40-dash/a40-boot-splash-portrait.png sr20@dash.local:~

# Then on the Pi
ssh sr20@dash.local
sudo mv /usr/share/plymouth/themes/pix/splash.png \
        /usr/share/plymouth/themes/pix/splash.png.bak    # first time only
sudo cp ~/a40-boot-splash-portrait.png /usr/share/plymouth/themes/pix/splash.png
sudo plymouth-set-default-theme -R pix                    # 1–2 minutes
sudo reboot
```

Expected boot sequence: panel powers on → stays black → A40 crest fades in → Plymouth quits, hands off the GPU → Sway brings up the Godot dashboard with sweeping needles.

### Updating the splash later

Once everything is wired, swapping the logo is a four-step routine — no code changes needed.

1. **Generate the images (Mac).** Run `python scripts/a40-splash-generator.py` — it writes both `a40-boot-splash-portrait.png` (Pi) and `a40-boot-splash-landscape.png` (blog) in one shot.
2. **Send the portrait copy to the Pi.** `scp scripts/output/a40-dash/a40-boot-splash-portrait.png sr20@dash.local:~`
3. **Drop it into Plymouth.** `ssh sr20@dash.local 'sudo cp ~/a40-boot-splash-portrait.png /usr/share/plymouth/themes/pix/splash.png'`
4. **Bake and reboot.** `ssh sr20@dash.local 'sudo plymouth-set-default-theme -R pix && sudo reboot'`

The new splash takes effect on the next power cycle.
