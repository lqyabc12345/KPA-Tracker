import matplotlib.pyplot as plt


kp_names = [
    "kp0",
    "kp1",
    "kp2",
    "kp3"
]


rho = [
    0.4928,
    0.7169,
    0.4853,
    0.5192
]


plt.figure(figsize=(6,4))

plt.bar(
    kp_names,
    rho
)

plt.ylabel(
    "Spearman correlation with child rotation error"
)

plt.xlabel(
    "Child keypoint"
)

plt.title(
    "Per-keypoint reliability analysis"
)

plt.tight_layout()

plt.savefig(
    "failure_analysis/figures/e3_keypoint_reliability.png",
    dpi=300
)

plt.close()