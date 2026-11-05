"""在无网络、无凭证的独立容器中，将权重转为有限大小的数值数组。"""
import json
import sys
from pathlib import Path

import torch

if sys.argv[1] == "smoke":
    # 零权重模型仅供教师验证流水线，不参与学生排名。
    state = {name: torch.zeros(shape) for name, shape in
             [("shared.0.weight",(2,3)), ("shared.0.bias",(2,)),
              ("head.weight",(2,2)), ("head.bias",(2,))]}
    torch.save({"widths":[2], "state":state}, sys.stdout.buffer)
    sys.exit()

ckpt = torch.load(Path("/input.pt"), map_location="cpu", weights_only=True)
widths = ckpt["widths"]
activation = ckpt.get("activation", "tanh")
if type(widths) is not list or not 1 <= len(widths) <= 8 or any(type(w) is not int or not 1 <= w <= 512 for w in widths):
    raise ValueError("隐藏层宽度或层数超出范围")
if activation not in ("tanh", "relu"):
    raise ValueError("仅接受 tanh 或 relu")
state = ckpt["state"]
expected = {}
dims = [3, *widths, 2]
for i, (a, b) in enumerate(zip(dims, dims[1:])):
    layer = "head" if i == len(widths) else f"shared.{2*i}"
    expected[layer+".weight"] = (b,a)
    expected[layer+".bias"] = (b,)
if set(state) != set(expected) or sum(t.numel() for t in state.values()) > 250000:
    raise ValueError("权重名称或参数量不符合约定")
values = []
for key, shape in expected.items():
    t = state[key]
    if type(t) is not torch.Tensor or t.layout != torch.strided or tuple(t.shape) != shape or t.dtype not in (torch.float32, torch.float64) or not t.isfinite().all():
        raise ValueError("张量形状、类型或数值无效")
    values.append(t.tolist())
json.dump({"activation":activation, "values":values}, sys.stdout, allow_nan=False)
