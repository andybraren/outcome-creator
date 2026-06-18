#!/usr/bin/env bash
# Clone or update the JTBD Knowledge Registry from internal GitLab.
# Requires Red Hat VPN and GitLab SAML authentication.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CONFIG="$ROOT/config/jtbd-registry.yaml"

if [[ ! -f "$CONFIG" ]]; then
  echo "error: config/jtbd-registry.yaml not found" >&2
  exit 1
fi

REGISTRY_PATH="$ROOT/$(python3 -c "
import yaml
from pathlib import Path
cfg = yaml.safe_load(Path('$CONFIG').read_text())
print(cfg['registry']['path'])
")"

GIT_URL="${JTBD_REGISTRY_URL:-$(python3 -c "
import yaml
from pathlib import Path
cfg = yaml.safe_load(Path('$CONFIG').read_text())
print(cfg['registry']['git_url'])
")}"

mkdir -p "$(dirname "$REGISTRY_PATH")"

if [[ -d "$REGISTRY_PATH/.git" ]]; then
  echo "Updating JTBD registry at $REGISTRY_PATH ..."
  git -C "$REGISTRY_PATH" pull --ff-only
elif [[ -d "$REGISTRY_PATH" ]]; then
  echo "error: $REGISTRY_PATH exists but is not a git clone" >&2
  exit 1
else
  echo "Cloning JTBD registry into $REGISTRY_PATH ..."
  git clone "$GIT_URL" "$REGISTRY_PATH"
fi

INDEX="$REGISTRY_PATH/index.yaml"
if [[ ! -f "$INDEX" ]]; then
  echo "error: clone succeeded but index.yaml missing — check GitLab access" >&2
  exit 1
fi

echo "JTBD registry ready at $REGISTRY_PATH"
