"""在教师端根据净化后的数值权重重建前向计算。"""
import json
import math
import os
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "materials"))
from generate_data import generate_data


def score(weights, seed):
    x, theta, speed = generate_data(2000, seed)
    arrays = [np.asarray(t, dtype=np.float64) for t in weights["values"]]
    h = x
    for i in range(0, len(arrays), 2):
        h = h @ arrays[i].T + arrays[i+1]
        if i+2 < len(arrays):
            h = np.tanh(h) if weights["activation"] == "tanh" else np.maximum(h, 0)
    mu, raw = h.T
    rate = np.logaddexp(0, raw) + 1e-8
    delta = theta - mu
    metrics = dict(nll=float(np.mean(math.log(2*np.pi*np.i0(8.)) - 8*np.cos(delta) - np.log(rate) + rate*speed)),
                   angle=float(np.rad2deg(np.abs(np.arctan2(np.sin(delta),np.cos(delta)))).mean()),
                   speed=float(np.abs(1/rate-speed).mean()))
    if not all(map(math.isfinite, metrics.values())):
        raise ValueError("模型产生非有限指标")
    return dict(params=sum(t.size for t in arrays), **metrics)


if __name__ == "__main__":
    entry = json.loads(Path("entry.json").read_text())
    result = score(json.loads(Path("weights.json").read_text()), int(os.environ["TEST_SEED"]))
    if result["params"] != entry["params"]:
        raise ValueError("填报的参数量与权重不一致，实际为 "+str(result["params"]))
    Path("result.json").write_text(json.dumps({**entry, **result}, ensure_ascii=False))
