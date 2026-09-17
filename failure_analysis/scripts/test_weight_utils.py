import numpy as np

from failure_analysis.weight_utils import compute_online_weight



kp_history=np.load(
    "failure_analysis/results/pred_child_kp_history.npy"
)


joint_history=np.load(
    "failure_analysis/results/optimized_joint_state_history.npy"
)



weights=compute_online_weight(
    kp_history,
    joint_history
)



print("shape:")
print(weights.shape)


for i in [
    0,
    10,
    50,
    100,
    200,
    376
]:

    print(
        "frame",
        i,
        weights[i]
    )


print("mean:")
print(
    weights.mean(axis=0)
)


print("std:")
print(
    weights.std(axis=0)
)