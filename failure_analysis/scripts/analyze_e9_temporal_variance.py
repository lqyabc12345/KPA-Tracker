import numpy as np
import pandas as pd


kp_path = (
    "failure_analysis/results/"
    "pred_child_kp_history.npy"
)

csv_path = (
    "failure_analysis/results/"
    "per_frame_results.csv"
)


# ======================
# load
# ======================

kp = np.load(kp_path)

df = pd.read_csv(csv_path)


print("="*60)
print("E9 TEMPORAL KEYPOINT STABILITY")
print("="*60)


print("kp shape:", kp.shape)


# kp:
# (377,4,3)


# ======================
# variance
# ======================

mean_kp = np.mean(
    kp,
    axis=0
)


var = np.mean(
    np.linalg.norm(
        kp - mean_kp[None,:,:],
        axis=2
    )**2,
    axis=0
)


print("\nKeypoint variance")
print("==================")


for i,v in enumerate(var):

    print(
        f"kp{i}: {v}"
    )


# ======================
# frame level instability
# ======================


frame_instability = np.mean(
    np.linalg.norm(
        kp - mean_kp[None,:,:],
        axis=2
    ),
    axis=1
)


df["kp_temporal_instability"] = (
    frame_instability
)


# ======================
# correlation
# ======================

from scipy.stats import pearsonr, spearmanr


target = "new_child_r"


print("\n")
print("="*60)
print("Instability vs pose error")
print("="*60)


pearson = pearsonr(
    df["kp_temporal_instability"],
    df[target]
)

spearman = spearmanr(
    df["kp_temporal_instability"],
    df[target]
)


print(
    "Pearson:",
    pearson
)

print(
    "Spearman:",
    spearman
)