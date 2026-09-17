import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# =====================================================
# Paths
# =====================================================

ROOT = "/home/qingyuan3/projects/KPA-Tracker"

csv_path = os.path.join(
    ROOT,
    "failure_analysis/results/Figure4_ablation_summary.csv"
)

save_png = os.path.join(
    ROOT,
    "failure_analysis/results/Figure4_ablation_final.png"
)

save_pdf = os.path.join(
    ROOT,
    "failure_analysis/results/Figure4_ablation_final.pdf"
)



# =====================================================
# Load data
# =====================================================

df = pd.read_csv(csv_path)


print("=" * 60)
print("Figure 4 Ablation")
print("=" * 60)

print(df)



methods = df["method"].values

rotation_error = df["child_r"].values

translation_error = df["child_t"].values



# =====================================================
# Figure setup
# =====================================================

fig, axes = plt.subplots(
    1,
    2,
    figsize=(8.2, 3.4),
    dpi=300
)


x = np.arange(len(methods))


# baseline gray, ours blue

colors = [
    "#BDBDBD",
    "#BDBDBD",
    "#377EB8"
]



# =====================================================
# (a) Rotation error
# =====================================================

bars1 = axes[0].bar(
    x,
    rotation_error,
    width=0.65,
    color=colors,
    edgecolor="black",
    linewidth=0.6
)


axes[0].set_title(
    "(a) Child Rotation Error ?",
    fontsize=12
)


axes[0].set_ylabel(
    "Rotation Error (deg)",
    fontsize=11
)


axes[0].set_xticks(x)

axes[0].set_xticklabels(
    methods,
    fontsize=10
)


axes[0].set_ylim(
    0,
    18
)


for i, v in enumerate(rotation_error):

    axes[0].text(
        i,
        v + 0.35,
        f"{v:.2f}",
        ha="center",
        fontsize=10
    )



# =====================================================
# (b) Translation error
# =====================================================

bars2 = axes[1].bar(
    x,
    translation_error,
    width=0.65,
    color=colors,
    edgecolor="black",
    linewidth=0.6
)


axes[1].set_title(
    "(b) Child Translation Error ?",
    fontsize=12
)


axes[1].set_ylabel(
    "Translation Error",
    fontsize=11
)


axes[1].set_xticks(x)

axes[1].set_xticklabels(
    methods,
    fontsize=10
)


axes[1].set_ylim(
    0,
    0.18
)


for i, v in enumerate(translation_error):

    axes[1].text(
        i,
        v + 0.003,
        f"{v:.3f}",
        ha="center",
        fontsize=10
    )



# =====================================================
# Style
# =====================================================

for ax in axes:

    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.25
    )

    ax.spines["top"].set_visible(False)

    ax.spines["right"].set_visible(False)

    ax.tick_params(
        labelsize=10
    )



plt.tight_layout()



# =====================================================
# Save
# =====================================================

plt.savefig(
    save_png,
    dpi=300,
    bbox_inches="tight"
)


plt.savefig(
    save_pdf,
    bbox_inches="tight"
)


plt.close()



print()
print("Saved:")
print(save_png)
print(save_pdf)