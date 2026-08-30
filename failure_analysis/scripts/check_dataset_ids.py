import torch

from dataset.dataset1_Tracker_camera import SapienDataset_OMADNet


DATA_ROOT = "./dataset1"
PARAMS_DIR = "./work_dir/KPA_generator_laptop_kp8"

dataset = SapienDataset_OMADNet(
    "val",
    data_root=DATA_ROOT,
    add_noise=False,
    num_pts=1024,
    num_parts=2,
    num_cates=5,
    cate_id=1,
    device=torch.device("cpu"),
    data_tag="train",
    kp_anno_path=f"{PARAMS_DIR}/unsup_test_keypoints.pkl"
)

print("dataset length:", len(dataset))

urdf_ids = []

for i in range(len(dataset)):
    data = dataset[i]

    # 与 video_func_dataset1.py 的返回顺序保持一致
    urdf_id = data[14]

    if torch.is_tensor(urdf_id):
        urdf_id = urdf_id.item()

    urdf_ids.append(int(urdf_id))

print("unique urdf ids:", sorted(set(urdf_ids)))

from collections import Counter

print("urdf id counts:")
for urdf_id, count in sorted(Counter(urdf_ids).items()):
    print(urdf_id, count)