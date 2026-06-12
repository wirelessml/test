---
name: delegating-to-masup-codex
description: Use when offloading heavy or parallelizable work (code review, security audit, transcription, large-corpus analysis, web research behind bot-walls) from the Mac to masu-p55's Codex CLI, or whenever the user says「masup codex使って」「コーデックスに投げて」
---

# masup Codex への作業委譲

## Overview

masu-p55 (WSL2 の Codex CLI) は **Claude（Mac）の委譲先ワーカー**（2026-06-12 役割転換）。Mac の Claude が司令塔として重い/並列な作業を `codex exec` で投げ、**返ってきた成果物は必ず Claude が検証してからユーザーに報告する**（CLAUDE.md ルール 4）。Codex に自走の判断はさせない＝指示は具体的に、出力形式は固定する。

## 何を委譲するか

| 向く | 向かない |
|---|---|
| コードレビュー・セキュリティ監査（大量ファイル読解） | ユーザーへの最終報告（Claude がやる） |
| 文字起こしの一次処理・長文要約 | 対人監視・反論文面など判断を伴うもの |
| bot 対策で WebFetch が弾かれる URL の調査（Codex の Web 検索が強い、dav2d/Anubis の前例） | 本番への破壊的変更（Claude が検証後に適用） |
| 240s を超える長時間タスク（run_in_background で完走） | 秘匿情報を含むファイルの送信（先に精査） |

## 標準手順（4 ステップ）

1. **プロンプトと成果物パスを固定**: 出力は「日本語 Markdown、構成見出し指定、`~/<name>.md`（ホーム直下）に**書き出させる**」。推測には(推測)明記・存在しないコード引用禁止を明記
2. **転送**: コードは `COPYFILE_DISABLE=1 tar czf ...`（後述の罠①）→ `scp ... masu-p55:` 。GitHub 公開物は WSL 側で直接 `git clone --depth 1`
3. **実行（run_in_background 推奨）**: ランナー .sh を作って投げる。回収段を必ずランナーに内蔵（罠②）:
   ```bash
   cd ~/workspace
   codex exec --skip-git-repo-check --sandbox workspace-write "$(cat /mnt/c/Users/gci_admin/prompt.txt)" > /mnt/c/Users/gci_admin/run.log 2>&1
   [ -f ~/out.md ] && cp ~/out.md /mnt/c/Users/gci_admin/out.md   # cwd外に直接書けないので salvage
   ```
   そして `ssh masu-p55 'wsl -e bash -lc "bash /mnt/c/Users/gci_admin/runner.sh"'` → `scp masu-p55:out.md /tmp/`
4. **検証（必須）**: 成果物を Claude が読み、**主張を実コード/実ファイルと抜き打ち照合**（A/B/C では各 3〜5 点を grep で確認、全一致を確認してから採用）。一致しない指摘は捨てる。本番への反映は安全なものだけ、提案と分けて報告

## 罠（2026-06-12 の A/B/C 実証で判明、ハマったら最初にここ）

| 症状 | 原因と対策 |
|---|---|
| scp で `out.md: No such file or directory`（exit 1） | **codex exec `--sandbox workspace-write` は cwd 外＝`/mnt/c` に書けない**（Codex 自身は「Read-only file system」と報告して諦める）。→ 成果物はワークスペース or `~/` に書かせ、ランナーの最後で `/mnt/c` へ `cp` 回収する |
| 監査結果に存在しないファイル `._foo.sh` が 58 件 | **macOS `tar` が AppleDouble (`._*`) を混入**。→ `COPYFILE_DISABLE=1 tar ...` で抑止。混入したら Mac 実体を `ls` して実在確認（前回は実在せず＝Codex の指摘を 1 件却下できた） |
| 成果物 .md が 5,845 行・289KB ある | **stdout リダイレクトは codex の実行ログ全部入り**。成果物は末尾。→ ファイル書き出しさせて回収するのが正道。ログから拾うなら `grep -n "^## "` で最終セクション境界を探す |
| 240s で切れる | Claude Code の Bash timeout。→ `run_in_background: true` で投げ、完了通知を待つ |
| codex のバージョン/到達確認 | `ssh masu-p55 'wsl -e bash -lc "codex --version"'`（codex は WSL2 側、claude/gemini は Windows 側）。詳細は updating-ai-cli-fleet スキル |

## 並列委譲

独立した複数タスクは別ワークスペース（`~/review-a` `~/review-b`）に分けて各々 run_in_background で同時投入できる（A/B を並走させた）。共有状態がないことだけ確認する。

## 関連

- マシン詳細: @docs/machines/masu-p55.md
- 実証ログと収蔵レビュー: @docs/journal/2026-06-12.md、docs/projects/review-*.md
- 成果物の検証規律: CLAUDE.md ルール 4（サブエージェントの成果物は必ず自分で検証）
