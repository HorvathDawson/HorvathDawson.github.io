---
title: "Steering"
date: 2024-04-01
status: in-progress
epic: research
tags: [steering, safety, fabrication]
---

The stock A40 steering is unassisted and the column is a solid shaft pointed straight at your chest. Both of those need to change. Plan is electric power assisted rack and pinion steering, a collapsible column, and a narrowed Miata rack to match the A40's reduced track width.

---

## EPAS options

Going the junkyard route to keep costs down. There are two main approaches people use for budget EPAS conversions.

### Column-mounted EPAS

The motor and torque sensor live on the steering column itself, assisting between the steering wheel and the rack. Popular junkyard donors:

- **Toyota Prius** — The go-to cheap option. The column and its small controller can be run in "failsafe" mode with simple wiring (power, ground, ignition on), no aftermarket controller needed. Columns go for $35-50 at U-Pull yards. The controller box bolts right to the column assembly.
- **Saturn Vue** — Another common donor. Pairs well with an aftermarket controller for adjustable assist. The wiring doesn't directly plug into a Prius controller but uses the same terminal sizes.
- **Kia Soul** — Reportedly works well in default mode (powered up, no controller). Key notes from forum experience: use good gauge power and ground cables, and replace the rubber coupling on the motor while the unit is out of the car.

Column-mount is the simplest approach since the assist unit is self-contained and doesn't care what rack you're running. It just adds torque to the column.

### Rack-mounted / electro-hydraulic

Some builders use an electric-hydraulic pump from a donor car to power a conventional hydraulic rack without needing a belt-driven pump. The MR2 Spyder and Volvo S40/V50 electric pumps are popular for this. You remotely mount the pump and run lines to the rack. Downside is you still have hydraulic lines and fluid, and some of these OEM pumps (especially the Volvo) are low-flow units better suited to parking lot speeds than spirited driving.

### Aftermarket kits

Companies like EPAS Performance (sold through Silver Sport Transmissions) make universal kits with a 60-amp electric motor, mounting hardware, and a prewired control module with a potentiometer for adjustable assist. These run around $1,500+ though, which defeats the junkyard budget approach.

### Decision

Going with a **junkyard column-mount EPAS unit**, most likely a Prius or Kia Soul column. Cheapest and simplest option, keeps the rack clean with no hydraulic anything, and the whole assembly can provide power steering even with the engine off (handy for pushing the car around the shop). The column will need to be adapted to fit the A40 dash and connect to the rack, but that's fab work that has to happen anyway since nothing about the stock steering is being reused.

The collapsible column is non-negotiable from a safety standpoint. EPAS keeps things simple: no hydraulic pump to drive off the engine, no high-pressure lines to route and leak, no parasitic power loss.

---

## Rack narrowing

The Miata NA rack housing is ~578mm. The A40's narrower track needs it shortened to match. The rack is depowered (Flyin' Miata method) and the EPAS unit replaces the hydraulic system.

### Process

The common approach for shortening a rack is to cut both the housing and the rack gear, then weld the housing back together shorter. There's a good [LocostUSA thread](https://www.locostusa.com/forums/viewtopic.php?t=2773) covering that process and the pitfalls. The critical failure mode is rack bar warping from welding heat (causes binding). Mitigate with a V-block fixture and a copper heat sink clamped along the bar during welding. Only cut the non-toothed section.

The plan is to remachine the rack gear as solid billet instead of welding it. A weld on the rack gear is a precision ground surface with a weak point under load.

### How much narrowing

Proven shortening ranges from [LocostUSA](https://www.locostusa.com/forums/viewtopic.php?t=2773): routine (<6"/152mm), moderate (6-8"), practical limit ~10-11". The baseline needs 175mm (6.9"), in the moderate zone.

<figure>
  <img src="/assets/projects/a40-austin/blog/plots/rack_narrowing.png" alt="Rack narrowing required vs front track width with difficulty zones" />
  <figcaption>Rack narrowing vs track width. Background color shows difficulty zone (from LocostUSA builder data). All three build scenarios fall within proven kit-car builder ranges.</figcaption>
</figure>

---

## Ackermann geometry

When the rack narrows by the same amount as the track (required for bump steer), the Miata knuckle steering arm geometry is preserved. The stock Miata arm converges at T=1405, WB=2265 ($\theta_{knuckle} = 17.2°$). On the A40, the narrower track shifts the convergence point 367mm ahead of the rear axle at 2350mm. This gives slightly too much Ackermann.

The mismatch is small. Even at autocross slalom angles (20 degrees of lock, ~7m turn radius) the Ackermann error stays under 1 degree, well within tire slip angles, compliance steer, and normal driver variation. No custom steering arms required.

<figure class="wide">
  <img src="/assets/projects/a40-austin/blog/plots/ackermann.png" alt="Ackermann error vs steering angle with driving scenarios and turn radii" />
  <figcaption>Miata stock knuckle (17.2 deg) on the A40 (track 1230 mm, wheelbase 2350 mm). Top: excess Ackermann vs steering lock with driving scenarios colour-coded and turn radii on the top axis. Even at autocross slalom angles (20 deg, ~7 m radius) the error is under 1 deg. Bottom: at autocross lock angles (15-20 deg) the Ackermann error ranges from ~0.5 deg (below compliance steer) at 15 deg to ~1.0 deg (slightly above compliance steer) at 20 deg, and well below tire slip angles (4+ deg) throughout. The error is tolerable without custom steering arms.</figcaption>
</figure>

### Rack positioning

Adjusting the fore-aft position of the rack by 10-15mm changes Ackermann behavior meaningfully. The inner tie rod angle at the ball joint should stay within 10-12 degrees of horizontal to avoid binding and wear. SA V2 should plot actual Ackermann and steering ratio across the full range before committing to a rack mount position.

---

## References

- [GRM - Junkyard Electric Power Steering Assist](https://grassrootsmotorsports.com/forum/grm/have-we-talked-about-the-junkyard-electric-power-steering-assist-stuff/257657/page1/) - Forum thread covering Prius, Vue, Kia Soul, and electro-hydraulic options with real-world install experiences.
- [ChevyHardcore - Add Electronic Power Steering To Your Classic](https://www.chevyhardcore.com/news/add-electronic-power-steering-to-your-classic/) - Overview of the EPAS Performance kit and how column-mount EPS works on vintage cars.
- [Vintage Mustang - Rack and Pinion Plus EPAS Options](https://www.vintage-mustang.com/threads/rack-and-pinion-plus-epas-options.1183512/) - Discussion of combining aftermarket rack and pinion with EPAS on classic platforms.
- [LocostUSA - Rack shortening thread](https://www.locostusa.com/forums/viewtopic.php?t=2773) - Detailed process and pitfalls of shortening a Miata steering rack, with builder data on proven shortening ranges.
