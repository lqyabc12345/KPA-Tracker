import os
import numpy as np
import matplotlib.pyplot as plt
import csv


# ============================
# path
# ============================

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../.."
    )
)


weight_path = os.path.join(
    PROJECT_ROOT,
    "failure_analysis",
    "results",
    "online_weight_history.npy"
)


save_dir = os.path.join(
    PROJECT_ROOT,
    "failure_analysis",
    "results"
)


os.makedirs(
    save_dir,
    exist_ok=True
)


# ============================
# load
# ============================

weights = np.load(
    weight_path
)


print("="*60)
print("E13C ONLINE WEIGHT ANALYSIS")
print("="*60)


print(
    "weight shape:",
    weights.shape
)


# only child keypoints
# first four dimensions
child_weights = weights[:, :4]


print(
    "child weight shape:",
    child_weights.shape
)



# ============================
# statistics
# ============================

mean_weight = np.mean(
    child_weights,
    axis=0
)


std_weight = np.std(
    child_weights,
    axis=0
)


min_weight = np.min(
    child_weights,
    axis=0
)


max_weight = np.max(
    child_weights,
    axis=0
)



print("\nMean weight")
print(mean_weight)


print("\nStd weight")
print(std_weight)


print("\nMin weight")
print(min_weight)


print("\nMax weight")
print(max_weight)



# ============================
# save csv
# ============================

csv_path = os.path.join(
    save_dir,
    "e13c_weight_statistics.csv"
)


with open(
    csv_path,
    "w",
    newline=""
) as f:

    writer = csv.writer(f)

    writer.writerow(
        [
            "keypoint",
            "mean",
            "std",
            "min",
            "max"
        ]
    )


    for i in range(4):

        writer.writerow(
            [
                i,
                mean_weight[i],
                std_weight[i],
                min_weight[i],
                max_weight[i]
            ]
        )


print(
    "saved:",
    csv_path
)



# ============================
# Figure 1
# weight curve
# ============================

plt.figure(
    figsize=(10,5)
)


for i in range(4):

    plt.plot(
        child_weights[:,i],
        label=f"kp{i}"
    )


plt.xlabel(
    "Frame"
)


plt.ylabel(
    "Adaptive weight"
)


plt.title(
    "E13C Online Keypoint Weight Evolution"
)


plt.legend()


plt.grid(
    True
)


curve_path = os.path.join(
    save_dir,
    "e13c_weight_curve.png"
)


plt.savefig(
    curve_path,
    dpi=300,
    bbox_inches="tight"
)


plt.close()


print(
    "saved:",
    curve_path
)



# ============================
# Figure 2
# mean weight
# ============================

plt.figure(
    figsize=(6,4)
)


plt.bar(
    np.arange(4),
    mean_weight
)


plt.xticks(
    np.arange(4),
    [
        "kp0",
        "kp1",
        "kp2",
        "kp3"
    ]
)


plt.ylabel(
    "Mean adaptive weight"
)


plt.title(
    "Average Keypoint Reliability Weight"
)


plt.grid(
    axis="y"
)


mean_path = os.path.join(
    save_dir,
    "e13c_mean_weight.png"
)


plt.savefig(
    mean_path,
    dpi=300,
    bbox_inches="tight"
)


plt.close()


print(
    "saved:",
    mean_path
)



print("="*60)
print("E13C ANALYSIS DONE")
print("="*60)