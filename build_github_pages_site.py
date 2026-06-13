#!/usr/bin/env python3
from __future__ import annotations

import re
import shutil
from pathlib import Path

from md_to_html import render_markdown
from accio_paths import ROOT, SITE_DIR, WEEKLY_REPORT_DIR
from accio_paths import CURRENT_SHOP_CONTEXT_FILE


WEEKLY_REPORT_NAME_RE = re.compile(r"^weekly_report_(\d{4})_(\d{2})\.md$")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def newest_path(paths: list[Path]) -> Path | None:
    if not paths:
        return None
    return max(paths, key=weekly_report_sort_key)


def extract_markdown_title(md: str, fallback: str) -> str:
    for line in md.splitlines():
        match = re.match(r"^#\s+(.*)$", line.strip())
        if match:
            return match.group(1).strip()
    return fallback


def canonical_weekly_reports() -> list[Path]:
    return sorted(
        [
            path
            for path in WEEKLY_REPORT_DIR.glob("*.md")
            if path.is_file() and WEEKLY_REPORT_NAME_RE.match(path.name)
        ],
        key=weekly_report_sort_key,
    )


def weekly_report_sort_key(path: Path | str) -> tuple[int, int]:
    report_path = Path(path)
    match = WEEKLY_REPORT_NAME_RE.match(report_path.name)
    if not match:
        return (-1, -1)
    return int(match.group(1)), int(match.group(2))


def load_shop_context() -> dict[str, str]:
    if not CURRENT_SHOP_CONTEXT_FILE.exists():
        return {}
    try:
        import json

        data = json.loads(CURRENT_SHOP_CONTEXT_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}
    if not isinstance(data, dict):
        return {}
    return {str(k): str(v) for k, v in data.items() if v is not None}


def ensure_current_shop_context() -> None:
    context = load_shop_context()
    required = (
        "web_shop_id",
        "web_shop_name",
        "accio_pair_shop_id",
        "accio_pair_shop_name",
        "report_source_dir",
        "report_output_dir",
    )
    missing = [key for key in required if not context.get(key, "").strip()]
    if missing:
        raise SystemExit(
            "shop context required for site build: missing current_shop_context.json fields: "
            + ", ".join(missing)
        )


def build_mobile_report_page(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
  <title>{title}</title>
  <style>
    :root {{
      --bg:#f4efe6;
      --bg-2:#efe6d7;
      --panel:rgba(255,250,243,.84);
      --panel-strong:#fffaf3;
      --text:#1d1916;
      --muted:#6f645d;
      --line:#e2d5c5;
      --accent:#0f766e;
      --accent-soft:rgba(15,118,110,.11);
      --shadow:0 24px 70px rgba(31,26,23,.10);
      --shadow-soft:0 10px 30px rgba(31,26,23,.06);
      --radius:28px;
      --radius-sm:18px;
    }}
    *{{box-sizing:border-box}}
    html{{scroll-behavior:smooth}}
    html,body{{margin:0;padding:0;background:
      radial-gradient(circle at top left, rgba(15,118,110,.13), transparent 24%),
      radial-gradient(circle at top right, rgba(194,65,12,.08), transparent 22%),
      linear-gradient(180deg, #faf7f0 0%, var(--bg) 50%, var(--bg-2) 100%);
      color:var(--text);
      font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
    }}
    body::before{{
      content:"";
      position:fixed;
      inset:0;
      pointer-events:none;
      opacity:.18;
      background-image: radial-gradient(rgba(0,0,0,.35) 0.45px, transparent 0.45px);
      background-size:18px 18px;
      mix-blend-mode:multiply;
    }}
    .shell{{position:relative;max-width:1420px;margin:0 auto;padding:22px}}
    .hero{{
      position:relative;
      overflow:hidden;
      border:1px solid rgba(226,213,197,.9);
      border-radius:34px;
      background:linear-gradient(145deg, rgba(255,255,255,.86), rgba(255,250,243,.76)),
                 linear-gradient(180deg, rgba(15,118,110,.04), rgba(194,65,12,.02));
      box-shadow:var(--shadow);
      padding:22px 24px;
    }}
    .hero::after{{
      content:"";
      position:absolute;
      inset:auto -8% -38% auto;
      width:420px;
      height:420px;
      border-radius:50%;
      background:radial-gradient(circle, rgba(15,118,110,.18), rgba(15,118,110,0) 68%);
      filter:blur(10px);
      pointer-events:none;
    }}
    .eyebrow{{
      display:inline-flex;
      align-items:center;
      gap:8px;
      padding:7px 12px;
      border-radius:999px;
      background:var(--accent-soft);
      color:var(--accent);
      font-size:12px;
      font-weight:700;
      letter-spacing:.02em;
    }}
    .hero h1{{
      margin:14px 0 10px;
      max-width:14ch;
      font-size:clamp(34px, 5vw, 58px);
      line-height:.98;
      letter-spacing:-.06em;
      text-wrap:balance;
    }}
    .hero p{{
      margin:0;
      max-width:70ch;
      font-size:15px;
      line-height:1.75;
      color:var(--muted);
    }}
    .meta{{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}}
    .chip{{display:inline-flex;align-items:center;justify-content:center;padding:7px 10px;border-radius:999px;background:#fff;border:1px solid var(--line);font-size:12px;color:var(--text);text-decoration:none;font-weight:700}}
    .chip.primary{{background:var(--text);border-color:var(--text);color:#fff}}
    .paper-shell{{
      margin-top:16px;
      border-radius:30px;
      background:rgba(255,250,243,.74);
      border:1px solid rgba(226,213,197,.9);
      box-shadow:var(--shadow);
      overflow:hidden;
    }}
    .paper-top{{
      display:flex;
      align-items:flex-end;
      justify-content:space-between;
      gap:16px;
      padding:16px 18px;
      border-bottom:1px solid rgba(226,213,197,.9);
      background:linear-gradient(180deg, rgba(255,255,255,.82), rgba(255,250,243,.72));
    }}
    .paper-top h2{{margin:0;font-size:18px;letter-spacing:-.02em}}
    .paper-top p{{margin:6px 0 0;color:var(--muted);font-size:13px;line-height:1.55}}
    .paper-actions{{display:flex;gap:8px;flex-wrap:wrap}}
    .paper{{
      max-width:1080px;
      margin:0 auto;
      padding:30px 36px 42px;
      min-height:64vh;
      background:linear-gradient(180deg, rgba(255,255,255,.78), rgba(255,255,255,.92));
    }}
    .paper > h1:first-child{{margin-top:2px;padding-bottom:10px;border-bottom:1px solid var(--line)}}
    .paper h1,.paper h2,.paper h3,.paper h4{{line-height:1.22;letter-spacing:-.03em;scroll-margin-top:22px;text-wrap:balance}}
    .paper h1{{font-size:34px;margin:0 0 18px}}
    .paper h2{{font-size:24px;margin:32px 0 12px}}
    .paper h3{{font-size:18px;margin:24px 0 10px}}
    .paper h4{{font-size:16px;margin:22px 0 8px;color:#362d28}}
    .paper p,.paper li{{font-size:15px;line-height:1.85;color:#2b2420}}
    .paper p{{margin:10px 0}}
    .paper ul,.paper ol{{padding-left:1.35em;margin:10px 0 16px}}
    .paper li{{margin:5px 0}}
    .paper blockquote{{margin:18px 0;padding:12px 16px;border-left:4px solid var(--accent);background:rgba(15,118,110,.06);color:#32524d;border-radius:0 14px 14px 0}}
    .paper hr{{border:0;height:1px;background:linear-gradient(90deg, transparent, var(--line), transparent);margin:24px 0}}
    .paper code{{background:#efe7db;color:#3b2d20;padding:2px 6px;border-radius:6px;font-size:.95em}}
    .paper pre{{overflow:auto;background:#101820;color:#e5e7eb;padding:14px 16px;border-radius:16px;margin:18px 0;box-shadow:inset 0 1px 0 rgba(255,255,255,.08)}}
    .paper pre code{{background:transparent;color:inherit;padding:0;font-size:14px;white-space:pre}}
    .paper a{{color:var(--accent);text-decoration:none}}
    .paper a:hover{{text-decoration:underline}}
    .paper table{{width:100%;border-collapse:collapse;margin:18px 0;overflow:hidden;border-radius:18px;display:block;overflow-x:auto}}
    .paper thead th{{background:#ede4d5;font-weight:700}}
    .paper th,.paper td{{border:1px solid #e1d6c8;padding:10px 12px;font-size:14px;text-align:left;vertical-align:top}}
    .paper img{{max-width:100%;border-radius:16px}}
    .empty{{display:grid;place-items:center;min-height:52vh;text-align:center;color:var(--muted)}}
    .empty .card{{max-width:540px;background:rgba(255,255,255,.84);border:1px solid var(--line);border-radius:28px;padding:28px;box-shadow:var(--shadow-soft)}}
    .footer{{margin:18px 0 4px;text-align:center;color:var(--muted);font-size:12px;line-height:1.65}}
    .masthead{{
      margin-bottom:16px;
      padding:6px 4px 0;
      border:none;
      background:transparent;
      box-shadow:none;
    }}
    .masthead h1{{
      margin:10px 0 6px;
      font-size:clamp(30px, 5vw, 54px);
      line-height:.98;
      letter-spacing:-.06em;
      max-width:14ch;
    }}
    .masthead p{{
      margin:0;
      max-width:70ch;
      font-size:15px;
      line-height:1.7;
      color:var(--muted);
    }}
    a{{color:var(--accent)}}
    @media (max-width: 640px) {{
      .shell{{padding:14px}}
      .hero{{padding:18px;border-radius:26px}}
      .paper{{padding:22px 14px 28px}}
      .paper-shell{{border-radius:24px}}
      .paper{{min-height:unset}}
      .hero h1{{max-width:none;font-size:clamp(34px, 11vw, 44px)}}
      .hero p{{font-size:15px;line-height:1.7}}
      .paper img,.paper table,.paper pre{{border-radius:12px}}
    }}
  </style>
</head>
<body>
  <div class="shell">
    <header class="masthead">
      <div class="eyebrow">最新周报</div>
      <h1>{title}</h1>
      <p>直接渲染当前 `.md` 内容，保留正文、表格、引用与清单，适合电脑和手机查看。</p>
    </header>
    <section class="paper-shell">
      <article class="paper">
      {body}
      </article>
    </section>
    <div class="footer">固定入口会随每次定时任务更新为最新内容。</div>
  </div>
</body>
</html>"""


def build_latest_alias_page() -> str:
    return """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta http-equiv="refresh" content="0; url=./latest.html" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Redirecting</title>
</head>
<body>
  <p>Redirecting to <a href="./latest.html">latest report</a>...</p>
</body>
</html>"""


def sync_site() -> None:
    ensure_current_shop_context()
    SITE_DIR.mkdir(parents=True, exist_ok=True)
    weekly_out = SITE_DIR / "weekly_report"
    weekly_out.mkdir(parents=True, exist_ok=True)
    mobile_out = SITE_DIR / "mobile"
    mobile_out.mkdir(parents=True, exist_ok=True)

    write_text(SITE_DIR / ".nojekyll", "")

    for md_path in canonical_weekly_reports():
        cleaned_md = read_text(md_path).strip() + "\n"
        write_text(weekly_out / md_path.name, cleaned_md)
        html_path = weekly_out / md_path.with_suffix(".html").name
        if html_path.exists():
            html_path.unlink()
        mobile_html_path = mobile_out / md_path.with_suffix(".html").name
        if mobile_html_path.exists():
            mobile_html_path.unlink()

    latest_md = newest_path(canonical_weekly_reports())
    if latest_md:
        latest_md_text = read_text(latest_md).strip() + "\n"
        write_text(weekly_out / "latest.md", latest_md_text)
        latest_title = extract_markdown_title(latest_md_text, latest_md.stem)
        latest_body, _, _ = render_markdown(latest_md_text)
        latest_html = build_mobile_report_page(latest_title, latest_body)
        write_text(weekly_out / "latest.html", latest_html)
        write_text(weekly_out / "latest", build_latest_alias_page())
        write_text(mobile_out / "latest.html", latest_html)
        write_text(weekly_out / "latest_source.txt", latest_md.name + "\n")

    shutil.copy2(ROOT / "site" / "md-viewer.html", SITE_DIR / "index.html")

    for obsolete in ["report-share.html", "wechat.html", "share-qr.png"]:
        obsolete_path = SITE_DIR / obsolete
        if obsolete_path.exists():
            obsolete_path.unlink()


def main() -> None:
    sync_site()
    print(SITE_DIR)


if __name__ == "__main__":
    main()
