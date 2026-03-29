# Claude Code 実行環境 - マシンスペック

## 概要

Claude Codeを運用しているマシンのスペック情報。

## PCスペック

| 項目 | 詳細 |
|------|------|
| 機種 | HP ProBook 450 15.6 inch G9 Notebook PC |
| OS | Windows 11 Pro (Build 26200) |
| CPU | Intel Core i5-1235U（第12世代）/ 10コア12スレッド |
| RAM | 8GB DDR4-3200 (Samsung) |
| ストレージ | SK hynix BC711 256GB NVMe SSD |
| GPU | Intel UHD Graphics（内蔵） |
| ホスト名 | MASU-P55 |

## Claude Code の利用環境

### 利用モード

- **コードタブ（CLI直接）** — リアルタイムに応答が見える。すぐ返事が欲しいときに最適
- **Dispatchタブ（バックグラウンド）** — タスクを投げて後で確認するモード。応答は「バックグラウンドタスクを表示」から確認が必要
- **スマホ（メッセージ経由）** — Dispatch経由でスマホからもタスクを送れる

### クラウド版との連携

- クラウド側のClaude Code（Web版）とは **Gitリポジトリ経由で間接連携** が可能
- 直接通信する仕組みはなく、`git push` / `git pull` でファイルを共有する
- `CLAUDE.md` をリポジトリに置くことで、どちらのClaude Codeでも同じ指示に従える
- 連携テスト済み（2026年3月29日）

### Dispatchの注意点

- Dispatchの応答はバックグラウンドで処理されるため、チャット画面に直接表示されない
- 結果を見るには「バックグラウンドタスクを表示」をクリックする必要がある
- メニューから「メモリをクリア」「会話を削除」「バックグラウンドタスクをクリア」も可能

### 使用モデル

- Opus 4.6 を使用中
- Opusは使用制限の消費が早いため、軽いタスクはSonnetへの切り替えも検討

### MCP接続状況（2026年3月29日）

| サービス | 状態 |
|---------|------|
| Slack | ✅ connected |
| Gmail | ✅ connected |
| Google Calendar | ✅ connected |
| マネーフォワードクラウド | ❌ failed |
| Discord | ❌ failed |
| Telegram | ❌ failed |

### アクセス方法

- **PC直接操作** — HP ProBookのClaude Code（コードタブ / Dispatch）
- **スマホからSSH接続** — リモートコントロールでCLI操作可能
- **クラウド版（Web）** — Git経由で間接連携

### Claude Code バージョン

- v2.1.86（現在インストール済み）
- Claude Pro プラン
- v2.1.87 がリリース間近（2026年3月29日時点、@ClaudeCodeLog が予告）

### v2.1.86 の主な変更点

- Claude Opus 4.6のデフォルト最大出力トークンを64kトークンに増加
- Opus 4.6 / Sonnet 4.6の上限を128kトークンに引き上げ
- `--resume` のバグ修正（v2.1.85以前のセッション再開時のエラー）

### 最近のアップデート（2026年3月）

- `--bare` フラグ追加（スクリプト用にフック等をスキップ）
- `--channels` パーミッションリレー（スマホへの承認転送）
- MCP elicitationサポート（MCPサーバーがタスク中に対話的な入力を要求可能に）
- `-n` / `--name` フラグ（セッションに名前をつける）
- PowerShellツール（Windows向け、プレビュー）

### インストール済みプラグイン（2026年3月29日）

マーケットプレース `anthropic-agent-skills` を追加し、以下をインストール：

- **document-skills** — ドキュメント関連スキル
- **example-skills** — サンプルスキル集

リロード後の状態：

| 項目 | 数 |
|------|-----|
| plugins | 5 |
| skills | 5 |
| agents | 5 |
| hooks | 0 |
| plugin MCP servers | 3 |
| plugin LSP servers | 0 |

## 注意事項（HP ProBook）

- RAM 8GBでメモリ使用率がかなり高い状態（利用可能 629MB）になることがある
- 作業中はメモリ消費に注意が必要
- ビジネス向けノートPCのため、重い処理には向かない

---

## MacBook Air M1（2台目・発注済み）

### スペック

| 項目 | 詳細 |
|------|------|
| 機種 | MacBook Air M1 (2020) ゴールド |
| チップ | Apple M1 |
| メモリ | 8GB ユニファイドメモリ |
| ストレージ | 256GB SSD |
| ディスプレイ | 13.3インチ Retina (2560x1600) |
| ポート | Thunderbolt (Type-C) x2 |
| 価格 | ¥33,700（送料込み・メルカリ整備品） |
| 購入日 | 2026年3月29日 |

### 注意事項

- **スクリーンの90%が表示不可**（整備品・画面不具合あり）
- **外部ディスプレイ必須**で運用する前提
- 本体自体はきれいな状態
- 純正アダプター・ケーブル・化粧箱付き

### 導入目的

- **Computer Use（画面操作）** — macOS対応なのでHP ProBook（Windows）ではできなかった機能が使える
- **macOS版Cowork** — フル機能が利用可能
- **Claude Code** — ターミナル動作なので外部ディスプレイがあれば問題なし

### HP ProBook vs MacBook Air 役割分担

| 機能 | HP ProBook (Windows) | MacBook Air M1 (macOS) |
|------|---------------------|----------------------|
| Claude Code CLI | ✅ | ✅ |
| Cowork（テキスト） | ✅ | ✅ |
| Computer Use（画面操作） | ❌ 未対応 | ✅ 対応 |
| Dispatch | ✅ | ✅ |
| MCP連携（Slack等） | ✅ | ✅ |

## 記録日

2026年3月29日
