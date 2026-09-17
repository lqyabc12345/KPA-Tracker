# From Failure Analysis to Method Design


## Overview

The failure analysis reveals that articulated tracking failure is not
caused by a single factor.

Instead, failure is related to:

1. temporal uncertainty;
2. keypoint geometric reliability;
3. keypoint-specific contribution;
4. articulation-related motion information.


These observations motivate a reliability-aware keypoint optimization
strategy.



---

# 1. Limitation of Current Uniform Keypoint Optimization


## Current formulation


The existing KPA optimization treats all predicted keypoints equally.


Given keypoints:

\[
K=\{k_1,k_2,...,k_N\}
\]


The optimization objective assumes:


\[
L=
\sum_i ||k_i-\hat{k_i}||
\]


where every keypoint has identical contribution.


---

## Problem


The failure analysis shows that this assumption is inaccurate.


Different keypoints exhibit different:


- geometric consistency;
- temporal stability;
- articulation relevance.



Therefore, unreliable keypoints may introduce incorrect optimization
constraints.



---

# 2. Observation 1: Keypoint Residual Indicates Reliability


## Evidence


E2 shows that pre-optimization keypoint residual strongly correlates
with tracking failure.


Mean residual:


Pearson:

0.5724


Spearman:

0.5345



## Interpretation


A large keypoint residual indicates that the predicted keypoint
constraint is unreliable.


Therefore, residual magnitude can be used as a reliability signal.



---

# 3. Observation 2: Reliability Is Keypoint Specific


## Evidence


E3 shows different keypoints have different failure correlation.


Example:


kp1:

Pearson:

0.7181



Other keypoints:

approximately:

0.52



## Interpretation


Different keypoints provide different quality of geometric constraints.


Therefore, assigning identical weights to all keypoints is suboptimal.



---

# 4. Observation 3: Keypoint Motion Contains Articulation Information


## Evidence


E10 analyzes the relationship between keypoint motion and
optimizer-recovered articulation state.


Keypoint motion correlation:


| Keypoint | Pearson |
|-|-|
| kp0 | 0.6814 |
| kp1 | 0.3797 |
| kp2 | 0.6665 |
| kp3 | 0.3681 |



## Interpretation


Some keypoints are more consistent with articulation state changes.


Therefore, reliability should not only consider geometric residual,
but also articulation-related information.



---

# 5. Method Motivation


Based on these observations, we hypothesize:


A keypoint confidence model should combine multiple signals:


## Geometric reliability


Derived from:

\[
r_i = ||e_i||
\]


where:

- \(e_i\) is keypoint fitting residual.



---

## Motion consistency


Derived from:


\[
m_i
\]


which measures the relationship between keypoint trajectory and
recovered articulation motion.



---

## Final reliability estimation


A confidence score can be constructed as:


\[
w_i=f(r_i,m_i)
\]


and incorporated into optimization:


\[
L=
\sum_i w_i||k_i-\hat{k_i}||
\]



---

# 6. Planned Evaluation


The proposed reliability-aware optimization will be compared with:

## Baseline

Uniform keypoint weighting:


\[
w_i=1
\]


## Proposed

Adaptive keypoint weighting:


\[
w_i=f(r_i,m_i)
\]


Evaluation metrics:

- articulation rotation error
- articulation translation error
- failure rate
- robustness under temporal propagation



---

# Summary


Failure analysis leads to the following design principle:


> Keypoints should not be treated equally.
> Their contribution should be dynamically adjusted according to
> geometric reliability and articulation-related information.


This motivates the development of an adaptive keypoint-aware
optimization method.
