#!/bin/bash
# Install skills for Factory Droid and OpenCode

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$SCRIPT_DIR/skills"

# Factory Droid
DROID_DIR="$HOME/.factory/skills"
mkdir -p "$DROID_DIR"
for skill in "$SKILLS_DIR"/*/; do
    skill_name=$(basename "$skill")
    ln -sf "$skill" "$DROID_DIR/$skill_name"
    echo "Linked $skill_name to $DROID_DIR"
done

# OpenCode
OPENCODE_DIR="$HOME/.config/opencode/skill"
mkdir -p "$OPENCODE_DIR"
for skill in "$SKILLS_DIR"/*/; do
    skill_name=$(basename "$skill")
    ln -sf "$skill" "$OPENCODE_DIR/$skill_name"
    echo "Linked $skill_name to $OPENCODE_DIR"
done

echo "Done! Skills installed for Droid and OpenCode."
