---
title: "Rocket Flight Data Computer - Introduction & Requirements Definition"
date: "2022-02-13"
author: Michael Wrona
draft: false
tags: []
---

I have been interested in model rocketry for a long time. Putting the time and energy into designing and building a model rocket, watching it leave the launch pad in a plume of smoke, and fly into the sky is very exciting and rewarding. The model rocketry community is a very passionate and supportive group, too. One figure in the community that I respect is Joe Barnard, founder of [BPS.space](https://bps.space/). Despite coming from a music background, his passion pushed him to learn as much as possible about the complex math and engineering required to design rockets, and created the YouTube channel [BPS.space](https://www.youtube.com/c/BPSspace) to share his progress and inspire others. My passion for space led me to pursue aerospace engineering and am now a spacecraft GNC engineer. I have wanted to dive into the world of model rocketry for a long time and have finally decided to pursue it. In this post, I'd like to introduce ideas for designing and building a model rocket flight data computer.

> MicWro Engineering is developing a model rocket Flight Data Unit (FDU) to log in-flight performance data and give further insight into a rocket's flight.

## Functional Requirements

- The FDU shall include a signal channel to deploy a parachute at apogee.
- The FDU shall include a buzzer to aid in locating the rocket during recovery.
- The FDU shall log data at a minimum sample rate of 50 samples per second.
- The FDU shall write flight data logs to a flash memory chip and dump the logs to a Micro SD card at the end of flight.


## Sensor Requirements

- The FDU shall, at minimum, measure and log the following parameters:
  - Position
  - Speed
  - Acceleration
  - Orientation
  - Apogee (maximum) altitude
  - Atmospheric temperature
- The FDU shall include the following sensors:
  - IMU (accelerometer + gyroscope)
  - Compass
  - GPS
  - Barometer
  - Temperature sensor

### Accelerometer Requirements

- The accelerometer shall have a measurement range of at least +/- 25G's.
- The accelerometer shall have a sample rate of at least 100Hz.
- The accelerometer shall have an ADC resolution of at least 12 bits.
- The accelerometer shall communicate using a SPI interface.

### Gyro Requirements

- The gyro shall have a measurement range of at least +/- 500 degrees per second.
- The gyro shall have a sample rate of at least 100Hz.
- The gyro shall have an ADC resolution of at least 12 bits.
- The gyro shall communicate using a SPI interface.

### Compass (Magnetometer) Requirements

- The compass shall be capable of measuring earth's magnetic field.
- The compass shall have an ADC resolution of at least 12 bits.
- The compass shall have a sample rate of at least 100Hz.
- The compass shall communicate using a SPI interface.

### Altimeter (Barometric Pressure Sensor) Requirements

- The altimeter shall have an ADC resolution of at least 12 bits.
- The altimeter shall be capable of measuring atmospheric pressures up to 30km altitude AGL.
- The altimeter shall communicate using a SPI interface.

### GPS Requirements

- The GPS shall have a sample rate of at least 10Hz.
- The GPS shall communicate at a serial baud rate of at least 115200 bauds per second.



These are high-level requirements that will be refined as development progresses.

## Design Timeline

Here is an approximate flow of events that this project will follow:

1. Define project requirements
2. Select electronics
3. Design electrical schematic
4. Design PCB
5. Design sensor fusion algorithms
6. Develop software
7. Ground testing
8. First flight test

## Ideas for Future Iterations

These features would be nice to have and are good features for future iterations:

- Transmit telemetry data to a ground station
- Bluetooth connectivity + mobile app that displays flight data
