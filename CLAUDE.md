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

## よく使うコマンド

```bash
# HTMLをPNGに変換（Playwright）
python docs/render_guide.py

# HTMLをブラウザでプレビュー
open *.html
```
