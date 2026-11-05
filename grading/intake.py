"""读取 GitHub 表单，仅下载 GitHub 托管的 ZIP 附件。"""
import io
import json
import os
import re
import urllib.request
import zipfile
from pathlib import Path

LIMIT = 8 * 1024**2


def unpack(blob):
    with zipfile.ZipFile(io.BytesIO(blob)) as archive:
        files = [f for f in archive.infolist() if not f.is_dir() and
                 not f.filename.startswith("__MACOSX/") and not f.filename.endswith(".DS_Store")]
        if len(files) != 1 or Path(files[0].filename).name != "best_model.pt" or files[0].file_size > LIMIT:
            raise ValueError("ZIP 应只含 best_model.pt，且权重须小于 8 MiB")
        return archive.read(files[0])


def parse(issue):
    body = issue["body"].replace("\r", "")
    parts = re.split(r"^### (.+)\n", body, flags=re.M)
    fields = dict(zip(parts[1::2], (s.strip() for s in parts[2::2])))
    team = fields["队名"]
    if not 1 <= len(team) <= 40 or not team.isprintable():
        raise ValueError("队名须为 1 至 40 个可显示字符")
    epochs, params = (int(fields[k]) for k in ["实际训练轮次", "总参数量"])
    if not (1 <= epochs <= 10000000 and 1 <= params <= 250000):
        raise ValueError("请检查训练轮次和参数量")
    urls = re.findall(r"https://github\.com/user-attachments/(?:files/\d+/[\w.%+-]+\.zip|assets/[0-9a-fA-F-]{36})(?=[)\s]|$)", fields["模型附件"], re.I)
    if len(urls) != 1:
        raise ValueError("请上传一个 GitHub ZIP 附件")
    with urllib.request.urlopen(urls[0], timeout=30) as response:
        blob = response.read(LIMIT + 1)
    if len(blob) > LIMIT:
        raise ValueError("附件过大")
    return dict(team=team, epochs=epochs, params=params), unpack(blob)


if __name__ == "__main__":
    issue = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())["issue"]
    meta, weights = parse(issue)
    Path("entry.json").write_text(json.dumps(meta, ensure_ascii=False))
    Path("input.pt").write_bytes(weights)
