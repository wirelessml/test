# Claude Code × Slack 連携ガイド（MCP Server）

## 概要

Claude CodeからSlackのメッセージを読み書きできるようにする設定手順。
Slack公式のMCPサーバーを利用する。

## できること

- チャンネルのメッセージを検索・閲覧
- スレッドの内容を取得
- メッセージの送信
- ファイルの検索
- ユーザープロフィールの取得
- Canvasの読み書き

## セットアップ手順

### Step 1: Slack Appの作成

1. https://api.slack.com/apps にアクセス
2. 「Create New App」→「From scratch」を選択
3. App名を入力（例: `Claude MCP`）
4. 対象のワークスペースを選択
5. 「Create App」をクリック

### Step 2: 権限（Scopes）の設定

左サイドバーの「OAuth & Permissions」→「User Token Scopes」に以下を追加：

| 機能 | 必要なScope |
|------|------------|
| メッセージ検索 | `search:read.public`, `search:read.private`, `search:read.mpim`, `search:read.im` |
| ファイル検索 | `search:read.files` |
| ユーザー検索 | `search:read.users` |
| メッセージ送信 | `chat:write` |
| チャンネル履歴 | `channels:history`, `groups:history`, `mpim:history`, `im:history` |
| Canvas操作 | `canvases:read`, `canvases:write` |
| ユーザー情報 | `users:read`, `users:read.email` |

### Step 3: Client IDとClient Secretの取得

1. 「Basic Information」ページで **Client ID** と **Client Secret** をコピー

### Step 4: Claude Codeに設定を追加

`~/.claude/settings.json` に以下を追加する：

```json
{
  "mcpServers": {
    "slack": {
      "type": "http",
      "url": "https://mcp.slack.com/mcp",
      "auth": {
        "type": "oauth",
        "clientId": "ここにClient IDを入力",
        "clientSecret": "ここにClient Secretを入力",
        "scopes": [
          "search:read.public",
          "search:read.private",
          "search:read.mpim",
          "search:read.im",
          "search:read.files",
          "search:read.users",
          "chat:write",
          "channels:history",
          "groups:history",
          "mpim:history",
          "im:history",
          "canvases:read",
          "canvases:write",
          "users:read",
          "users:read.email"
        ]
      }
    }
  }
}
```

### Step 5: 認証

1. Claude Codeを再起動
2. Slackの認証画面が表示される
3. 「許可する」をクリック
4. 以降、Claude CodeからSlackの操作が可能になる

## 動作確認

設定後、Claude Codeに以下のように聞いてみる：

```
Slackの#generalチャンネルの最新メッセージを表示して
```

## トラブルシューティング

- **認証エラー**: Client IDとClient Secretが正しいか確認
- **権限エラー**: Slack App側のScopesが不足していないか確認
- **接続できない**: Claude Codeを再起動してみる
- **ワークスペース管理者の承認が必要**: 管理者にアプリのインストールを承認してもらう

## 参考リンク

- Slack MCP Server公式ドキュメント: https://docs.slack.dev/ai/slack-mcp-server/
- Claude Code MCP設定ドキュメント: https://code.claude.com/docs/en/slack

## 記録日

2026年3月29日
