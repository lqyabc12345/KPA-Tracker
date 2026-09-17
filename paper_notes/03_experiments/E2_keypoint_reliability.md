# E2 Keypoint Geometric Reliability Analysis


# 1. Motivation


The temporal analysis in E1 shows that keyframe distance affects
tracking performance.

However, temporal distance alone cannot fully explain tracking failures.

Frames with similar keyframe distances may still exhibit different
articulation estimation errors.


This experiment investigates whether the quality of predicted
keypoints provides a stronger explanation of tracking failure.



---

# 2. Hypothesis


We hypothesize:


> Keypoint geometric inconsistency before optimization is strongly
> correlated with final articulation tracking error.


The assumption is:


larger keypoint residual

↓

less reliable geometric constraint

↓

larger optimization error



---

# 3. Experimental Setup


## Dataset


Dataset:
# E2 Keypoint Geometric Reliability Analysis


# 1. Motivation


The temporal analysis in E1 shows that keyframe distance affects
tracking performance.

However, temporal distance alone cannot fully explain tracking failures.

Frames with similar keyframe distances may still exhibit different
articulation estimation errors.


This experiment investigates whether the quality of predicted
keypoints provides a stronger explanation of tracking failure.



---

# 2. Hypothesis


We hypothesize:


> Keypoint geometric inconsistency before optimization is strongly
> correlated with final articulation tracking error.


The assumption is:


larger keypoint residual

↓

less reliable geometric constraint

↓

larger optimization error



---

# 3. Experimental Setup


## Dataset


Dataset:


dataset1



Object:


laptop



Frames:


377



Model:


num_parts = 2

num_kp = 8



For child part:


4 keypoints




---

# 4. Data Collection


During tracking, the following quantities are recorded:


## Pre-optimization keypoint residual


Before geometric refinement:


child_kp_pre_residual



This represents the initial inconsistency between predicted
keypoints and the articulated model.


Statistics:

- mean residual
- maximum residual
- residual variance



## Tracking error


Target metric:



new_child_r



Child part rotation error after optimization.



---

# 5. Implementation


Generated files:



failure_analysis/results/per_frame_results.csv



Important columns:



child_kp_pre_res_mean

child_kp_pre_res_max

child_kp_pre_res_std

new_child_r




Analysis script:



failure_analysis/scripts/analyze_e2_reliability.py




The script computes:

- Pearson correlation
- Spearman correlation



---

# 6. Results


## Mean keypoint residual


Correlation with child rotation error:


Pearson:



0.5724



Spearman:



0.5345




---

## Maximum keypoint residual


Pearson:



0.5329




Spearman:



0.4953




---

## Residual variation


Residual standard deviation:


Pearson:



0.4718




Spearman:



0.4389




---

# 7. Comparison with Temporal Distance


E1:


key_dis vs tracking error:



Pearson = 0.3558

Spearman = 0.3360




E2:


mean keypoint residual vs tracking error:



Pearson = 0.5724

Spearman = 0.5345




Keypoint residual provides a stronger correlation signal.



---

# 8. Non-keyframe Analysis


To exclude the influence of keyframe initialization,
only non-keyframes are evaluated:


Condition:



key_dis > 0




Results:


Mean residual:



Pearson = 0.5180

Spearman = 0.4829




The correlation remains significant.



---

# 9. Analysis


The experiment demonstrates that keypoint geometric quality is a
major factor affecting articulated tracking performance.


Compared with temporal distance, keypoint residual provides a
stronger indicator of failure.


This suggests that:

- tracking failure is related to observation quality;
- keypoints should not be treated as equally reliable constraints.



---

# 10. Limitations


Keypoint residual alone does not describe the complete usefulness of
a keypoint.


A keypoint may have:

- low residual but limited articulation information;
- high motion sensitivity but unstable geometry.


Therefore, additional analysis is required to study
keypoint-specific reliability and motion characteristics.



---

# 11. Impact on Method Design


E2 provides the first evidence for reliability-aware optimization:


> Keypoint contribution should depend on observation quality rather
> than uniform weighting.


This motivates:

- per-keypoint reliability estimation;
- adaptive optimization weighting.


Further experiments E3-E10 analyze different aspects of keypoint
reliability.