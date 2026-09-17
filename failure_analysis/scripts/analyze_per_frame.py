import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(SCRIPT_DIR)
)

RESULT_DIR = os.path.join(
    PROJECT_ROOT,
    "failure_analysis",
    "results"
)

os.makedirs(RESULT_DIR, exist_ok=True)

csv_path = os.path.join(
    RESULT_DIR,
    "per_frame_results.csv"
)

print("PROJECT_ROOT:", PROJECT_ROOT)
print("RESULT_DIR:", RESULT_DIR)
print("CSV:", csv_path)

df = pd.read_csv(csv_path)


fig1_path = os.path.join(
    RESULT_DIR,
    "ini_vs_new_child_r.png"
)

plt.figure(figsize=(6, 5))

plt.scatter(
    df["ini_child_r"],
    df["new_child_r"]
)

plt.xlabel("Initial Child Rotation Error (deg)")
plt.ylabel("Refined Child Rotation Error (deg)")
plt.title("Initial vs Refined Child Rotation Error")

plt.tight_layout()
plt.savefig(
    fig1_path,
    dpi=200,
    bbox_inches="tight"
)
plt.close()

print("Saved:", fig1_path)

fig2_path = os.path.join(
    RESULT_DIR,
    "new_child_r_over_frames.png"
)

plt.figure(figsize=(8, 4))

plt.plot(
    df["sample_id"],
    df["new_child_r"],
    marker="o"
)

plt.xlabel("Sample ID")
plt.ylabel("Refined Child Rotation Error (deg)")
plt.title("Refined Child Rotation Error over Frames")

plt.tight_layout()
plt.savefig(
    fig2_path,
    dpi=200,
    bbox_inches="tight"
)
plt.close()

print("Saved:", fig2_path)


# =========================
# 1. 只取第一个完整 29-frame sequence
# =========================

seq_df = df[df["sample_id"] < 29].copy()

print("\n===== Sequence Analysis =====")
print("Number of frames:", len(seq_df))


# =========================
# 2. 计算相关系数
# =========================

corr = np.corrcoef(
    seq_df["frame_id"],
    seq_df["new_child_r"]
)[0, 1]

print(
    "Correlation between frame_id and new_child_r:",
    corr
)


# =========================
# 3. 画 frame_id vs error
# =========================

fig3_path = os.path.join(
    RESULT_DIR,
    "new_child_r_vs_frame_id.png"
)

plt.figure(figsize=(9, 5))

plt.plot(
    seq_df["frame_id"],
    seq_df["new_child_r"],
    marker="o"
)

# 标出几个关键 frame 位置
for x in [0, 5, 10, 15, 20, 25, 28]:
    plt.axvline(
        x=x,
        linestyle="--",
        alpha=0.3
    )

plt.xlabel("Frame ID")
plt.ylabel("Refined Child Rotation Error (deg)")

plt.title(
    f"Refined Child Rotation Error vs Frame ID\n"
    f"Pearson r = {corr:.3f}"
)

plt.tight_layout()

plt.savefig(
    fig3_path,
    dpi=200,
    bbox_inches="tight"
)

plt.close()

print("Saved:", fig3_path)




# =========================
# Keyframe-distance analysis
# =========================

print("\n===== Key Distance Analysis =====")

# 先看 key_dis 有哪些取值
print("key_dis values:")
print(sorted(df["key_dis"].unique()))

# 每个 key_dis 对应多少帧、平均误差是多少
key_stats = (
    df.groupby("key_dis")["new_child_r"]
    .agg(["count", "mean", "std", "max"])
    .reset_index()
)

print("\nError statistics by key_dis:")
print(key_stats)


# -------------------------
# Pearson correlation
# -------------------------

key_corr = df["key_dis"].corr(
    df["new_child_r"],
    method="pearson"
)

print(
    "\nCorrelation between key_dis and new_child_r:",
    key_corr
)


# -------------------------
# Plot
# -------------------------

fig4_path = os.path.join(
    RESULT_DIR,
    "new_child_r_vs_key_dis.png"
)

plt.figure(figsize=(7, 5))

plt.scatter(
    df["key_dis"],
    df["new_child_r"]
)

plt.xlabel("Distance to Keyframe (key_dis)")
plt.ylabel("Refined Child Rotation Error (deg)")
plt.title(
    f"Child Rotation Error vs Keyframe Distance\n"
    f"Pearson r = {key_corr:.3f}"
)

plt.tight_layout()

plt.savefig(
    fig4_path,
    dpi=200,
    bbox_inches="tight"
)

plt.close()

print("Saved:", fig4_path)