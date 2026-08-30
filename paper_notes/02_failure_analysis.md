# 02_failure_analysis.md

# Failure Analysis

## Purpose
The goal is not only to measure average performance, but to identify when and why KPA-Tracker fails.

## Logged per-frame variables

sample_id
frame_id
key_dis
urdf_id
num_points
num_kp

ini_base_r
ini_child_r
ini_base_t
ini_child_t

new_base_r
new_child_r
new_base_t
new_child_t

cam_base_r
cam_child_r
cam_base_t
cam_child_t

## Current diagnostic setup

Category: laptop
num_points = 1024
num_kp = 8
Random seed = 0

Initial diagnostic run:
30 frames

## Observation 1: Refinement strongly improves child rotation

In the 30-frame run:

Mean initial child rotation error:
87.79°

Mean refined child rotation error:
14.30°

This shows that the refinement / optimization stage is essential.

However, large initial error does not always lead to large final error.

Examples:
- ini_child_r ≈ 158.94°, new_child_r ≈ 5.13°
- ini_child_r ≈ 177.96°, new_child_r ≈ 36.19°

Therefore:

Large initial error is not sufficient to explain final tracking failure.

## Observation 2: Catastrophic failure frames exist

Top refined child rotation failures:

frame 15: 38.31°
frame 14: 36.19°
frame 20: 30.04°
frame 13: 21.17°
frame 25: 20.22°

The refined error distribution is not uniform.
There are several strong failure peaks.

## Observation 3: Frame index has only weak positive correlation

Pearson correlation:

frame_id vs new_child_r:
r = 0.347

Interpretation:
There is a weak-to-moderate increasing trend over time, but frame index alone does not explain the failures.

Conclusion:
Simple temporal drift is not sufficient as the only explanation.

## Observation 4: Distance to keyframe is more strongly correlated with error

Statistics:

key_dis = 0
mean = 0.0169°

key_dis = 1
mean = 10.93°

key_dis = 2
mean = 11.33°

key_dis = 3
mean = 14.10°

key_dis = 4
mean = 18.36°

key_dis = 5
mean = 23.82°

Pearson correlation:

key_dis vs new_child_r:
r = 0.638

Interpretation:
Tracking error increases noticeably as the distance to the current keyframe increases.

This suggests that the fixed keyframe update strategy may not adapt well to varying tracking reliability.

## Current limitation

Only 30 frames have been analyzed.

The current result is preliminary evidence, not a final conclusion.

Next:
Run the full 377-frame validation set and check whether the same trend holds across multiple objects / sequences.



## E1: Full Baseline Failure Analysis

### Research Question

Does KPA-Tracker become less reliable as the current frame moves farther
away from the latest keyframe?

The main variable used for this analysis is:

`key_dis`

which represents the distance from the current frame to the current
keyframe / reference update.

The main tracking error considered in this analysis is:

`new_child_r`

which is the refined child rotation error.

### Observation 1: Refinement substantially reduces child rotation error

Across the 377-frame run:

- Mean initial child rotation error: 86.19°
- Mean refined child rotation error: 14.37°
- Median refined child rotation error: 12.52°

This indicates that the refinement stage is essential for recovering
from poor initial child rotation predictions.

However, refinement does not always succeed.

The maximum refined child rotation error reaches:

54.08°

Therefore, the main failure-analysis question is not simply whether
the initial prediction is inaccurate, but why some inaccurate predictions
can be successfully refined while others remain large failures.

### Observation 2: Tracking error increases with keyframe distance

The refined child rotation error shows a positive relationship with
`key_dis`.

Correlation results:

- Pearson r = 0.356
- Spearman rho = 0.336
- Spearman p = 2.10e-11

The mean refined child rotation error increases from:

- 12.25° at `key_dis = 1`
- to 18.65° at `key_dis = 5`

The median error shows the same overall increasing tendency,
although it is not strictly monotonic for every intermediate key distance.

This suggests that tracking becomes less reliable as the current frame
moves farther away from the latest keyframe.

### Observation 3: Severe failures become more frequent at larger keyframe distances

The failure-rate analysis reveals a clearer trend for large errors.

For refined child rotation error > 20°:

- key_dis = 1: 7.69%
- key_dis = 2: 12.82%
- key_dis = 3: 23.08%
- key_dis = 4: 24.62%
- key_dis = 5: 40.00%

For refined child rotation error > 30°:

- key_dis = 1: 1.28%
- key_dis = 2: 3.85%
- key_dis = 3: 7.69%
- key_dis = 4: 9.23%
- key_dis = 5: 13.85%

Unlike the >10° threshold, the >20° and >30° failure rates increase
consistently with keyframe distance.

This indicates that increasing keyframe distance is associated not only
with a higher average error, but also with a higher probability of
catastrophic tracking failures.

### Observation 4: The largest failures are concentrated at larger keyframe distances

Among the top five refined child rotation failures:

- sample 189: key_dis = 5, error = 54.08°
- sample 188: key_dis = 4, error = 47.41°
- sample 194: key_dis = 5, error = 45.19°
- sample 187: key_dis = 3, error = 45.01°
- sample 286: key_dis = 5, error = 42.43°

Four of the top five failure cases occur at `key_dis >= 4`.

This provides additional evidence that severe tracking failures tend
to occur farther from the latest keyframe.


## What E1 Does Not Prove

E1 shows correlation, not causality.

The current experiment does not prove that large `key_dis` itself
causes tracking failure.

Possible confounding factors include:

1. accumulated pose error,
2. increasing motion magnitude,
3. more difficult observations,
4. degraded keypoint quality,
5. view changes or partial observations,
6. the fixed keyframe update mechanism itself.

Therefore, the causal mechanism behind the observed degradation
still needs to be investigated.


## Important Data Issue

The dataset loader reports:

5 objects

but the current per-frame results contain only:

1 unique URDF ID: 10040

Therefore, E1 cannot currently support claims about cross-object
generalization.

This issue must be investigated before using the result as final
paper evidence.

## Current Interpretation

E1 provides preliminary full-run evidence that KPA-Tracker becomes
less reliable as the distance to the latest keyframe increases.

The evidence includes:

1. positive Pearson and Spearman correlations,
2. increasing mean tracking error with `key_dis`,
3. increasing severe-failure rates at >20° and >30°,
4. concentration of top failure cases at larger `key_dis`.

However, the observed correlation is moderate rather than strong:

Pearson r = 0.356.

Therefore, keyframe distance is likely one contributing factor,
but not the only factor determining tracking failure.

The next research question is:

> What reliability signal explains why some frames can still be
> refined successfully while other frames become catastrophic failures?

A key candidate is keypoint reliability / uncertainty.