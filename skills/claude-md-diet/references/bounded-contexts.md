# よくある Bounded Context と切り出し方

## 判定フローチャート

```
ある情報を CLAUDE.md に書こうとしている
    ↓
Q1: これは現在進行中のこと？
    Yes → CLAUDE.md の「現在の状態」セクション
    No  → Q2

Q2: これは完了した作業記録？
    Yes → docs/journal/YYYY-MM-DD.md (今日分)
    No  → Q3

Q3: これは特定のマシンに関する詳細？
    Yes → docs/machines/<hostname>.md
    No  → Q4

Q4: これは定期タスクの定義？
    Yes → docs/routines/<name>.md
    No  → Q5

Q5: これは期限・日付のある予定？
    Yes → docs/reminders.md
    No  → Q6

Q6: これは重要な判断・決定？
    Yes → docs/adr/NNNN-<topic>.md
    No  → Q7

Q7: これは特定プロジェクトの詳細？
    Yes → docs/projects/<project>.md
    No  → Q8

Q8: これは操作ルール・規約？
    Yes → docs/rules/<category>.md
    No  → 再考する（本当に CLAUDE.md に書く必要がある？）
```

## Context 一覧と特徴

### 1. Machines（機材）

**場所**: `docs/machines/<hostname>.md`

**内容**:
- ハードウェア仕様（CPU / RAM / GPU / ストレージ）
- OS / ソフトウェア / ツールバージョン
- ネットワーク設定
- 稼働プロセス
- トラブル履歴
- バックアップ運用

**粒度**: 1 マシン = 1 ファイル

**更新頻度**: マシン追加時、重要変更時（SSD 交換・OS アップデート等）

**CLAUDE.md 残留**: 1 行サマリー + `@import`

### 2. Journal（日次ログ）

**場所**: `docs/journal/YYYY-MM-DD.md`

**内容**:
- その日の主要イベント
- 完了タスク
- 発生した問題と対応
- 学び
- 関連コミット

**粒度**: 1 日 = 1 ファイル（同日複数セッションは 1 ファイル内にセクション）

**更新頻度**: 毎セッション終了時

**CLAUDE.md 残留**: 過去 2 週間のサマリーリスト（詳細はジャーナルへ）

### 3. Routines（定期ルーチン）

**場所**: `docs/routines/<name>.md`

**内容**:
- タスクの目的
- 実行頻度・スケジュール
- 手順
- 監視 URL
- 発動トリガー
- 関連スクリプト

**粒度**: 1 ルーチン = 1 ファイル

**更新頻度**: ルーチン追加時・変更時

**CLAUDE.md 残留**: 一覧のみ（`@import`）

**例**:
- `docs/routines/x-daily-briefing.md` — X 情報収集ルーチン
- `docs/routines/session-schedule.md` — Claude Code セッション時間枠
- `docs/routines/ssd-price-monitor.md` — SSD 価格監視
- `docs/routines/hourly-report.md` — 定時報告

### 4. Reminders（期限・リマインダー）

**場所**: `docs/reminders.md`（1 ファイル集約）

**内容**:
- 日付
- 事項
- アクション内容
- 関連リンク

**粒度**: 1 ファイルに全期限、日付順ソート

**更新頻度**: 項目追加・完了時

**CLAUDE.md 残留**: 次の 2 週間分のみ、それ以外は `@docs/reminders.md`

### 5. Projects（個別プロジェクト）

**場所**: `docs/projects/<project>.md` または `docs/projects/<project>/index.md`

**内容**:
- プロジェクト目的
- 参加者
- タスクリスト
- 関連リソース
- 進捗

**粒度**: 1 プロジェクト = 1 ファイル（or 1 ディレクトリ）

**更新頻度**: プロジェクト活動時

**CLAUDE.md 残留**: プロジェクト名と 1 行説明 + `@import`

**例**:
- `docs/projects/shibu-observation.md` — しぶエコ観察
- `docs/projects/substack.md` — Substack 連載
- `docs/projects/shibu-chatbot.md` — しぶチャットボット

### 6. Rules（操作規約）

**場所**: `docs/rules/<category>.md`

**カテゴリ例**:
- `operations.md` — 一般操作ルール（削除前確認など）
- `coding.md` — コーディング規約
- `security.md` — セキュリティルール（ログイン・金銭操作）
- `machines.md` — 機材別の注意事項
- `git.md` — git 運用ルール

**更新頻度**: ルール改訂時

**CLAUDE.md 残留**: 最重要 3-5 ルールのみ、詳細は `@import`

### 7. ADR（Architecture Decision Record）

**場所**: `docs/adr/NNNN-<topic>.md`（連番 + スラッグ）

**内容** (ADR 標準フォーマット):
```markdown
# NNNN. <決定事項タイトル>

## Status
Accepted / Deprecated / Superseded by ADR-MMMM

## Context
<決定の背景>

## Decision
<何を決めたか>

## Consequences
<結果として起こること>
```

**例**:
- `0001-no-memory-feature.md` — メモリ機能を使わない判断
- `0002-ssd-purchase-hold.md` — 2026/04 SSD 購入保留判断
- `0003-claude-md-diet-skill.md` — このスキル導入判断

### 8. Archive（アーカイブ）

**場所**: `docs/archive/YYYY-MM/index.md`

**内容**:
- その月の全体サマリー
- 個別日誌ファイルへのリンク
- 月次の重要トピック

**更新頻度**: 月末に実施（翌月初旬の整理で）

**CLAUDE.md 残留**: なし（個別参照もしない、必要時のみ grep で検索）

## ドメイン別の切り出しパターン（例）

### パターン A: 個人のマルチプロジェクト運用

```
docs/
├── machines/       # 複数マシン
├── journal/        # 日次
├── routines/       # 個人ルーチン
├── projects/       # 複数プロジェクト並行
└── reminders.md    # 個人期限
```

### パターン B: 単一プロジェクト深掘り型

```
docs/
├── journal/
├── spec/           # 仕様書
├── adr/            # 判断記録多め
├── tests/          # テスト戦略
└── deployment.md
```

### パターン C: 情報収集・研究型

```
docs/
├── journal/
├── sources/        # 情報源ごとのノート
├── analysis/       # 分析記録
├── briefings/      # 日次・週次ブリーフィング
└── entities/       # 追跡対象（人物・組織）
```

## 切り出し判断の心得

1. **迷ったら切り出す** — CLAUDE.md の「現在の状態」ではない情報は基本外出し
2. **単一責任の原則** — 1 ファイル = 1 Context
3. **サマリー重複は OK** — CLAUDE.md の 1 行 + 詳細ファイルの全文は意図した冗長性
4. **ファイル名は未来の自分に優しく** — 内容を開かず推測できる命名
5. **日付は常に ISO 8601 (YYYY-MM-DD)** — 検索性・ソート性
