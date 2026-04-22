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



