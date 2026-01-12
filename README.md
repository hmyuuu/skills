# Skills

AI made action cheap. Validation is still expensive.

Agents can search, write, code, and iterate at near-zero cost. But someone still has to check if the output is correct, useful, or even sane. That's you.

**Humans validate. AI executes.**

## Three Levels of Autonomy

| Level | You | Agent |
|-------|-----|-------|
| **L1** Conversational | Check every step | Draft, suggest |
| **L2** Directed | Set method, review results | Execute with tests |
| **L3** Autonomous | Approve goal, review final | Plan, orchestrate, self-validate, deliver |

Every skill has explicit checkpoints where your judgment is required.

## Skills

| Skill | Level | Description |
|-------|-------|-------------|
| `issue-triage` | L2 | Evaluate, polish, and create GitHub issues |
| `academic-research` | L1-L2 | Research papers, write typst with cetz plots |
| `arxiv-digest` | L3 | Daily digest of relevant arxiv papers |
| `latex-to-typst` | L3 | Convert LaTeX to typst format |
| `flowchart` | L2 | Generate flowcharts with typst/cetz |
| `derivation-checker` | L1 | Step-by-step math derivation verification |
| `experiment-logger` | L2 | Log ML experiments with params and plots |
| `citation-manager` | L3 | Find and format citations |

## Tools

| Tool | Language | Description |
|------|----------|-------------|
| `arxiv-fetch` | Python | Fetch papers from arxiv by category/keywords |
| `latex2typst` | Rust | Convert LaTeX to typst format |

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
