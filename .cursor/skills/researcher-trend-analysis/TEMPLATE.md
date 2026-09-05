# <研究者姓名>：近期研究趋势分析（<起止年份>）

> 更新时间：YYYY-MM-DD  
> Google Scholar（按时间排序）：[<姓名>](https://scholar.google.com/citations?hl=en&user=<ID>&view_op=list_works&sortby=pubdate)  
> arXiv 作者检索：[<Lastname, Firstname>](https://arxiv.org/search/?query=<Lastname>%2C+<Firstname>&searchtype=author&order=-announced_date_first)

> 方法说明：本文引用的每一篇论文都通过 arXiv 作者检索与 Google Scholar 交叉核对（`scripts/verify_links.py` 通过）；分类数据见同目录 `papers.csv`，图表由 `scripts/plot_trends.py` 生成。趋势判断以论文摘要明确陈述的内容为依据，个人推断单独标出。

---

## 一句话结论

<两三句话：研究者当前的核心问题是什么，用哪条主线串起近期工作。>

> <一个问句形式的核心研究问题>

---

## 数据速览（图表）

<图表紧跟结论，让读者打开报告就能看到数据。嵌入 figures/ 下的图，每张图后写 1–3 句解读，指出图上能看出的具体现象。>

### 图 1 · 各主题论文数量与占比

![](figures/fig1_papers_per_year_by_theme.png)

<粘贴 plot_trends.py 输出的主题 × 年份统计表。>

<解读。>

### 图 2 · 主题占比 … 图 5 · Google Scholar 每年被引数

<同上。>

---

## 1. 论文全景（按主题分组）

<按 CATEGORIES.md 中的类别分组。每个类别先给 2–4 句简介（研究什么、核心问题），末尾用 `→ 深度分析：[categories/<id>.md](categories/<id>.md)` 链到该类别的深度分析文件，再给表格。>

### 1A. <类别中文名>

**这一类在研究什么：** <简介。> → 深度分析：[categories/<category-id>.md](categories/<category-id>.md)

| 年份 | 论文 | 要点 |
|---|---|---|
| 2024 | [短名](https://arxiv.org/abs/XXXX.XXXXX) | 一句话要点（只写摘要里明确说的）。 |

<其余类别同上。>

---

## 2. 主要趋势

### 2.1 <趋势名>

<用具体论文（带链接）支撑；说明"变化在哪里"。>

---

## 3. 时间线：<起止年份> 的演变

- **2024**：...
- **2025**：...
- **2026**：...

---

## 4. 与 VLA、RL、world model 的关系

| 方向 | 该研究者路线中的作用 | 代表工作 |
|---|---|---|

---

## 5. 对机器人与 AI 趋势的判断

1. ...

---

## 6. 与我的研究方向的连接

<项目所有者自己的研究方向与该研究者路线的结合点。>

---

## 7. 与其他研究者的区别

<与项目中其他已分析研究者的横向比较。>

---

## 8. 后续更新时应追踪的问题

- ...

---

## 9. 完整讨论结论

<综合判断。>
