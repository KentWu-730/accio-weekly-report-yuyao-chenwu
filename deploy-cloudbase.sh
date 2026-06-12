#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ $# -lt 1 ]]; then
  cat <<'EOF'
Usage: ./deploy-cloudbase.sh <environment-id> [cloud-path]

Examples:
  ./deploy-cloudbase.sh env-xxxx / 
  ./deploy-cloudbase.sh env-xxxx /accio-weekly-report

What it does:
  1. Rebuilds the static site into ./site
  2. Deploys ./site to CloudBase static hosting
EOF
  exit 1
fi

ENV_ID="$1"
CLOUD_PATH="${2:-/}"

python3 "$ROOT/build_github_pages_site.py"

if ! command -v tcb >/dev/null 2>&1; then
  echo "CloudBase CLI (tcb) is not installed. Install it first:" >&2
  echo "  npm i -g @cloudbase/cli" >&2
  exit 2
fi

echo "Deploying ./site to CloudBase environment: $ENV_ID"
echo "Cloud path: $CLOUD_PATH"
tcb hosting deploy "$ROOT/site" "$CLOUD_PATH" -e "$ENV_ID"
