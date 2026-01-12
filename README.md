# Human Values Skills Repository

> **"You Validate"** — Human values are the source of truth. AI agents execute; humans judge what matters.

## Philosophy

These skills are designed around a simple principle: **you think, AI types**.

- **AI is good at**: search, synthesis, formatting, boilerplate, checking algebra, running tests
- **You are better at**: judging what matters, spotting nonsense, creative leaps, knowing when something "feels wrong"

Every skill has explicit **human checkpoints** where your judgment is required.

## Three Autonomy Levels

| Level | Name | Human Role | AI Role | Validation |
|-------|------|------------|---------|------------|
| **L1** | Conversational | Active dialog, manual check each step | Respond, draft, suggest | Human validates every output |
| **L2** | Directed | Set direction & method, review results, plan next | Execute with unit tests, ensure correctness | Unit tests + human review |
| **L3** | Autonomous | Approve goal, review final output | Plan → orchestrate subagents → validate loop → present when done | Agent loop + unit tests + human final approval |

## AI Subagent Roles

| Subagent | Responsibility |
|----------|----------------|
| **Researcher** | Web search, context gathering, fact-finding |
| **Coder** | Implementation, scripts, automation |
| **Writer** | Drafting prose, typst/latex, documentation |
| **Polisher** | Refining, formatting, style consistency |
| **Prover** | Unit tests, validation, derivation checks |

## Skills

| Skill | Level | Description |
|-------|-------|-------------|
| `issue-triage` | L2 | Evaluate, polish, and create GitHub issues |
| `academic-research` | L1-L2 | Research papers, write typst with cetz plots |
| `arxiv-digest` | L3 | Daily digest of relevant arxiv papers |
| `latex-to-typst` | L3 | Convert LaTeX to typst format |
| `derivation-checker` | L1 | Step-by-step math derivation verification |
| `experiment-logger` | L2 | Log ML experiments with params and plots |
| `citation-manager` | L3 | Find and format citations |

## Installation

### Claude Code
```bash
claude plugin add github:hmyuuu/skills
# or clone and:
claude plugin add /path/to/skills
```

### Factory Droid / OpenCode
```bash
./install.sh
```

This symlinks skills to `~/.factory/skills/` and `~/.config/opencode/skill/`.

## Creating New Skills

Use the template:
```bash
cp templates/SKILL.template.md skills/my-new-skill/SKILL.md
```

## License

MIT
