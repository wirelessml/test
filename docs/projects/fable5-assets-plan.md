# Fable 5 無料期間（〜6/22）資産化プラン

> 方針: **「6/23 以降も残る成果物」への変換に全振り**（スキル・ハーネス・ドキュメント・重い執筆・コードレビュー）。使い捨て出力に枠を使わない。
> 各枠の冒頭でこのメニューから取る。判定基準は毎回「これは 6/23 に残るか？」。重いものは枠の前半、Codex に委譲できるものは masup へ。

> ⚠️ **2026-06-14 更新**: **Fable 5 は予定の 6/22 を待たず使用不可となった**（標準モデルは Opus 4.8 に移行、settings.json `"model": "opus"`）。「無料期間」の緊急性は消滅したが、**ここに並ぶキューは「残る成果物」への変換として通常作業で継続する**（タイトルの「〜6/22」は歴史的経緯として残置）。

## 運用前提（2026-06-14〜・Fable 不在を前提に組み立てる）

**「無料の重処理枠がある」前提は捨てる。** Fable が使えない以上、以下を計画の土台にする:

1. **委譲ファースト** — 重い/長い処理（コードレビュー・監査・文字起こし・長文分析・大量調査・bot 壁の Web 調査）は **masup Codex / しゅん先生 Codex** に委譲し、Claude(Opus) のレート枠を温存する（手順: @skills/delegating-to-masup-codex/。Claude は指示と検証＝ルール4 に徹する）。6/14 のしぶエコ動画分析がこの型（43分字幕を Codex 分析→実字幕 8/8 照合）。
2. **Opus 枠は有限として配分** — 「枠の頭で計画」「時間かかりすぎ＝中止」（@docs/rules/session-setup.md）を厳守。低 ROI 作業に Opus を使わない。
3. **キューは『残る価値 × 緊急度』で優先** — 締切前の一括消化ではなく、ROI 順に少しずつ。必要なら下のキューを都度並べ替える。

## 消化ログ

### 6/12（初日・8 項目）
- [x] CLAUDE.md 再ダイエット（212→168 行、4-5 月 archive 化、povo 発掘）
- [x] スキル 4 本＋配線（journal / 録画文字起こし / 全機更新 / X ファクトチェック）
- [x] ハーネス（SessionStart フック＋launchagent-doctor＋permissions 床）→ **doctor が実害 3 件を即検出・即修理、全緑達成**
- [x] scripts/ 棚卸し（masup Codex 委譲→検証 3 点訂正→削除 24・archive 16 実行、ゾンビ watchdog・shibu.stream 無効化）
- [x] 体験報告書（本文完成済みと判明→レビュー→**矛盾 2 点を Word に適用済み**、残りは本人の事務手続きのみ）
- [x] 災害復旧ブートストラップ（plist 9 本を config/launchagents/ 収容＋bootstrap-launchd.sh check/install、check 18/18 ✅、email-job-report の正本ドリフト解消）
- [x] rules/routines 鮮度監査 第 1 弾（operations.md の Manus 記述に 5/4 認識訂正を反映、instagram-watch.md 休眠注記）
- [x] Substack 政治家版ドラフト 2 案（docs/substack/2026-06-12-ai-rikai-seijika.md）

### 6/13（Codex引き継ぎ・資産化継続）
- [x] **job-search-daily.py レビュー残パッチ反映** — 0件正常レポート防止済みに加え、`git pull/add/commit/push` とメール送信を非0検知する `run_cmd()` 化、push失敗後メール送信・メール失敗の成功扱いを停止。`email-job-report.sh` は送信失敗時 `exit $rc`、明示再送は `JS_FORCE_EMAIL=1`。本番 App Support 側へ同期済み、`JS_NO_PUSH=1 JS_NO_EMAIL=1` 実走で91件レポート生成まで確認
- [x] **machines docs 鮮度更新** — m1 / shun-sensei-pc / masu-p55 を実機照合し、AI CLI 3 種、OS build、Codex Desktop App MSIX版、IP/容量/タスク状態を 2026-06-13 実測へ更新。全機 `claude 2.1.176` / `codex 0.139.0` / `gemini 0.46.0` で揃っていることを記録
- [x] Codex側 Gmail 認証・運用ルール整備、テクノプロ返信下書き作成、エボルカWEB面談チートシート更新（詳細は @docs/journal/2026-06-13.md）

### 6/14（video-editor レビュー反映＝資産化キュー#1 完了）
- [x] **takeru-video-editor レビュー反映** — Codex レビュー A の実バグを Claude 側で実コード再検証（#1 typer.Context 即死は venv で `AttributeError` 再現確認）→ TDD で 5 点修正し公開リポ（github.com/wirelessml/shibu-video-editor）へ **2 コミットで push**（`6cb0baf` リブランド shibu→takeru / `11080a1` fix）。
  - #1 pipeline 即死 → `_transcribe_video()` 純関数を CLI と pipeline で共有 ／ #2 境界フェード未実装 → `select` を `trim/atrim+concat+afade(in/out)` へ書換え（**実 ffmpeg で完走・再デコード検証**）／ #3 プラン無検証 → `EditingPlan` に時刻 validator ／ #4 空 keeps → 明確な `ValueError` ／ #6 do_not_touch 部分重複 → 区間差し引き ／ 安全: 生成スクリプトのコメント改行 injection サニタイズ＋`.gitignore` に PII 生成物追加
  - テスト **23 passed**（新規 11＋既存 12、実 ffmpeg テスト含む）。重い YAGNI（API リトライ/コスト上限・長尺チャンク分割・外部API異常系の全モック）は意図的に見送り＝コミットメモに明記

### 進行中（masup Codex 並走）
- [x] **Codex レビュー A**: takeru-video-editor 静的レビュー **受領・検証済み**（抜き打ち照合 3/3 一致 → docs/projects/review-video-editor-2026-06-12.md。実バグ: typer.Context 誤用＝pipeline 即死 / カット境界フェード未実装 / AI 生成プラン無検証。**→ 6/14 公開リポへ修正 push 済み**）
- [x] **Codex レビュー B**: job-search-daily-mac.py（毎朝 04:30 本番）堅牢性レビュー **受領・反映済み**。6/12 fail gate、6/13 push/mail失敗検知と二重送信制御を本番同期
- [x] **Codex レビュー C**: takeru-chatbot セキュリティ監査 **受領・検証済み**（重大 5 点を実コード照合で全一致 → docs/projects/review-chatbot-security-2026-06-12.md）。`/api/voice` は 657 行 return が 658 行レート制限の前＝課金ノーガード、`/stats` は innerHTML 連結で保存型 XSS。**サーバは現在停止中＝露出なし**、再公開前必読警告を start.sh / chatbot CLAUDE.md に埋込済み
- 運用知見: codex exec の `--sandbox workspace-write` は **cwd 外（/mnt/c）に書けない** → 成果物はワークスペース内（or ホーム直下）に書かせて shell 側で回収する（A〜C で確立、ランナーに salvage 段を内蔵）
- **job-search 本番はレビュー B 反映の堅牢版を App Support に同期済み＝明日 04:30 から本番稼働**（silent failure 根治）

## キュー（優先順）

1. ~~**video-editor レビュー反映**~~ ✅ **6/14 完了**（公開リポへ push、実バグ 5 点修正＋テスト 23＋実 ffmpeg 検証。詳細は上記 6/14 ログ）
2. **takeru-chatbot 再公開前パッチ** — セキュリティ監査 C の重大5点を、公開判断が出た時点で修正
3. **しぶエコ人物相関の正本化** — ジャーナル散在の人物情報（八木仁平=源流〜りくと/あい/なかそにー等）を takeru-chatbot/knowledge/ に集約
4. **スキル実地テスト** — 6 スキルの呼出確認（writing-skills の検証負債解消）、SessionStart フック発火確認
5. rules 鮮度パス第 2 弾 — mac-processes.md（Codex/Manus 言及）、useful-commands の棚卸し
6. Substack 本編化 — 政治家版 or 「動いている LaunchAgent も TCC 時限爆弾」技術記事
7. 訪問動画パイプライン拡充 — B グループ 1 本目の実制作と連動（テロップ・カット支援）
8. **6/22 クローズ作業** — 達成棚卸し（このログを集計）→ `/model opusplan` 復帰 → CLAUDE.md の ⭐ 行を実績サマリーに置換

## 関連
- 戦略の発端: @docs/journal/2026-06-12.md（AI 使い方論 3 連〜「消費でなく蒸留」）
- 期限: @docs/reminders.md（2026-06-22）
