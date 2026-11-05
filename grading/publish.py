"""用 GitHub 文件 SHA 检测并发更新，避免两次提交覆盖彼此。"""
import base64
import json
import os
import time
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

repo = os.environ["GITHUB_REPOSITORY"]
url = f"https://api.github.com/repos/{repo}/contents/scores.json"
headers = {"Authorization": "Bearer "+os.environ["GH_TOKEN"], "Accept":"application/vnd.github+json"}
event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
issue = event.get("issue")
key = str(issue["number"]) if issue else "selfcheck"
link = f"https://github.com/{repo}/actions/runs/"+os.environ["GITHUB_RUN_ID"]
row = {"ok":os.environ["GRADED"] == "success", "run":link}
if issue:
    row["account"] = issue["user"]["login"]
if row["ok"]:
    row.update(json.loads(Path("result.json").read_text()))
for i in range(12):
    with urlopen(Request(url+"?ref=score-data", headers=headers), timeout=20) as response:
        file = json.load(response)
    scores = json.loads(base64.b64decode(file["content"]))
    scores[key] = row
    content = base64.b64encode(json.dumps(scores, ensure_ascii=False,indent=1).encode()).decode()
    body = {"branch":"score-data","message":"更新评分 "+key,"sha":file["sha"],"content":content}
    try:
        with urlopen(Request(url,headers=headers,data=json.dumps(body).encode(),method="PUT"),timeout=25):
            break
    except HTTPError as e:
        if e.code not in (409,422) or i==11:
            raise
        time.sleep(1+i/2)
