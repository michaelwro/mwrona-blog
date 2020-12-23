---
title: "Designing a Quaternion-Based EKF for Accelerometer, Gyroscope, & Magnetometer Fusion"
date: "2020-12-20"
author: Michael Wrona
draft: true
tags: ["control theory", "sensors"]
---

One of the most important parts of any aerospace control system are the sensor fusion and state estimation algorithms. This software system is responsible for recording sensor observations and 'fusing' measurements to estimate parameters such as orientation, position, and speed. The quality of sensor fusion algorithms will directly influence how well your control system will perform. Poor, low-grade sensor fusion software will result in poor controller performance. Therefore, especially for costly aerospace systems, designing robust, efficient, and high-performance sensor fusion software is extremely important to ensuring mission success. One of the most popular sensor fusion algorithms is the Extended Kalman Filter (EKF). Unlike the linear Kalman Filter, EKFs are nonlinear and can therefore more accurately account for nonlinearities in sensor measurements and system dynamics. One popular sensor fusion application is fusing inertial measurement unit (IMU) measurements to estimate roll, pitch, and yaw/heading angles. This article will describe how to design an Extended Kalman Filter (EFK) to estimate gyro biases, roll, pitch, and heading angles from 9-DOF (degree of freedom) IMU accelerometer, gyroscope, and magnetomoeter measurements.

# Background

## Coordinate System

Roll, pitch, and yaw angles need to be defined relative to something. We will be computing roll, pitch, and yaw relative to the [NED (North, East, Down) reference frame](https://en.wikipedia.org/wiki/Local_tangent_plane_coordinates). In the NED frame, the positive X-axis points towards true north, the positive Z-axis is parallel to gravitational acceleration downwards, and the Y-axis completes the right-handed triad.

## Quaternions

We will be using quaternions to describe our IMU's orientation. Quaternions (denoted as `$q$`) are a four-parameter set used to describe orientation. Compared to Euler angles, quaternions do not suffer from gimbal lock and are more numerically stable and computationally efficient. Quaternion orientation is described as a rotation angle `$\theta$` about an Euler axis `$\vec{e}$`.

`$$\begin{equation} \vec{q} = \begin{bmatrix} q_0 \\ q_1 \\ q_2 \\ q_3 \end{bmatrix} = \begin{bmatrix} cos\theta \\ e_1 sin(\theta/2) \\ e_2 sin(\theta/2) \\ e_3 sin(\theta/2) \end{bmatrix} \end{equation}$$`

The quaternion kinematic differential equation is given in equation `$\eqref{eq:quat-kin}$` in matrix form, and relates body angular velocities to quaternions:

`$$ \begin{equation} \begin{bmatrix} \dot{q_0} \\ \dot{q_1} \\ \dot{q_2} \\ \dot{q_3} \end{bmatrix} = \frac{1}{2} \begin {bmatrix} -q_1 & -q_2 & -q_3 \\ q_0 & -q_3 & q_2 \\ q_3 & q_0 & -q_1 \\ -q_2 & q_1 & q_0 \end{bmatrix}  \begin{bmatrix} \omega_1 \\ \omega_2 \\ \omega_3 \end{bmatrix} \label{eq:quat-kin} \end{equation}$$`

### Euler Angles and Quaternions

Euler angles are a three-parameter set used to describe orientation. In particular, we will be using the '3-2-1' Euler angles, commonly referred to as roll (`$\phi$`), pitch (`$\theta$`), and yaw (`$\psi$`). Euler angles are intuitive and easy to visualize attitude parameters but are subject to [gimbal lock](https://en.wikipedia.org/wiki/Gimbal_lock) when pitch angle `$\theta$` is 90 degrees. We can use equations `$\eqref{eq:quat2roll}$` through `$\eqref{eq:quat2yaw}$` to convert from quaternions and Euler angles.

`$$\begin{equation} \phi = atan2 \left( 2(q_2 q_3 + q_0 q_1), \quad q_0^2 - q_1^2 - q_2^2 + q_3^2 \right) \label{eq:quat2roll} \end{equation}$$`
`$$\begin{equation} \theta = -asin \left( 2(q_1 q_3 - q_0 q_2) \right) \label{eq:quat2pitch} \end{equation}$$`
`$$\begin{equation} \psi = atan2 \left( 2(q_1 q_2 + q_0 q_3), \quad q_0^2 + q_1^2 - q_2^2 - q_3^2 \right) \label{eq:quat2yaw} \end{equation}$$`

## Gyroscope Measurement Model

Gyroscopes measure body angular rotation rates in degrees per second [deg/s]. Ideally, gyro measurements could be time-integrated to compute body angles in degrees. Unfortunately, this direct integration is not possible due to gyro offset and gyro drift. If raw gyro measurements were taken while stationary, the readings would be close to zero, but non-zero. This offset from zero while stationary is called gyro offset. If these raw gyro measurements were time-integrated, the computed angles would slowly increase over time, despite the gyro being stationary. This angle 'drift' is called gyro drift. Therefore, gyro measurement offset causes gyro drift in time-integrated gyro measurements. An illustration of gyro grift can be seen in ___________. 

Gyro offset can be determined by experimentation and hard-coded into software. This is the simplest approach and may suffice for recreational applications. However, it is very advantageous and relatively simple to estimate gyro bias with an EKF. In order to estimate gyro bias, a measurement model must be developed. It is assumed that gyro bias is time-invariant, or constant with time, in this derivation. In reality, the gyro bias varies with time and temperature, but the change is typically small, making constant bias a reasonable simplification. Equation `$\eqref{eq:gyro-model}$` is the simplified sensor model used in this derivation.

`$$\begin{equation} \vec{\omega}_{corr} = \vec{\omega}_{meas} - \vec{b} \quad , \quad \dot{b} = 0 \label{eq:gyro-model} \end{equation}$$`

Where `$\vec{\omega}_{corr}$` are the corrected gyro measurements (three measurements), `$\vec{\omega}_{meas}$` are the measured gyro readings, and `$\vec{b}$` are the gyro biases.

## Roll and Pitch From Accelerometer Measurements

One important operation performed in our EKF will be computing roll and pitch angles from accelerometer measurements. Since we assume gravitational acceleration is straight down in our coordinate system, we can compute roll and pitch angles relative to the gravity vector. [A detailed derivation of this method can be found here](/posts/04-accel-roll-pitch/). We will assume the positive Z-axis is parallel to gravitational acceleration downwards, and the XY plane is perpendicular to gravity. Since gravity is independent of heading angle, yaw angle cannot be deterrmined from accelerometer measurements. To put it simply, we cannot measure heading with an accelerometer and gyro because gravity does not depend on heading. The equations to compute roll and pitch from accelerometer measurements are given in equations `$\eqref{eq:accel2roll}$` and `$\eqref{eq:accel2pitch}$`.

`$$\begin{equation} Roll = \phi = arctan \frac{a_y}{a_z} \label{eq:accel2roll} \end{equation}$$`
`$$\begin{equation} Pitch = \theta = arcsin \frac{a_x}{g} = arcsin \frac{a_x}{\sqrt{a_x^2 + a_y^2 + a_z^2}} \label{eq:accel2pitch} \end{equation}$$`

Where `$a_x, a_y$` and `$a_z$` are the accelerometer measurements. It is important to note that these equations are valid only when the accelerometer is stationary and not influenced by accelerations other than gravitational. These equations should still work for most applications, accept dynamic ones.

{{< figure src="/post-imgs/04-accel-roll-pitch/coord-sys.png" alt="Coordinate System" width="300px" position="center" style="border-radius: 8px;" caption="Visualization of roll and pitch angles w.r.t the NED frame." captionPosition="center">}}

## Tilt-Compensated Compass

Three-axis magnetometers are essentially three-dimensional compasses. They measure the local magnetic field vector, including earth's mangetic field. External paramagnetic and electromagnetic sources can cause [hard and soft-iron distortions](https://www.vectornav.com/resources/magnetometer-errors-calibration) to magnetometer measurements. These distortions can be accounted for through calibration. We will assume that the magnetometer measurements are already calibrated for hard and soft-iron distortions.

Also, the NED coordinate frame is relative to [true north](https://gisgeography.com/magnetic-north-vs-geographic-true-pole/). Our magnetometer measures earth's magnetic field and therefore compass heading relative to mangetic north. The difference in heading between true north and magnetic north is called [magnetic declination](https://www.ngdc.noaa.gov/geomag/declination.shtml), often denoted as `$\delta$`. Magnetic declination is dependent on latitude, longitude, and altitude. Declination, field strength, and other parameters can be determined via a earth magnetic field model, such as the [World Magnetic Model 2020 (WMM2020)](https://www.ngdc.noaa.gov/geomag/WMM/limit.shtml).

In order to compute true heading from magnetometer measurements and correct for sensor tilt, we will create a 'tilt-compensated compass' using equation `$\eqref{eq:tilt-compass}$`.

`$$\psi_{true} = \psi_{mag} + \delta $$`

`$$\begin{equation} \psi_{true} = atan2 \begin{pmatrix} -m_y cos\phi + m_z sin \phi \\ m_x cos\theta + m_y sin\phi sin\theta + m_z cos\phi sin\theta \end{pmatrix} + \delta \label{eq:tilt-compass} \end{equation}$$`

Where `$\psi_{true}$` is true heading, `$\psi_{mag}$` is magnetic heading, and `$m_x$`, `$m_y$`, and `$m_z$` are (calibrated) magnetometer measurements. Roll and pitch can be determined from accelerometer measurements and used in equation `$\eqref{eq:tilt-compass}$`.

# EKF Development

EKFs 





