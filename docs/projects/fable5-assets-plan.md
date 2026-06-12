# Fable 5 無料期間（〜6/22）資産化プラン

> 方針: **「6/23 以降も残る成果物」への変換に全振り**（スキル・ハーネス・ドキュメント・重い執筆・コードレビュー）。使い捨て出力に枠を使わない。
> 各枠の冒頭でこのメニューから取る。判定基準は毎回「これは 6/23 に残るか？」。重いものは枠の前半、Codex に委譲できるものは masup へ。

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

### 進行中（masup Codex 並走）
- [ ] **Codex レビュー A**: takeru-video-editor（公開 OSS、Python ~1.5K 行）静的レビュー → 受領後 Fable 5 が検証し、修正 PR/パッチ判断
- [ ] **Codex レビュー B**: job-search-daily-mac.py（毎朝 04:30 本番）堅牢性レビュー → 同上。**本番スクリプトの 6/23 後の自走品質に直結**

## キュー（優先順）

1. **job-search-daily.py へのレビュー反映** — B の指摘からパッチ適用＋動作確認（本番堅牢化、最優先）
2. **machines docs 鮮度更新** — 6/13 しゅん先生 PC の日とセットで 3 台分を実機照合（m1 / shun-sensei-pc / masu-p55。6/2 役割分離・6/12 watchdog 無効化を反映）
3. **video-editor レビュー反映** — A の指摘から公開リポへ修正コミット（OSS 品質＝対外資産）
4. **takeru-chatbot レビュー** — masup Codex 第 3 弾候補（tar 転送）＋ knowledge/ の整理
5. **しぶエコ人物相関の正本化** — ジャーナル散在の人物情報（八木仁平=源流〜りくと/あい/なかそにー等）を takeru-chatbot/knowledge/ に集約
6. **スキル実地テスト** — 次セッションで 5 スキルの Skill 呼出確認（writing-skills の検証負債解消）、SessionStart フック発火確認
7. rules 鮮度パス第 2 弾 — mac-processes.md（Codex/Manus 言及）、useful-commands の棚卸し
8. Substack 本編化 — 政治家版 or 「動いている LaunchAgent も TCC 時限爆弾」技術記事
9. 訪問動画パイプライン拡充 — B グループ 1 本目の実制作と連動（テロップ・カット支援）
10. **6/22 クローズ作業** — 達成棚卸し（このログを集計）→ `/model opusplan` 復帰 → CLAUDE.md の ⭐ 行を実績サマリーに置換

## 関連
- 戦略の発端: @docs/journal/2026-06-12.md（AI 使い方論 3 連〜「消費でなく蒸留」）
- 期限: @docs/reminders.md（2026-06-22）
