# E3 Keypoint-wise Reliability Analysis


## 1. Motivation


E2 demonstrates that aggregated keypoint residual is strongly
associated with tracking failure.

However, the aggregated metric treats all keypoints equally.

Different keypoints may contribute differently to optimization
because they may have different geometric reliability and influence.


This experiment performs a keypoint-wise analysis to investigate
whether individual keypoints exhibit different failure sensitivity.



---

# 2. Hypothesis


We hypothesize:


> Individual keypoints have different relationships with tracking
> degradation.


Therefore, uniform keypoint weighting may not be optimal.



---

# 3. Experimental Setup


Dataset:


dataset1



Object:


laptop



Frames:


377



Child keypoints:


4



For each keypoint:


Input:


child_kp_pre_res_i



where:

i ∈ {0,1,2,3}



Target:



new_child_r




---

# 4. Implementation


Analysis script:



failure_analysis/scripts/analyze_e3_keypoint.py



The script computes:


- Pearson correlation
- Spearman correlation


between each keypoint residual and child rotation error.



---

# 5. Results


Correlation between individual keypoint residual
and tracking error:


| Keypoint | Pearson | Spearman |
|---|---|---|
| kp0 | 0.5303 | 0.4928 |
| kp1 | 0.7181 | 0.7169 |
| kp2 | 0.5233 | 0.4853 |
| kp3 | 0.5247 | 0.5192 |



---

# 6. Analysis


The results show that keypoint reliability is highly non-uniform.


Among the four child keypoints:

kp1 demonstrates the strongest correlation with tracking error.


This indicates that errors from different keypoints do not have
the same influence on final articulation estimation.



However, this analysis does not directly indicate which keypoint
is always the most useful.

Instead, it reveals that keypoint contributions should be modeled
individually rather than uniformly.



---

# 7. Limitation


Correlation with tracking error only measures failure sensitivity.


It does not describe:

- articulation motion information;
- temporal stability;
- geometric observability.


Therefore, additional analysis is required.



---

# 8. Impact on Method Design


E3 provides evidence that:


> Different keypoints play different roles in articulated tracking.


This motivates a keypoint-specific reliability model instead of
uniform keypoint weighting.


Further experiments analyze:

- uncertainty estimation (E4-E8)
- temporal motion consistency (E9-E10)