# プロジェクトコンテキスト

> 目標: 200-300 行。肥大化したら `claude-md-diet` スキルで再度分解。

## 現在の状態 (最重要、最初に目を通すセクション)

<!-- 直近 1-2 週間のアクティブな状況。週次で更新 -->

- **メイン作業機**: <例: M1 MacBook Air は持ち運び用、しゅん先生 PC がコワーキング据え置きメイン>
- **進行中プロジェクト**: <例: しぶエコ観察、Substack 連載、Ollama ローカル LLM 実験>
- **直近の重要イベント**: <例: 2026-04-22 Plextor SSD 死亡 → Seagate HDD 延命運用中>
- **今週の優先 TODO**: 
  - [ ] <具体タスク 1>
  - [ ] <具体タスク 2>
  - [ ] <具体タスク 3>

## 機材 (1 行サマリー、詳細は @docs/machines/)

- **<マシン名 1>**: <1 行の役割と現状>（詳細: @docs/machines/<hostname1>.md）
- **<マシン名 2>**: <1 行の役割と現状>（詳細: @docs/machines/<hostname2>.md）
- **<マシン名 3>**: <1 行の役割と現状>（詳細: @docs/machines/<hostname3>.md）

## 運用ルール (AI が従うべき核ルール、常時有効)

- <例: 読んでいないコードは変更するな>
- <例: 複雑なタスクでは十分に調査してから行動する>
- <例: サブエージェントの成果物は必ず自分で検証する>
- <例: 記事の削除や一括更新をする前は件数を確認>
- <例: 金銭トランザクション（発注・送金・取引）は代行しない>

詳細な操作規約: @docs/rules/operations.md

## 情報の保存方針

- メモリ機能は使用しない
- 情報はすべて git 管理のドキュメントに書く
- 会話中の知見は毎回 git に保存
- ナレッジ: `docs/` 配下、プロジェクト情報・ユーザー情報: この `CLAUDE.md`

## 最近の完了 (過去 2 週間のサマリー、詳細は journal/)

- **YYYY-MM-DD**: <1 行サマリー> (@docs/journal/YYYY-MM-DD.md)
- **YYYY-MM-DD**: <1 行サマリー> (@docs/journal/YYYY-MM-DD.md)
- **YYYY-MM-DD**: <1 行サマリー> (@docs/journal/YYYY-MM-DD.md)

2 週間より古い完了記録: @docs/archive/

## 定期ルーチン

運用中のルーチン一覧: @docs/routines/index.md

- <例: X 情報収集 (各セッション毎)>: @docs/routines/x-daily-briefing.md
- <例: セッションスケジュール>: @docs/routines/session-schedule.md
- <例: SSD 価格監視 (毎週月曜)>: @docs/routines/ssd-price-monitor.md

## 期限・リマインダー

全期限リスト: @docs/reminders.md

次の 2 週間の重要期限:
- YYYY-MM-DD: <要約>
- YYYY-MM-DD: <要約>

## 個別プロジェクト

- <例: AIミニマリストしぶ>: @docs/projects/shibu.md
- <例: Substack 連載>: @docs/projects/substack.md
- <例: しぶチャットボット>: @docs/projects/shibu-chatbot.md

## Claude Code セッション運用

- モデル: `/model opusplan` でセッション開始時
- 週次使用量: `/usage` or StatusLine で確認
- セッションスケジュール詳細: @docs/routines/session-schedule.md

## 参照

- @docs/rules/ — 操作規約・セキュリティ・コーディング規約
- @docs/machines/ — 機材詳細
- @docs/journal/ — 日次作業ログ
- @docs/routines/ — 定期タスク
- @docs/reminders.md — 期限リスト
- @docs/projects/ — 個別プロジェクト
- @docs/adr/ — 重要判断記録 (Architecture Decision Record)
- @docs/archive/ — 古い完了記録の月次まとめ
