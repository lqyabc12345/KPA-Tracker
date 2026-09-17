import pandas as pd
from scipy.stats import pearsonr, spearmanr


CSV_PATH = "failure_analysis/results/per_frame_results.csv"


def report(name,x,y):

    print("="*50)
    print(name)

    print(
        "Pearson:",
        pearsonr(x,y).statistic
    )

    print(
        "Spearman:",
        spearmanr(x,y).statistic
    )


def main():

    df=pd.read_csv(CSV_PATH)


    target=df["new_child_r"]


    A=(
        df["child_kp_pre_res_0"]
        +
        df["child_kp_pre_res_2"]
    )/2


    B=(
        df["child_kp_pre_res_1"]
        +
        df["child_kp_pre_res_3"]
    )/2


    rho_A=0.4885259551868938
    rho_B=0.6756733453351099


    total=rho_A+rho_B


    wA=rho_A/total
    wB=rho_B/total


    print("weights:")
    print("Group A:",wA)
    print("Group B:",wB)


    score=wA*A+wB*B


    report(
        "Correlation weighted",
        score,
        target
    )


if __name__=="__main__":
    main()