# RA-KPA Motivation Figure Design


## Figure Objective


Figure 1 introduces the fundamental problem addressed by RA-KPA.


The figure should convince readers that:


1. Keypoints are useful geometric constraints.

2. However, their reliability is not constant during temporal tracking.

3. Treating all keypoints equally may degrade pose estimation.

4. Adaptive reliability-aware optimization is required.



---

# Figure Title


Temporal Keypoint Reliability Variation in Articulated Tracking



---

# Main Message


Existing tracking methods assume:


\[
w_i = 1
\]


for all keypoints.


However, during tracking:


\[
w_i^t
\neq constant
\]


because keypoint reliability changes over time.



RA-KPA estimates reliability online and adapts keypoint contribution.



---

# Figure Layout


Use a three-stage horizontal layout.




Temporal Observation

    |

    v

Conventional Optimization

    |

    v

RA-KPA




---

# Stage 1

## Temporal Keypoint Observation


## Purpose


Show that reliability changes across frames.



Input:


A short tracking sequence:



Frame t-1

Frame t

Frame t+1



Each frame contains:


- articulated object pose
- detected keypoints



Example:


Frame t:


kp0: reliable

kp1: unreliable

kp2: reliable

kp3: uncertain



Frame t+1:


kp reliability changes.



Key visual:


The same keypoint can have different reliability at different times.



---

# Stage 2

## Conventional Uniform Keypoint Optimization



## Assumption


All keypoints contribute equally.



Optimization:


\[
w=[1,1,1,1]
\]



Problem:


Unreliable keypoints introduce incorrect constraints.



Visual:


Show one unreliable keypoint with:


- high residual
- incorrect pose influence
- drift direction



Message:


Uniform weighting ignores temporal reliability variation.



---

# Stage 3

## RA-KPA Adaptive Reliability Optimization



## Reliability Estimation


The system estimates:


\[
r_i^t
\]


from temporal observations.



Example:


kp0:

high reliability


kp1:

low reliability


kp2:

high reliability


kp3:

medium reliability



Convert to:


\[
w_i^t
\]



Example:


\[
[1.15,0.82,1.12,0.86]
\]



---

# Visual Comparison


## Existing Method


Keypoints:



kp0 kp1 kp2 kp3

1 1 1 1



All constraints have equal influence.



## RA-KPA


Keypoints:



kp0 kp1 kp2 kp3

1.15 0.82 1.12 0.86



Reliable constraints are emphasized.



---

# Required Annotations


The figure should include:



## Problem Annotation


"Temporal reliability variation"



## Existing Method Annotation


"Uniform keypoint contribution"



## Proposed Method Annotation


"Online reliability-aware adaptation"



---

# Data Source


Possible real examples:


- online_weight_history.npy
- per_frame_results.csv
- keypoint trajectory history



---

# Figure Style


Recommended style:


- clean CVPR style
- simple object illustration
- limited text
- clear arrows
- emphasize comparison


Avoid:


- implementation details
- code names
- debugging outputs



---

# Relation to PAGE


Difference:


PAGE focuses on improving keypoint generation and selection.


RA-KPA focuses on adapting the reliability of existing keypoints during temporal tracking.



The motivation figure should make this distinction visually clear.



---

# Future Implementation Steps


1. Select representative failure sequence.

2. Extract baseline failure frame.

3. Extract RA-KPA recovered frame.

4. Overlay keypoint reliability.

5. Draw final vector figure.



---

# Expected Figure Outcome


After viewing Figure 1, readers should understand:


"Keypoints are not equally reliable over time, therefore tracking systems should adapt their contribution dynamically."