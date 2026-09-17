# RA-KPA Paper Figure Plan


## Overview


The goal of figures is to communicate:

1. Why keypoint reliability is a problem.
2. How RA-KPA solves this problem.
3. Why adaptive reliability improves tracking.



The figure order should follow the paper story:


Problem

↓

Observation

↓

Method

↓

Evidence

↓

Improvement



---

# Figure 1

## Motivation: Temporal Keypoint Reliability Variation


## Purpose


Show that keypoints do not maintain constant reliability during articulated tracking.



## Layout


Two-column comparison.



## Left: Conventional Optimization


Input:

Temporal keypoint observations.



Assumption:


All keypoints have equal importance.


\[
w_i=1
\]


Problem:


Unreliable keypoints contribute equally and may degrade pose optimization.



Visual elements:


- Stable keypoints
- Unstable keypoints
- Pose drift



---

## Right: RA-KPA


Show:


Temporal reliability estimation.


Keypoints receive adaptive weights:


\[
w_i^t
\]


Reliable keypoints:

larger weights.


Unreliable keypoints:

smaller weights.



Result:


More stable pose estimation.



---

# Figure 2

## RA-KPA Framework Overview



## Pipeline



Input frames

↓

Keypoint tracking

↓

Temporal Reliability Estimation

↓

Adaptive Weight Generation

↓

Reliability-guided Optimization

↓

Articulated Pose Output



## Highlighted Modules


Module 1:

Temporal Keypoint Reliability Estimation



Module 2:

Adaptive Weight Update



Module 3:

Reliability-guided Pose Optimization



---

# Figure 3

## Keypoint Reliability Analysis



## Purpose


Validate the motivation that keypoints have different reliability levels.



## Subfigures



### (a)

Keypoint residual distribution



Show:

kp0-kp3 residual statistics.



### (b)

Temporal residual variation



Show:

residual change across frames.



### (c)

Motion / reliability correlation



Show:

relationship between keypoint behavior and tracking quality.



---

# Figure 4

## Online Adaptive Weight Evolution



## Purpose


Demonstrate that RA-KPA dynamically updates keypoint reliability.



## Data Source


online_weight_history.npy



## Subfigures



### (a)

Weight evolution curve


x-axis:

Frame


y-axis:

Adaptive weight



Show:

kp0

kp1

kp2

kp3



### (b)

Mean and variance


Show:

average reliability differences.



---

# Figure 5

## Quantitative Comparison



## Table Instead of Figure


Methods:


Baseline

Fixed Weight

Offline Weight

RA-KPA



Metrics:


Rotation Error

Translation Error

Joint Error



---

# Figure 6

## Qualitative Failure Recovery



## Purpose


Explain why adaptive reliability improves robustness.



## Layout


Three columns:



Input Observation



Baseline Tracking



RA-KPA Tracking



Additional visualization:


keypoint weight change over time.



---

# Figure Generation Priority


## Priority 1


Figure 2:

Method Overview



## Priority 2


Figure 1:

Motivation



## Priority 3


Figure 4:

Online Weight Visualization



## Priority 4


Figure 3:

Reliability Analysis



## Priority 5


Figure 6:

Failure Cases



---

# Current Data Availability


Available:


- keypoint trajectory history
- optimization residual history
- online weight history
- per-frame tracking results



Need:


- qualitative screenshots
- baseline comparison
- final paper-style plots



---

# Final Paper Figure Sequence


Figure 1:

Why reliability matters.



Figure 2:

How RA-KPA works.



Figure 3:

Evidence that reliability varies.



Figure 4:

Online adaptation behavior.



Figure 5:

Quantitative comparison.



Figure 6:

Robustness visualization.
