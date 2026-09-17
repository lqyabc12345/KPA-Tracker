# E10 Articulation Observability Analysis


## 1. Motivation


Previous experiments reveal that keypoints have different reliability
characteristics.

E4-E8 analyze geometric reliability and keypoint contribution, while
E9 studies temporal stability.


However, articulated tracking requires keypoints to provide motion
information related to joint changes.

Therefore, E10 investigates the articulation observability of different
keypoints.



---

# 2. Objective


The objective of E10 is to answer:


> Do different keypoints provide different levels of articulation
> motion information?


This analysis examines the relationship between keypoint motion and
joint state variation.



---

# 3. Data Representation


During tracking, two trajectories are recorded:


Child keypoint trajectory:



pred_child_kp_history.npy



Joint state trajectory:



optimized_joint_state_history.npy



The recorded dimensions are:



Keypoints:
(377,4,3)

Joint state:
(377,1)




---

# 4. Keypoint Motion Magnitude


The average motion magnitude of each keypoint is computed.


Results:



kp0:
0.2292

kp1:
0.1845

kp2:
0.2286

kp3:
0.1851



Two motion patterns are observed:


High-motion group:



kp0, kp2



Low-motion group:



kp1, kp3




---

# 5. Correlation with Joint Motion


The relationship between keypoint displacement and joint state change
is analyzed.


Results:



kp0:
Pearson = 0.6814

kp1:
Pearson = 0.3797

kp2:
Pearson = 0.6665

kp3:
Pearson = 0.3681



Keypoints kp0 and kp2 show stronger coupling with joint motion.



---

# 6. Motion Sensitivity Analysis


Jacobian-based sensitivity analysis is further performed.


The obtained sensitivities are:



kp0:
0.01284

kp1:
0.00880

kp2:
0.01284

kp3:
0.00880



The result confirms that different keypoints have different
articulation observability.



---

# 7. Discussion


The experiments demonstrate that keypoints provide complementary
information.


High observability keypoints:



kp0, kp2



provide stronger articulation motion cues.


Meanwhile:



kp1, kp3



show higher temporal stability according to E9.



Therefore, keypoint reliability should not be defined by a single
criterion.

A robust tracking framework should consider both:

- stability;
- articulation relevance.



---

# 8. Connection to Method Design


E10 completes the reliability analysis.


Together with E4-E9, the analysis reveals three reliability
dimensions:


1. Observation reliability

2. Temporal stability

3. Articulation observability


These observations motivate a reliability-aware adaptive keypoint
optimization strategy.