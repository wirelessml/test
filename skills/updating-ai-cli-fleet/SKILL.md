---
name: updating-ai-cli-fleet
description: Use when the user asks「claude / codex / gemini のアプデ」「全機更新」「最新にして」, when unifying CLI versions across Mac / masu-p55 / しゅん先生 PC, or when checking machine reachability and health
---

# 全機 AI CLI 更新 & 健康チェック

## Overview

3 台（Mac M1 / masu-p55 / しゅん先生 PC）× 3 CLI（claude / codex / gemini）の定例更新。**更新前に「ピン留め判断が記録されていないか」直近ジャーナルを確認する**のが鉄則（5/25 に 5/20 の 0.130.0 ピン留めを見落として誤更新→差し戻しの前科）。

## 手順

### 1. 現状確認（並列で一気に）

```bash
# Mac ローカル
claude --version; codex --version; gemini --version

# 到達確認（ping は当てにならない、SSH まで試す）
ssh -o ConnectTimeout=6 shun-sensei "echo OK"
ssh -o ConnectTimeout=6 masu-p55 "echo OK"

# masup 3 種（claude/gemini=Windows 側、codex=WSL2 側に注意）
ssh masu-p55 'claude --version & gemini --version & wsl -e bash -lc "codex --version"'

# npm 最新版（更新要否の判定）
npm view @openai/codex version; npm view @google/gemini-cli version
```

### 2. 更新（必要な分だけ）

| ツール | Mac | Windows 機 |
|---|---|---|
| claude | `claude update` | `ssh <host> "claude update"`。配信が遅れていたら GitHub release zip で強制更新（`scripts/archive/update-claude-win.ps1` の方式、`$ver` を書き換えて再利用） |
| codex | `npm install -g @openai/codex@latest` | **masup は WSL2 側**: `ssh masu-p55 'wsl -e bash -lc "npm install -g @openai/codex@latest"'` |
| gemini | `npm install -g @google/gemini-cli@latest` | Windows 側 npm（WSL から見えるのは PATH interop） |

### 3. 結果報告

マシン × ツールの表で Before/After を報告し、ジャーナルに「全機 claude X / codex Y / gemini Z 統一」の形で記録。

## 絶対に守ること

- **`@anthropic-ai:registry=http://localhost:1` は消すな**。npm 経由の claude インストールを物理的に塞ぐ意図的ガード（3 台統一済み）。`npm view @anthropic-ai/...` が ECONNREFUSED になるのは正常。claude の更新は `claude update` / GitHub release のみ
- **更新前にピン留め記録を確認**: `grep -riE "ピン留め|pin" docs/journal/ | tail` 。意図的に止めてあるバージョンを上げない（上げる場合は理由をユーザーに確認）
- バージョン以外の変更（設定・plist・サービス）はこのルーチンの範囲外。混ぜない

## 到達不能時の切り分け

| 観察 | 解釈 |
|---|---|
| `ping` 不通だが SSH は通る | Windows Firewall の ICMP ブロック。**ping ≠ オフライン** |
| `.local` が解決しない | mDNS 圏外（別ネットワーク）か電源オフ。しゅん先生 PC は `.local` エントリのみ（Tailscale 代替経路なし）なので LAN 外からは届かない |
| masup は届くがしゅん先生 PC が届かない | 同一 LAN にいる証拠 → しゅん先生 PC 電源オフの可能性大。持ち越しとして記録 |

## 機材の役割（更新対象の前提）

- Mac = Claude Code 専用 / masup = Codex 専用（CLI は WSL2）/ しゅん先生 PC = 据え置きメイン
- 詳細: CLAUDE.md「現在の状態」と @docs/machines/
