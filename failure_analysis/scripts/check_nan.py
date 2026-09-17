import pandas as pd


csv_path = "failure_analysis/results/per_frame_results.csv"

df = pd.read_csv(csv_path)


print("=" * 60)
print("DATA CHECK")
print("=" * 60)

print("shape:")
print(df.shape)

print()

print("NaN count:")
print(df.isna().sum())

print()

print("Inf check:")

for col in df.columns:
    if pd.api.types.is_numeric_dtype(df[col]):
        inf_num = (~df[col].apply(lambda x: abs(x) != float("inf"))).sum()

        if inf_num > 0:
            print(col, "has inf")

print()

print("Pre residual abnormal rows:")

cols = [
    "child_kp_pre_res_mean",
    "child_kp_pre_res_max",
    "child_kp_pre_res_std"
]


print(
    df[
        df[cols].isna().any(axis=1)
    ]
)
