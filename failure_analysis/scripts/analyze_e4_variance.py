import pandas as pd


CSV_PATH = "failure_analysis/results/per_frame_results.csv"


def main():

    df = pd.read_csv(CSV_PATH)


    print("="*60)
    print("E4 VARIANCE BASED UNCERTAINTY")
    print("="*60)


    stds=[]


    for i in range(4):

        col=f"child_kp_pre_res_{i}"

        s=df[col].std()

        stds.append(s)

        print(
            col,
            "std =",
            s
        )


    print("\nWeights")


    inv=[
        1/x
        for x in stds
    ]


    total=sum(inv)


    for i,w in enumerate(inv):

        print(
            f"kp{i}:",
            w/total
        )


if __name__=="__main__":
    main()