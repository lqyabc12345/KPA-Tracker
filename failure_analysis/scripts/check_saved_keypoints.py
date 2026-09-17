import pickle
import numpy as np


path = (
"work_dir/KPA_generator_laptop_kp8/"
"unsup_test_keypoints.pkl"
)


with open(path, "rb") as f:
    data = pickle.load(f)


print(type(data))

if isinstance(data, dict):
    print(data.keys())

else:
    print(len(data))
    print(type(data[0]))


print(data)