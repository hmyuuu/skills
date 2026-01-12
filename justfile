# Skills Repository Management

default:
    @just --list

# List all plugins
list:
    @ls -1 plugins/

# Install plugins for Droid/OpenCode
install:
    ./install.sh

# Clear local Claude plugin cache
clear-cache:
    rm -rf ~/.claude/plugins/cache/hmyuuu-skills/
    @echo "Cache cleared. Reinstall plugins via /plugin"

# Create a new plugin from template
new name:
    mkdir -p plugins/{{name}}/.claude-plugin
    mkdir -p plugins/{{name}}/skills/{{name}}
    cp templates/SKILL.template.md plugins/{{name}}/skills/{{name}}/SKILL.md
    @echo '{"name": "{{name}}", "version": "1.0.0", "author": {"name": "hmyuuu"}}' > plugins/{{name}}/.claude-plugin/plugin.json
    @echo "Created plugins/{{name}}/"

# Validate marketplace.json
validate:
    @cat .claude-plugin/marketplace.json | jq . > /dev/null && echo "marketplace.json is valid"

# Show plugin structure
tree:
    @find plugins -type f | sort
