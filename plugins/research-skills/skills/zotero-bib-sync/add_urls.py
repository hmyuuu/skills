#!/usr/bin/env python3
"""Add arXiv URLs to Zotero items that have arXiv IDs in their extra field."""

import json
import re
from pathlib import Path
from pyzotero import zotero

config_path = Path.home() / ".config" / "zotero-mcp" / "config.json"
with open(config_path) as f:
    config = json.load(f)

zot = zotero.Zotero(config["library_id"], config["library_type"], config["api_key"])

COLLECTION_KEY = "JKLY9EZJ"

items = zot.everything(zot.collection_items(COLLECTION_KEY))
print(f"Found {len(items)} items in collection")

updated = 0
for item in items:
    data = item.get("data", {})
    extra = data.get("extra", "")
    current_url = data.get("url", "").strip()

    # Skip if already has a URL
    if current_url:
        continue

    # Extract arXiv ID from extra field
    arxiv_id = None
    for line in extra.split("\n"):
        line_stripped = line.strip()
        if line_stripped.lower().startswith("arxiv:"):
            arxiv_id = line_stripped.split(":", 1)[1].strip()
            break

    if not arxiv_id:
        print(f"  No arXiv ID found for: {data.get('title', '?')}")
        continue

    url = f"https://arxiv.org/abs/{arxiv_id}"
    data["url"] = url
    try:
        zot.update_item(item)
        print(f"  Updated: {data['title'][:60]}  ->  {url}")
        updated += 1
    except Exception as e:
        print(f"  FAILED: {data['title'][:60]}: {e}")

print(f"\nDone: {updated} items updated with URLs")
