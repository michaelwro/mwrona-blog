---
title: "Quadcopter Flight Controller Project Intro"
date: "2020-08-31"
author: Michael Wrona
draft: false
tags: ["drone", "sensors"]
---

Ever since I was first introduced to the world of flight dynamics and controls, I have wanted to design my own quadcopter flight controller from scratch. I thought it would be a great opportunity to apply my knowledge of electronics and circuitry, programming, and flight controls towards a real-world project. Unfortunately, my intense aerospace engineering coursework got in the way and never gave me enough time to get started. Now that I graduated from college and am spending a lot more time at home during the COVID-19 quarantine, now is a good of time as ever for me to get started with this project! This post will serve as a brief overview of the project and outline my short and long-term goals for it.

## Desired Features

* Made from widely available COTS components
* Custom-made PCB
* Sensors: IMU, magnetometer, barometer, and GPS
* Extended Kalman Filter (EKF) for sensor fusion/state estimation
* Linear Quadratic Regulator (LQR) flight control

### Components

When I first sat down to begin planning out my quadcopter flight controller, I made a list of high-level features that I wanted to incorporate. First and foremost, I wanted the flight controller to be made from widely available commercial off the shelf (COTS) components. I wanted to ensure that all sensors and quadcopter parts would not stop being manufactured anytime soon and become unavailable for future readers.

### Custom PCB

Next, I would like to design a custom PCB for the flight controller board. The other alternative to a custom PCB would be to solder components to perf-board. This has the advantage of being cheaper and faster to prototype, but the overall board footprint would be larger, and the wiring would be very messy. Creating a custom PCB for the flight controller would allow the board footprint to be smaller and a bit more reliable in terms of electrical connections. Also, it would make the whole thing look way more professional :)

### Sensor Suite

Sensors are the most important components in a flight controller. They are your system's eyes and ears, after all. The absolute bare-minimum sensor suite to fly a drone is a gyroscope and accelerometer. The gyro measures angular rates, and the accelerometer measures roll and pitch angles. With this minimum sensor suite, I'd be limited to only flying in what's called 'Acro Mode.' This flight mode is what professional drone racers use and is very unstable to fly in. Altitude hold and GPS waypoint missions are completely out of the question as well.

Therefore, my flight controller will have an IMU, mangetometer, barometer, and GPS sensor onboard. The IMU, or intertial measurement unit, consists of an accelerometer and gyroscope. The gyro and accelerometer measurements can be fused to compute roll and pitch angles and rates. The magnetometer is basically a 3D compass. It will be used to determine our quadcopter's mangetic heading, just like a compass! Next, the barometer is an atmospheric pressure sensor. We can use a math equation to convert the change in atmospheric pressure from our takeoff location and pressure during flight into a change in altitude. Therefore, on a flight controller, a barometer is referred to as a barometric altimeter: they measure changes in altitude based on changes in pressure. Finally, a GPS sensor will tell our drone its position as latitude and longitude, ground speed in knots, and course/bearing with respect to true north. This sensor configuration is very common among quadcopters and will enable ours to fly in both manual and autonomous flight modes!

### EKF Sensor Fusion

In order to convert and fuse sensor readings into useful state parameters (state variables) for our flight controller, we need something called a state observer/estimator. [Kalman filters](https://en.wikipedia.org/wiki/Kalman_filter) are an extremely common state estimator, especially in aerospace control systems. At a high level, Kalman filters are based on a predictor-corrector model. High-rate, low-accuracy sensors predict state variables between low-rate, high-accuracy sensor readings which update those predictions. Also, not all state variables are directly observable by our sensors. Therefore, Kalman filters are used to estimate all state variables based on partial sensor observations.

The two most commonly implemented Kalman filters are the linear Kalman Filter (KF) and the nonlinear [Extended Kalman Filter (EKF)](https://en.wikipedia.org/wiki/Extended_Kalman_filter). EKFs have the advantage of taking system and sensor nonlinearities into account and therefore predict state variables a bit better than the linear KF. Unfortunately, EKFs are very complex to develop and are more computationally complex/intense than the KF. Therefore, a beefy computer is required if an EKF is going to fly onboard our flight controller!

### LQR Control

After sensor readings are taken and fused via the EKF, they are handed over to the control algorithms. The control algorithms decide what commands to send to the quadcopter's rotors in order to control the drone to a desired state. This desired state could be a desired pitch angle, altitude, GPS position, and so on. The most popular control technique by far is [PID control](https://en.wikipedia.org/wiki/PID_controller#:~:text=A%20proportional%E2%80%93integral%E2%80%93derivative%20controller,applications%20requiring%20continuously%20modulated%20control.). PID stands for proportional, integral, and derivative. Just as the name hints, PID control uses the sum of the error, the time-integral of the error, and time-derivative of the error between the current state and desired state, with each term multiplied by a respective constant gain. These gains are referred to as the PID gains. PID control has the advantage of being conceptually and computationally simple. Our control algorithms will have to control multiple state variables simultaneously, which illuminates the major drawback of PID control. PID control is a SISO, or single-input, single-output, control technique. This means that a PID controller can only control one state variable at a time. Therefore, multiple PID controllers are required to control multiple state variables.

`$$e(t) = x(t)_{desired} - x(t)_{current}$$`
`$$u(t)_{ctrl} = K_p e(t) + K_i\int_0^t e(t)dt + K_d\frac{de(t)}{dt}$$`

[LQR control](https://en.wikipedia.org/wiki/Linear%E2%80%93quadratic_regulator), or linear quadratic regulator control, is a MIMO, or multi-input, multi-output control technique. LQR control allows multiple states to be controlled simultaneously with a single controller. The linear part refers to the fact that the controller needs a linear [state-space model](https://en.wikipedia.org/wiki/State-space_representation#:~:text=The%20%22state%20space%22%20is%20the,variables%20are%20expressed%20as%20vectors.) of your system. The quadratic part comes from the fact that a quadratic cost function is minimized to compute control gains. Therefore, LQR controls a system in an optimal sense. Finally, the regular part refers to the fact that LQR control regulates, or controls, all states to zero. This is typically not desired, so instead, the time-integral of the error between current and desired state values are regulated to zero. LQR is also a bit more intuitive to tune than PID control. For these reasons, I will implement a LQR controller on my drone.

## Development Progression

Below is a rough outline of the flight controller development progression I will follow.

1. Test sensors
2. Create sensor libraries
3. Implement AHRS
4. Design and manufacture full flight controller PCB
5. Implement full-state EKF
6. Assemble drone frame with motors, ESCs, etc.
7. Design, test, and tune LQR controller
   1. [Stabilize flight mode](https://ardupilot.org/copter/docs/stabilize-mode.html)
8. First test flight!

First, I will test the sensors and develop my own sensor libraries. Next, I will develop my first EKF and create an AHRS, or attitude and heading reference system. Just as the acronym suggests, an AHRS fuses gyroscope, accelerometer, and magnetometer data to compute the drone's roll, pitch, and heading angles. Developing an AHRS will serve as an opportunity for me to develop an EKF from scratch and figure out how to implement it with C++ code. The AHRS can simply be contructed on a breadboard for testing. Next, I will design, print, and assemble the final flight controller PCB. In order to accomplish this, I will need to identify all circuit components and learn how to use PCB design software (I am planning on using [KiCAD](https://kicad-pcb.org/)). I am constructing the flight computer first so that I can then design the full-state EKF and control algorithms. This would be very hard to accomplish with all the sensors on a breadboard, so that's why I'm creating the PCB first. After I finish the PCB and EKF, I will assemble the quadcopter frame, complete with motors and ESCs. With the quadcopter fully assembled, complete with the controller, I can move onto developing, testing, and tuning the LQR control algorithms. Finally, after some simple tests, I can attempt a first test flight!

## Long-Term Goals

My first long-term goal for my quadcopter flight controller project is to implement more complex flight modes, such as altitude/position hold and GPS waypoint-following capabilities.

Next, I would like to investigate implementing model predictive control (MPC) algorithms onboard the controller. MPC algorithms are very complex and require very fast computers in order to function. If I were to implement MPC onboard my flight controller, I'd likely need a separate computer dedicated solely to performing MPC calculations.

Finally, I am very interested in the prospect of using drones for package delivery. I would really like to design a quadcopter capable of flying a package delivery mission profile completely autonomously and deliver a tiny package at its destination.


## Conclusion

I hope this served as a thorough glimpse into my quadcopter flight controller project. I am looking forward to making progress and sharing tidbits along the way!
