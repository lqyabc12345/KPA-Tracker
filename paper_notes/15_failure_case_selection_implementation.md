# RA-KPA Failure Case Selection Implementation


## Purpose


Automatically select representative tracking failure cases for:


- Figure 1 motivation
- Figure 6 qualitative comparison



The selected cases should demonstrate:


1. Baseline tracking degradation.

2. RA-KPA recovery.

3. Significant adaptive weight change.



---

# 1. Input Data


## Tracking Results


File:



failure_analysis/results/per_frame_results.csv



Contains:


- frame index
- baseline tracking error
- optimized tracking error
- keypoint residual statistics



---

## Online Weight History


File:



failure_analysis/results/online_weight_history.npy



Shape:


\[
T \times N_{kp}
\]


where:


T:

number of frames


Nkp:

number of keypoints



---

# 2. Candidate Score


Each frame receives:


\[
Score_f
=
S_e
\times
S_w
\]


---

# 3. Error Improvement Score


Define:


\[
S_e
=
E_{baseline}
-
E_{RA-KPA}
\]


Large value:


strong recovery.



---

# 4. Weight Adaptation Score


Define:


\[
S_w
=
||w_t-\mathbf 1||
\]


Large value:


strong reliability adaptation.



---

# 5. Final Ranking


Sort:


descending score



Output:



failure_case_candidates.csv



Example:



frame_id,
baseline_error,
ours_error,
improvement,
weight_change,
score




---

# 6. Manual Verification


After ranking:


Inspect top candidates.


Check:


- visible pose drift
- articulation error
- keypoint instability
- recovery quality



---

# 7. Visualization Preparation


For selected frame:


Prepare:


## Input


Original observation.



## Baseline


Uniform weighting result.



## RA-KPA


Adaptive weighting result.



## Additional


Weight vector:


\[
w_t
\]


---

# 8. Expected Paper Usage


The selected case supports:



Figure 1:

Motivation example.



Figure 6:

Qualitative robustness comparison.



---

# 9. Implementation Notes


Important:


The selected frame should not only have large error.


It must contain:


\[
\text{Failure}
+
\text{Recovery}
+
\text{Adaptation}
\]


otherwise the qualitative result is weak.


---

# Current Status


Available:


✓ tracking results

✓ weight history

✓ keypoint trajectory


Next:


Implement:



select_failure_case.py



Generate:



failure_case_candidates.csv