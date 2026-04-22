# Windows PC (MASU-P55)

> Last updated: 2026-04-22

## 役割

**コワーキングオフィス サブ作業機**
- 配置: コワーキングスペース据え置き
- 主用途: サブ Windows 機、印刷・スキャン・ネット検索、WSL Ubuntu 上で OpenClaw 実行
- 所属: コワーキング設置（一部共用）

## ハードウェア

- **モデル**: HP ProBook（Intel Core i5）（4/21 判明）

## OS / ソフトウェア

- OS: Windows（バージョン詳細未記録）
- Claude Code v2.1.116（`C:\Users\gci_admin\.local\bin\claude.exe`、4/21 08:52 自動更新、毎日 0:00 タスクスケジューラで最新化）
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

## WSL Ubuntu 24.04（2 用途併存、稼働中）

### ① Claude Desktop Code mode SSH 接続先
- 2222 ポート
- keepalive タスク稼働
- アーカイブ状態

### ② Openclaw（OpenAI Codex ベース AI エージェント CLI）実行環境
- 4/21 09:02 に update-check 実行、**アクティブ運用中**
- Node.js v24.13.1（nvm 管理、Openclaw 依存）
- WSL 側 Claude Code セッション保存: 2 件（4/17 / 4/18）

## 変更履歴

- 2026-04-21: ハードウェア型番判明（HP ProBook、Intel Core i5）
- 2026-04-21: AVerMedia Assist Central Pro + OBS Studio 32.1.1 導入
- 2026-04-11: Tailscale 導入、Mac からの SSH 接続確立

## 関連ファイル

- 運用ルール: @docs/rules/operations.md
- GC313Pro セットアップ: @docs/gc313pro-user-guide-ja.md
