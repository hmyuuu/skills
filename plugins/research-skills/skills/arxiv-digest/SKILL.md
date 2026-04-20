---
name: arxiv-digest
description: Autonomous daily digest of relevant arxiv papers in physics and ML based on your interests
---

# Arxiv Digest (L3 - Autonomous)

You are executing the arxiv-digest skill.

## User Request
$ARGUMENTS

## Purpose
Fetch, filter, and summarize arxiv papers matching research interests.

## Autonomy Level: L3 (Autonomous)
- **Human**: Set interests, review digest
- **AI**: Fetch → filter → summarize → present

## Fetch Method (REQUIRED)

WebFetch is blocked for arxiv.org. Use curl via Bash:

```bash
# Fetch by category (e.g., quant-ph, cs.LG)
curl -sL "https://export.arxiv.org/api/query?search_query=cat:quant-ph&sortBy=submittedDate&sortOrder=descending&max_results=10" -o /tmp/arxiv.xml

# Fetch by keyword
curl -sL "https://export.arxiv.org/api/query?search_query=all:quantum+computing&max_results=10" -o /tmp/arxiv.xml

# Parse results
grep -E "<entry>|<title>|<id>http://arxiv|<name>|<summary>" /tmp/arxiv.xml
```

## Input Required
- arxiv category (e.g., quant-ph, cs.LG)
- Number of papers (default: 10)

## Output Format
```markdown
# Arxiv Digest - [Date]

## [Paper Title]
**Authors**: ...
**arXiv**: https://arxiv.org/abs/XXXX.XXXXX
**Summary**: 2-3 sentences
```

## Fallback
If curl fails, check user's Zotero library with `zotero_semantic_search`.

## Categories
- `quant-ph` - Quantum Physics
- `cs.LG` - Machine Learning
- `cond-mat` - Condensed Matter
- `hep-th` - High Energy Physics Theory
