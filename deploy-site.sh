#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python3 "$ROOT/build_github_pages_site.py"
echo "Built site at: $ROOT/site"
echo "Next step:"
echo "1. Push this repo to GitHub main branch"
echo "2. Enable GitHub Pages -> Source: GitHub Actions"
echo "3. Open the generated github.io URL"
