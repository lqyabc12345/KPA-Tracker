# 03_hypotheses.md

# Research Hypotheses

## H1: Fixed keyframe interval may be suboptimal

### Observation
Refined child rotation error increases with keyframe distance.

Pearson r = 0.638 in the 30-frame diagnostic run.

### Hypothesis
The fixed keyframe update interval may fail to adapt to changes in tracking reliability.

When the current reference becomes unreliable, continuing to use it can increase tracking error.

### Evidence needed
- Full 377-frame analysis
- Per-object analysis
- Pearson and Spearman correlation
- Mean and median error by key_dis
- Failure rate by key_dis

---

## H2: Keypoint reliability may explain tracking failures

### Observation
Some frames with very large initial pose error are successfully refined, while others still fail.

Therefore initial pose error alone cannot explain failure.

### Hypothesis
The quality / reliability of predicted keypoints may determine whether refinement succeeds.

### Evidence needed
- Define a keypoint quality metric
- Measure keypoint quality per frame
- Correlate keypoint quality with refined pose error
- Inspect top failure frames
- Compare reliable vs unreliable keypoint cases

---

## H3: Uncertainty could guide adaptive keyframe updates

### Motivation
If keypoint uncertainty can indicate poor tracking reliability, it may be used not only to weight keypoints, but also to decide when to update the keyframe.

### Possible method
Uncertainty estimation
→ keypoint weighting
→ frame reliability score
→ adaptive keyframe update

### Status
Candidate direction only.
Not yet validated.