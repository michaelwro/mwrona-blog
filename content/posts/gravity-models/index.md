---
title: "Earth Gravity Modelling"
date: "2022-01-14"
author: Michael Wrona
draft: false
tags: ["sensors"]
---

Contrary to popular belief, EARTH IS *NOT* FLAT. Earth's mean equatorial radius is about 6,378km and its mean polar radius is about 6,357km - a 21km difference! Earth's mountains, vallies, oceans, and varying sub-surface composition also contributes towards earth's irregular shape and therefore mass distribution. While this may seem unimportant for the average person, they are extremely important to consider for high-precision land, air, sea, and space navigation.

Equations of motion for ground vehicles, submarines, aircraft, rockets, missiles, and spacecraft use gravitational acceleration `$g$` in them.  and Therefore, high-precision navigation of the above vehicles depends on how accurately you can compute `$g$`.

The field of geodesy involves measuring and modelling earth's size, shape, mass distribution, and gravitational acceleration. If you've taken any basic physics class, you probably know `$g$` as `$9.81m/s^2$` and never questioned it, as did I. This simple approximation works fine for back-of-the-napkin calculations, but as with most things in science and engineering, is not good enough for actual use. In this post, I'll introduce a relatively simple, yet accurate formula developed by geodesists to compute gravitational acceleration as a function of position and altitude.

## WGS84

Gravity as we all know it, `$g = 9.81 m/s^2$`, is derived from the World Geodetic System 1984 (WGS84) standard. WGS84 was developed by the US National Geospatial-Intelligence Agency to be a standard coordinate system and parameter set for cartography and geodesy. In fact, the WGS84 system is what GPS uses to define your latitude, longitude, and altitude. The WGS84 standard contains fundamental constants that define earth's shape and gravitational acceleration. WGS84 gravitational acceleration is `$g_0 = 9.80665 m/s^2$`. Round that to 2 decimal places, and you arrive at the familiar `$g = 9.81m/s^2$`.

### WGS84 Constants

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

As you travel farther away from earth, you'll begin to escape earth's gravity influence and `$g$` will decrease. In fact, gravity altitude losses follow an inverse-square law and are a function of altitude above mean sea level (MSL). According to the models I'll introduce in a bit, at 10km MSL, `$g$` will have decreased by about `$0.03 m/s^2$`. At 50km MSL, the loss is about `$0.15m/s^2$`. For non-precision applications near sea-level, this factor could be negligible, but for airliners, rockets, and spacecraft, altitude losses must be accounted for.

### Earth's Oblateness

Earth's equatorial radius is about 21km greater than the polar radius due to earth's rotation (outwards centripetal force). This phenomena is called 'oblateness.' In fact, **earth's oblateness is the most significant gravitational perturbation.** To explain why earth's oblateness affects `$g$`, we must assume a point mass approximation, where earth's mass is concentrated at a point at it's center. At the equator, we'd be about 21km farther away from earth's center of mass compared to the poles. As described in the Altitude Losses section, this means `$g$` will less at the equator than at the poles. Oblateness effects are typically modelled as a function of latitude (and longitude in high fidelity models).

## Modelling Altitude Losses

Modelling altitude losses are the simplest. The following equation computes altitude loss as a function of altitude above MSL:

`$$\Delta g(h) =  \frac{GM}{(a + h)^2} - \frac{GM}{a^2} \,\, m/s^2$$`

`$h$` is altitude above MSL, and values for `$GM$` and `$a$` can be found in the WGS84 table above. This equation is known as "free air correction" (FAC).

## Gravity Models

The two most popular gravity models are Helmert's equation and the WGS84 model.

### Helmert's Equation

Helmert's equation is also known as the [International Gravity Formula](https://en.wikipedia.org/wiki/Theoretical_gravity#Basic_formulas). It computes *MSL* gravitational acceleration as a function of geodetic latitude `$\phi$`.

`$$ g(\phi) = 9.780327 \left[1 + 0.0053024\sin^{2}(\phi) - 0.0000058\sin^{2}(2\phi)\right]\ \, m/s^{2} $$`

### WGS84 Gravity Model

The [WGS84 gravity model](https://en.wikipedia.org/wiki/Theoretical_gravity#Somigliana_equation) coefficients are derived from WGS84 constants. It also computes *MSL* gravitational acceleration as a function of geodetic latitude.

`$$ g(\phi) = 9.780325335903891718546\left[{\frac {1+0.00193185265245827352087\sin ^{2}(\phi )}{\sqrt {1-0.006694379990141316996137\sin ^{2}(\phi )}}}\right]\ \, m/s^{2}$$`

## Combining Equations

The two gravity models compute gravitational acceleration at sea level. To accound for altitude above MSL, you must apply the free air corrections. Simply add the free air correction equation to Helmert's equation or the WGS84 model. I'll use Helmert's equation as an example.

`$$ g(\phi, h) = g(\phi) + \Delta g(h) $$`

`$$ g(\phi, h) = 9.780327 \left[1 + 0.0053024\sin^{2}(\phi) - 0.0000058\sin^{2}(2\phi)\right] + \left(\frac{GM}{(a + h)^2} - \frac{GM}{a^2}\right) \,\, m/s^{2} $$`

# Final Remarks

Both of these equations are pretty accurate approximations compared to higher fidelity gravity models. Personally, I would feel comfortable using these equations for altitudes less than 70 km. For higher altitude applications, I would use a more accurate gravity model. Have fun using this in your projects!

