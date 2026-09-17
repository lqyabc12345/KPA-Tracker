import pandas as pd


CSV_PATH = "failure_analysis/results/per_frame_results.csv"


def main():

    df = pd.read_csv(CSV_PATH)


    print("="*60)
    print("E3.3 FAILURE CONDITIONED ANALYSIS")
    print("="*60)


    kp_cols = [
        f"child_kp_pre_res_{i}"
        for i in range(4)
    ]


    # top 20% failure frames
    threshold = df["new_child_r"].quantile(0.8)


    normal = df[
        df["new_child_r"] < threshold
    ]

    failure = df[
        df["new_child_r"] >= threshold
    ]


    print(
        "normal frames:",
        len(normal)
    )

    print(
        "failure frames:",
        len(failure)
    )


    print("\nMean residual comparison")

    for kp in kp_cols:

        print("="*40)
        print(kp)

        print(
            "normal:",
            normal[kp].mean()
        )

        print(
            "failure:",
            failure[kp].mean()
        )

        print(
            "increase:",
            failure[kp].mean()
            /
            normal[kp].mean()
        )


if __name__ == "__main__":
    main()