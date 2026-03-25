#!/usr/bin/env python3
"""Render the Claude Computer Use guide markdown to a PNG image."""

import markdown
from pathlib import Path

md_path = Path(__file__).parent / "claude-computer-use-guide.md"
md_text = md_path.read_text(encoding="utf-8")

html_body = markdown.markdown(md_text, extensions=["tables", "fenced_code"])

html_full = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<style>
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Hiragino Sans",
                 "Noto Sans CJK JP", sans-serif;
    max-width: 820px;
    margin: 40px auto;
    padding: 0 32px;
    color: #1a1a1a;
    background: #ffffff;
    font-size: 15px;
    line-height: 1.7;
  }}
  h1 {{
    font-size: 26px;
    border-bottom: 3px solid #d4a574;
    padding-bottom: 12px;
    margin-bottom: 8px;
  }}
  h2 {{
    font-size: 20px;
    color: #c45a20;
    margin-top: 36px;
    border-left: 4px solid #d4a574;
    padding-left: 12px;
  }}
  h3 {{
    font-size: 17px;
    margin-top: 24px;
  }}
  h4 {{
    font-size: 15px;
    margin-top: 18px;
    color: #555;
  }}
  blockquote {{
    border-left: 4px solid #d4a574;
    margin: 16px 0;
    padding: 12px 20px;
    background: #fdf6ee;
    color: #5a4a3a;
    border-radius: 0 8px 8px 0;
  }}
  blockquote p {{
    margin: 4px 0;
  }}
  table {{
    border-collapse: collapse;
    width: 100%;
    margin: 16px 0;
    font-size: 14px;
  }}
  th {{
    background: #f5ebe0;
    color: #5a4a3a;
    font-weight: 600;
    text-align: left;
    padding: 10px 14px;
    border: 1px solid #ddd;
  }}
  td {{
    padding: 10px 14px;
    border: 1px solid #ddd;
    vertical-align: top;
  }}
  tr:nth-child(even) td {{
    background: #fafafa;
  }}
  code {{
    background: #f4f0ec;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 13px;
  }}
  pre {{
    background: #f4f0ec;
    padding: 14px 18px;
    border-radius: 8px;
    overflow-x: auto;
    font-size: 13px;
  }}
  pre code {{
    background: none;
    padding: 0;
  }}
  hr {{
    border: none;
    border-top: 1px solid #e0d6cc;
    margin: 32px 0;
  }}
  ul, ol {{
    padding-left: 24px;
  }}
  li {{
    margin: 4px 0;
  }}
  strong {{
    color: #333;
  }}
</style>
</head>
<body>
{html_body}
</body>
</html>
"""

out_html = Path(__file__).parent / "claude-computer-use-guide.html"
out_html.write_text(html_full, encoding="utf-8")
print(f"HTML written to {out_html}")
