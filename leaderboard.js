const repo = "lllolaa330/wind-prediction-assignment";
const best = document.querySelector("#best");
const recent = document.querySelector("#recent");
const statusText = document.querySelector("#status");
const button = document.querySelector("#refresh");

function render(scores) {
  const attempts = Object.entries(scores).filter(([id]) => /^\d+$/.test(id));
  const ranked = attempts.filter(([, row]) => row.ok)
    .sort(([a, x], [b, y]) => x.nll - y.nll || Number(a) - Number(b));
  best.replaceChildren();
  const accounts = new Set();
  for (const [, row] of ranked) {
    if (accounts.has(row.account)) continue;
    accounts.add(row.account);
    const tr = best.insertRow();
    for (const value of [accounts.size, row.team, row.nll.toFixed(5), row.angle.toFixed(3),
      row.speed.toFixed(3), row.params, row.epochs]) tr.insertCell().textContent = value;
  }
  recent.replaceChildren();
  for (const [id, row] of attempts.sort(([a], [b]) => Number(b)-Number(a)).slice(0, 12)) {
    const p = document.createElement("p");
    const a = document.createElement("a");
    a.href = "https://github.com/" + repo + "/issues/" + id;
    a.textContent = "#" + id + " " + (row.team || row.account);
    p.append(a, row.ok ? "　NLL " + row.nll.toFixed(5) : "　评分失败，请查看运行记录后重新提交。");
    if (!row.ok) {
      const log = document.createElement("a");
      log.href = row.run;
      log.textContent = "运行记录";
      p.append(log);
    }
    recent.append(p);
  }
  const empty = accounts.size ? "" : "暂无学生成绩。";
  statusText.textContent = empty + "上次刷新 " + new Date().toLocaleTimeString("zh-CN");
}

async function refresh() {
  if (button.disabled) return;
  button.disabled = true;
  try {
    const url = "https://raw.githubusercontent.com/" + repo + "/score-data/scores.json?t=" + Math.floor(Date.now()/10000);
    const response = await fetch(url, {cache: "no-store"});
    if (!response.ok) throw Error();
    render(await response.json());
  } catch {
    statusText.textContent = "暂时无法获取成绩，请稍后刷新。";
  } finally {
    button.disabled = false;
  }
}
button.addEventListener("click", refresh);
refresh();
setInterval(() => { if (!document.hidden) refresh(); }, 20000);
