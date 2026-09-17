"""
Select representative failure cases for RA-KPA paper visualization.

Purpose:
    Find frames where:
    1. baseline tracking is difficult
    2. RA-KPA improves accuracy
    3. adaptive weighting changes significantly

Output:
    failure_analysis/results/failure_case_candidates.csv
"""


import os
import csv
import numpy as np
import pandas as pd


PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../.."
    )
)


RESULT_DIR = os.path.join(
    PROJECT_ROOT,
    "failure_analysis",
    "results"
)


CSV_PATH = os.path.join(
    RESULT_DIR,
    "per_frame_results.csv"
)


WEIGHT_PATH = os.path.join(
    RESULT_DIR,
    "online_weight_history.npy"
)


OUTPUT_PATH = os.path.join(
    RESULT_DIR,
    "failure_case_candidates.csv"
)



def main():


    print("="*60)
    print("RA-KPA FAILURE CASE SELECTION")
    print("="*60)



    # --------------------------------------------------
    # Load tracking results
    # --------------------------------------------------

    df = pd.read_csv(
        CSV_PATH
    )


    print(
        "Loaded frames:",
        len(df)
    )


    # --------------------------------------------------
    # Load adaptive weights
    # --------------------------------------------------

    weights = np.load(
        WEIGHT_PATH
    )


    print(
        "Weight shape:",
        weights.shape
    )


    assert len(df) == weights.shape[0], \
        "Frame number and weight history mismatch"



    # --------------------------------------------------
    # Compute improvement
    # --------------------------------------------------

    #
    # Initial child rotation error
    #
    # Before optimization
    #
    initial_error = df[
        "ini_child_r"
    ].values



    #
    # RA-KPA optimized error
    #
    optimized_error = df[
        "new_child_r"
    ].values



    gain = (
        initial_error -
        optimized_error
    )



    # --------------------------------------------------
    # Compute weight adaptation magnitude
    # --------------------------------------------------

    #
    # 8 keypoint weights
    #
    # compare with uniform weighting
    #

    weight_change = np.linalg.norm(
        weights - 1.0,
        axis=1
    )



    # --------------------------------------------------
    # Combined paper score
    # --------------------------------------------------

    score = (
        np.maximum(gain,0)
        *
        weight_change
    )



    result = pd.DataFrame({

        "frame":
            np.arange(len(df)),


        "initial_child_r":
            initial_error,


        "optimized_child_r":
            optimized_error,


        "gain":
            gain,


        "weight_change":
            weight_change,


        "score":
            score

    })


    # --------------------------------------------------
    # Ranking
    # --------------------------------------------------

    result = result.sort_values(
        by="score",
        ascending=False
    )


    result.insert(
        0,
        "rank",
        np.arange(
            1,
            len(result)+1
        )
    )


    # --------------------------------------------------
    # Save
    # --------------------------------------------------

    result.to_csv(
        OUTPUT_PATH,
        index=False
    )


    print()
    print(
        "Saved:"
    )

    print(
        OUTPUT_PATH
    )


    print()
    print(
        "Top candidates:"
    )


    print(
        result.head(10)
    )



if __name__ == "__main__":

    main()
