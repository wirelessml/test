## よく使うコマンド

```bash
# HTMLをPNGに変換（Playwright）
python docs/render_guide.py

# HTMLをブラウザでプレビュー
open *.html

# YouTube字幕取得（最新版yt-dlp + deno）
# Mac (M1):
PATH="$HOME/.deno/bin:$PATH" ~/yt-dlp --write-auto-sub --sub-lang ja --skip-download -o "保存先/yt-VIDEO_ID" "https://www.youtube.com/watch?v=VIDEO_ID"

# しゅん先生 PC (Windows、winget で導入済 5/3 朝):
# yt-dlp 2026.03.17 / ffmpeg 8.1 / deno 2.7.14、PATH 既設定済み、SSH 経由でも素直に使える
ssh shun-sensei 'powershell -Command "yt-dlp --write-auto-sub --sub-lang ja --skip-download -o yt-VIDEO_ID https://www.youtube.com/watch?v=VIDEO_ID"'

# 動画本体ダウンロード (Mac):
~/yt-dlp -f "bv*[height<=1080]+ba/best[height<=1080]" --merge-output-format mp4 -o "yt-VIDEO_ID-%(title).80s.%(ext)s" "URL"

# 動画本体ダウンロード (しゅん先生 PC):
ssh shun-sensei 'powershell -Command "yt-dlp -f \"bv*[height<=1080]+ba/best[height<=1080]\" --merge-output-format mp4 -o yt-VIDEO_ID.%%(ext)s URL"'

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


