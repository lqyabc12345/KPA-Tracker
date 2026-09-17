import os
import pandas as pd
from scipy.stats import pearsonr, spearmanr


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

CSV_PATH = os.path.join(
    PROJECT_ROOT,
    "failure_analysis",
    "results",
    "per_frame_results.csv"
)


def compute_corr(df, x_col, y_col):
    pearson = pearsonr(df[x_col], df[y_col])
    spearman = spearmanr(df[x_col], df[y_col])

    return {
        "pearson_r": pearson.statistic,
        "pearson_p": pearson.pvalue,
        "spearman_rho": spearman.statistic,
        "spearman_p": spearman.pvalue,
    }


def print_corr(title, df, x_col, y_col="new_child_r"):
    result = compute_corr(df, x_col, y_col)

    print(title)
    print(f"  n            = {len(df)}")
    print(f"  Pearson r    = {result['pearson_r']:.4f}")
    print(f"  Pearson p    = {result['pearson_p']:.4e}")
    print(f"  Spearman rho = {result['spearman_rho']:.4f}")
    print(f"  Spearman p   = {result['spearman_p']:.4e}")
    print()


def main():
    df = pd.read_csv(CSV_PATH)

    print("=" * 60)
    print("E2: KEYPOINT RELIABILITY ANALYSIS")
    print("=" * 60)
    print(f"Number of frames: {len(df)}")
    print()

    metrics = [
        "key_dis",
        "child_kp_pre_res_mean",
        "child_kp_pre_res_max",
        "child_kp_pre_res_std",
        "child_kp_res_mean",
        "child_kp_res_max",
        "child_kp_res_std",
    ]

    print("=" * 60)
    print("ALL FRAMES")
    print("=" * 60)

    for metric in metrics:
        print_corr(
            metric,
            df,
            metric,
        )

    non_key_df = df[df["key_dis"] > 0].copy()

    print("=" * 60)
    print("NON-KEYFRAMES ONLY: key_dis > 0")
    print("=" * 60)

    for metric in metrics:
        print_corr(
            metric,
            non_key_df,
            metric,
        )

    print("=" * 60)
    print("WITHIN KEY_DIS")
    print("=" * 60)

    for key_dis in sorted(non_key_df["key_dis"].unique()):
        subset = non_key_df[
            non_key_df["key_dis"] == key_dis
        ]

        print(f"--- key_dis = {key_dis} ---")

        print_corr(
            "pre mean",
            subset,
            "child_kp_pre_res_mean",
        )

        print_corr(
            "post mean",
            subset,
            "child_kp_res_mean",
        )


if __name__ == "__main__":
    main()