import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import spearmanr


# ============================================================
# Paths
# ============================================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(SCRIPT_DIR)
)

RESULT_DIR = os.path.join(
    PROJECT_ROOT,
    "failure_analysis",
    "results"
)

CSV_PATH = os.path.join(
    RESULT_DIR,
    "per_frame_results.csv"
)

print("PROJECT_ROOT:", PROJECT_ROOT)
print("CSV_PATH:", CSV_PATH)


# ============================================================
# Load data
# ============================================================

df = pd.read_csv(CSV_PATH)

print("\n===== Dataset Info =====")
print("Number of frames:", len(df))
print("Number of objects:", df["urdf_id"].nunique())

print("URDF IDs:")
print(sorted(df["urdf_id"].unique()))


# ============================================================
# 1. Overall statistics
# ============================================================

print("\n===== Overall Statistics =====")

metrics = [
    "ini_child_r",
    "new_child_r",
    "cam_child_r",
    "new_base_r",
    "new_child_t"
]

print(
    df[metrics].describe()
)


# ============================================================
# 2. Keyframe-distance statistics
# ============================================================

print("\n===== Statistics by key_dis =====")

key_stats = (
    df.groupby("key_dis")["new_child_r"]
    .agg([
        "count",
        "mean",
        "median",
        "std",
        "min",
        "max"
    ])
    .reset_index()
)

print(key_stats)


# ============================================================
# 3. Pearson correlation
# ============================================================

pearson_r = df["key_dis"].corr(
    df["new_child_r"],
    method="pearson"
)

print(
    "\nPearson correlation "
    "(key_dis vs new_child_r):",
    pearson_r
)


# ============================================================
# 4. Spearman correlation
# ============================================================

spearman_r, spearman_p = spearmanr(
    df["key_dis"],
    df["new_child_r"]
)

print(
    "Spearman correlation "
    "(key_dis vs new_child_r):",
    spearman_r
)

print(
    "Spearman p-value:",
    spearman_p
)


# ============================================================
# 5. Failure rates
# ============================================================

print("\n===== Failure Rate by key_dis =====")

# These are diagnostic thresholds, not official benchmark criteria.
FAILURE_THRESHOLDS = [10, 20, 30]

failure_rows = []

for key_dis, group in df.groupby("key_dis"):

    row = {
        "key_dis": key_dis,
        "count": len(group)
    }

    for threshold in FAILURE_THRESHOLDS:

        rate = (
            group["new_child_r"] > threshold
        ).mean()

        row[f"failure_rate_gt_{threshold}deg"] = rate

    failure_rows.append(row)

failure_df = pd.DataFrame(failure_rows)

print(failure_df)


# ============================================================
# 6. Per-object analysis
# ============================================================

print("\n===== Per-object Analysis =====")

object_rows = []

for urdf_id, group in df.groupby("urdf_id"):

    pearson_obj = group["key_dis"].corr(
        group["new_child_r"],
        method="pearson"
    )

    spearman_obj, _ = spearmanr(
        group["key_dis"],
        group["new_child_r"]
    )

    object_rows.append({
        "urdf_id": urdf_id,
        "count": len(group),
        "mean_new_child_r":
            group["new_child_r"].mean(),
        "median_new_child_r":
            group["new_child_r"].median(),
        "pearson_keydis_error":
            pearson_obj,
        "spearman_keydis_error":
            spearman_obj
    })

object_df = pd.DataFrame(object_rows)

print(object_df)


# ============================================================
# 7. Top failures
# ============================================================

print("\n===== Top-10 Failure Frames =====")

top_failures = (
    df.sort_values(
        "new_child_r",
        ascending=False
    )[
        [
            "sample_id",
            "frame_id",
            "key_dis",
            "urdf_id",
            "ini_child_r",
            "new_child_r",
            "cam_child_r"
        ]
    ]
    .head(10)
)

print(top_failures)


# ============================================================
# 8. Save statistics as CSV
# ============================================================

key_stats.to_csv(
    os.path.join(
        RESULT_DIR,
        "e1_key_dis_stats.csv"
    ),
    index=False
)

failure_df.to_csv(
    os.path.join(
        RESULT_DIR,
        "e1_failure_rate_by_key_dis.csv"
    ),
    index=False
)

object_df.to_csv(
    os.path.join(
        RESULT_DIR,
        "e1_per_object_stats.csv"
    ),
    index=False
)

top_failures.to_csv(
    os.path.join(
        RESULT_DIR,
        "e1_top_failures.csv"
    ),
    index=False
)


# ============================================================
# 9. Figure 1: Error vs key_dis
# ============================================================

fig_path = os.path.join(
    RESULT_DIR,
    "e1_error_vs_key_dis.png"
)

plt.figure(figsize=(7, 5))

plt.scatter(
    df["key_dis"],
    df["new_child_r"],
    alpha=0.5
)

plt.xlabel("Distance to Keyframe (key_dis)")
plt.ylabel(
    "Refined Child Rotation Error (deg)"
)

plt.title(
    "Tracking Error vs Keyframe Distance\n"
    f"Pearson r = {pearson_r:.3f}, "
    f"Spearman rho = {spearman_r:.3f}"
)

plt.tight_layout()

plt.savefig(
    fig_path,
    dpi=200,
    bbox_inches="tight"
)

plt.close()

print("\nSaved:", fig_path)


# ============================================================
# 10. Figure 2: Mean / median trend
# ============================================================

trend_path = os.path.join(
    RESULT_DIR,
    "e1_key_dis_mean_median.png"
)

plt.figure(figsize=(7, 5))

plt.plot(
    key_stats["key_dis"],
    key_stats["mean"],
    marker="o",
    label="Mean"
)

plt.plot(
    key_stats["key_dis"],
    key_stats["median"],
    marker="o",
    label="Median"
)

plt.xlabel("Distance to Keyframe (key_dis)")
plt.ylabel(
    "Refined Child Rotation Error (deg)"
)

plt.title(
    "Mean and Median Tracking Error "
    "vs Keyframe Distance"
)

plt.legend()
plt.tight_layout()

plt.savefig(
    trend_path,
    dpi=200,
    bbox_inches="tight"
)

plt.close()

print("Saved:", trend_path)