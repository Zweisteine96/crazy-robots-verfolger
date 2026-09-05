#!/usr/bin/env python3
"""Verify that every arXiv link in a markdown report (and every id in papers.csv)
refers to a paper actually authored by the researcher.

Usage:
    python verify_links.py sergey_levine/Sergey_Levine.md --arxiv sergey_levine/arxiv_papers.json
    python verify_links.py sergey_levine/Sergey_Levine.md --arxiv sergey_levine/arxiv_papers.json --csv sergey_levine/papers.csv

Exit code 0 = all ids verified; 1 = at least one unverified id (listed on stderr).
"""
import argparse
import csv
import json
import re
import sys

ARXIV_RE = re.compile(r"arxiv\.org/abs/(\d{4}\.\d{4,5})")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("markdown")
    p.add_argument("--arxiv", required=True, help="JSON produced by fetch_arxiv_author.py")
    p.add_argument("--csv", help="optional papers.csv; its arxiv_id column is also checked")
    a = p.parse_args()

    known = {x["id"]: x["title"] for x in json.load(open(a.arxiv, encoding="utf-8"))}

    md_ids = set(ARXIV_RE.findall(open(a.markdown, encoding="utf-8").read()))
    csv_ids = set()
    if a.csv:
        with open(a.csv, encoding="utf-8") as f:
            csv_ids = {r["arxiv_id"] for r in csv.DictReader(f)}

    bad = sorted(i for i in md_ids | csv_ids if i not in known)
    only_md = sorted(md_ids - csv_ids) if a.csv else []
    only_csv = sorted(csv_ids - md_ids) if a.csv else []

    print(f"markdown links: {len(md_ids)} unique arXiv ids; csv rows: {len(csv_ids)}")
    if only_md:
        print(f"in markdown but not in csv ({len(only_md)}): {', '.join(only_md)}")
    if only_csv:
        print(f"in csv but not in markdown ({len(only_csv)}): {', '.join(only_csv)}")
    if bad:
        print(f"UNVERIFIED ids ({len(bad)}), not found in author search:", file=sys.stderr)
        for i in bad:
            print(f"  {i}", file=sys.stderr)
        sys.exit(1)
    print("OK: every arXiv id is in the author's verified paper list")


if __name__ == "__main__":
    main()
