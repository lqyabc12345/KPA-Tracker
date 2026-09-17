import pandas as pd
from scipy.stats import pearsonr, spearmanr


CSV_PATH = "failure_analysis/results/per_frame_results.csv"


def analyze(df, kp_col, target_col):

    x = df[kp_col]
    y = df[target_col]

    pearson = pearsonr(x, y)
    spearman = spearmanr(x, y)

    print("=" * 60)
    print(kp_col)

    print(
        "Pearson r = %.4f  p = %.4e"
        %
        (
            pearson.statistic,
            pearson.pvalue
        )
    )

    print(
        "Spearman rho = %.4f  p = %.4e"
        %
        (
            spearman.statistic,
            spearman.pvalue
        )
    )


def main():

    df = pd.read_csv(CSV_PATH)

    print("="*60)
    print("E3: PER-KEYPOINT RELIABILITY ANALYSIS")
    print("="*60)

    print("Number of frames:", len(df))


    target = "new_child_r"


    print()
    print("Target:", target)


    for i in range(4):

        kp_col = f"child_kp_pre_res_{i}"

        analyze(
            df,
            kp_col,
            target
        )


if __name__ == "__main__":
    main()