# Human Values Skills Marketplace

Curated **Agentic Skills** for academic research, LaTeX/Typst workflows, and development automation.

> AI made action cheap. Validation is still expensive.
> **Humans validate. AI executes.**

## Installation

### Claude Code (Marketplace)
```bash
/plugin marketplace add hmyuuu/skills
```

Then browse and install individual skills with `/plugin`.

### Direct Installation
```bash
claude plugin add github:hmyuuu/skills
```

### Factory Droid / OpenCode
```bash
./install.sh
```

## Three Levels of Autonomy

| Level | You | Agent |
|-------|-----|-------|
| **L1** Conversational | Check every step | Draft, suggest |
| **L2** Directed | Set method, review results | Execute with tests |
| **L3** Autonomous | Approve goal, review final | Plan, orchestrate, self-validate, deliver |

Every skill has explicit checkpoints where your judgment is required.

## Available Skills

| Skill | Level | Category | Description |
|-------|-------|----------|-------------|
| `issue-triage` | L2 | Development | Evaluate, polish, and create GitHub issues |
| `academic-research` | L1-L2 | Research | Research papers, write typst with cetz plots |
| `arxiv-digest` | L3 | Research | Daily digest of relevant arxiv papers |
| `latex-to-typst` | L3 | Productivity | Convert LaTeX to typst format |
| `flowchart` | L2 | Productivity | Generate flowcharts with typst/cetz |
| `derivation-checker` | L1 | Research | Step-by-step math derivation verification |
| `experiment-logger` | L2 | Development | Log ML experiments with params and plots |
| `citation-manager` | L3 | Research | Find and format citations |

## Creating New Skills

Use the template:
```bash
cp templates/SKILL.template.md skills/my-new-skill/SKILL.md
```

## License

MIT
