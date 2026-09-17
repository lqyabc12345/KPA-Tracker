import os
import numpy as np
from scipy.stats import pearsonr, spearmanr


ROOT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

RESULT_DIR = os.path.join(
    ROOT_DIR,
    "../results"
)


kp_history = np.load(
    os.path.join(
        RESULT_DIR,
        "pred_child_kp_history.npy"
    )
)


joint_history = np.load(
    os.path.join(
        RESULT_DIR,
        "optimized_joint_state_history.npy"
    )
)


print("kp shape:", kp_history.shape)
print("joint shape:", joint_history.shape)


kp_motion_vec = np.diff(
    kp_history,
    axis=0
)



kp_motion = np.linalg.norm(
    kp_motion_vec,
    axis=-1
)

joint_history = joint_history.reshape(-1)


joint_motion = np.abs(
    np.diff(joint_history)
)


print("="*60)
print("KEYPOINT MOTION MAGNITUDE")
print("="*60)


for kp in range(4):

    m = kp_motion[:,kp]

    print(
        f"kp {kp}: "
        f"mean={m.mean():.6f}, "
        f"std={m.std():.6f}, "
        f"max={m.max():.6f}"
    )

print()
print("="*60)
print("KEYPOINT MOTION vs JOINT MOTION")
print("="*60)


for kp in range(4):

    m = kp_motion[:,kp]


    pearson = pearsonr(
        m,
        joint_motion
    )


    spearman = spearmanr(
        m,
        joint_motion
    )


    print("-"*40)
    print("kp",kp)

    print(
        "Pearson:",
        pearson
    )

    print(
        "Spearman:",
        spearman
    )