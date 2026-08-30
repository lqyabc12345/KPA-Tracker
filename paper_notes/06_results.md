# 06_results.md

# Results

## Diagnostic Run 01

Setup:
- laptop
- 30 frames
- num_points = 1024
- num_kp = 8
- seed = 0

### Key results

Mean initial child rotation error:
87.79°

Mean refined child rotation error:
14.30°

Frame ID correlation:
Pearson r = 0.347

Keyframe distance correlation:
Pearson r = 0.638

### Keyframe distance statistics

| key_dis | count | mean | std | max |
|---|---:|---:|---:|---:|
| 0 | 2 | 0.0169 | 0.0041 | 0.0198 |
| 1 | 6 | 10.93 | 3.66 | 15.21 |
| 2 | 6 | 11.33 | 5.47 | 17.71 |
| 3 | 6 | 14.10 | 6.14 | 21.17 |
| 4 | 5 | 18.36 | 10.49 | 36.19 |
| 5 | 5 | 23.82 | 10.54 | 38.31 |

### Current interpretation
Error increases with distance to keyframe.

This is preliminary evidence that fixed keyframe updating may be a failure mode.


## E1: Full Baseline Failure Analysis

### Experimental Setup

- Category: laptop
- Evaluated frames: 377
- Logged URDF objects: 1
- URDF ID: 10040
- num_points: 1024
- num_kp: 8
- num_parts: 2
- num_basis: 10
- random seed: 0
- checkpoint: model_current_laptop.pth

### Data Integrity Check

- Expected CSV lines: 378
- Actual CSV lines: 378
- Logged frames: 377
- Filtered frames: 0

Note:
Although the dataset loading message reports 5 objects, the current per-frame log contains only one URDF ID (10040).
This needs to be investigated before making cross-object conclusions.

### Overall Results

| Metric | Mean | Median | Std | Max |
|---|---:|---:|---:|---:|
| Initial child rotation error | 86.19° | 82.38° | 50.93° | 179.75° |
| Refined child rotation error | 14.37° | 12.52° | 8.39° | 54.08° |
| Camera child rotation error | 14.39° | 12.76° | 8.41° | 53.88° |

The refinement stage substantially reduces the average child rotation error:

- Initial: 86.19°
- Refined: 14.37°

### Error by Keyframe Distance

| key_dis | Count | Mean | Median | Std | Max |
|---:|---:|---:|---:|---:|---:|
| 0 | 13 | 0.01° | 0.01° | 0.01° | 0.02° |
| 1 | 78 | 12.25° | 11.35° | 5.33° | 31.98° |
| 2 | 78 | 13.11° | 11.52° | 6.94° | 40.54° |
| 3 | 78 | 15.22° | 14.22° | 8.02° | 45.01° |
| 4 | 65 | 16.01° | 13.38° | 8.55° | 47.41° |
| 5 | 65 | 18.65° | 16.94° | 9.95° | 54.08° |

### Correlation Analysis

- Pearson correlation between `key_dis` and `new_child_r`:
  - r = 0.356

- Spearman rank correlation:
  - rho = 0.336
  - p = 2.10e-11

Both correlations are positive.

Compared with the preliminary 30-frame experiment (Pearson r = 0.638),
the correlation becomes weaker on the full 377-frame run but remains positive.


### Failure Rate by Keyframe Distance

The following thresholds are diagnostic thresholds for failure analysis,
not official benchmark criteria.

| key_dis | Count | Error > 10° | Error > 20° | Error > 30° |
|---:|---:|---:|---:|---:|
| 0 | 13 | 0.00% | 0.00% | 0.00% |
| 1 | 78 | 65.38% | 7.69% | 1.28% |
| 2 | 78 | 57.69% | 12.82% | 3.85% |
| 3 | 78 | 74.36% | 23.08% | 7.69% |
| 4 | 65 | 73.85% | 24.62% | 9.23% |
| 5 | 65 | 86.15% | 40.00% | 13.85% |

For the more severe thresholds (>20° and >30°), the failure rate
increases consistently with keyframe distance.

At `key_dis = 5`:

- 40.00% of frames have refined child rotation error > 20°.
- 13.85% of frames have refined child rotation error > 30°.

For the lower threshold (>10°), the trend is generally increasing
but is not strictly monotonic.

### Top Failure Frames

| Sample | Frame | key_dis | Initial Child R | Refined Child R |
|---:|---:|---:|---:|---:|
| 189 | 15 | 5 | 150.01° | 54.08° |
| 188 | 14 | 4 | 94.76° | 47.41° |
| 194 | 20 | 5 | 71.61° | 45.19° |
| 187 | 13 | 3 | 93.42° | 45.01° |
| 286 | 25 | 5 | 176.18° | 42.43° |

Four of the top five failure frames occur at `key_dis >= 4`.


### Generated Figures

- `failure_analysis/results/e1_error_vs_key_dis.png`
- `failure_analysis/results/e1_key_dis_mean_median.png`

### Generated Data Files

- `failure_analysis/results/per_frame_results.csv`
- `failure_analysis/results/e1_key_dis_stats.csv`
- `failure_analysis/results/e1_failure_rate_by_key_dis.csv`
- `failure_analysis/results/e1_per_object_stats.csv`
- `failure_analysis/results/e1_top_failures.csv`

### Logs

- `failure_analysis/results/e1_full_baseline.log`
- `failure_analysis/results/e1_analysis.log`