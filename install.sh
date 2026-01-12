#!/bin/bash
# Install skills for Factory Droid and OpenCode

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGINS_DIR="$SCRIPT_DIR/plugins"

# Factory Droid
DROID_DIR="$HOME/.factory/skills"
mkdir -p "$DROID_DIR"
for plugin in "$PLUGINS_DIR"/*/; do
    plugin_name=$(basename "$plugin")
    skill_dir="$plugin/skills/$plugin_name"
    if [ -d "$skill_dir" ]; then
        ln -sf "$skill_dir" "$DROID_DIR/$plugin_name"
        echo "Linked $plugin_name to $DROID_DIR"
    fi
done

# OpenCode
OPENCODE_DIR="$HOME/.config/opencode/skill"
mkdir -p "$OPENCODE_DIR"
for plugin in "$PLUGINS_DIR"/*/; do
    plugin_name=$(basename "$plugin")
    skill_dir="$plugin/skills/$plugin_name"
    if [ -d "$skill_dir" ]; then
        ln -sf "$skill_dir" "$OPENCODE_DIR/$plugin_name"
        echo "Linked $plugin_name to $OPENCODE_DIR"
    fi
done

echo "Done! Skills installed for Droid and OpenCode."
