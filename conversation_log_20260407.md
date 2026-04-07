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

## --dangerously-skip-permissions について
- Xの投稿で `claude --dangerously-skip-permissions` の紹介を見た
- 全承認をスキップするため非推奨
- より安全な代替手段: `claude --enable-auto-mode`（安全性チェック付き自動承認）、セッション中にShift+Tabでモード切替

## Microsoft 365 インストール
- Homebrewは未インストール、管理者権限あり
- microsoft.comから直接ダウンロード（curl、約2.6GB）
- ダウンロード途中で切断（75%）→ curl -C - で再開して完了
- sudo installer はパスワード入力が必要なためGUIインストーラーを起動（open コマンド）
- ユーザーのパスワード入力待ち

## App Store / Final Cut Pro
- App Storeを開いてFinal Cut Proを検索
- AssistiveControlが画面全体に重なりクリック不可 → キーボード操作（Cmd+F）で検索成功
- 「App Storeに接続できません」エラーが一時的に発生（Returnキーで解消）
- 検索結果: Final Cut Pro（Mac版、レビュー1.6万件）と Final Cut Pro: ビデオ制作（iPad版）
- Mac版（左上の方）を推奨
- インストールはApple ID認証が必要なためユーザーが操作

## チャレンジタッチ用ケーブル
- munesada.comの記事からケーブルを特定
- Access Mini USB 延長ケーブル（25cm）Mini-B メス → USB A オス、OTG対応
- Amazon: https://www.amazon.co.jp/dp/B08R5MQMHX
- 購入はユーザー自身で行う必要あり

## ネットワーク変更
- Wi-Fiから変更、iPad Pro「彩羽」（楽天SIM）のUSBテザリングで接続
- その後iPhone「結花」（iPhone 15 Pro）のテザリングに切り替え
- Network Analyzerで確認:
  - iPhone（172.20.10.1）— 結花（ゲートウェイ）
  - MACBOOKAIR-FD33（172.20.10.3）— MacBook Air
  - Nintendo Co.,Ltd（172.20.10.5）— Nintendo Switch

## デバイス情報
- MacBook Air — コワーキングオフィスに設置
- iPhone 15 Pro（名前: 結花）— メインスマホ
- 初代iPad Pro 9.7インチ（名前: 彩羽）— 楽天SIM挿入、テザリング用
- Nintendo Switch — 同じネットワークに接続

## リモートコントロール状態報告の実行記録（4/7）
- 03:42, 03:46, 04:46, 05:46, 06:46, 08:18, 08:47, 09:47, 10:47, 11:47, 12:46, 13:46, 14:46, 15:46, 16:46, 17:46
