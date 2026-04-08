# Chrome DevTools MCP — 技術知見

## 本質

「APIがないサービス」にもClaude Codeは接続できる。
ChromiumベースのアプリならChrome DevTools Protocol経由でDOMを読み書きできる。

## 仕組み

1. ChromiumベースのアプリがDevTools Protocolを公開
2. Chrome DevTools MCPがプロトコル経由で接続
3. Claude CodeがDOM読み取り・JS実行・操作を行う

## 実用事例

### TradingView（Pine Script自動生成）
- TradingViewデスクトップ版はChromiumで動いている
- Chrome DevTools Protocol経由で接続
- Claude Codeがチャートを読む
- Pine Scriptを自動生成
- コンパイル→エラー修正まで全自動

### CyberAgent/Ameba（ランタイムエラー検知）
- Storybook上の目視確認ループを自動化
- DevToolsでランタイムエラーを検知
- 1時間で回るようになった
- 地味な運用の置き換えで効く

### 我々の活用（YouTubeコミュニティ投稿）
- WebFetchではJSレンダリングコンテンツが取得不可
- Playwright + Chromiumで動的コンテンツを取得成功
- セッション再起動なしでBash経由で実行

## 対応可能なアプリ（Chromiumベース）
- Google Chrome / Brave / Edge
- TradingView（デスクトップ版）
- Electronアプリ（Cursor, Slack, Discord, VS Code等）
- Storybook
- その他Chromiumベースのアプリ全般
