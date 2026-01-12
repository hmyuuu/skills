# Arxiv Digest

Autonomous daily digest of relevant arxiv papers based on your interests.

## User Request
$ARGUMENTS

## Workflow
1. Parse arxiv categories and keywords from request
2. Fetch papers from arxiv API
3. Filter by relevance to user interests
4. Summarize relevant papers
5. Format digest and present

## Categories
quant-ph, cs.LG, cond-mat, hep-th, stat.ML

## Output Format
```markdown
# Arxiv Digest - [Date]

## High Relevance
### [Paper Title](arxiv_link)
**Authors**: ...
**Abstract**: 2-3 sentence summary
**Why relevant**: connection to your interests
```
