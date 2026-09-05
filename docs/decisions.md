# 决策与变更日志（项目记忆）

按时间倒序追加。每条记录：日期 · 涉及对象 · 做了什么 · 为什么 / 取舍。目的是让后来者（包括未来的自己和 agent）
不必重新推导已经做过的判断。

---

## 2026-09-05 · 项目基础设施

- **建立 skill `researcher-trend-analysis`** 与两条 Cursor 规则（`project-conventions` 常驻；`researcher-report-format`
  作用于研究者报告与 papers.csv）。目的：让每位研究者的分析走同一流程、同一分类、同一验证标准。
- **默认语言定为中文**（用户明确要求）；论文名与术语保留英文。
- **统一分类表**（`CATEGORIES.md` / `categories.json`）：8 个来自 Levine 分析的类别 + 6 个为 Finn / Abbeel / 人形与
  运动控制研究者预留的类别（world-model、humanoid-locomotion、dexterous-manipulation、sim2real、
  human-robot-interaction、other）。每篇论文只归一类，以摘要的主要贡献为准。
- **链接验证口径**：以 arXiv API 作者检索（`au:Lastname_Firstname`）为 ground truth；Scholar 用于期刊/引用信息。
  原因：Scholar 抓取不稳定且第 2 页以后经常失败；arXiv 返回的作者列表可以机器核对。
- **图表数据源**：一律从 `papers.csv` + `arxiv_papers.json` 生成，禁止手写数字，避免报告与数据漂移。
  图内文字用英文（避免 CJK 字体缺失），解读写中文。
- **"大团队"阈值**：≥ 15 位作者记为大团队 / 工业系统论文（`plot_trends.py` 的 `BIG_TEAM`），并在报告中以 † 标注。
  阈值取自 Physical Intelligence 论文（24–88 位作者）与学术论文（2–12 位）之间的明显间隔。

## 2026-09-05 · Sergey Levine 报告重写

- **删除**旧版中 ICL / test-time training 的概念背景章节与相关表格行（用户指出与主题无关）。
- **保留**"与我的研究方向的连接"与 Finn / Abbeel 比较两节（用户自己的分析）。
- 从 2024 年以来 147 篇 arXiv 论文中**精选 73 篇**入 `papers.csv`。排除：专利、科学设计 / 材料优化（Cliqueformer 等）、
  优化器（Stable Whitening）、纯 LLM 对话安全类（deceptive dialogue、persona simulation）、以及研究者为边缘作者的论文。
  纳入 11 篇 LLM / 智能体 RL 论文，因为它们与机器人侧的 RL 后训练、测试时计算构成明显的方法论平行线。
- 分类取舍说明：
  - `Flow Q-Learning`、`QAM`、`Reversal Q-Learning` 归入 `test-time-steering` 而非 `scalable-value-learning`，
    因为它们的核心是"如何用价值改进 flow/diffusion 策略"，与 QGF / FRS 属同一问题。
  - `Scalable Offline MBRL with Action Chunks` 归入 `chunking-realtime` 而非 `world-model`，因为其贡献点是动作分块
    对复合误差的作用；但在"与 world model 的关系"一节中仍作为世界模型相关工作引用。
  - `ViVa`（视频价值函数）归入 `eval-reward-data`，视作奖励 / 价值信号来源。
  - `Behavioral Exploration`、`LITEN` 归入 `reasoning-hierarchy-memory`（上下文内适应），不单设 ICL 类别。
- Scholar 每年被引数（`scholar_citations.csv`）抄录自 2026-09-05 的 Scholar 页面；2026 为部分年份。

## 2026-09-05 · 报告结构调整：图表前置 + 每类别一个深度分析文件

- 主报告 `Sergey_Levine.md` 的"数据图表"节移到"一句话结论"之后，改名"数据速览（图表）"，小节编号改为"图 1–图 5"，
  后续章节编号顺延（原 3–10 → 2–9）。理由：用户希望打开报告即可看到图。
- 新建 `sergey_levine/categories/<category-id>.md` 共 8 个文件，每类别一个：研究什么 → 逐篇分析（按时间，覆盖该类别
  在 `papers.csv` 中的全部论文，结果数字只取自摘要）→ 演进脉络 → 深度分析 → 与其他类别的连接 → 与我的研究方向的连接 →
  待追踪问题。文件名用类别 ID 而非 1A/1B 编号，避免章节调整时改名。
- 主报告各类别的说明段压缩为 2–4 句简介，并以 `→ 深度分析：[categories/<id>.md]` 链接到深度文件；表格保留在主报告。
- skill 新增 `CATEGORY_TEMPLATE.md`；`TEMPLATE.md`、`SKILL.md`、`researcher-report-format.mdc`、`project-conventions.mdc`、
  `docs/onboarding.md`、`README.md` 同步更新。`verify_links.py` 对每个类别文件单独运行，并检查其 id 集合等于
  `papers.csv` 中 `category == <id>` 的行。
