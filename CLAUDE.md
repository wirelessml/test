# プロジェクトコンテキスト

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

## 情報の保存方針

- **メモリ機能（`~/.claude/projects/*/memory/`）は使用しない**
- 情報はすべてgit管理のドキュメントに書く（他のデバイス・エージェントからも参照可能にするため）
- 会話記録: `conversation_log_YYYYMMDD.md`
- ナレッジ: `docs/` 配下
- プロジェクト情報・ユーザー情報: この `CLAUDE.md` に追記

## ユーザー情報

- MacBook Air — コワーキングオフィスに設置、メイン作業機
- iPhone 15 Pro（名前: 結花）— メインスマホ
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

## 操作上の注意

- computer-use操作時、アクセス許可リクエストを事前説明せず直接実行する
- Dispatchは使わない、CLIで完結させる
- ブラウザはcomputer-useでtier "read"（クリック不可）、URLを開くことはできるが再生・停止などの操作は不可
- 音量制御はosascriptで可能

## よく使うコマンド

```bash
# HTMLをPNGに変換（Playwright）
python docs/render_guide.py

# HTMLをブラウザでプレビュー
open *.html
```
