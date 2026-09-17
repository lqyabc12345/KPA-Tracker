import pandas as pd
from scipy.stats import pearsonr, spearmanr


CSV_PATH = "failure_analysis/results/per_frame_results.csv"


def print_corr(name, x, y):

    pearson = pearsonr(x, y)
    spearman = spearmanr(x, y)

    print("=" * 60)
    print(name)

    print(
        "Pearson r = %.4f p=%.4e"
        %
        (
            pearson.statistic,
            pearson.pvalue
        )
    )

    print(
        "Spearman rho = %.4f p=%.4e"
        %
        (
            spearman.statistic,
            spearman.pvalue
        )
    )


def main():

    df = pd.read_csv(CSV_PATH)

    print("="*60)
    print("E3.2 NORMALIZED KEYPOINT RELIABILITY")
    print("="*60)

    print(
        "Number of frames:",
        len(df)
    )


    target = df["new_child_r"]


    for i in range(4):

        col = f"child_kp_pre_res_{i}"


        # z-score normalization
        normalized = (
            df[col] - df[col].mean()
        ) / df[col].std()


        print_corr(
            f"{col} (normalized)",
            normalized,
            target
        )


if __name__ == "__main__":
    main()