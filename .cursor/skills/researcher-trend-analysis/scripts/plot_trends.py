#!/usr/bin/env python3
"""Generate trend figures for a researcher folder.

Inputs (all inside the researcher folder unless overridden):
    papers.csv            curated, categorised papers (columns: arxiv_id, category, short_name[, note])
    arxiv_papers.json     full author output from fetch_arxiv_author.py (dates, author counts, titles)
    scholar_citations.csv optional; columns: year, citations   (copied by hand from Google Scholar)

Usage:
    python plot_trends.py sergey_levine --name "Sergey Levine" --end 2026-08

Outputs PNGs into <folder>/figures/ and prints a per-year x category count table (markdown) to stdout.
Figure labels are in English to avoid missing CJK fonts; write Chinese captions in the report.

Requires: matplotlib, numpy (any Python env that has them, e.g. the conda base env).
"""
import argparse
import csv
import json
import os
from collections import Counter, defaultdict

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
CATS = json.load(open(os.path.join(HERE, "..", "categories.json"), encoding="utf-8"))
BIG_TEAM = 15  # >= this many authors is treated as a large-team / industry-style paper


def load(folder):
    papers = {x["id"]: x for x in json.load(open(os.path.join(folder, "arxiv_papers.json"), encoding="utf-8"))}
    rows = []
    with open(os.path.join(folder, "papers.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            meta = papers.get(r["arxiv_id"])
            if meta is None:
                raise SystemExit(f"{r['arxiv_id']} not in arxiv_papers.json; run verify_links.py first")
            r.update(date=meta["date"], year=int(meta["date"][:4]), n_authors=meta["n_authors"], title=meta["title"])
            r["quarter"] = f"{r['year']}Q{(int(meta['date'][5:7]) - 1) // 3 + 1}"
            rows.append(r)
    cites = None
    cpath = os.path.join(folder, "scholar_citations.csv")
    if os.path.exists(cpath):
        with open(cpath, encoding="utf-8") as f:
            cites = [(int(r["year"]), int(r["citations"])) for r in csv.DictReader(f)]
    return rows, list(papers.values()), cites


def cat_order(rows):
    counts = Counter(r["category"] for r in rows)
    return [c for c in CATS if c in counts]


def fig_year_by_category(rows, years, out, name, partial_year):
    cats = cat_order(rows)
    M = np.array([[sum(1 for r in rows if r["year"] == y and r["category"] == c) for y in years] for c in cats])
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    for ax, data, title in [
        (axes[0], M, "Curated papers per year (count)"),
        (axes[1], 100 * M / np.maximum(M.sum(0), 1), "Category share per year (%)"),
    ]:
        bottom = np.zeros(len(years))
        for i, c in enumerate(cats):
            ax.bar([str(y) for y in years], data[i], bottom=bottom, color=CATS[c]["color"], label=CATS[c]["label"])
            bottom += data[i]
        ax.set_title(title)
        ax.set_xticks(range(len(years)))
        ax.set_xticklabels([f"{y}*" if y == partial_year else str(y) for y in years])
    axes[1].legend(loc="upper left", bbox_to_anchor=(1.02, 1), fontsize=8, frameon=False)
    fig.suptitle(f"{name}: curated 2024-2026 papers by theme  (* = partial year)")
    fig.tight_layout()
    fig.savefig(out, dpi=160, bbox_inches="tight")
    plt.close(fig)


def fig_pie(rows, out, name):
    cats = cat_order(rows)
    counts = [sum(1 for r in rows if r["category"] == c) for c in cats]
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(counts, labels=[f"{CATS[c]['label']} ({n})" for c, n in zip(cats, counts)],
           colors=[CATS[c]["color"] for c in cats], startangle=90, textprops={"fontsize": 8},
           autopct="%1.0f%%", pctdistance=0.8)
    ax.set_title(f"{name}: share of curated papers by theme, 2024-2026 (n={sum(counts)})")
    fig.tight_layout()
    fig.savefig(out, dpi=160, bbox_inches="tight")
    plt.close(fig)


def quarters(start, end):
    y, q = int(start[:4]), int(start[-1])
    ey, eq = int(end[:4]), int(end[-1])
    out = []
    while (y, q) <= (ey, eq):
        out.append(f"{y}Q{q}")
        q += 1
        if q == 5:
            y, q = y + 1, 1
    return out


def fig_cumulative(rows, out, name, end_q):
    qs = quarters(min(r["quarter"] for r in rows), end_q)
    cats = cat_order(rows)
    fig, ax = plt.subplots(figsize=(11, 5.5))
    for c in cats:
        per_q = Counter(r["quarter"] for r in rows if r["category"] == c)
        cum = np.cumsum([per_q.get(q, 0) for q in qs])
        ax.plot(qs, cum, marker="o", ms=3, lw=2, color=CATS[c]["color"], label=CATS[c]["label"])
    ax.set_ylabel("cumulative curated papers")
    ax.set_title(f"{name}: cumulative curated papers per theme (by arXiv first-submission quarter)")
    ax.grid(alpha=0.3)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    ax.legend(fontsize=8, frameon=False, loc="upper left")
    fig.tight_layout()
    fig.savefig(out, dpi=160, bbox_inches="tight")
    plt.close(fig)


def fig_output_and_team(all_papers, rows, out, name, end_q):
    qs = quarters(min(r["quarter"] for r in rows), end_q)

    def q_of(p):
        return f"{p['date'][:4]}Q{(int(p['date'][5:7]) - 1) // 3 + 1}"

    total = Counter(q_of(p) for p in all_papers if q_of(p) in qs)
    big = Counter(q_of(p) for p in all_papers if q_of(p) in qs and p["n_authors"] >= BIG_TEAM)
    curated = Counter(r["quarter"] for r in rows)
    x = np.arange(len(qs))
    fig, ax = plt.subplots(figsize=(11, 5.5))
    ax.bar(x - 0.2, [total[q] for q in qs], 0.4, color="#cccccc", label="all arXiv papers (author search)")
    ax.bar(x + 0.2, [curated[q] for q in qs], 0.4, color="#1f77b4", label="curated in this report")
    ax.plot(x, [big[q] for q in qs], color="#d62728", marker="s", lw=2, label=f"large-team papers (>= {BIG_TEAM} authors)")
    ax.set_xticks(x)
    ax.set_xticklabels(qs, rotation=45, ha="right")
    ax.set_ylabel("papers per quarter")
    ax.set_title(f"{name}: arXiv output per quarter and large-team share")
    ax.legend(frameon=False, fontsize=9)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(out, dpi=160, bbox_inches="tight")
    plt.close(fig)


def fig_citations(cites, out, name, partial_year):
    years = [y for y, _ in cites]
    vals = [c for _, c in cites]
    fig, ax = plt.subplots(figsize=(9, 4.5))
    colors = ["#1f77b4" if y != partial_year else "#aec7e8" for y in years]
    ax.bar([str(y) for y in years], vals, color=colors)
    for i, v in enumerate(vals):
        ax.text(i, v, f"{v/1000:.1f}k", ha="center", va="bottom", fontsize=8)
    ax.set_ylabel("citations received in year")
    ax.set_title(f"{name}: Google Scholar citations per year (light bar = partial year)")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(out, dpi=160, bbox_inches="tight")
    plt.close(fig)


def print_table(rows, years, partial_year):
    cats = cat_order(rows)
    head = "| 主题 | " + " | ".join(f"{y}{'*' if y == partial_year else ''}" for y in years) + " | 合计 |"
    print(head)
    print("|" + "---|" * (len(years) + 2))
    for c in cats:
        n = [sum(1 for r in rows if r["year"] == y and r["category"] == c) for y in years]
        print(f"| {CATS[c]['label_zh']} | " + " | ".join(map(str, n)) + f" | {sum(n)} |")
    tot = [sum(1 for r in rows if r["year"] == y) for y in years]
    print("| **合计** | " + " | ".join(map(str, tot)) + f" | {sum(tot)} |")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("folder", help="researcher folder, e.g. sergey_levine")
    p.add_argument("--name", required=True, help="display name for titles")
    p.add_argument("--end", required=True, help="last month covered, YYYY-MM (marks the partial year)")
    a = p.parse_args()

    rows, all_papers, cites = load(a.folder)
    years = sorted({r["year"] for r in rows})
    end_year = int(a.end[:4])
    end_q = f"{end_year}Q{(int(a.end[5:7]) - 1) // 3 + 1}"
    partial_year = end_year if a.end[5:7] != "12" else None
    figs = os.path.join(a.folder, "figures")
    os.makedirs(figs, exist_ok=True)

    fig_year_by_category(rows, years, os.path.join(figs, "fig1_papers_per_year_by_theme.png"), a.name, partial_year)
    fig_pie(rows, os.path.join(figs, "fig2_theme_share_pie.png"), a.name)
    fig_cumulative(rows, os.path.join(figs, "fig3_cumulative_by_theme.png"), a.name, end_q)
    fig_output_and_team(all_papers, rows, os.path.join(figs, "fig4_output_and_team_size.png"), a.name, end_q)
    if cites:
        fig_citations(cites, os.path.join(figs, "fig5_scholar_citations_per_year.png"), a.name, partial_year)
    print_table(rows, years, partial_year)
    print(f"\nfigures written to {figs}/")


if __name__ == "__main__":
    main()
