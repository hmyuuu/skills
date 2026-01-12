---
name: issue-triage
description: Evaluate necessity and difficulty of issues, polish body, and create on GitHub with AI-assisted triage
---

# Issue Triage (L2 - Directed)

## Purpose
Help you create well-formed GitHub issues by evaluating necessity, assessing difficulty, and polishing the issue body before opening.

## Autonomy Level: L2 (Directed)
- **Human**: Decide if problem matters, set priority, final approve
- **AI**: Draft, check duplicates, format, open issue

## Workflow

| Phase | Actor | Action |
|-------|-------|--------|
| 1 | **Human** | Describe problem, set intent |
| 2 | Researcher | Check for duplicates in target repo |
| 3 | Prover | Assess necessity & difficulty rating |
| 4 | **Human** | Confirm priority & scope |
| 5 | Writer | Draft issue body |
| 6 | Polisher | Refine title, labels, formatting |
| 7 | **Human** | Final approval |
| 8 | Coder | Execute `gh issue create` |

## Input Required
- Raw problem description
- Target repository (owner/repo)
- Optional: suggested labels, assignees

## Difficulty Rating Scale
- **trivial**: typo, config change, <10 min
- **easy**: clear fix, <1 hour
- **medium**: some investigation needed, <1 day
- **hard**: significant work, >1 day
- **research-needed**: unclear solution path

## Effort Recommendation
- **manual-only**: requires human judgment throughout
- **human-assisted**: AI can help but human must guide
- **fully-automatable**: AI can handle with minimal oversight

## Human Checkpoints (REQUIRED)
1. Is this worth doing? (necessity judgment)
2. How hard is this really? (domain intuition)
3. Final approval before `gh issue create`

## Commands Used
```bash
gh issue list -R <repo> --search "<keywords>"  # check duplicates
gh issue create -R <repo> -t "<title>" -b "<body>" -l "<labels>"
```
