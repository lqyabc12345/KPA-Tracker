import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import pearsonr


# ============================================================
# RA-KPA Figure 3 v2
#
# (a) Temporal keypoint reliability
# (b) Reliability-weight relationship
# (c) Tracking refinement
#
# Output:
#   Figure3_RA_KPA_final.pdf
# ============================================================


ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)

RESULT_DIR = os.path.join(
    ROOT,
    "failure_analysis",
    "results"
)


REL_PATH = os.path.join(
    RESULT_DIR,
    "reliability_history.npy"
)

WEIGHT_PATH = os.path.join(
    RESULT_DIR,
    "online_weight_history.npy"
)

CSV_PATH = os.path.join(
    RESULT_DIR,
    "per_frame_results.csv"
)


SAVE_PATH = os.path.join(
    RESULT_DIR,
    "Figure3_RA_KPA_final.pdf"
)


# ============================================================
# style
# ============================================================

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 10
plt.rcParams["axes.labelsize"] = 10
plt.rcParams["axes.titlesize"] = 11
plt.rcParams["legend.fontsize"] = 8


# ============================================================
# utilities
# ============================================================

def moving_average(x, window=9):

    out = np.zeros_like(x)

    for i in range(len(x)):

        l=max(0,i-window//2)
        r=min(len(x),i+window//2+1)

        out[i]=np.mean(
            x[l:r]
        )

    return out



def load_data():

    reliability=np.load(
        REL_PATH
    )

    weights=np.load(
        WEIGHT_PATH
    )


    df=pd.read_csv(
        CSV_PATH
    )


    print("reliability:", reliability.shape)
    print("weights:", weights.shape)
    print("csv:", df.shape)


    return reliability,weights,df



def prepare_reliability(rel,total):

    full=np.ones(
        (total,4)
    )*np.nan


    start=total-rel.shape[0]


    full[start:]=rel


    return full



# ============================================================
# panel a
# ============================================================

def plot_reliability(ax,rel):


    frames=np.arange(
        len(rel)
    )


    names=[
        "kp0",
        "kp1",
        "kp2",
        "kp3"
    ]


    for i in range(4):

        y=rel[:,i]

        valid=~np.isnan(y)


        ax.plot(
            frames[valid],
            moving_average(y[valid]),
            linewidth=1.8,
            label=names[i]
        )


    ax.set_title(
        "(a) Temporal keypoint reliability"
    )

    ax.set_xlabel(
        "Frame"
    )

    ax.set_ylabel(
        "Reliability"
    )


    ax.grid(
        alpha=0.25
    )


    ax.legend(
        ncol=2,
        frameon=False
    )



# ============================================================
# panel b
# ============================================================

def plot_relation(ax,rel,w):


    colors=[
        "tab:blue",
        "tab:orange",
        "tab:green",
        "tab:red"
    ]


    names=[
        "kp0",
        "kp1",
        "kp2",
        "kp3"
    ]


    all_r=[]
    all_w=[]


    for i in range(4):

        r=rel[:,i]

        weight=w[:,i]


        valid=~np.isnan(r)


        ax.scatter(

            r[valid],
            weight[valid],

            s=8,

            alpha=0.25,

            color=colors[i],

            label=names[i]

        )


        all_r.extend(
            r[valid]
        )

        all_w.extend(
            weight[valid]
        )



    corr,_=pearsonr(
        all_r,
        all_w
    )


    x=np.linspace(
        min(all_r),
        max(all_r),
        100
    )


    coef=np.polyfit(
        all_r,
        all_w,
        1
    )


    y=np.polyval(
        coef,
        x
    )


    ax.plot(
        x,
        y,
        linewidth=2,
        color="black",
        linestyle="--"
    )


    ax.text(
        0.05,
        0.92,
        f"Pearson r={corr:.3f}",
        transform=ax.transAxes
    )


    ax.set_title(
        "(b) Reliability-weight correlation"
    )


    ax.set_xlabel(
        "Reliability"
    )


    ax.set_ylabel(
        "Adaptive weight"
    )


    ax.grid(
        alpha=0.25
    )


    ax.legend(
        frameon=False,
        ncol=2
    )



# ============================================================
# panel c
# ============================================================

def plot_tracking(ax,df):


    ini=df["ini_child_r"].values

    new=df["new_child_r"].values


    frames=np.arange(
        len(df)
    )


    ax.plot(
        frames,
        moving_average(ini),
        linewidth=1.8,
        label="Before"
    )


    ax.plot(
        frames,
        moving_average(new),
        linewidth=1.8,
        label="RA-KPA"
    )


    drop=(

        np.mean(ini)
        -
        np.mean(new)

    )/np.mean(ini)*100


    ax.text(

        0.03,
        0.95,

        f"Mean error:\n"
        f"{np.mean(ini):.1f}° → {np.mean(new):.1f}°\n"
        f"Reduction {drop:.1f}%",

        transform=ax.transAxes,

        va="top",

        bbox=dict(
            facecolor="white",
            alpha=0.8
        )

    )


    ax.set_title(
        "(c) Tracking refinement"
    )


    ax.set_xlabel(
        "Frame"
    )


    ax.set_ylabel(
        "Rotation error (deg)"
    )


    ax.grid(
        alpha=0.25
    )


    ax.legend(
        frameon=False
    )



# ============================================================
# main
# ============================================================


def main():


    rel,w,df=load_data()


    total=len(df)


    rel=prepare_reliability(
        rel,
        total
    )


    w=w[:,:4]


    fig,axs=plt.subplots(

        1,
        3,

        figsize=(12,3.3)

    )


    plot_reliability(
        axs[0],
        rel
    )


    plot_relation(
        axs[1],
        rel,
        w
    )


    plot_tracking(
        axs[2],
        df
    )


    plt.tight_layout()


    plt.savefig(
        SAVE_PATH,
        bbox_inches="tight"
    )


    print(
        "saved:",
        SAVE_PATH
    )



if __name__=="__main__":

    main()