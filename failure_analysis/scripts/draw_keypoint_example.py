"""
Draw keypoint example asset for RA-KPA paper figure.

Purpose
-------
Generate a clean visual asset from one selected frame:
1. show the 4 active child keypoints in 2D projection
2. show their adaptive weights
3. highlight which keypoints are emphasized or suppressed

Input
-----
- failure_analysis/results/pred_child_kp_history.npy
- failure_analysis/results/online_weight_history.npy

Output
------
- failure_analysis/results/keypoint_example_frame282.svg
- failure_analysis/results/keypoint_example_frame282.png

Usage
-----
python failure_analysis/scripts/draw_keypoint_example.py
python failure_analysis/scripts/draw_keypoint_example.py --frame 282
"""

import os
import argparse
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# 1. Helper: project 3D keypoints to 2D
# ============================================================
def project_to_2d(points_3d, mode="xy"):
    """
    Convert 3D keypoints to 2D for paper illustration.

    Parameters
    ----------
    points_3d : np.ndarray
        shape = (N, 3)
    mode : str
        "xy", "xz", or "yz"

    Returns
    -------
    points_2d : np.ndarray
        shape = (N, 2)
    """
    if mode == "xy":
        return points_3d[:, [0, 1]]
    elif mode == "xz":
        return points_3d[:, [0, 2]]
    elif mode == "yz":
        return points_3d[:, [1, 2]]
    else:
        raise ValueError("mode must be one of: xy, xz, yz")


# ============================================================
# 2. Helper: normalize 2D coordinates for prettier layout
# ============================================================
def normalize_points(points_2d, target_scale=1.0):
    """
    Normalize 2D points into a compact display range,
    while preserving relative geometry.

    Parameters
    ----------
    points_2d : np.ndarray
        shape = (N, 2)
    target_scale : float
        target display size

    Returns
    -------
    norm_pts : np.ndarray
        normalized 2D points
    """
    pts = points_2d.copy()

    center = pts.mean(axis=0, keepdims=True)
    pts = pts - center

    max_abs = np.max(np.abs(pts))
    if max_abs < 1e-8:
        max_abs = 1.0

    pts = pts / max_abs * target_scale
    return pts


# ============================================================
# 3. Helper: infer reliability label from weight
# ============================================================
def weight_label(w):
    """
    Convert weight value to qualitative label.
    """
    if w > 1.05:
        return "reliable"
    elif w < 0.95:
        return "suppressed"
    else:
        return "neutral"


# ============================================================
# 4. Main
# ============================================================
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--frame",
        type=int,
        default=282,
        help="Frame index to visualize. Default: 282"
    )
    parser.add_argument(
        "--proj",
        type=str,
        default="xy",
        choices=["xy", "xz", "yz"],
        help="2D projection mode. Default: xy"
    )
    args = parser.parse_args()

    # --------------------------------------------------------
    # Project root
    # --------------------------------------------------------
    project_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../..")
    )

    result_dir = os.path.join(
        project_root,
        "failure_analysis",
        "results"
    )

    kp_path = os.path.join(
        result_dir,
        "pred_child_kp_history.npy"
    )

    weight_path = os.path.join(
        result_dir,
        "online_weight_history.npy"
    )

    # --------------------------------------------------------
    # Check input files
    # --------------------------------------------------------
    if not os.path.exists(kp_path):
        raise FileNotFoundError(f"Missing file: {kp_path}")

    if not os.path.exists(weight_path):
        raise FileNotFoundError(f"Missing file: {weight_path}")

    # --------------------------------------------------------
    # Load data
    # --------------------------------------------------------
    kp_history = np.load(kp_path)
    weight_history = np.load(weight_path)

    print("=" * 60)
    print("DRAW KEYPOINT EXAMPLE")
    print("=" * 60)
    print("kp_history shape:", kp_history.shape)
    print("weight_history shape:", weight_history.shape)

    # --------------------------------------------------------
    # Frame validity
    # --------------------------------------------------------
    num_frames = kp_history.shape[0]
    frame_id = args.frame

    if frame_id < 0 or frame_id >= num_frames:
        raise ValueError(
            f"frame {frame_id} out of range. valid range: [0, {num_frames-1}]"
        )

    # --------------------------------------------------------
    # Extract frame data
    # --------------------------------------------------------
    # keypoints: expected shape (4,3)
    child_kp_3d = kp_history[frame_id]

    # weights: current file stores 8 values, but only first 4 correspond
    # to the active child keypoints used in our paper analysis.
    frame_weight = weight_history[frame_id]

    if frame_weight.shape[0] < 4:
        raise ValueError(
            f"weight dimension too small: got {frame_weight.shape[0]}, expected >= 4"
        )

    active_weight = frame_weight[:4]

    print("frame:", frame_id)
    print("child_kp_3d shape:", child_kp_3d.shape)
    print("active_weight:", active_weight)

    # --------------------------------------------------------
    # Project 3D -> 2D
    # --------------------------------------------------------
    child_kp_2d = project_to_2d(child_kp_3d, mode=args.proj)
    child_kp_2d = normalize_points(child_kp_2d, target_scale=1.0)

    # --------------------------------------------------------
    # Output paths
    # --------------------------------------------------------
    svg_path = os.path.join(
        result_dir,
        f"keypoint_example_frame{frame_id}.svg"
    )

    png_path = os.path.join(
        result_dir,
        f"keypoint_example_frame{frame_id}.png"
    )

    # --------------------------------------------------------
    # Create figure
    # --------------------------------------------------------
    fig = plt.figure(figsize=(10, 5))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.1, 1.0])

    ax_geom = fig.add_subplot(gs[0, 0])
    ax_weight = fig.add_subplot(gs[0, 1])

    fig.suptitle(
        f"RA-KPA Keypoint Example (frame {frame_id})",
        fontsize=16,
        fontweight="bold"
    )

    # ========================================================
    # Left panel: keypoint geometry
    # ========================================================
    ax_geom.set_title("(a) Child Keypoint Observation", fontsize=13)

    x = child_kp_2d[:, 0]
    y = child_kp_2d[:, 1]

    # Draw a simple polygon to suggest object structure
    # Order chosen to create a readable quadrilateral:
    # kp0 -> kp2 -> kp3 -> kp1 -> kp0
    poly_order = [0, 2, 3, 1, 0]
    ax_geom.plot(
        x[poly_order],
        y[poly_order],
        linestyle="--",
        linewidth=1.5,
        alpha=0.6
    )

    # Scatter keypoints
    for i in range(4):
        w = active_weight[i]
        label = weight_label(w)

        # choose marker size based on weight
        size = 250 + 120 * (w - 1.0)

        # choose alpha and edge emphasis
        if label == "reliable":
            edge_lw = 2.5
        elif label == "suppressed":
            edge_lw = 1.2
        else:
            edge_lw = 1.8

        ax_geom.scatter(
            x[i],
            y[i],
            s=size,
            edgecolors="black",
            linewidths=edge_lw,
            zorder=3
        )

        ax_geom.text(
            x[i] + 0.04,
            y[i] + 0.04,
            f"kp{i}\nw={w:.2f}",
            fontsize=10,
            va="center"
        )

    ax_geom.axhline(0, linewidth=0.8, alpha=0.2)
    ax_geom.axvline(0, linewidth=0.8, alpha=0.2)

    ax_geom.set_aspect("equal")
    ax_geom.set_xlim(-1.4, 1.4)
    ax_geom.set_ylim(-1.4, 1.4)
    ax_geom.set_xlabel(f"{args.proj[0].upper()} axis")
    ax_geom.set_ylabel(f"{args.proj[1].upper()} axis")

    # reduce clutter for paper asset
    ax_geom.set_xticks([])
    ax_geom.set_yticks([])

    # ========================================================
    # Right panel: adaptive weight
    # ========================================================
    ax_weight.set_title("(b) Reliability-Aware Weight", fontsize=13)

    kp_names = [f"kp{i}" for i in range(4)]
    bars = ax_weight.bar(kp_names, active_weight)

    ax_weight.axhline(
        1.0,
        linestyle="--",
        linewidth=1.5,
        alpha=0.8
    )

    ax_weight.text(
        3.35,
        1.02,
        "uniform weight",
        fontsize=9,
        va="bottom"
    )

    ax_weight.set_ylabel("Adaptive weight")
    ax_weight.set_ylim(0.4, max(1.6, float(np.max(active_weight) + 0.15)))

    for i, bar in enumerate(bars):
        h = bar.get_height()
        label = weight_label(h)

        ax_weight.text(
            bar.get_x() + bar.get_width() / 2,
            h + 0.03,
            f"{h:.2f}",
            ha="center",
            va="bottom",
            fontsize=10
        )

        ax_weight.text(
            bar.get_x() + bar.get_width() / 2,
            0.45,
            label,
            ha="center",
            va="bottom",
            fontsize=9,
            rotation=90
        )

    # ========================================================
    # Bottom annotation / explanation
    # ========================================================
    fig.text(
        0.5,
        0.02,
        "Only the first 4 weights are visualized here, because they correspond to the active child keypoints used in optimization.",
        ha="center",
        fontsize=9
    )

    plt.tight_layout(rect=[0, 0.05, 1, 0.95])

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------
    plt.savefig(svg_path, bbox_inches="tight")
    plt.savefig(png_path, dpi=300, bbox_inches="tight")
    plt.close()

    print("Saved SVG:", svg_path)
    print("Saved PNG:", png_path)


if __name__ == "__main__":
    main()