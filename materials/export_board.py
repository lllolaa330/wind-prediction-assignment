"""把已训练的共享 MLP 导出成打榜用 best_model.pt 和模型提交.zip。"""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

import torch
from torch import nn


def export_board(hidden_layers, output, activation="tanh", out_dir="board_export"):
    """按前向顺序传入隐藏层 Linear。output 为双输出 Linear 或 (mu_head, raw_rate_head)。"""
    layers = list(hidden_layers)
    if not 1 <= len(layers) <= 8 or activation not in ("tanh", "relu"):
        raise ValueError("请使用 1 至 8 个隐藏层，激活函数为 tanh 或 relu")
    state = {}
    size = 3
    for i, layer in enumerate(layers):
        if not isinstance(layer, nn.Linear) or layer.bias is None or layer.in_features != size or not 1 <= layer.out_features <= 512:
            raise ValueError("检查隐藏层顺序、维度和偏置")
        state[f"shared.{2*i}.weight"] = layer.weight.detach().cpu()
        state[f"shared.{2*i}.bias"] = layer.bias.detach().cpu()
        size = layer.out_features
    heads = [output] if isinstance(output, nn.Linear) else list(output)
    if [h.out_features for h in heads] not in ([2], [1,1]) or any(h.in_features != size or h.bias is None for h in heads):
        raise ValueError("输出层须依次给出 mu 和未经 Softplus 的实数")
    for key in ("weight", "bias"):
        state["head."+key] = torch.cat([getattr(h,key).detach().cpu() for h in heads])
    count = sum(t.numel() for t in state.values())
    if count > 250000:
        raise ValueError("参数量上限为 250000")
    dest = Path(out_dir)
    dest.mkdir(exist_ok=True, parents=True)
    pt = dest/"best_model.pt"
    torch.save(dict(widths=[h.out_features for h in layers],state=state,activation=activation),pt)
    with ZipFile(dest/"模型提交.zip", "w", ZIP_DEFLATED) as z:
        z.write(pt, pt.name)
    print(f"总参数量 {count}，请上传 {dest/'模型提交.zip'}")
