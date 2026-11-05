"""读取生成好的训练样本，画风向圆周散点图和风速散点图。

随机种子已在生成数据时由你设置，绘图直接使用同一批观测。
绘图逻辑仅供参考，可自行修改本脚本，换一个输入分量或进一步分析数据。
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def plot_data(X, theta, v, out_dir="results"):
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

    # 风速用普通散点图，与风向图使用同一批样本和同一输入分量。
    fig, ax = plt.subplots(figsize=(4, 2.8), layout="constrained")
    ax.scatter(x1, v, s=10, color="#2878B5", alpha=.55, linewidths=0)
    ax.set(xlabel=r"Input $x_1$", ylabel="Wind speed (m/s)", xlim=(-1.02, 1.02))
    ax.spines[["right", "top"]].set_visible(False)
    fig.savefig(out_dir / "speed.png", dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    with np.load("data/train.npz") as train:
        plot_data(train["X"], train["theta"], train["v"])
    print("两张图已保存到 results/direction.png 和 results/speed.png")
