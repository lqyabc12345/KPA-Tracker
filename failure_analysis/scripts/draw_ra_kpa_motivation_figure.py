"""
RA-KPA Motivation Figure

Purpose:
    Figure 1 of paper.

Story:
    Uniform keypoint weighting fails because keypoint reliability changes.
    RA-KPA adapts weights online and recovers pose.

Input:
    pred_child_kp_history.npy
    online_weight_history.npy
    per_frame_results.csv


Output:
    RA_KPA_motivation_figure.png
    RA_KPA_motivation_figure.svg
"""


import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.patches import Circle, Rectangle, FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D



# =====================================================
# paths
# =====================================================


ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../.."
    )
)


RESULT = os.path.join(
    ROOT,
    "failure_analysis",
    "results"
)


KP_FILE = os.path.join(
    RESULT,
    "pred_child_kp_history.npy"
)

W_FILE = os.path.join(
    RESULT,
    "online_weight_history.npy"
)

CSV_FILE = os.path.join(
    RESULT,
    "per_frame_results.csv"
)



SAVE_PNG = os.path.join(
    RESULT,
    "RA_KPA_motivation_figure.png"
)


SAVE_SVG = os.path.join(
    RESULT,
    "RA_KPA_motivation_figure.svg"
)




# =====================================================
# helper
# =====================================================


def box(ax,x,y,w,h,text,fontsize=13,color="black"):

    patch = FancyBboxPatch(
        (x,y),
        w,
        h,

        boxstyle="round,pad=0.01",

        linewidth=2,

        edgecolor="black",

        facecolor="white",

        transform=ax.transAxes
    )

    ax.add_patch(patch)


    ax.text(
        x+w/2,
        y+h/2,

        text,

        ha="center",
        va="center",

        fontsize=fontsize,

        color=color,

        transform=ax.transAxes
    )



def arrow(ax,start,end):

    a=FancyArrowPatch(
        start,
        end,

        arrowstyle="->",

        mutation_scale=20,

        linewidth=2,

        transform=ax.transAxes
    )

    ax.add_patch(a)



def kp_projection(kp):

    pts=kp[:,:2]

    pts=pts-pts.mean(axis=0)

    pts=pts/(np.max(np.abs(pts))+1e-8)

    return pts



def weight_color(w):

    if w>1.05:
        return "#2ca02c"

    if w<0.95:
        return "#d62728"

    return "#777777"





# =====================================================
# keypoint drawing
# =====================================================


def draw_object(
        ax,
        position,
        kp,
        weights,
        title
):

    x,y,w,h=position


    box(
        ax,
        x,y,w,h,
        title,
        fontsize=14
    )


    pts=kp_projection(kp)


    px=x+0.5*w
    py=y+0.52*h


    scale=min(w,h)*0.32


    pts2=[]

    for p in pts:

        pts2.append(
            [
                px+p[0]*scale,
                py+p[1]*scale
            ]
        )

    pts2=np.array(pts2)


    # object shape

    order=[0,2,3,1]


    ax.plot(
        pts2[order,0],
        pts2[order,1],
        "--",
        linewidth=2,
        color="#6baed6",
        transform=ax.transAxes
    )


    for i,p in enumerate(pts2):

        c=weight_color(weights[i])


        circ=Circle(
            (
                p[0],
                p[1]
            ),

            0.015,

            color=c,

            ec="black",

            transform=ax.transAxes
        )

        ax.add_patch(circ)


        ax.text(
            p[0],
            p[1]+0.025,

            f"kp{i}",

            ha="center",

            fontsize=10,

            transform=ax.transAxes
        )





# =====================================================
# main
# =====================================================


def main():


    kp_hist=np.load(
        KP_FILE
    )


    weights=np.load(
        W_FILE
    )


    df=pd.read_csv(
        CSV_FILE
    )


    frame=282


    kp=kp_hist[frame]


    w=weights[frame][:4]


    row=df.iloc[frame]


    before=float(
        row["ini_child_r"]
    )

    after=float(
        row["new_child_r"]
    )



    fig=plt.figure(
        figsize=(15,8)
    )


    ax=fig.add_axes(
        [0,0,1,1]
    )


    ax.axis("off")



    # title

    ax.text(
        0.5,
        0.95,

        "Why Reliability-Aware Keypoint Adaptation?",

        ha="center",

        fontsize=24,

        fontweight="bold",

        transform=ax.transAxes
    )



    # -----------------------------
    # left
    # -----------------------------


    ax.text(
        0.25,
        0.83,

        "(a) Conventional Tracking",

        ha="center",

        fontsize=16,

        fontweight="bold",

        transform=ax.transAxes
    )


    draw_object(
        ax,

        (0.05,0.42,0.4,0.32),

        kp,

        np.ones(4),

        "Uniform keypoint assumption"
    )


    box(
        ax,

        0.12,
        0.25,

        0.25,

        0.08,

        "$w=[1,1,1,1]$",

        fontsize=18
    )


    arrow(
        ax,
        (0.25,0.25),
        (0.25,0.18)
    )


    box(
        ax,

        0.08,
        0.05,

        0.34,

        0.1,

        f"Pose failure\nerror={before:.2f}°",

        fontsize=16,

        color="#d62728"
    )




    # -----------------------------
    # right
    # -----------------------------


    ax.text(
        0.75,
        0.83,

        "(b) RA-KPA",

        ha="center",

        fontsize=16,

        fontweight="bold",

        transform=ax.transAxes
    )



    draw_object(
        ax,

        (0.55,0.42,0.4,0.32),

        kp,

        w,

        "Reliability-aware weighting"
    )


    box(
        ax,

        0.60,

        0.25,

        0.3,

        0.08,

        rf"$w=[{w[0]:.2f},{w[1]:.2f},{w[2]:.2f},{w[3]:.2f}]$",

        fontsize=16
    )


    arrow(
        ax,
        (0.75,0.25),
        (0.75,0.18)
    )


    box(
        ax,

        0.58,

        0.05,

        0.34,

        0.1,

        f"Recovered pose\nerror={after:.2f}°",

        fontsize=16,

        color="#2ca02c"
    )



    # middle explanation

    ax.text(
        0.5,

        0.35,

        "Temporal reliability estimation\n"
        "suppresses unreliable keypoints\n"
        "and emphasizes stable observations",

        ha="center",

        fontsize=14,

        transform=ax.transAxes
    )



    arrow(
        ax,
        (0.45,0.58),
        (0.55,0.58)
    )


    # save


    plt.savefig(
        SAVE_PNG,

        dpi=300,

        bbox_inches="tight"
    )


    plt.savefig(
        SAVE_SVG,

        bbox_inches="tight"
    )


    plt.close()


    print("saved:")
    print(SAVE_PNG)
    print(SAVE_SVG)




if __name__=="__main__":

    main()
