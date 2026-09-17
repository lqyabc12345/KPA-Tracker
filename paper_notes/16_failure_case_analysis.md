# RA-KPA Failure Case Analysis


# 1. Purpose


The failure case analysis provides qualitative evidence that RA-KPA improves robustness under challenging articulated motion.


The goal is not to show the worst tracking frame.

Instead, the goal is to demonstrate a representative failure mode where:


1. Keypoint reliability becomes unstable.

2. Uniform optimization is affected by unreliable constraints.

3. Adaptive reliability weighting recovers accurate tracking.



---

# 2. Selected Case


Current automatic selection:


Frame:


282



Statistics:


Initial child rotation error:


\[
167.68^\circ
\]


RA-KPA optimized error:


\[
15.79^\circ
\]


Improvement:


\[
151.89^\circ
\]



Weight adaptation magnitude:


\[
||w_t-1||=0.7115
\]



---

# 3. Failure Scenario Explanation


## Before Adaptation


During difficult articulated motion:


- some keypoints become unreliable
- residual increases
- incorrect constraints affect optimization



Traditional optimization assumes:


\[
w_i=1
\]


for all keypoints.



Therefore:


unreliable observations contribute equally.



---

# 4. RA-KPA Behavior


RA-KPA estimates temporal keypoint reliability:


\[
r_i^t
\]


and updates optimization weights:


\[
w_i^t
\]



Reliable keypoints:


increase contribution.



Unreliable keypoints:


decrease contribution.



The optimization becomes:


\[
L=
\sum_i
w_i^t
||e_i||^2
\]



---

# 5. Required Visualization


The final qualitative figure should contain three parts.



## Part 1

Input Observation


Show:


- RGB/depth frame
- object pose
- keypoint observations



---

## Part 2

Baseline Result


Show:


- incorrect articulated pose
- keypoint mismatch
- tracking drift



Annotation:


"Uniform keypoint weighting"



---

## Part 3

RA-KPA Result


Show:


- corrected pose
- stable keypoint alignment
- adaptive weights



Annotation:


"Reliability-aware adaptation"



---

# 6. Additional Evidence


The figure should include:


## Weight Vector


Example:


\[
w_t=
[w_0,w_1,...]
\]


Highlight:


keypoints with reduced confidence.



---

## Residual Comparison


Show:


Before:


large unreliable keypoint residual



After:


balanced contribution



---

# 7. Paper Description


Possible text:


"Figure X shows a representative failure case under severe articulated motion. When unreliable keypoints dominate the optimization, the uniform weighting strategy produces significant pose drift. By estimating temporal keypoint reliability and adapting keypoint contribution, RA-KPA suppresses unstable constraints and successfully recovers the articulated pose."



---

# 8. Selection Rule


Future qualitative examples should satisfy:


\[
Recovery
+
Reliability\ Adaptation
+
Visual\ Interpretability
\]


A large error alone is insufficient.



---

# 9. Current Status


Completed:


✓ Automatic candidate ranking

✓ Best recovery candidate found


Next:


- visualize frame 282
- generate qualitative figure
- integrate into paper