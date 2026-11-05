# 习题 5.10+ · 风向与风速的联合概率预测

[打开学生作业网页](https://lllolaa330.github.io/wind-prediction-assignment/)

两人一组，用 Python 和 PyTorch 完成五项任务。用 [generate_data.py](materials/generate_data.py) 生成数据，自选并记录训练和验证用的两个不同随机种子。[plot_data.py](materials/plot_data.py) 演示风向圆周图和风速散点图，可按需要改写。分工、评分和提交清单都在网页上。

网页由 GitHub Pages 从 `main` 分支的 `index.html` 发布。

[公开模型排行榜](https://lllolaa330.github.io/wind-prediction-assignment/leaderboard.html) 提供提交入口、权重格式和评分规则。学生通过打榜 Issue 表单上传 ZIP，每次新建提交触发一次 GitHub Actions 评测。训练轮次为学生填报，参数量由权重核对。

教师在 Actions secret `WIND_TEST_SEED` 保存固定种子，评测使用 NumPy 2.2.6 和 2,000 条样本。工作流在无网络、无凭证的限额容器中读取权重，再由教师代码根据数值数组评分。请在同一轮打榜中固定种子、生成公式与评分代码。成绩存于 `score-data` 分支的 scores.json。手动运行“模型打榜”可用零权重模型自检，自检记录不参与排名。正式验收若要独立评价，可另取未用于打榜的种子。
