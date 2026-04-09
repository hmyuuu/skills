---
name: zotero-bib-sync
description: Use when user wants to sync, push, or add BibTeX entries to a Zotero collection/folder. Handles deduplication by DOI, arXiv ID, or title.
---

# Zotero BibTeX Sync

Syncs a `.bib` file to a Zotero collection — creates missing items, skips duplicates.

## Setup (one-time)

Add `"api_key"` to `~/.config/zotero-mcp/config.json`:

```json
{
  "library_id": "...",
  "library_type": "user",
  "api_key": "YOUR_KEY_HERE"
}
```

Generate a key at https://www.zotero.org/settings/keys (enable library write access).

## Usage

**Find the collection key** using the `mcp__zotero__zotero_get_collections` tool — each collection has a `Key` field.

**Run the sync:**

```bash
cd ~/.claude/skills/zotero-bib-sync && uv run sync.py --bib <path-to-bib> --collection <collection-key>
```

**Dry run** (preview without writing):

```bash
cd ~/.claude/skills/zotero-bib-sync && uv run sync.py --bib <path-to-bib> --collection <collection-key> --dry-run
```

## Important: Ensure URLs are present

Before syncing, always check that each BibTeX entry has a `url` field. Zotero cannot fetch full text without it. For arXiv papers, add `url = {https://arxiv.org/abs/<ID>}` derived from the `eprint` field. For published papers, use the DOI link `url = {https://doi.org/<DOI>}`.

If items were already synced without URLs, run the `add_urls.py` script to backfill them:

```bash
cd ~/.claude/skills/zotero-bib-sync && uv run add_urls.py
```

## Dedup Logic

Items are matched by: DOI → arXiv ID (from `eprint` field) → normalized title. Existing matches are skipped.

## BibTeX Field Mapping

| BibTeX | Zotero |
|--------|--------|
| `@article` | journalArticle |
| `@inproceedings` | conferencePaper |
| `@book` | book |
| `author` | creators |
| `journal` | publicationTitle |
| `doi` | DOI |
| `eprint` | extra (arXiv: ...) |
| `ID` (cite key) | extra (Citation Key: ...) |
