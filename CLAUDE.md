# Skills Repository

A collection of AI agent skills following the "You Validate" philosophy.

## Structure
- `plugins/` - Isolated plugin folders (each with `.claude-plugin/plugin.json` and `skills/`)
- `.claude-plugin/marketplace.json` - Marketplace manifest
- `templates/` - Blank skill template
- `install.sh` - Symlink installer for Droid/OpenCode
- `justfile` - CLI task runner

## Key Concepts
- **Three autonomy levels**: L1 (conversational), L2 (directed), L3 (autonomous)
- **Five subagent roles**: Researcher, Coder, Writer, Polisher, Prover
- **Human checkpoints**: Every skill requires human validation at key decision points

## Plugin Structure
Each plugin is isolated in `plugins/<name>/`:
```
plugins/<name>/
├── .claude-plugin/plugin.json
└── skills/<name>/SKILL.md
```
