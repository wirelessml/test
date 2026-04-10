# プロジェクトコンテキスト

## TODO（次回セッション）

- [ ] **Dispatchペアリング**（Mac or WindowsでClaude Desktopにサインイン → 設定でDispatch有効化）
- [ ] **Tailscaleログイン**（Macメニューバーからwirelessml@gmail.comでサインイン）
- [ ] YouTube動画 QzMDrHjAhpI の字幕取得（shoの片付けサービス相談会ライブ、Whisper文字起こし必要）
- [ ] YouTube動画 ukfCg8ZgMjA の字幕取得（しぶ最新ルームツアー「究極の自宅」39分、音声のみ取得済み、Whisper文字起こし必要）
- [ ] Google Photos MCPのセットアップ（Google Cloud Console → OAuth設定が必要）
- [ ] Google Drive MCPのセットアップ
- [ ] Whisperインストール（pip3 install openai-whisper、ukfCg8ZgMjA等の文字起こし用）
- [ ] しぶ自己語りダイジェスト動画のチャプター時間の微調整（実際の再生で確認）

## 完了（4/10）

- [x] agent-browserインストール（v0.25.3、Vercel Labs製Rust高速CLI、Chrome 147同梱）
- [x] ブラウザ自動化CLI 4ツール比較調査・ナレッジ保存（docs/browser-automation-cli-comparison.md）
- [x] ブラウザ自動化メインをdev-browser → agent-browserに切り替え
- [x] Windows PC（MASU-P55）でのClaude Code v2.1.92起動確認（iPhone SSH経由）
- [x] 定時報告にネットワーク接続状況（Wi-Fi SSID/テザリングデバイス名）を追加
- [x] Homebrew 5.1.5 インストール
- [x] Tailscale 1.96.5 インストール（GUIログインは次回Mac前で）
- [x] Claudeデスクトップアプリ v1.1617.0 インストール
- [x] claude-rcエイリアス設定（~/.zshrc）
- [x] Windows PC（MASU-P55）にSSH接続・git pull同期完了
- [x] AIミニマリストしぶ Webチャットボット作成・公開（server.py + Cloudflare Tunnel）
  - URL: Cloudflare Tunnel経由（セッション毎にURL変わる）
  - Claude CLI経由、APIキー不要、追加費用ゼロ
  - ナレッジ11ファイル埋め込み、しぶ口調再現
  - 会話ログ自動保存（logs/chat_YYYY-MM-DD.jsonl）
  - 同じ質問は塩対応（回数は言わない）
  - 起動: `python3 ai-minimalist-shibu/server.py` + `cloudflared tunnel --url http://localhost:8787`
- [x] 捨て方ガイドブック35種類PDF GitHub Pages公開
  - ビューア: https://wirelessml.github.io/test/docs/sutetekata-guide.html
- [x] しぶ公式「AIミニマリストしぶ」LINE Bot情報をナレッジに記録
- [x] しぶプロフィール修正（住民票: 福岡市中央区、年齢: 31歳）
- [x] Cloudflareインストール（cloudflared 2026.3.0）
- [x] sshpassインストール（Windows SSH用）
- [x] Windows PC Claudeデスクトップアプリ v1.569.0→v1.1348.0にアップデート
- [x] 「なぜAIはPythonで作られるのか」ナレッジ保存（docs/why-ai-uses-python.md）
- [x] AIあんの（チームみらい）参考事例調査
- [x] ミニマムライフコスト計算シートをチャットボットに組み込み
  - 13項目（家賃〜年金）+ カスタム項目追加
  - 通信費（スマホ+WiFi統合）、コワーキング追加
  - 水道代は2ヶ月分入力→自動で月額換算
  - 「しぶに相談」で生活費をしぶに送信→アドバイス
- [x] Monitorツール導入（イベント駆動監視）
  - Wi-Fi接続状態（10秒間隔）
  - しぶチャットサーバー死活（15秒、停止→自動再起動）
  - Cloudflare Tunnel死活（30秒、停止→自動再起動）
  - Windows PC死活（30秒、オンライン/オフライン通知）
- [x] 定時報告cronにサービス稼働状況を追加（しぶサーバー/Tunnel/Windows PC）
- [x] Rust→TS移植事例(@bcherny)をナレッジに追加
- [x] GitHub Copilot CLI + Claude Opus の品質観察を記録

## 完了（4/9コワーキング）

- [x] YouTube動画 2oySXA967II の字幕取得 + しぶ自己語り9場面抽出
- [x] しぶInstagramストーリー情報記録（Obsidianボルト構造 + ポケモンチャンピオンズ）
- [x] iPhone動画編集マニュアル GitHub Pages公開
- [x] ffmpegインストール（ARM64静的バイナリ、~/local/bin/ffmpeg）
- [x] 自動ジェットカットスクリプト jetcut.py 作成・テスト完了
- [x] しぶ自己語りダイジェスト動画作成（9場面 + 宣伝パート合成、23:32）
- [x] チャプター付き動画プレーヤー GitHub Pages公開
- [x] リモートコントロールcronジョブ運用（毎時33分×5回報告）

## 完了（4/8コワーキング）

- [x] マネーフォワードクラウドMCPの認証（exchangeツールでトークン交換が必要）
- [x] Microsoft 365のインストール完了（Word, Excel, PowerPoint）
- [x] Safariへのcomputer-useアクセス許可（完了、tier "read"）
- [x] AIミニマリストしぶ: YouTube20本のトランスクリプト内容把握
- [x] AIミニマリストしぶ: テスラ車上生活のナレッジ更新（モデル3→モデルY、家を手放す）
- [x] AIミニマリストしぶ: 春木開コラボ（172万回再生）・新R25インタビュー追加
- [x] AIミニマリストしぶ: iPhone編集マニュアル作成（りくとの手法）
- [x] AIミニマリストしぶ: Wikipedia・Web記事からの情報補完（メディア出演・人物特徴・ブランド詳細）
- [x] AIミニマリストしぶ: テスラ車上生活への批判的分析の記録
- [x] AIミニマリストしぶ: モノ減らしコーチング料金体系の完全把握（33万〜440万円、値上げ履歴）
- [x] AIミニマリストしぶ: しぶエコシステム分析（りくと・じゅん・sho）

## このリポジトリについて

Claude活用のナレッジベース。AI関連の知見・ガイド・テンプレートを蓄積し、どのAIエージェントからでも参照できる状態を維持する。

## リポジトリ構成

```
├── docs/                          ← ガイド・ナレッジ
│   ├── claude-computer-use-guide.md   ← Computer Use セットアップガイド
│   ├── claude-code-tips-2025.md       ← Claude Code 最新Tips
│   └── ai-knowledge-strategy.md       ← AI時代の情報管理戦略
├── templates/                     ← テンプレート・ワークフロー
│   ├── KNOWLEDGE.md                   ← 学校プリントHTML化ナレッジ
│   └── school-newsletter-template.html
├── spring-break-3rd-grade.html    ← 実際の成果物
└── CLAUDE.md                      ← このファイル（AI向けコンテキスト）
```

## コーディング規約

- ドキュメントは日本語で記述
- Markdownファイルは見出し構造を明確にする
- HTMLはPlaywrightでPNG出力する前提で作成（幅794px）
- ファイル名は英語のケバブケース（例: `claude-code-tips-2025.md`）
- **読んでいないコードは変更するな** — 必ずReadで内容を確認してから編集すること
- 複雑なタスクでは十分に調査してから行動すること（いきなり編集に飛びつかない）
- **サブエージェントの成果物は必ず自分で検証してからユーザーに報告すること** — 「完了しました」の丸投げ禁止

## 情報の保存方針

- **メモリ機能（`~/.claude/projects/*/memory/`）は使用しない**
- 情報はすべてgit管理のドキュメントに書く（他のデバイス・エージェントからも参照可能にするため）
- **会話中に得た情報・知見は毎回gitに保存する**（ルーチン）
  - 技術知見 → `ai-minimalist-shibu/knowledge/` または `docs/`
  - 会話記録 → `conversation_log_YYYYMMDD.md`
  - AIミニマリストしぶ関連 → `ai-minimalist-shibu/knowledge/`
- 会話記録: `conversation_log_YYYYMMDD.md`
- ナレッジ: `docs/` 配下
- プロジェクト情報・ユーザー情報: この `CLAUDE.md` に追記

## ユーザー情報

- 現在無職（ハローワーク通い中、雇用保険受給予定）
- ミニマムライフコスト: 約136,288円/月
- 国民年金: 17,920円/月（免除申請予定）
- MacBook Air M1 8GB — コワーキングオフィスに設置、メイン作業機
  - Homebrew 5.1.5、Tailscale 1.96.5、Claudeデスクトップアプリ インストール済み
  - Claude Code CLI + agent-browser + dev-browser
- Windows PC（MASU-P55）— コワーキングオフィス、サブ作業機
  - ユーザー: gci_admin / IP: 192.168.2.248 (masu-p55.local)
  - SSH接続情報は ~/.claude/local-notes/wifi.txt（パスワードはgit管理外）
  - Claude Code v2.1.98 インストール済み
  - Claudeデスクトップアプリ インストール済み（Microsoft Store版）
  - Computer Use対応（Windows版、2026/4/3〜）
  - リポジトリ: C:\Users\gci_admin\test（同じナレッジベース共有）
  - MacからSSH経由でリモート操作可能
- iPhone 15 Pro（名前: 結花）— メインスマホ、Dispatch + Tailscale
- 初代iPad Pro 9.7インチ（名前: 彩羽）— 楽天SIM挿入、テザリング用
- パナソニック VIERA TH-40CX700 — 自宅テレビ（2015年モデル）
- LG 40WP95C-W — 39.7インチ 5K2Kウルトラワイドモニター（Mac接続）
- Nintendo Switch

## リモートコントロール状態報告

- 毎時33分にcronジョブで自動実行（セッション毎に再設定が必要）
- 内容: screencapture → log.json更新 → Gmail下書き作成 → git commit & push
- screencaptureコマンドを使用（computer-useのスクショはCursorがフィルタされるため不可）
- スクリーンショットは ~/Desktop/screenshots/ に保存
- GitHub Pages: https://wirelessml.github.io/test/
- **ネットワーク接続状況を毎回報告する**
  - Wi-Fi: `system_profiler SPAirPortDataType | grep -A5 "Current Network"` でSSID・周波数
  - YKSmas318 = コワーキングスペースWi-Fi（メイン）
  - rams502 = コワーキングスペースWi-Fi（バックアップ、パスワードは ~/.claude/local-notes/wifi.txt）
  - テザリング: `ifconfig en5 2>/dev/null` でiPhone USB接続確認
  - テザリング時はデバイス名も報告（結花=iPhone 15 Pro / 彩羽=iPad Pro 9.7）
  - 有線接続はなし（Wi-Fiかテザリングのどちらか）
  - **Wi-Fi切り替え後は /rc で接続状況を報告する**

## AIミニマリストしぶ チャットサーバー

- サーバー: `python3 ~/Desktop/ai-minimalist-shibu/server.py`（ポート8787）
- 外部公開: `cloudflared tunnel --url http://localhost:8787`（セッション毎にURL変わる）
- Claude CLI経由、APIキー不要、Claude Pro範囲内で無料
- 会話ログ: `ai-minimalist-shibu/logs/chat_YYYY-MM-DD.jsonl`
- ナレッジ更新時: `python3 ai-minimalist-shibu/src/build-knowledge.py` → サーバー再起動

## セッション設定

- セッション開始時に `/model opusplan` を実行する（思考=Opus、実行=Sonnetの自動切り替え）

## 操作上の注意

- computer-use操作時、アクセス許可リクエストを事前説明せず直接実行する
- Dispatchは使わない、CLIで完結させる
- ブラウザはcomputer-useでtier "read"（クリック不可）、URLを開くことはできるが再生・停止などの操作は不可
- Web情報取得はWebFetch/curl優先
- ブラウザ自動化は**agent-browser優先**（Rust高速CLI、トークン93%削減、snapshotベース）
- dev-browserも利用可能（Playwright API直接、1スクリプト完結型のタスク向け）
- 画面の読み取りだけならChrome DevTools MCPでも可
- `open`コマンドでBraveを開かない
- 音量制御はosascriptで可能

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
