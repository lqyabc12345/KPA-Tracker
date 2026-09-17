# Failure Analysis Framework


## 1. Objective


Keypoint-based articulated tracking relies on predicted keypoints as
geometric constraints for pose and articulation optimization.

However, tracking failures may occur when predicted keypoints provide
inaccurate or unreliable constraints.


The objective of this failure analysis is to:

1. identify the main factors causing articulated tracking degradation;
2. analyze the reliability characteristics of individual keypoints;
3. discover reliability cues for adaptive keypoint-aware optimization.



---

# 2. Failure Analysis Philosophy


Instead of directly designing a new optimization strategy, this work
follows a failure-driven methodology.


The analysis follows:


Tracking failure

↓

Error pattern analysis

↓

Identification of reliability factors

↓

Keypoint reliability modeling

↓

Adaptive optimization design



The goal is to understand why existing keypoint-based optimization
fails before introducing additional mechanisms.



---

# 3. Research Questions


## RQ1: Temporal Propagation


### Question


Does temporal propagation distance influence tracking degradation?


### Motivation


Keypoint-based tracking usually propagates information from previous
keyframes.

As the distance from the latest keyframe increases, prediction error
may accumulate.


### Analysis variable


Temporal distance:



key_dis



### Corresponding experiment



E1 Temporal Failure Analysis




---

# RQ2: Keypoint Observation Reliability


### Question


Are tracking failures related to inaccurate keypoint predictions?


### Motivation


Optimization assumes predicted keypoints provide reliable geometric
constraints.

However, inaccurate keypoints may introduce incorrect optimization
directions.



### Analysis variable


Pre-optimization keypoint residual:



child_kp_pre_res




### Corresponding experiment



E2 Keypoint Reliability Analysis




---

# RQ3: Keypoint-specific Contribution


### Question


Do all keypoints provide equivalent tracking information?


### Motivation


Most optimization formulations treat all keypoints equally.

However, different keypoints may have different:

- geometric reliability;
- temporal stability;
- optimization influence.



### Analysis


Individual keypoint analysis:



child_kp_pre_res_i



where:



i ∈ {0,1,2,3}




### Corresponding experiments



E3-E8 Keypoint Reliability Design Analysis




---

# RQ4: Articulation Observability


### Question


Do different keypoints encode different articulation motion
information?


### Motivation


A keypoint may be geometrically reliable but provide limited
information about joint motion.

Therefore, reliability should consider articulation relevance.



### Analysis variables


Keypoint trajectory:



pred_child_kp_history.npy



Joint trajectory:



optimized_joint_state_history.npy




### Corresponding experiments



E9-E10 Motion and Articulation Analysis




---

# 4. Analysis Pipeline


The complete failure analysis pipeline is:



Input Tracking Sequence

      |
      v

Tracking Result Extraction

      |
      v

Articulation Error Measurement

      |
      |
      +---------------------+
      |                     |
      v                     v

Temporal Analysis Keypoint Analysis

      |                     |
      +---------------------+

                |
                v

      Reliability Factor Discovery

                |
                v

      Adaptive Keypoint Optimization



---

# 5. Reliability Factors


The analysis investigates three major reliability dimensions.



## 5.1 Observation Reliability


Definition:


The consistency between predicted keypoints and articulated model
constraints.


Measurement:



keypoint residual



Related experiments:



E2-E3




---

## 5.2 Temporal Stability


Definition:


The consistency of keypoint behavior over temporal propagation.


Measurement:



keypoint trajectory variation



Related experiments:



E4-E9




---

## 5.3 Articulation Observability


Definition:


The amount of articulation motion information contained in a keypoint.


Measurement:



keypoint motion response to joint state changes



Related experiments:



E10




---

# 6. Experiment Organization


The experiments are organized into three analysis stages.



## Stage I: Failure Characterization


Experiments:



E1-E2



Goal:


Identify major factors correlated with tracking degradation.



---

## Stage II: Keypoint Reliability Analysis


Experiments:



E3-E8



Goal:


Understand whether keypoints provide different levels of reliability
and influence.



---

## Stage III: Motion and Articulation Analysis


Experiments:



E9-E10



Goal:


Investigate the temporal and physical meaning of keypoint reliability.



---

## Stage IV: Method Development


Experiment:



E11



Goal:


Develop a reliability-aware keypoint optimization strategy based on
the observations.



---

# 7. Expected Insights


The failure analysis aims to reveal:


1. Temporal distance alone cannot fully explain tracking failures.


2. Keypoint prediction quality is strongly related to articulation
   estimation accuracy.


3. Different keypoints provide different levels of useful information.


4. Reliable keypoint contribution should be modeled adaptively rather
   than uniformly.



---

# 8. Connection to Method Design


The observations obtained from failure analysis provide the motivation
and design principles for the proposed method.


The final optimization framework is expected to incorporate
keypoint-specific reliability estimation and adaptive weighting to
reduce the influence of unreliable keypoint constraints.