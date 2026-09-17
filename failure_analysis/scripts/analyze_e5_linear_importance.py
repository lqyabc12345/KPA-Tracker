import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler


CSV_PATH = "failure_analysis/results/per_frame_results.csv"


def main():

    df = pd.read_csv(CSV_PATH)


    X = df[
        [
        "child_kp_pre_res_0",
        "child_kp_pre_res_1",
        "child_kp_pre_res_2",
        "child_kp_pre_res_3"
        ]
    ]


    y = df["new_child_r"]


    # normalize input
    scaler = StandardScaler()

    X_norm = scaler.fit_transform(X)


    model = LinearRegression()

    model.fit(
        X_norm,
        y
    )


    print("="*60)
    print("E5 KEYPOINT INFLUENCE")
    print("="*60)


    for i,c in enumerate(X.columns):

        print(
            c,
            "coef =",
            model.coef_[i]
        )


    print(
        "R2 =",
        model.score(
            X_norm,
            y
        )
    )


if __name__=="__main__":
    main()