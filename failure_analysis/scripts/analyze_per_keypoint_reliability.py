import pandas as pd
from scipy.stats import pearsonr, spearmanr


csv_path = "failure_analysis/results/per_frame_results.csv"


df = pd.read_csv(csv_path)


target = "new_child_r"


for i in range(8):

    col = f"child_kp_pre_res_{i}"

    pearson = pearsonr(
        df[col],
        df[target]
    )

    spearman = spearmanr(
        df[col],
        df[target]
    )

    print("="*40)
    print(col)

    print(
        "Pearson:",
        pearson.statistic,
        pearson.pvalue
    )

    print(
        "Spearman:",
        spearman.statistic,
        spearman.pvalue
    )