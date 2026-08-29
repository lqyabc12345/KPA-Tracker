import os
import os.path as osp

import pandas as pd
import matplotlib.pyplot as plt


# 当前脚本：
# KPA-Tracker/failure_analysis/scripts/plot_results.py
SCRIPT_DIR = osp.dirname(osp.abspath(__file__))

# KPA-Tracker/failure_analysis
FAILURE_ANALYSIS_ROOT = osp.dirname(SCRIPT_DIR)

# results 和 figures
RESULT_DIR = osp.join(
    FAILURE_ANALYSIS_ROOT,
    "results"
)

FIGURE_DIR = osp.join(
    FAILURE_ANALYSIS_ROOT,
    "figures"
)

os.makedirs(FIGURE_DIR, exist_ok=True)


# CSV
CSV_PATH = osp.join(
    RESULT_DIR,
    "results.csv"
)

print("读取 CSV：", CSV_PATH)

if not osp.exists(CSV_PATH):
    raise FileNotFoundError(
        f"找不到 CSV 文件：{CSV_PATH}"
    )

if osp.getsize(CSV_PATH) == 0:
    raise RuntimeError(
        f"CSV 文件是空的：{CSV_PATH}"
    )


df = pd.read_csv(CSV_PATH)

print("\n读取到的数据：")
print(df)


# -------------------------
# Point Cloud Sparsity
# -------------------------

df = df.sort_values("num_points")


plt.figure(figsize=(7, 5))

plt.plot(
    df["num_points"],
    df["new_child_r"],
    marker="o",
    linewidth=2
)

plt.xlabel("Number of points")
plt.ylabel("Child rotation error (degree)")
plt.title("KPA-Tracker under Point Cloud Sparsity")

plt.grid(True, alpha=0.3)

plt.tight_layout()


SAVE_PATH = osp.join(
    FIGURE_DIR,
    "point_number_rotation.png"
)

plt.savefig(
    SAVE_PATH,
    dpi=300,
    bbox_inches="tight"
)

print("\n图片保存位置：", SAVE_PATH)

plt.show()