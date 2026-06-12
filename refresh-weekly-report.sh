#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python3 "$ROOT/sync_weekly_reports.py" --finalize-weekly-review
echo "Refreshed weekly report HTML, latest page, share page, and QR code."
echo "Site output: $ROOT/site"
