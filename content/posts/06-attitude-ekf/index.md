---
title: "Designing a Quaternion-Based EKF for Accelerometer/Gyroscope Fusion"
date: "2020-12-20"
author: Michael Wrona
draft: true
tags: ["control theory", "sensors"]
---

One of the most important parts of any aerospace control system are the sensor fusion and state estimation algorithms. This software system is responsible for recording sensor observations and 'fusing' measurements to estimate parameters such as orientation, position, and speed. The quality of the sensor fusion algorithms will directly influence how well your control system will perform. Poor, low-grade sensor fusion software will result in poor controller performance. Therefore, especially for costly aerospace systems, designing robust, efficient, and high-performance sensor fusion software is extremely important to ensuring mission success. One of the most popular sensor fusion algorithm is the Extended Kalman Filter (EKF). Unlike the linear Kalman Filter, EKFs are nonlinear and can therefore more accurately account for nonlinearities in sensor measurements and system dynamics. One popular sensor fusion application is fusing inertial measurement unit (IMU) measurements to estimate roll, pitch, and yaw/heading angles. This article will describe how to design an Extended Kalman Filter (EFK) to estimate quaternion orientation and sensor biases from 6-DOF (degree of freedom) IMU accelerometer and gyroscope measurements.

## Quaternions

We will be using quaternions to describe our IMU's orientation. Quaternions (denoted as `$q$`) are a four-parameter set used to describe orientation. Compared to Euler angles, quaternions do not suffer from gimbal lock and are more numerically stable and computationally efficient. Quaternion orientation is described as a rotation angle `$\theta$` about an Euler axis `$\vec{e}$`.

`$$\begin{equation} \vec{q} = \begin{bmatrix} q_0 \\ q_1 \\ q_2 \\ q_3 \end{bmatrix} = \begin{bmatrix} cos\theta \\ e_1 sin(\theta/2) \\ e_2 sin(\theta/2) \\ e_3 sin(\theta/2) \end{bmatrix} \end{equation}$$`

The quaternion kinematic differential equation is given in equation `$\eqref{eq:quat-kin}$` in matrix form, and relates body angular velocities to quaternions:

`$$ \begin{equation} \begin{bmatrix} \dot{q_0} \\ \dot{q_1} \\ \dot{q_2} \\ \dot{q_3} \end{bmatrix} = \frac{1}{2} \begin {bmatrix} -q_1 & -q_2 & -q_3 \\ q_0 & -q_3 & q_2 \\ q_3 & q_0 & -q_1 \\ -q_2 & q_1 & q_0 \end{bmatrix}  \begin{bmatrix} \omega_1 \\ \omega_2 \\ \omega_3 \end{bmatrix} \label{eq:quat-kin} \end{equation}$$`

## Gyroscope Measurement Model

Gyroscopes measure body angular rotation rates in radians per second [rad/s]. Ideally, the gyro measurements would be time-integrated to compute body angles in degrees or radians. Unfortunately, this direct integration is not possible due to gyro offset and gyro drift. If raw gyro measurements were taken while stationary, the readings would be close to zero, but non-zero. This offset from zero while stationary is called gyro offset. A visualization of gyro offset can be seen in ________. If these raw gyro measurements were integrated, the computed angles would slowly increase over time, despite the gyro being stationary. This angle 'drift' is called gyro drift. Therefore, gyro measurement offset causes gyro drift in time-integrated gyro measurements. An illustration of gyro grift can be seen in ___________.

Gyro offset can be determined by experimentation and hard-coded into software. This is the simplest approach and may suffice for recreational applications. 

## Accelerometer Measurement Model

## 







