from __future__ import annotations

import os
from pathlib import Path


ROOT = Path(__file__).resolve().parent
WEEKLY_REPORT_DIR = Path(
    os.environ.get("ACCIO_WEEKLY_REPORT_DIR", str(ROOT / "output" / "weekly_report"))
).expanduser().resolve()
CURRENT_SHOP_CONTEXT_FILE = Path(
    os.environ.get("ACCIO_CURRENT_SHOP_CONTEXT_FILE", str(ROOT / "output" / "current_shop_context.json"))
).expanduser().resolve()
CURRENT_AUTH_STATE_FILE = Path(
    os.environ.get("ACCIO_CURRENT_AUTH_STATE_FILE", str(ROOT / "output" / "current_auth_state.json"))
).expanduser().resolve()
SITE_DIR = ROOT / "site"
PUBLIC_SITE_URL_FILE = ROOT / "public_site_url.txt"
