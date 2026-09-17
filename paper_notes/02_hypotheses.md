# Research Hypotheses


## Overview

This project investigates the failure mechanism of keypoint-based
articulated object tracking.

The initial observation is that tracking accuracy decreases during
longer temporal propagation. However, temporal distance alone cannot
fully explain failure cases.

Therefore, we analyze whether failures are caused by different
keypoint reliability and geometric constraints.

The research follows:

Temporal degradation
        |
        v
Keypoint reliability
        |
        v
Keypoint influence
        |
        v
Adaptive weighting method



---

# H1: Temporal distance causes tracking degradation


## Motivation

KPA tracking relies on temporal propagation between keyframes.

As the distance from the previous keyframe increases, predicted
keypoints and estimated articulation states may become inaccurate.


## Hypothesis

Larger temporal distance leads to larger tracking error.


## Evaluation

Metric:

- key_dis
- new_child_r


Analysis:

Pearson correlation:

0.3558

Spearman correlation:

0.3360


## Conclusion

Supported.

Temporal distance contributes to tracking degradation.

However, the correlation strength indicates that temporal distance
alone cannot fully explain failure.



---

# H2: Keypoint geometric reliability explains tracking failures


## Motivation

Different keypoints may provide different geometric constraints.

Unreliable keypoints can introduce incorrect optimization gradients
and bias articulation estimation.


## Hypothesis

Keypoint residual before optimization is correlated with tracking error.


## Evaluation

Metrics:

- child_kp_pre_res_mean
- child_kp_pre_res_max
- child_kp_pre_res_std

Target:

- new_child_r


Results:

Mean residual:

Pearson:

0.5724


Spearman:

0.5345


Max residual:

Pearson:

0.5329


Std residual:

Pearson:

0.4718



## Conclusion

Strongly supported.

Keypoint geometric inconsistency provides stronger failure prediction
than temporal distance.



---

# H3: Different keypoints have different reliability


## Motivation

Current KPA optimization treats keypoints equally.

However, different keypoints may have different stability,
visibility and articulation sensitivity.


## Hypothesis

Individual keypoints contribute differently to tracking failure.


## Evaluation


Per-keypoint correlation:

kp0:

Pearson = 0.5303


kp1:

Pearson = 0.7181


kp2:

Pearson = 0.5233


kp3:

Pearson = 0.5247



## Conclusion

Supported.

Keypoint reliability is highly non-uniform.

In particular, kp1 shows stronger correlation with tracking error.



---

# H4: Keypoint reliability can be characterized through motion and geometry


## Motivation

Residual magnitude alone may not fully describe keypoint usefulness.

A useful keypoint should:

1. remain geometrically stable
2. contain articulation-related motion information


## Evidence


Temporal reliability:

E9:

predicted keypoint trajectory variance was analyzed.


Motion consistency:

E10:

keypoint motion was compared with optimized articulation states.


Results:

kp0 and kp2:

higher motion correlation


kp1 and kp3:

lower motion magnitude but strong residual correlation



## Conclusion

Partially supported.

Keypoint reliability contains multiple factors:

- geometric consistency
- temporal stability
- articulation observability



---

# H5: Reliability-aware keypoint weighting improves tracking


## Motivation

Since keypoint reliability is non-uniform,
uniform optimization weights may not be optimal.


## Hypothesis

Adaptive keypoint weighting based on reliability estimation
can improve articulated tracking robustness.


## Status

To be evaluated in E11.
