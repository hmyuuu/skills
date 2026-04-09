#!/usr/bin/env python3
"""Sync a BibTeX file to a Zotero collection.

Usage:
    uv run sync.py --bib <path> --collection <key> [--api-key <key>] [--dry-run]

Reads BibTeX entries, maps them to Zotero item format, creates missing items
in the target collection, and optionally removes items no longer in the BibTeX.
"""

import argparse
import json
import os
import sys
from pathlib import Path

import bibtexparser
from pyzotero import zotero


# ---------------------------------------------------------------------------
# BibTeX → Zotero mapping
# ---------------------------------------------------------------------------

BIBTEX_TYPE_MAP = {
    "article": "journalArticle",
    "inproceedings": "conferencePaper",
    "conference": "conferencePaper",
    "book": "book",
    "incollection": "bookSection",
    "phdthesis": "thesis",
    "mastersthesis": "thesis",
    "techreport": "report",
    "misc": "document",
    "unpublished": "manuscript",
}


def parse_authors(author_str: str) -> list[dict]:
    """Parse BibTeX author string into Zotero creator list."""
    creators = []
    # Split on " and " (BibTeX convention)
    parts = [a.strip() for a in author_str.replace("\n", " ").split(" and ")]
    for part in parts:
        if not part:
            continue
        if "," in part:
            # "Last, First" format
            pieces = [p.strip() for p in part.split(",", 1)]
            creators.append({
                "creatorType": "author",
                "lastName": pieces[0],
                "firstName": pieces[1] if len(pieces) > 1 else "",
            })
        else:
            # "First Last" format
            pieces = part.rsplit(" ", 1)
            if len(pieces) == 2:
                creators.append({
                    "creatorType": "author",
                    "firstName": pieces[0],
                    "lastName": pieces[1],
                })
            else:
                creators.append({
                    "creatorType": "author",
                    "lastName": pieces[0],
                    "firstName": "",
                })
    return creators


def clean_latex(s: str) -> str:
    """Remove common LaTeX artifacts from a string."""
    return (
        s.replace("{", "")
        .replace("}", "")
        .replace("\\&", "&")
        .replace("\\textendash", "–")
        .replace("--", "–")
        .replace("~", " ")
    )


def bib_entry_to_zotero(entry: dict, collection_key: str) -> dict:
    """Convert a single bibtexparser entry dict to a Zotero item dict."""
    bib_type = entry.get("ENTRYTYPE", "misc").lower()
    zot_type = BIBTEX_TYPE_MAP.get(bib_type, "document")

    item: dict = {"itemType": zot_type}

    # Title
    item["title"] = clean_latex(entry.get("title", ""))

    # Authors
    item["creators"] = parse_authors(entry.get("author", ""))

    # Date / Year
    item["date"] = entry.get("year", "")

    # Journal / Booktitle / Publisher
    if zot_type == "journalArticle":
        item["publicationTitle"] = clean_latex(entry.get("journal", ""))
    elif zot_type == "conferencePaper":
        item["proceedingsTitle"] = clean_latex(
            entry.get("booktitle", entry.get("series", ""))
        )
    elif zot_type == "book":
        item["publisher"] = clean_latex(entry.get("publisher", ""))

    # Volume, issue, pages
    item["volume"] = entry.get("volume", "")
    item["issue"] = entry.get("number", "")
    item["pages"] = entry.get("pages", "").replace("--", "–")

    # DOI
    item["DOI"] = entry.get("doi", "")

    # URL
    item["url"] = entry.get("url", "")

    # Abstract
    item["abstractNote"] = clean_latex(entry.get("abstract", ""))

    # Extra field: store arXiv eprint + BibTeX cite key for dedup
    extra_parts = []
    eprint = entry.get("eprint", "")
    if eprint:
        extra_parts.append(f"arXiv: {eprint}")
    note = entry.get("note", "")
    if note:
        extra_parts.append(clean_latex(note))
    cite_key = entry.get("ID", "")
    if cite_key:
        extra_parts.append(f"Citation Key: {cite_key}")
    item["extra"] = "\n".join(extra_parts)

    # Series (for conference proceedings with volume/series info)
    if "series" in entry and zot_type == "conferencePaper":
        item["series"] = clean_latex(entry.get("series", ""))

    # Publisher (for conferencePaper too)
    if "publisher" in entry:
        item["publisher"] = clean_latex(entry["publisher"])

    # Tags from BibTeX keywords
    keywords = entry.get("keywords", "")
    if keywords:
        item["tags"] = [{"tag": k.strip()} for k in keywords.split(",")]
    else:
        item["tags"] = []

    # Assign to collection
    item["collections"] = [collection_key]

    return item


# ---------------------------------------------------------------------------
# Deduplication
# ---------------------------------------------------------------------------


def get_existing_items(zot: zotero.Zotero, collection_key: str) -> dict[str, dict]:
    """Fetch existing items in collection. Returns dict keyed by dedup key."""
    items = zot.everything(zot.collection_items(collection_key))
    existing = {}
    for it in items:
        data = it.get("data", {})
        key = _dedup_key(data)
        if key:
            existing[key] = it
    return existing


def _dedup_key(data: dict) -> str | None:
    """Generate a deduplication key from an item's data."""
    # Prefer DOI
    doi = data.get("DOI", "").strip().lower()
    if doi:
        return f"doi:{doi}"
    # Fall back to arXiv ID in extra
    extra = data.get("extra", "")
    for line in extra.split("\n"):
        if line.strip().lower().startswith("arxiv:"):
            arxiv_id = line.split(":", 1)[1].strip().lower()
            return f"arxiv:{arxiv_id}"
    # Fall back to normalized title
    title = data.get("title", "").strip().lower()
    if title:
        return f"title:{title}"
    return None


def _dedup_key_from_bib(entry: dict) -> str | None:
    """Generate dedup key from a BibTeX entry."""
    doi = entry.get("doi", "").strip().lower()
    if doi:
        return f"doi:{doi}"
    eprint = entry.get("eprint", "").strip().lower()
    if eprint:
        return f"arxiv:{eprint}"
    title = clean_latex(entry.get("title", "")).strip().lower()
    if title:
        return f"title:{title}"
    return None


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------


def load_config() -> dict:
    """Load Zotero config from ~/.config/zotero-mcp/config.json."""
    config_path = Path.home() / ".config" / "zotero-mcp" / "config.json"
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    return {}


def get_api_key(cli_key: str | None) -> str:
    """Resolve API key from CLI arg, env var, or config."""
    if cli_key:
        return cli_key
    env_key = os.environ.get("ZOTERO_API_KEY")
    if env_key:
        return env_key
    config = load_config()
    stored = config.get("api_key", "")
    if stored:
        return stored
    print(
        "ERROR: No Zotero API key found.\n"
        "Provide one via:\n"
        "  --api-key <key>\n"
        "  ZOTERO_API_KEY env var\n"
        '  "api_key" field in ~/.config/zotero-mcp/config.json\n\n'
        "Generate one at: https://www.zotero.org/settings/keys",
        file=sys.stderr,
    )
    sys.exit(1)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Sync BibTeX file to a Zotero collection"
    )
    parser.add_argument("--bib", required=True, help="Path to .bib file")
    parser.add_argument("--collection", required=True, help="Zotero collection key")
    parser.add_argument("--api-key", help="Zotero API key")
    parser.add_argument(
        "--dry-run", action="store_true", help="Show what would be done, don't write"
    )
    args = parser.parse_args()

    # Load BibTeX
    bib_path = Path(args.bib).expanduser().resolve()
    if not bib_path.exists():
        print(f"ERROR: BibTeX file not found: {bib_path}", file=sys.stderr)
        sys.exit(1)

    with open(bib_path) as f:
        bib_db = bibtexparser.load(f)

    entries = bib_db.entries
    if not entries:
        print("No entries found in BibTeX file.")
        return

    print(f"Parsed {len(entries)} entries from {bib_path.name}")

    # Connect to Zotero
    api_key = get_api_key(args.api_key)
    config = load_config()
    library_id = config.get("library_id", "")
    library_type = config.get("library_type", "user")

    if not library_id:
        print(
            "ERROR: No library_id in ~/.config/zotero-mcp/config.json", file=sys.stderr
        )
        sys.exit(1)

    zot = zotero.Zotero(library_id, library_type, api_key)

    # Check collection exists
    try:
        col = zot.collection(args.collection)
        col_name = col["data"]["name"]
        print(f"Target collection: {col_name} ({args.collection})")
    except Exception as e:
        print(f"ERROR: Could not find collection {args.collection}: {e}", file=sys.stderr)
        sys.exit(1)

    # Get existing items for dedup
    print("Fetching existing items in collection...")
    existing = get_existing_items(zot, args.collection)
    print(f"  Found {len(existing)} existing items")

    # Determine what to create
    to_create = []
    skipped = 0
    for entry in entries:
        dk = _dedup_key_from_bib(entry)
        if dk and dk in existing:
            skipped += 1
            continue
        zot_item = bib_entry_to_zotero(entry, args.collection)
        to_create.append(zot_item)

    print(f"  Skipping {skipped} duplicates")
    print(f"  Creating {len(to_create)} new items")

    if not to_create:
        print("Nothing to do.")
        return

    if args.dry_run:
        print("\n--- DRY RUN: would create ---")
        for item in to_create:
            print(f"  [{item['itemType']}] {item['title']}")
        return

    # Create items in batches of 50 (Zotero API limit)
    batch_size = 50
    created = 0
    failed = 0
    for i in range(0, len(to_create), batch_size):
        batch = to_create[i : i + batch_size]
        try:
            resp = zot.create_items(batch)
            created += len(resp.get("success", {}))
            fail_map = resp.get("failed", {})
            if fail_map:
                failed += len(fail_map)
                for idx, err in fail_map.items():
                    print(
                        f"  FAILED: {batch[int(idx)]['title']}: {err.get('message', err)}",
                        file=sys.stderr,
                    )
        except Exception as e:
            print(f"  ERROR creating batch: {e}", file=sys.stderr)
            failed += len(batch)

    print(f"\nDone: {created} created, {failed} failed, {skipped} skipped (duplicates)")


if __name__ == "__main__":
    main()
