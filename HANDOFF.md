# Research Handoff

## Goal

This project reproduces and analyzes KPA-Tracker for articulated object tracking.

The current research goal is to identify a real failure mode first, then design an uncertainty-aware improvement rather than adding modules blindly.

Candidate direction:
- uncertainty-aware keypoints
- possibly uncertainty-guided adaptive keyframe update

The intended research workflow is:

Problem
→ Failure Analysis
→ Hypothesis
→ Method
→ Experiments
→ Paper

---

## Current Environment

- Ubuntu 22.04 / WSL2
- Python 3.8.20
- PyTorch 2.1.2
- CUDA 12.1
- RTX 4050 Laptop GPU
- Open3D 0.19.0

Category currently studied:
- laptop

Tracker configuration:
- num_points = 1024
- num_kp = 8
- num_parts = 2
- num_basis = 10
- seed = 0

---

## Important Code Changes

### Environment compatibility

`model/Pointnet2_PyTorch_master/pointnet2_ops_lib/setup.py`

CUDA architecture changed to 8.9 for RTX 4050 compatibility.

### Numerical stability

Rotation error calculation now clips cosine before arccos:

```python
cos_theta = np.clip(cos_theta, -1.0, 1.0)

This fixed NaN rotation errors.

Failure analysis logging

video_funcs/video_func_dataset1.py

Added per-frame logging for:

sample_id

frame_id

key_dis

urdf_id

initial pose errors

refined pose errors

camera pose errors

Random seed is fixed to 0.

CSV output:
failure_analysis/results/per_frame_results.csv

E1: Full Baseline Failure Analysis

Full run:

377 frames

category: laptop

num_points = 1024

num_kp = 8

Overall refined child rotation error

mean = 14.374°

median = 12.518°

std = 8.387°

max = 54.083°

Initial child rotation mean:

86.186°

This confirms refinement is very strong but does not eliminate all catastrophic failures.

Keyframe Distance Analysis

Mean refined child rotation error:

key_dis	count	mean	median	max
0	13	0.011	0.014	0.024
1	78	12.251	11.347	31.980
2	78	13.113	11.524	40.538
3	78	15.223	14.221	45.013
4	65	16.010	13.377	47.408
5	65	18.655	16.938	54.083

Correlation:

Pearson r = 0.356

Spearman rho = 0.336

Spearman p = 2.10e-11

Interpretation:
Tracking error has a moderate positive association with distance from the current keyframe.

Failure Rate

Diagnostic thresholds only, not official benchmark criteria.

key_dis	>10°	>20°	>30°
0	0.00%	0.00%	0.00%
1	65.38%	7.69%	1.28%
2	57.69%	12.82%	3.85%
3	74.36%	23.08%	7.69%
4	73.85%	24.62%	9.23%
5	86.15%	40.00%	13.85%

Severe failures (>20°, >30°) increase consistently with key_dis.

Current Research Interpretation

Current evidence suggests:

Refinement is essential.

Initial error alone does not explain final tracking failure.

Error tends to increase with keyframe distance.

Severe failure probability rises substantially at larger key_dis.

key_dis only moderately explains failure, so another reliability factor likely matters.

Main candidate:

keypoint reliability / uncertainty

Possible future direction:

uncertainty-aware keypoint weighting

uncertainty-guided adaptive keyframe update

Important:
Do not claim causality yet.
Current evidence is correlational.

Important Unresolved Issue

Dataset loader reports:

377 annotations

5 objects

But direct inspection of all Dataset samples gives:

unique urdf ids: [10040]
10040: 377 samples

This is not a CSV bug.

The Dataset code shows:

num_objs = 5 counts loaded test URDF model metadata

obj_annotation_list contains the actual evaluation annotations

all 377 current annotations correspond to URDF 10040

Still unresolved:
Why do the other test URDFs not appear in the evaluation annotations?

This must be investigated before claiming cross-object generalization.

Relevant file:
dataset/dataset1_Tracker_camera.py

Relevant logic:

TEST_URDF_IDs

obj_annotation_list

obj_urdf_id_list

data_tag / mode split

test.txt matching logic

Next Immediate Task

Do not modify the model yet.

First audit the dataset split:

inspect dataset1/laptop/test.txt

inspect which videos / annotations match it

count urdf_id per matched annotation

determine whether 377×URDF10040 is intended by the original dataset or caused by split/loading logic

Then decide whether E1 must be rerun.

After dataset validity is confirmed:

proceed to keypoint reliability analysis

correlate keypoint quality with refined tracking error

only then design uncertainty module