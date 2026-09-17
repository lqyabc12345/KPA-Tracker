import pickle
import numpy as np


kp_path = (
"work_dir/KPA_generator_laptop_kp8/"
"unsup_test_keypoints.pkl"
)


with open(kp_path,"rb") as f:
    kp_dict=pickle.load(f)


kp = kp_dict[10040][1]


print("child keypoints")
print(kp)


# small rotation around y axis
theta=np.deg2rad(1)


R=np.array([
    [np.cos(theta),0,np.sin(theta)],
    [0,1,0],
    [-np.sin(theta),0,np.cos(theta)]
])


for i,p in enumerate(kp):

    moved=R@p

    sensitivity=np.linalg.norm(
        moved-p
    )

    print(
        "kp",
        i,
        "sensitivity=",
        sensitivity
    )