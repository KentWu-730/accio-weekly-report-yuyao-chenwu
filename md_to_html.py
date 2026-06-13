#!/usr/bin/env python3
import argparse
import html
import re
from typing import Optional
from pathlib import Path


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def slug(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\u4e00-\u9fa5]+", "-", text)
    return text.strip("-") or "section"


def inline_md(text: str) -> str:
    placeholders: list[str] = []

    def stash(html_snippet: str) -> str:
        placeholders.append(html_snippet)
        return f"@@MD{len(placeholders) - 1}@@"

    out = esc(text)
    out = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", lambda m: stash(f'<img alt="{m.group(1)}" src="{m.group(2)}" />'), out)
    out = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: stash(f'<a href="{m.group(2)}" target="_blank" rel="noopener noreferrer">{m.group(1)}</a>'), out)
    out = re.sub(r"`([^`]+)`", lambda m: stash(f"<code>{m.group(1)}</code>"), out)
    out = re.sub(r"\*\*([^*]+)\*\*", lambda m: f"<strong>{m.group(1)}</strong>", out)
    out = re.sub(r"__([^_]+)__", lambda m: f"<strong>{m.group(1)}</strong>", out)
    out = re.sub(r"(?<!\w)\*([^*]+)\*(?!\w)", lambda m: f"<em>{m.group(1)}</em>", out)
    out = re.sub(r"(?<!\w)_([^_]+)_(?!\w)", lambda m: f"<em>{m.group(1)}</em>", out)
    for idx, html_snippet in enumerate(placeholders):
        out = out.replace(f"@@MD{idx}@@", html_snippet)
    return out


def render_markdown(md: str):
    lines = md.replace("\r\n", "\n").split("\n")
    html_parts = []
    toc = []
    i = 0
    in_code = False
    code_lang = ""
    code_buf = []
    in_ul = False
    in_ol = False
    in_quote = False
    paragraph = []
    heading_count = 0

    def flush_p():
      nonlocal paragraph
      if paragraph:
          html_parts.append(f"<p>{inline_md(' '.join(paragraph))}</p>")
          paragraph = []

    def close_blocks():
        nonlocal in_ul, in_ol, in_quote
        if in_ul:
            html_parts.append("</ul>")
            in_ul = False
        if in_ol:
            html_parts.append("</ol>")
            in_ol = False
        if in_quote:
            html_parts.append("</blockquote>")
            in_quote = False

    def parse_table(start):
        rows = []
        j = start
        while j < len(lines) and re.match(r"^\|.*\|$", lines[j].strip()):
            rows.append(lines[j].strip())
            j += 1
        if len(rows) < 2:
            return None
        header = [c.strip() for c in rows[0][1:-1].split("|")]
        body = [[c.strip() for c in row[1:-1].split("|")] for row in rows[2:]]
        t = ["<table><thead><tr>"]
        t.extend(f"<th>{inline_md(h)}</th>" for h in header)
        t.append("</tr></thead><tbody>")
        for row in body:
            t.append("<tr>")
            t.extend(f"<td>{inline_md(cell)}</td>" for cell in row)
            t.append("</tr>")
        t.append("</tbody></table>")
        return "".join(t), j - 1

    while i < len(lines):
        raw = lines[i]
        trimmed = raw.strip()

        if in_code:
            if trimmed.startswith("```"):
                html_parts.append(
                    f'<pre><code class="language-{esc(code_lang)}">{esc(chr(10).join(code_buf))}</code></pre>'
                )
                in_code = False
                code_lang = ""
                code_buf = []
            else:
                code_buf.append(raw)
            i += 1
            continue

        if trimmed.startswith("```"):
            flush_p()
            close_blocks()
            in_code = True
            code_lang = trimmed[3:].strip()
            i += 1
            continue

        if not trimmed:
            flush_p()
            close_blocks()
            i += 1
            continue

        table = parse_table(i)
        if table:
            flush_p()
            close_blocks()
            html_parts.append(table[0])
            i = table[1] + 1
            continue

        heading = re.match(r"^(#{1,6})\s+(.*)$", trimmed)
        if heading:
            flush_p()
            close_blocks()
            level = len(heading.group(1))
            text = heading.group(2).strip()
            hid = slug(text)
            heading_count += 1
            toc.append((level, text, hid))
            html_parts.append(f'<h{level} id="{hid}">{inline_md(text)}</h{level}>')
            i += 1
            continue

        if trimmed.startswith(">"):
            flush_p()
            close_blocks()
            if not in_quote:
                html_parts.append("<blockquote>")
                in_quote = True
            html_parts.append(f"<p>{inline_md(trimmed.lstrip('>').strip())}</p>")
            i += 1
            continue

        if re.match(r"^[-*+]\s+", trimmed):
            flush_p()
            close_blocks()
            if not in_ul:
                html_parts.append("<ul>")
                in_ul = True
            item = re.sub(r"^[-*+]\s+", "", trimmed)
            html_parts.append(f"<li>{inline_md(item)}</li>")
            i += 1
            continue

        if re.match(r"^\d+\.\s+", trimmed):
            flush_p()
            close_blocks()
            if not in_ol:
                html_parts.append("<ol>")
                in_ol = True
            item = re.sub(r"^\d+\.\s+", "", trimmed)
            html_parts.append(f"<li>{inline_md(item)}</li>")
            i += 1
            continue

        if re.match(r"^-{3,}$", trimmed):
            flush_p()
            close_blocks()
            html_parts.append("<hr />")
            i += 1
            continue

        flush_p()
        close_blocks()
        html_parts.append(f"<p>{inline_md(trimmed)}</p>")
        i += 1

    flush_p()
    close_blocks()
    body = "\n".join(html_parts)
    nav = "\n".join(
        f'<a href="#{hid}" style="display:block;padding:8px 10px;border-radius:12px;text-decoration:none;color:#1f1a17;">{"&nbsp;" * (lvl - 1) * 2}{esc(text)}</a>'
        for lvl, text, hid in toc
    )
    return body, nav, heading_count


def build_html(title: str, body: str, toc: str, share_url: Optional[str] = None) -> str:
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{esc(title)}</title>
  <style>
    body{{margin:0;font-family:system-ui,-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;background:#f7f1e6;color:#1f1a17}}
    .shell{{display:grid;grid-template-columns:300px 1fr;min-height:100vh}}
    .sidebar{{padding:20px;border-right:1px solid #e2d7c8;background:#fffaf2;position:sticky;top:0;height:100vh;overflow:auto}}
    .viewer{{padding:24px}}
    .paper{{max-width:980px;margin:0 auto;background:rgba(255,255,255,.9);border:1px solid #e2d7c8;border-radius:24px;padding:34px 38px;box-shadow:0 18px 50px rgba(31,26,23,.06)}}
    h1,h2,h3,h4{{line-height:1.25;letter-spacing:-.02em}}
    h1{{font-size:32px}} h2{{font-size:24px}} h3{{font-size:18px}}
    p,li{{font-size:15px;line-height:1.85}}
    ul,ol{{padding-left:1.3em}}
    blockquote{{border-left:4px solid #0f766e;background:rgba(15,118,110,.07);padding:12px 14px;margin:16px 0;border-radius:0 12px 12px 0}}
    table{{width:100%;border-collapse:collapse;display:block;overflow:auto;margin:16px 0;border-radius:14px}}
    th,td{{border:1px solid #e2d7c8;padding:9px 10px;text-align:left;vertical-align:top;font-size:14px}}
    thead th{{background:#ede3d3}}
    pre{{background:#111827;color:#e5e7eb;padding:14px;border-radius:14px;overflow:auto}}
    code{{background:#efe7db;padding:2px 6px;border-radius:6px}}
    pre code{{background:transparent;padding:0}}
    a{{color:#0f766e}}
    @media (max-width: 900px){{.shell{{grid-template-columns:1fr}} .sidebar{{position:relative;height:auto;border-right:0;border-bottom:1px solid #e2d7c8}}}}
  </style>
</head>
<body>
  <div class="shell">
    <aside class="sidebar">
      <h2 style="margin:0 0 10px">目录</h2>
      {toc or '<p style="color:#71655a">没有标题。</p>'}
    </aside>
    <main class="viewer">
      <article class="paper">
        {body}
      </article>
    </main>
  </div>
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(description="Convert Markdown to a single HTML report.")
    parser.add_argument("input", help="Markdown file path")
    parser.add_argument("-o", "--output", help="Output HTML path")
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    md = input_path.read_text(encoding="utf-8")
    body, toc, _ = render_markdown(md)
    out = Path(args.output).expanduser().resolve() if args.output else input_path.with_suffix(".html")
    out.write_text(build_html(input_path.name, body, toc), encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
