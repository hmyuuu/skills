# Skills Repository

This is a collection of AI agent skills following the "You Validate" philosophy.

## Structure
- `skills/` - All skill definitions (SKILL.md files)
- `templates/` - Blank skill template
- `plugin.json` - Claude plugin manifest
- `install.sh` - Symlink installer for Droid/OpenCode

## Key Concepts
- **Three autonomy levels**: L1 (conversational), L2 (directed), L3 (autonomous)
- **Five subagent roles**: Researcher, Coder, Writer, Polisher, Prover
- **Human checkpoints**: Every skill requires human validation at key decision points

## Skill Format
Each skill is a folder with SKILL.md containing YAML frontmatter (name, description) and markdown instructions.
