"""在生成训练数据后调用 plot_task1(X_train, theta_train, v_train)。"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def plot_task1(X, theta, v, out_dir="results"):
    """X 的形状为 (N, 3)，theta 为弧度，v 的单位为 m/s。"""
    x1 = np.asarray(X)[:, 0]
    theta = np.asarray(theta).reshape(-1)
    v = np.asarray(v).reshape(-1)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # 角度取风向，半径平移 1 以容纳负输入，刻度显示原始 x1。
    fig, ax = plt.subplots(figsize=(4, 3.3), subplot_kw={"projection": "polar"},
                           layout="constrained")
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.scatter(theta, x1 + 1, s=9, alpha=.5, linewidths=0, color="#2878B5")
    ax.set_ylim(0, 2)
    ax.set_yticks([.5, 1, 1.5, 2], labels=["−0.5", "0", "0.5", "1"])
    ax.set_rlabel_position(55)
    ax.tick_params(axis="y", labelsize=8)
    ax.grid(color="#bcc9cd", linewidth=.7)
    ax.set_title(r"Radial scale: input $x_1$", fontsize=11)
    fig.savefig(out_dir / "direction.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(4, 2.8), layout="constrained")
    ax.scatter(x1, v, s=10, color="#2878B5", alpha=.55, linewidths=0)
    ax.set(xlabel=r"Input $x_1$", ylabel="Wind speed (m/s)", xlim=(-1.02, 1.02))
    ax.spines[["right", "top"]].set_visible(False)
    fig.savefig(out_dir / "speed.png", dpi=180)
    plt.close(fig)
