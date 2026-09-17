# Method Validation


## 1. Purpose


Previous failure analysis demonstrates that keypoints have different
levels of reliability.

Based on these observations, a reliability-aware keypoint optimization
method is proposed.


This section describes the experimental protocol used to validate
whether adaptive keypoint weighting improves articulated tracking.



---

# 2. Validation Questions


The experiments are designed to answer three questions.


## Q1: Does reliability-aware weighting improve tracking accuracy?


The proposed method is compared with the original uniform keypoint
optimization.


## Q2: Which reliability component contributes to the improvement?


Different reliability factors are removed or replaced to analyze their
effect.


## Q3: Does the method improve robustness under difficult tracking
conditions?


The performance under large temporal distance and challenging
articulation states is evaluated.



---

# 3. Baseline Method


The baseline follows the original KPA optimization formulation.


All keypoints contribute equally:


\[
L_{base}
=
\sum_i ||k_i-\hat{k_i}||
\]


where every keypoint has:


\[
w_i=1
\]


This baseline represents uniform keypoint optimization.



---

# 4. Proposed Method


The proposed method introduces adaptive keypoint weighting:


\[
L_{ours}
=
\sum_i w_i||k_i-\hat{k_i}||
\]


where:


\[
w_i
\]


is calculated from keypoint reliability.


The reliability score considers:


1. geometric consistency;

2. temporal stability;

3. articulation observability.



---

# 5. Evaluation Metrics


The following metrics are used.


## 5.1 Rotation Error


The difference between predicted and ground-truth rotation:


\[
E_R
\]


is measured in degrees.



## 5.2 Translation Error


The translation difference:


\[
E_T
\]


is measured in meters.



## 5.3 Tracking Failure Rate


Frames exceeding predefined error thresholds are counted as failures.



---

# 6. Experimental Comparisons


The following variants are evaluated.


## Baseline


Uniform keypoint optimization.



w_i = 1



---

## Residual-aware weighting


Only geometric reliability is used.



w_i=f(g_i)



---

## Motion-aware weighting


Only articulation relevance is used.



w_i=f(m_i)



---

## Stability-aware weighting


Only temporal consistency is used.



w_i=f(s_i)



---

## Full reliability-aware weighting


All reliability factors are combined:



w_i=f(g_i,s_i,m_i)




---

# 7. Ablation Design


To understand each component contribution, the following ablations
are performed.


| Variant | Geometry | Stability | Motion |
|---|---|---|---|
| baseline | ✗ | ✗ | ✗ |
| A | ✓ | ✗ | ✗ |
| B | ✗ | ✓ | ✗ |
| C | ✗ | ✗ | ✓ |
| Full | ✓ | ✓ | ✓ |



---

# 8. Robustness Evaluation


The method is further evaluated under challenging conditions:


## Temporal distance


Frames with larger keyframe distance are analyzed.


## Articulation motion


Different joint configurations are evaluated.


## Failure cases


Frames with large tracking errors are inspected.



---

# 9. Expected Outcome


The proposed method is expected to:


1. reduce rotation and translation errors;

2. decrease tracking failure rate;

3. provide more robust optimization under difficult conditions.



---

# 10. Connection to Results


The quantitative comparisons and ablation results are reported in the
following Results section.