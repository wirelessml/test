# プロジェクトコンテキスト

## 現在のセッション状態（4/14午前）

### 配信状態
- **YouTube Live配信中**（動画ID: `mRE18XYo6rg`、ゆいかアカウント）
- **OBS 32.1.1** でRTMP配信（プロファイル: YouTube Live）— 10時間45分稼働、90.9GB送信
- **しぶ声コメント読み上げ稼働中**（shibu-live.py、screenセッション `shibu-chat`、自動再接続正常）

### Maestri（AIエージェントオーケストレーター）
- **Maestri** インストール済み（/Applications/Maestri.app、DMGから手動インストール）
- macOS用Swift製アプリ、無限キャンバスで複数AIエージェントを空間配置
- **Claude Code 2台**をキャンバスに配置・接続（Connection）済み
  - Claude Code: Remote Control有効（session_0187RKjgSVFMAeoe7r6WUMgq）
  - Claude Code #2: 入力待ち
- 接続方法: ターミナル選択 → サブツールバーのY字アイコン（「ターミナルに接続」）→ 2つ目をクリック
- 接続するとMaestri Agent Skillが自動インストール、エージェント間で直接プロンプト送受信可能
- 公式ドキュメント: https://www.themaestri.app/en/docs/connections
- 無料版: ワークスペース1つ、エージェント無制限 / Pro $18買い切り: ワークスペース無制限
- CPU使用量: 約27-30%（M1 8GBではOBS同時稼働でギリギリ）

### 4/14午前セッションで実施した内容
- 定時報告6回（04:37, 05:35, 06:35, 07:35, 08:35, 09:35, 10:35）
- Maestriインストール・起動・Claude Code 2台作成・接続
- Chrome高負荷（load 18超）のため終了 → load 2台に改善
- Maestri使い方ガイドHTML作成・GitHub Pages公開
- Obsidian Claude エコシステム ガイドHTML作成・公開
- Windows PC SSH接続・Claude Code統一（npm版削除→スタンドアロン版のみ）
- Windows PC Claude Code 2.1.104→2.1.105アップデート
- Windows PC Claude Code自動更新スケジュール設定（毎日0:00 タスクスケジューラ）
- Windows PC npm版インストールブロック（@anthropic-ai スコープレジストリ無効化）
- masu-p55 Tailscale復旧（masupユーザーのtailscale-ipn停止で解決）
- Maestri解説動画ナレッジ保存（まさおAIじっくり解説ch 2026/04/13）
- BGM変更:「新生活/騒音のない世界」をYouTubeからDL→ループ再生
- shibu-live.py大幅改善:
  - AI回答: Claude Haiku 4.5でしぶとして回答生成
  - 漢字→ひらがな変換（pykakasi）でTTS読み正確化
  - BGM音量0.1% / しぶ声音量1000%に調整
  - しぶ声再生中BGM自動ミュート（SIGSTOP/SIGCONT）
  - コメント読み上げ+AI回答読み上げの2段構成
  - デバッグログ追加

### 4/13 Mac側セッションで実施した内容
- **gh CLI再認証**（wirelessml、ブラウザOAuth + GitHub Mobile認証）
- **YouTube Data API 403修正**: クォータ超過 → **pytchat**に切り替え（APIキー不要、クォータなし）
- **OBSマイクミュート**: 環境音を配信から除去（しぶ声はBlackHole経由なのでマイク不要）
- **マルチ出力デバイス作成**: Audio MIDI設定でMacBook Airスピーカー + BlackHole 2ch
  - 最終的にBlackHole 2chのみに設定（スピーカー音不要）
- **OBS画面キャプチャ追加**: screen_capture、display ID=2（LG ULTRAWIDE 5120x2160）
  - OBSに画面収録権限を付与 → OBS再起動で有効化
  - 5120x2160 → 1280x720キャンバスにscale 0.25で全画面フィット（上下90px黒帯）
- **OBS配信再開**: 停止→OBS再起動→配信開始をOBS WebSocket経由で実行

### YouTube Live配信の教訓（重要）
- **YouTube Data APIはクォータに注意** — 10,000ユニット/日、ポーリングですぐ枯渇する
- **pytchatを使う**（APIキー不要、クォータなし、signalモンキーパッチ必要）
- **子ども向けでない + チャットON + 公開 + 通常の遅延** で設定してから接続
- **古いストリームを終了してから**新しいストリームを作成（ストリームキーが古いのに紐付く）
- **OBS画面キャプチャ**: display IDはmacOS再起動で変わる可能性あり（現在ID=2）
- 音声出力先確認: `SwitchAudioSource -c`、切替: `SwitchAudioSource -s "BlackHole 2ch"`

### YouTube Live配信情報
- **仲啓輔アカウント**: ストリームキー `pg5g-27x1-k8s9-a6um-1srj`
  - 全機能有効（標準/中級/上級すべて緑）、24時間制限なし
- **ゆいかアカウント**: ストリームキー `31ph-0za2-ce26-my5j-bxga`
- ストリームURL: `rtmp://a.rtmp.youtube.com/live2`
- YouTube Studio設定必須: 子ども向けでない / チャットON / 公開 / 通常の遅延 / デュアルストリームOFF

### しぶライブ配信システム（shibu-live.py v3）
- **映像**: OBS画面キャプチャ → YouTube RTMP（ffmpeg不要）
- **オーバーレイサーバー**: `http://localhost:8789/overlay`（Q&Aカード、3秒自動更新）
- **しぶ声読み上げ**: コメント+AI回答をElevenLabsでTTS生成、afplayで再生（音量10倍）
- **AI回答**: Claude Haiku 4.5でしぶとして回答生成（50文字以内、タイムアウト30秒）
- **漢字→ひらがな変換**: pykakasi使用、TTS読み正確化
- **音声ルーティング**: afplay → BlackHole 2ch → OBS coreaudio_input_capture → YouTube配信
- **BGM**: `~/Desktop/shinsekatsu-bgm.mp3`（新生活/騒音のない世界、3分33秒、音量0.1%ループ）
- **BGM自動ミュート**: しぶ声再生中はBGMをSIGSTOP、再生後SIGCONT
- **YouTube Chat取得**: pytchat + signalモンキーパッチ（APIキー不要、クォータなし）
- **OBS WebSocket**: ポート4455、リモートから配信開始/停止/ソース操作可能

### 配信起動手順
1. OBS起動（画面キャプチャ + BlackHole Audio入力済み）
2. `screen -dmS shibu-chat bash -c 'source ~/.zshrc; export YOUTUBE_VIDEO_ID=<ID>; export PYTHONUNBUFFERED=1; cd ~/Desktop; python3 -u shibu-live.py 2>&1 | tee /tmp/shibu-chat.log'`
3. OBS WebSocket経由で配信開始
4. ログ確認: `tail -f /tmp/shibu-chat.log`

### ElevenLabs声クローン情報
- APIキー: `~/.zshrc`の`ELEVENLABS_API_KEY`
- Voice ID: `LIDNtfJHRfi2AFJWPFeV`
- モデル: `eleven_v3`（最新）
- パラメータ: stability=0.5, similarity_boost=1.0, style=0.0
- プラン: Starter解約済み（2026/5/11まで有効、残約35,000クレジット）
- 生成コマンド: MacからcurlでAPI直叩き（Python SDK不要）

## リマインダー（セッション開始時に日付を確認し、該当日に通知すること）

- **2026/04/19**: YouTubeプレミアムを解約する（当日中に手続き必要）
- **2026/05/11**: ElevenLabs Starter プラン失効（声クローン・Scribe 使用不可に）— それまでに使い倒す

## TODO（次回Mac前での作業）

全てブラウザGUI操作が必要なため、リモートからは実行不可。

### 6. YouTubeプレミアムを解約する（4/19当日中）
- ブラウザでYouTubeの設定 → 有料メンバーシップ → プレミアム解約

### 7. ゲームCD到着後: 維新の嵐 幕末志士伝をWindows XP VMにインストール
- メルカリ注文済み（コーエー定番シリーズ版、¥2,450）— CD到着待ち
- 手順:
  1. 外付けDVDドライブにCDを挿入
  2. `dd if=/dev/disk? of=~/Desktop/ishin2.iso` でISOイメージ作成
  3. `bash ~/Desktop/winxp-start.sh --cdrom ~/Desktop/ishin2.iso` でVM起動
  4. マイコンピュータ → D:ドライブ → セットアップ実行
- VM環境: QEMU i386、Windows XP SP3日本語版、スナップショット `winxp_ready` 保存済み
- パッチ1.1.0.0はオンライン入手不可（Steam版は対応済みだがCD版用は配布終了）

### 8. Codex for Mac「Computer Use」プラグインをインストール
- 手順: Codex.app → Settings… → コンピュータの使用 → プラグイン → インストール
- 前提: macOS システム設定 → プライバシーとセキュリティ → 画面収録 で computer-use MCP を許可
- 許可後に再度 request_access を呼び、Codex を前面化してインストール操作を実行
- 4/17 11:40 試行: 画面収録権限の許可ダイアログが出たため中断、ユーザ対応待ち

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



## TODO（ElevenLabs使い倒し 〜5/11）

Starter プラン解約済み、2026/5/11まで有効、残クレジット32,472+（4/15時点）。以下の順で着手、指示を待ってから実行。

### D. しぶYouTube動画20本のScribe一括書き起こし（先行）
- ElevenLabs Scribe で word-level タイムスタンプ + 話者分離を一括生成
- 保存先: `ai-minimalist-shibu/transcripts/`
- 今後 video-use で再利用できる資産として残す

### A. video-use で過去素材を編集（Dのあと）
- しぶInstagram動画 / しぶライブアーカイブ / jetcut.py 9場面ダイジェストを video-use で再編集
- プロ品質のカット・字幕焼き込み・カラーグレーディング

### B. しぶライブ配信を再開
- shibu-live.py v3 で YouTube Live コメント読み上げ + AI回答 TTS を eleven_v3 で再稼働
- 長時間配信するとクレジット消費が早いので節度ある運用

### C. しぶ小説2編をしぶ声で朗読動画化
- 「自前のVision ProとComputer Use」「誰もいない部屋のComputer Use」をしぶ声朗読
- 映像（静止画 or スライドショー）と合成 → video-use で字幕焼き込み

## 運用ルーチン（タスク管理との二層構造）

- **CLAUDE.md = マスター**（Single Source of Truth、永続、git管理、次セッション以降も継続）
- **タスク管理システム = セッション作業ビュー**（進行状況、依存関係、セッションローカル）
- フロー: 新タスク発生 → CLAUDE.md追記 + TaskCreate / 進行 → TaskUpdate / 完了 → CLAUDE.md「完了」セクション移動 + git commit

## 今後の見直し

- **4/18 10:00**: 5セッション/日スケジュール（9/14/19/0/5時）の運用見直し

## しぶInstagram監視

- アカウント: @minimalist_sibu（認証済み、48投稿、フォロワー7万）
- Chrome DevTools MCPでログイン済み（セッション毎に再ログイン必要）
- ストーリーズ定期チェック: 毎時17分（cron、セッション内のみ）
- 新情報はai-minimalist-shibu/knowledge/shibu-ai-update.mdに追記
- Google Photosしぶ関連画像: **約272枚/615枚**（44%）チェック完了 → `docs/google-photos-shibu-inventory.md`

## Claude Codeセッションスケジュール（4/17〜、毎日繰り返し、JST）

Googleカレンダー登録済み（RRULE:FREQ=DAILY、colorId:7 Peacock）。4/18 10:00に見直し予定。

| 時刻 | セッション | 主な用途 |
|---|---|---|
| 9:00 | セッション1 | 朝の状況確認・当日TODO整理・X情報収集 |
| 14:00 | セッション2 | メイン作業・X情報収集 |
| 19:00 | セッション3 | 夕方作業・配信メンテ・X情報収集 |
| 0:00 | セッション4 | 1日のまとめ・git commit・X情報収集 |
| 5:00 | セッション5 | 夜間監視ログ確認・X情報収集 |

### X情報収集ルーチン（各セッション毎回実施）
- **手段**: agent-reach の `twitter` CLI（Cookie取得済み、@minimalistneko）
  - Cookie更新: `agent-reach configure --from-browser chrome`（Chromeでログイン維持すればOK）
  - バックアップ手段: X PWA（`com.google.Chrome.app.lodlkdfmihgonocnmddehnfgiljnadcf`、full tier）
- **対象**:
  1. For Youタイムライン: `twitter -c feed | head -30`
  2. キーワード検索: `twitter -c search "Claude"` / `"Anthropic"` / `"Opus 4.7"` など
- **出力**:
  1. `docs/x-daily-briefing.md` にセッション日時でセクション追記
  2. 要約をチャットで報告（注目ポスト・トレンド・インフルエンサー反応）
- **twitterコマンド主要**: `feed`/`search`/`likes`/`followers`/`article`/`post`/`show`（全て `-c` でLLM向けJSON）

## 完了（4/17未明）

- [x] Claude Opus 4.7 リリース確認（claude-opus-4-7、エージェントコーディング大幅向上、Opus 4.6はLegacy化）
  - 新トークナイザー、知識カットオフ2026年1月、Adaptive Thinking採用
  - 現セッションは4.6、新セッションで `claude --model opus` で4.7に切替可能
- [x] Google Gemini Mac/Windowsネイティブアプリ情報確認
  - Mac: Option+Space（コンパクト）/ Option+Shift+Space（フル）、Swift製
  - Windows: Alt+Space、TODO #5 で4/17朝インストール予定
  - Mac版は `/Applications/Gemini.app` v1.45.6.217 インストール済み
- [x] GitHub Copilot CLI brew版確認（brew install copilot-cli、Ctrl+Vスクショ入力対応）
- [x] YouTubeショーツ非表示設定の情報確認（保護者設定で0分制限→完全非表示）
- [x] Claude Codeデスクトップアプリ /btw Side chat マルチターン対応の発見
- [x] visionOS向けYouTubeアプリv1.01更新情報確認
- [x] Wi-Fi切替: 彩羽（iPad）→ 結花（iPhone 15 Pro）
- [x] Windows PC（masu-p55）オフライン確認（9時間前からオフライン）
- [x] Claude Opus 4.7 切替完了（現セッション claude-opus-4-7 で稼働中）
- [x] Googleカレンダー 1日5セッション・毎日繰り返しスケジュール作成（9/14/19/0/5時 JST、RRULE:FREQ=DAILY）
- [x] X情報収集ルーチン確立（agent-reach twitter CLI、Cookie取得済み、`docs/x-daily-briefing.md` 追記運用）
- [x] PowerShell 7.6.0 osx-arm64 インストール（brew不可のためtar.gz直、`~/local/bin/pwsh`、`CLAUDE_CODE_USE_POWERSHELL_TOOL=1` 設定済み）
- [x] Windows PC（MASU-P55）への Google App（Gemini）インストール完了
  - 既存DL済みインストーラーは 0x1252a（Omaha tag parse error）で失敗、`search.google/google-app/desktop` から再DLで解消
  - `C:\Users\gci_admin\AppData\Local\Google\Google\latest\google.exe --start_hidden` で起動、Alt+Space で呼び出し可能
  - v1.0.2.0（Canary 10%）は**英語UIのみ**、日本語ロケール未同梱（検索結果・AI Mode応答自体は日本語可）
  - appguid: `{06A8089E-0B65-445D-B5C4-10B0D1B540F2}`、ClientState lang=ja-JP（将来の多言語化で反映見込み）
- [x] Claudeデスクトップアプリ Code mode から Windows (WSL Ubuntu) への SSH 接続を実現
  - Claude Desktop Code mode は **Linux/macOS のみサポート**（Windowsネイティブは `__bin_missing__` で弾かれる）→ WSL経由で回避
  - Ed25519 鍵生成（`~/.ssh/id_ed25519`）→ WSL Ubuntu の `~/.ssh/authorized_keys` に登録
  - 先に Windows OpenSSH 側にも `C:\ProgramData\ssh\administrators_authorized_keys` を登録（gci_admin がAdmin権限のため `~/.ssh/authorized_keys` は無視される仕様）
  - WSL Ubuntu 24.04 に `openssh-server` インストール、sshd 有効化（systemd 管理）
  - Windows `netsh interface portproxy` で `0.0.0.0:2222 → WSL:22` フォワード
  - Windows ファイアウォール 2222/tcp 開放（`New-NetFirewallRule`）
  - `.wslconfig` に `vmIdleTimeout=-1` でアイドル終了無効化
  - `schtasks` で「WSL SSH Keepalive」をログオン時自動起動登録（`C:\Users\gci_admin\wsl-start.ps1` で sshd起動＋portproxy再設定＋`sleep infinity` でWSL永続化）
  - Claude Desktop 設定: `gci_admin@100.125.21.47:2222` / IDファイル `~/.ssh/id_ed25519`
  - ※ WSL IP（現 `192.168.254.131`）は再起動で変わる可能性あり、keepaliveスクリプトが自動更新
  - WSL内Claudeが自身を `Linux 6.6.87.2-microsoft-standard-WSL2` として認識することを確認
- [x] Claude Desktop v1.3109.0 Dispatch/Cowork サブプロセスのモデル確認
  - `ps aux` で Dispatch 起動時のサブプロセス引数を確認: `/claude --model claude-sonnet-4-6 ...`
  - Opus 4.7 GA後も **Sonnet 4.6 ハードコード継続**（4/15時点の制約が解消されていない）
  - UIのモデル選択（Opus 4.7 等）はメイン会話のみ反映、Dispatch/Cowork内部呼び出しは app.asar 側で固定
- [x] X投稿 2件
  - Claude Desktop Dispatch Sonnet 4.6 固定の検証結果: https://x.com/i/status/2044900089647558987
  - Claude Desktop Code mode Windows(WSL)接続の回避策: https://x.com/i/status/2044910455983050890
- [x] Claudeデスクトップアプリを閉じた（4/14判断の再確認）
  - Code mode で WSL Ubuntu への SSH 接続は実現したが、**親の Claude Code からオーケストレーションできない**ため実用性なしと判断
  - Maestri は Electron 製の Claude Desktop を制御不可（ターミナル版 Claude Code 専用）
  - Dispatch/Cowork は Sonnet 4.6 ハードコード継続、UIでモデル選択しても反映されない
  - M1 8GB でのリソースコストに見合わない（Electron×10プロセス、~786MB / CPU 27.7%）
  - WSL SSH 環境は将来のため残す（keepaliveタスク・portproxy・.wslconfig すべて稼働中）
  - crashpad handler 残存プロセス（PID 608, v1.2773.0）も kill で掃除済み
- [x] X投稿: Claude Desktop使わない結論: https://x.com/i/status/2044915100436558067

## 完了（4/17 13:00セッション）

- [x] メルペイ支払い確認（水道 13,068円 / ガス 8,522円 / 電気 11,554円 = **合計33,144円**、全てメルペイ）
- [x] システムリソース確認（load 1.24 / Pages free 4,166・inactive 2.5GB、実質逼迫なし）
- [x] **browser-use/video-use 導入完了**（Claude Code 用動画編集スキル、OSS、2026-04-12 公開、515★/41fork）
  - クローン先: `~/Desktop/video-use`（414MB）
  - シンボリックリンク: `~/.claude/skills/video-use` → `~/Desktop/video-use`
  - Python 3.12 venv `.venv/` に `pip install -e .` 完了（librosa 0.11 / numpy 2.4 / matplotlib 3.10 / scipy 1.17 / numba 0.65 / scikit-learn 1.8 / pillow 12.2 他）
  - `.env` に `ELEVENLABS_API_KEY` を `~/.zshrc` から転記
  - ffmpeg 6.0 / yt-dlp 2026.03.17 既存利用
  - 起動手順: 素材フォルダに `cd` → `claude` → `edit these into a launch video`
  - 仕組み: LLM は動画を観ず**読む** — ElevenLabs Scribe で単語単位タイムスタンプ取得 → `takes_packed.md` (~12KB) に圧縮、`timeline_view` が必要時だけ filmstrip+波形+単語ラベル PNG を生成
  - 機能: filler削除 / 自動カラーグレード / 30ms audio fade / 字幕焼き込み / Manim・Remotion・PIL でアニメ生成 / 自己評価ループ（最大3回やり直し）/ `project.md` でセッション記憶
  - 次回新セッションから `video-use` スキル自動認識（現セッションは再起動で反映）

## 完了（4/17 12:00セッション）

- [x] MCPサーバー自動起動整理（メモリ逼迫対策、Pages free 3,942 → 97,421、約1.5GB解放）
  - User-scope削除（`~/.claude.json` の `mcpServers`）: `context7` / `notebooklm-mcp` / `voicemode`
  - Desktop project-scope削除（`~/.claude.json` の `projects["/Users/yuika/Desktop"].mcpServers`）: `chrome-devtools` / `google-photos` / `playwright`
  - claude-mem プラグインは維持（セッション観察一覧・mem-search/smart-explore/make-plan/do/timeline-report/version-bump/knowledge-agent スキル稼働継続）
  - バックアップ: `~/.claude.json.bak.20260417-1215`
  - 再登録が必要になったら `claude mcp add <name> ...`
  - 次回セッションから6個のMCPサーバーは自動起動しない

## 完了（4/17 10:00セッション・iPhone SSH）

- [x] GitHubアカウント `wirelessml` のリポジトリ確認: 公開1（test、370MB、362ファイル）/非公開0
- [x] リポジトリ全文走査（README/scripts/docs全16md/shibu app code/shibu knowledge全80md/templates/.claude/.github/メモ memory/）
  - 既知ファイル多数は SessionStart hookの prior observation で1行だけ返却（コンテキスト節約）
- [x] Codex デスクトップアプリ Windows版 (MASU-P55) インストール状況確認
  - Microsoft Store版 OpenAI.Codex 26.406.3494.0、`shell:AppsFolder\OpenAI.Codex_2p2nqsd0c76g0!App` で起動成功（PowerShell `!` エスケープのため base64 EncodedCommand 経由）
  - 起動後プロセス6個・約620MB（Electron系）
  - Microsoft Store displaycatalog API（9PLM9XGG6VKS）で最新版 **26.415.1938.0** (2026-04-16リリース) を確認
  - MDM CIM `UpdateScanMethod` で更新スキャン発動（ReturnValue: 0）→ 反映なし
  - `winget install --id 9PLM9XGG6VKS --source msstore --silent --force` 実行 → MS Store認証待ちでハング・タイムアウト
  - rg-adguard.net で直接msixbundle URL取得試行 → Cloudflareチャレンジで失敗
  - **未完了**: Windows版は古い 26.406.3494.0 のまま。MS Store GUI から手動更新が必要

- [x] Codex デスクトップアプリ Mac版インストール
  - `brew install --cask codex-app` → `/Applications/Codex.app` v26.415.20818 (build 1727) 配置
  - `auto_updates` 対応、Apple Silicon専用 (arm64)、macOS ≥12 必須
- [ ] Codex Mac版の **「コンピュータの使用」プラグイン (Computer Use, openai-bundled)** インストール — **未完了**
  - SSH (iPhone 100.74.77.115 → Mac 100.99.41.2) からは Codex.app (Electron) が起動しない
  - 直接バイナリ実行 → 32KB RSS で `_dyld_start` ハング → Window未登録（Quartz CGWindowList 確認）
  - quarantine xattr 除去・署名検証OK・Notarized Developer ID・メモリ500MB+ 確保しても症状変わらず
  - 原因: SSH経由 `open -a` ではAquaセッショントークンが正しく確立されない（Tahoe 26.5の制約と推測）
  - Computer Use MCPサーバーは Claude Code CLI に未登録（GitHub #44209既知バグ、Claude Desktop専用機能）
  - cliclick / osascript / pyautogui / Playwright(Web専用) いずれも screencap+正確座標が取れず断念
  - 解決策: ユーザがMac前で Spotlight → Codex → Settings → コンピュータの使用 → インストール を直接クリック必要

- [x] 重いプロセス整理（Codex起動メモリ確保用）
  - `claude-sonnet-4-6` サブエージェント（PID 39103, 287MB）→ kill（既に消滅）
  - `chroma-mcp` (PID 1002, 333MB) → kill 成功
  - `chrome-devtools-mcp` 系 (PID 27280/27281/27245, 計140MB) → kill（その後MCP切断通知あり）
  - `bun` plugin worker (PID 967, 95MB) → kill
  - `context7-mcp` (PID 27111, 45MB) → kill
  - 結果: Pages free 6,443 → 34,341（約470MB空き増）、Total RSS 7,257MB → 6,615MB

- [x] X 投稿系の準備調査: 「2時間で企業向けLP作成」ポストの取り扱いを確認（X投稿/実装/スキル化/保存の選択肢を提示、未着手）

## 完了（4/17 9:00セッション1）

- [x] Claude Code 最新バージョン確認: **2.1.112**（Mac既に最新、npm最新も2.1.112）
- [x] 9:00セッションの仕組み再確認: Googleカレンダーは通知のみで自動起動なし（運用上は手動でClaude Code起動）
- [x] X情報収集ルーチン実施（docs/x-daily-briefing.md 追記、9:10 JST実施）
  - 注目: Claude Code週次使用制限リセット（4/16深夜）/ OpenAI Codex大型アップデート（Macアプリ操作・gpt-image-1.5） / Perplexity Comet（iMessage統合）
  - Opus 4.7の反応: @SuguruKun_ai 103 / @bioshok3 47 / @AI_masaou 38 / @claudecode_lab 35
  - "Opus 4.7は賢くなったより崩れずに走り切るのが上手くなった"（@AI_masaou）
- [x] Windows PC（MASU-P55）稼働確認: 今朝06:46:15起動、正常稼働中（Tailscale 100.125.21.47経由SSH成功）
- [x] git worktree の概念を説明（並列AI開発コンテキストで）
- [x] Claude Code 1Mコンテキスト有効化: `~/.claude/settings.json` から `CLAUDE_CODE_DISABLE_1M_CONTEXT` 削除
  - 次回新セッションから1M context有効、現セッションは起動時環境変数なので反映されない
  - 使用制限に注意（Maxプランでも週次リミットあり）

## 完了（4/16午後）

- [x] Windows XP SP3 日本語版 QEMU VMセットアップ完了
  - 目的: コーエー「維新の嵐 幕末志士伝」（1998年Windows用）をM1 Macでプレイ
  - ゲームCDはメルカリで注文済み（コーエー定番シリーズ版、¥2,450）
  - ISO: Internet Archiveからダウンロード（ja_windows_xp_professional_with_service_pack_3_x86_dvd_vl_x14-74058.iso、630MB）
  - QEMU 10.2.2（Homebrew）でi386エミュレーション
  - 仮想ディスク: `~/Desktop/winxp.qcow2`（10GB QCOW2）
  - インストール全工程をQEMU telnetモニター経由で自動操作（sendkey/mouse_move/screendump）
  - VLプロダクトキー: MRX3F-47B9T-2487J-KWKMF-RPWBY
  - ユーザー: Administrator（パスワードなし）、ネットワークなし
  - VMスナップショット `winxp_ready`（310MB）保存済み → 次回即起動可能
  - 起動スクリプト: `~/Desktop/winxp-start.sh`（`--cdrom ISO` オプション対応）
  - QEMUモニター: `telnet 127.0.0.1:4444`
- [x] 維新の嵐 幕末志士伝 パッチ1.1.0.0の網羅的調査（結果: オンラインでは入手不可）
- [x] 初代「維新の嵐」Switch 2/PS5 本日配信開始の情報確認
  - コンソールアーカイブスで配信、SNS反応はまだ少ない
  - 5chスレッドはSSL証明書障害でアクセス不可
- [x] Claudeデスクトップアプリ分析（docs/claude-desktop-app-analysis.md）
  - Code モード統合、モデル選択、工数設定、環境セレクター
  - クラウド環境はTailscale到達不可（サンドボックス外）
  - 結論: 2層構成（Mac CLI + クラウド）が最適、アプリ不要の判断維持

## 完了（4/15午後）

- [x] 毎朝TODOリスト配信を設定（2系統）
  - リモートエージェント: 毎朝8:00 JST → Gmail下書き（trig_01AXQE4PAYPQW4wyfXKFZBqY）
  - ローカルcron: 毎朝8:00 → /tmp/todo-check.log
  - スクリプト: ~/Desktop/todo-check.sh
- [x] Claude Webルーチン知見: Slack日次要約をDMに自動送信するプロンプト安定化
  - slack_search_public_and_private + after:YYYY-MM-DD
  - Slack記法対応（##不可→【】■*太字*使用）
  - user_idをchannel_idとして直接指定
- [x] GitHub Copilot CLI v1.0.27 インストール（npm経由、gh copilot組み込み済み）
  - Freeプラン: 月50プレミアムリクエスト、GPT-5 miniがデフォルト
  - 非インタラクティブモード: `copilot -p "prompt"` でClaude Codeから指示可能
  - GitHub MCP経由でリポジトリアクセス確認済み
- [x] ElevenLabs残高確認（32,472/40,000クレジット、5/11まで有効）
- [x] DaVinci Resolve 21 写真編集ページのナレッジ保存（docs/davinci-resolve-photo-editing.md）
- [x] Mind Render / AI Drill 調査（東大共同開発ML教材、2026/4月に無料公開）
- [x] Unity Hub 3.16.4 インストール（brew、Unity 2021.3 LTSインストールは保留）
- [x] Agent-Reach v1.4.0 インストール（pipx、GitHub zip）
  - 8/16チャネル有効: GitHub, YouTube, 微信公衆号, V2EX, RSS, Exa検索, Jina Reader, Bilibili
  - yt-dlp（pipx版）、rdt-cli v0.4.1 追加インストール
  - twitter-cli インストール済み（Cookie未設定、ChromeでXログイン後に設定予定）
  - Claude Codeスキルとして自動登録済み
- [x] pipx 1.11.1 インストール（brew）
- [x] 操作ルール追加: 削除・一括更新前は件数報告+確認必須
- [x] AI駆動開発ツール時系列まとめ（Copilot→Cursor→Cline→Replit→Claude Code→Codex→OpenCode）

## 完了（4/15昼）

- [x] Claudeデスクトップアプリ Dispatch/Coworkサブプロセスが Sonnet 4.6 固定であることを発見
  - UIで「Opus 4.6」を選んでもCoworkサブプロセスには反映されない
  - psコマンドで `--model claude-sonnet-4-6` を確認
  - app.asar解析でコード上もモデル選択がUI非連動と判明
  - Mac/Windows両方で確認済み（v1.2581.0、同一app.asar）
  - DispatchはComputer Useの要で、Windowsではこれが唯一の手段
  - 設定ファイルでの変更手段なし
- [x] Claude Code CLI最新確認（Mac/Windows両方 2.1.108、最新）
- [x] Claudeデスクトップアプリ最新確認（v1.2581.0、Homebrew cask 1.2278.0より新しい、自動更新済み）
- [x] Mac/Windows両方のClaudeデスクトップアプリ終了
- [x] しぶチャットボット復活（サーバー起動 + Cloudflare Tunnel公開）

## 完了（4/15午前）

- [x] Dataverse「システム管理者」ロールを仲啓輔に付与
  - 原因: Dataverse環境プロビジョニング時にGlobal Admin→System Administrator自動同期が発生せず、人間ユーザーにシステム管理者が未付与のチキン＆エッグ問題
  - 試行して失敗した方法（9種類以上）:
    - Dataverse Web API `Associate` → 403 prvAssignRole
    - BAP Admin API `addUser` → 200だがロール未付与
    - BAP Admin API `roleAssignments` → 403 LinkedEnvironmentForbiddenOperation
    - PPAC UI「ユーザーの追加」→ Dataverse APIに透過し権限エラー
    - PowerShell `Set-AdminPowerAppEnvironmentRoleAssignment` → CDS環境非対応
    - MSCRMCallerID/CallerObjectId 偽装 → 403
    - Dynamics 365 UCI「ロールの管理」→ ボタン非表示（権限不足）
    - Power Platform API (api.powerplatform.com) → ロール管理エンドポイント無し
  - **解決方法**: レガシーDynamics 365 UIの「管理者に昇格」機能
    - 経路: `main.aspx?settingsonly=true` → 設定 → セキュリティ → ユーザー → ツールバー「管理者に昇格」
    - 内部: `Mscrm.SystemUserActions.promoteToAdmin()` → `/_grid/cmds/dlg_promotetoadmin.aspx?userid=<id>`
    - サーバー側でAzure AD Global Admin権限を直接チェックし、prvAssignRoleをバイパス
- [x] Copilot Studio正常アクセス確認（「追加のアクセスが必要です」エラー解消、ウェルカム画面表示）
- [x] Copilot Studioエージェント作成・Claude Opus 4.5をプライマリモデルに設定
  - エージェント名: Copilot Studio エージェント（Claude Opus 4.5）
  - エージェントID: 7555f9b5-6b38-f111-88b5-6045bd51375e
  - 環境: SUMA-p (default) / Default-f0460786-8be9-4e25-8de6-291b84b9c42e
  - 指示: 日本語AIアシスタント（Web検索有効）
  - チャネル: Microsoft Teams / Microsoft 365 Copilot
  - Teams Web動作確認済み（富士山の質問に表付き回答）
  - 公開日: 2026/4/15
  - Copilot Studio URL: https://copilotstudio.microsoft.com
  - Teams URL: https://teams.cloud.microsoft/ → Copilot → エージェント選択

## 完了（4/14午後）

- [x] M365 Copilot Chat Claude Opus 4.6 調査・ナレッジ作成（docs/m365-copilot-claude-opus.md）
- [x] Copilot Studio仕様調査（料金・モデル・制限事項・Mac対応）
- [x] Copilot Studio Claude Opus/Sonnet 4.6 プライマリモデルGA情報追記
- [x] Claudeデスクトップアプリ不要の判断を記録（Dispatch唯一の差別化だがリソースコスト過大）
- [x] Microsoft Edge インストール（Homebrew、Mac）
- [x] EdgeでCopilot Studio URL表示（Microsoftサインイン画面まで）
- [x] Safari終了（Copilot Studio非推奨）
- [x] Windows PC全プロセス終了→再起動（SSH経由 shutdown /r /t 0）
- [x] Windows Claude Code認証修復（Mac OAuth keychain→Windows転送）
- [x] Windows Claude Code Bunクラッシュ対応（Segmentation fault、メモリ不足が原因）
- [x] OBS・Maestri・shibu-chat・BGM全停止（CPU負荷軽減）
- [x] afplay BGM 19プロセス重複→クリーンアップ（1プロセスに）
- [x] claude.ai M365コネクタ未ロールアウト確認
- [x] 定時報告3回（15:35, 16:35, 17:35）
- [x] CPU/メモリ監視・定時報告の定期実行停止（ユーザー指示）
- [x] Claude Code 2.1.105→2.1.107アップデート
- [x] Copilot Studio Edgeログイン画面スクリーンショット→GitHub Pages公開

## 完了（4/14午前）

- [x] 定時報告6回実施（04:37, 05:35, 06:35, 07:35, 08:35, 09:35, 10:35）
- [x] Maestri使い方ガイドHTML作成・GitHub Pages公開（docs/maestri-guide.html）
- [x] Obsidian Claude エコシステム ガイドHTML作成・公開（docs/obsidian-claude-guide.html）
- [x] Windows PC Claude Code npm版削除→スタンドアロン版統一（2.1.105）
- [x] Windows PC Claude Code自動更新設定（タスクスケジューラ毎日0:00）
- [x] Windows PC npm版インストールブロック（@anthropic-ai スコープ無効化）
- [x] masu-p55 Tailscale復旧（masupのtailscale-ipn停止で解決）
- [x] Maestri解説動画ナレッジ保存（docs/maestri-youtube-masao.md）
- [x] BGM変更: 新生活/騒音のない世界（shinsekatsu-bgm.mp3）
- [x] shibu-live.py v3: AI回答（Claude Haiku）、ひらがなTTS（pykakasi）、BGMミュート、音量調整

## 完了（4/14早朝）

- [x] Maestriインストール（themaestri.app、DMG→/Applications/Maestri.app）
- [x] Maestri上にClaude Code 2台作成（ターミナルツール→Claude Codeクイックスタート）
- [x] 2台のClaude Code間を接続（Connection機能、物理アニメーション付きケーブル）
- [x] Maestri内Claude CodeでRemote Control有効化（/rc）
- [x] MCP接続確認（9サーバー中8接続、plugin:github:github のみfailed）
- [x] Chrome終了によるCPU負荷改善（load 18→2）
- [x] しぶの一日一食ページ作成・GitHub Pages公開（docs/shibu-one-meal.html）
- [x] CLAUDE.mdユーザー情報修正（雇用保険受給なし）

## 完了（4/13夕方）

- [x] gh CLI再認証（wirelessml、OAuth + GitHub Mobile）
- [x] YouTube Data API 403修正 → pytchatに切り替え（クォータ不要）
- [x] OBSマイクミュート（環境音除去）
- [x] マルチ出力デバイス作成（MacBook Airスピーカー + BlackHole 2ch）
- [x] OBS画面キャプチャ追加・権限付与・OBS再起動
- [x] 画面キャプチャのdisplay ID修正（0→2）+ スケーリング（5120x2160→1280x720）
- [x] OBS配信再開（WebSocket経由）
- [x] Windowsマシン作業の把握（セッションログ・マニュアル・claude-mem等）

## 完了（4/13午前、Windowsマシン）

- [x] YouTube Live コメント読み上げ問題修正（動画ID・pytchat→YouTube API・afplay追加）
- [x] youtube-live-manual.md 作成（Win操作→Mac配信の完全マニュアル230行）
- [x] claude-mem インストール（Windows + Mac両方）
- [x] Mac定時報告再開（report.sh + cron毎時33分）
- [x] Claude Code settings.json最適化（両マシン）
- [x] Mac Claude Codeログイン修復（Windows credentials.jsonをSFTP転送）

## 完了（4/12夕方）

- [x] しぶライブ配信システム v2 構築（shibu-live.py 271→403行）
  - v1（プロトタイプ）→ v2（オーバーレイ・Chat連携・回答読み上げ）
  - オーバーレイHTTPサーバー（localhost:8789、Q&Aカード表示、CSS animation）
  - YouTube Live Chat自動取得（chat_downloader、APIキー不要）
  - 質問+回答の両方をしぶ声読み上げ（ElevenLabs eleven_v3）
  - YouTube RTMP配信テスト成功（画面キャプチャ、ステータス「非常に良い」）
  - ノイズフィルタで1800Kbps確保（静的画面では42Kbps→1800Kbpsに改善）
  - YouTube 24時間有効化待ち（初回ライブ配信のチャンネル制限）
- [x] chat_downloader, pytchat インストール
- [x] gcloud SDK認証試行（expect/FIFO等、最終的にブラウザ認証が必要と判明）
- [x] Google Cloud YouTube Data API v3 有効化確認（プロジェクト: My First Project）

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

- 現在無職（雇用保険受給なし）
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

- **セッション開始時にターミナルを常に最前面に設定する**（ユーザーに案内して実行）
  - SkyLight プライベートAPIでウィンドウレベルをフローティング（3）に設定
  - コマンド:
    ```bash
    /usr/bin/python3 -c "
    import ctypes
    sl = ctypes.CDLL('/System/Library/PrivateFrameworks/SkyLight.framework/SkyLight')
    SLSMainConnectionID = sl.SLSMainConnectionID
    SLSMainConnectionID.restype = ctypes.c_uint32
    SLSSetWindowLevel = sl.SLSSetWindowLevel
    SLSSetWindowLevel.argtypes = [ctypes.c_uint32, ctypes.c_uint32, ctypes.c_int32]
    SLSSetWindowLevel.restype = ctypes.c_int32
    conn = SLSMainConnectionID()
    import subprocess
    r = subprocess.run(['osascript', '-e', 'tell application \"Terminal\" to get id of every window'], capture_output=True, text=True)
    for wid in r.stdout.strip().split(', '):
        if wid.strip():
            result = SLSSetWindowLevel(conn, int(wid.strip()), 3)
            print(f'Window {wid}: level=3 (floating), result={result}')
    "
    ```
  - ウィンドウを閉じて再度開くとリセットされるため、毎セッション実行が必要
  - 元に戻す場合はレベルを0に設定
- セッション開始時に `/model opusplan` を実行する（思考=Opus、実行=Sonnetの自動切り替え）

## 操作上の注意

- **記事の削除や一括更新をする前は、必ず件数を教えて確認を取ること。それ以外は確認不要**
- computer-use操作時、アクセス許可リクエストを事前説明せず直接実行する
- Dispatchは使わない、CLIで完結させる
- **Claudeデスクトップアプリは不要**（4/14判断）
  - Dispatch（iPhone操作）だけが唯一の差別化だが、SSH経由でClaude Code CLIを直接操作可能
  - M1 8GBではDesktop起動でload急増（Electron製、load 85まで跳ねた実績あり）
  - MCP・Computer Use等の機能はCLIでも利用可能
  - リソースコストに見合わないため、今後は起動しない方針
- ブラウザはcomputer-useでtier "read"（クリック不可）、URLを開くことはできるが再生・停止などの操作は不可
- **X PWAアプリ（Chrome PWA）はcomputer-useでfull tier操作可能**
  - バンドルID: `com.google.Chrome.app.lodlkdfmihgonocnmddehnfgiljnadcf`
  - ブラウザ扱いではないのでクリック・入力・投稿が全てできる
  - @minimalistnekoでログイン済み
  - X投稿はこのPWA経由で操作する（Safari/Edge/Brave/Chromeは全てtier read）
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

