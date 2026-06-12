#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DEFAULT_LINKS_FILE = ROOT / "output" / "weekly_report" / "latest_share_links.json"
DEFAULT_WEBHOOK_FILE = ROOT / "dingding_webhook.txt"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def load_webhook(explicit: str | None) -> str | None:
    if explicit:
        return explicit.strip() or None
    env_value = os.environ.get("DINGTALK_WEBHOOK_URL", "").strip()
    if env_value:
        return env_value
    if DEFAULT_WEBHOOK_FILE.exists():
        value = read_text(DEFAULT_WEBHOOK_FILE)
        if value:
            return value
    return None


def load_links(path: Path) -> dict[str, str]:
    if not path.exists():
        raise FileNotFoundError(f"links file not found: {path}")
    data = json.loads(read_text(path))
    if not isinstance(data, dict):
        raise ValueError("links file must contain a JSON object")
    return {str(k): str(v) for k, v in data.items()}


def build_markdown_message(links: dict[str, str]) -> dict[str, object]:
    web_render_url = links.get("web_render_url", "")

    text_lines = [
        "## 周报链接 已更新",
        "",
        "- 关键词：周报链接",
        f"- 网页端渲染版：[直接打开]({web_render_url})" if web_render_url else "- 网页端渲染版：未生成",
    ]
    return {
        "msgtype": "markdown",
        "markdown": {
            "title": "周报已更新",
            "text": "\n".join(text_lines),
        },
    }


def send_webhook(webhook_url: str, payload: dict[str, object]) -> None:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        webhook_url,
        data=body,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=20) as resp:
        content = resp.read().decode("utf-8", errors="replace")
        print(f"sent: HTTP {resp.status}")
        if content.strip():
            print(content)


def main() -> int:
    parser = argparse.ArgumentParser(description="Send weekly report links to DingTalk robot webhook.")
    parser.add_argument("--webhook", help="DingTalk robot webhook URL. Falls back to env/file if omitted.")
    parser.add_argument("--links-file", default=str(DEFAULT_LINKS_FILE), help="Path to latest_share_links.json")
    parser.add_argument("--dry-run", action="store_true", help="Print payload without sending")
    args = parser.parse_args()

    webhook_url = load_webhook(args.webhook)
    if not webhook_url:
        print("no webhook configured; skip send")
        return 0

    links = load_links(Path(args.links_file))
    payload = build_markdown_message(links)

    if args.dry_run:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    try:
        send_webhook(webhook_url, payload)
    except urllib.error.HTTPError as exc:
        print(f"send failed: HTTP {exc.code} {exc.reason}", file=sys.stderr)
        return 1
    except urllib.error.URLError as exc:
        print(f"send failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
