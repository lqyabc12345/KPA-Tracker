# Failure Analysis Findings Summary


## Overview

This document summarizes the major observations discovered from
failure analysis experiments of KPA-Tracker.

The goal is to understand:

1. why keypoint-based articulated tracking fails;
2. which factors contribute to failure;
3. how these observations motivate a reliability-aware tracking method.


The analysis is conducted on:

- Dataset: dataset1
- Object category: laptop
- Number of frames: 377
- Number of parts: 2
- Number of keypoints: 8
- Child keypoints used for analysis: 4


---

# Finding 1: Temporal propagation affects tracking accuracy,
but cannot fully explain failures


## Observation

The temporal distance from the previous keyframe (`key_dis`)
shows positive correlation with articulation tracking error.


Metric:

Target:


new_child_r



Correlation:


Pearson:
0.3558

Spearman:
0.3360



## Interpretation

Longer temporal propagation increases tracking difficulty.

However, the correlation strength indicates that temporal distance
alone is insufficient to explain failure cases.

Frames with similar temporal distance can still show very different
tracking accuracy.


## Implication

Additional factors related to keypoint quality should be investigated.



---

# Finding 2: Keypoint geometric residual is a strong failure indicator


## Observation

The initial keypoint fitting residual before optimization
(`child_kp_pre_res_mean`) has strong correlation with tracking error.


Results:



Pearson:
0.5724

Spearman:
0.5345



Other residual statistics also show positive correlation:

- maximum residual:


Pearson = 0.5329



- residual standard deviation:


Pearson = 0.4718



## Interpretation

Frames with larger keypoint geometric inconsistency are more likely
to produce inaccurate articulation estimation.


Compared with temporal distance, keypoint residual provides a stronger
signal of failure.


## Implication

Keypoint reliability should be considered during optimization.



---

# Finding 3: Keypoint reliability is non-uniform


## Observation

Different keypoints show different relationships with tracking failure.


Per-keypoint analysis:


| Keypoint | Pearson correlation |
|---|---|
| kp0 | 0.5303 |
| kp1 | 0.7181 |
| kp2 | 0.5233 |
| kp3 | 0.5247 |


## Interpretation

Although all keypoints contribute geometric constraints,
their reliability is not equivalent.

Some keypoints are more strongly associated with tracking failures.


In particular:


kp1


shows the strongest correlation with articulation error.



## Implication

Uniform keypoint weighting may be suboptimal.



---

# Finding 4: Keypoint reliability contains multiple factors


## Motivation

A keypoint should not only be geometrically stable,
but should also provide useful articulation information.


Therefore, both:

- geometric reliability
- motion-related observability

are investigated.


---

## Geometric reliability


Measured by:


child_kp_pre_residual



Higher residual indicates unreliable keypoint observation.



---

## Motion-related consistency


E9 and E10 analyze:

1. predicted child keypoint trajectory:


pred_child_kp_history.npy



2. optimized articulation state trajectory:


optimized_joint_state_history.npy



The optimized joint state represents the articulation state
recovered by geometric refinement.



---

# Finding 5: Different keypoints have different motion characteristics


## Observation


Keypoint motion magnitude:



kp0:
mean = 0.2292

kp1:
mean = 0.1845

kp2:
mean = 0.2286

kp3:
mean = 0.1851



Two groups appear:


High-motion group:


kp0, kp2



Low-motion group:


kp1, kp3



---

## Motion consistency with optimized articulation


Correlation between keypoint motion and optimized joint state change:


| Keypoint | Pearson |
|-|-|
| kp0 | 0.6814 |
| kp1 | 0.3797 |
| kp2 | 0.6665 |
| kp3 | 0.3681 |


## Interpretation

kp0 and kp2 exhibit stronger consistency with recovered articulation
motion.


This indicates that keypoint usefulness depends not only on residual
magnitude, but also on articulation-related motion information.



---

# Overall Findings


The failure analysis reveals three important characteristics:


## 1. Temporal degradation exists

Increasing keyframe distance increases tracking difficulty.

However, temporal distance alone cannot predict failure.



## 2. Keypoint reliability is uneven

Different keypoints provide different quality constraints.

Treating all keypoints equally may introduce optimization bias.



## 3. Keypoint usefulness is multi-dimensional

A reliable keypoint should consider:


- geometric consistency
- temporal stability
- articulation observability


These findings motivate the development of:

> an adaptive keypoint reliability-aware optimization strategy.



---

# Next Step


Based on these observations, the next stage is to design
and evaluate an adaptive weighting mechanism:

Input:

- keypoint residual
- keypoint reliability
- articulation-related motion information


Output:

- adaptive keypoint weights


Evaluation:

Compare against uniform keypoint optimization.