#!/usr/bin/env sh
# Workspace 2.0 installer: skill + slash commands + output style -> ~/.claude
set -e
SRC="$(cd "$(dirname "$0")" && pwd)"
DEST="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
mkdir -p "$DEST/skills" "$DEST/commands" "$DEST/output-styles"
KEEP=""
if [ -f "$DEST/skills/workspace-2/scripts/models.json" ]; then
  KEEP="$(mktemp)"; cp "$DEST/skills/workspace-2/scripts/models.json" "$KEEP"
fi
rm -rf "$DEST/skills/workspace-2"
cp -r "$SRC/skill/workspace-2" "$DEST/skills/"
[ -n "$KEEP" ] && mv "$KEEP" "$DEST/skills/workspace-2/scripts/models.json" && echo "Kept your models.json"
cp "$SRC"/commands/*.md "$DEST/commands/"
cp "$SRC"/output-styles/*.md "$DEST/output-styles/"
echo "Installed to $DEST"
echo "Next: set model ids in $DEST/skills/workspace-2/scripts/models.json"
echo "Optional: pick output style 'Workspace Terse' (/output-style, or the app's settings)"
echo "Type /ws in Claude Code to see the commands."
