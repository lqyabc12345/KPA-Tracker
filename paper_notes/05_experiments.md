# 05_experiments.md

# Experiment Plan

## E1: Full Baseline Failure Analysis

### Research Question

Does the refined tracking error increase with the distance to the latest keyframe?

### Setup

- Category: laptop
- Validation samples: 377
- Test objects: 5
- num_points: 1024
- num_kp: 8
- num_parts: 2
- num_basis: 10
- seed: 0
- checkpoint: model_current_laptop.pth

### Variables

Per-frame logging:

- sample_id
- frame_id
- key_dis
- urdf_id

- ini_base_r
- ini_child_r
- ini_base_t
- ini_child_t

- new_base_r
- new_child_r
- new_base_t
- new_child_t

- cam_base_r
- cam_child_r
- cam_base_t
- cam_child_t

### Analysis

1. Overall error statistics
2. Error grouped by key_dis
3. Pearson correlation
4. Spearman correlation
5. Failure rate by key_dis
6. Per-object analysis
7. Top failure frames

### Status

Running

## E2 Keypoint reliability analysis

Goal:
Test whether keypoint quality correlates with refined tracking error.

Possible measurements:
- keypoint displacement
- geometric spread
- correspondence residual
- optimization residual
- predicted uncertainty

Status:
Not started.

---

## E3 Stress tests

Possible conditions:
- point sparsity: 1024 / 768 / 512 / 256 / 128
- occlusion
- motion perturbation

Goal:
Identify which conditions increase tracking failure and whether uncertainty responds correctly.

Status:
Not started.