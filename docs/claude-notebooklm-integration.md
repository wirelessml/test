# Claude Code × NotebookLM 統合（MCP経由の無限記憶）

## 出典
- 動画: https://youtu.be/vByAJJUSHu8
- チャンネル: Generative AI and InfoBusiness Institute

## 課題と解決

### Claudeの「健忘症」問題
- 各セッションが断絶、過去の文脈を維持できない
- 毎回膨大なドキュメントを再入力 → コンテキストウィンドウ浪費
- トークン課金の増大

### 解決策: NotebookLMを外部脳として接続
- GoogleのNotebookLMをClaudeの長期記憶として利用
- MCP（Model Context Protocol）で接続
- 「ほぼ無限の長期記憶」+「ゼロトークンコストでの大規模コンテキスト処理」

## 技術構成

### MCPサーバー
- パッケージ: `notebooklm-mcp-cli`（GitHub公開）
- CLI: `nlm` コマンド
- MCPサーバー: `notebooklm-mcp`
- 接続先: Claude Desktop / Claude Code / Cursor

### 35種類のツール（抜粋）
- **ノートブック/ソース管理**: notebook_list, notebook_create, source_add（URL/Text/Drive/File対応）
- **AI分析・検索**: notebook_query（RAG）, cross_notebook_query, research_start（Web/Driveディープリサーチ）
- **コンテンツ生成**: studio_create（Podcast, Video, Infographic等）, studio_revise, download_artifact

## 戦略的価値

1. **長期記憶**: 会話内容を「デジタル脳」として保存、過去の文脈を維持
2. **コスト削減**: Googleの無料リソースで処理、トークンコスト大幅削減
3. **リサーチ自動化**: Web/Driveディープリサーチを自律実行
4. **コンテンツ生成**: Podcast・動画・インフォグラフィックを自動生成
5. **エージェント・オーケストレーション**: 単一モデルのプロンプトから複数AIツール連動へ

## 現在の自分の運用との比較

| 項目 | 現在（CLAUDE.md + git） | NotebookLM統合 |
|------|------------------------|----------------|
| 永続化 | gitでMarkdown管理 | NotebookLMに自動保存 |
| 検索 | ファイル名・grep | RAG（意味検索） |
| 他デバイス参照 | git pull | Google経由で自動同期 |
| コスト | 無料 | 無料（Google） |
| セットアップ | CLAUDE.md書くだけ | MCP設定が必要 |
| コンテンツ生成 | なし | Podcast・動画・画像自動生成 |

### 検討ポイント
- 現在のgit管理は十分機能しているが、RAG検索がないのが弱点
- NotebookLM統合はRAG + コンテンツ生成が強み
- 両方併用も可能（gitで永続化 + NotebookLMでRAG検索）
