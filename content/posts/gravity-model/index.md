---
title: "Earth Gravity Modelling"
date: "2020-09-28"
author: Michael Wrona
draft: true
tags: ["sensors"]
---

Contrary to popular belief, EARTH IS *NOT* FLAT. In fact, earth is kinda lumpy and fat. Earth has a larger radius at it's equator compared to the poles. According to the World Geological Survey 1984, earth's mean equatorial radius is about 6,378km and its mean polar radius is about 6,357km - a 21km difference! Earth's peaks, vallies, and varying composition also contributes towards earth's irregular shape and mass distribution. While these properties may seem unimportant to the average person, they are extremely important to consider for high-precision land, air, sea, and space navigation.

Equations of motion for ground vehicles, submarines, aircraft, rockets, missiles, and spacecraft use gravitational acceleration `$g$` in them. If you've taken any basic physics class, you probably took `$g$` to be `$9.81m/s^2$` and never questioned it, and so did I. This simple approximation works fine for back-of-the-napkin calculations, but as with most things in science and engineering, is not good enough for actual use. Therefore, high-precision navigation of the above vehicles depends on how accurately you can compute `$g$`.

The field of geodesy involves measuring and modelling earth's size, shape, mass distribution, and gravitational acceleration. These scientists develop complex mathematical models that approximate earth's topology and gravitational acceleration. In this post, I'll explain a simple, yet reasonably accurate formula used to compute gravitational acceleration as a function of position.

## WGS84

Gravity as we all know it, `$g = 9.81 m/s^2$`, was derived from the World Geological Survey 1984 (WGS84) standard. This was an international meeting to arrive on globally-accepted parameter values that described earth's shape and gravitational acceleration. WGS84 gravitational acceleration is `$g_0 = 9.80665 m/s^2$`. Round that to 2 decimal places, and you arrive at the familiar `$g = 9.81m/s^2$`.

If you're curious, here are the WGS84 parameters:

Parameter | Symbol | Value
--- | --- | ---
Semi-Major Axis | a | `$6378137 m$`
Semi-Minor Axis | b | `$6356752.314245 m$`
Eccentricity | e | `$0.0818191908426215$`
Standard Grav. Accel. | `$g_0$` | `$9.80665 m/s^2$`
Gravitational Constant | GM | `$3.986004418 * 10^{14} m^{3}/s^2$`


## Things that Affect `$g$`

Before introducing the gravity model, it is beneficial to know what factors perturb `$g$`.

### Altitude Losses

As you travel farther away from earth, you'll begin to escape earth's gravity influence and `$g$` will decrease. In fact, gravity altitude losses follow an inverse-square law. According to the models I introduce later, at 10,000m above mean sea level (MSL), `$g$` decreases by about `$0.03 m/s^2$`. At 50,000m above MSL, `$g$` decreases by about `$0.15m/s^2$`. For non-precision applications near sea-level or very close to the surface, this factor could be negligible, but for airliners, rockets, and spacecraft, altitude losses must be accounted for. Therefore, we will model altitude losses as a function of altitude above MSL.

### Earth's Oblateness

Earth is not perfectly spherical - it's equatorial radius is about 21km greater than the polar radius due to outwards rotational centripetal force. This phenomena is called 'oblateness.' In fact, **earth's oblateness is the most significant gravitational perturbation** (in magnitude). To explain why earth's oblateness affects `$g$`, we must assume a point mass approximation where earth's mass is concentrated at a point at it's center. At the equator, we'd be higher and further away from earth's center due to oblateness. As described in the Altitude Losses section, this means `$g$` will less at the equator than at the poles. Therefore, we will model oblateness effects as a function of latitude.

### Sub-Surface Composition

The earth beneath our feet is not uniform. Earth's crust is made of dirt and rock, and the its core dense, molten rock. The gravity force we experience is due to earth's mass, so denser sub-surface compositions will increase gravitational acceleration slightly. Local changes in sub-surface composition are smaller in magnitude than oblateness effects and altitude losses, making it much more difficult to model. State-of-the-art gravity models can compute this as functions of latitude and longitude, but are not included in the much simpler model I will introduce.

### Recap

In decreasing order:

1. Oblateness effects
2. Altitude losses
3. Sub-surface composition

## 

## Modelling Altitude Losses

Modelling altitude losses is the simplest. The following equation computes altitude loss as a function of altitude above MSL:

$\Delta g(h) =  \frac{GM}{(a + h)^2} - \frac{GM}{a^2}$
