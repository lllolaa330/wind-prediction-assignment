"""习题 5.10+ 数据生成器，按课程提供的 PDF 整理。"""

import math

import torch
from torch.distributions import VonMises


def wrap_angle(a):
    """将弧度映射到 [-pi, pi)。"""
    return torch.remainder(a + math.pi, 2 * math.pi) - math.pi


def make_wind_data(n=5000, seed=2026, kappa=8.0):
    """生成 n 条模拟观测。x 的形状为 [n, 3]，其余字段形状均为 [n]。"""
    if n <= 0 or kappa <= 0:
        raise ValueError("n and kappa must be positive")

    g = torch.Generator(device="cpu").manual_seed(seed)
    x = 2 * torch.rand(n, 3, generator=g) - 1
    x1, x2, x3 = x.unbind(dim=1)

    # 所有角度均用弧度计算。
    mu = wrap_angle(
        2.8 + 1.1 * torch.sin(math.pi * x1) + 0.65 * x2 - 0.4 * x3
    )
    mean_speed = (
        2.5 + 1.2 * torch.sigmoid(2 * x1 - 0.8 * x2) + 0.7 * x3.square()
    )
    rate = 1.0 / mean_speed

    with torch.random.fork_rng(devices=[]):
        torch.manual_seed(seed + 100_003)
        direction = VonMises(mu, torch.full_like(mu, kappa)).sample()

    u = torch.rand(n, generator=g).clamp(min=1e-7, max=1 - 1e-7)
    speed = -torch.log(u) / rate
    return {
        "x": x,
        "direction": direction,
        "speed": speed,
        "mu_true": mu,
        "rate_true": rate,
        "mean_speed_true": mean_speed,
    }


if __name__ == "__main__":
    # 示例种子沿用讲义。教师另行生成隐藏测试集。
    train = make_wind_data(n=5000, seed=100)
    val = make_wind_data(n=1000, seed=200)
    for name, data in [("Training", train), ("Validation", val)]:
        print(name, {key: tuple(data[key].shape) for key in ("x", "direction", "speed")})
