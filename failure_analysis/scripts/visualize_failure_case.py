"""
RA-KPA Failure Case Visualization

Generate paper prototype figure for selected failure case.

Current case:
    frame 282

Generated:
    failure_case_282.png
    failure_case_282.pdf

Author:
    RA-KPA project
"""


import os
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt



# =====================================================
# Project paths
# =====================================================


PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../.."
    )
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


WEIGHT_PATH = os.path.join(
    RESULT_DIR,
    "online_weight_history.npy"
)


KP_PATH = os.path.join(
    RESULT_DIR,
    "pred_child_kp_history.npy"
)



OUTPUT_PNG = os.path.join(
    RESULT_DIR,
    "failure_case_282.png"
)


OUTPUT_PDF = os.path.join(
    RESULT_DIR,
    "failure_case_282.pdf"
)



# =====================================================
# Selected frame
# =====================================================


FRAME_ID = 282



# =====================================================
# Load data
# =====================================================


print("="*60)
print("RA-KPA FAILURE CASE VISUALIZATION")
print("="*60)



df = pd.read_csv(
    CSV_PATH
)


# IMPORTANT:
# remove possible spaces in csv headers
df.columns = df.columns.str.strip()



weights = np.load(
    WEIGHT_PATH
)


kp_history = np.load(
    KP_PATH
)



print(
    "CSV:",
    df.shape
)


print(
    "weights:",
    weights.shape
)


print(
    "keypoints:",
    kp_history.shape
)



# =====================================================
# Extract selected frame
# =====================================================


row = df.iloc[FRAME_ID]


initial_error = row[
    "ini_child_r"
]


optimized_error = row[
    "new_child_r"
]


residuals = []


# =====================================================
# Keypoint residuals
# IMPORTANT:
# CSV only stores child_kp_pre_res_0~3
# These are the per-keypoint residuals before optimization
# =====================================================

residuals = []


for i in range(4):

    residuals.append(
        row[
            f"child_kp_pre_res_{i}"
        ]
    )


residuals = np.array(
    residuals
)


residuals = np.array(
    residuals
)



frame_weight = weights[
    FRAME_ID
]


frame_kp = kp_history[
    FRAME_ID
]



print()
print(
    "Frame:",
    FRAME_ID
)


print(
    "Initial error:",
    initial_error
)


print(
    "RA-KPA error:",
    optimized_error
)


print(
    "Weight:",
    frame_weight
)


print(
    "Residual:",
    residuals
)



# =====================================================
# Create figure
# =====================================================


fig = plt.figure(
    figsize=(12,9)
)



# -----------------------------------------------------
# (a) Error comparison
# -----------------------------------------------------


ax1 = fig.add_subplot(
    221
)


ax1.bar(
    [
        "Before",
        "RA-KPA"
    ],
    [
        initial_error,
        optimized_error
    ]
)


ax1.set_title(
    "(a) Tracking Error Reduction"
)


ax1.set_ylabel(
    "Child Rotation Error (deg)"
)



# -----------------------------------------------------
# (b) Residual
# -----------------------------------------------------


ax2 = fig.add_subplot(
    222
)


ax2.bar(
    [
        f"kp{i}"
        for i in range(4)
    ],
    residuals
)


ax2.set_title(
    "(b) Keypoint Residual"
)


ax2.set_ylabel(
    "Residual"
)



# -----------------------------------------------------
# (c) Weight
# -----------------------------------------------------


ax3 = fig.add_subplot(
    223
)


ax3.bar(
    [
        f"kp{i}"
        for i in range(8)
    ],
    frame_weight
)


ax3.axhline(
    1.0,
    linestyle="--"
)


ax3.set_title(
    "(c) Adaptive Weight"
)


ax3.set_ylabel(
    "Weight"
)



# -----------------------------------------------------
# (d) 3D keypoint
# -----------------------------------------------------


ax4 = fig.add_subplot(
    224,
    projection="3d"
)



for i,p in enumerate(frame_kp):

    ax4.scatter(
        p[0],
        p[1],
        p[2]
    )

    ax4.text(
        p[0],
        p[1],
        p[2],
        f"kp{i}"
    )



ax4.set_title(
    "(d) Keypoint Geometry"
)



ax4.set_xlabel(
    "X"
)

ax4.set_ylabel(
    "Y"
)

ax4.set_zlabel(
    "Z"
)



# =====================================================
# Save
# =====================================================


plt.tight_layout()


plt.savefig(
    OUTPUT_PNG,
    dpi=300,
    bbox_inches="tight"
)


plt.savefig(
    OUTPUT_PDF,
    bbox_inches="tight"
)


plt.close()



print()
print(
    "Saved:"
)

print(
    OUTPUT_PNG
)

print(
    OUTPUT_PDF
)