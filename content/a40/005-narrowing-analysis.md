---
title: "Narrowing Analysis"
date: 2026-03-01
status: in-progress
epic: chassis
tags: [suspension, geometry, analysis]
---

This is where it gets interesting. There are two obvious ways to narrow a double wishbone suspension and they do very different things to the geometry.

## Two options

**Option 1: Shorten the control arms.** The Miata arms are stamped steel so you can't just cut and sleeve them like tube arms. You'd need to fabricate entirely new arms that are shorter, or find a way to section the stamped ones and reweld them. Either way you end up with shorter arms on the same knuckle. The problem is this changes the arm length ratios and the geometry goes bad fast. Shorter arms means more camber change per inch of travel, the roll center drops, and the suspension becomes twitchy. You're also putting structural welds in components that see huge loads every time you hit a bump.

**Option 2: Move the inner pickup points inward on the frame.** Keep the arms at or near stock length, keep the knuckle and spindle stock, but mount everything further inboard. This is only possible if you're building a custom frame, which I am.

I'm going with option 2. The arm geometry stays closer to what Mazda designed. The ratio between upper and lower arm lengths is what defines how the wheel moves through travel, and if you keep those ratios similar you keep the camber curve closer to stock. The roll center migration through travel also stays more predictable. And you don't have to fabricate or modify the arms themselves.

## The tricky part

Moving pickup points inward isn't free either. The challenges:

- **Roll center height.** Even with stock-length arms, moving the inner points inward changes the instant center location. The roll center wants to migrate differently than stock. I'm adjusting the vertical position of the pickup points (moving them up or down slightly) to bring the roll center migration back toward something reasonable. This is an iterative process in SA V2.
- **Camber curve.** The goal is to keep the camber curve close to stock through the full range of travel. Small changes in pickup point height make a big difference here. A few millimeters of vertical offset on the inner upper pickup can swing the curve significantly.
- **Packaging.** The frame rails have to physically accommodate these pickup points. The locations that work best geometrically might not work structurally, or they might conflict with motor mounts or steering rack placement. Everything has to fit.
- **Bump steer.** The steering rack and tie rod ends need to be in the right geometric plane relative to the lower control arm. Moving the suspension inward means the rack probably needs narrowing too, and if the tie rod angle is wrong you get the wheels steering themselves over bumps.
- **Scrub radius.** With the wheel closer to the frame, the relationship between the kingpin axis and the tire contact patch changes. Too much positive scrub radius and the car pulls under braking and feels heavy to steer.

## The process in Suspension Analyzer V2

SA V2 lets you model the full 3D geometry and see what happens as you change each pickup point. But it's not just about narrowing, the whole vehicle context matters. The A40 has a different wheelbase, a much higher center of gravity, and different weight distribution than the Miata. All of that feeds into the model.

The approach is to model the full geometry from the start rather than narrowing first and adjusting later. Less iteration, fewer surprises:

1. Enter the stock MX-5 NA geometry as baseline
2. Set the actual A40 wheelbase length and estimated weight distribution, these change longitudinal weight transfer characteristics like dive under braking and squat under acceleration
3. Set the COG height to reflect the A40 body sitting on the frame, this is significantly higher than the Miata and directly affects how much body roll the suspension has to manage
4. Move inner pickup points inward to the target A40 track width, keeping the knuckle/spindle stock
5. Adjust pickup point heights to correct roll center and camber curve, checking that the roll couple (distance between roll center and COG) isn't producing excessive body roll for the spring rates available
6. Check: camber curve through full travel, roll center height and migration, scrub radius, bump steer, kingpin inclination
7. Verify anti-dive and anti-squat percentages are reasonable for the new wheelbase, the longer or shorter wheelbase changes the side-view swing arm geometry which controls how much the nose dips under braking and the rear squats under acceleration
8. Find the combination where the track width fits the A40 and the geometry is still acceptable across all parameters

## Wheelbase and COG considerations

The Miata NA wheelbase is 2265mm. The A40 Devon is around 2350mm. That difference changes things:

- **Anti-dive geometry.** The side-view instant center location is a function of arm angles and wheelbase. With a longer wheelbase the longitudinal weight transfer per unit of deceleration is slightly less, but the arm angles need to be set to get reasonable anti-dive percentages. Too little anti-dive and the front dives excessively under braking, too much and the ride gets harsh over bumps because the suspension can't compress freely.
- **Anti-squat.** Same idea for the rear. The four-link rear setup needs its instant center set relative to the A40's actual wheelbase and COG height, not the Miata's.
- **Body roll.** This is the big one. The A40 body sits much higher than a Miata. The COG might be 100-150mm higher depending on final build weight and how low the body sits on the frame. A higher COG means more roll moment for the same lateral acceleration. The roll center height needs to be set carefully, if it's too low the roll couple is huge and you need very stiff springs to control body roll, which kills ride quality. If the roll center is too high you get jacking effects and unpredictable weight transfer. The sweet spot is narrower than it would be on the Miata.
- **Spring and damper rates.** These have to be chosen in context. The model needs to show that the geometry works with spring rates that are stiff enough to control body roll at the higher COG but soft enough that the car isn't brutal on rough roads. The 1950s Austin was a cruiser, it shouldn't ride like a go-kart.

There's always a compromise. The narrowed geometry won't match stock Miata exactly, the goal is to keep it in a range that drives well and is predictable. Getting the roll center migration close to stock is the priority since that's what defines how the car feels in corners, but everything has to be evaluated in the context of the A40's actual dimensions and weight.

More to come with screenshots and the actual analysis results as I work through the iterations. This post will be updated with images showing the geometry at each stage.
