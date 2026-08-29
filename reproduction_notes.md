项目：
KPA-Tracker

环境：
Ubuntu 22.04 / WSL2
Python 3.8.20
PyTorch 2.1.2 + CUDA 12.1
GPU: RTX 4050 Laptop
Open3D 0.19.0

Dataset：
dataset1
Category: laptop
Train annotations: 8323
Test annotations: 377
Test objects: 5

KPA Generator：
num_kp = 8
num_parts = 2
symtype = shape

KPA Tracker：
num_kp = 8
num_parts = 2
num_basis = 10
num_points = 1024

Test result：

Initial:
Base R = 4.8579°
Child R = 27.4524°
Base T = 0.06808
Child T = 0.28644

New:
Base R = 2.4359°
Child R = 2.0859°
Base T = 0.01193
Child T = 0.00953

Camera:
Base R = 2.4121°
Child R = 2.0765°
Base T = 0.00982
Child T = 0.00869