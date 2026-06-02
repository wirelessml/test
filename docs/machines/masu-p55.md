# Windows PC (MASU-P55)

> Last updated: 2026-06-02

## 役割

**コワーキングオフィス サブ作業機**
- 配置: コワーキングスペース据え置き
- 主用途: **Codex 専用機**（WSL2 の Codex CLI ＋ Windows の Codex Desktop App）。印刷・スキャン・ネット検索も。**OpenClaw は 2026-06-02 に削除**（旧: WSL Ubuntu 上で OpenClaw 実行）
- 所属: コワーキング設置（一部共用）

## ハードウェア

- **モデル**: HP ProBook（Intel Core i5）（4/21 判明）

## OS / ソフトウェア

- OS: Windows（バージョン詳細未記録）
- Claude Code v2.1.157（`C:\Users\gci_admin\.local\bin\claude.exe`、standalone binary、2026-05-30 `claude update` で確認、毎日 0:00 タスクスケジューラで最新化）
- Codex CLI v0.135.0（npm `@openai/codex` global、`%APPDATA%\npm\codex`、設定一式は `~/.codex/`、2026-05-30 更新）
- Gemini CLI v0.44.1（npm `@google/gemini-cli` global、2026-05-30 更新）
- **Codex Desktop App v26.527.3378.0（Microsoft Store / MSIX、`OpenAI.Codex`）** — 詳細は下記「Codex Desktop App」セクション
- Claudeデスクトップアプリ（Microsoft Store 版）
- Computer Use 対応（Windows 版、2026/4/3〜）
- AVerMedia Assist Central Pro（4/21 インストール、GC313Pro 用）
- OBS Studio 32.1.1（4/21 インストール、iPhone 縦画面キャプチャ動作確認済み）
- リポジトリ: `C:\Users\gci_admin\test`（同じナレッジベース共有）

## ユーザーアカウント

- **gci_admin**: 個人メインアカウント
- **masup**: 追加アカウント、PIN は紙メモ記載、コワーキング共用（印刷・スキャン・ネット検索用途）

## ネットワーク

- ローカル IP: `192.168.2.248` (masu-p55.local)
- Tailscale: 導入済み（IP 100.125.21.47）
- Mac からの SSH 経由でリモート操作可能
- SSH 接続情報: `~/.claude/local-notes/wifi.txt`（git 管理外）
- Windows パスワード: `~/.claude/local-notes/winpass.txt`（git 管理外）

## Codex 画像添付の扱い

- Mac 側 ChatGPT/Codex に添付された画像は、Mac の `/tmp/codex-remote-attachments` に配置される
- Mac の LaunchAgent `com.yuika.masup-codex-attachment-sync` が 20 秒間隔で MASU-P55 の `C:\tmp\codex-remote-attachments` へ同期
- Windows 側 Codex では `/tmp/codex-remote-attachments/...` が `C:\tmp\codex-remote-attachments\...` として読めることを確認済み
- Windows 側の `C:\Users\gci_admin\AGENTS.md` と `C:\Users\gci_admin\test\AGENTS.md` に、このパス変換と `codex exec --image ...` の注意を記録済み
- Mac 側から明示的に画像を MASU-P55 Codex に読ませる補助コマンド: `/Users/yuika/local/bin/masup-codex-image`
- 添付フォルダの手動同期コマンド: `/Users/yuika/local/bin/masup-sync-codex-attachments`

## Codex Desktop App (Microsoft Store / MSIX)

- **発見: 2026-05-30**。`OpenAI.Codex` が **Microsoft Store (MSIX) 経由**で導入済み（v26.527.3378.0、x64、PackageFullName `OpenAI.Codex_26.527.3378.0_x64__2p2nqsd0c76g0`）。CLI（npm `@openai/codex`）とは別物の GUI アプリ。
- ⚠️ **MSIX/Store アプリは従来の検出法に出ない**: アンインストールレジストリ・Program Files・スタートメニュー・`winget list | findstr` いずれにも現れず、`AppData\Local\OpenAI\Codex` には CLI ヘルパー（`rg.exe`）しか無い。**検出は `Get-AppxPackage` のみ**:
  ```bash
  ssh masu-p55 "powershell -NoProfile -Command \"(Get-AppxPackage -AllUsers | ? Name -eq 'OpenAI.Codex').Version\""
  ```
- **更新方法**: winget は id 指定で掴めない（「一致するインストール済みパッケージ無し」）。Store アプリの CLI 更新は MDM CIM `UpdateScanMethod` で Store 更新スキャンを発火（全 Store アプリ対象・async・ReturnValue=0 で成功）:
  ```powershell
  $o=Get-CimInstance -Namespace 'root\cimv2\mdm\dmmap' -ClassName 'MDM_EnterpriseModernAppManagement_AppManagement01'
  Invoke-CimMethod -InputObject $o -MethodName UpdateScanMethod
  ```
  もしくはコンソールで Microsoft Store → ライブラリ → 「更新プログラムを入手」。
- 🚧 **Windows Computer Use / Remote Connections の有効化は SSH 不可**: 2026-05-29 OpenAI が Windows 版 Codex Desktop App の Computer Use + Remote Connections を解禁（@seratch_ja）。有効化には GUI 操作・サインイン・OS 権限付与・ChatGPT モバイルとのペアリングが必要で、SSH は Session 0 隔離で GUI が出ないため不可。コンソール（物理 or RDP）で実施する。
- ⚠️ masu-p55 は**共有機**のため、AI に全画面制御を許す Computer Use の常時有効化は要検討（専用機のしゅん先生 PC の方が適切）。
- CLI の `codex remote-control` は Desktop App の Computer Use とは別機構の遠隔操舵（2026-05-30 時点で常駐稼働を確認、PID は再起動で変動）。

## WSL Ubuntu 24.04（2 用途併存、稼働中）

### ① Claude Desktop Code mode SSH 接続先
- 2222 ポート
- keepalive タスク稼働
- アーカイブ状態

### ② ~~Openclaw 実行環境~~ → **2026-06-02 削除済み**
- OpenClaw（`openclaw-gateway`、systemd user service `openclaw-gateway.service`、localhost:18789-18792 待受）は **2026-06-02 に完全削除**（停止＋無効化＋npm パッケージ削除＋`~/.openclaw` 削除＋.bashrc 行削除）。
- **復元用バックアップ**: `C:\Users\gci_admin\openclaw-backup.tar.gz`（112K、`~/.openclaw` 丸ごと）。
- Node.js v24.13.1（nvm 管理）は残置。
- WSL 側 Claude Code セッション保存: 2 件（4/17 / 4/18）

## 変更履歴

- 2026-06-02: **Codex 専用機に整理**。AI CLI 確認（claude 2.1.159 / codex 0.136.0 / gemini 0.44.1、すべて最新。Windows claude.exe も 2.1.159）。**OpenClaw 完全削除**（systemd user service `openclaw-gateway.service` 停止+無効化、npm `openclaw` 削除、`~/.openclaw` 削除、.bashrc 行削除。復元 backup = `C:\Users\gci_admin\openclaw-backup.tar.gz`）。**Antigravity（Google Gemini系IDE）アンインストール**（Inno `unins000.exe /VERYSILENT` ＋ user データ `~/.antigravity` 336M・`AppData\Roaming\Antigravity` 110M 削除、計~750MB 解放）。Whisper 検証残骸（uv/HFモデルキャッシュ/音声、~5.3G）削除。CLI `codex remote-control` は WSL2(Linux) で稼働＝Windows Codex Desktop と OS 分離で app-server 競合せず
- 2026-05-30: AI CLI 3 種を最新化（claude 2.1.156→2.1.157、codex 0.130.0→0.135.0、gemini 0.43.0→0.44.1）。**Codex Desktop App が Microsoft Store/MSIX 経由で導入済みと判明**（`OpenAI.Codex` v26.527.3378.0、`Get-AppxPackage` でのみ検出可）→ Store 更新スキャン発火（CIM `UpdateScanMethod` RV=0）。codex npm 更新で出た 224MB のステージング残骸（`.codex-0T2poKJG`、Defender がロック）を次回再起動で自動削除するワンショットタスク `CleanupCodexStaging`（SYSTEM/起動時、実行ログ `C:\Users\gci_admin\cleanup-codex-staging.log`）を登録。Windows Computer Use の有効化はコンソール操作が必要（SSH 不可）と確認
- 2026-05-18: Mac 側の Codex 添付画像を MASU-P55 の `C:\tmp\codex-remote-attachments` へ自動同期する LaunchAgent を追加。Windows 側 Codex が Mac と同じ `/tmp/codex-remote-attachments/...` 形式の画像パスで読めることを確認
- 2026-04-29: voice-stack 物理セットアップ完了（SuperWhisper v1.3.9 + Python 12 ファイル + ELEVENLABS_API_KEY 永続化、starter tier）、Claude Code v2.1.122 確認、ELEVENLABS_API_KEY を HKCU\Environment に永続化
- 2026-04-21: ハードウェア型番判明（HP ProBook、Intel Core i5）
- 2026-04-21: AVerMedia Assist Central Pro + OBS Studio 32.1.1 導入
- 2026-04-11: Tailscale 導入、Mac からの SSH 接続確立

## 関連ファイル

- 運用ルール: @docs/rules/operations.md
- GC313Pro セットアップ: @docs/gc313pro-user-guide-ja.md
