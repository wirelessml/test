## リモートコントロール状態報告

> ⚠️ **2026-06-05 注記（重要・2点）**
> 1. **この自作ルーチンは現在 無効/廃止状態**。remote-control 自体は 6/2 に廃止、cron（report.sh :33）は 6/4 夜に撤去、report.sh は macOS TCC で実行不能、`~/Desktop/screenshots/`（90枚・公開分含む）は 6/5 に削除済み。下記は履歴として残すのみ。
> 2. **🚨 `/rc` の名前衝突に注意**。ここでの「`/rc`」は本ルーチン（screencapture→GitHub Pages の*状況報告*、閲覧専用）の口頭ショートカット。一方 **Claude Code 本体には正式機能 `/remote-control`（短縮 `/rc`）が存在**（v2.1.53+、Pro/Max、claude.ai 中継でスマホから実セッションを操作。外からでも VPN/Tailscale 不要）。両者は**別物**。今後 `/rc` と言われたら、文脈が「状況報告」か「本物のリモコン切替」かを必ず確認すること。詳細 @docs/journal/2026-06-05.md

- 毎時33分にcronジョブで自動実行（セッション毎に再設定が必要）
- 内容: screencapture → log.json更新 → Gmail下書き作成 → git commit & push
- screencaptureコマンドを使用（computer-useのスクショはCursorがフィルタされるため不可）
- スクリーンショットは ~/Desktop/screenshots/ に保存
- GitHub Pages: https://wirelessml.github.io/test/
- **ネットワーク接続状況を毎回報告する**
  - Wi-Fi: `system_profiler SPAirPortDataType | grep -A5 "Current Network"` でSSID・周波数
  - YKSmas318 = コワーキングスペースWi-Fi（メイン）
  - rams502 = コワーキングスペースWi-Fi（バックアップ、パスワードは ~/.claude/local-notes/wifi.txt）
  - テザリング: `ifconfig en5 2>/dev/null` でiPhone USB接続確認
  - テザリング時はデバイス名も報告（結花=iPhone 15 Pro / 彩羽=iPad Pro 9.7）
  - 有線接続はなし（Wi-Fiかテザリングのどちらか）
  - **Wi-Fi切り替え後は /rc で接続状況を報告する**

