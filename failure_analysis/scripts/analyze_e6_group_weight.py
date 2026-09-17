import pandas as pd
from scipy.stats import spearmanr, pearsonr


CSV_PATH = "failure_analysis/results/per_frame_results.csv"


def report(name, x, y):

    p = pearsonr(x,y)
    s = spearmanr(x,y)

    print("="*50)
    print(name)
    print("Pearson:", p.statistic)
    print("Spearman:", s.statistic)



def main():

    df = pd.read_csv(CSV_PATH)

    target=df["new_child_r"]


    group_A = (
        df["child_kp_pre_res_0"]
        +
        df["child_kp_pre_res_2"]
    )/2


    group_B = (
        df["child_kp_pre_res_1"]
        +
        df["child_kp_pre_res_3"]
    )/2


    for lam in [
        0.25,
        0.5,
        1,
        2,
        4
    ]:

        score = (
            group_A
            +
            lam*group_B
        )


        report(
            f"lambda={lam}",
            score,
            target
        )


if __name__=="__main__":
    main()