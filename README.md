# Skills 

AI made action cheap. Validation is still expensive.

Agents can search, write, code, and iterate at near-zero cost. But someone still has to check if the output is correct, useful, or even sane. That's you.


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

## Installation

### Add the Marketplace

```bash
claude plugin marketplace add /path/to/skills
```

### Install Plugins

Enter Claude Code and use `/plugin` to navigate to the marketplace and install each skill.

```bash
# Install individual skills
claude plugin install academic-research@hmyuuu-skills
claude plugin install arxiv-digest@hmyuuu-skills
claude plugin install citation-manager@hmyuuu-skills
claude plugin install derivation-checker@hmyuuu-skills
claude plugin install experiment-logger@hmyuuu-skills
claude plugin install flowchart@hmyuuu-skills
claude plugin install issue-triage@hmyuuu-skills
claude plugin install latex-to-typst@hmyuuu-skills
```

### Alternative: Let an LLM Agent do it

Paste this into a fresh Claude Code session:

```
Install and configure by following the instructions here https://raw.githubusercontent.com/hmyuuu/skills/refs/heads/main/README.md
```

<details>
<summary>Instructions for LLM Agents (click to expand)</summary>

**Instructions for LLM Agents**

If you're an LLM Agent helping set up hmyuuu/skills, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/hmyuuu/skills.git /path/to/skills
   ```

2. **Add the marketplace:**
   ```bash
   claude plugin marketplace add /path/to/skills
   ```

3. **Ask user which skills to install:**
   - `academic-research` - Research papers, write typst with cetz plots
   - `arxiv-digest` - Daily digest of relevant arxiv papers
   - `citation-manager` - Find and format citations automatically
   - `derivation-checker` - Step-by-step math derivation verification
   - `experiment-logger` - Log ML experiments with params and plots
   - `flowchart` - Generate flowcharts with typst/cetz
   - `issue-triage` - Evaluate, polish, and create GitHub issues
   - `latex-to-typst` - Convert LaTeX to typst format

4. **Install selected skills:**
   ```bash
   claude plugin install academic-research@hmyuuu-skills
   claude plugin install arxiv-digest@hmyuuu-skills
   claude plugin install citation-manager@hmyuuu-skills
   claude plugin install derivation-checker@hmyuuu-skills
   claude plugin install experiment-logger@hmyuuu-skills
   claude plugin install flowchart@hmyuuu-skills
   claude plugin install issue-triage@hmyuuu-skills
   claude plugin install latex-to-typst@hmyuuu-skills
   ```

5. **Verify installation:** Run `claude plugin list` to confirm skills are installed.

Tell the user installation is complete!

</details>

### Factory Droid / OpenCode

```bash
./install.sh
```

### Justfile

```bash
just install    # Install all skills
```

## Creating New Skills

Use the template:
```bash
mkdir -p plugins/my-new-skill/{.claude-plugin,skills/my-new-skill}
cp templates/SKILL.template.md plugins/my-new-skill/skills/my-new-skill/SKILL.md
# Add plugin.json to plugins/my-new-skill/.claude-plugin/
```

## License

MIT
