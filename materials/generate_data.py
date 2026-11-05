"""按作业公式生成训练集和验证集。请自己选两个不同的随机种子，并记在 README 中。"""
import argparse
from pathlib import Path

import numpy as np


def generate_data(n, seed):
    """返回输入 X（n 行 3 列）、风向 theta（弧度）和风速 v（m/s）。"""
    rng = np.random.default_rng(seed)
    X = rng.uniform(-1, 1, size=(n, 3))
    x1, x2, x3 = X.T

    # 先计算中心风向，再从 von Mises 分布中抽取每条观测。
    mu = 2.8 + 1.1 * np.sin(np.pi * x1) + 0.65 * x2 - 0.4 * x3
    mu = (mu + np.pi) % (2 * np.pi) - np.pi
    theta = rng.vonmises(mu, kappa=8)

    # NumPy 的指数分布接收平均风速 scale，它等于速率参数的倒数。
    sigmoid = 1 / (1 + np.exp(-(2 * x1 - 0.8 * x2)))
    mean_speed = 2.5 + 1.2 * sigmoid + 0.7 * x3**2
    v = rng.exponential(scale=mean_speed)
    return X, theta, v


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--train-seed", type=int, required=True, help="自选训练集种子")
    parser.add_argument("--val-seed", type=int, required=True, help="自选验证集种子")
    args = parser.parse_args()
    if min(args.train_seed, args.val_seed) < 0 or args.train_seed == args.val_seed:
        parser.error("请为训练集和验证集选择两个不同的非负整数种子。")

    folder = Path("data")
    folder.mkdir(exist_ok=True)
    for name, n, seed in [("train", 5000, args.train_seed), ("val", 1000, args.val_seed)]:
        X, theta, v = generate_data(n, seed)
        path = folder / f"{name}.npz"
        np.savez(path, X=X, theta=theta, v=v, seed=seed)
        print(f"{path} 已保存，共 {n} 条，随机种子为 {seed}")
