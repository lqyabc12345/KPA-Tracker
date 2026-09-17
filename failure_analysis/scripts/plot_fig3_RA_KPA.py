import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# FIGURE 3: RA-KPA Online Reliability-Aware Adaptation
#
# Panel (a): reliability evolution over frames
# Panel (b): reliability-to-weight relation
# Panel (c): initial vs optimized child rotation error
#
# Inputs:
#   failure_analysis/results/reliability_history.npy
#   failure_analysis/results/online_weight_history.npy
#   failure_analysis/results/per_frame_results.csv
#
# Outputs:
#   failure_analysis/results/Figure3_RA_KPA.png
#   failure_analysis/results/Figure3_RA_KPA.pdf
# ============================================================


# =========================
# path setup
# =========================
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

RESULT_DIR = os.path.join(PROJECT_ROOT, "failure_analysis", "results")

RELIABILITY_PATH = os.path.join(RESULT_DIR, "reliability_history.npy")
WEIGHT_PATH = os.path.join(RESULT_DIR, "online_weight_history.npy")
CSV_PATH = os.path.join(RESULT_DIR, "per_frame_results.csv")

SAVE_PNG = os.path.join(RESULT_DIR, "Figure3_RA_KPA.png")
SAVE_PDF = os.path.join(RESULT_DIR, "Figure3_RA_KPA.pdf")


# =========================
# helper functions
# =========================
def load_data():
    """
    Load reliability, weights, and per-frame csv.
    """
    reliability = np.load(RELIABILITY_PATH)
    weights = np.load(WEIGHT_PATH)
    df = pd.read_csv(CSV_PATH)

    print("Loaded:")
    print("  reliability:", reliability.shape)
    print("  weights     :", weights.shape)
    print("  csv         :", df.shape)

    return reliability, weights, df


def prepare_weight_child(weights):
    """
    online_weight_history.npy may be:
      - (377, 4)
      - (377, 8)

    We only want the first 4 child keypoints.
    """
    if weights.ndim != 2:
        raise ValueError(f"weights should be 2D, got shape {weights.shape}")

    if weights.shape[1] < 4:
        raise ValueError(f"weights should have at least 4 columns, got {weights.shape}")

    child_weights = weights[:, :4]
    return child_weights


def prepare_reliability_full(reliability, total_frames):
    """
    reliability_history.npy is currently (374, 4),
    because the first few frames do not have enough temporal history.

    We pad it to (377, 4) with NaN in the first frames.
    """
    if reliability.ndim != 2:
        raise ValueError(f"reliability should be 2D, got shape {reliability.shape}")

    if reliability.shape[1] != 4:
        raise ValueError(
            f"reliability should have 4 columns for child keypoints, got {reliability.shape}"
        )

    full = np.full((total_frames, 4), np.nan, dtype=np.float32)

    start = total_frames - reliability.shape[0]
    if start < 0:
        raise ValueError(
            f"reliability has more rows than total_frames: {reliability.shape[0]} > {total_frames}"
        )

    full[start:, :] = reliability
    return full


def moving_average(x, window=9):
    """
    Simple moving average for smoother curves.
    NaNs are preserved at locations where the input neighborhood is invalid.
    """
    x = np.asarray(x, dtype=np.float32)

    if window <= 1:
        return x.copy()

    y = np.full_like(x, np.nan, dtype=np.float32)
    half = window // 2

    for i in range(len(x)):
        left = max(0, i - half)
        right = min(len(x), i + half + 1)
        chunk = x[left:right]
        valid = chunk[~np.isnan(chunk)]
        if len(valid) > 0:
            y[i] = valid.mean()

    return y


def setup_style():
    """
    Make the figure cleaner for paper usage.
    """
    plt.rcParams["font.size"] = 11
    plt.rcParams["axes.titlesize"] = 12
    plt.rcParams["axes.labelsize"] = 11
    plt.rcParams["legend.fontsize"] = 10
    plt.rcParams["figure.dpi"] = 150
    plt.rcParams["savefig.dpi"] = 300


# =========================
# plotting
# =========================
def plot_panel_a(ax, reliability_full):
    """
    Panel (a): reliability evolution over frames.
    """
    frames = np.arange(reliability_full.shape[0])

    labels = ["kp0", "kp1", "kp2", "kp3"]

    for k in range(4):
        y = reliability_full[:, k]
        y_smooth = moving_average(y, window=11)
        ax.plot(frames, y_smooth, linewidth=2, label=labels[k])

    ax.set_title("(a) Temporal reliability evolution")
    ax.set_xlabel("Frame")
    ax.set_ylabel("Reliability score")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper right", ncol=2)


def plot_panel_b(ax, reliability_full, child_weights):
    """
    Panel (b): reliability vs weight relation.

    Because the first few frames of reliability are NaN,
    we only keep valid entries for scatter.
    """
    labels = ["kp0", "kp1", "kp2", "kp3"]

    for k in range(4):
        r = reliability_full[:, k]
        w = child_weights[:, k]

        valid = ~np.isnan(r)
        ax.scatter(
            r[valid],
            w[valid],
            s=16,
            alpha=0.55,
            label=labels[k]
        )

    ax.set_title("(b) Reliability drives adaptive weighting")
    ax.set_xlabel("Reliability score")
    ax.set_ylabel("Adaptive weight")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="best", ncol=2)


def plot_panel_c(ax, df):
    """
    Panel (c): initial vs optimized child rotation error.
    """
    frames = np.arange(len(df))

    ini_err = df["ini_child_r"].to_numpy(dtype=np.float32)
    new_err = df["new_child_r"].to_numpy(dtype=np.float32)

    ax.plot(
        frames,
        moving_average(ini_err, window=9),
        linewidth=2,
        label="Initial child rotation error"
    )

    ax.plot(
        frames,
        moving_average(new_err, window=9),
        linewidth=2,
        label="Optimized child rotation error"
    )

    mean_ini = float(np.mean(ini_err))
    mean_new = float(np.mean(new_err))

    ax.set_title("(c) Tracking refinement over time")
    ax.set_xlabel("Frame")
    ax.set_ylabel("Child rotation error (deg)")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper right")

    text = (
        f"mean initial = {mean_ini:.2f}°\n"
        f"mean optimized = {mean_new:.2f}°\n"
        f"relative drop = {(mean_ini - mean_new) / mean_ini * 100:.1f}%"
    )

    ax.text(
        0.02,
        0.98,
        text,
        transform=ax.transAxes,
        va="top",
        ha="left",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.85)
    )


def main():
    setup_style()

    reliability, weights, df = load_data()

    total_frames = len(df)

    child_weights = prepare_weight_child(weights)
    reliability_full = prepare_reliability_full(reliability, total_frames)

    print("Prepared:")
    print("  child_weights    :", child_weights.shape)
    print("  reliability_full :", reliability_full.shape)

    fig, axes = plt.subplots(1, 3, figsize=(16, 4.6))
    plt.subplots_adjust(wspace=0.28)

    plot_panel_a(axes[0], reliability_full)
    plot_panel_b(axes[1], reliability_full, child_weights)
    plot_panel_c(axes[2], df)

    fig.suptitle(
        "Figure 3. Online Reliability-Aware Keypoint Adaptation",
        fontsize=14,
        y=1.03
    )

    plt.tight_layout()

    plt.savefig(SAVE_PNG, bbox_inches="tight")
    plt.savefig(SAVE_PDF, bbox_inches="tight")

    print("Saved:")
    print(" ", SAVE_PNG)
    print(" ", SAVE_PDF)


if __name__ == "__main__":
    main()