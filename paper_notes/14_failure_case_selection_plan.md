# RA-KPA Failure Case Selection Plan


# 1. Purpose


The purpose of failure case analysis is to provide qualitative evidence that RA-KPA improves robustness under unreliable keypoint observations.


The selected example should demonstrate:


1. Keypoint reliability degradation.
2. Failure of uniform keypoint optimization.
3. Adaptive reliability adjustment.
4. Recovery of articulated pose tracking.



---

# 2. Selection Principle


A useful qualitative example should not simply contain the largest tracking error.


Instead, it should satisfy:


\[
\text{Failure Case Quality}
=
\text{Baseline Failure}
+
\text{RA-KPA Recovery}
+
\text{Reliability Adaptation Evidence}
\]



---

# 3. Selection Criteria


## Criterion 1

## Large Baseline Error


The selected frame should have significant tracking difficulty.


Candidate metrics:


- child rotation error
- articulation error
- keypoint residual



Example:


\[
E_{baseline}^{child}
\gg 0
\]



---

## Criterion 2

## Large Improvement After RA-KPA


The selected frame should show clear improvement:


\[
\Delta E
=
E_{baseline}
-
E_{RA-KPA}
\]


Large improvement indicates that adaptive reliability weighting contributes to recovery.



---

## Criterion 3

## Significant Weight Adaptation


The selected frame should contain meaningful weight changes.



Example:


Before:


\[
w=[1,1,1,1]
\]


After adaptation:


\[
w=[1.2,0.8,1.15,0.85]
\]



This demonstrates that RA-KPA does not simply refine pose, but identifies unreliable constraints.



---

## Criterion 4

## Visual Interpretability


The selected sequence should clearly show:


- articulated motion
- keypoint instability
- pose drift
- recovery



Avoid selecting examples where:

- improvement is too small
- failure is invisible
- object motion is ambiguous



---

# 4. Candidate Ranking Strategy


For every frame:


Compute:


## Tracking degradation score


\[
S_f=
E_{baseline}
-
E_{RA-KPA}
\]


Higher:


better recovery example.



---

## Weight adaptation score


\[
S_w=
||w_t-\mathbf{1}||
\]


Higher:


stronger reliability adaptation.



---

## Final ranking


\[
Score
=
S_f
\times
S_w
\]


The highest ranked frames are inspected manually.



---

# 5. Required Data


## Per-frame Tracking Results


Source:



failure_analysis/results/per_frame_results.csv



Contains:


- frame id
- initial error
- optimized error
- keypoint residual statistics



---

## Weight History


Source:



failure_analysis/results/online_weight_history.npy



Contains:


\[
w_t
\]


for each frame.



---

## Keypoint Trajectory


Source:



failure_analysis/results/pred_child_kp_history.npy



Used for visualization.



---

# 6. Selection Script


Create:



failure_analysis/scripts/select_failure_case.py



The script should:


1. Load per-frame results.

2. Load online weights.

3. Compute improvement score.

4. Rank candidate frames.

5. Save:



failure_case_candidates.csv




---

# 7. Final Visualization


The selected case should become:


## Figure 6

Qualitative Tracking Comparison



Layout:


Three columns:


### Input Observation


Show RGB/depth frame and keypoints.



### Baseline


Show:

- incorrect pose
- keypoint drift
- wrong articulation



### RA-KPA


Show:

- adaptive weights
- corrected pose



---

# 8. Additional Visualization


For the selected sequence:


Include:


## Weight Change


Example:


kp0:

increase


kp1:

decrease



## Keypoint Residual


Show:


unreliable keypoint has reduced influence.



---

# 9. Paper Narrative


The qualitative example should support the statement:


"RA-KPA improves robustness by reducing the influence of temporarily unreliable keypoints rather than treating all keypoints equally."



---

# 10. Current Status


Available:


✓ per-frame tracking results

✓ keypoint trajectory history

✓ online weight history



Need:


- automatic candidate selection
- frame visualization
- final qualitative figure
