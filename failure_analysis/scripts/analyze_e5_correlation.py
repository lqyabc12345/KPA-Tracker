import pandas as pd


CSV_PATH = "failure_analysis/results/per_frame_results.csv"


df = pd.read_csv(CSV_PATH)


cols = [
    "child_kp_pre_res_0",
    "child_kp_pre_res_1",
    "child_kp_pre_res_2",
    "child_kp_pre_res_3"
]


print(
    df[cols].corr()
)