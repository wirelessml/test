# scripts/archive — 退役スクリプト置き場

> 2026-06-12 の棚卸しで「再利用価値はあるが現役参照なし」と判定された 16 件を収容（経緯と全分類: @docs/projects/scripts-audit-2026-06-12.md）。
> 現役スクリプトは `scripts/` 直下。ここのものを再利用する時はパス・バージョン前提（claude のバージョン番号等）を確認してから。

| ファイル | 元用途 |
|---|---|
| browser-automation/ | しゅん先生 PC で Playwright を動かす手順書+疎通テスト |
| doda/ | doda 職務経歴書・写真アップロード自動化（就活） |
| codex-tui-pets-pr-watch.sh | Codex TUI pets PR #21206 マージ監視（5/7 仕込み） |
| conductor-typing-autobot.js | Conductor Studio タイピング自動入力 |
| generate-shibu-pet-sprite.py | Codex Pet しぶ風スプライト生成（5/7） |
| install-noto-defaults*.ps1 ×3 | Windows 既定フォント Noto Sans JP 化（5/6、段階版） |
| install-pretendard-jp.ps1 | Pretendard JP フォント導入（5/6） |
| update-claude-win.ps1 / -145.ps1 | Windows claude.exe の GitHub release 強制更新（`$ver` 書換えで再利用可） |
| install-codex-appserver-shun.ps1 | しゅん先生 PC への AppServer task 登録（※実際は未設置のまま終了、5/8 訂正参照） |
| xinput-dump.ps1 | XInput コントローラ入力の診断表示 |
