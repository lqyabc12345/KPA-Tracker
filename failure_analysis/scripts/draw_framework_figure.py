"""
Draw RA-KPA framework overview figure.

Prototype version for paper Figure 2.

Output:
    failure_analysis/results/framework_overview.png
"""


import os
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch



# =====================================================
# Path
# =====================================================


PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../.."
    )
)


OUTPUT_PATH = os.path.join(
    PROJECT_ROOT,
    "failure_analysis",
    "results",
    "framework_overview.png"
)



# =====================================================
# Helper function
# =====================================================


def draw_box(
        ax,
        xy,
        text,
        width=2.4,
        height=0.8
):

    x,y = xy


    box = FancyBboxPatch(
        (
            x-width/2,
            y-height/2
        ),
        width,
        height,

        boxstyle="round,pad=0.08",

        linewidth=1.8,

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

        fontsize=11
    )



def draw_arrow(
        ax,
        start,
        end
):

    arrow = FancyArrowPatch(
        start,
        end,

        arrowstyle="->",

        mutation_scale=18,

        linewidth=1.5
    )


    ax.add_patch(
        arrow
    )



# =====================================================
# Create canvas
# =====================================================


fig, ax = plt.subplots(
    figsize=(12,5)
)



ax.set_xlim(
    0,
    12
)

ax.set_ylim(
    0,
    6
)


ax.axis(
    "off"
)



# =====================================================
# Main pipeline
# =====================================================


boxes = [

    (
        1.0,
        3,
        "Input\nSequence"
    ),


    (
        3.0,
        3,
        "Keypoint\nHistory"
    ),


    (
        5.2,
        3,
        "Reliability\nEstimation\n$r_i^t$"
    ),


    (
        7.4,
        3,
        "Adaptive\nWeight\n$w_i^t$"
    ),


    (
        9.6,
        3,
        "Weighted\nOptimization"
    ),


    (
        11.3,
        3,
        "Refined\nPose"
    )

]



for x,y,text in boxes:

    draw_box(
        ax,
        (x,y),
        text
    )



# arrows

for i in range(
    len(boxes)-1
):

    draw_arrow(
        ax,
        (
            boxes[i][0]+1.2,
            3
        ),
        (
            boxes[i+1][0]-1.2,
            3
        )
    )



# =====================================================
# Reliability side information
# =====================================================


draw_box(
    ax,
    (
        5.2,
        1.3
    ),
    "Motion /\nCorrelation\nAnalysis"
)


draw_arrow(
    ax,
    (
        5.2,
        2.6
    ),
    (
        5.2,
        1.8
    )
)



draw_arrow(
    ax,
    (
        5.8,
        1.3
    ),
    (
        7.0,
        2.6
    )
)



# =====================================================
# Feedback loop
# =====================================================


feedback = FancyArrowPatch(

    (11.3,2.6),

    (3.0,2.6),

    connectionstyle="arc3,rad=-0.3",

    arrowstyle="->",

    mutation_scale=18,

    linewidth=1.5
)


ax.add_patch(
    feedback
)


ax.text(
    7.0,
    1.0,

    "Temporal Feedback",

    ha="center",

    fontsize=11
)



# title

ax.text(
    6,
    5.3,

    "RA-KPA: Reliability-Aware Keypoint Adaptation",

    ha="center",

    fontsize=15,

    weight="bold"
)



plt.tight_layout()


plt.savefig(
    OUTPUT_PATH,

    dpi=300,

    bbox_inches="tight"
)


plt.close()



print(
    "Saved:"
)

print(
    OUTPUT_PATH
)
