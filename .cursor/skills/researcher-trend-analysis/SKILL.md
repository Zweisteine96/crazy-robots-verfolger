---
name: researcher-trend-analysis
description: Analyze a robotics/AI researcher's recent publications (Google Scholar + arXiv) into a verified, categorised trend report with figures. Use when the user gives a Google Scholar or arXiv author page, asks to analyze a lab's or researcher's recent work, update an existing <researcher>/<Name>.md report, add papers to a report, regenerate trend figures, or verify that cited papers are real.
---

# Researcher Trend Analysis

Produces `<researcher_dir>/<Name>.md` (overview: conclusion → figures → per-category tables → trends),
`<researcher_dir>/categories/<category-id>.md` (one deep-dive per category), plus machine-readable
`papers.csv`, `arxiv_papers.json`, optional `scholar_citations.csv`, and `figures/*.png`.
Every cited paper must be verifiable.

## Workflow

```
- [ ] 1. Fetch the verified paper list (arXiv author search)
- [ ] 2. Read abstracts; categorise papers into papers.csv using the shared taxonomy
- [ ] 3. Write / update the main report from TEMPLATE.md (intro + tables + trends)
- [ ] 4. Generate figures; embed them right after 一句话结论; paste the stats table
- [ ] 5. Write / update one deep-dive per category from CATEGORY_TEMPLATE.md
- [ ] 6. Verify links (main report + every category file); fix anything unverified
- [ ] 7. Log notable decisions in docs/decisions.md
```

### Step 1: fetch verified papers

```bash
python .cursor/skills/researcher-trend-analysis/scripts/fetch_arxiv_author.py Lastname_Firstname \
    --since 2024-01-01 --out <researcher_dir>/arxiv_papers.json
```

Also open the Scholar page sorted by date (`&view_op=list_works&sortby=pubdate&pagesize=100`) to catch
venue info and citation counts. Scholar pagination beyond 100 often fails; the arXiv JSON is the
ground truth for links. If a paper is only on Scholar (journal, patent), cite the publisher/DOI page and
mark it `note=non-arxiv` — never guess an arXiv id.

Optional: copy the "Citations per year" numbers from the Scholar profile into
`<researcher_dir>/scholar_citations.csv` (`year,citations`).

### Step 2: categorise

Read abstracts from `arxiv_papers.json` (do not rely on titles). Assign each paper exactly one
category ID from [CATEGORIES.md](CATEGORIES.md) / `categories.json`. Write `papers.csv`:

```csv
arxiv_id,category,short_name,note
2410.24164,generalist-vla,pi0,VLM + flow-matching action head (PI)
```

Curate, don't dump: include papers that carry a trend; skip patents, minor workshop variants,
and papers where the researcher is a peripheral author on an unrelated topic (or put in `other`).
Aim for 50–80 rows for a prolific author over three years.

### Step 3: write the report

Follow [TEMPLATE.md](TEMPLATE.md). Rules that keep reports consistent across researchers:

- Chinese prose; English for paper names, method names and technical terms.
- Each category section starts with a 2–4 sentence intro for non-experts (adapt from CATEGORIES.md) and ends
  with `→ 深度分析：[categories/<id>.md](categories/<id>.md)`; the long-form explanation lives in that file.
- Table rows: `年份 | [短名](arxiv abs link) | 要点`. The 要点 must be supported by the abstract; do not
  invent numbers or claims.
- Trend sections cite specific papers with links; mark inference as 个人推断.
- Keep the owner's "与我的研究方向的连接" section and the cross-researcher comparison section.
- Mark large-team industry papers (e.g. Physical Intelligence, >= 15 authors) with a symbol and explain it.

### Step 4: figures

```bash
# any Python with matplotlib + numpy; e.g. the conda base env
/home/cguo-iit.local/miniforge3/bin/python .cursor/skills/researcher-trend-analysis/scripts/plot_trends.py \
    <researcher_dir> --name "Full Name" --end YYYY-MM
```

Outputs `figures/fig1..fig5` and prints a markdown 主题 × 年份 table. Embed all figures in the
`## 数据速览（图表）` section **directly after 一句话结论** (so they are the first thing a reader sees) with
`![](figures/....png)` and write 1–3 sentences of interpretation under each. Figure text is English
(CJK fonts may be missing); captions in the report are Chinese. `--end` marks the partial year.

### Step 5: per-category deep dives

For every category ID used in `papers.csv`, write `<researcher_dir>/categories/<category-id>.md` from
[CATEGORY_TEMPLATE.md](CATEGORY_TEMPLATE.md). File name = category ID (stable even if section letters
change). Each file must:

- explain the topic for non-experts (terms bilingual on first use);
- analyse **every** paper of that category in `papers.csv` (2–4 sentences each: problem → method →
  results quoted from the abstract → significance), in date order;
- give an evolution timeline, a deep-analysis section (tensions, route comparisons, recurring patterns),
  cross-category links, the owner's research connection, and open questions.

The check below (Step 6) will list any csv paper missing from a category file.

### Step 6: verify (mandatory before finishing)

```bash
python .cursor/skills/researcher-trend-analysis/scripts/verify_links.py \
    <researcher_dir>/<Name>.md --arxiv <researcher_dir>/arxiv_papers.json --csv <researcher_dir>/papers.csv
for f in <researcher_dir>/categories/*.md; do
  python .cursor/skills/researcher-trend-analysis/scripts/verify_links.py "$f" --arxiv <researcher_dir>/arxiv_papers.json
done
```

All must print `OK`. The main-report run also reports ids present in the markdown but not in `papers.csv`
(and vice versa); keep the two in sync so figures match the text. For category files, additionally check
that the set of ids in `categories/<id>.md` equals the csv rows with `category == <id>`.

### Step 7: record decisions

Append to `docs/decisions.md`: date, researcher, what changed, any taxonomy additions or judgement
calls (e.g. why a paper went into category X). This is the project's shared memory.

## Updating an existing report

1. Re-run Step 1 (new `arxiv_papers.json`), diff ids against `papers.csv` to find new papers.
2. Add rows to `papers.csv`, add table rows and adjust trend text; bump 更新时间.
3. Add the new papers to the matching `categories/<id>.md` (逐篇分析 + 演进脉络).
4. Re-run Steps 4, 6, 7.

## Files in this skill

- `scripts/fetch_arxiv_author.py` — arXiv API → JSON (stdlib only)
- `scripts/verify_links.py` — checks markdown/csv ids against the JSON; exit 1 on failure
- `scripts/plot_trends.py` — figures + stats table (needs matplotlib, numpy)
- `categories.json` — taxonomy IDs, bilingual labels, colors
- `CATEGORIES.md` — taxonomy descriptions for readers and for the report's category intros
- `TEMPLATE.md` — main report skeleton
- `CATEGORY_TEMPLATE.md` — per-category deep-dive skeleton (`<researcher_dir>/categories/<id>.md`)
