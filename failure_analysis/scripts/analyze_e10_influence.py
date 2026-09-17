import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr
import os

print("="*60)
print("E10 KEYPOINT MOTION INFLUENCE")
print("="*60)


# -------------------------
# load
# -------------------------




ROOT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

RESULT_DIR = os.path.join(
    ROOT_DIR,
    "../results"
)


vectors = np.load(
    os.path.join(
        RESULT_DIR,
        "child_pre_vector_history.npy"
    )
)


joint_state = np.load(
    os.path.join(
        RESULT_DIR,
        "optimized_joint_state_history.npy"
    )
)


print("vector shape:", vectors.shape)
print("joint shape:", joint_state.shape)



# flatten joint state

joint_state = joint_state.reshape(-1)



# residual magnitude

res_mag = np.linalg.norm(
    vectors,
    axis=-1
)


print()
print("Residual magnitude")
print("="*60)


for kp in range(4):

    r = res_mag[:,kp]

    print(
        f"kp {kp}: mean={r.mean():.5f}, std={r.std():.5f}, max={r.max():.5f}"
    )



# ------------------------------------------------
# temporal motion
# ------------------------------------------------

motion = np.linalg.norm(
    np.diff(vectors,axis=0),
    axis=-1
)


print()
print("="*60)
print("Temporal motion")
print("="*60)


for kp in range(4):

    m=motion[:,kp]

    print(
        f"kp {kp}: mean={m.mean():.5f}, std={m.std():.5f}"
    )



# ------------------------------------------------
# joint correlation
# ------------------------------------------------

print()
print("="*60)
print("Motion vs joint state")
print("="*60)


for kp in range(4):

    m=motion[:,kp]


    p=pearsonr(
        m,
        np.abs(np.diff(joint_state))
    )

    s=spearmanr(
        m,
        np.abs(np.diff(joint_state))
    )


    print("--------------------------------")
    print("kp",kp)
    print("Pearson:",p)
    print("Spearman:",s)