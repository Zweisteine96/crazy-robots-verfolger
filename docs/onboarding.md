# 新协作者入门（Onboarding）

## 这个项目做什么

追踪机器人与 AI 领域重要研究者 / 实验室 2024 年以来的论文，从中归纳技术趋势，并把这些趋势与项目所有者的研究方向
（physics-grounded human-motion prediction、uncertainty-aware crowd navigation、humanoid 长时域任务的
skill-level world model）联系起来。产物是每位研究者一份中文分析报告 + 可复现的数据与图表。

## 5 分钟看懂仓库

```
<firstname_lastname>/
  <Firstname_Lastname>.md     报告正文（主产物）
  papers.csv                  报告引用论文的分类：arxiv_id, category, short_name, note
  arxiv_papers.json           arXiv 作者检索原始结果（链接核对依据；由脚本生成）
  scholar_citations.csv       Google Scholar 每年被引数（手动抄录，可选）
  figures/                    由脚本生成的图
  categories/<id>.md          每个论文类别一个深度分析文件（主报告只放简介 + 表格 + 链接）
docs/
  onboarding.md               本文件
  decisions.md                决策与变更日志（项目"记忆"）
.cursor/
  rules/                      Cursor 规则：语言、结构、硬性要求
  skills/researcher-trend-analysis/
    SKILL.md                  分析流程（六步）
    CATEGORIES.md             统一的论文主题分类表及说明
    categories.json           分类 ID、双语标签、颜色（图表用）
    TEMPLATE.md               报告骨架
    scripts/                  fetch_arxiv_author.py / verify_links.py / plot_trends.py
```

已完成的报告：`sergey_levine/`（完整流程范例）、`chelsea_finn/`、`pieter_abbel/`（旧格式，待迁移）。
空目录（`guanya_shi/`、`hao_su/`、`xiaolong_wang/`、`xuebin_peng/`）是待分析的研究者。

## 三条不可违反的规则

1. **每篇引用的论文必须真实且可点开**（优先 arXiv 摘要页）。提交前 `verify_links.py` 必须输出 `OK`。
2. **要点只写摘要里明确说的**；自己的推断标"个人推断"。
3. **分类只用 `CATEGORIES.md` 中的 ID**，保证不同研究者之间可比。要加类别先在那里登记并记入 `docs/decisions.md`。

## 环境

- Python 3.10+。`fetch_arxiv_author.py` 与 `verify_links.py` 只用标准库。
- `plot_trends.py` 需要 `matplotlib`、`numpy`（见 `requirements.txt`；本机可用 conda base 环境：
  `/home/cguo-iit.local/miniforge3/bin/python`）。

## 典型工作流：新增一位研究者

```bash
# 1. 拉取 arXiv 作者论文（Lastname_Firstname）
python .cursor/skills/researcher-trend-analysis/scripts/fetch_arxiv_author.py Finn_Chelsea \
    --since 2024-01-01 --out chelsea_finn/arxiv_papers.json

# 2. 读摘要，手写 chelsea_finn/papers.csv（分类 ID 见 CATEGORIES.md）
# 3. 依 TEMPLATE.md 写 chelsea_finn/Chelsea_Finn.md（每个主题先写说明段，再放表）

# 4. 出图并把打印出的统计表贴进报告
python .cursor/skills/researcher-trend-analysis/scripts/plot_trends.py chelsea_finn --name "Chelsea Finn" --end 2026-08

# 5. 核对链接（必须 OK）
python .cursor/skills/researcher-trend-analysis/scripts/verify_links.py chelsea_finn/Chelsea_Finn.md \
    --arxiv chelsea_finn/arxiv_papers.json --csv chelsea_finn/papers.csv

# 6. 在 docs/decisions.md 追加一条记录
```

在 Cursor 里，直接对 agent 说"分析 XXX 的 Google Scholar：<链接>"即可，规则会让它自动走上述流程；默认中文。

## 更新已有报告

重跑第 1 步得到新 JSON，与 `papers.csv` 的 id 做差集找出新论文，补 csv 与表格、修改趋势段落、更新"更新时间"，
再跑第 4–6 步。

## 常见问题

- **Scholar 抓取失败 / 只显示前 100 条**：正常，以 arXiv JSON 为链接依据；Scholar 只用来看期刊/会议信息和引用数。
- **论文只在期刊 / 专利，没有 arXiv**：引用出版社或 DOI 页面，`papers.csv` 的 `note` 写 `non-arxiv`，且不要编 arXiv 编号。
- **图里中文显示为方块**：脚本刻意用英文标签；中文解读写在报告里。
- **同一论文有多个 arXiv 版本**：链接用不带 `vN` 的编号。
