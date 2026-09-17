import pandas as pd
from scipy.stats import spearmanr, pearsonr


CSV_PATH = "failure_analysis/results/per_frame_results.csv"


def corr(name, x, y):

    p = pearsonr(x, y)
    s = spearmanr(x, y)

    print("="*60)
    print(name)

    print(
        "Pearson:",
        p.statistic
    )

    print(
        "Spearman:",
        s.statistic
    )


def main():

    df = pd.read_csv(CSV_PATH)

    target = df["new_child_r"]


    kp_cols = [
        f"child_kp_pre_res_{i}"
        for i in range(4)
    ]


    # baseline
    corr(
        "Mean residual",
        df["child_kp_pre_res_mean"],
        target
    )


    # sensitivity from E3.3
    sensitivity = [
        1.6401,
        2.0602,
        1.6327,
        1.9926
    ]


    uncertainty = 0

    for i, col in enumerate(kp_cols):

        uncertainty += (
            sensitivity[i]
            *
            df[col]
        )


    uncertainty /= 4


    corr(
        "Sensitivity weighted residual",
        uncertainty,
        target
    )


if __name__ == "__main__":
    main()