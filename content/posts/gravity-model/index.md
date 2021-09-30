---
title: "Earth Gravity Modelling"
date: "2020-09-28"
author: Michael Wrona
draft: true
tags: ["sensors"]
---

Contrary to popular belief, EARTH IS *NOT* FLAT. In fact, earth is kinda lumpy and fat. Earth has a larger radius at it's equator compared to the poles. According to the World Geological Survey 1984, earth's mean equatorial radius is about 6,378km and its mean polar radius is about 6,357km - a 21km difference! Earth's peaks, vallies, and varying composition also contributes towards earth's irregular shape therefore mass distribution. While these properties may seem unimportant to the average person, they are extremely important to consider for high-precision land, air, sea, and space navigation.

Equations of motion for ground vehicles, submarines, aircraft, rockets, missiles, and spacecraft have gravitational acceleration `$g$` in them. If you've taken any basic physics class, you probably took `$g$` to be `$9.81m/s^2$` and never questioned it. This simple approximation works fine for back-of-the-napkin calculations, but as with most things in science and engineering, is not good enough for actual use. Therefore, high-precision navigation of the above vehicles depends on how accurately you can compute `$g$`. 





The field of geodesy involves measuring and modelling earth's size, shape, mass distribution, and gravitational acceleration. 


High-precision navigation therefore depends on how accurately you can compute `$g$`.



I've Engineers programming navigation code for these vehicles use gravity models to compute `$g$` in real-time. 



