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
- 中古品のため到着後動作確認:
  1. 通電・LED点灯確認
  2. Mac M1 で OBS → 映像キャプチャデバイス（UVC、ドライバ不要）として認識されるか
  3. 1080p60 出力可否・遅延確認
  4. 100W GaN PD 給電動作確認
- 接続フロー: Switch 2 → USB-C(100W入力) → GC313Pro → HDMI(パススルー) → モニター / GC313Pro → USB-C(PC側) → Mac M1
- 別途 Switch 2 本体購入が必要（未購入）

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

