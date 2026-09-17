# E9 Temporal Keypoint Stability Analysis


## 1. Motivation


Previous experiments demonstrate that different keypoints provide
different levels of reliability.

However, reliability is not only determined by instantaneous
geometric accuracy.

A keypoint may have small prediction error while exhibiting unstable
temporal behavior during tracking.


Therefore, this experiment investigates the temporal stability of
articulated keypoints over a tracking sequence.



---

# 2. Objective


The objective of E9 is to answer:


> Do different keypoints exhibit different temporal stability
> characteristics?


Specifically, we analyze whether keypoint trajectory variation
provides additional information for reliability modeling.



---

# 3. Data Representation


The optimized child keypoint trajectories are recorded during tracking:



pred_child_kp_history.npy



The stored trajectory has the dimension:



(number of frames, number of keypoints, 3D coordinates)

(377, 4, 3)



where each keypoint represents the predicted child-part articulation
constraint.



---

# 4. Temporal Variance Analysis


For each keypoint, temporal trajectory variance is calculated.


The results are:



kp0:
0.06685

kp1:
0.03789

kp2:
0.06733

kp3:
0.03801



Two different stability patterns are observed.


High-variation group:



kp0, kp2



Low-variation group:



kp1, kp3



This indicates that keypoints do not exhibit identical temporal
behavior during articulated motion.



---

# 5. Relationship with Tracking Error


The correlation between temporal instability and tracking error is
further analyzed.


The obtained correlations are:



Pearson:
0.1617

Spearman:
0.1556



Although the correlation is statistically significant, the magnitude
is relatively small.


This suggests that temporal instability alone is not a sufficient
failure predictor.



---

# 6. Discussion


The results provide two important observations.


## 6.1 Keypoint stability is keypoint-specific


Different keypoints exhibit different temporal variations.

This supports the previous observation that keypoints should not be
treated equally.



## 6.2 Stability is complementary to geometric reliability


Temporal variance does not directly explain tracking failure.

Instead, it provides additional information about keypoint behavior
during motion.


Therefore, reliability modeling should combine:

- geometric consistency;
- temporal stability;
- articulation relevance.



---

# 7. Connection to Next Analysis


E9 reveals that keypoint trajectories contain different motion
patterns.

However, temporal stability does not explain why some keypoints are
more informative for articulation estimation.


Therefore, E10 further investigates the relationship between keypoint
motion and joint state changes.