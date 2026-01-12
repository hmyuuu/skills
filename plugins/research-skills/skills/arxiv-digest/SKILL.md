---
name: skill:arxiv-digest
description: Autonomous daily digest of relevant arxiv papers in physics and ML based on your interests
---

# Arxiv Digest (L3 - Autonomous)

You are executing the arxiv-digest skill.

## User Request
$ARGUMENTS

## Purpose
Automatically fetch, filter, and summarize arxiv papers matching your research interests.

## Autonomy Level: L3 (Autonomous)
- **Human**: Set interests once, review final digest
- **AI**: Search → filter → summarize → validate → present

## Agent Loop
```
while not goal_reached:
    main_agent.plan(current_state)
    researcher.fetch_arxiv(categories, keywords)
    prover.filter_by_relevance(papers, interests)
    writer.summarize(relevant_papers)
    polisher.format_digest()
    if digest_ready:
        present_to_human(digest)
```

## Input Required
- arxiv categories (e.g., quant-ph, cs.LG, cond-mat)
- Keywords/topics of interest
- Digest frequency (daily/weekly)

## Output Format
```markdown
# Arxiv Digest - [Date]

## High Relevance
### [Paper Title](arxiv_link)
**Authors**: ...
**Abstract**: 2-3 sentence summary
**Why relevant**: connection to your interests

## Medium Relevance
...

## Quick Mentions
- [Title](link) - one-line summary
```

## Human Checkpoint
- Review digest, mark papers to read in full
- Optionally refine interest keywords

## Categories
- `quant-ph` - Quantum Physics
- `cs.LG` - Machine Learning
- `cond-mat` - Condensed Matter
- `hep-th` - High Energy Physics Theory
- `stat.ML` - Statistics ML

## Tool

`arxiv_fetch.py` - CLI to fetch papers from arxiv API.

```bash
# Fetch ML papers
./arxiv_fetch.py -c cs.LG -n 10 -f markdown

# Search by keywords
./arxiv_fetch.py -k "transformer" "attention" -f json
```
