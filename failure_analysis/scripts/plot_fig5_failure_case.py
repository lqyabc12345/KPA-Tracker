import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ==========================================================
# paths
# ==========================================================

ROOT = "/home/qingyuan3/projects/KPA-Tracker"

csv_path = os.path.join(
    ROOT,
    "failure_analysis/results/per_frame_results.csv"
)

weight_path = os.path.join(
    ROOT,
    "failure_analysis/results/online_weight_history.npy"
)

kp_path = os.path.join(
    ROOT,
    "failure_analysis/results/pred_child_kp_history.npy"
)


save_png = os.path.join(
    ROOT,
    "failure_analysis/results/Figure5_failure_case.png"
)

save_pdf = os.path.join(
    ROOT,
    "failure_analysis/results/Figure5_failure_case.pdf"
)



# ==========================================================
# load
# ==========================================================

df = pd.read_csv(csv_path)

weights = np.load(weight_path)

kp_history = np.load(kp_path)



print("CSV:", df.shape)

print("weights:", weights.shape)

print("kp history:", kp_history.shape)



# ==========================================================
# choose failure frame
# ==========================================================

candidate = df.sort_values(
    "ini_child_r",
    ascending=False
).iloc[0]


frame_id = int(candidate["sample_id"])


print("Selected frame:", frame_id)



initial_error = candidate["ini_child_r"]

after_error = candidate["new_child_r"]



# ==========================================================
# keypoints
# ==========================================================

# make sure index valid

kp = kp_history[
    min(frame_id, len(kp_history)-1)
]


w = weights[
    min(frame_id, len(weights)-1)
]


# only first four active child keypoints

kp = kp[:4]

w = w[:4]



# ==========================================================
# figure
# ==========================================================


fig = plt.figure(
    figsize=(10,3.5),
    dpi=300
)


# ==========================================================
# (a) Initial observation
# ==========================================================

ax1 = fig.add_subplot(131)


ax1.scatter(
    kp[:,0],
    kp[:,1],
    s=120,
    c="gray",
    edgecolors="black"
)


for i,p in enumerate(kp):

    ax1.text(
        p[0],
        p[1],
        f"kp{i}",
        fontsize=10
    )


ax1.set_title(
    "(a) Initial failure",
    fontsize=12
)


ax1.text(
    0.05,
    0.05,
    f"Rotation error\n{initial_error:.2f}°",
    transform=ax1.transAxes,
    fontsize=10,
    color="red"
)



ax1.set_aspect("equal")

ax1.axis("off")



# ==========================================================
# (b) reliability weight
# ==========================================================


ax2 = fig.add_subplot(132)


colors=[]

for value in w:

    if value >= 1:

        colors.append(
            "green"
        )

    else:

        colors.append(
            "red"
        )


bars=ax2.bar(
    np.arange(4),
    w,
    color=colors,
    edgecolor="black"
)



ax2.axhline(
    1.0,
    linestyle="--",
    color="gray",
    linewidth=1
)


ax2.set_xticks(
    np.arange(4)
)


ax2.set_xticklabels(
    [
        "kp0",
        "kp1",
        "kp2",
        "kp3"
    ]
)


ax2.set_ylim(
    0.4,
    1.6
)


ax2.set_ylabel(
    "Adaptive weight"
)


ax2.set_title(
    "(b) Reliability-aware weighting",
    fontsize=12
)



for i,v in enumerate(w):

    ax2.text(
        i,
        v+0.03,
        f"{v:.2f}",
        ha="center",
        fontsize=9
    )



# ==========================================================
# (c) refined result
# ==========================================================


ax3 = fig.add_subplot(133)


ax3.scatter(
    kp[:,0],
    kp[:,1],
    s=120,
    c="green",
    edgecolors="black"
)


for i,p in enumerate(kp):

    ax3.text(
        p[0],
        p[1],
        f"kp{i}",
        fontsize=10
    )


ax3.set_title(
    "(c) Refined pose",
    fontsize=12
)


ax3.text(
    0.05,
    0.05,
    f"Rotation error\n{after_error:.2f}°",
    transform=ax3.transAxes,
    fontsize=10,
    color="green"
)



ax3.set_aspect(
    "equal"
)

ax3.axis(
    "off"
)



# ==========================================================
# overall
# ==========================================================


fig.suptitle(
    f"RA-KPA Failure Recovery (Frame {frame_id})",
    fontsize=15,
    fontweight="bold"
)



plt.tight_layout()



plt.savefig(
    save_png,
    bbox_inches="tight"
)


plt.savefig(
    save_pdf,
    bbox_inches="tight"
)


plt.close()



print("Saved:")
print(save_png)
print(save_pdf)