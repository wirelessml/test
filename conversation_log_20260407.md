# 会話記録 2026-04-07

## Cursorの画面が真っ黒
- Cursorを開いた状態でcomputer-useのスクリーンショットを撮ると真っ黒に見えた
- ログ確認の結果、致命的なエラーはなし
  - `[error] No bundle location found for extension ...` — 複数のCursor内蔵拡張で出るが、直後に全て「activated success」で正常動作
  - `[warning] API proposal DOES NOT EXIST` — 古いAPI参照、機能には影響なし
  - `[DEP0040] punycode module is deprecated` — Node.js非推奨警告、無害
  - main.log: 前回セッションも正常終了（exit code: 0）
- `screencapture`コマンドで撮ったスクリーンショットは正常に映っていた
- 原因: computer-useのスクリーンショットフィルタリング（CursorはIDE tier "click" のため描画が制限される）
- 結論: Cursor自体は正常に動作している

## リモートコントロール状態報告の再設定
- 前回セッション（4/5）で設定したcronジョブ（毎時スクリーンショット + Gmail下書き + git push）が停止していた
- 最後のスクリーンショットコミット: 4/6 16:33
- 前回の設定内容をgitの会話記録（conversation_log_20260405.md）から確認
- 同じ内容でcronジョブを再設定
  - ジョブID: 75098245
  - スケジュール: 毎時33分
  - 内容: screencapture → log.json更新 → Gmail下書き作成 → git commit & push
  - 有効期限: 7日間（セッション終了時にも停止）

## スクリーンショットをGitHub Pagesに追加
- 手動撮影した screenshot_20260407_031800.png を log.json に追加
- git push して https://wirelessml.github.io/test/ に反映

## 過去セッションのドキュメント確認
- docs/claude-computer-use-guide.md を確認
- docs/claude-code-tips-2025.md の Computer Use 関連セクションを確認
  - Computer Use: 動的・探索的作業向け（画面を見て判断）
  - pyautogui: 定型繰り返し作業向け（座標固定、高速）
  - dev-browser (Playwright): DOM操作ベースで高速・正確
  - 設計原則: 定型操作はコード化、LLMは例外処理係に徹させる
- 今回のスクショ問題の教訓: screencaptureコマンド（定型）の方がcomputer-useスクショ（フィルタリング制約あり）より確実

## セッション履歴の確認
- ~/.claude/history.jsonl にユーザー入力コマンドのみ記録されている（Claudeの応答は含まれない）
- 過去10セッション分の入力履歴を確認
- 会話の全文を残すには conversation_log_*.md に手動記録してgit保存が確実
