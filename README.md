# crazy-robots-verfolger

To learn the trends in robotics and AI by analyzing the most recent works from different labs.

追踪机器人与 AI 领域重要研究者 2024 年以来的论文，归纳技术趋势，并与项目所有者的研究方向建立连接。
每位研究者一份中文总览报告（结论 → 图表 → 分类表 → 趋势）+ 每个论文类别一份深度分析（`categories/`）+ 可复现的数据（`papers.csv`）与图表（`figures/`）。

## 快速开始

- 新协作者请先读 [`docs/onboarding.md`](docs/onboarding.md)。
- 项目的判断与取舍记录在 [`docs/decisions.md`](docs/decisions.md)。
- 分析流程、统一分类表与脚本在 [`.cursor/skills/researcher-trend-analysis/`](.cursor/skills/researcher-trend-analysis/SKILL.md)。
- 完整流程范例：[`sergey_levine/Sergey_Levine.md`](sergey_levine/Sergey_Levine.md)。

## 研究者

| 研究者 | 报告 | 状态 |
|---|---|---|
| Sergey Levine | [`sergey_levine/Sergey_Levine.md`](sergey_levine/Sergey_Levine.md) | 已按新流程完成（73 篇已核验，含图表） |
| Chelsea Finn | [`chelsea_finn/Chelsea_Finn.md`](chelsea_finn/Chelsea_Finn.md) | 旧格式，待迁移到新流程 |
| Pieter Abbeel | [`pieter_abbel/Pieter_Abbeel.md`](pieter_abbel/Pieter_Abbeel.md) | 旧格式，待迁移到新流程 |
| Guanya Shi / Hao Su / Xiaolong Wang / Xue Bin Peng | — | 待分析 |

## 三条规则

1. 引用的每篇论文必须真实且可点开；`verify_links.py` 必须通过。
2. 要点只写摘要中明确陈述的内容；推断标"个人推断"。
3. 论文分类只用统一分类表中的 ID。

## 环境

`fetch_arxiv_author.py`、`verify_links.py` 仅需 Python 标准库；出图需要 `pip install -r requirements.txt`。
