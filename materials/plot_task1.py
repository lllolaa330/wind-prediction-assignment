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

    # 两幅图用同一批样本，各自保留对应的纵轴单位。
    panels = [(theta, r"Wind direction $\theta$ (rad)", "direction"),
              (v, "Wind speed (m/s)", "speed")]
    for values, ylabel, name in panels:
        fig, ax = plt.subplots(figsize=(4.0, 2.8), layout="constrained")
        ax.scatter(x1, values, s=10, color="#2878B5", alpha=0.55, linewidths=0)
        ax.set(xlabel=r"Input $x_1$", ylabel=ylabel, xlim=(-1.02, 1.02))
        if name == "direction":
            ax.set_yticks([-np.pi, 0, np.pi], [r"$-\pi$", "0", r"$\pi$"])
        ax.spines[["right", "top"]].set_visible(False)
        fig.savefig(out_dir / f"{name}.png", dpi=180)
        plt.close(fig)
