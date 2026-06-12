#!/usr/bin/env bash
# masup WSL2 の Codex に、しぶ3時間動画の文字起こし分析を依頼するランナー。
set -u
cd /home/gci_admin || exit 1

PROMPT="あなたはミニマリストしぶ（YouTuber／ミニマリスト）の動画を観察分析するアシスタントです。同じディレクトリにある sibu-transcript.txt を読んでください。これはしぶの新作3時間動画『「ミニマリストに憧れるけど…」捨てられない女性の自宅へ。モノ減らしたら汚部屋もキレイに片付いた』（2026-06-06公開）のYouTube自動字幕(ASR)で、誤変換が多い（例:「整理収納」→「生理収納」、句読点や数字のずれ）。文脈で補正しながら読むこと。

読み終えたら、日本語のMarkdownで /home/gci_admin/sibu-analysis.md を作成・保存してください（実際にファイルを書き出すこと）。構成:
1. 概要（動画の主旨・登場人物・舞台を3〜5行）
2. 依頼者プロフィール（『とこさん』。年齢／職業／世帯／趣味／抱える課題／保有資格 等、字幕から拾えるだけ）
3. 動画の流れ（時系列の章立てを推定して箇条書き：導入→片付け作業→気づき→ビフォーアフター 等）
4. しぶの片付け哲学・印象的な発言（ASR誤変換を補正した上で『』付きで10個前後引用）
5. しぶ定番フレーム『モノ・お金・デジタル』の3軸で内容を整理
6. 50代・整理収納アドバイザー・就活 という観点での学び（同じ境遇の視聴者向けに）
7. 観察ナレッジ用メモ（しぶエコシステム上の位置づけ、過去動画との接続、Substackネタ候補）

注意: ASR誤変換は文脈補正、推測には『(推定)』と明記、字幕に無いことは創作しない。簡潔かつ具体的に。"

~/.local/bin/codex exec --skip-git-repo-check --sandbox workspace-write "$PROMPT" < /dev/null > /home/gci_admin/sibu-codex-run.log 2>&1
RC=$?
echo "codex exit=$RC"
if [ -f /home/gci_admin/sibu-analysis.md ]; then
  echo "ANALYSIS_OK lines=$(wc -l < /home/gci_admin/sibu-analysis.md) chars=$(wc -m < /home/gci_admin/sibu-analysis.md)"
else
  echo "ANALYSIS_MISSING (see sibu-codex-run.log)"
  tail -15 /home/gci_admin/sibu-codex-run.log
fi
