## よく使うコマンド

```bash
# LaunchAgent 健全性チェック（6/12 新設。未ロード/実行失敗/TCC罠/期待リスト突合を一括診断）
bash scripts/launchagent-doctor.sh
# 期待リスト: scripts/launchagents-expected.txt（エージェント増減時に更新）
# ⚠️ launchd 起動物は ~/Desktop に置かない（TCC罠）。実体は ~/Library/Application Support/<name>/、git 正本は scripts/

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

## X / Twitter の読み取り（2026-06-13 確立）

> WebFetch は X に弾かれる（402 / ログインwall）。**ブラウザ操作・スクショ不要**で、agent-reach 同梱の `twitter-cli`（ログイン済みセッション経由）で読む。`agent-reach doctor` で「Twitter/X 完整可用」を確認済み。

```bash
# 単一ツイート＋リプライ（YAML=詳細 / -c=LLM向けJSON）
twitter tweet "https://x.com/<user>/status/<id>" --yaml
twitter -c tweet "<URL_or_ID>"

# ユーザーの投稿一覧 / プロフィール / ホームTL
twitter user-posts @username -n 20
twitter user @username
twitter feed -n 20

# 長文(Article) / 検索（searchはGraphQL変更で404のことあり→ pipx upgrade twitter-cli）
twitter article "<URL_or_ID>"
twitter search "query" -n 10
```

- 投稿（書き込み）は別。閲覧用 X PWA（@minimalistneko）は computer-use full tier、読み取りは上記 CLI が最速
- 環境確認: `agent-reach doctor`（社交=推特/Reddit/V2EX、web=Jina Reader 等の在否を一括表示）


