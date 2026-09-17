import pandas as pd


df = pd.read_csv(
    "failure_analysis/results/per_frame_results.csv"
)


for i in range(4):

    col=f"child_kp_pre_res_{i}"

    print("="*40)
    print(col)

    print("mean:", df[col].mean())
    print("std:", df[col].std())
    print("max:", df[col].max())
    print("95%:", df[col].quantile(0.95))