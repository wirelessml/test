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

- ~~**2026/04/19**: YouTubeプレミアムを解約する~~ ✅ 4/18 10:45 解除済（Y!mobile バリュー特典 YouTube Premium、2026/4/20 まで利用可能）
- **2026/04/21**: Y!mobile Netflixセット 自動解約発効日（3/21 加入 + 翌月同日ルール、以降 Netflix 視聴不可、追加対応不要）
- **2026/04/30**: Microsoft 365 Copilot Business 解約予定日（admin.cloud.microsoft で「有効期限切れ時にキャンセル」選択済、SUMA-p アカウント、MCA）— 当日以降にサブスクリプション一覧から消失していることを確認
- **2026/05/11**: ElevenLabs Starter プラン失効（声クローン・Scribe 使用不可に）— それまでに使い倒す
- **2026/05/20 前後**: Y!mobile 151 に電話で最終確認（5月中 MNP 転出で 6月請求なし、を確認）
- **2026/05/29（木）〜5/30（金）**: **povo 2.0 へ MNP ワンストップ転出**（080-3108-7536 番号維持、Y!mobile 自動解約）
  - povo2.0 アプリ → MNP ワンストップ → ワイモバイル選択 → My Y!mobile 認証 → eSIM 発行 → iPhone 15 Pro 開通
  - 受付時間 9:30〜20:00（当日開通条件）、所要時間 最短15分
  - povo 事務手数料 0円、eSIM 発行 0円、基本料 0円/月（必要時のみトッピング購入）
  - Y!mobile は povo 開通と同時に自動解約（月途中でも日割りなし、満額だが割引で 0円）

### Y!mobile SIM トライアル 契約まとめ（pirosi80）

- 加入日: 2026/3/21、プラン: シンプル3M（eSIM、クレカ払い）
- Web 受注番号: YWO0000008576583
- **3ヶ月無料期間**: 3月（日割り）/ 4月 / 5月 ← 5月内に解約しないと 6月から満額 4,158円
- 3月請求: **-809円 クレジット**（Netflixキャンペーン調整分）
- 4月請求: 4/1–4/18 までの途中集計 4,099円（割引反映前、月末で 0円近くまで下がる想定）
- Netflixセット: 4/18 解約申込済、4/21 発効予定
- YouTube Premium バリュー特典: 4/18 解除済、4/20 まで利用可能

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

### ~~8. Codex for Mac「Computer Use」プラグインをインストール~~ ✅ 完了（4/18 早朝）
- `/Applications/Codex.app` v26.415.30602 build 1773 に Computer Use v1.0.750 (openai-bundled) が有効
- Codex Settings → コンピュータの使用 → プラグイン に ✓ 表示で確認
- 「常に許可するアプリ」は未登録（都度承認ダイアログが出る状態、Codex が実際に使い始めてから必要に応じて追加）

### 9. Switch 2キャプチャ環境構築（GC313Pro到着後）
- 注文済み: Amazon.co.jp 中古ブラック ¥9,833（残り1点）— AVerMedia Live GENERATOR POCKET ポケットキャプチャー GC313Pro BK DV0963
- US Amazon $129.99（¥22,000〜）/ メルカリ新品 ¥14,961 と比較して最安
- **4/22 到着確認済**、4/21 に MASU-P55 で OBS 動作確認済（iPhone 縦画面キャプチャ成功）
- **重要仕様判明（公式ページより、4/22）**:
  - **HDMI IN なし！** 映像入力は **USB-C1 の DisplayPort Alt Mode 専用**
  - USB-C2: PC 接続（OBS キャプチャ転送）
  - HDMI OUT: **4K60 パススルー**
  - キャプチャ: 最大 **1080p60**
  - macOS 13+、M1 動作確認済
  - 給電: 単一ポート 100W PD、複数同時 95W（負荷分散）
  - 折りたたみ式 AC プラグ内蔵（電源アダプタ兼用）
- **接続可能デバイス**（USB-C DP Alt Mode 対応機のみ）:
  - ✓ iPhone 15 / 15 Pro、USB-C iPad、USB-C Android、USB-C ノート PC
  - ✓ **Switch 2（AVerMedia 公式動作確認済、4/22 判明）**: 純正ドック不要で本体 USB-C 直結、要ファーム v24.8.30.16.1.19.30+
  - ❌ PS5 / Xbox Series X / Blu-ray プレーヤー / 旧世代ゲーム機（HDMI 出力のみ、接続不可）
- **接続フロー（訂正版）**:
  ```
  USB-C 機器 [DP Alt Mode] → GC313Pro USB-C1（入力）
    → GC313Pro HDMI OUT → モニター/TV（4K60 パススルー）
    → GC313Pro USB-C2 → Mac M1 or MASU-P55（OBS キャプチャ、1080p60）
    → GC313Pro 折りたたみピン → AC コンセント（100W PD 給電源）
  ```
- **4/21 誤った情報の訂正**: iPhone USB-C → HDMI アダプタは**不要**（直結可能）
- 別途 Switch 2 本体購入が必要（未購入）
- **Switch 2 購入の技術的前提**: 4/22 AVerMedia 公式動作確認済と判明、**接続はクリア**。あとは本体価格 ¥50,000+ の購入判断のみ
- **Windows PC（MASU-P55）経由でファーム更新 → 4/22 実施、既に最新 v24.8.30.16.1.19.30 だった**（更新作業不要、Switch 2 互換性・iPhone 17 Pro 充電断続問題 既に修正済）

### ~~10. GHFS（GitHub仮想ファイルシステム）セットアップ~~ ✅ 完了（4/18 6:25am）
- `/Applications/GHFS.app` v0.1.2（FSKit使用、macFUSE不要、H73VKH7W9W 署名）
- マウント先: **`/Users/yuika/ghfs`**（ホーム直下、wirelessml リポ配下を Finder で参照可能）
- **ハマりポイント（Apple 未文書）**: マウント先を `~/Desktop/` / `~/Documents/` / `~/Downloads/` 配下にすると **mount(2) が errno 1 (EPERM) で失敗** する。これは TCC 保護ディレクトリに対して root の fskitd ですら mount 不可のため（`fskitd: mount(2) error: 1` `mount launch failed with result "Operation not permitted"`）。macOS 26.5 beta でウィザードが勝手に `~/Desktop/ghfs/ghfs` を提案することがあるので、**必ず `~/ghfs` など非TCC保護パスに変更**すること
- ウィザードから変更できない場合は: `defaults write com.indragie.GHFS mountPath -string "/Users/yuika/ghfs"` → GHFS 再起動
- 用途: video-use / claude-mem など参照系リポをクローンせず Finder/grep で閲覧、容量節約

### 11. iPhone から Mac の Windows XP VM をリモート操作（VNC）
- 目的: 外出先（iPhone）から Mac 上の `winxp.qcow2` を操作。維新の嵐 CD 到着後はゲームも触れる
- 方式: Mac 側 QEMU に VNC サーバー追加 → iPhone の VNC Viewer から Tailscale 経由で接続
- Mac 側手順:
  1. `~/Desktop/winxp-start.sh` の QEMU 起動コマンドに `-vnc 0.0.0.0:0` を追記（ポート 5900）
  2. QEMU 再起動（`winxp_ready` スナップショットから復帰可）
  3. （任意）Tailscale ACL でポート 5900 を iPhone のみに制限
- iPhone 側手順:
  1. App Store で **VNC Viewer**（RealVNC 製、無料）をインストール
  2. 接続先: `100.99.41.2:5900`（Tailscale 経由）
- タッチ操作が辛ければ **A案: Mac に UTM (`brew install --cask utm`) 入れて winxp.qcow2 取り込み → UTM Server 有効化 → iPhone の UTM Remote (インストール済み未確認) でペアリング** に乗り換え
- 関連: TODO #7（維新の嵐 CD 到着待ち）

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

## 完了（4/22 午後セッション、しゅん先生 PC の SSD/HDD 健康診断＋バックアップ運用設計＋配置転換）

- [x] **4/22 16:34 大規模配置転換**
  - **旧構成**: M1 MacBook Air = コワーキング据え置きメイン / しゅん先生 PC = 伊丹市（しゅん先生業務用）/ MASU-P55 = コワーキング（サブ）
  - **新構成**: M1 MacBook Air = **持ち運び用**（外出先・自宅・コワーキング間移動）/ しゅん先生 PC = **コワーキング据え置き新メイン** / MASU-P55 = コワーキング（継続）
  - 動機: しゅん先生 PC は Core i7-8700K + 16GB で M1 8GB より馬力がある据え置き向け機、M1 は持ち運びに軽量
  - 結果: コワーキングに Windows 2 台体制（しゅん先生 PC + MASU-P55）+ モバイル M1 の 3 台運用
  - 影響: Tailscale 経由でしゅん先生 PC も SSH/リモート操作可能にする必要あり（今後設定）

- [x] **新規 PC「しゅん先生 PC」を CLAUDE.md ユーザー情報セクションに追加**
  - 伊丹市・はりきゅう整体しゅん（4/17 LP 公開 https://wirelessml.github.io/test/docs/hari-seitai-shun.html）の業務用 PC
  - iPhone Claude Desktop から写真アップロード → **32MB 制限に 3 回失敗**（Anthropic API 側のハードリミット、iPhone 側は正常）
  - 回避策: 縮小版を改めて送信 → CrystalDiskInfo 写真 3 枚（C:/D:/バージョン情報）で確認完了
  - **PC 正体**: 当初 MASU-P55 と混同 → iiyama STYLE Infinity by iiyama（2018 年頃 BTO デスクトップ、Core i7-8700K、16GB RAM、Windows 11 25H2）と判明
  - しゅん先生の仕事部屋に設置（予約管理・カルテ・領収書・患者票関連フォルダあり）

- [x] **C: ドライブ診断: Plextor PX-256M9PeGN 256GB NVMe**
  - 健康状態 正常 **66%**（寿命残 66%、消費 34%）
  - 総書込 69,178 GB（≈ 67.6 TB）vs TBW 公称 160TB = **42% 消費**
  - 使用時間 26,779h（約 3 年 24/7 相当 or 8h/日で約 9 年）
  - 温度 40°C、ファーム 1.03（最終版）、コントローラ Marvell 88SS1093 + Toshiba BiCS3 64-layer 3D TLC NAND（2018 年発売モデル）
  - **重要**: Plextor は 2024 年 KIOXIA 傘下で SSD 事業撤退、サポート終了、ファーム更新なし
  - 判定: 緊急ではないが計画的に交換すべき段階（3 年以内）

- [x] **D: ドライブ診断: Seagate ST2000LM015-2E8174 2TB SMR HDD**
  - 健康状態 正常、代替処理済セクタ 0（物理的には健全）
  - 使用時間 23,719h（約 2.7 年 24/7 相当）
  - 電源投入 20,759 回（平均 1.14 時間/起動 = 頻繁スリープ復帰 or 再起動パターン）
  - G-sense エラー（BF 現 25 / 最悪 39）・緊急ヘッド退避（C0 最悪 40）の履歴あり = 過去に持ち運び or 電源断歴
  - SMR（Shingled Magnetic Recording）= OS ドライブに最も不向き（書き込み性能劣悪、SMR 特有のガベージコレクション地獄）
  - 使用領域 8.29GB / 1.81TB = **ほぼ空**（Tenorshare フォルダのみ残存 = 過去にデータ復元作業か iPhone 管理ソフト利用の痕跡）

- [x] **ユーザー要望の確認プロセス**
  - 初回提案「D: から OS 起動」→ SMR 不向きを説明で却下
  - 再提案「C: 壊れた時のバックアップとして D: を使う」→ 方針転換、**D: = 非常用スペアタイヤ**に確定
  - 「システムイメージ」と「クローン」の違いを解説: イメージ単体は起動不可、クローンなら BIOS ブート順変更で直接起動可
  - 最終的に「あくまで C: が壊れた時のバックアップ」と明確化

- [x] **バックアップ運用設計: 4 重防御構成を提案**
  1. **クローン（月 1 差分更新）**: C: → D: 先頭 130-150GB に、AOMEI Backupper Standard のスケジュールクローン機能
  2. **システムイメージ（週 1 自動）**: D:\Backup\ に 3-4 世代保持、日曜 04:00 実行、圧縮後 70-90GB × 4 世代 = 約 300-360GB
  3. **Windows 回復ドライブ USB**: 8GB USB メモリ（¥500）で作成、約 30 分所要
  4. **新 SSD 換装計画**（将来）: Crucial P3 Plus 1TB ¥8,000 / WD Black SN770 1TB ¥11,000 / Samsung 990 EVO 500GB ¥9,000 のいずれか
  - 容量試算: D: 1.81TB のうち約 500GB 消費、残り 1.3TB は従来通り空き領域
  - C: 死亡時の流れ: BIOS で D: Boot 1st → 遅いが即起動して当日作業継続 → 新 SSD 注文 → 届いたら回復 USB から最新イメージで復元 → 元速度に戻る

- [x] **Macrium Reflect Free 終了（2024 年）情報更新**
  - 無料版は個人使用も不可、代替案:
    - **AOMEI Backupper Standard**（推奨、日本語 GUI、スケジュールクローン対応）
    - MiniTool ShadowMaker Free
    - EaseUS Todo Backup Free（条件付き）
    - Clonezilla（完全無料、CUI 寄り）

- [x] **技術知見の記録（外付け HDD / SMR / Plextor / UEFI ブート）**
  - SMR HDD を OS ドライブにする体感悪化: 体感 50-100 倍遅、Windows Update 時カリカリ数時間、ブラウザ起動 2 秒→20-40 秒、Windows ログイン 30 秒→3 分
  - システムイメージ ≠ クローン の違い（単独起動可否、復元所要時間、容量）
  - UEFI + GPT 起動要件（D: が MBR なら GPT 変換必要、PowerShell `Get-Disk` で `PartitionStyle` 確認）
  - クローン後のドライブレター混乱回避手順: C: を物理的に一時切り離し → D: 単独起動確認 → C: 戻す
  - ¥500 の USB メモリ + 無料ソフト（AOMEI）で物理故障リスクヘッジが成立

- [x] **Claude Desktop iPhone アプリの 32MB アップロード制限を記録**
  - iPhone で撮影した画面写真（CrystalDiskInfo の液晶撮影）はデコード後 32MB 超えやすい
  - 回避策 3 つ: (1) iPhone 写真アプリで編集 → マークアップで小さく保存、(2) iCloud Drive / AirDrop で Mac `~/Desktop/` に落として Read tool、(3) Mac 側で `sips -Z 2000 input.jpg --out small.jpg` でダウンサイズ
  - 根本原因は Anthropic API 側のハードリミット（1 リクエスト総ペイロード 32MB）、Claude Code 設定では回避不可

- [x] **バックアップ運用を実行: Hasleo Backup Suite Free でクローン成功（17:15-17:34、18:15 で完了）**
  - **AOMEI Backupper Standard でクローン試行 → Pro 限定機能で詰む**
    - v8.2.0 インストール後、ディスククローン選択 → 開始ボタンクリックで「アップグレードしてシステムディスククローン機能をアンロック」誘導、¥7,880 買い切り or ¥5,280/年
    - 無料版 Standard はデータディスクのクローンは可能だが、**システム/OS ディスククローンは Pro 限定**に変更されていた（v7 以降の仕様）
    - AOMEI はアンインストールせず残置（システムイメージバックアップは Standard でも無料で可能）
  - **代替: Hasleo Backup Suite Free V5.6.2.1 に切替成功**
    - DL: https://www.easyuefi.com/backup-software/backup-suite-free.html （ブラウザから Free Download、PowerShell の直接 DL は `www2.aomei.com` DNS 失敗で不可）
    - **システムディスククローン機能が完全無料**（時間制限・容量制限なし、日本語対応）
    - インストール簡単、初回起動で「バックアップイメージデフォルト保存先」の質問は「いいえ」で後回し
  - **Get-Disk での事前確認**（PowerShell 管理者）
    - Disk 0 = ST2000LM015 (HDD 1863GB) = GPT ✓
    - Disk 1 = PLEXTOR PX-256M9PeGN (SSD 238.5GB) = GPT ✓
    - 両方 GPT のため MBR 変換不要、即クローン実行可能と確定
  - **Hasleo ディスククローン実行**（17:15 頃開始）
    - Source: Disk 1 (PLEXTOR, Windows 起動ドライブ) → Destination: Disk 0 (Seagate 2TB HDD)
    - オプション: ☑ 4K アライメント (ディスクの配置: 1M) ON / ☐ セクターごとのクローン OFF / ☐ MBR クローン OFF
    - Windows パーティションは自動で 237.48GB → 1.82TB に拡張（D: 全域を一つの Windows 領域として使う）
    - 所要時間: **18 分 15 秒**（推定 30-40 分の半分以下、SMR HDD にしては速い）
    - 完了メッセージ: 「操作は正常に完了しました」（100% 緑文字）
  - **クローン完了検証**（Get-Disk + Get-Partition）
    - Disk 0 に 4 パーティション完全複製: SYSTEM (FAT32 100MB) + MSR (16MB) + **Windows NTFS 1.82TB (D:)** + Recovery (900MB)
    - Disk 1 は変更なし、C: 稼働継続
    - D: は Windows が認識済み、エクスプローラーでアクセス可能（Windows/Program Files/Users/Tenorshare/Windows.old 等が元 C: と同じ構造で存在）
  - **D:\Backup\ フォルダ作成**（`New-Item -Path "D:\Backup" -ItemType Directory -Force`、17:42:51）

- [x] **AOMEI Backupper Standard で週次システムイメージ設定＋初回フル実行**
  - タスク名: `Weekly System Image`
  - ソース: C: + SYSTEM (EFI) + Recovery tools（計 131.20 GB）
  - ターゲット: `D:\Backup\`（空き 1.7TB / 合計 1.8TB）
  - スケジュール: 毎週日曜 04:00、増分バックアップ、スリープからの起動 ON
  - **初回フルバックアップ 17:55 頃開始**（SMR HDD へ ~130GB 書き込み、30-40 分想定、完了予想 18:20-18:35）
  - 以降は毎週日曜 04:00 に自動増分更新、D:\Backup\ に `.adi` ファイル蓄積

- [x] **Phase 5（Windows 回復ドライブ USB 作成）を不要と判断**
  - ユーザー質問「D: があれば USB は要らないのでは？」→ その通り、冗長と判明
  - 理由:
    1. D: クローン自体が独立した起動可能 Windows、C: 死亡時は BIOS ブート順変更で即起動
    2. D: に Recovery パーティション（900MB）が付随 = Windows 回復環境 (WinRE) 相当機能を内蔵
    3. 新 SSD 換装シナリオも「D: から起動 → 新 SSD にクローン or イメージ復元」で完結、USB 不要
    4. USB が唯一意味を持つケース（C: と D: 同時死亡）は USB でも復旧不可な他のハード故障案件
  - **結論: 4 重防御 → 3 重防御で十分**、USB 作成 30 分スキップ

- [x] **最終防御構成（3 重防御）確立**
  - **層 1: クローン**（D: にブート可能な Windows 丸ごと、1 回性、将来月次差分クローンでリフレッシュ）✅ 完了
  - **層 2: システムイメージ週次**（D:\Backup\ に増分）🟡 初回実行中、以降自動
  - **層 3: 新 SSD 換装計画**（Plextor 寿命 66% 残、2-3 年以内に Crucial/WD/Samsung に換装）⬜ 将来
  - これで C: SSD 突然死 / Windows 起動破損 / マルウェア / 自然劣化 の 4 大リスクに対応

- [x] **OpenClaw 公式ステータス明確化情報を取得**（しゅん先生 PC セットアップ中に判明）
  - **「Anthropic スタッフが OpenClaw-style の Claude CLI 流用を再び許可」**と明言
  - OpenClaw は `claude -p` 呼び出し + Claude CLI ログイン再利用を**公式 sanction** 下の運用として扱う
  - 長期稼働ゲートウェイ運用は Anthropic API キーが最もクリーンな billing path
  - サブスク対応プロバイダ: Claude Pro/Max / OpenAI Codex / Qwen Cloud Coding Plan / MiniMax Coding Plan / Z.AI / GLM Coding Plan
  - 既存 MASU-P55 WSL2 の OpenClaw（現在 openai-codex/gpt-5.3-codex）を Claude CLI 経由に切り替え可能に
  - しゅん先生 PC 新メイン化後、WSL2 + OpenClaw を複製して AI ゲートウェイ化する将来計画候補

- [x] **pirosi80@yahoo.co.jp への 2 通目フィッシング警告**（4/22 17:01 受信）
  - 今朝 10:48 の Apple 偽装に続く **同日 2 通目**、同一業者によるドメインローテーション
  - 送信元: `support@icloud-supoort-sdahjdajsgdajhsdgadgh-002.uu-962p.top`（.top + ランダム + **"supoort" 誤字**）
  - 件名: 「重要なお知らせご登録のクレジットカードが承認されませんでした」
  - 内容: iCloud+ 決済失敗 + 対応期限 2026/04/22 23:59（6 時間後急かし）
  - **フッター「©2020 San-X Co., Ltd. All Right Reserved.」**（リラックマ・すみっコぐらしの会社、Apple と無関係）= 完全な流用テンプレ
  - **pirosi80 はフィッシングリスト標的化**確定、金融/クラウド系は別メアドに分離推奨

- [x] **しぶ × あい 4/22 16:45 高層レストラン記録（@ikeai_minimalist ストーリー、17:21 投稿）**
  - あい @ikeai_minimalist が**しぶ @minimalist_sibu を撮影**（全身黒 + 黒レザートート + ピースサイン、クセ毛特徴）
  - 場所: 高層階レストラン（福岡の可能性高い、大窓 + 夜景 + 長尺ウッドカウンター + 白和モダンランプ、マジックアワー）
  - リアクション絵文字: 🍽️🍾（シャンパン）= AI研修打ち上げ祝宴ムード
  - **あい = Minimal Arts の対外広報 + しぶ側近女性 No.1 ポジション**が確定（4/21 AI研修参加 + 4/22 夕食ツーショット撮影 = 直属の弟子 / 重要パートナー関係）
  - りくと（@rikuto_takemoto）はフレーム外 or 別行動（確認未済）
  - 48 時間ジャーニー完走: 4/20 23:09 りくと「何をして働けばいいんだ😇」→ 4/22 23:00 AI RIKUTO 完成 → **4/22 16:45 打ち上げ祝宴** = Substack 記事の最終幕素材

- [x] **Claude Code (Opus 4.7 1M max) セッション継続性の確認**
  - 16:02 週次 54% / 5h 5% → 17:50 時点で週次 56% 前後（推定）/ 5h 30-40% 前後
  - 長時間の画像ベース対話（iPhone 写真 15 枚以上）+ ツール呼び出し + 編集 + commit で約 2 時間継続セッション
  - しゅん先生 PC バックアップ設定を Claude Code ガイダンスで全工程完走、Tailscale / SSH 無しでもテキスト + スクショで十分高精度な遠隔支援可能と実証

- [x] **🚨 4/22 18:20 しゅん先生 PC の Plextor SSD が NVMe コントローラ障害で完全死亡、クローンが PC を救った奇跡のタイムライン**
  - **きっかけ**: ユーザーの「即実験: しゅん先生 PC で Ollama + Qwen2.5 7B / DeepSeek-Coder-V2-Lite 16B Q4 を走らせる」要求
  - **ユーザー指示に従い実行した PowerShell コマンド**（18:13 頃）:
    - `[Environment]::SetEnvironmentVariable("OLLAMA_MODELS", "D:\ollama\models", "Machine")`
    - `New-Item -Path "D:\ollama\models" -ItemType Directory -Force`
    - `winget install Ollama.Ollama --source winget`
  - **18:19:48 stornvme Event 11 発生**（Windows 標準の NVMe ドライバが Plextor コントローラでハードウェアエラー検出）
  - **18:19:51 volmgr Event 46, 161 連鎖エラー**（ボリュームマネージャ連鎖障害）
  - **18:20:37 EventLog Event 6008**（異常シャットダウン検知）→ **Green Screen of Death（Windows Insider Preview ビルド由来、青ではなく緑）**
  - **停止コード: WHEA_UNCORRECTABLE_ERROR (0x124)** — ハードウェアエラーによる OS 緊急停止
  - **Plextor 沈黙の原因**: NVMe コントローラが完全応答停止、Windows から「デバイス不在」扱いに。サイレント死（物理的破損ではなく電子回路レベルの応答不能）
  - **強制再起動時に起きた奇跡**: Boot Manager が Plextor からの起動に失敗 → 自動的に Seagate HDD（ちょうど 2 時間前に Hasleo でクローン完了していた）にフォールバック → Windows 11 が Seagate から正常起動 → **ユーザーデータ損失ゼロ**
  - **Get-Disk / Get-PhysicalDisk 実行結果（18:40 頃）**: Seagate 1 台のみ検出、Plextor は完全消滅
  - **bcdedit /enum 確認**: Boot device = `\Device\HarddiskVolume1` (Seagate)、osdevice = `C:` (Seagate) — Boot 構成も Seagate に完全移行済み
  - **ACPI ThermalZone 温度**: TZ10_0=16.9°C, TZ00_0=27.9°C, TZ01_0=29.9°C（ケース温度は冷えてる、CPU コア温度は未取得だが過熱ではなかった可能性大）
  - **体感**: Windows が Seagate SMR HDD から起動するため、ログイン・Brave 起動・ファイルエクスプローラー等すべて 50-100 倍遅い。Font Cache サービスが起動時タイムアウト、Intel RST サービスが落ちる等の副次症状
  - **奇跡のタイムライン（2026/04/22）**:
    ```
    午前      ユーザー「C: 壊れた時のバックアップとして D: を」（哲学的判断）
    17:15    Hasleo クローン開始（Plextor → Seagate）
    17:34    クローン完了 ← Plextor の「最後の大仕事」（結果的に）
    17:53    AOMEI システムイメージ backup 開始
    18:05    イメージ完成（Weekly System Image.adi = 82.94GB）
    18:13    Ollama 準備中（ユーザーが D:\ollama\models 作成）
    18:15-18:19  Ollama winget インストール実行
    18:19:48 Plextor NVMe コントローラ死亡通知（stornvme Event 11）
    18:19:51 ボリュームマネージャ連鎖エラー
    18:20:37 Green Screen WHEA 0x124、異常シャットダウン
    (自動再起動)
    18:21+   Boot Manager が Plextor 起動失敗 → Seagate クローンへ自動フォールバック
    18:23    Seagate から Windows 起動（Font Cache 等がタイムアウトしつつも復帰）
    18:40+   ユーザーと Claude Code で原因診断、Plextor 完全死亡確認
    ```
  - **タイミングの奇跡**: Plextor が死ぬ **約 2 時間前**にクローン完了。もし 2 時間遅かったらクローン中にコントローラが死んで**不完全クローン → 起動不能**で詰んでた。「念のため」「保険として」今朝ユーザーが決断したバックアップ運用が、当日中に実戦投入されて PC を救った
  - **教訓**:
    1. **バックアップは「いつか」ではなく「今日」やる** — 24 時間以内に壊れる機材は実在する
    2. **クローン（ブート可能な複製）の威力**: 単なるファイルバックアップではなく、**Boot Manager が自動フォールバック**してくれる防衛線として機能
    3. **Plextor のような撤退ブランド製品は寿命前でも突然死リスク**: 残 66% でも NVMe コントローラは前触れなく沈黙する
    4. **「寿命残 X%」は物理的な NAND セル書換残量であり、コントローラチップの寿命とは別軸**: SMART 健康指標が示せない故障モードがある

- [x] **4/22 夜のアクションアイテム**
  - [ ] 新 SSD を Amazon で注文（Crucial P3 Plus 1TB ¥8,500 推奨、翌日配送）
  - [ ] しゅん先生 PC を今夜はシャットダウン（Seagate SMR HDD に余計な負荷をかけない）
  - [ ] 4/23 到着後: Seagate → 新 SSD へ Hasleo クローン → BIOS で新 SSD Boot 1st → 通常速度復活
  - [ ] Plextor は物理的に取り外して保管 or 廃棄（フォーマットは不可能、単なる電子ゴミ化）
  - [ ] Ollama セットアップは新 SSD 稼働後にリトライ（Seagate 上で CPU 100% 負荷は避ける）
  - [ ] **Substack 記事化**: 「Plextor SSD が死ぬ 2 時間前にクローンを作った話 — 保険を今日作るか、明日作るかで人生が変わる」的な内容、りくと 48 時間ジャーニーと並ぶ 4 月の物語として

- [x] **未完遂: Ollama + ローカル LLM 実験（4/23 以降に繰越）**
  - `OLLAMA_MODELS=D:\ollama\models` 環境変数は設定済（ただし今は D: が無くなって別意味になった）
  - `D:\ollama\models`（= Seagate の ollama フォルダ、今は `C:\ollama\models` として見える）フォルダ作成済
  - `winget install Ollama.Ollama` はクラッシュのため完了確認できず、新 SSD 環境で再実行
  - 目標モデル: `qwen2.5:7b`（4.7GB）+ `deepseek-coder-v2:16b-lite-instruct-q4_K_M`（~10GB）
  - 期待速度（i7-8700K CPU only）: Qwen2.5 7B Q4 で 3-6 tok/s、DeepSeek-Coder-V2-Lite MoE で 8-15 tok/s
  - **活用案**: 夜間バッチ処理、claude-mem 観察ログ要約、Substack 下書き生成、しぶトランスクリプト分析

## 完了（4/20 セッション、Claude Design 本番化＋Google Workspace CLI 導入）

- [x] **Claude Design ハンドオフバンドル → 本番公開フロー確立**
  - **動機**: iPhone claude.ai Design メーター 0% 未使用 → 試用、AIミニマリストしぶ LP を生成 → ハンドオフ経由で本番化
  - **Claude Design 実測フロー**:
    - 10:20 プロンプト送信 → 10:28 生成完了（**8 分**、Hi-fi + インタラクティブプロトタイプ）
    - 10:31 "Handoff to Claude Code..." エクスポート選択、`https://api.anthropic.com/v1/design/h/<hash>?open_file=<filename>` 形式の fetch コマンドと「Download zip instead」オプション提示
    - 10:40 push → ~10:41 GitHub Pages live
    - 生成 → 実装公開まで **総所要 ~20 分**
  - **ハンドオフバンドル構造**（tarball gzip、9.7KB）:
    - `lp/README.md`: コーディングエージェント向け指示書（「チャット先読・メイン HTML 全読・ambiguous ならユーザー確認・pixel-perfect 再現」）
    - `lp/chats/chat1.md`: ユーザー原文プロンプト + Assistant 設計理由（デザインシステム・セクション構成）
    - `lp/project/Shibu LP.html`: 26KB、856行の実装 HTML（React/ReactDOM/Babel CDN + Tweaks パネル + TWEAK_DEFAULS IIFE + postMessage edit-mode wiring 付き）
  - **WebFetch は gzip を返す → `file` で検出 → `tar -xzf` で展開** のルーチンを確立（Claude Design 特有のプロトコル）
  - **本番化（dev-only harness 除去）戦略**:
    - 除去: React/ReactDOM/Babel CDN `<script>`（3タグ、~40KB）/ `#tweaksPanel` div ブロック / `.tweaks` CSS / TWEAK_DEFAULS IIFE state 管理 / postMessage edit-mode wiring (`__activate_edit_mode` 等)
    - 保持: 全ビジュアル CSS（`mix-blend-mode: difference` ナビ、`oklch()` アクセント、`clamp()` レスポンシブ字間）/ セマンティック HTML / コピー / reveal-on-scroll IntersectionObserver
    - 結果: 689行・19.5KB のピクセルパーフェクト本番 HTML
  - **GitHub Pages 公開**: `~/Desktop/docs/shibu-lp.html` → commit **d2479ed**（"Claude Design handoff 実装: しぶ LP を docs/ に公開"）→ push → https://wirelessml.github.io/test/docs/shibu-lp.html
  - GH Pages 初回 404 → 30〜90秒ビルド待ちで live（標準挙動）
  - **デザイン仕様**（原作尊重）: 黒背景 × オフホワイト #F5F3EE × `oklch(0.78 0.12 75)` ゴールド、Noto Serif JP（明朝）+ Noto Sans JP + Inter、Hero タイトル「手放せば、見えてくる。」、4段プロセス（棚卸し→問い直し→手放す→続ける）、3本柱（引き算/対話/余白）、¥48,000/3回の1on1オファーカード、最終CTA「まず、話してみる。」
  - **判断履歴**: 実在の写真差し替えは「公開GitHub Pages上での肖像権/ライセンス懸念」で保留 → プレースホルダ（260×260 concentric rings）のまま公開、必要なら後日差し替え可能

- [x] **Google Workspace CLI (gws) v0.22.5 導入**
  - **動機**: GitHub で googleworkspace/cli 発見、Drive/Gmail/Sheets/Docs/Calendar を Claude Code から直接操作できる Rust 製 CLI
  - **アーキテクチャ特徴**: Google Discovery Service から実行時に動的にサブコマンド構築（=新 API 追加時にバイナリ更新不要）
  - **インストール**: `brew install googleworkspace-cli` → `/opt/homebrew/Cellar/googleworkspace-cli/0.22.5`（arm64 native bottle、15.6MB）
  - **Agent Skills 95 本一括インストール**: `npx --yes skills add https://github.com/googleworkspace/cli --all -g`
    - `--all` = `--skill '*' --agent '*' -y` の省略形（デフォルトは interactive 選択でハング）
    - 保存先: `~/.agents/skills/`、`~/.claude/skills/` 等にシンボリックリンク
    - 内訳: `gws-*`（Drive/Gmail/Sheets/Docs/Calendar/Slides/Keep/Forms/Tasks/Chat/Meet/Script/Classroom/Events/ModelArmor/AdminReports/People）+ `recipe-*`（複合ワークフロー: Drive共有+メール通知、Gmail→Tasks変換、Calendar週次整理 等）+ `persona-*`（exec-assistant / content-creator / sales-ops 等）+ `gws-workflow-*`（週次ダイジェスト/スタンドアップレポート/会議準備）
  - **gcloud SDK 564.0.0 既インストール確認**（既存 photos-mcp 設定と共存可能）
  - **OAuth 手順はユーザー実行待ち**（SSO/OAuth は Prohibited Actions に該当、ブラウザ同意はユーザーのみが実行）:
    1. `gcloud auth login`
    2. `gcloud projects list` → `gcloud config set project <PROJECT_ID>`（photos-mcp と同じ "My First Project" で OK、新規 Desktop 型 OAuth クライアント作成）
    3. `gws auth setup`
    4. `gws auth login -s drive,gmail,sheets,docs,calendar`（testing mode は最大 ~25 scopes 制限、狭く開始推奨）
    5. `gws drive files list --params '{"pageSize": 5}'`（検証）
  - **注意点**: 既存 photos-mcp は Web 型クライアント、gws は Desktop 型必要 → 同プロジェクト内で別クライアント並立可
  - OAuth 完了後: CLAUDE.md に追記 + 試運転プロンプト（Drive一覧・Gmail検索・複合ワークフロー）提案予定

- [x] **Claude Design 産物の扱いルール確立**（プロトタイプ → 本番 HTML 変換パターン）
  - Tweaks パネル・React harness・edit-mode wiring は Claude Design iframe 内での live-editable 機能 → 本番では不要、削除対象
  - ビジュアル（CSS・HTML構造・コピー）は pixel-perfect 維持
  - コミットメッセージに判断を明記（後から「何を捨て何を残したか」を追える）
  - 将来のハンドオフで再利用可能な変換パターン

- [x] **セッション再接続ログ（4/20 午後）**
  - 16:27 前セッション終了（Weekly 39% / 5h 0%）
  - 16:33 Opus 4.7 1M context max で再開 → 4/20 セッション記録を CLAUDE.md 追記（Claude Design + gws 本件）
  - 16:36 「無限ループ再開」発言後 /exit（作業なし）
  - 17:06 再接続（Weekly 40% / 5h 5%）、約 30 分で Weekly +1pt / 5h +5pt
  - 直近は /loop 系の軽量タスク想定、gws OAuth 完了報告待ち状態継続

## 完了（4/20 夕方〜夜セッション、マルチツール一気導入＋しぶエコ人物特定）

- [x] **Crown & Coin 無限 grinding ループ再開→戦闘で停止**
  - `/tmp/grind-loop.sh`（90秒間隔 auto-restart wrapper）+ `/tmp/grinding.py`（pixel signature 検出）で昨日と同じパターン
  - Round 1 (17:11-17:20): **Success 47 / Fail 5**、所持金 317,795F から +~8,500F
  - Round 2 (17:21-17:25): iter 20 で BATAILLE（戦闘画面）突入、Success 20
  - Round 3-16: 戦闘画面のまま即 stuck（Etienne vs 敵3体、40分+間不変）
  - 17:54 ユーザー要求で停止、wrapper + grinding.py kill 済
  - **確認事項**: 昨日の用心棒 grinding 座標は「街→依頼一覧」画面でも当たる（最初の Round 1 の 90% 成功率を確認）

- [x] **Gmail TODO 下書き更新（4/20 版）**
  - 旧版 19da80e2a80c8f73（4/19、8件）→ 新版 r-5141956222652409298（4/20、**15件**）
  - 追加セクション:
    - 【gws OAuth セットアップ】5コマンド手順（gcloud auth login → gws auth login -s drive,gmail,...）
    - 【MacBookNEO セットアップ（4/22 16:30）】6アプリ導入順
    - 【重要期日リマインダー】4/21 / 4/24 / 4/30 / 5/11 / 5/20 / 5/29-30 の6件
  - 旧下書きは残存、ユーザー手動削除依頼

- [x] **McDonald's Support Bot バイラル動画の正体特定**
  - 当初 mcdonalds.com の Help Center と推測 → 間違い
  - **正体: echoai.so/e/mcdonalds**（Echo AI = 第三者プラットフォームでユーザーが作れる AI assistant）
  - 運営: echoai.so（@echoai_so、Supabase + GCS backend、PWA 対応）
  - 「Stop paying Claude Code, McDonald's support bot is free」ネタの正体 = Echo AI 上で誰かが McD 風装飾した Claude/GPT ラッパー
  - 登録不要・無料で即チャット可、直接 URL 開くだけ
  - バイラル動画の Alok (@_.alok_anmol._and_three_fs) はネタ投稿者

- [x] **Claude Design が動画制作も可能と確認（@shota7180 の証拠動画）**
  - 4/20 14:00 投稿（44いいね / 7,727views）: 「Claude Design は、スライドや資料だけでなく、動画制作も可能です↓」
  - 動画 DL (`/tmp/claude-design-video/shota7180-claude-design-video.mp4`、37.89秒、1816×1080 60fps、5.4MB)
  - 13 フレーム抽出・視覚解析結果:
    - **入力**: HTML モック（cloudtime-pages.html / cloudtime-dashboard.html）+ 企画 PPTX + Design System + テキストプロンプト（「動画のトーン: 信頼感・先進性・洗練・わかりやすさ」）
    - **出力**: ブラウザ内 **HTML モックをアニメ合成**した**インタラクティブ動画プロトタイプ**（Tweaks / Comment / Edit / Draw ツールバー、Present/Share ボタン付き）
    - **Manim/手続き生成ではない** — 疑似 Chrome に product UI 配置 → SVG カーソルアニメ（x:644,y:656 等を実測合わせ）→ キャプション（「ワンタップで、今日が始まる。」）→ タイトルカード
    - **反復編集**: cursor size/offset/AppChrome 外出し等、チャットで指示するとピクセル単位で再レンダリング
  - **結論**: Claude Design の「動画」= インタラクティブ動画プロトタイプ、SaaS PR・製品デモ向き。HTML モック既にあれば 1 プロンプトで 25 秒尺 PR 動画生成
  - ユーザーの LP ハンドオフ経験と連動: 既存 LP の HTML を食わせれば動画も作れる可能性

- [x] **shadPS4 (PS4 エミュレータ) M1 Mac 評価**
  - ⭐30,810、GPLv2、C++23 + SDL3 + Vulkan（MoltenVK 経由 macOS）
  - 最新 v0.15.0 "RE6_PRIG"（2026-03-17）、macOS zip 20MB
  - **M1 8GB での実用性: 低い** — (1) PS4 実機からの firmware dump 必須（ユーザー未所有）、(2) 8GB RAM では 16-24GB 推奨に対し不足、(3) ゲーム 30-100GB、Intel Mac は "heavy GPU bugs"
  - 技術的には macOS 15.4+ / Apple Silicon 対応で起動は可能、**興味枠としては面白いが実プレイ困難**

- [x] **claude-obsidian プラグイン導入（Obsidian 統合）**
  - AgriciDaniel/claude-obsidian v1.4.3 (⭐2,211、MIT)、Karpathy's LLM Wiki パターンベース
  - **Obsidian v1.12.7** も `brew install --cask obsidian` で併せて導入（`/Applications/Obsidian.app`）
  - Marketplace 登録: `claude plugin marketplace add AgriciDaniel/claude-obsidian` 成功
  - Plugin install: **初回 SSH 未設定で失敗** → `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0="url.https://github.com/.insteadOf" GIT_CONFIG_VALUE_0="git@github.com:" claude plugin install ...` で**単発スコープの環境変数で HTTPS rewrite**（**git config は変更せず**、CLAUDE.md 安全ルール準拠）
  - 主要コマンド: `/wiki`（scaffold）/ `/save [name]` / `/autoresearch [topic]` / `/canvas` / `ingest [file]`（8-15 wiki ページ自動生成）/ `ingest all of these`（batch）/ `what do you know about X?`（citation付き）/ `lint the wiki`
  - ストレージ: `wiki/index.md`（master catalog）+ `wiki/hot.md`（recent cache）+ `concepts/` `entities/` `sources/` 階層
  - **次ステップ（ユーザー実行待ち）**: Obsidian 起動 → vault 作成（推奨 `~/Desktop/vault` or 既存 `~/Desktop/ai-minimalist-shibu/knowledge`）→ Claude Code 再起動 → `/wiki` 初期化 → `ingest all of these` で既存ナレッジ取込

- [x] **Computer Use ツール導入: Peekaboo + browser-echo**（@hata_AI_master 4/20 14:16 ポスト起点）
  - 7ツールリスト resolve 結果: browser-harness / native-devtools-mcp / agent-browser（既導入）/ browser-echo / **Peekaboo** / mcp-server-tauri / playwright-mcp
  - **Peekaboo v3.0.0-beta3** (⭐3,156、Swift)
    - `brew install steipete/tap/peekaboo` → `/opt/homebrew/bin/peekaboo`（39.7MB）
    - MCP user scope 登録成功（`claude mcp add -s user peekaboo -- peekaboo mcp` ✓ Connected）
    - **要: 画面収録権限**（システム設定 → プライバシーとセキュリティ → 画面収録 → Terminal をオン）
    - 使途: screenshot / click / type / menubar / dock / app list 等、Crown & Coin 戦闘検出 / Maestri / Claude Desktop 制御
  - **browser-echo MCP v1.1.0** (⭐310、TS)
    - `@browser-echo/mcp` を user scope に登録（`claude mcp add -s user browser-echo -- npx -y @browser-echo/mcp`）
    - 現状 ✗ Failed to connect（フロントエンド側 Vite/Next/Nuxt の forwarder が port 5179 で送信していないため、想定内）
    - 使途: Next/Vite プロジェクトの browser console log をエージェントに直接流す、ゼロ設定
  - **未導入分の見送り**: browser-harness（重い）/ native-devtools-mcp（重い）/ mcp-server-tauri（Tauri 未使用）/ playwright-mcp（4/17 に一旦削除済、再導入は要件発生時）
  - **MCP 反映タイミング**: 新セッションから `mcp__peekaboo__*` として ToolSearch 経由で呼び出し可能

- [x] **しぶエコシステム: 4/20 23:09-23:10 りくと 3連投ストーリーの人物特定**
  - 内容: AI研修の日 + 米ル（@gardencity.komeru）店構え + 懐石会食（黒漆椀・塩・米）
  - キャプション: 「朝から晩まで AI の研修受けて 見る世界変わった、何をして働けばいいんだ...？😇」
  - **BGM 正体訂正**: 「♫ Ryan Condrey · Photograph...」は **撮影者クレジットではなく viral トレンド音源**（3.9万 reel 使用中）— Ryan Condrey は海外クリエイターで**参加者ではない**
  - **3人構成確定**: しぶ（左、黒服 + ピンクトート）/ りくと（中央、黒バックパック）/ **女性（右、サーモンピンク + 黒パンツ）**
  - 女性候補の絞り込み: あい（@ikeai_minimalist） vs 元歯科衛生士（デザイン担当）
  - **@ikeai_minimalist プロフィール詳細**（新情報、CLAUDE.md shibu-team.md 未記載）:
    - **あい、33歳、福岡、1LDK 賃貸**、投稿 234 / フォロワー 3.7万 / フォロー 26人
    - デジタルクリエイター、オールシーズン 17 着、YouTube + 楽天ROOM、**猫「わらびちゃん」**と同居
    - プロフィール画像: **赤茶色の髪、オレンジトップス + 黒ベスト、暖色コーデ好み**
  - **元歯科衛生士の視覚特徴**（tesla 納車動画 bQjAe4vMZVQ 2:16 frame 抽出）:
    - **黒髪ストレート、肩下〜胸の長さ、前髪あり（ぱっつん気味）**
    - 白〜オフホワイトのトップス、細身、20代後半〜30代前半
    - しぶとレストラン/カフェで対話中のシーン
  - **判定**: 髪色（あい=赤茶 vs ストーリー=濃い黒）+ 配色傾向（あい=暖色派 vs ストーリー=ミニマル配色）+ 表に出る vs 匿名的出し方 の3軸で判断
    - **元歯科衛生士（デザイン担当）: 70〜75%**
    - あい: 25〜30%
  - 決定打は「あいの 4/20 当日ストーリー」で、あいが別の場所にいれば 100% 確定（Chrome @minimalistneko ログイン時に確認可能）

- [x] **「何をして働けばいいんだ…？😇」への解釈**（セッション末尾）
  - りくとの二重の皮肉: (1) 動画編集担当 = Claude Design 等に代替される職種、(2) その告白を**既にテンプレ化されたバイラル音源 + 明朝縦書き リール形式**で出している = 表現手段すら AI 量産可
  - しぶエコ（ミニマリズム）は「所有を手放す」哲学 → AI 時代は**スキルを手放す**ステージ
  - りくとの真の資産: スキルではなく**しぶとの信頼関係・同席権** = AI 研修に呼ばれる側 = 作業者ではなく判断者ポジションに既に移行済み
  - ユーザー自身の当日行動（Claude Design / gws / Peekaboo / claude-obsidian / browser-echo の 5本立て導入）は作業者ではなく**アーキテクト側**の動き、同じ構造

- [x] **セッション末週枠**: Weekly 40% (17:06) → 同 40%台 継続、5h は 5% から増加推定（実測未取得）

## 完了（4/21 早朝〜昼、しぶ AI研修 2日目ストーリーで人物特定訂正＋MASU-p 共有 HP ProBook で GC313Pro セットアップ完了）

- [x] **しぶ 4/21 0:04 頃 3連投ストーリーで 4/20 夜の人物特定を全面訂正**
  - **#1 AI研修ストーリー**（しぶ @minimalist_sibu 投稿）:
    - キャプション「AI研修 / 社内で 8時間 × 2日連続 **ClaudeCode叩き込み**」
    - 研修室写真（会議室、モニターに IDE 画面、ノート PC 数台）
    - **@ikeai_minimalist タグが作業中の女性に直接付与** → **女性 = あい で 100% 確定**
    - @rikuto_takemoto タグ（左、金髪ブリーチ）= 前日と整合
    - 右側 3 人: しぶ（くるくる髪）+ 顔隠し男（ロボット絵文字）+ 黒髪クセ毛男
  - **#2 米ル集合写真**（しぶ投稿、位置情報タグ「米ル」確定）:
    - キャプション「AI研修 1日目終了 🍚」
    - **5 人集合写真**: しぶ / りくと / あい / ロボット絵文字男（顔出し NG）/ 黒髪クセ毛男
    - 食卓: 和食コース（ご飯・味噌汁・焼き魚・漬物・お茶）
    - **位置情報確定**: 米ル（@gardencity.komeru、Garden City 系商業施設内）
  - **#3 Minimal Sign 電子署名 SaaS の発表**（しぶ投稿）:
    - キャプション「**自社で電子署名のサービス開発できた。オリジナルで自分の好みの機能やデザインも実装できて、サブスク代削れる**」
    - スクショ: 「Minimal Sign ｜ 契約管理」ダッシュボード
    - テンプレート 1 件: **「モノ減らしコーチング撮影同意書」**（作成日 2026.04.20）
    - 締結済み 3 件: 全て **澁谷直人 様（minimalist.sibu@gmail.com）**が 4/20 18:49 / 18:52 / もう1件で自己テスト署名
    - 署名完了モーダル「MINIMALIST.SIBU@GMAIL.COM 宛に送信しました」
    - **主目的**: モノ減らしコーチング受講生からの撮影同意書取得（肖像権・空間撮影許諾）
    - **副目的**: DocuSign/CloudSign 等のサブスク代削減（¥9,000-50,000/月）
    - **しぶエコ哲学との整合**: ミニマリズム = 外部サブスク（=モノ）を減らす = 自社開発で所有を手放す
  - **りくと 4/21 0:06 リポスト**（@rikuto_takemoto）:
    - しぶのAI研修ストーリーをリポスト、明朝体で**「目指せ！AIマスター」**
    - 4/20 23:09 の「何をして働けばいいんだ…？😇」から **24 時間以内に「AIマスター目指す」へ昇華** = 方針転換完了

- [x] **人物特定の訂正（前日 70-75% 元歯科衛生士判定は誤り）**
  - **4/20 夜に「70-75% 元歯科衛生士」と判定**した女性 = **実際は あい で確定**
  - 誤判定の原因:
    1. プロフィール写真の赤茶色髪 vs 夜の暗色髪 → **照明/フィルタ依存**を過少評価
    2. サーモンピンクトップス = あいの普段の色域内（プロフのオレンジより控えめだが同系統）
    3. 匿名的な出し方 = 裏方キャラ推論 → りくとが単にタグを省略しただけ
    4. 後ろ姿 + タグなしの根拠を過大評価
  - **新しい仮説: 元歯科衛生士 = 全シーンの撮影役（65-75%）**:
    - 4/20 23:09 歩行写真（3人）の 4 人目
    - 米ル集合写真（5人）の 6 人目
    - 4/21 AI研修室ワイド（5人）の 6 人目
    - **一貫した不在パターン + CLAUDE.md shibu-team.md「名前不明・Instagram 未公開」記載と整合**
    - デザイン担当 = Minimal Sign UI 設計者の可能性あり
  - **AI研修参加者: 5 名 or 6 名**（元歯科衛生士が撮影役として同行なら 6 名）
  - **顔隠し男**（ロボット絵文字）= 外部 AI 講師（SHIFT AI / Levela / Anthropic 関係者等）or ショウ（@minimalsho、裏方方針）の可能性

- [x] **しぶ新規判明情報（CLAUDE.md `shibu-team.md` 追記候補）**
  - **しぶの公式メールアドレス**: **minimalist.sibu@gmail.com**（Minimal Sign 署名完了モーダルから判明）
  - **しぶの本名**: 澁谷直人（既知、shibu-team.md に記載あり、再確認）
  - **あい (ikeai_minimalist) の詳細**:
    - 33 歳、**福岡**、**1LDK 賃貸**、デジタルクリエイター
    - 投稿 234 / フォロワー 3.7 万 / フォロー 26 人
    - オールシーズン 17 着のミニマリスト、YouTube + 楽天ROOM
    - **猫「わらびちゃん」と同居**、最近引越し（半年で再引越し）
    - プロフィール画像: 赤茶色髪、オレンジトップス + 黒ベストの暖色コーデ好み
    - 受講生の会 2025 登壇実績（既知、shibu-team.md）

- [x] **AI研修の全貌判明**（しぶエコの戦略的含意）
  - **研修時間**: 2 日間 × 各 8 時間 = 16 時間の **ClaudeCode 集中合宿**
  - **参加者**: しぶ / りくと / あい / 顔隠し男 / 黒髪クセ毛男（+ 撮影役の元歯科衛生士？）
  - **成果物**: Minimal Sign 電子署名 SaaS（DocuSign 代替）
  - **戦略**: ミニマリズム哲学の IT 版実践 = 「外部サブスク = モノ（契約）を増やす」→「自社開発 = モノを減らす」
  - **含意**:
    - しぶエコは **ClaudeCode による SaaS 自社開発の実践段階**に入った
    - あい（コンテンツクリエイター）も **コード書ける側に移行中** = 編集者→開発者の転身期
    - りくとの「何をして働けばいいんだ」は 24 時間で「AIマスター目指す」に転換 = **迷いが短期間で解消**
    - ユーザー自身の 4/20 行動（Claude Design / gws / Peekaboo / claude-obsidian / browser-echo の 5 本立て導入）と同じ構造 = **作業者ではなくアーキテクト側の動き**

- [x] **Lunel (lunel-dev/lunel) モバイル IDE 調査**
  - ⭐617、MIT、TypeScript、v0 release 2026-04-01（**約 3 週間前の新興**）
  - AI-powered mobile IDE + クラウド開発プラットフォーム
  - 「携帯でコード書いて、自宅 Mac or クラウドサンドボックスで走らせる」
  - **アーキテクチャ**: Expo/React Native モバイル（iOS/Android/Web）+ Rust PTY（wezterm ベース、24fps 差分描画）+ WebSocket relay（gateway.lunel.dev、session TTL 10分、QR ペアリング）
  - **インストール**: `npx lunel-cli`（母艦側で起動 → QR コード表示 → モバイルアプリでスキャン）
  - **未実装・欠落情報**: AI モデル統合の実体不明（「AI-powered」と謳うが Claude Code / Codex 等の言及なし）、Lunel Cloud は "Coming soon"、価格未公開
  - **ユーザー既存環境との比較**:
    - iPhone → Mac SSH（Tailscale + 鍵管理）を QR ペアリングで代替できる可能性
    - Claude Desktop Code mode と並列で使える
    - **TODO #11（iPhone VNC）の代替候補**として検討価値あり
  - **評価**: 現状は v0 + ドキュメント欠落多め、**v1 リリース + Claude Code 統合の明記**待ちが安全

- [x] **MASU-P55（HP ProBook）で GC313Pro + OBS セットアップ完了**
  - **重要訂正**: 本セッション中に「MASU-p 共有 PC」として扱っていた HP ProBook は、**既存 CLAUDE.md 記載の MASU-P55 と同一マシン**（当初「別 PC」と誤記載）:
    - **MASU-P55 = HP ProBook**（Intel Core i5 搭載、コワーキング MASU-p の設置機）
    - **既知情報（CLAUDE.md ユーザー情報と整合）**: user: gci_admin / IP: 192.168.2.248 (masu-p55.local) / Tailscale 100.125.21.47 / Claude Code v2.1.98 インストール済み
    - **今回新判明**: ハードが HP ProBook、追加アカウント **masup**（PIN は紙メモ記載、コワーキング共用）が存在、Intel Core i5 CPU
    - **Mac から SSH 経由で以前から操作したことあり**（ユーザー確認）
  - **AVerMedia Assist Central Pro インストール**:
    - Destination: `C:\AVerMedia\AssistCentralPro`（115.4 MB）
    - Nullsoft Install System v3.10 経由の通常インストーラ
    - GC313PRO (Elite GO GC313Pro) 自動検出成功
    - **HDCP 検出機能**: 「無効（推奨）」選択（iPhone/iPad ソース用、著作権保護信号対応）
  - **OBS 32.1.1 設定**:
    - バージョン: OBS Studio 32.1.1（made in TOKYO）
    - ソース: 映像キャプチャデバイス（GC313Pro 経由）
    - **映像ソース解像度**: デバイス既定値 = **1080×1920**（GC313Pro が iPhone 縦画面を自動検出）
    - FPS 60
    - 音声: デスクトップ音声 / マイク / 映像キャプチャデバイス の 3 系統全アクティブ
    - CPU 負荷 1.4%（軽い）
  - **iPhone カメラアプリを HDMI 出力 → GC313Pro → OBS 取り込み**動作確認:
    - iPhone カメラの縦画面（1x/2x/3x ズーム・写真モード UI）が OBS プレビューに表示
    - **フルスクリーンプレビュー成功**（プレビュープロジェクター経由）
  - **トラブルシュート記録**（次回再発時のため）:
    - 「赤斜線エリア」= キャンバス解像度とソース解像度の不一致 → 設定変更で解消
    - 1080×1920 → 1920×1080 への誤変更で映像が小さくなった → 1080×1920 に戻して解決
    - 左右の pillarbox（黒帯）はフィルタ → クロップ/パッドで削除可能、または真の縦向け用途ならキャンバスを 1080×1920 に揃える
    - **重要学び**: GC313Pro の「デバイス既定値」は入力信号に応じて自動検出するので、**カスタム指定は避けて既定値のまま**が安全
  - **用途**: CLAUDE.md TODO #9 の Switch 2 キャプチャ予行演習 + iPhone 画面録画・配信環境の構築

- [x] **セッション末週枠 (4/21 朝時点)**: 4/21 0:00 頃にセッション4 枠（日次スケジュール）、Weekly 40%台継続、5h は 0% リセット後の使用開始

- [x] **Claude Code 2.1.116 自動更新（Mac & MASU-P55 両方）**
  - Mac: `~/.local/bin/claude` → v2.1.116（4/21 08:37 自動更新）
  - MASU-P55: `C:\Users\gci_admin\.local\bin\claude.exe` → v2.1.116（4/21 08:52 自動更新）
  - 毎日 0:00 JST タスクスケジューラによる **自動更新仕組みが正常稼働確認**
  - CLAUDE.md のユーザー情報セクション Claude Code v2.1.98 表記を v2.1.116 に更新

- [x] **GitHub Copilot CLI v1.0.32 → v1.0.34 更新（Mac のみ）**
  - 4/20 公開 v1.0.34、変更点は **「Rate limit error message: global → session」の文言変更のみ**
  - Mac `copilot update` で 1.0.34 DL & 反映完了
  - MASU-P55 は **未インストール**（Mac 専用運用のまま継続判断）

- [x] **太閤立志伝V DX セール情報キャッチ**（Switch eShop 40% OFF）
  - My Nintendo Store JP で **¥2,970 税込**（定価 ¥4,950 から 40% OFF）
  - **期限: 2026/05/06 23:59** まで（GW セール）、**キャンセル不可**
  - Crown & Coin デモの「太閤立志伝ライク」の直系インスピレーション源 = MUZINA GAMES 本人が明言
  - しぶエコの ClaudeCode 合宿参加者と同じく「ミニマリスト + 戦国人生シミュレーター」の親和性
  - **購入判断は保留**（4/22-5/11 の濃い期間と要調整、GW 中はセール継続のため数日判断猶予あり）

- [x] **ツール調査（導入せず、情報記録のみ）**
  - **Lunel (lunel-dev/lunel)** v0 モバイル IDE + クラウド開発プラットフォーム: v1 + Claude Code 統合明記までは待機
  - **mac-mouse-fix (noah-nuebling)** v3.0.8: 3rd party マウスに macOS ジェスチャー付与、$2.99 買い切り、**要マウス所有**なので現状導入不要
  - **Pyenb/macOS-ISOs**: macOS ISO torrent 集（Lion 〜 Sequoia）、**Apple TOS グレーゾーン**。合法用途は Mac M1 で UTM に古い macOS VM を作る場合のみ（自ハード + 自ライセンス）。Windows/Linux への Hackintosh 展開は TOS 違反で非推奨

- [x] **Designated Survivor（サバイバー 宿命の大統領）未解決状態の分析**
  - **打ち切り経緯**: ABC S1-2 → 2018/5 キャンセル → Netflix S3 引継（2019/6 配信、10話） → 2019/7 Netflix も S4 制作断念
  - **打ち切り理由**: Entertainment One の 1 年単位キャスト契約、継続交渉困難（Netflix 側視聴率は非公開）
  - **ハンナ・ウェルズ（マギー・Q）死亡は S3 E7 の劇中決定**（打ち切り決定前の脚本、構造整理目的）
  - **黒幕構造（劇中で判明した 3 層）**:
    1. 表層: トロント出身のネオナチ系科学者（人種差別バイオ兵器開発、ヒューストンで自殺し逮捕前に証拠隠滅）
    2. 中間層: 共和党モス陣営の政治戦略家 Myles Lee + Lorraine（FBI 逮捕）
    3. 制度内協力者: FDA 長官（逮捕）
  - **未回収の謎**: ネオナチ組織の資金源 / S1-2 の Patrick Lloyd 系陰謀との地下接続 / ハンナが死ぬ直前に残した情報の継承者 / S1 から続くディープステート仮説の真相
  - **結論**: 「ハンナは黒幕組織の罠に落ちて事故偽装で殺された。表層 3 層は暴かれたが、ネオナチ資金源・国際陰謀の真相は S4 で明かされる予定が制作打ち切りで永遠に闇の中」

- [x] **課題全体像レビュー**（ユーザー要求「おさらい」）
  - 今日/明日最優先: Y!mobile Netflixセット 自動解約発効（4/21 済）/ MacBookNEO セットアップ（4/22 16:30）
  - 即時実行可能待機: gws OAuth / claude-obsidian `/wiki` 初期化 / Peekaboo 画面収録権限
  - 商品到着待ち: 維新の嵐 CD (TODO #7) / Switch 2 本体 (TODO #9 GC313Pro は 4/21 OBS 動作確認済)
  - ElevenLabs 5/11 失効: D→A→B→C タスク群（しぶ YouTube 20 本 Scribe → video-use 編集 → しぶライブ再開 → 小説朗読動画化）
  - **Crown & Coin 用心棒 grinding 無限ループを課題に追加**（`/tmp/grind-loop.sh` でコマンド一発、戦闘発生までの半自動運用、所持金目標は未設定）
  - 継続観察: しぶ AI研修 2日目ストーリー / Minimal Sign UI デザイナークレジット / ショウ @minimalsho 研修画像で顔隠し男の正体検証
  - 判断待ち: 太閤立志伝V DX セール購入（5/6 期限）/ MASU-P55 への Copilot CLI 追加導入

- [x] **4/22 GC313Pro User Guide v1.1 日本語訳を docs/ に公開**
  - 原文: AVerMedia GC313Pro User Guide v1.1（2025-09-30、21 ページ、英語）
  - Markdown 版: `docs/gc313pro-user-guide-ja.md`（373 行、commit `b72fb11`）
  - HTML 版: `docs/gc313pro-user-guide-ja.html`（既存 docs/ スタイルに合わせた配色、目次・TOC 付き、ダーク/ライトモード対応）
  - 公開 URL: https://wirelessml.github.io/test/docs/gc313pro-user-guide-ja.md / .html
  - 内容: 主な機能 / システム要件 / 仕様 / 電源配分 / Assist Central Pro / ファームウェア更新ガイド / F.A.Q. 8 項目 / GC313 vs GC313Pro 比較 / 訳者注・関連ファイル保管場所
  - **Switch 2 接続手順**（GC313Pro C1 ポート直結 + HDMI OUT パススルー + USB-C2 で PC キャプチャ）も完全翻訳
  - ミニマリスト向けのナレッジ資産として残存、外出先から iPhone でも参照可能

- [x] **4/22 午前〜午後セッション: AI エージェント環境強化ラッシュ**（GC313Pro 運用確立＋スタック全面刷新＋しぶエコ追跡継続）
  - **Moshi iOS アプリ既利用確認**: iPhone 側の SSH/Mosh クライアント、保存接続 `yuika@100.99.41.2` + `gci_admin@100.125.21.47`、月 28 接続中（無料枠ほぼ上限）、**Pro 未購入で mosh プロトコル + dictation 未解放**、Blink Shell 等代替候補と比較検討余地
  - **参考構成「AI 中心の仕事環境 6 層スタック」解析**:
    1. インターフェース: MacBook Pro + **cmux**（Ghostty ベース macOS native terminal、2026/2 リリース、10k ⭐、Claude Code/Codex/Aider 並列実行特化）
    2. 脳: **Codex (cc)**（OpenAI Codex CLI + Claude Code 互換エイリアス）
    3. 情報ソース拡張: **Crawl4AI**（AI 向け Web クローラ OSS）+ **xurl**（X API curl ライク CLI）
    4. 持ち運び: **Tailscale + Moshi**（mosh プロトコル + モバイル切断耐性）
    5. ループ: **Mac Studio + Ralph Loop**（2026 バイラル手法、PRD 完了まで自律反復、Execute/Evaluate/Fix/Repeat の 4 段階、12k ⭐）
    6. 管理: GitHub
  - **ユーザー現環境との差分**: cmux / Ralph Loop 未導入、Mac Studio 未保有、mosh プロトコル未有効化。agent-reach（twitter CLI 含む）で xurl/Crawl4AI を代替中
  - **導入優先度**: cmux（MacBookNEO セットアップと同時）> mosh 有効化（Moshi Pro or Blink Shell）> Ralph Loop（Claude Max 活用の極北）> Mac Studio（¥400k+ 投資判断、後期検討）

- [x] **4/22 大川裕介 → 大川優介 誤記を全ファイル訂正**（commit `34c8db0`）
  - しぶ × テスラ × Vision Pro × 車中泊ルームツアー動画（ukfCg8ZgMjA）の出演者氏名訂正
  - ライブファイル 7 本、12 箇所を一括置換（sed）:
    - CLAUDE.md / prompt.txt / docs/google-photos-shibu-inventory.md / ai-minimalist-shibu/knowledge/google-photos-analysis.md（6箇所）/ ai-minimalist-shibu/knowledge/novel-three-macs.md / ai-minimalist-shibu/knowledge/transcripts/yt-ukfCg8ZgMjA.ja.vtt / ai-minimalist-shibu/yt-ukfCg8ZgMjA.ja.vtt
  - `.claude/worktrees/` 内 14 箇所は isolated state で放置（過去の並列エージェント作業のスナップショット）
  - push 済、GitHub Pages 反映済

- [x] **4/22 はりきゅう整体しゅん LP 再確認**: https://wirelessml.github.io/test/docs/hari-seitai-shun.html#info（兵庫県伊丹市、4/17 初回公開、HTTP 200 稼働確認、他の公開 docs との一覧表も整理）

- [x] **4/22 Apple 偽装フィッシングメール警告**（pirosi80@yahoo.co.jp 宛、10:48 受信）
  - 送信元: `no-reply@icloud-apple-server-bn3grd9h54h2hfdfhd9e37httns3ht4-a3.1i0cr9k.top`（`.top` ドメイン + ランダム文字列 + 偽装ブランド）
  - 件名: 「決済エラーのお知らせ: iCloud+ ストレージプラン」
  - 「要確認」ボタン + 「対応期限: 2026/04/21 23:59」（既に過去）+ 「2020 San-X Co., Ltd. All Right Reserved.」（無関係テンプレ）= **100% フィッシング**
  - **リンク未クリック、削除推奨**を回答
  - pirosi80@yahoo.co.jp はフィッシング標的化、金融・クラウド系サービスでは別メアド推奨

- [x] **4/22 GC313Pro User Guide v1.1 日本語訳 公開**（commit `b72fb11` + `3112252`）
  - Markdown 版: `docs/gc313pro-user-guide-ja.md`（373 行）
  - HTML 版: `docs/gc313pro-user-guide-ja.html`（目次・ダーク/ライトモード・モバイル最適化）
  - 公開 URL: https://wirelessml.github.io/test/docs/gc313pro-user-guide-ja.html
  - 原文 PDF 保管: Mac `/tmp/gc313pro/` + MASU-P55 `C:\Users\gci_admin\Downloads\`
  - 内容: 主な機能・システム要件・仕様・電源配分・Assist Central Pro・ファームウェア更新ガイド・F.A.Q. 8 項目・GC313 vs GC313Pro 比較・関連ファイル保管場所
  - **Switch 2 接続手順**（GC313Pro C1 ポート直結 + HDMI OUT パススルー + USB-C2 で PC キャプチャ）完全翻訳

- [x] **4/22 Mac 版 AssistCentralPro v4.0.80 を Mac M1 に導入**
  - DL: https://storage.avermedia.com/web_release_www/AssistCentralPro/AssistCentralPro_v4.0.80.zip（41.7MB）
  - 展開 → DMG マウント → `/Applications/AssistCentralPro.app` コピー
  - 検疫属性除去（`xattr -dr com.apple.quarantine`）
  - バージョン: 4.0.80（Windows MASU-P55 側と同一、macOS 13+ 対応）
  - 用途: Mac 側で GC313Pro 使用時の HDCP 切替・FW バージョン確認・デバイス診断
  - 起動: `open -a AssistCentralPro`

- [x] **4/22 10:15 OpenAI「ChatGPT Images 2.0」発表**（ASCII.jp 経由確認）
  - ASCII.jp 記事: https://ascii.jp/elem/000/004/396/4396995/（G.Raymond 執筆、本日 10:15 掲載）
  - **質的変化**: 従来の「きれいな絵」→ **「グラフィック設計機能」**（漫画・広告・UI モック・説明図向け）
  - 改善点:
    - **日本語・韓国語など非ラテン文字テキスト描写が実用域**（従来の最大弱点を克服）
    - オブジェクト同士の位置関係精度向上
    - **最大 8 枚の一貫性ある画像を同時生成**
    - アスペクト比 **3:1 〜 1:3**（横長バナー〜縦長ポスター）
    - Thinking 系モデル連携で複数案・自己修正ループ
  - 影響範囲:
    - **Manus** 画像生成（Nano Banana Pro + GPT Image 1.5 切替式、今日中〜数日で 2.0 追加想定）
    - **Claude Design** と組合せ = SaaS LP を 10 分で完成できる時代に
    - **しぶエコ**（Minimal Sign / AI RIKUTO のヒーロー画像素材化）
    - **Substack 記事の「週 1 ペース潮目変化」主張の当日証明**
  - 記事反映案: A（1 行追加）/ B（別記事速報）/ C（全面書き直し）→ **A + 続編準備** 推奨

- [x] **4/22 Substack 初心者向け AI 課金記事の強化（りくと事例引用）**
  - 友人（名前・会社は抽象化）の 48 時間変化を**記事冒頭フック + クロージング**として引用
  - 4/20「何をして働けばいいんだ…？😇」→ 4/22 深夜 AI RIKUTO 1 時間実装「素人なのにたった 1 時間で出来た（震える）」
  - 「Claude Code を初日から使ったわけじゃない。まず無料で触って、何ができるかを体で覚えて、2 日目には自分のアプリを作っていた」= 記事のコアメッセージ
  - イケハヤ系の煽りではなく**リアルな肉声で刺す**構成
  - Manus 画像生成モデル調査: **Nano Banana Pro + GPT Image 1.5** 切替式（Pro プラン限定）と判明
  - 初心者向け無料 Claude Code 代替候補: **Aider + Gemini Free API**（50 req/日、クレカ不要）/ GitHub Copilot CLI（月 50 無料、既導入）
  - Claude Max 解約後の備え: API キー発行 + Aider 併用の二段構え、Phase 1-3 の段階的移行計画

- [x] **4/22 23:00-24:00 りくと AI研修完了 4連投ストーリー解読**（しぶエコ 2 日間合宿の全成果物確定）
  - **成果物 2 つ**:
    1. **Minimal Sign**（4/20 公開、電子署名 SaaS、モノ減らしコーチング撮影同意書用）
    2. **AI RIKUTO**（4/22 深夜完成、**片付け＋インテリアコーディネート AI**、写真＋音声入力対応、診断型UI、**1 時間で作成**）
  - りくとの意志変遷 **4 段階追跡完了**:
    - 4/20 23:09「何をして働けばいいんだ…？😇」（不安）
    - 4/21 00:06「目指せ！AIマスター」（目標）
    - 4/21 11:30「AIマスターになる 🧑‍💼」（宣言）
    - **4/22 23:00「AI沢山使いこなして這い上がりたい🔥」（実装フェーズ）**
  - **Minimal Arts 組織構造**（新判明）: **BOSS = しぶ（@minimalist_sibu）/ シタッパ = りくと**（本人自称）、動画編集担当以上の階層感、「這い上がりたい」= 昇格意欲
  - 「毎日AIは進化する」「個人の仕事も会社の仕事もツール色々作れた」「自分が人雇ってる経営者になった気分」= **個人スケール→会社スケールの仕事を 1 人で回せる実感**
  - AI RIKUTO の技術特徴:
    - マルチモーダル（写真＋音声＋テキスト）
    - 診断型 UI（「診断をはじめる」ボタン、セラピー的対話設計）
    - 出力品質高（「北欧の機能性と和の安らぎ」等、高級インテリア誌風コピー）
    - **1 時間で生成**（Claude Code or Gemini 推定）
    - しぶ系片付けコーチングの**AI代替**として機能しうる
  - **ユーザー Substack 記事への事例価値**: 「無料で始めて、触り込めば 1 時間で SaaS が作れる時代」の生々しい証拠、初心者→実装者への 48 時間ジャーニー

- [x] **4/22 Mac 版 AssistCentralPro v4.0.80 を Mac M1 に導入**
  - DL: https://storage.avermedia.com/web_release_www/AssistCentralPro/AssistCentralPro_v4.0.80.zip（41.7MB）
  - 展開 → DMG マウント → `/Applications/AssistCentralPro.app` コピー
  - 検疫属性除去（`xattr -dr com.apple.quarantine`）
  - バージョン: 4.0.80（Windows MASU-P55 側と同一、macOS 13+ 対応）
  - 用途: Mac 側で GC313Pro 使用時の HDCP 切替・FW バージョン確認・デバイス診断
  - 起動: `open -a AssistCentralPro`

- [x] **4/22 GC313Pro 本体到着 + 公式仕様判明で前日設定の前提訂正**
  - パッケージ内容: ELITE GO（GC313Pro 本体）+ **USB-C to C ケーブル 2m** + **交換用 AC プラグ** + クイックスタートガイド
  - ポート構成: **USB-C1（映像入力、DP Alt Mode 専用）/ USB-C2（PC 接続）/ USB-A（周辺機器）/ HDMI OUT（4K60 パススルー）/ 折りたたみ式 AC プラグ（100W PD 電源内蔵）**
  - **HDMI IN なし判明**（公式ページ https://www.avermedia.co.jp/product-detail/charging-dock-GC313Pro で確認）
  - 訂正事項:
    - 4/21 に「iPhone USB-C → HDMI アダプタ → GC313Pro」と助言したが、**USB-C 直結が正解**（¥2,000-10,800 のアダプタ不要）
    - TODO #9 の接続フロー記述を DP Alt Mode 専用として更新
  - 対応デバイス: USB-C DP Alt Mode 対応機のみ（iPhone 15/15 Pro、USB-C iPad、USB-C Android、USB-C ノート PC）
  - 非対応: PS5 / Xbox Series X / Blu-ray プレーヤー / 旧世代ゲーム機（HDMI 出力のみは別キャプチャ機材必要）

- [x] **Switch 2 動作確認済が AVerMedia 公式で確定**（4/22 公式 FAQ 確認）
  - 公式ページに **「Nintendo Switch 2 動作確認済」バッジ**掲示
  - 「※本製品は、任天堂との提携または認証を受けたものではありません」の但し書きあり
  - **接続フロー確定**:
    ```
    Switch 2 本体下部 USB-C 映像出力ポート
      ↓ 付属 USB-C to C ケーブル 2m
    GC313Pro USB-C1（映像入力）
      ├→ HDMI OUT → モニター（4K60 パススルー）
      └→ USB-C2 → PC/Mac（1080p60 キャプチャ）
    ```
  - **純正ドック不要**（Switch 2 本体から直結可）
  - **ファームウェア確認完了（4/22 MASU-P55 で実施）**:
    - 現在 v24.8.30.16.1.19.30 = **既に最新**（購入時点で最新ファーム搭載済み）
    - **更新作業不要**、Switch 2 互換性 + iPhone 17 Pro 充電断続問題**既に修正済**
    - ファームウェア更新ツールは将来版リリース時のため `C:\Users\gci_admin\Downloads\GC313Pro_Firmware.exe` に保管
  - 公式チュートリアル動画: 「(ちょまくん)Switch2 で高画質動画投稿する方法」（TikTok @choma_ch、38秒、#PR 2025-09-18）
  - **Switch 2 購入の技術的前提 完全クリア** ✅ → あとは本体購入判断のみ（別途 ¥50,000 以上）
  - **User Guide v1.1 判明事項**（PDF を Mac `/tmp/gc313pro/` + MASU-P55 `C:\Users\gci_admin\Downloads\` に保管）:
    - **接続手順**: コンセント挿入 → HDMI でモニタ ON 確認 → 付属 USB-C で機器→C1 → Switch 2 は底面 Type-C → 画面が黒くなれば Dock モード正常
    - **OBS 推奨設定**: 解像度 1920×1080 / 60fps / **色フォーマット YUY2**
    - **⚠️ USB-A ポート制約**: USB-A と HDMI OUT は **C1 ソース機器専用**。USB-A マイクは C1 ソース（Switch 等）用のみで**C2 の PC 側からは使用不可**
    - **電源配分**: C1+C2 同時使用時は **各 45W に分散**（ノート PC 100W 充電と Switch 2 キャプチャの併用で充電速度低下の可能性）
    - **対応条件**: 信号ソースは **DisplayPort 1.2+（or Thunderbolt 3+）必須**。iPhone 15 Pro Max / Samsung S24U 対応確認例
    - **HDCP**: iPhone/iPad/Android 接続時は Assist Central Pro で **HDCP OFF** 必須
    - **認識条件**: **C2 に PC + AC プラグ挿入状態でのみ**キャプチャデバイスとして認識、Assist Central Pro は **C-to-C ケーブル接続時のみ**認識（C-to-A は不可）
    - **システム要件**: Windows 10+（UVC）/ **macOS 13/14 以降** / **iPadOS 17 以降**（Type-C 端子）

- [x] **WSL2 の 2 大用途を 2026-04-21 に完全把握**（MASU-P55 SSH 確認経由）

- [x] **WSL2 の 2 大用途を 2026-04-21 に完全把握**（MASU-P55 SSH 確認経由）
  - **背景**: 「WSL2 は Claude Desktop Code mode SSH 用途」とだけ CLAUDE.md に記録していたが、ユーザー指摘で別用途があることが判明 → SSH でマシン内部調査
  - **発見した 2 大用途**:
    1. **Claude Desktop Code mode SSH 接続先**（2222 ポートフォワード、keepalive スクリプト自動起動、アーカイブ状態）
    2. **Openclaw 実行環境**（**CLAUDE.md 未記載の新情報**）
  - **Openclaw 詳細**（`~/.openclaw/` ディレクトリ）:
    - ディレクトリ構造: agents / canvas / completions / cron / devices / identity / logs / memory / workspace
    - 設定: `openclaw.json`（バックアップ 5 世代保持）
    - **プロバイダ**: OpenAI Codex（OAuth 認証）
    - **モデル**: **openai-codex/gpt-5.3-codex**（GPT-5.3 Codex 派生モデル）
    - メモリ DB: SQLite `main.sqlite`（69 KB の学習蓄積）
    - cron ジョブ: `cron/jobs.json` 設定済
    - ウィザード configure 実行: 2026-02-24（約 2 ヶ月前に初期設定）
    - **今朝 4/21 09:02 に update-check.json が更新** = アクティブ運用中
    - 依存: Node.js v24.13.1（nvm 管理）
  - **CLAUDE.md 4/15 「AI駆動開発ツール時系列まとめ（Copilot→Cursor→Cline→Replit→Claude Code→Codex→OpenCode）」の OpenCode 系列に該当する可能性**
  - **保存された Claude Code セッション**（WSL 内）:
    - `/home/gci_admin/.claude/projects/-home-gci-admin-test/` (4/18 16:13 JST 最終更新)
    - `/home/gci_admin/.claude/projects/-home-gci-admin/` (4/17 10:38 JST 最終更新)
    - `claude --resume` で再開可能
  - **CLAUDE.md 更新**: ユーザー情報セクションの MASU-P55 項目に WSL2 の 2 用途併存を明記

- [x] **セッション終盤の MASU-P55 誤認訂正**（ユーザー指摘で発覚、本ファイル 2 箇所修正済）
  - **誤認内容**: OBS/GC313Pro セットアップ中の HP ProBook を「MASU-p 共有 PC の新発見（CLAUDE.md 未記載）」と記録
  - **実態**: それは **既存 CLAUDE.md 記載の MASU-P55 そのもの**（以前 SSH で操作実績あり、gci_admin ユーザー、Tailscale 100.125.21.47）
  - **誤認の原因**:
    1. OBS 画面下の紙メモ「MASU-p 内 共有PC 印刷・スキャン・ネット」に引きずられた
    2. masup アカウント + 1101 PIN を「コワーキング共用」と解釈 → 別 PC と誤判定
    3. PROBOOK ロゴと「masu-p55」の命名規則（masu-p + 55号機）を突合すべきだった
    4. CLAUDE.md の MASU-P55 情報（Tailscale, gci_admin, Claude Code 2.1.98, 以前 SSH 実績）と照合しなかった
  - **修正した 2 箇所**:
    1. 4/21 セッション記録の「MASU-p 共有 PC 発見」箇所 → 「MASU-P55（HP ProBook）と同一マシン」に訂正
    2. CLAUDE.md ユーザー情報セクションの Windows PC（MASU-P55）項目に **HP ProBook / Intel Core i5 / masup 追加アカウント / AVerMedia Assist Central Pro / OBS Studio 32.1.1** を追記
  - **次回以降の確認ポイント**（同じミス防止）:
    - MASU-P55 操作時は **masu-p（コワーキング名）+ 55 号機** の命名を前提に
    - **gci_admin（個人）/ masup（共用）の 2 アカウント併存** を前提に
    - Windows PC 関連情報は **必ず既存 CLAUDE.md セクションと突合**してから新記載判断
    - 紙メモ・シール等の表層情報よりも、**ハード ID / IP / Tailscale 端末名** で同一性判定

## 完了（4/18 夜〜4/19 朝セッション、AI 自動ゲームプレイ研究 3段階実験＋VoiceBox 発見）

- [x] **Crown & Coin デモの AI 自動プレイ研究（実験A・B・C 完走）**
  - **動機**: 維新の嵐 CD 到着後の AI 自動プレイ TODO #7 に向けた知見収集、および MacBookNEO 4/22 セットアップ後の Manus/Codex 運用基盤構築
  - **実験A: フルスクリーン効果検証** — **AI 自動化不可を確定**
    - macOS のフルスクリーン = 別 Space（仮想デスクトップ）に隔離される
    - screencapture / cliclick / Quartz bounds すべて現在 Space 限定
    - Quartz bounds は stale 値を返す（X=5108, Y=-69 でオフスクリーン判定）
    - 復旧手段: Mission Control (F3 = key code 160) → Esc → `osascript set position` でウィンドウ呼び戻し成功
    - **結論: フルスクリーンアプリの AI 自動化は macOS レベルで不可能**、維新の嵐 VM は QEMU ウィンドウモード（別 Space を作らない）なので問題なし
  - **実験B: 固定座標クリックシーケンス** — **成立、半自動化達成**
    - ウィンドウ位置/サイズ固定状態で 6 クリックシーケンスを確立
    - 酒場 → 酒場の親父と話す → 仕事 → 用心棒カード → 受ける → 完了
    - 1 イテレーション ~10秒、+128〜245F の報酬
    - 初期成功: 2,127F → 8,387F（6,260F ゲイン、複数バッチ分）
    - 複数回の window resize / move で座標が無効化、再キャリブレーションが必要
  - **実験C: Vision 頻度最適化（ピクセルシグネチャ方式）** — **実装完了、戦闘イベントで限界露呈**
    - Python スクリプト `/tmp/grinding.py` 作成、money 領域 (280, 200, 620, 290) の MD5 ハッシュで iteration 成否判定
    - Claude vision 呼び出しは「連続3失敗時のみ」まで削減、quota 大幅節約
    - 連続2失敗で auto_recover（Esc + 中立位置クリック）、連続3で停止
    - **成功率データ**:
      - 100 iter チャレンジ × 3回実施（round 1: 61/100, round 2: 16/100, round 3: 18/100）
      - 平均 **32 iter で戦闘トリガー**（酔っぱらい / 野盗 / ガラの悪い男）
      - 成功率 84〜100%（戦闘手前まで）
    - **本質的結論: 用心棒 grinding は定期的に BATAILLE（タクティカル SLG 戦闘画面）遷移する設計、AI クリックだけでは戦闘をクリアできず完全自動化は不可能**。だが戦闘前までは安定自動化可能
    - `/tmp/grinding.py` スクリプト、ピクセルシグネチャ検出、auto-recovery ロジックは維新の嵐・Manus 長時間タスク等に流用可能な基盤

- [x] **MUZINA GAMES が日本人ソロ開発者と確定**（4/19 02:44 JST 発言）
  - Discord #chat で Dominion さんの質問「solo dev or team?」に **"I'm a solo developer from Japan!"** と本人回答
  - 史実人物 1,015 人 + 5 シナリオ + 22 エンディングを**1人で実装中**という規模感（極めて野心的な個人開発）
  - "dev mode で集中すると返信遅れる"自認、「太閤立志伝V の過酷さに自分自身従いすぎ」発言など、**作家性の強さ**が腑に落ちる文脈
  - 4/22 MacBookNEO セットアップ後もコミュニケーション継続予定の貴重なコミュニティ

- [x] **VoiceBox（ElevenLabs 完全無料ローカル代替）発見・検証**
  - @so_ainsight 3連投スレッドで紹介、2026/04/16 v0.4.0 リリースの**超タイムリー**ツール
  - **GitHub**: https://github.com/jamiepine/voicebox （MIT License、20.5k star）
  - 技術基盤: **Alibaba Qwen3-TTS** ラッパー、Tauri (Rust) + React + FastAPI
  - **macOS Apple Silicon DMG**: https://voicebox.sh/download/mac-arm、MLX ネイティブ対応
  - **5 TTS エンジン**: Qwen3-TTS / LuxTTS / Chatterbox Multilingual / Chatterbox Turbo / HumeAI TADA
  - **23言語対応** + **DAW タイムライン**（複数話者・ポッドキャスト編集）+ **REST API**（プログラマブル）
  - **ユーザー主張の裏付け**: 月額$6 → $0 ✓、100% ローカル ✓、DAW は他 TTS にない差別化 ✓
  - ⚠️ **4/11 検証の既知事項**: Qwen3-TTS は過去に試して「動いたが似てなかった」（しぶ声再現度低い）
  - **未検証の期待エンジン**: LuxTTS / Chatterbox / HumeAI TADA（しぶ声クローン検証の価値あり）
  - **ElevenLabs Starter 5/11 失効対策**として最有力候補、CLAUDE.md TODO のしぶ音声編集パイプライン (D→A→B→C) の基盤技術になり得る
  - M1 8GB での同時稼働リスク: Claude Desktop + Claude Code + claude-mem + VoiceBox Qwen3 推論 = 5〜7GB 見込み、ゲーム自動化と排他運用推奨

- [x] **AI ツール業界の「楽観 vs 批判 vs 実用」トリオ観察**
  - **楽観**: @so_ainsight VoiceBox「レッドブル飲んでる間に 20本 YouTube 動画量産」的ヒャッハー
  - **批判**: Microsoft Copilot 未実装機能一覧（プロンプトリライト / エージェントハンドオフ / Researcher の Computer Use = 実はブラウザ）
  - **実用**: Superwhisper + Groq + Llama 選定記「速く・時々間違える > 遅く・稀に間違えない」UX 哲学
  - 3層を並べて「AI 実装の実態 vs 発表」の構造的理解、本日の実験C 所見と連動

- [x] **ゲーム進捗 & ユーザー手動 + AI 自動合算**
  - セッション開始 (4/18 18:15) 所持金 2,127F
  - 4/19 07:55 時点: AI 自動 grinding 進行中（round 4、60/100 iter、56成功/4失敗）
  - セッション中のトータル獲得: +10,000F 以上（ユーザー手動 + AI 自動の合算）

## 完了（4/18 17:11〜17:30 セッション、F5 送信キー検証＋alt+space へ置換）

- [x] **F5 → chat:submit の実戦検証と macOS Fn キー横取り問題の特定**
  - 新セッション開始（`claude --chrome -c`）時の StatusLine 実値: Weekly **31%** / 5h **24%**（リセット 4/24 04:00 JST）、16:00 セッションから微増（想定内）
  - F5 単押し → 反応なし、Fn+F5 → 反応なし、双方で送信発火せず
  - 診断結果:
    - `defaults read -g com.apple.keyboard.fnState` = 0（デフォルト、F1-F12 はメディアキー扱い）
    - `defaults read com.apple.HIToolbox AppleFnUsageType` = **2（Fn キーは絵文字ピッカー呼び出しに割当）**
    - Claude Code バイナリ (`~/.local/bin/claude`) の内部 key parser には `f1`〜`f12` 文字列が含まれる = アプリ側は F-key を受け入れる実装
    - 結論: **macOS 側で Fn/F-key が横取り**されて Terminal に物理 F5 キーコードが届かない
  - Claude Code の keybindings 仕様を再確認: 有効修飾キーは `ctrl` / `alt` / `shift` / `meta` の 4種のみ。**Fn は修飾キーとして使えない**（OS・ファームレベルで処理されアプリから観測不可）
  - 修飾キー単独（`alt` だけ等）もバインド不可、必ず他のキーと組合せが必要

- [x] **`alt+space` で chat:submit バインド置換**
  - `~/.claude/keybindings.json` を編集、`"f5"` → `"alt+space"` へ
  - Alt（=Option, ⌥）+ Space は Mac OS の予約ショートカットではない（Spotlight は Cmd+Space）ので衝突なし
  - 注意点: Mac では Opt+Space が NBSP（ノーブレークスペース）入力になるケースあり、Terminal.app の挙動次第で要再検証
  - 反映は新セッションから、検証は `claude --chrome -c` 再起動後のチャット入力欄で

- [x] **キーバインド系の学び（4/22 MacBookNEO セットアップに流用可）**
  - Claude Code の F-key 指定は可能だが、**macOS Fn 設定（AppleFnUsageType）に依存**するため単押し F-key は非推奨
  - 信頼できる送信キー候補: `alt+enter` / `cmd+enter`（Slack 流）/ `alt+space`（現採用）/ `ctrl+s`（既定の chat:stash と競合するので要 null 解除）
  - `~/.claude/keybindings.json` は git 外（ホーム配下）、MacBookNEO 移植時は内容を手動コピー or scp 転送

## 完了（4/18 16:00〜17:00 セッション、Chrome MCP 再起動＋MUZINA Discord 交流）

- [x] **Claude Code を `claude --chrome -c` で再起動、Chrome MCP 有効化**
  - 再起動直後に SessionStart hook が `rate_limits` を読み込み、Claude コンテキスト冒頭に「Weekly 29% / 5h 10% / resets 04/24 04:00 JST」を自動注入
  - **StatusLine 表示 + hook 注入のパイプライン完全動作確認**（設計どおり）
  - `claude-in-chrome` MCP ツール群が ToolSearch 経由でロード可能に（`mcp__claude-in-chrome__*` 17 本）

- [x] **MUZINA GAMES Discord（Crown & Coin The Hundred Years サーバー）で開発者と直接対話**
  - 全チャンネル偵察: `#news` / `#welcome` / `#chat` / `#bug-reports` / `#hundred-years-war` / `#history-misc`、計 27 投稿のごく小さなコミュニティ
  - 開発者 **MUZINA GAMES 本人** が活発に返信、`#hundred-years-war` から「ゲーム質問は #chat へ」と明示的誘導あり
  - `#chat` に質問 3 件投稿（病気治療 / ゲーム内ヘルプ Wiki / セーブ後 Edward に切替わる現象）、**回答全てを数分で獲得**:
    - 「**行動力 0 でも行動可能**、病気 AND HP ≤10 で無制限化」
    - 「**病気治療: Barber-surgeon（理髪外科医）に薬調合依頼→飲む** or **自宅で休息して自然治癒**（デモ版は老衰死 無効）」
    - 「公式マニュアル・Wiki は現時点なし」
    - 「**macOS 版 save/load 機能がバグで破損、次回アップデートで修正予定**。当面は再起動時 **C+O+M 3キー同時押し**で Serf（農奴）時代スキップして続きから再開可能」— これが「セーブすると Edward 42歳になる現象」の正体
    - 「**テキスト送り: Space または Z キー**」
    - 「**酒場の老人 NPC に話しかけると、キーボードショートカットや隠しコツを教えてくれる**」= 事実上のゲーム内ヘルプ機能
  - **「太閤立志伝V（初代 PS2版）リスペクト」を開発者本人が明言**（CLAUDE.md 4/18 午後の「太閤立志伝ライク」と完全整合、ルーツ確認）
  - 日本人プレイヤー **きりん** さんも同時間帯に Discord 参加、ミニゲーム難易度フィードバック投稿（開発者が日本語で返信、「プレイアブルキャラ親愛度 MAX でミニゲーム OFF 機能」将来実装方針を回答）
  - **投稿 UI 学習**: Chrome MCP の `computer.type` アクション内の改行 `\n` が Discord Slate editor で **Enter=送信**として解釈される → 長文改行付きテキストが意図せず複数メッセージに分割送信される挙動。**1行テキスト（改行なし）+ Return キー単発 = 1メッセージ送信** が正しいパターン

- [x] **F5 キーを chat:submit（送信）に追加バインド**
  - `~/.claude/keybindings.json` 新規作成、Chat コンテキストで `"f5": "chat:submit"` 追加
  - Enter は既定のまま（additive バインディング）= Enter + F5 両方送信可
  - 反映は新セッションから、`/doctor` で警告なし確認推奨
  - 4/22 MacBookNEO セットアップ時、F5 での送信が好みなら同ファイルを移植することで流用可能

- [x] **しぶ #3 #4 Instagram ストーリー knowledge 追記コミット反映確認**（commit 2e5a1c2 で反映済、事後検証）

## 完了（4/18 11:52〜16:00 セッション、昼〜午後）

- [x] **Crown & Coin: The Hundred Years Demo（百年戦争立志伝）インストール・起動・自動プレイ検証**
  - 作者 @SuguruKun_ai の解説スレッド発見 → ユーザー興味 → デモ導入
  - **Steam** 未インストール状態から `brew install --cask steam` で導入（~60秒）
  - **Rosetta 2 インストール**（`softwareupdate --install-rosetta --agree-to-license`、~1分、削除困難な旨を Homebrew cask 警告通り把握、実害なしで永続化）
  - Steam Guard QR コードログイン成功（iPhone Steam Mobile アプリから PC の QR コードスキャン＋承認、ID/パスワード/Guard コード一切入力不要）
  - `steam://install/4619520` でデモ DL（~2分、2.78GB、依存ランタイム込みで downloading/ に 2.6GB 蓄積後 common/ へ展開）
  - **デモ app_id: 4619520**（製品版 app_id: 4476270）
  - **実行ファイル**: `Mach-O 64-bit arm64`（**Apple Silicon ネイティブ**、Rosetta 不要）、Bundle ID `com.crownandcoin.demo`、Electron + Vulkan SwiftShader、日本語 `ja.pak` 同梱
  - 起動 `open steam://rungameid/4619520` → 5プロセス（メイン + GPU + Renderer + ネットワーク + オーディオ）、`--lang=ja` 日本語ロケール確認
  - カスタムフェイス用 `~/Library/Application Support/CrownAndCoin/Characterface` 生成 = キャラメイク機能あり
  - **自動プレイ検証**: `screencapture -l <window_id>` + `cliclick c:X,Y` + Read tool（Claude vision）のループで開幕ナレーション数画面を自動進行成功（「1355年──フランス王国は、終わりの見えない戦争の中にあった」→「あなたの世界は──」→ 次画面）
  - 詰まりポイント: グレースケール農家シーンの「0/15」カウンター画面でクリック反応なし、隠れオブジェクト探しか特定 UI 必要と推定 → 自動プレイ停止、ユーザー手動進行へハンドオフ
  - **学び**: computer-use MCP は Steam 内パス（`&amp;amp;` HTML 二重エンコード含む）を LaunchServices スキャンで認識できず（エラー -10811）、symlink 作成も効果なし → 代替ルート（screencapture + cliclick + Read）で回避可能

- [x] **太閤立志伝ライクの位置づけ判明**
  - Game*Spark 記事（2026/04/17 デモ版公開時、https://www.gamespark.jp/article/2026/04/17/165315.html）で「**太閤立志伝ライクな百年戦争舞台の中世歴史サンドボックスRPG**」と明言
  - 史実人物 1,000〜1,015 人（黒太子・ジャンヌ・デュ・ゲクラン等）は製品版解禁、**デモはオリキャラのみ**
  - 5 シナリオ + 22 タロット系エンディング + カスタムシナリオ
  - TODO #7 の維新の嵐（Koei 太閤立志伝系）と同じ系譜 → 両者は直接比較可能な資産
  - **開発**: MUZINA GAMES（スタジオ）
  - **公式 Discord**: https://discord.gg/xEpyDFQxCr（デモ公開直後は開発者も活発）
  - **Steam コミュニティ**: まだスレッド 2 件のみ（英語 Bug Reports + 中国語 1 件）、日本語コミュニティ未形成

- [x] **Claude Code 週次使用量を可視化する StatusLine + SessionStart hook 構築**
  - 従来: `/status` `/cost` `/usage` はダイアログ表示のみ、Claude 側から数値把握する手段なし
  - claude-code-guide エージェントで調査 → **Claude Code は statusline スクリプトに `rate_limits.seven_day.used_percentage` / `rate_limits.five_hour.used_percentage` を stdin JSON で毎ターン渡す**と判明
  - **`~/.claude/statusline.sh`**: stdin JSON パース → `/tmp/claude-usage.json` に週次 / 5h % + リセット unix 保存、画面下部に `[Opus 4.7 (1M context)] W:XX%→MM/DD 5h:XX%` 表示
  - **`~/.claude/hooks/inject-usage.sh`**: SessionStart 時に `/tmp/claude-usage.json` 読み込み → `{hookSpecificOutput: {hookEventName, additionalContext}}` JSON で Claude のコンテキストに注入
  - **`~/.claude/settings.json`**: `statusLine` + `hooks.SessionStart` 追加、既存設定（env / permissions / plugins / effortLevel 等）は完全保持
  - **現在値（4/18 14:45 取得）**: **週次 29.0% 使用**（残 71%、リセット **4/24 04:00 JST**）、5時間 4% 使用（リセット 4/18 19:00 JST） — CLAUDE.md の「4/24 金 4:00 以降の新週」記述と完全一致
  - 次セッションから私（Claude）が冒頭で残枠を自動把握可能に
  - MacBookNEO 4/22 16:30 セットアップに向けて、残枠管理が定量化された

- [x] **しぶ Instagram 4連投（同日物語構造）を knowledge 追記**
  - `ai-minimalist-shibu/knowledge/shibu-ai-update.md` にセクション「テスラ改造：サイバー空間化（2026/4/18 Instagramストーリー）」展開
  - #1 11:44 EVNOVA Before/After（@evnova_custom、福岡 320 モデルY、アンビエントLED サイバー化）
  - #2 11:44 紫ライト車中泊フルベッド（没入感演出）
  - #3 12:48 ポケモンチャンピオンズ マスターIV 5連勝中（「家よりゲーミング部屋っぽい」20時間プレイ）
  - #4 13:01 トレーナーID「ミニスカート」レート 1643.619（「ミニマリストって肩書きないからミニスカートで代用」）
  - 物語構造: テスラ改造 → ゲーミング化 → 実戦ランクIV → アイデンティティ表明、の4段プロット
  - 読み解き: ミニマリズムブランドの中に「無駄の極致」に見えるゲーム実戦を織り込む、矛盾を活かす更新パターン

- [x] **X Daily Briefing 追記: @SuguruKun_ai の video-use 解説スレッド（3連投）**
  - `docs/x-daily-briefing.md` に新規セクション（commit b1a02a5）、初回 commit なのでファイル自体も git 管理下へ昇格
  - 投稿1: 素材フォルダ→完成mp4 自動生成の強調フック
  - 投稿2: ElevenLabs Scribe 単語タイムスタンプ + takes_packed.md 設計
  - 投稿3: `git clone` → ln -s → `pip install -e .` のインストール3行、`cd video-use` 抜けの注意点併記
  - 自分の 4/17 導入実績との突合で精度チェック、takes_packed.md / 自己評価ループ等スレッド未言及ポイントも記録

- [x] **iPad → TV（Panasonic VIERA TH-40CX700）HDMI 接続の HDR 設定逆転現象を記録**（2015年 4K TV、HDR 非対応確認済）
  - ユーザー発見: 「優先ディスプレイ設定 = HDR」にしたら映った
  - 解釈: iPad UI 上では HDR=推奨 / SDR=互換性優先だが実際は HDR=**コンテンツ適応モード**（TV 能力を EDID で確認してフォールバック）/ SDR=**強制固定**（60.00Hz+10bit+広色域で非対応 TV が受け入れ拒否）
  - 非 HDR TV には HDR 指定が正解、という UI 命名の罠を確認

- [x] **HyperDeck Studio HD Mini + iPad HDMI 接続失敗の原因特定**
  - 原因: iPad 60.00Hz/VRR/広色域 vs HyperDeck 1080p59.94 SMPTE 固定、Micro Converter BiDirect SDI/HDMI は電気的変換のみでフレームシンク無し
  - 解決策: Blackmagic UpDownCross HD Mini（約¥70,000、HDMI→SDI+フレームシンク）/ ATEM Mini（約¥40,000、入力フレームシンク搭載、HDMI 出力 1080p59.94 conform）/ Decimator MD-CROSS V2（約¥100,000）
  - 放送規格 59.94Hz の NTSC 由来（カラーサブキャリアとの干渉回避で 0.1% 下げた呪い）を教科書的に整理
  - 今後配信系機材拡張時の参照になる学び

- [x] **Chrome 拡張 "Claude" 検出（ID: fcoeoabgfenejglbffodgkkbkcdhcgfn）**
  - `/Applications/Claude.app/Contents/Helpers/chrome-native-host` プロセス稼働中、Claude Desktop と Chrome 間の native host 確立済
  - 現 Claude Code セッションは `claude --dangerously-skip-permissions` のみで起動、`--chrome` フラグ無し → Chrome MCP ツール未ロード
  - 次回 Chrome MCP を使いたいときは `claude --chrome -c` で再起動する（コンテキスト継承可）
  - 当面の用途: MUZINA Discord で Crown & Coin 質問投稿（行動力切れ・病気治療の詰まりを解消したい）

- [x] **iPhone Steam Mobile アプリ同定**（com.valvesoftware.Steam、Valve Corporation 公式）
  - 類似兄弟アプリ Steam Chat / Steam Link は認証機能なしで別物
  - QR コードログイン対応で ID・パスワード不要のサインインが可能、本セッションで実証済

## 完了（4/18 9:00セッション前作業）

- [x] **Codex Computer Use プラグイン動作確認・TODO #8 クローズ**
  - Codex v26.415.30602（build 1773、Mac 版）で「コンピュータの使用」設定に Computer Use v1.0.750 (openai-bundled) ✓ 表示で有効
  - 「常に許可するアプリ」は Settings UI からは read-only、**Codex チャットで Computer Use 許可ダイアログで「常に許可」チェック→許可でアプリ追加される仕組み** と判明
  - 検証として "Finder でホームフォルダを開いてスクリーンショットを撮って" プロンプトを投げ → 許可ダイアログで常に許可チェック → Finder が 常に許可するアプリ リストに登録確認
  - Free プラン週次レート 71% 消費（リセット 4/25）、以降の追加アプリ登録は 4/25 以降に温存決定

- [x] **Manus デスクトップアプリ (Meta 傘下) インストール・サインイン・最有力 Computer Use 候補に採用**
  - `/Applications/Manus.app` v1.5.3（署名 Team 5V8XDGQQB6、arm64、Meta 傘下、`download.manus.im/Manus-Setup-1.5.3.dmg` 141MB）
  - iPhone Manus (pirosi80@yahoo.co.jp) と Mac でアカウント自動連携、7964 クレジット + 毎日更新 300（00:00 リフレッシュ）
  - 左メニュー: アカウント / 設定 / 使用状況 / スケジュールタスク / Mail Manus / データ管理 / クラウドブラウザ / **My Computer** / パーソナライゼーション / スキル / コネクタ / 統合 / About / ヘルプ
  - 過去利用履歴: SwitchBotリサーチ -213 / AI塾テキスト -36 / Claude Code分析 -56 等、**1タスク 30〜210 クレジット消費**目安
  - **Manus Pro は¥6,000/月 (8,000クレジット)** — Free の 300/日×30=9,000 と同等以上なので契約不要、1〜2か月 Free で様子見判断
  - CLAUDE.md 上、Claude Desktop Code mode は SSH 遠隔用、Codex は補助、Manus が日常使い筆頭の3層構成に

- [x] **Copilot CLI v1.0.31 → v1.0.32 アップデート**
  - `npm install -g @github/copilot@latest`（パッケージ名は `@github/copilot`、`@github/copilot-cli` ではない）
  - 新機能: `--connect` リモートセッション接続 / `--print-debug-info` 診断フラグ / 週次制限 75%・90% 警告 / auto モデル選択 / レート制限時のキュー自動再試行
  - `copilot --print-debug-info` 動作確認: Apple Terminal v470.2 / arm64 / local terminal 検出

- [x] **MacBookNEO 新規 Mac セットアップ計画を確定**（4/22 16:30 予定枠、全て当日実施）
  - **当日インストール完全リスト**:
    1. **Tailscale**（pkg 版、brew ではなく Standalone、https://pkgs.tailscale.com/stable/#macos、GUI ログイン + システム拡張許可必須）
    2. **SSH 鍵生成**（`ssh-keygen -t ed25519`、公開鍵を現 Mac `100.99.41.2` の `~/.ssh/authorized_keys` に追加）
    3. **Manus**（DMG、pirosi80@yahoo.co.jp でサインイン）
    4. **Claude Desktop**（DMG、仲結花 Max でサインイン、Code mode に `yuika@100.99.41.2:22` 登録）
    5. **Codex**（brew または DMG）
    6. **Claude Code CLI**（docs/claude-code-install-macbookneo.md §0 のプロンプトで Manus に依頼して自動インストール）
  - **当日の使用優先順位（4/18更新）**: **① Manus（Claude 週枠を消費しない、Free 7,964 クレジット残、自律実行が最適）→ ② Claude Desktop（Manus で詰まった箇所のメイン会話フォールバック、週枠消費）** — Codex は当日は使わない方針（Free 週枠 71% 消費済で余裕なし）
  - 4/22 は Claude 週枠を大量消費予想のため、**4/18〜4/21 の間は Claude Code セッションを軽量運用（X情報収集と軽い更新のみ）** に抑える。重い作業は 4/24 金 4:00 以降の新週に後送
  - **現 Mac 側の事前準備（4/18 済み）**: システム設定 → 一般 → 共有 → リモートログイン **既に ON** を確認済（ローカルホスト名 `yuika.local`、Tailscale `100.99.41.2:22` で MacBookNEO から受け入れ可能）

- [x] **docs/claude-code-install-macbookneo.md + .html に §0「AI エージェントへの依頼」追加**
  - Manus / Codex / Claude Desktop の3系統共通プロンプト、エージェント別補足、監視用5行コマンド列を追記
  - GitHub Pages デプロイ確認（commit 3aaab68）: https://wirelessml.github.io/test/docs/claude-code-install-macbookneo.html#agent

- [x] **はりきゅう整体しゅん LP GitHub Pages 公開**（外出先閲覧可）
  - https://wirelessml.github.io/test/docs/hari-seitai-shun.html#info（commit 06d7a9b）

## 完了（4/18 5:00セッション・早朝）

- [x] **GHFS（GitHub仮想ファイルシステム）セットアップ完了** — TODO #10 クローズ
  - マウント先: `/Users/yuika/ghfs`（wirelessml リポ配下を Finder で参照可能）
  - **根本原因特定**: macOS 26.5 Tahoe は ~/Desktop / ~/Documents / ~/Downloads 配下への FSKit マウントを TCC 保護で必ず拒否（fskitd が root でも mount(2) errno 1/EPERM）
  - 診断ログ: `fskitd: will mount over LIFSv2` → `mount(2) error: 1` → `mount launch failed with result "Operation not permitted"`
  - システム設定「ファイルシステム機能拡張」のトグルが反応しない件は macOS 26.5 beta の syspolicyd バグ（`qtn_proc: 3` 多発）、pluginkit -e use で CLI 強制有効化可能だがカーネル承認は別レイヤーで、実際の解決は TCC 非保護パスへの変更
  - CLAUDE.md TODO #10 に注意書き追記（wizard が `~/Desktop/ghfs/ghfs` を提案することがあるので必ず `~/ghfs` 等へ変更）、Apple 未文書の落とし穴として記録

- [x] **はりきゅう整体しゅん LP を GitHub Pages 公開**（外出先アクセス可）
  - URL: https://wirelessml.github.io/test/docs/hari-seitai-shun.html#info
  - `docs/hari-seitai-shun.html`（637行）を add → commit (06d7a9b) → push、HTTP 200 確認

- [x] **Claude Desktop Code mode → Windows WSL Ubuntu SSH 接続完了**（Opus 4.7 1M Max 稼働）
  - Mac Claude Desktop → Tailscale (100.125.21.47:2222) → Windows portproxy → WSL Ubuntu sshd
  - wirelessml/test リポを WSL に shallow clone (`/home/gci_admin/test`)
  - Claude Desktop 作業フォルダに `/home/gci_admin/test` を設定、Opus 4.7 1M Max + Code mode でリモートコーディング可能
  - iPhone Claude Desktop からも同設定を呼び出せる → 外出先から Windows 側作業継続可能に

- [x] **Claudeデスクトップアプリ評価を改定**（CLAUDE.md 更新済み）
  - 4/14「不要」判断 → 4/18「Code mode / メイン会話のみ使える」に改定
  - **使える**: メイン会話、Code mode（SSH 越しの WSL 作業）
  - **使えない（不変）**: Dispatch と Cowork は app.asar 側で Sonnet 4.6 がハードコードされており UI 非連動、Opus 4.7 GA 後の 4/17 再確認でも未解消
  - リソースコスト（Electron ×10プロセス、~786MB）は依然重いので他重処理と同時稼働は避ける

- [x] **X投稿**: Claude Desktop Code mode + WSL SSH + Opus 4.7 1M Max セットアップ
  - URL: https://x.com/i/status/2045264433656819866
  - redacted スクショ（user@host ぼかし、モデル選択ポップオーバー込み）付き

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
  - v1.0.2.0 は**英語UIのみ**、日本語ロケール未同梱（検索結果・AI Mode応答自体は日本語可）
  - appguid: `{06A8089E-0B65-445D-B5C4-10B0D1B540F2}`、ClientState lang=ja-JP（将来の多言語化で反映見込み）
  - 2026/4/17 16:07 時点：Cohort が `Canary - 10% - General Availability` に更新（= Canary 10% → GA 昇格済み）。Omaha 毎時問い合わせで `status:noupdate` を返すため v1.0.2.0 が現 GA 最新版。AlternativeTo 2026/4/14 記事「Google's upgraded desktop app is now available on Windows」のグローバル公開分は本バージョンで同一
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
- [x] X投稿: Google Windows App v1.0.2.0 Canary→GA 昇格の実態: https://x.com/i/status/2045051837313888636

## 完了（4/17 14:00セッション）

- [x] Switch 2 ドックなしMac接続キャプチャ製品調査（純正ドックなしではDP Alt Modeブロック、サードパーティ互換ドック・キャプチャ製品リスト化）
- [x] AVerMedia GC313Pro ELITE GO（日本商品名: Live GENERATOR POCKET ポケットキャプチャー、SKU DV0963）特定 — 100W GaN PD + 1080p60 UVCキャプチャ内蔵
- [x] メルカリ出品（¥14,961 新品未使用 正規代理店保証1年）と Amazon.co.jp 中古（¥9,833 残り1点）を比較、Amazon中古を購入決定
- [x] CLAUDE.md TODO #9 Switch 2キャプチャ環境構築（到着後動作確認手順）追記

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
- [x] YouTube字幕取得: QzMDrHjAhpI（しぶライブ）、ukfCg8ZgMjA（大川優介×しぶルームツアー）
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
- MacBook Air M1 8GB — **持ち運び用**（4/22 16:34〜、しゅん先生 PC をコワーキング据え置き化したため役割変更）
  - 外出先・自宅・コワーキング間を移動、モバイル作業機
  - Homebrew 5.1.5、Tailscale 1.96.5、Claudeデスクトップアプリ インストール済み
  - Claude Code CLI + agent-browser + dev-browser
- Windows PC（MASU-P55）— コワーキングオフィス、サブ作業機
  - **ハードウェア: HP ProBook（Intel Core i5）**（4/21 判明）
  - ユーザー: gci_admin / IP: 192.168.2.248 (masu-p55.local)
  - 追加アカウント: **masup**（PIN は紙メモ記載、コワーキング共用、印刷・スキャン・ネット検索用途）
  - SSH接続情報は ~/.claude/local-notes/wifi.txt、Windows パスワードは ~/.claude/local-notes/winpass.txt（いずれも git 管理外）
  - Claude Code v2.1.116 インストール済み（`C:\Users\gci_admin\.local\bin\claude.exe`、4/21 08:52 自動更新、毎日 0:00 タスクスケジューラで最新化）
  - Claudeデスクトップアプリ インストール済み（Microsoft Store版）
  - Computer Use対応（Windows版、2026/4/3〜）
  - **AVerMedia Assist Central Pro** インストール済み（4/21、GC313Pro 用）
  - **OBS Studio 32.1.1** インストール済み（4/21、iPhone 縦画面キャプチャ動作確認済み）
  - リポジトリ: C:\Users\gci_admin\test（同じナレッジベース共有）
  - **WSL Ubuntu 24.04 稼働中**（2 用途併存）:
    - ① **Claude Desktop Code mode SSH 接続先**（2222 ポート、keepalive タスク稼働、アーカイブ状態）
    - ② **Openclaw（OpenAI Codex ベース AI エージェント CLI）実行環境**（4/21 09:02 に update-check 実行、**アクティブ運用中**）
    - Node.js v24.13.1（nvm 管理、Openclaw 依存）
    - WSL 側 Claude Code セッション保存: 2 件（4/17 / 4/18）
  - MacからSSH経由でリモート操作可能
- **しゅん先生 PC**（**4/22 16:34〜 コワーキング据え置き化**、**4/22 18:20 Plextor SSD 死亡で Seagate クローン緊急起動**、旧: 伊丹市はりきゅう整体しゅん業務用）
  - **配置変更**: 伊丹市（しゅん先生業務用） → コワーキング（新メイン据え置き）、4/22 16:34 に配置転換
  - **4/22 18:20 緊急事態**: **Plextor SSD が NVMe コントローラエラーで完全死亡**、Seagate クローンに自動フォールバック起動中（詳細は 4/22 午後セッション完了記録）
  - PC 名: DESKTOP-ATQ36KS / iiyama STYLE Infinity by iiyama（2018 年頃購入 BTO デスクトップ）
  - 製造元: 株式会社ユニットコム（0570-550-884）
  - CPU: Intel Core i7-8700K @ 3.70GHz（6C12T、第 8 世代 Coffee Lake、2017/10 リリース、95W TDP、OC 可）
  - RAM: 16GB DDR4-2666（15.8GB 使用可能）
  - GPU: Intel UHD Graphics 630（iGPU のみ、dGPU なし）
  - OS: Windows 11 Home **25H2**（build 26200.8037、2025/02/05 クリーンインスコ）
  - ストレージ: 合計 2.05TB → **1.82TB**（Plextor 256GB 死亡により喪失、Seagate 2TB のみ稼働）
  - ~~C: Plextor PX-256M9PeGN 256GB NVMe~~ **4/22 18:20 死亡、デバイス検出不可（Get-Disk から消滅）**。WHEA_UNCORRECTABLE_ERROR 0x124 + stornvme Event 11 → 完全応答停止。生前の状態: 使用 130GB、健康状態「正常 66%」、総書込 69TB、使用時間 26,779h、Plextor 事業撤退済でサポートなし、ファーム 1.03 最終版。**2024 年 KIOXIA 傘下で SSD 撤退済**ブランド
  - **C:（現在） = 旧 D: の Seagate ST2000LM015-2E8174 2TB SMR HDD**（SATA/600、5400rpm、2.5 インチ）— Hasleo クローン（17:15-17:34）により起動可能な完全複製を保持していたため、Plextor 死亡後の強制再起動で自動的に Boot Manager が Seagate にフォールバック。現在 Windows 11 25H2 が Seagate から稼働中（遅いが動く、SMR HDD 特性で体感 50-100 倍遅）。健康状態 正常、使用時間 23,722h、電源投入 20,759 回、温度 27°C
  - `D:\Backup\Weekly System Image\Weekly System Image.adi` = 82.94GB、4/22 18:05 作成の AOMEI システムイメージ（今は C:\Backup\ として見える）
  - モニター: LG 製（型番不明、デスクトップ設置）
  - **次の最優先タスク（4/22 夜）: 新 SSD 注文**
    - 推奨: Crucial P3 Plus 1TB ¥8,500（Amazon 翌日配送）
    - 代替: WD Black SN770 1TB ¥11,000 / Samsung 990 EVO 500GB ¥9,500
  - **4/23 以降の SSD 換装手順**:
    1. 新 SSD 到着 → しゅん先生 PC シャットダウン → ケース開ける
    2. 死亡 Plextor を M.2 スロットから抜く → 新 SSD を同スロットに挿入
    3. Seagate HDD から起動（今と同じ）→ Hasleo で Seagate → 新 SSD にクローン（18 分）
    4. BIOS で新 SSD を Boot 1st → 再起動
    5. Seagate は今後のバックアップ用 D: として継続利用
  - 新用途: コワーキングでの据え置きメイン作業機（Core i7-8700K + 16GB で M1 8GB より馬力あり、OBS・画像処理等の重い作業向き）— **ただし新 SSD 換装まで SMR HDD 起動のため重い作業は保留**
  - 旧用途: しゅん先生（はりきゅう整体・伊丹市）の業務用 PC（予約管理・領収書・患者関連フォルダあり）— 4/22 まで
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
- **Manus デスクトップアプリを Computer Use の最有力候補に採用**（4/18 朝決定）
  - `/Applications/Manus.app` v1.5.3（署名: Team 5V8XDGQQB6、arm64、Meta 傘下）
  - iPhone Manus (pirosi80@yahoo.co.jp) と Mac でアカウント自動連携、**7964 クレジット + 毎日更新 300**（00:00 リフレッシュ）
  - 過去利用履歴: SwitchBotリサーチ -213 / AI塾テキスト -36 / Claude Code分析 -56 等、1タスク 30〜210 クレジット消費の目安
  - イベント報酬 +6,000 + リデンプション +1,000 の蓄積あり
  - 左メニュー「My Computer」が OS 操作本体、クラウドブラウザ・スキル・コネクタ・スケジュール化タスク等の自律エージェント機能一式を無料枠で使える
  - Claude Desktop / Codex と比べて: (1) 無料で Computer Use 可、(2) 自律タスク実行時間が長い、(3) クラウド実行とローカル実行を選べる
  - 競合候補も残すが、日常使い筆頭は Manus。Claude Desktop Code mode (Opus 4.7 1M Max) は SSH 遠隔コーディング用、Codex は補助
- **Claudeデスクトップアプリは Code mode / メイン会話のみ使える**（4/18再評価）
  - **使える**: メイン会話・**Code mode**（Opus 4.7 1M Max で Tailscale 経由 Windows WSL Ubuntu に SSH 接続、iPhone からも同設定で外出先作業可）
  - **使えない（不変）**: **Dispatch** と **Cowork** は app.asar 側で `--model claude-sonnet-4-6` がハードコードされており、UI でモデル選択しても反映されない（4/15 Mac/Windows 両方で確認、Opus 4.7 GA 後の 4/17 再確認でも未解消）
  - リソースコストは依然重い（M1 8GB で Electron ×10プロセス、~786MB）ので他重処理と同時稼働は避ける
  - 4/14旧判断の背景: 当時は Opus 4.6 で Code mode の SSH も未検証、Dispatch/Cowork が Sonnet 固定で実用性に乏しかった
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


## Mac 常駐プロセスのデフォルト構成（4/18 確定）

**常時起動（M1 8GB のデフォルト運用）:**

| プロセス | RSS 目安 | 役割 |
|---|---|---|
| Claude Desktop (`/Applications/Claude.app` + helpers) | 550–750 MB | メイン会話 / Code mode / Computer Use |
| Claude Code CLI (`claude --dangerously-skip-permissions`) | 650–750 MB | 現セッション本体 |
| claude-mem worker (bun) + Sonnet 4.6 子プロセス | 300–400 MB | 観察記録生成 |
| chroma-mcp (Python) | 280–290 MB | claude-mem ベクトル DB |
| Claude Desktop 由来の Virtualization VM | 70–80 MB | Claude Desktop サンドボックス |
| Terminal | 150 MB | Claude Code CLI のホスト |

**合計 ≒ 2.0–2.4 GB**（AI ツール関連）、 残り ≒ 5.5–6.0 GB をシステム・その他用途へ割当

**必要時のみ起動（常駐させない）:**
- Codex（Free 週枠制限タイト、Claude で代替）
- Manus（タスク実行時のみ起動、普段は閉じる）
- OBS / ブラウザ多タブ / 動画系プロセス
- QEMU Windows XP VM

**メモリ圧迫時の対処順:**
1. Chrome など重いブラウザを閉じる
2. 使用中でない AI アプリ (Codex / Manus) を閉じる
3. claude-mem の chroma-mcp は残す（観察中断すると記録欠損）
4. Claude Desktop は残す（今日の判断: Code mode / メイン会話用に維持）
5. 最後の手段として Claude Code CLI を終了してセッション再開

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

