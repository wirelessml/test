---
name: fact-checking-x-posts
description: Use when the user shares an X/Twitter URL or screenshot and asks「これ本当？」「ファクトチェック」, or when an AI-related claim from social media needs verification before acting on it
---

# X 投稿ファクトチェック

## Overview

仲氏の定常ワークフロー。AI 系インフルエンサーの投稿は**機能の存在は正しいが適用範囲を盛る**パターンが多い。検証の本体は「一次ソースに当たる」こと。投稿の真偽を ✅/⚠️/❌ ＋根拠で返す。

## 取得ルート（上から順に試す）

1. **syndication API / `twitter` CLI**（agent-reach、@minimalistneko の Cookie 取得済み）: `twitter -c tweet <id>` など
2. **WebFetch**（公開ツイートなら `x.com` → `fixupx.com` 等の代替ドメインも）
3. **ログイン済み Chrome プロファイル**: `open -a "Google Chrome" <url>` → osascript で navigate → `screencapture -x` → Read で画像解析（login wall 突破の定番）
4. 操作が要るときは **X PWA**（`com.google.Chrome.app.lodlkdfmihgonocnmddehnfgiljnadcf`、computer-use full tier。Safari/Chrome 等のブラウザは read tier）

### twitter CLI の既知バグ（6/6 確認）

- `tweet <id>` が**親ツイートを誤返却**することがある → ID とテキストの対応を必ず目視確認
- `isQuote` フラグは**返信を拾わない**
- 投稿は 280 加重（日本語 ≒ 140 字）上限

## 検証プロトコル

1. **主張を分解**: 「機能 X が存在する」「全プランで使える」「コマンドは /foo」のように検証可能な単位へ
2. **一次ソースに当たる**（優先順）: 公式ドキュメント / 公式リリースノート / GitHub リポジトリ実体 / **手元での実機テスト**（コマンドは実行して確かめる）/ アプリバイナリ直接調査（app.asar を strings+grep した 5/4 の前例）
3. **過去ジャーナルと突合**: `grep -ri "<キーワード>" docs/journal/ takeru-chatbot/knowledge/` — 既に検証済みのことが多い
4. **判定を 3 値で報告**:
   - ✅ 事実（一次ソース併記）
   - ⚠️ 部分的に正しい（**何が盛られているか**を特定して書く）
   - ❌ 誤り/捏造（正しい情報を併記）

## 頻出の盛りパターン（過去の実例）

| パターン | 実例 |
|---|---|
| プラン適用範囲の過大化（「全プランで使える」） | Artifacts 永続ストレージ / Projects RAG 拡張 → 実際は Pro 以上のみ（@hoshino_aisales、5/4・5/5 の 2 連発） |
| 存在しないコマンドの捏造 | `/statusline` 単独コマンド、`/codex:test` 等 → 実在コマンド一覧と突合（@claudecode_love） |
| 他ツールの数字の流用 | 「コンテキスト 71.5 倍」が別ツールの計測値（@sumika45379） |
| 機能は実在するが条件を省略 | `codex remote-control` は実在したが OS 競合条件あり（6/2 実機検証で「概ね真」と判定） |

## 報告と投稿のルール

- 検証結果はジャーナルに記録（誰の何という主張を、何で確認したか）
- **反論・返信ツイートの投稿はユーザーの最終判断**。文面案は出してよいが、投稿実行と修正はユーザー（partisan 化回避の修正が入った 5/3 の前例）
- 誤りと断定する前に**自分の context の鮮度を疑う**（「/rc は存在しない」と誤判定→公式ソースで訂正した 6/5 の前科。knowledge cutoff 後の新機能はWebSearch/公式で確認）
