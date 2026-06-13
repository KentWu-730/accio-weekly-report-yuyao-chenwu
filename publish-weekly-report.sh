#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

"$ROOT/refresh-weekly-report.sh"
if command -v accio-dingtalk-notify >/dev/null 2>&1; then
  accio-dingtalk-notify --links-file "$ROOT/output/weekly_report/latest_share_links.json"
else
  python3 "$ROOT/notify_dingtalk.py" --links-file "$ROOT/output/weekly_report/latest_share_links.json"
fi
echo "Built GitHub Pages site at: $ROOT/site"
echo "Next step:"
echo "1. Commit and push this repo to GitHub main branch"
echo "2. Make sure GitHub Pages source is set to GitHub Actions"
echo "3. Open the generated github.io URL"
