#!/usr/bin/env python3
"""Fetch a researcher's arXiv papers via the arXiv API and save them as JSON.

Usage:
    python fetch_arxiv_author.py "Levine_Sergey" --since 2024-01-01 --out sergey_levine/arxiv_papers.json

The author query uses arXiv's ``au:`` field, which expects ``Lastname_Firstname``.
Output is a JSON list sorted by date (newest first) with fields:
    id, version, date, title, first_author, n_authors, authors, abstract, categories

Only the Python standard library is required.
"""
import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

NS = {"a": "http://www.w3.org/2005/Atom"}
API = "http://export.arxiv.org/api/query"
PAGE = 200


def fetch_page(author: str, start: int) -> bytes:
    q = urllib.parse.urlencode(
        {
            "search_query": f"au:{author}",
            "sortBy": "submittedDate",
            "sortOrder": "descending",
            "start": start,
            "max_results": PAGE,
        }
    )
    with urllib.request.urlopen(f"{API}?{q}", timeout=60) as r:
        return r.read()


def parse(xml_bytes: bytes):
    root = ET.fromstring(xml_bytes)
    out = []
    for e in root.findall("a:entry", NS):
        raw_id = e.find("a:id", NS).text.split("/abs/")[-1]
        base, _, ver = raw_id.rpartition("v")
        authors = [a.find("a:name", NS).text for a in e.findall("a:author", NS)]
        out.append(
            {
                "id": base if ver.isdigit() else raw_id,
                "version": int(ver) if ver.isdigit() else None,
                "date": e.find("a:published", NS).text[:10],
                "title": " ".join(e.find("a:title", NS).text.split()),
                "first_author": authors[0] if authors else "",
                "n_authors": len(authors),
                "authors": authors,
                "abstract": " ".join(e.find("a:summary", NS).text.split()),
                "categories": [c.get("term") for c in e.findall("a:category", NS)],
            }
        )
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("author", help='arXiv author query, e.g. "Levine_Sergey"')
    p.add_argument("--since", default="2024-01-01", help="keep papers published on/after this date (YYYY-MM-DD)")
    p.add_argument("--out", required=True, help="output JSON path")
    a = p.parse_args()

    papers, start = [], 0
    while True:
        page = parse(fetch_page(a.author, start))
        if not page:
            break
        papers.extend(page)
        if page[-1]["date"] < a.since or len(page) < PAGE:
            break
        start += PAGE
        time.sleep(3)  # arXiv API rate-limit etiquette

    papers = [x for x in papers if x["date"] >= a.since]
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(papers, f, ensure_ascii=False, indent=1)
    print(f"saved {len(papers)} papers since {a.since} to {a.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
