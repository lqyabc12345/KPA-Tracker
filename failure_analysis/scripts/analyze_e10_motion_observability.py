import numpy as np
from scipy.stats import pearsonr, spearmanr


kp = np.load(
    "failure_analysis/results/pred_child_kp_history.npy"
)

theta = np.load(
    "failure_analysis/results/optimized_joint_state_history.npy"
)


print("="*60)
print("E10 MOTION OBSERVABILITY")
print("="*60)


# theta
theta = theta.reshape(-1)


delta_theta = np.abs(
    np.diff(theta)
)


# kp motion
delta_kp = np.linalg.norm(
    np.diff(kp, axis=0),
    axis=2
)


# remove first frame
eps = 1e-6


for i in range(4):

    sensitivity = (
        delta_kp[:,i]
        /
        (delta_theta+eps)
    )


    print("="*50)
    print("kp",i)

    print(
        "mean sensitivity:",
        np.mean(sensitivity)
    )

    print(
        "std:",
        np.std(sensitivity)
    )

    print(
        "max:",
        np.max(sensitivity)
    )