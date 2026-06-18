# Windows PC (MASU-P55)

> Last updated: 2026-06-19

## 役割

**コワーキングオフィス サブ作業機 ＝ Claude（Mac）の委譲先 Codex ワーカー**
- 配置: コワーキングスペース据え置き
- 主用途: **Claude のサポートに徹する Codex 実行機**（2026-06-12 役割転換）。独立した自走エージェント（旧: job-search / remote-control / OpenClaw 等）としては運用しない。**WSL2 の Codex CLI を、Mac の Claude が `codex exec` で叩いて重い作業（コードレビュー・監査・文字起こし・大量調査）を委譲**する。印刷・スキャン・ネット検索の物理用途は継続
- 委譲の標準手順とハマりどころ: **@skills/delegating-to-masup-codex/SKILL.md**
- 所属: コワーキング設置（一部共用）
- ⚠️ 旧「Codex 専用機（独立運用）」ポリシー（6/2）は **6/12 に「Claude のサポート役」へ更新**。masup 上で Codex が自分の判断で本番タスク（求人サーチ等）を回すことはしない（6/10 に job-search は Mac へ移管済み、6/12 にゾンビ watchdog 無効化済み）

## ハードウェア

- **モデル**: HP ProBook（Intel Core i5）（4/21 判明）

## OS / ソフトウェア

- OS: Windows 11 Pro（build 26200、2026-06-13 実測。LastBootUpTime 2026-06-10 06:08:37）
- RAM: 8GB（2026-06-13 実測: 空き約1.35GB）
- C: 空き約74.9GB（2026-06-13 実測）
- Claude Code v2.1.181（`C:\Users\gci_admin\.local\bin\claude.exe`、standalone binary **単一**、毎日 0:00 タスク `Claude Code Update` が `claude.exe update` で最新化。config install method=native）。⚠️ 2026-06-19 に npm-global `@anthropic-ai/claude-code` 重複（PATH を先取りしていた）を撤去し standalone 単一化。**claude は npm で入れない**（Mac も同様＝npm globals に claude 無し。`@anthropic-ai` localhost ガードは Mac・masup とも未設定＝「入れない」運用で統一）
- Codex CLI v0.141.0（WSL2 Ubuntu 24.04.4 LTS 側 npm `@openai/codex`。Mac から `ssh masu-p55 "wsl -e bash -lc \"codex --version\""` で確認）。⚠️ 2026-06-19 に Windows-native npm codex（0.140.0、壊れた Windows remote-control 専用だった）を撤去し WSL2 単一に。`codex exec` 委譲先はこの WSL2 版
- Gemini CLI v0.47.0（Windows 側 npm `@google/gemini-cli` global）
- **Codex Desktop App v26.609.4994.0（Microsoft Store / MSIX、`OpenAI.Codex`）** — `Get-AppxPackage -AllUsers` では旧 v26.609.3341.0 も併存表示。詳細は下記「Codex Desktop App」セクション
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

- **発見: 2026-05-30**。`OpenAI.Codex` が **Microsoft Store (MSIX) 経由**で導入済み（2026-06-13 実測の最新表示 v26.609.4994.0、x64、PackageFullName `OpenAI.Codex_26.609.4994.0_x64__2p2nqsd0c76g0`）。CLI（npm `@openai/codex`）とは別物の GUI アプリ。
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
- CLI の `codex remote-control` は Desktop App の Computer Use とは別機構の遠隔操舵。**2026-06-19 時点: WSL2 版のみ維持＝稼働中**（task `CodexWSLRemoteControl` → `~/.codex/start-wsl-remote-control.cmd` → `wsl ... codex remote-control start`、PID は再起動で変動）。**Windows-native 版（task `codex-remote-control` → `C:\ProgramData\codex-watchdog\run-codex-remote.bat`）は codex 0.131+ で Windows サポートが壊れていたため 6/19 にタスク・CLI とも撤去**（ユーザー判断「WSL2版は残す」）。詳細は変更履歴 2026-06-19。

## WSL Ubuntu 24.04（2 用途併存、稼働中）

- 2026-06-19 実測: Ubuntu 24.04.4 LTS、Codex CLI 0.141.0
- 現在の主用途は、Mac 司令塔からの `codex exec` 委譲先。Windows 側の GUI アプリや本番ジョブとは切り離して考える

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

- 2026-06-19: **AI CLI 更新 ＋ 二重インストール/旧remote-control の大掃除**。①3CLI を更新（claude standalone 2.1.179→2.1.181 / WSL2 codex →0.141.0 / Windows gemini 0.46.0→0.47.0）。②**claude 重複撤去**: npm-global `@anthropic-ai/claude-code` を uninstall し standalone（`.local\bin`）単一化、config install method を native へ正常化（SSH 越し `claude update` が一時 global に書換えていたのを是正）。③**codex Windows-native（npm 0.140.0）撤去**: 委譲は WSL2 codex を使うため Windows 側 CLI は不要。残るは WSL2 0.141.0 のみ。④**旧 remote-control 整理**（ユーザー判断「WSL2版は残す」）: 壊れた Windows 版 task `codex-remote-control` を削除、無効ゾンビ task `codex-watchdog` を削除、`C:\ProgramData\codex-watchdog\` を `C:\Users\gci_admin\codex-watchdog-removed-20260619\` へ退避。**稼働中の WSL2 remote-control（task `CodexWSLRemoteControl`、PID 148367 `codex app-server --remote-control`）は意図的に温存**。⑤発見: `@anthropic-ai` localhost ガードは Mac・masup とも未設定（スキル updating-ai-cli-fleet の「3台統一済み」記述は実態と相違＝要修正）。Mac/masup とも「claude を npm で入れない」運用で統一。検証: `where claude`=standalone のみ / `where codex`(Win)=なし / WSL2 remote-control 稼働継続 / 残存タスク=`Claude Code Update`+`CodexWSLRemoteControl` のみ
- 2026-06-13: 実機照合で OS / AI CLI / Codex Desktop App を更新。Windows 11 Pro build 26200、Claude Code 2.1.176、Gemini 0.46.0、WSL Ubuntu 24.04.4 LTS 側 Codex 0.139.0。C: 空き約74.9GB、RAM空き約1.35GB。`Get-AppxPackage -AllUsers` で `OpenAI.Codex` v26.609.3341.0 と v26.609.4994.0 が併存表示され、最新は v26.609.4994.0
- 2026-06-12: **役割を「Claude の委譲先 Codex ワーカー」へ転換**（ユーザー指示「今後 masup Codex はあなたのサポートに徹してもらう」）。独立自走をやめ、Mac の Claude が `codex exec` で重い作業を投げる subagent 的位置づけに。同日この体制で実証＝コードレビュー 3 本（takeru-video-editor / job-search-daily / takeru-chatbot セキュリティ）を委譲→Claude 検証→反映。委譲パターンをスキル化（@skills/delegating-to-masup-codex/）。実証で判明したハマり: ①codex exec `--sandbox workspace-write` は cwd 外（/mnt/c）に書けない→ワークスペース or ホーム直下に書かせ shell で回収 ②macOS tar が `._*`（AppleDouble）を混入させる→`COPYFILE_DISABLE=1` ③stdout は実行ログ全部入りで巨大→末尾の成果物だけ回収
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
