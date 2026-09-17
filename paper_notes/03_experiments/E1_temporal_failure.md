# E1 Temporal Failure Analysis


## 1. Motivation


Keypoint-based articulated tracking relies on temporal propagation
between keyframes.

When the current frame is far from the previous keyframe,
the accumulated prediction error may increase.

However, the relationship between temporal distance and tracking
failure has not been quantitatively studied.


This experiment investigates whether temporal propagation distance
is a factor contributing to tracking degradation.



---

# 2. Hypothesis


We hypothesize:


> Larger temporal distance from the previous keyframe leads to larger
> articulation tracking error.



The hypothesis is:

\[
key\_dis \uparrow
\Rightarrow
error \uparrow
\]



---

# 3. Experimental Setup


## Dataset


Dataset:


dataset1



Object category:


laptop



Number of frames:


377



Model configuration:


num_parts = 2

num_kp = 8

child keypoints = 4




---

## Variables


### Independent variable


Temporal distance:



key_dis



Definition:

Number of frames after the latest keyframe.



---

### Dependent variable


Articulation tracking error:



new_child_r



Rotation error of child part after optimization.



---

# 4. Implementation


The experiment uses:


failure_analysis/results/results.csv

failure_analysis/results/per_frame_results.csv



Analysis script:



failure_analysis/scripts/analyze_e1_*.py



The pipeline computes:

- Pearson correlation
- Spearman correlation
- failure statistics by keyframe distance



---

# 5. Results


## Correlation between key distance and tracking error


Pearson correlation:



r = 0.3558



Spearman correlation:



rho = 0.3360




Both correlations are statistically significant.



---

# 6. Analysis


The results demonstrate that temporal propagation distance
is positively correlated with tracking degradation.


As keyframe distance increases, the child articulation error
tends to increase.



However, the correlation strength is moderate.

This indicates that temporal distance alone cannot fully explain
tracking failures.



Frames with the same keyframe distance can still have very different
tracking performance.



---

# 7. Limitation


Although temporal distance provides a useful indicator,
it does not describe the quality of keypoint observations.


A frame may fail even with a small temporal distance if the predicted
keypoints provide inaccurate geometric constraints.



Therefore, additional keypoint-level analysis is required.



---

# 8. Impact on Method Design


E1 provides the first observation:


> Temporal propagation contributes to failure, but is insufficient
> as a failure predictor.



This motivates the following investigation:


- Are failures related to keypoint reliability?
- Do different keypoints provide different quality constraints?



These questions are studied in E2-E8.