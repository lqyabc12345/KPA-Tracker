import numpy as np
from scipy.stats import pearsonr


print("="*60)
print("E12 KEYPOINT WEIGHT DESIGN")
print("="*60)


kp_history = np.load(
    "failure_analysis/results/pred_child_kp_history.npy"
)

joint_history = np.load(
    "failure_analysis/results/optimized_joint_state_history.npy"
)


print("kp shape:", kp_history.shape)
print("joint shape:", joint_history.shape)


# ==========================
# Motion score
# ==========================

kp_motion = np.linalg.norm(
    kp_history[1:] - kp_history[:-1],
    axis=-1
)


motion_score = kp_motion.mean(axis=0)


print("\nMotion score")
print("="*40)

for i,v in enumerate(motion_score):
    print(
        f"kp{i}: {v}"
    )


motion_weight = (
    motion_score /
    motion_score.sum()
)


print("\nMotion weight")
print("="*40)

for i,v in enumerate(motion_weight):
    print(
        f"kp{i}: {v}"
    )


# ==========================
# Correlation
# ==========================

joint_motion = np.abs(
    joint_history[1:,0]
    -
    joint_history[:-1,0]
)


corr_score=[]


print("\nCorrelation")
print("="*40)


for i in range(4):

    corr,_ = pearsonr(
        kp_motion[:,i],
        joint_motion
    )

    corr_score.append(abs(corr))

    print(
        f"kp{i}: {corr}"
    )


corr_score=np.array(corr_score)


corr_weight = (
    corr_score /
    corr_score.sum()
)


print("\nCorrelation weight")
print("="*40)


for i,v in enumerate(corr_weight):
    print(
        f"kp{i}: {v}"
    )


# ==========================
# Combined
# ==========================


combined_weight = (
    motion_weight
    +
    corr_weight
)/2


print("\nCombined weight")
print("="*40)


for i,v in enumerate(combined_weight):
    print(
        f"kp{i}: {v}"
    )


print("="*60)