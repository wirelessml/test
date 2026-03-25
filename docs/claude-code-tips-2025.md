# Claude Code 最新Tips & 活用ガイド（2025年版）

> 進化が速すぎて週1でアップデート確認しないと置いていかれる時代。ここに最新の知見をまとめておく。

---

## 1. `--dangerously-skip-permissions` はもう古い

### 従来の問題

```bash
# 危険：全権限を無条件でスキップ
claude --dangerously-skip-permissions
```

名前の通り危険。ファイル削除も `rm -rf` も確認なしで実行される。

### 現在の正解：`--permission-mode auto`

```bash
claude --permission-mode auto
```

**2段階の安全設計：**

```
ユーザーの指示
    ↓
┌─────────────────────┐
│  AI自身の判断層       │  ← Claude が「この操作は安全か」を判断
│  (意図・文脈を理解)   │
└─────────┬───────────┘
          ↓
┌─────────────────────┐
│  セーフガード層       │  ← 破壊的操作をシステムレベルでブロック
│  (ハードコードルール) │
└─────────────────────┘
```

### 比較表

| モード | 安全性 | 自動化 | 用途 |
|--------|--------|--------|------|
| `default` | 毎回確認 | 低い | 慎重な作業 |
| `--dangerously-skip-permissions` | なし（全許可） | 最大だが危険 | 非推奨 |
| `--permission-mode auto` | AI判断 + セーフガード | 高い＆安全 | 推奨 |

---

## 2. 権限管理のベストプラクティス

### allowedTools（ツール単位の許可制御）

```jsonc
// .claude/settings.json
{
  "permissions": {
    "allow": [
      "Bash(npm test)",
      "Bash(npm run lint)",
      "Read",
      "Glob",
      "Grep"
    ]
  }
}
```

「全部許可」ではなく「必要なものだけ許可」が事故を防ぐ。

### Hooks（ツール実行前後のカスタムスクリプト）

ツール実行のタイミングにフックを仕込める：
- **PreToolUse**: ツール実行前に検証・ブロック
- **PostToolUse**: ツール実行後に記録・通知
- **SessionStart**: セッション開始時の初期化
- **Stop**: セッション終了時のクリーンアップ

---

## 3. Claude Subconscious（セッション横断メモリ）

### 概要

Letta製のオープンソースプラグイン。Claude Codeの各セッションを観察し、記憶を自動蓄積する。

- **GitHub**: github.com/letta-ai/claude-subconscious
- **開発元**: Letta（Anthropic公式ではない）

### 8つのメモリブロック

| ブロック | 内容 |
|----------|------|
| `core_directives` | 役割定義 |
| `guidance` | 次セッション向けガイダンス |
| `user_preferences` | 学習したユーザー設定 |
| `project_context` | コードベース知識 |
| `session_patterns` | 行動パターン |
| `pending_items` | 未完了タスク |
| `self_improvement` | メモリ進化指針 |
| `tool_guidelines` | ツール使用方法 |

### セットアップ

```bash
/plugin marketplace add letta-ai/claude-subconscious
/plugin install claude-subconscious@claude-subconscious
# LETTA_API_KEY を app.letta.com で取得して設定
```

### 動作モード

| モード | 動作 |
|--------|------|
| `whisper` | メッセージ注入のみ（軽量） |
| `full` | メモリブロック + メッセージ |
| `off` | 無効化 |

### 組み込みメモリとの比較

| 仕組み | スコープ | 性質 |
|--------|----------|------|
| `CLAUDE.md` | プロジェクト | 手動で書く「明示的な記憶」 |
| `~/.claude/CLAUDE.md` | ユーザー全体 | 個人の好み・共通設定 |
| Claude Subconscious | セッション横断 | 自動蓄積される「暗黙的な記憶」 |

### 注意点

- Letta のクラウドAPIを使うため、セッションデータが外部に送信される
- セキュリティ要件が厳しいプロジェクトでは慎重に検討すること

---

## 4. Computer Use vs pyautogui：使い分け

### 判断基準

> **「次に何をするか画面を見ないとわからない」→ Computer Use**
> **「やることは決まってる、ただ繰り返すだけ」→ pyautogui**

### 比較表

| | Computer Use | pyautogui |
|---|---|---|
| **判断** | AIがリアルタイムで画面を見て判断 | 事前に座標・手順を固定 |
| **向き** | 動的・探索的な作業 | 繰り返し・定型作業 |
| **速度** | スクショ→判断のループで遅め | 直接操作で高速 |
| **コスト** | APIトークン消費 | ローカル実行で無料 |

### pyautogui の使い方

Claude Codeに「この操作をpyautoguiで書いて」と指示するだけ。

```python
# 例：同じボタンを100回クリック
import pyautogui, time

for i in range(100):
    pyautogui.click(x=500, y=300)
    time.sleep(0.5)
```

```python
# 例：スクリーンショットを撮って画像マッチングでクリック
import pyautogui

button = pyautogui.locateOnScreen('button.png')
if button:
    pyautogui.click(button)
```

---

## 5. Slack連携

### メリット

- **チーム共有**: 会話の流れがチーム全員に見える
- **非エンジニアも参加**: ターミナル不要でClaudeに指示できる
- **通知が楽**: 結果がSlackに来るので別ツールを開かなくていい
- **モバイル対応**: スマホからでも指示を出せる

### 使い分け

| | Claude Code (CLI/Desktop) | Slack連携 |
|---|---|---|
| **コード編集** | 直接ファイル操作 | 制限あり |
| **ツール連携** | MCP/Hooks/全機能 | 限定的 |
| **向いてる人** | 開発者が手元で作業 | チームで共有・非同期作業 |

### Coworkとの組み合わせ

Slackでタスクを投げる → Claudeがバックグラウンドで作業 → 完了通知がSlackに届く

---

## 6. まとめ：Claude Code エコシステム全体像

```
┌─────────────────────────────────────────────────┐
│                Claude Code CLI                   │
│                                                   │
│  ┌──────────┐  ┌──────────┐  ┌───────────────┐  │
│  │ CLAUDE.md │  │  Hooks   │  │ allowedTools  │  │
│  │ (記憶)    │  │ (自動化) │  │ (権限制御)    │  │
│  └──────────┘  └──────────┘  └───────────────┘  │
│                                                   │
│  ┌──────────────────────────────────────────┐    │
│  │  --permission-mode auto (推奨)            │    │
│  │  AI判断層 + セーフガード層                 │    │
│  └──────────────────────────────────────────┘    │
│                                                   │
│  ┌──────────┐  ┌──────────┐  ┌───────────────┐  │
│  │ Computer │  │ pyautogui│  │ Subconscious  │  │
│  │ Use      │  │ (定型)   │  │ (Letta製)     │  │
│  │ (動的)   │  │          │  │               │  │
│  └──────────┘  └──────────┘  └───────────────┘  │
│                                                   │
│  ┌──────────────────────────────────────────┐    │
│  │  Slack連携 / Cowork / MCP サーバー        │    │
│  └──────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
```

---

## 更新履歴

- 2025-03-25: 初版作成
