# RA-KPA Failure Case Visualization Design


# 1. Objective


The purpose of the failure case visualization is to provide qualitative evidence that RA-KPA improves robustness by adapting keypoint reliability.


The figure should demonstrate:


1. Uniform weighting fails under unreliable keypoint observations.

2. RA-KPA suppresses unreliable constraints.

3. Adaptive weighting improves articulated pose tracking.



---

# 2. Selected Example


Current selected frame:



Frame 282



Statistics:


Initial child rotation error:


\[
167.679^\circ
\]


After RA-KPA:


\[
15.793^\circ
\]


Improvement:


\[
151.886^\circ
\]


Weight adaptation magnitude:


\[
0.7115
\]



---

# 3. Figure Message


The figure should communicate:


"During challenging articulated motion, some keypoints become unreliable. Uniform optimization treats all observations equally, while RA-KPA dynamically adjusts their contribution and recovers stable tracking."



---

# 4. Figure Layout


Recommended layout:



Input Observation

    |

    v

Uniform Optimization

    |

    v

RA-KPA Optimization

    |

    v

Reliability Evidence



---

# 5. Component Design


## Part A

## Input Observation


Show:


- object observation
- keypoint locations
- articulated state


Purpose:


Show challenging tracking condition.



---

# Part B

## Baseline Optimization


Show:


Uniform weights:


\[
w_i=1
\]


Visualization:


- unstable keypoint influence
- tracking drift
- high rotation error



Annotation:


"All keypoints contribute equally"



---

# Part C

## RA-KPA Result


Show:


Adaptive weights:


\[
w_i^t
\]


Visualization:


- reliable keypoints emphasized
- unreliable keypoints reduced


Annotation:


"Reliability-aware keypoint adaptation"



---

# Part D

## Quantitative Evidence


Include:


## Weight Vector


Example:


\[
w_t=
[w_0,w_1,...]
\]


Show:


different keypoint importance.



## Error Comparison


Example:



Uniform:

167.7 deg

RA-KPA:

15.8 deg




---

# 6. Required Data


## Tracking Result


Source:



per_frame_results.csv



Used for:


- error comparison
- frame selection



---

## Weight History


Source:



online_weight_history.npy



Used for:


- adaptive weight visualization



---

## Keypoint History


Source:



pred_child_kp_history.npy



Used for:


- keypoint trajectory visualization



---

# 7. Visualization Script


Future script:



failure_analysis/scripts/visualize_failure_case.py



Function:


1. Load selected frame.

2. Load keypoint history.

3. Load adaptive weight.

4. Generate publication-quality figure.



Output:



failure_analysis/results/failure_case_282.png




---

# 8. Paper Usage


This visualization can support:


## Figure 6

Qualitative Failure Recovery



## Figure 1

Motivation example


The same example can be simplified for motivation.



---

# 9. Future Improvement


For a stronger qualitative figure:


Modify tracker to save:


- baseline pose
- optimized pose
- keypoint confidence


Then generate:


baseline vs RA-KPA overlay.



---

# Current Status


Completed:


✓ failure case selection

✓ quantitative evidence


Next:


Implement visualization script.