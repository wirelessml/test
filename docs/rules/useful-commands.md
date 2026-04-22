## よく使うコマンド

```bash
# HTMLをPNGに変換（Playwright）
python docs/render_guide.py

# HTMLをブラウザでプレビュー
open *.html

# YouTube字幕取得（最新版yt-dlp + deno）
PATH="$HOME/.deno/bin:$PATH" ~/yt-dlp --write-auto-sub --sub-lang ja --skip-download -o "保存先/yt-VIDEO_ID" "https://www.youtube.com/watch?v=VIDEO_ID"

# agent-browser（ブラウザ自動化・メイン）
agent-browser open https://example.com
agent-browser snapshot -i -c          # インタラクティブ要素のみ、コンパクト
agent-browser click @e2               # refで要素クリック
agent-browser fill @e3 "text"         # フォーム入力
agent-browser screenshot              # スクリーンショット
agent-browser close --all             # 終了

# dev-browser（ブラウザ自動化・サブ、Playwright API直接）
dev-browser --headless <<'EOF'
const page = await browser.getPage("main");
await page.goto("URL");
// Playwright API使用可能
EOF
```


