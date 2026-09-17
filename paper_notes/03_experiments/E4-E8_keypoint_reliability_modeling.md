# E4-E8 Keypoint Reliability Modeling


## 1. Motivation


Previous experiments reveal that keypoint quality has a strong
relationship with articulated tracking accuracy.

E2 shows that keypoint prediction residual is correlated with tracking
error.

E3 further demonstrates that different keypoints exhibit different
reliability characteristics.


However, using all keypoints equally assumes identical contribution
from every keypoint.

Therefore, this experiment series investigates how keypoint
reliability can be characterized and aggregated.


The goal of E4-E8 is to answer:


> How can keypoint-specific reliability be modeled for adaptive
> articulated tracking?



---

# 2. Overall Experimental Design


The analysis follows a progressive design:



Residual reliability

    |

    v

Keypoint influence analysis

    |

    v

Keypoint grouping

    |

    v

Reliability weighting

    |

    v

Motion-aware reliability analysis



The experiments gradually move from observation quality to
keypoint-specific importance.



---

# 3. E4: Residual-based Reliability Analysis


## Objective


Determine whether keypoint residual can serve as a reliability indicator.


## Motivation


Optimization relies on predicted keypoints as geometric constraints.

Large keypoint residual indicates inconsistency between predicted
observations and articulated structure.


Therefore, residual magnitude is analyzed as a potential reliability
measurement.


## Metric


For each keypoint:



child_kp_pre_res_i



is used as the observation residual.


Two reliability scores are evaluated:


### Mean residual


The direct average residual across keypoints.


### Sensitivity weighted residual


Residual weighted by estimated keypoint sensitivity.



## Observation


Mean residual shows a positive correlation with tracking error.


Sensitivity weighting provides a small improvement.


This indicates that residual magnitude contains useful reliability
information, but residual alone is insufficient.



---

# 4. E4: Variance-based Reliability


## Objective


Investigate whether temporal residual stability provides additional
reliability information.


## Motivation


A keypoint may occasionally produce large residuals, but a stable
keypoint should maintain consistent behavior over time.


Therefore, residual variance is analyzed.


## Analysis


The standard deviation of each keypoint residual is computed:



std(child_kp_pre_res_i)



The resulting reliability weights indicate different stability levels
among keypoints.


## Observation


Different keypoints show significantly different variance.


Keypoints with lower residual variance are more stable and may provide
more reliable constraints.



---

# 5. E5: Keypoint Influence and Correlation Structure


## Objective


Analyze whether different keypoints contribute equally to tracking
accuracy.


## Motivation


Although all keypoints are optimized together, their influence on
tracking error may differ.


A linear regression model is used to estimate keypoint contribution.



## Keypoint Influence


The regression analysis shows different coefficients among keypoints.


This indicates that:

- some keypoints have stronger influence;
- some keypoints contribute less;
- keypoint importance is not uniform.



## Correlation Structure


Correlation analysis reveals strong relationships between keypoints.


Two groups are identified:



Group A:
kp0 + kp2

Group B:
kp1 + kp3



The result suggests that keypoints may contain shared structural
information.



---

# 6. E6: Group-level Reliability Weighting


## Objective


Investigate whether modeling keypoint groups improves reliability
estimation.


## Motivation


Highly correlated keypoints may represent similar geometric regions.

Instead of treating every keypoint independently, group-level weighting
is explored.



## Method


Two keypoint groups are weighted:



Group A:
kp0 + kp2

Group B:
kp1 + kp3



Different weighting factors are evaluated.



## Observation


Increasing the contribution of the more informative group improves
correlation with tracking error.


This indicates that reliability imbalance exists between keypoint
groups.



---

# 7. E7: Correlation-based Reliability Weighting


## Objective


Evaluate whether reliability weights can be derived from statistical
relationships.


## Method


Group correlation with tracking error is used to generate
data-driven weights.


The obtained weights are:



Group A:
0.4196

Group B:
0.5804



## Observation


Correlation-based weighting improves prediction of tracking error
compared with uniform weighting.


This demonstrates that reliability can be estimated from keypoint
behavior statistics.



---

# 8. E8: Motion-aware Reliability Transition


## Objective


Extend reliability analysis from static observation quality to motion
behavior.


## Motivation


A keypoint can be geometrically accurate but provide limited information
about articulation motion.

Therefore, reliability should also consider motion response.


## Analysis


Keypoint motion sensitivity is analyzed with respect to articulation
changes.


The analysis investigates:


joint motion
|
v
keypoint displacement response



## Observation


Different keypoints exhibit different motion sensitivity.

This motivates the later temporal and articulation analysis in
E9-E10.



---

# 9. Summary


The E4-E8 experiments reveal three important properties:


## 1. Residual reliability


Keypoint residual provides useful information about tracking quality.



## 2. Keypoint-specific importance


Different keypoints contribute differently to optimization accuracy.



## 3. Reliability imbalance


Uniform keypoint weighting is insufficient because keypoints contain
different levels of useful information.



These observations motivate a reliability-aware keypoint optimization
strategy.



---

# 10. Connection to Method Development


The findings from E4-E8 provide the design principles for the proposed
method:



Observation reliability

Keypoint importance

Motion relevance

    |

    v

Adaptive keypoint weighting



The following experiments further analyze temporal consistency and
articulation observability before introducing the final method.