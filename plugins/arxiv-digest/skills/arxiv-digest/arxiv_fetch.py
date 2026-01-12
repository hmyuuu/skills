#!/usr/bin/env python3
"""Fetch papers from arxiv by category and keywords."""

import argparse
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime
import json
import sys

ARXIV_API = "http://export.arxiv.org/api/query"

@dataclass
class Paper:
    id: str
    title: str
    authors: list[str]
    abstract: str
    categories: list[str]
    published: str
    link: str

def fetch_arxiv(categories: list[str], keywords: list[str] = None, max_results: int = 20) -> list[Paper]:
    """Fetch papers from arxiv API."""
    query_parts = []
    
    if categories:
        cat_query = " OR ".join(f"cat:{c}" for c in categories)
        query_parts.append(f"({cat_query})")
    
    if keywords:
        kw_query = " OR ".join(f"all:{k}" for k in keywords)
        query_parts.append(f"({kw_query})")
    
    search_query = " AND ".join(query_parts) if query_parts else "all:*"
    
    params = {
        "search_query": search_query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }
    
    url = f"{ARXIV_API}?{urllib.parse.urlencode(params)}"
    
    with urllib.request.urlopen(url, timeout=30) as response:
        xml_data = response.read()
    
    return parse_response(xml_data)

def parse_response(xml_data: bytes) -> list[Paper]:
    """Parse arxiv API XML response."""
    root = ET.fromstring(xml_data)
    ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
    
    papers = []
    for entry in root.findall("atom:entry", ns):
        paper = Paper(
            id=entry.find("atom:id", ns).text.split("/abs/")[-1],
            title=entry.find("atom:title", ns).text.strip().replace("\n", " "),
            authors=[a.find("atom:name", ns).text for a in entry.findall("atom:author", ns)],
            abstract=entry.find("atom:summary", ns).text.strip().replace("\n", " "),
            categories=[c.get("term") for c in entry.findall("atom:category", ns)],
            published=entry.find("atom:published", ns).text[:10],
            link=entry.find("atom:id", ns).text
        )
        papers.append(paper)
    
    return papers

def output_papers(papers: list[Paper], format: str):
    """Output papers in specified format."""
    if format == "json":
        print(json.dumps([p.__dict__ for p in papers], indent=2))
    elif format == "markdown":
        for p in papers:
            print(f"### [{p.title}]({p.link})")
            print(f"**Authors**: {', '.join(p.authors[:3])}{'...' if len(p.authors) > 3 else ''}")
            print(f"**Date**: {p.published} | **Categories**: {', '.join(p.categories[:3])}")
            print(f"\n{p.abstract[:300]}{'...' if len(p.abstract) > 300 else ''}\n")
    else:
        for p in papers:
            print(f"{p.id}: {p.title}")

def main():
    parser = argparse.ArgumentParser(description="Fetch arxiv papers")
    parser.add_argument("-c", "--categories", nargs="+", help="arxiv categories (e.g., cs.LG quant-ph)")
    parser.add_argument("-k", "--keywords", nargs="+", help="search keywords")
    parser.add_argument("-n", "--max-results", type=int, default=10, help="max results")
    parser.add_argument("-f", "--format", choices=["json", "markdown", "plain"], default="plain")
    
    args = parser.parse_args()
    
    if not args.categories and not args.keywords:
        parser.error("At least one of --categories or --keywords required")
    
    papers = fetch_arxiv(args.categories or [], args.keywords, args.max_results)
    output_papers(papers, args.format)

if __name__ == "__main__":
    main()
