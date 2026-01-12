---
name: skill:citation-manager
description: Find, format, and manage academic citations in BibTeX and typst formats
---

# Citation Manager (L3 - Autonomous)

You are executing the citation-manager skill.

## User Request
$ARGUMENTS

## Purpose
Autonomously find and format citations from paper titles, DOIs, or arxiv IDs.

## Autonomy Level: L3 (Autonomous)
- **Human**: Request citation, approve final
- **AI**: Find → format → dedupe → validate → present

## Agent Loop
```
while not citations_complete:
    researcher.find_paper(query)
    coder.extract_metadata(paper)
    writer.format_citation(metadata, style)
    prover.validate_bibtex()
    polisher.dedupe_existing()
    present_to_human(formatted_citation)
```

## Input Required
- Paper title, DOI, or arxiv ID
- Output format: bibtex, typst, or both
- Existing .bib file (optional, for deduplication)

## Output Formats

### BibTeX
```bibtex
@article{einstein1905,
  author = {Einstein, Albert},
  title = {On the Electrodynamics of Moving Bodies},
  journal = {Annalen der Physik},
  year = {1905},
  volume = {322},
  pages = {891--921},
  doi = {10.1002/andp.19053221004}
}
```

### Typst
```typst
#bibliography("refs.bib")
// or inline:
@einstein1905
```

## Sources Searched
- Semantic Scholar API
- CrossRef
- arxiv API
- Google Scholar (fallback)

## Human Checkpoint
- Verify citation is for correct paper
- Check author names spelled correctly
