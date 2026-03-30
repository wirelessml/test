# Microsoft Copilot / Frontier プログラム 調査レポート

## 調査日

2026年3月30日

## 結論

**個人利用では「時期尚早」。現在のMicrosoft 365 Personal + Claude Codeの組み合わせで運用するのが賢明。**

## 背景

Copilot Cowork（Microsoft版）のFrontier機能を試したいと考えたが、以下の理由で見送り。

## Copilot Pro の現状

- **Copilot Pro単体購入は廃止**されている
- 個人向け有料Copilot機能はMicrosoft 365プランに統合済み
- Frontier機能を使うにはPremium以上が必要

## プラン比較

| プラン | 年額（日本） | Copilot | Frontier |
|--------|------------|---------|----------|
| Microsoft 365 Personal（現在加入中） | ¥14,900/年 | 基本機能 | ❌ |
| Microsoft 365 Family | ¥27,400/年 | 基本機能 | ❌ |
| Microsoft 365 Premium | ¥21,300/年（初年度）→ ¥32,000/年 | 高度機能 | ✅ |
| E7バンドル（企業向け） | $99/ユーザー/月 | フル機能 | ✅ |
| GitHub Copilot | $10/月 | コード補完のみ | 別製品 |

## 判断基準

- **業務の複雑さ**: 複数アプリ横断で自律実行が本当に必要か
- **ガバナンス準備**: Entra/SharePoint/データ保護が整っているか
- **コスト許容度**: 高額ライセンスを正当化できるか

## リスク

- Frontier はResearch Previewで仕様が頻繁に変わる
- 英語・米国優先で日本語対応は限定的
- データアクセスのセキュリティ懸念

## 現在の環境で十分できること

Claude Code（Pro $20/月）+ Microsoft 365 Personal で以下が可能：

- Claude Code CLI でのコーディング・自動化
- Dispatch / Cowork（テキストタスク）
- MCP連携（Slack, Gmail, Google Calendar）
- Git経由のクラウド⇔ローカル連携
- スマホからSSHでリモート操作
- MacBook Air M1 到着後はComputer Useも可能

## 推奨アクション

1. **現在はPersonalのまま待つ** — Frontier機能が正式版で降りてくる可能性あり
2. **Claude Code環境を充実させる** — MCP連携やSKILL.mdの整備に注力
3. **MacBook Air M1でComputer Useを試す** — macOS限定機能を活用
4. **Frontier正式リリース時に再検討** — 価格・機能が安定してから判断
