"""
RA-KPA Concept Figure

Paper-style framework illustration.

Output:
    failure_analysis/results/RA_KPA_concept_figure.svg
    failure_analysis/results/RA_KPA_concept_figure.png
"""


import os
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np



# =====================================================
# path
# =====================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../.."
    )
)


SAVE_DIR = os.path.join(
    PROJECT_ROOT,
    "failure_analysis",
    "results"
)


os.makedirs(
    SAVE_DIR,
    exist_ok=True
)


SVG_PATH = os.path.join(
    SAVE_DIR,
    "RA_KPA_concept_figure.svg"
)


PNG_PATH = os.path.join(
    SAVE_DIR,
    "RA_KPA_concept_figure.png"
)



# =====================================================
# drawing utilities
# =====================================================


def add_box(
        ax,
        center,
        text,
        width=2.2,
        height=0.7,
        fontsize=11,
        linewidth=1.8
):

    x,y=center

    box = FancyBboxPatch(
        (
            x-width/2,
            y-height/2
        ),
        width,
        height,

        boxstyle="round,pad=0.05",

        linewidth=linewidth,

        edgecolor="black",

        facecolor="white"
    )

    ax.add_patch(box)

    ax.text(
        x,
        y,
        text,

        ha="center",
        va="center",

        fontsize=fontsize
    )



def add_arrow(
        ax,
        start,
        end,
        linewidth=1.5
):

    arrow = FancyArrowPatch(
        start,
        end,

        arrowstyle="->",

        mutation_scale=18,

        linewidth=linewidth
    )

    ax.add_patch(
        arrow
    )



# =====================================================
# canvas
# =====================================================


fig, ax = plt.subplots(
    figsize=(13,7)
)


ax.set_xlim(
    0,
    13
)

ax.set_ylim(
    0,
    7
)

ax.axis("off")



# =====================================================
# title
# =====================================================


ax.text(
    6.5,
    6.5,

    "RA-KPA: Reliability-Aware Keypoint Adaptation",

    ha="center",

    fontsize=18,

    fontweight="bold"
)



# =====================================================
# input keypoint observation
# =====================================================


add_box(
    ax,
    (1.5,4.5),
    "Keypoint\nObservation"
)


# fake keypoints inside box

kp=np.array(
    [
        [1.2,4.7],
        [1.3,4.2],
        [1.8,4.2],
        [1.9,4.7]
    ]
)


for i,p in enumerate(kp):

    ax.scatter(
        p[0],
        p[1],
        s=120,
        edgecolors="black"
    )

    ax.text(
        p[0]+0.05,
        p[1]+0.05,
        f"kp{i}",
        fontsize=8
    )



# =====================================================
# history
# =====================================================


add_box(
    ax,
    (3.8,4.5),
    "Temporal\nHistory"
)



# =====================================================
# reliability estimator
# =====================================================


add_box(
    ax,
    (6.2,4.5),
    "Reliability\nEstimator\n$r_i^t$"
)


# motion input

add_box(
    ax,
    (6.2,2.8),
    "Motion /\nCorrelation"
)


add_arrow(
    ax,
    (6.2,3.15),
    (6.2,4.05)
)



# =====================================================
# adaptive weight
# =====================================================


add_box(
    ax,
    (8.6,4.5),
    "Adaptive\nWeight\n$w_i^t$"
)


ax.text(
    8.6,
    3.85,

    "$[1.33,0.65,1.38,0.64]$",

    ha="center",

    fontsize=10
)



# =====================================================
# optimization
# =====================================================


add_box(
    ax,
    (11.0,4.5),
    "Weighted\nOptimization"
)


ax.text(
    11.0,
    3.85,

    "$\\sum_i w_i^t||e_i||^2$",

    ha="center",

    fontsize=10
)



# arrows main

add_arrow(ax,(2.6,4.5),(2.8,4.5))
add_arrow(ax,(5.0,4.5),(5.1,4.5))
add_arrow(ax,(7.3,4.5),(7.5,4.5))
add_arrow(ax,(9.7,4.5),(9.9,4.5))



# =====================================================
# output pose
# =====================================================


add_box(
    ax,
    (11.0,1.5),
    "Refined\nPose"
)


add_arrow(
    ax,
    (11.0,4.1),
    (11.0,1.9)
)



# =====================================================
# temporal feedback loop
# =====================================================


feedback = FancyArrowPatch(

    (10.5,1.5),

    (3.8,4.05),

    connectionstyle="arc3,rad=0.35",

    arrowstyle="->",

    mutation_scale=18,

    linewidth=1.5
)


ax.add_patch(
    feedback
)


ax.text(
    7.2,
    1.0,

    "Online Temporal Adaptation",

    ha="center",

    fontsize=12
)



# =====================================================
# save
# =====================================================


plt.savefig(
    PNG_PATH,
    dpi=300,
    bbox_inches="tight"
)


plt.savefig(
    SVG_PATH,
    bbox_inches="tight"
)


plt.close()



print("saved:")
print(PNG_PATH)
print(SVG_PATH)
