# プロジェクトコンテキスト

## TODO（次回Mac前での作業）

全てブラウザGUI操作が必要なため、リモートからは実行不可。

### ~~1. Tailscaleログイン~~ ✅ 完了（4/11）
- Standalone版(pkg)でシステム拡張機能を許可→接続成功
- macbook-air: 100.99.41.2（Tailscale 1.96.5、macOS 26.5.0）
- iphone-15-pro: 100.74.77.115（Tailscale 1.96.5、iOS 26.5.0）
- masu-p55: 100.125.21.47（Tailscale 1.96.3、Windows 11 25H2）
- 3台すべてtailnet接続済み

### ~~2. Dispatchペアリング~~ ✅ 完了（4/11）
- MacのClaudeデスクトップアプリ サインイン済み（仲結花 マックスプラン）
- Dispatch接続済み、Computer Use有効化済み
- iPhoneからMac操作可能

### ~~3. Google Photos MCPセットアップ~~ ✅ 完了（4/11）
- プロジェクト: My First Project（既存利用）
- Photos Library API 有効化済み
- OAuth同意画面: photos-mcp（外部、テストユーザー: wirelessml@gmail.com）
- OAuthクライアント: photos-mcp（ウェブアプリケーション）
- ブラウザ認証完了、トークン取得済み（4/11 06:16再認証）
- Claude Code MCP登録済み: `claude mcp add google-photos`（環境変数付き）
- **STDIOモードの.env読み込み問題を修正済み**（`dotenv.config()`に`__dirname`ベースのpath指定）
- トークン保存先: `google-photos-mcp/tokens.json`（実体はSQLite）
- 2025/3/31以降のAPI制限: アプリ作成コンテンツのみアクセス可、Picker APIで既存写真選択可能



## しぶInstagram監視

- アカウント: @minimalist_sibu（認証済み、48投稿、フォロワー7万）
- Chrome DevTools MCPでログイン済み（セッション毎に再ログイン必要）
- ストーリーズ定期チェック: 毎時17分（cron、セッション内のみ）
- 新情報はai-minimalist-shibu/knowledge/shibu-ai-update.mdに追記
- Google Photosしぶ関連画像: **約272枚/615枚**（44%）チェック完了 → `docs/google-photos-shibu-inventory.md`

## 完了（4/11）

- [x] RVC声クローン断念（M1 8GBでは学習不可）
  - WebUI起動・データ処理・特徴抽出まで成功
  - 学習フェーズで.cuda()→.to(device)、autocast、f0サイズ不一致、spectrogram描画等を全修正
  - しかしDataLoaderのforward pass後にハング（CPU/MPS両方）
  - 結論: M1 8GBではRVC学習は現実的でない。推論のみ可能な環境
  - **次の選択肢（優先順）:**
    1. Voxtral TTS（Mistral AI、オープンソース、3GB RAM、無料、声クローン3秒）※日本語非対応が懸念
    2. ElevenLabs Starter（月$5、1ヶ月で解約）
- [x] 声クローン試行: Spark TTS, Qwen3-TTS（動いたが似てなかった）
- [x] mlx-audio環境構築（Python 3.12 venv、Kokoro/Spark/Qwen3モデル）
- [x] ElevenLabs調査（声クローンは有料Starter $5/月、ボイスデザインは無料）
- [x] HuggingFaceアカウント作成・トークン取得（wirelessml）
- [x] SwitchBotシーリングライト提案書HTML+PNG（A4印刷対応）
- [x] しぶ新動画 字幕取得+ナレッジ化: YAJddeKh914（かなさん53歳、3時間、モノ減らしコーチング）
- [x] しぶ音声クリップ切り出し→トップページに埋め込み（「AIミニマリストしぶ」言及箇所）
  - ffmpegの-ss位置問題で無音→修正完了
  - https://wirelessml.github.io/test/
- [x] しぶ画像分析レポートHTML公開（219枚、カテゴリフィルタ+検索機能）
  - https://wirelessml.github.io/test/docs/shibu-photos-report.html
- [x] しぶ画像219枚をWindows PCで詳細分析（25枚バッチ×8回、レート制限1回）
  - `ai-minimalist-shibu/knowledge/google-photos-analysis.md`（70KB）
- [x] しぶ関連画像219枚を`ai-minimalist-shibu/photos/`に集約（182MB、ローカル管理）
- [x] Google Photos全画像エクスポート・しぶ関連272枚特定（Google Takeout→HEIC変換→6エージェント並列チェック）
- [x] Google Photos MCP再認証・修正（STDIOモードの.env読み込み問題修正、環境変数付きMCP再登録）
- [x] しぶ小説2編作成:「自前のVision ProとComputer Use」「誰もいない部屋のComputer Use」
- [x] しぶAI導入ナレッジ作成（31歳誕生日、しぶ次郎Bot、Claude用M5購入）
- [x] テスラナレッジ更新（ナンバー詳細、アメリカ旅行、年越し2026）
- [x] SwitchBotシーリングライト提案書HTML+PNG（A4印刷対応）
- [x] Tailscale Mac接続成功（macbook-air/iphone-15-pro/masu-p55 3台tailnet接続）
- [x] Google Photos MCPセットアップ完了（OAuth認証・Claude Code登録）
- [x] Whisperインストール済み
- [x] YouTube字幕取得: QzMDrHjAhpI（しぶライブ）、ukfCg8ZgMjA（大川裕介×しぶルームツアー）
- [x] ナレッジ57→99ファイル（Windows Claude Codeで42ファイル新規作成、バンドル再生成済み）
- [x] セルフ開発ループ完了（Issue 100件完了、ナレッジ99ファイル、server.py 668行で完成）
- [x] Instagram監視設定（Chrome DevTools MCPでログイン、定期チェックcron）

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
- [x] GitHub CLI (gh 2.89.0) インストール・認証
- [x] セルフ開発ループ実行: Issue 10件作成→全件実装→完了
  - #41 start.sh（ワンコマンド起動）
  - #42 save-logs.sh（会話ログ定期git保存、cron毎時03分）
  - #43 簡易RAG（質問に関連するナレッジだけ選択送信）
  - #44 会話リセットボタン（「身軽になったね」）
  - #45 しぶ決まり文句カウンター（全出し・手放す等）
  - #46 ダーク/ライトモード切替
  - #47 質問サジェストボタン3つ
  - #48 ローディングアニメーション（CSSドット）
  - #49 エラー時自動リトライ
  - #50 リセット時会話統計表示
  - #51 メッセージタイムスタンプ
  - #52 30の質問体験モード
  - #53 チャット統計ダッシュボード（/stats）
  - #54 PWA対応（ホーム画面追加可能）
  - #55 入力欄オートフォーカス
  - #56 /healthエンドポイント
  - #57 start.shヘルスチェック+統計URL表示
  - #58 テスラ車上生活ナレッジfact化
  - #59 メッセージHTML改行レンダリング
  - #60 リクエストレート制限（5秒、しぶ口調で拒否）
  - #61 メッセージコピーボタン
  - #62 クレジット表示（Powered by Claude）
  - #63 モバイルEnter改行対応
  - #64 しぶ名言集ナレッジ追加
  - #65 共有ボタン（Web Share API）
  - #66 マルチスレッド対応（ThreadingMixIn）
  - #67 会話ログエクスポート（/api/export）
  - #68 入力文字数カウンター
  - #69 キーボードショートカット（Ctrl+L/Ctrl+/）
  - #70 アクセスログ記録
  - #71 会話履歴復元（リロード時）
  - #72 しぶ持ち物リストナレッジ追加
  - #73 しぶ口調404ページ（「そのページ、もう手放したよ。」）
  - #74 ランダムしぶ名言表示
  - #75 レスポンス時間表示
  - #76 レスポンスキャッシュ（同じ質問即返答）
  - #77 しぶの1日のルーティンナレッジ
  - #78 送信ボタンスピナー
  - #79 起動時ナレッジ統計ログ
  - #80 空メッセージ送信防止改善
  - #81 SNS戦略分析ナレッジ
  - #82 プレースホルダーランダム化
  - #83 graceful shutdown
  - #84 スクロール自動追従改善
  - #85 食生活ナレッジ
  - #86 収益構造分析ナレッジ
  - #87 会話ログにタイトル追加
  - #88 CORS設定
  - #89 メッセージ削除ボタン
  - #90 著書・愛読書リストナレッジ
  - #76-#80 キャッシュ/ルーティン/スピナー/起動統計/空メッセージ
  - #81-#85 SNS戦略/プレースホルダー/graceful shutdown/スクロール/食生活
  - #86-#90 収益構造/タイトル/CORS/削除ボタン/著書
  - #91-#95 自動リロード/用語辞典/uptime
  - #96-#100 音声入力/ファッション/Markdownリスト/エラーログ/統計リンク
  - #101-#105 サウナ/処理時間ログ/旅行/フィードバック
  - #106-#110 人間関係/片付けチャレンジ/ナレッジAPI/デジタルミニマリズム
  - #111-#115 睡眠/回答200文字制限/起業ストーリー
  - #116-#120 健康管理/会話20往復上限/バージョンv0.120/時間管理
  - #121-#125 お金哲学/引っ越し術/ナレッジ自動検出/部屋づくり
  - #126-#130 掃除術/買い物ルール/防災/.gitignore/server.py 668行
  - #131-#135 コンテンツ制作/失敗談/FAQ/幸福論/全記録保存
  - ナレッジ: 47ファイル、サーバー: 668行
  - #136-#150 家族/影響人物/検索API/福岡/教育/趣味/AI全体像 + ナレッジ56ファイル達成
  - JS構文エラー修正（miniMd正規表現エスケープ問題 — 全機能停止の原因だった）
  - ヘッダー簡素化（「生活費計算」ボタンのみに）
  - **v1.0完成: Issue 100件完了、ナレッジ56ファイル、サーバー668行**
  - v1.0後の修正: JS構文エラー修正、生活費計算パネル修正、履歴復元無効化、Safari最適化、リセットボタン復活、👍👎削除、税金項目追加、カスタム項目グリッド修正
  - 著書データ追加: 平日スケジュール（1日1食/寝袋）、生活費69,087円版
  - しぶプレジデント誌掲載を記録（2026年4月、片付けの10大鉄則）
  - しぶInstagram: テスラ車内就寝写真、東京放浪中→大阪ライブ、kiyoonとの撮影（3/7、モデルY福岡ナンバー確認）
  - ※GitHub Pages連続デプロイ制限に抵触 → 5件まとめてpushに変更

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


## Macプロセス管理の教訓（4/11夜）

### M1 8GBの限界
- Claude Desktop + Cursorだけでも重い（合計CPU ~300%）
- RVC学習は不可能（DataLoaderでハング）。推論のみ可能
- 重いPythonプロセスとの同時稼働は避ける

### RVC-WebUI運用時の注意
- 再起動時は `ps aux | grep frpc` で古いGradioトンネルを確認・kill
- 学習失敗後は `ps aux | grep python3.10` で孤児ワーカーを確認・kill
- `torch_shm_manager` も残るので `ps aux | grep torch_shm` で確認

### リモート監視（Windows PCから）
- SSH: `yuika@100.99.41.2`（Tailscale経由、paramiko使用）
- 負荷確認: `uptime` + `ps aux | sort -nrk 3,3 | head -10`
- メモリ確認: `vm_stat`（Pages freeが数千以下なら危険）

