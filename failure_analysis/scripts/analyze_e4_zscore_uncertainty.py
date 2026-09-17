import pandas as pd
from scipy.stats import pearsonr, spearmanr


CSV_PATH = "failure_analysis/results/per_frame_results.csv"


def report(name, x, y):

    p = pearsonr(x, y)
    s = spearmanr(x, y)

    print("="*60)
    print(name)

    print("Pearson:", p.statistic)
    print("Spearman:", s.statistic)


def main():

    df = pd.read_csv(CSV_PATH)

    target=df["new_child_r"]


    cols=[
        f"child_kp_pre_res_{i}"
        for i in range(4)
    ]


    # baseline
    report(
        "mean residual",
        df["child_kp_pre_res_mean"],
        target
    )


    # z-score uncertainty

    z=[]

    for c in cols:

        z.append(
            abs(
                (
                    df[c]-df[c].mean()
                )
                /
                df[c].std()
            )
        )


    zscore_uncertainty=sum(z)/4


    report(
        "z-score uncertainty",
        zscore_uncertainty,
        target
    )


if __name__=="__main__":
    main()