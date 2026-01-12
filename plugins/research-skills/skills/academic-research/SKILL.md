---
name: skill:academic-research
description: Research academic papers and questions, write typst documents with cetz visualizations, teach until human understands
---

# Academic Research (L1-L2)

You are executing the academic-research skill.

## User Request
$ARGUMENTS

## Purpose
Research academic topics, produce typst documents with proper citations and cetz plots, and iteratively explain until you truly understand.

## Autonomy Level: L1-L2
- **L1 (Teaching mode)**: Guide question, confirm understanding at each step
- **L2 (Writing mode)**: Set direction, AI executes, review output

## Workflow

| Phase | Actor | Action |
|-------|-------|--------|
| 1 | **Human** | Pose research question |
| 2 | Researcher | Web search for papers, extract key insights |
| 3 | **Human** | Judge source quality and relevance |
| 4 | Writer | Draft typst document with structure |
| 5 | Coder | Generate cetz plots for diagrams/graphs |
| 6 | Polisher | Add citations, formatting, flow |
| 7 | Prover | Check logic consistency, math validity |
| 8 | **Human** | Confirm understanding (loop until yes) |

## Input Required
- Research question or paper URL
- Output format preference (notes, summary, full document)
- Target audience level (undergrad, grad, expert)

## Typst Output Structure
```typst
#import "@preview/cetz:0.2.2"

= Title

== Background
// Context and motivation

== Key Concepts
// Main ideas with cetz diagrams

== Analysis
// Detailed breakdown

== References
// BibTeX-style citations
```

## Human Checkpoints (REQUIRED)
1. Is the research question well-formed?
2. Are sources trustworthy? (AI cannot reliably judge this)
3. Does the explanation actually make sense to YOU?
4. Is the typst output publication-worthy?

## Teaching Loop
```
while not human_confirms_understanding:
    explain_concept()
    ask_clarifying_questions()
    adjust_explanation_level()
```

## Tools Used
- Web search for papers
- typst compile for validation
- cetz for plotting
