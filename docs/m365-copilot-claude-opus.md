# Microsoft 365 Copilot Chat で Claude Opus 4.6 が利用可能

- **確認日**: 2026/04/14
- **URL**: https://m365.cloud.microsoft/chat

## 利用可能モデル（M365 Copilot Chat）

### Claude（Anthropic）
- **Claude Opus 4.6** — Coworkエージェント経由で選択可能
- Claude Sonnet 4.6

### GPT（OpenAI）
- GPT 5.4 Think Deeper
- GPT 5.3 Quick Response
- GPT 5.2 Quick Response / Think Deeper

### モード
- **自動** — 考える時間の長さを自動決定（デフォルト）
- **Quick Response** — すぐに回答
- **Think Deeper** — より良い回答のために長く考える
- **Opus** — Claude Opus 4.6

## 選び方
1. M365 Copilot Chat（https://m365.cloud.microsoft/chat）を開く
2. 右上の「自動 ▼」ドロップダウンをクリック
3. 「Opus - Claude」を選択

## 料金・プランの区別（重要）

| プラン | 料金 | Claude Opus | GPT-5.4 | Officeアプリ内Copilot |
|--------|------|-------------|---------|---------------------|
| **Copilot Chat (Basic)** | 無料（M365契約者） | Cowork経由で利用可 | ？ | なし |
| **Microsoft 365 Copilot** | 月$30/ユーザー（購入必要） | Excel等のエージェントで選択可 | 利用可 | Word/Excel/PPT内で利用可 |

- **無料のCopilot Chat**と**有料のMicrosoft 365 Copilot**は別物
- PowerPoint内でClaude Opus 4.6でスライド生成 → **有料版（Microsoft 365 Copilot）**
- Excel内のエージェントでOpus選択 → **有料版**
- GPT-5.4 Think Deeper → **有料版（個人版でも利用可）**
- 有料版はじわじわと機能追加中（2026年4月時点）

## claude.ai側のM365コネクタ
- **2026/04/14時点**: まだロールアウトされていない（検索しても表示されず）
- Anthropicが「すべてのClaudeプランで利用可能」と発表済み
- Outlook、OneDrive、SharePointを接続予定
- 設定URL: https://claude.ai/customize/connectors
- 利用可能なコネクタ（現時点）: GitHub, Gmail, Google Calendar, Google Drive, マネーフォワードクラウド

## Copilot Studio — Claude がプライマリモデルとしてGA

- **確認日**: 2026/04/14
- **公式ドキュメント**: https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-select-primary-model
- Claude Sonnet 4.6 / Claude Opus 4.6 が**プライマリAIモデル**として一般提供（GA）
- エージェント全体のメインAIとしてClaudeを選択可能（モード切替ではなく、エージェントの根幹モデル）
- GPT-4.1（デフォルト）、GPT-5、Claude Sonnet 4.5/4.6、Claude Opus から選択
- GCC（米国政府クラウド）環境では非対応

### Copilot Studio 概要
- 旧Power Virtual Agentsの後継、ローコードAIエージェント構築プラットフォーム
- URL: https://copilotstudio.microsoft.com
- 自然言語でエージェント自動生成、Power Automate連携、MCPサーバー接続
- Teams/SharePoint/Web/WhatsApp等へ展開可能

### Copilot Studio 料金
| プラン | 価格 | 内容 |
|--------|------|------|
| プリペイドパック | $200/月 | 25,000クレジット/パック |
| 従量課金 | 使用量に応じて | Azure課金 |
| M365 Copilotライセンス付帯 | 追加費用なし | 社内チャネル限定 |
| 試用版（バイラル試験版） | 無料 | 作成・テストのみ、公開不可 |

## 意義
- MicrosoftがAnthropicモデルを公式採用（OpenAI独占からの脱却）
- 双方向統合: M365→Claude（Cowork）+ Claude→M365（コネクタ、近日）
- 同一UI内でGPTとClaudeを切り替え比較可能
- Copilot StudioでエージェントのプライマリモデルとしてClaude Opus選択可能
