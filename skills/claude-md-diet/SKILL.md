---
name: claude-md-diet
description: 肥大化した CLAUDE.md を DDD 的 bounded context に分解してスリム化する。機材情報・日次ログ・ルーチン・履歴・期限リマインダーを個別ファイルに切り出し、CLAUDE.md 本体を 200-300 行の「プロジェクト糊」に戻す。Use when CLAUDE.md が 500 行超え / セッション開始時のトークン消費が気になる / AI が CLAUDE.md のルールを部分的に無視し始めた (instruction dilution 症状) / プロジェクト成長でドメインが増えた時。
triggers:
  - CLAUDE.md が大きすぎる
  - CLAUDE.md 肥大化
  - CLAUDE.md ダイエット
  - DDD で CLAUDE.md を分割
  - bounded context で整理
  - claude.md refactor
---

# CLAUDE.md Diet — 肥大化した CLAUDE.md を DDD 的に分解するスキル

## 哲学

CLAUDE.md は **「プロジェクト糊」** であって **「仕様書」「ログ」「リファレンス」ではない**。長期運用で起きる症状:

- **Instruction dilution**: ルール数が増えると AI は優先順位を推測で並べ替える → 上位 3-5 個しか厳密に守らない
- **Middle-context weakness**: long context は真ん中の attention が薄い（Claude 4.x でも残存）
- **Update cost inflation**: 変更のたびに全体を読み直させる → 週次トークンを圧迫
- **Knowledge entropy**: 新旧情報が同居して矛盾が発生、AI は混乱してハルシネートしやすくなる

DDD (Domain-Driven Design) の bounded context / aggregate root / ubiquitous language の 3 概念を CLAUDE.md 運用に借用することで、この症状を解消する。

## いつ使うか

| サイン | 対処 |
|---|---|
| `wc -l CLAUDE.md` が **500 超**え | Phase 1 から順次実行 |
| セッション開始時のコンテキスト注入量が体感で重い | Phase 2 (ジャーナル切り出し) 優先 |
| AI がルールを守らない瞬間が増えた | Phase 3 (ルール優先順位の再設計) 優先 |
| 複数マシン・複数ドメインを扱うプロジェクトに成長した | Phase 1 (機材・ドメイン分離) |
| 月次の定期メンテナンスとして | フルサイクル実行 |

## 標準的な切り出し対象 (Bounded Contexts)

| Context | 移行先 | 内容 | 発動頻度 |
|---|---|---|---|
| **Machines** | `docs/machines/*.md` | ハード仕様・IP・SSH 情報・稼働プロセス | マシン追加 / 重要変更時 |
| **Journal** | `docs/journal/YYYY-MM-DD.md` | 日次作業ログ・完了セクション | 毎セッション終了時 |
| **Routines** | `docs/routines/*.md` | 定期タスク・スケジュール・監視項目 | 月次見直し |
| **Reminders** | `docs/reminders.md` | 期限・解約日・イベント日付 | 項目追加時 |
| **Projects** | `docs/projects/<name>.md` | 個別プロジェクト固有情報 | プロジェクト作成時 |
| **Archive** | `docs/archive/YYYY-MM/*.md` | 月次まとめ・2 週間以上前の完了記録 | 月次バッチ |
| **Decisions** | `docs/adr/NNNN-*.md` | 重要判断記録 (Architecture Decision Record) | 決定時 |
| **Rules** | `docs/rules/*.md` | 操作規約・セキュリティルール・コーディング規約 | 改訂時 |

## 実行手順

### Phase 0: 現状分析 (~5 分)

```bash
# ボリューム計測
wc -l CLAUDE.md

# セクション構造
grep -n "^## " CLAUDE.md | head -50
grep -c "^## " CLAUDE.md
grep -c "^### " CLAUDE.md

# 肥大セクション特定（上位 5 つ）
awk '/^## /{if(h)print h,n; h=$0; n=0; next}{n++}END{print h,n}' CLAUDE.md | sort -k2 -n -r | head -5

# 重複候補の検出
grep -E "^- " CLAUDE.md | sort | uniq -c | sort -rn | head -20
```

**出力**: `skills/claude-md-diet/reports/<date>-analysis.md` に分析レポートを保存。

**判定基準**:
- 合計 500 行超 → 即実行
- 単一セクションが 200 行超 → そのセクションのみ優先切り出し
- 2 週間以上更新なしの完了セクション → archive 対象

### Phase 1: 機材情報切り出し (~30 分、約 200 行削減)

CLAUDE.md の **ユーザー情報 > 機材** セクションから、各マシンの詳細を個別ファイルへ。

**手順**:

1. `docs/machines/` ディレクトリ作成
2. マシンごとに `docs/machines/<hostname>.md` を作成（例: `shun-sensei-pc.md`, `masu-p55.md`, `m1-macbook-air.md`）
3. 各ファイルに以下のテンプレートで移行:
   ```markdown
   # <マシン名>

   ## 役割
   <1-2 行のサマリー>

   ## ハードウェア
   <CPU / RAM / GPU / ストレージの詳細>

   ## ネットワーク
   <IP / Tailscale / SSH 情報>

   ## インストール済みツール
   <バージョン情報付き>

   ## 稼働中プロセス / サービス
   <常駐サービス>

   ## 既知の問題 / 注意事項
   <トラブル履歴や運用注意>

   ## 変更履歴
   - YYYY-MM-DD: <変更内容>
   ```
4. CLAUDE.md 本体は以下に置換:
   ```markdown
   - **<マシン名>**: <1 行サマリー>（詳細: @docs/machines/<hostname>.md）
   ```

### Phase 2: 完了セクションのジャーナル化 (~1 時間、約 1000 行削減)

CLAUDE.md の `## 完了 (YYYY-MM-DD ...)` セクション群を日次ジャーナルファイルへ移動。

**手順**:

1. `docs/journal/` ディレクトリ作成
2. 各完了セクションを `docs/journal/YYYY-MM-DD.md` として保存
   - 同日に複数セクションがある場合は 1 ファイルに集約
3. 2 週間以内のものだけは CLAUDE.md に**サマリーリスト**を残す:
   ```markdown
   ## 最近 2 週間の完了サマリー
   - 2026-04-22: しゅん先生 PC バックアップ実装 + Plextor 死亡 + Seagate 延命 (@docs/journal/2026-04-22.md)
   - 2026-04-21: AI研修 2 日目 / GC313Pro セットアップ (@docs/journal/2026-04-21.md)
   - ...
   ```
4. 2 週間より古いものは `docs/archive/YYYY-MM/index.md` に月次でまとめる

### Phase 3: ルーチンの切り出し (~15 分、約 100 行削減)

定期タスク・監視・スケジュール系は `docs/routines/` へ。

**対象**:
- X 情報収集ルーチン
- Claude Code セッションスケジュール
- Instagram 監視設定
- SSD 価格監視
- 定時報告設定

**CLAUDE.md 側の残骸**:
```markdown
## 定期ルーチン
運用中のルーチン一覧: @docs/routines/index.md
- X 情報収集 (各セッション毎): @docs/routines/x-daily-briefing.md
- セッションスケジュール (9/14/19/0/5 時): @docs/routines/session-schedule.md
- SSD 価格監視 (毎週月曜): @docs/routines/ssd-price-monitor.md
```

### Phase 4: リマインダー・期限の集約 (~10 分、約 30 行削減)

`## リマインダー` セクション全体を `docs/reminders.md` へ移動。

CLAUDE.md には:
```markdown
## 期限・リマインダー
@docs/reminders.md (全期限リスト)

次の 2 週間の重要期限:
- YYYY-MM-DD: <要約>
- ...
```

### Phase 5: 検証 (~10 分)

```bash
# 行数確認
wc -l CLAUDE.md   # 目標: 200-300 行

# @import リンクの整合性確認
grep -oE "@[a-zA-Z0-9_/\.-]+\.md" CLAUDE.md | while read p; do
  path="${p#@}"
  [ -f "$path" ] && echo "OK: $p" || echo "MISSING: $p"
done

# 情報損失チェック（git で移動元と移動先を比較）
git diff HEAD~5 --stat
```

**チェックリスト**:
- [ ] CLAUDE.md が 200-300 行
- [ ] 重要な「現在の状態」は CLAUDE.md に残ってる
- [ ] `@import` パスが全部解決する
- [ ] 新しい Claude Code セッション開始で正しくコンテキストが読まれる
- [ ] 移動元と移動先の diff 確認で情報損失なし

### Phase 6: コミット

**小さな単位で複数コミット推奨**（rollback しやすく）:

```bash
# Phase 1
git add docs/machines/ CLAUDE.md
git commit -m "refactor: 機材情報を docs/machines/ に DDD 分割"

# Phase 2
git add docs/journal/ docs/archive/ CLAUDE.md
git commit -m "refactor: 完了セクションを journal/archive に分離"

# Phase 3
git add docs/routines/ CLAUDE.md
git commit -m "refactor: 定期ルーチンを docs/routines/ に集約"

# Phase 4
git add docs/reminders.md CLAUDE.md
git commit -m "refactor: リマインダーを docs/reminders.md に集約"

# 最終
git push
```

## アンチパターン (やってはいけないこと)

| ❌ NG | 理由 |
|---|---|
| 情報の削除 | 移動 != 削除。迷ったら archive に退避 |
| `@import` ネスト 3 階層超 | Claude Code のロード動作が不安定、可読性低下 |
| 日誌ファイル名を自由形式 | `YYYY-MM-DD.md` 固定、検索性と時系列整合性のため |
| 機材詳細を複数ファイルに分散 | 1 マシン = 1 ファイル原則を守る |
| git commit を 1 個にまとめる | 失敗時 rollback できない、差分レビュー困難 |
| CLAUDE.md を完全に空にする | 現在の状態・運用ルールは CLAUDE.md に最低限残す |
| @import 先を読めない場所に置く | `~/.claude/foo.md` のような外部パスは避け、リポジトリ内に収める |

## 実行頻度

| タイミング | やること |
|---|---|
| **初回** | 500 行超え検知時点で Phase 1-6 を数日かけて段階実行 |
| **継続** | 月次で Phase 0 (分析) → 肥大兆候あれば該当 Phase |
| **四半期** | フルサイクル再実行、docs/ の構造見直し |
| **緊急** | AI 指示追従率低下を感じた時点で即 Phase 3 |

## 参照

- @references/ddd-principles.md — DDD 3 原則の詳細と CLAUDE.md への適用例
- @references/bounded-contexts.md — よくある bounded context 例と切り出し方
- @references/import-syntax.md — Claude Code `@import` 機構と制約
- @templates/claude-md-minimal.md — 目標とする 200 行テンプレート
- @templates/machine-template.md — `docs/machines/*.md` のテンプレート
- @templates/journal-template.md — `docs/journal/YYYY-MM-DD.md` のテンプレート
- @examples/before-after.md — 実例（1800 行 → 250 行）

## 関連スキル

- `claude-obsidian:wiki-ingest` — 切り出したファイルを Obsidian 側にも同期する
- `superpowers:writing-plans` — 移行計画を事前に書く
- `superpowers:verification-before-completion` — Phase 5 検証の強化版
