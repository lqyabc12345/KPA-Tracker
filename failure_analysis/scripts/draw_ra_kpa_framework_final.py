"""
RA-KPA paper-style framework figure
-----------------------------------
This script creates a cleaner, more paper-like overview figure for RA-KPA.

Main idea:
1. show the observation keypoints from one real frame
2. compare uniform vs adaptive weight
3. emphasize the RA-KPA core module
4. show temporal online update

Input files:
- failure_analysis/results/pred_child_kp_history.npy
- failure_analysis/results/online_weight_history.npy
- failure_analysis/results/per_frame_results.csv

Output files:
- failure_analysis/results/RA_KPA_framework_final.png
- failure_analysis/results/RA_KPA_framework_final.svg

Usage:
python failure_analysis/scripts/draw_ra_kpa_framework_final.py
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Circle, Polygon
from matplotlib.lines import Line2D


# ============================================================
# 1. basic path setup
# ============================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

RESULT_DIR = os.path.join(PROJECT_ROOT, "failure_analysis", "results")

KP_PATH = os.path.join(RESULT_DIR, "pred_child_kp_history.npy")
WEIGHT_PATH = os.path.join(RESULT_DIR, "online_weight_history.npy")
CSV_PATH = os.path.join(RESULT_DIR, "per_frame_results.csv")

SAVE_PNG = os.path.join(RESULT_DIR, "RA_KPA_framework_final.png")
SAVE_SVG = os.path.join(RESULT_DIR, "RA_KPA_framework_final.svg")


# ============================================================
# 2. helper functions
# ============================================================

def project_to_2d(points_3d, mode="xy"):
    """
    Project 3D points to 2D for visualization.
    """
    if mode == "xy":
        return points_3d[:, [0, 1]]
    elif mode == "xz":
        return points_3d[:, [0, 2]]
    elif mode == "yz":
        return points_3d[:, [1, 2]]
    else:
        raise ValueError("mode must be xy, xz, or yz")


def normalize_2d(points_2d, scale=1.0):
    """
    Center + normalize 2D points for prettier plotting.
    """
    pts = points_2d.copy()
    pts = pts - pts.mean(axis=0, keepdims=True)
    max_abs = np.max(np.abs(pts))
    if max_abs < 1e-8:
        max_abs = 1.0
    pts = pts / max_abs * scale
    return pts


def weight_state(w):
    """
    Convert numeric weight to qualitative label.
    """
    if w > 1.05:
        return "reliable"
    elif w < 0.95:
        return "suppressed"
    else:
        return "neutral"


def weight_color(w):
    """
    Map weight to a paper-friendly color.
    """
    if w > 1.05:
        return "#2ca02c"   # green
    elif w < 0.95:
        return "#d62728"   # red
    else:
        return "#7f7f7f"   # gray


def add_round_box(ax, x, y, w, h, text="", fontsize=12,
                  fc="white", ec="black", lw=1.8,
                  radius=0.03, text_weight="normal"):
    """
    Add a rounded rectangle box.
    (x, y) is lower-left corner in figure coordinates [0,1].
    """
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.008,rounding_size={radius}",
        linewidth=lw,
        edgecolor=ec,
        facecolor=fc,
        transform=ax.transAxes
    )
    ax.add_patch(patch)

    if text:
        ax.text(
            x + w / 2.0,
            y + h / 2.0,
            text,
            transform=ax.transAxes,
            ha="center",
            va="center",
            fontsize=fontsize,
            fontweight=text_weight
        )

    return patch


def add_arrow(ax, start, end, lw=1.8, style="-|>", mutation=18,
              connectionstyle="arc3,rad=0.0", color="black"):
    """
    Add arrow in figure coordinate system.
    start/end are (x,y) in ax.transAxes coordinates.
    """
    arr = FancyArrowPatch(
        start, end,
        arrowstyle=style,
        mutation_scale=mutation,
        linewidth=lw,
        color=color,
        connectionstyle=connectionstyle,
        transform=ax.transAxes
    )
    ax.add_patch(arr)
    return arr


def draw_keypoint_panel(ax, x, y, w, h, points_2d, weights):
    """
    Draw observation panel with keypoints and object silhouette.
    """
    # outer panel
    add_round_box(
        ax, x, y, w, h,
        text="",
        fc="#fbfbfb",
        ec="black",
        lw=1.8
    )

    ax.text(
        x + 0.02, y + h - 0.035,
        "Observation at frame t",
        transform=ax.transAxes,
        fontsize=13,
        fontweight="bold",
        va="top"
    )

    # inner plotting region
    inner_x = x + 0.04
    inner_y = y + 0.08
    inner_w = w * 0.58
    inner_h = h * 0.70

    # background rectangle
    rect = Rectangle(
        (inner_x, inner_y), inner_w, inner_h,
        linewidth=1.0,
        edgecolor="#cccccc",
        facecolor="#f2f2f2",
        transform=ax.transAxes
    )
    ax.add_patch(rect)

    # object polygon
    # use a quadrilateral connecting keypoints in a stable order
    order = [0, 2, 3, 1]
    pts = points_2d[order]
    pts_min = pts.min(axis=0)
    pts_max = pts.max(axis=0)

    # rescale to panel
    rescaled = []
    for p in points_2d:
        px = (p[0] - pts_min[0]) / (pts_max[0] - pts_min[0] + 1e-8)
        py = (p[1] - pts_min[1]) / (pts_max[1] - pts_min[1] + 1e-8)
        sx = inner_x + 0.12 * inner_w + px * 0.76 * inner_w
        sy = inner_y + 0.12 * inner_h + py * 0.76 * inner_h
        rescaled.append([sx, sy])
    rescaled = np.array(rescaled)

    poly = Polygon(
        rescaled[order],
        closed=True,
        facecolor="#d9d9d9",
        edgecolor="#8c8c8c",
        linewidth=1.8,
        alpha=0.85,
        transform=ax.transAxes
    )
    ax.add_patch(poly)

    # draw dashed edges
    closed_order = [0, 2, 3, 1, 0]
    for i in range(len(closed_order) - 1):
        p1 = rescaled[closed_order[i]]
        p2 = rescaled[closed_order[i + 1]]
        line = Line2D(
            [p1[0], p2[0]],
            [p1[1], p2[1]],
            linestyle="--",
            linewidth=1.2,
            color="#6baed6",
            transform=ax.transAxes
        )
        ax.add_line(line)

    # draw keypoints
    for i in range(4):
        p = rescaled[i]
        wc = weight_color(weights[i])
        circ = Circle(
            (p[0], p[1]),
            radius=0.011,
            facecolor=wc,
            edgecolor="black",
            linewidth=1.4,
            transform=ax.transAxes
        )
        ax.add_patch(circ)

        ax.text(
            p[0] + 0.012, p[1] + 0.006,
            f"kp{i}",
            transform=ax.transAxes,
            fontsize=10,
            fontweight="bold"
        )

    # right-side explanation text
    txt_x = x + w * 0.68
    txt_y = y + h * 0.72

    ax.text(
        txt_x, txt_y,
        "Keypoint reliability",
        transform=ax.transAxes,
        fontsize=12,
        fontweight="bold"
    )

    for i in range(4):
        yi = txt_y - 0.055 - i * 0.055
        label = weight_state(weights[i])
        ax.text(
            txt_x, yi,
            f"kp{i}: w={weights[i]:.2f}  ({label})",
            transform=ax.transAxes,
            fontsize=10,
            color=weight_color(weights[i])
        )


def draw_uniform_vs_adaptive(ax, x, y, w, h, weights):
    """
    Draw a comparison panel:
    uniform weight vs adaptive weight.
    """
    add_round_box(
        ax, x, y, w, h,
        text="",
        fc="#ffffff",
        ec="black",
        lw=1.8
    )

    ax.text(
        x + 0.02, y + h - 0.035,
        "Uniform vs Adaptive weighting",
        transform=ax.transAxes,
        fontsize=13,
        fontweight="bold",
        va="top"
    )

    # baseline
    ax.text(
        x + 0.03, y + h - 0.09,
        "Conventional tracking",
        transform=ax.transAxes,
        fontsize=11,
        fontweight="bold"
    )
    ax.text(
        x + 0.03, y + h - 0.13,
        r"$w=[1,1,1,1]$",
        transform=ax.transAxes,
        fontsize=14
    )

    # RA-KPA
    ax.text(
        x + 0.03, y + h - 0.21,
        "RA-KPA",
        transform=ax.transAxes,
        fontsize=11,
        fontweight="bold"
    )
    ax.text(
        x + 0.03, y + h - 0.25,
        rf"$w=[{weights[0]:.2f}, {weights[1]:.2f}, {weights[2]:.2f}, {weights[3]:.2f}]$",
        transform=ax.transAxes,
        fontsize=14
    )

    # small bars
    base_x = x + 0.42 * w
    base_y = y + 0.14 * h
    bar_w = 0.09 * w
    gap = 0.04 * w
    max_h = 0.40 * h

    # baseline line
    ax.text(
        base_x - 0.12 * w, base_y + max_h + 0.015,
        "uniform",
        transform=ax.transAxes,
        fontsize=9
    )

    for i in range(4):
        xi = base_x + i * (bar_w + gap)
        # dashed uniform bar height = 1
        ax.add_patch(Rectangle(
            (xi, base_y), bar_w, max_h * 0.52,
            linewidth=1.0, edgecolor="#999999",
            facecolor="#e6e6e6",
            linestyle="--",
            transform=ax.transAxes
        ))

        # adaptive bar
        hh = (weights[i] / 1.5) * max_h
        ax.add_patch(Rectangle(
            (xi, base_y), bar_w, hh,
            linewidth=1.0,
            edgecolor="black",
            facecolor=weight_color(weights[i]),
            alpha=0.85,
            transform=ax.transAxes
        ))

        ax.text(
            xi + bar_w / 2,
            base_y - 0.03,
            f"kp{i}",
            transform=ax.transAxes,
            ha="center",
            fontsize=9
        )


def draw_ra_kpa_core(ax, x, y, w, h):
    """
    Draw central RA-KPA module.
    """
    add_round_box(
        ax, x, y, w, h,
        text="",
        fc="#f7fbff",
        ec="#2171b5",
        lw=2.2
    )

    ax.text(
        x + w / 2, y + h - 0.03,
        "RA-KPA core module",
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=14,
        fontweight="bold",
        color="#08519c"
    )

    # inner sub-boxes
    box_w = 0.24 * w
    box_h = 0.36 * h
    y0 = y + 0.28 * h

    x1 = x + 0.04 * w
    x2 = x + 0.38 * w
    x3 = x + 0.72 * w

    add_round_box(
        ax, x1, y0, box_w, box_h,
        text="Reliability\nestimation\n$\\,r_i^t$",
        fontsize=12,
        fc="white",
        ec="#6baed6",
        lw=1.6
    )

    add_round_box(
        ax, x2, y0, box_w, box_h,
        text="Adaptive\nweighting\n$\\,w_i^t$",
        fontsize=12,
        fc="white",
        ec="#6baed6",
        lw=1.6
    )

    add_round_box(
        ax, x3, y0, box_w, box_h,
        text="Weighted\noptimization",
        fontsize=12,
        fc="white",
        ec="#6baed6",
        lw=1.6
    )

    # arrows between inner boxes
    add_arrow(ax,
              (x1 + box_w, y0 + box_h / 2),
              (x2, y0 + box_h / 2),
              lw=1.8)

    add_arrow(ax,
              (x2 + box_w, y0 + box_h / 2),
              (x3, y0 + box_h / 2),
              lw=1.8)

    # formulas below
    ax.text(
        x1 + box_w / 2, y + 0.16 * h,
        "motion + temporal consistency",
        transform=ax.transAxes,
        ha="center", fontsize=10
    )

    ax.text(
        x2 + box_w / 2, y + 0.16 * h,
        r"$w_i^t=\alpha w_i^{t-1} + (1-\alpha)\hat{w}_i^t$",
        transform=ax.transAxes,
        ha="center", fontsize=11
    )

    ax.text(
        x3 + box_w / 2, y + 0.16 * h,
        r"$\sum_i w_i^t \|e_i\|^2$",
        transform=ax.transAxes,
        ha="center", fontsize=13
    )


def draw_temporal_panel(ax, x, y, w, h, weight_history, frames=(50, 282, 376)):
    """
    Draw temporal online adaptation with several time snapshots.
    """
    add_round_box(
        ax, x, y, w, h,
        text="",
        fc="#ffffff",
        ec="black",
        lw=1.8
    )

    ax.text(
        x + 0.02, y + h - 0.035,
        "Online temporal adaptation",
        transform=ax.transAxes,
        fontsize=13,
        fontweight="bold",
        va="top"
    )

    # explanatory text
    ax.text(
        x + 0.02, y + h - 0.08,
        "Weights evolve over time and are updated from keypoint history.",
        transform=ax.transAxes,
        fontsize=10
    )

    # draw 3 mini columns
    col_w = 0.22 * w
    gap = 0.07 * w
    start_x = x + 0.06 * w
    top_y = y + 0.16 * h
    max_bar_h = 0.45 * h
    bar_w = 0.035 * w

    for idx, f in enumerate(frames):
        cur_x = start_x + idx * (col_w + gap)
        ax.text(
            cur_x + 0.06 * w,
            y + h - 0.13,
            f"frame {f}",
            transform=ax.transAxes,
            ha="center",
            fontsize=10,
            fontweight="bold"
        )

        w4 = weight_history[f][:4]

        for k in range(4):
            xi = cur_x + k * (bar_w + 0.012 * w)
            hh = (w4[k] / 1.5) * max_bar_h
            ax.add_patch(Rectangle(
                (xi, top_y), bar_w, hh,
                facecolor=weight_color(w4[k]),
                edgecolor="black",
                linewidth=0.8,
                transform=ax.transAxes
            ))
            ax.text(
                xi + bar_w / 2,
                top_y - 0.028,
                f"k{k}",
                transform=ax.transAxes,
                ha="center",
                fontsize=8
            )

        # baseline line
        base_h = (1.0 / 1.5) * max_bar_h
        line = Line2D(
            [cur_x - 0.01 * w, cur_x + 4 * (bar_w + 0.012 * w)],
            [top_y + base_h, top_y + base_h],
            linestyle="--",
            linewidth=1.0,
            color="#777777",
            transform=ax.transAxes
        )
        ax.add_line(line)

    # arrow from left to right inside panel
    add_arrow(
        ax,
        (x + 0.25 * w, y + 0.08 * h),
        (x + 0.75 * w, y + 0.08 * h),
        lw=1.6
    )
    ax.text(
        x + 0.50 * w, y + 0.05 * h,
        "history accumulation and online update",
        transform=ax.transAxes,
        ha="center",
        fontsize=10
    )


def draw_result_panel(ax, x, y, w, h, ini_child_r, new_child_r):
    """
    Draw refined result panel.
    """
    add_round_box(
        ax, x, y, w, h,
        text="",
        fc="#f9f9f9",
        ec="black",
        lw=1.8
    )

    ax.text(
        x + 0.02, y + h - 0.035,
        "Tracking outcome",
        transform=ax.transAxes,
        fontsize=13,
        fontweight="bold",
        va="top"
    )

    ax.text(
        x + 0.04, y + h - 0.10,
        "Before RA-KPA:",
        transform=ax.transAxes,
        fontsize=11,
        fontweight="bold"
    )
    ax.text(
        x + 0.04, y + h - 0.14,
        f"child rotation error = {ini_child_r:.2f}°",
        transform=ax.transAxes,
        fontsize=11,
        color="#d62728"
    )

    ax.text(
        x + 0.04, y + h - 0.23,
        "After RA-KPA:",
        transform=ax.transAxes,
        fontsize=11,
        fontweight="bold"
    )
    ax.text(
        x + 0.04, y + h - 0.27,
        f"child rotation error = {new_child_r:.2f}°",
        transform=ax.transAxes,
        fontsize=11,
        color="#2ca02c"
    )

    gain = ini_child_r - new_child_r
    ax.text(
        x + 0.04, y + h - 0.37,
        f"error reduction = {gain:.2f}°",
        transform=ax.transAxes,
        fontsize=12,
        fontweight="bold"
    )

    ax.text(
        x + 0.04, y + 0.10,
        "Reliable keypoints receive\nhigher weights and dominate\npose refinement.",
        transform=ax.transAxes,
        fontsize=10
    )


# ============================================================
# 3. main figure
# ============================================================

def main():
    # --------------------------------------------------------
    # load data
    # --------------------------------------------------------
    if not os.path.exists(KP_PATH):
        raise FileNotFoundError(f"Missing file: {KP_PATH}")
    if not os.path.exists(WEIGHT_PATH):
        raise FileNotFoundError(f"Missing file: {WEIGHT_PATH}")
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"Missing file: {CSV_PATH}")

    kp_hist = np.load(KP_PATH)
    weight_hist = np.load(WEIGHT_PATH)
    df = pd.read_csv(CSV_PATH)

    print("kp_hist shape:", kp_hist.shape)
    print("weight_hist shape:", weight_hist.shape)
    print("csv shape:", df.shape)

    # --------------------------------------------------------
    # select representative frame
    # --------------------------------------------------------
    frame_id = 282

    child_kp_3d = kp_hist[frame_id]
    weights = weight_hist[frame_id][:4]   # only active child kps
    row = df.iloc[frame_id]

    ini_child_r = float(row["ini_child_r"])
    new_child_r = float(row["new_child_r"])

    child_kp_2d = project_to_2d(child_kp_3d, mode="xy")
    child_kp_2d = normalize_2d(child_kp_2d, scale=1.0)

    # --------------------------------------------------------
    # create canvas
    # --------------------------------------------------------
    fig = plt.figure(figsize=(16, 9))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")

    # title
    ax.text(
        0.5, 0.955,
        "RA-KPA: Reliability-Aware Keypoint Adaptation for Articulated Tracking",
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=23,
        fontweight="bold"
    )

    # subtitle / one-line message
    ax.text(
        0.5, 0.918,
        "RA-KPA estimates temporal keypoint reliability and adapts optimization weights online.",
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=12
    )

    # --------------------------------------------------------
    # layout blocks
    # --------------------------------------------------------

    # Left top: real keypoint observation
    draw_keypoint_panel(
        ax,
        x=0.04, y=0.54, w=0.28, h=0.28,
        points_2d=child_kp_2d,
        weights=weights
    )

    # Left bottom: uniform vs adaptive
    draw_uniform_vs_adaptive(
        ax,
        x=0.04, y=0.25, w=0.28, h=0.22,
        weights=weights
    )

    # Center: RA-KPA core
    draw_ra_kpa_core(
        ax,
        x=0.36, y=0.43, w=0.38, h=0.34
    )

    # Right top: tracking outcome
    draw_result_panel(
        ax,
        x=0.78, y=0.54, w=0.18, h=0.24,
        ini_child_r=ini_child_r,
        new_child_r=new_child_r
    )

    # Bottom center: temporal adaptation panel
    draw_temporal_panel(
        ax,
        x=0.36, y=0.14, w=0.46, h=0.20,
        weight_history=weight_hist,
        frames=(50, 282, 376)
    )

    # --------------------------------------------------------
    # main arrows between blocks
    # --------------------------------------------------------

    # observation -> RA-KPA core
    add_arrow(ax, (0.32, 0.68), (0.36, 0.68), lw=2.0)

    # comparison -> RA-KPA core
    add_arrow(ax, (0.32, 0.36), (0.42, 0.43), lw=1.7)

    # RA-KPA core -> outcome
    add_arrow(ax, (0.74, 0.60), (0.78, 0.66), lw=2.0)

    # temporal panel -> RA-KPA core
    add_arrow(ax, (0.58, 0.34), (0.58, 0.43), lw=1.8)

    # RA-KPA core -> temporal panel (feedback)
    add_arrow(
        ax,
        (0.65, 0.43),
        (0.76, 0.33),
        lw=1.6,
        connectionstyle="arc3,rad=0.25"
    )

    # small labels for sections
    ax.text(0.18, 0.84, "(a) Observation & failure evidence",
            transform=ax.transAxes, ha="center", fontsize=13, fontweight="bold")
    ax.text(0.55, 0.80, "(b) RA-KPA method",
            transform=ax.transAxes, ha="center", fontsize=13, fontweight="bold")
    ax.text(0.87, 0.80, "(c) Tracking improvement",
            transform=ax.transAxes, ha="center", fontsize=13, fontweight="bold")
    ax.text(0.59, 0.36, "(d) Online adaptation over time",
            transform=ax.transAxes, ha="center", fontsize=13, fontweight="bold")

    # footnote
    ax.text(
        0.5, 0.045,
        "Example frame: 282. Only the first four weights are shown because they correspond to the active child keypoints used in optimization.",
        transform=ax.transAxes,
        ha="center",
        fontsize=10
    )

    # save
    plt.savefig(SAVE_PNG, dpi=300, bbox_inches="tight")
    plt.savefig(SAVE_SVG, bbox_inches="tight")
    plt.close()

    print("Saved PNG:", SAVE_PNG)
    print("Saved SVG:", SAVE_SVG)


if __name__ == "__main__":
    main()