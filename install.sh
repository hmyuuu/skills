#!/bin/bash
# Install skills for Factory Droid and OpenCode

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGINS_DIR="$SCRIPT_DIR/plugins"

# Factory Droid
DROID_DIR="$HOME/.factory/skills"
mkdir -p "$DROID_DIR"
for plugin in "$PLUGINS_DIR"/*/; do
    plugin_name=$(basename "$plugin")
    skills_base="$plugin/skills"
    if [ -d "$skills_base" ]; then
        for skill_dir in "$skills_base"/*/; do
            skill_name=$(basename "$skill_dir")
            ln -sf "$skill_dir" "$DROID_DIR/$skill_name"
            echo "Linked $skill_name to $DROID_DIR"
        done
    fi
done

# OpenCode
OPENCODE_DIR="$HOME/.config/opencode/skill"
mkdir -p "$OPENCODE_DIR"
for plugin in "$PLUGINS_DIR"/*/; do
    plugin_name=$(basename "$plugin")
    skills_base="$plugin/skills"
    if [ -d "$skills_base" ]; then
        for skill_dir in "$skills_base"/*/; do
            skill_name=$(basename "$skill_dir")
            ln -sf "$skill_dir" "$OPENCODE_DIR/$skill_name"
            echo "Linked $skill_name to $OPENCODE_DIR"
        done
    fi
done

echo "Done! Skills installed for Droid and OpenCode."
