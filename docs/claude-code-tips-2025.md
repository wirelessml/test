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

### auto mode が使えるか確認する方法

auto mode は段階的にロールアウトされており、まだ使えないユーザーもいる。以下のコマンドで確認可能：

```bash
jq '.cachedGrowthBookFeatures.tengu_auto_mode_config' ~/.claude.json
```

**出力例：**

```json
{
  "enabled": "disabled",
  "twoStageClassifier": true
}
```

| フィールド | 値 | 意味 |
|-----------|-----|------|
| `enabled` | `"enabled"` | auto mode 使用可能 |
| `enabled` | `"disabled"` | まだロールアウトされていない |
| `twoStageClassifier` | `true` | 2段階判断（AI判断層 + セーフガード層）が有効 |

> **参考**: github.com/anthropics/claude-code/issues/33587

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

### ブラウザ操作の最適設計

ブラウザ操作は **毎回LLMに探索させるのではなく、コードベースに定型化する** のが正解。

```
┌─────────────────────────────┐
│  定型操作（コードベース）     │  ← pyautogui / Playwright
│  速い・安い・確実             │
│  通常時はこちらが実行         │
└─────────────┬───────────────┘
              ↓ 異常時のみ
┌─────────────────────────────┐
│  LLM がハンドリング          │  ← Claude Code
│  UI変更・想定外エラー対応     │
└─────────────────────────────┘
```

**設計原則**：
- **通常時**: コードが実行（トークン消費ゼロ、高速）
- **異常時**: LLMが判断（UI変更、エラー等の例外処理のみ）
- **探索**: 初回だけLLMで操作手順を特定 → コードに落とす

```python
# 例：Playwright で定型化したブラウザ操作
from playwright.sync_api import sync_playwright

def login_and_export(url, username, password):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        page.fill('#username', username)
        page.fill('#password', password)
        page.click('#login-button')
        page.wait_for_selector('#dashboard')
        # 定型操作をここに書く
        page.click('#export-button')
        page.wait_for_download()
        browser.close()
```

> Computer Use で毎回スクショ→判断させるのはコストの無駄。
> 定型化できるものはコードにして、LLMは「例外処理係」に徹させる。

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

## 6. Gmail & Google Calendar 連携

### なぜ全人類がやるべきか

Claude Code から直接メールと予定を操作できる。MCP サーバー経由で連携するだけ。

| 連携 | 具体例 |
|------|--------|
| **Gmail → Claude Code** | 「未読メールを要約して」「この件に返信案を書いて」 |
| **Calendar → Claude Code** | 「今日の予定を確認して」「来週の空き時間を探して」 |
| **Gmail + Calendar** | 「メールの内容から会議を予定に入れて」 |
| **コードと連動** | 「デプロイ完了をチームにメールで通知して」 |

### セットアップ

```jsonc
// ~/.claude/settings.json
{
  "mcpServers": {
    "google": {
      "command": "npx",
      "args": ["-y", "@anthropic/google-mcp-server"],
      "env": {
        "GOOGLE_CLIENT_ID": "your_client_id",
        "GOOGLE_CLIENT_SECRET": "your_client_secret",
        "GOOGLE_REFRESH_TOKEN": "your_refresh_token"
      }
    }
  }
}
```

### Google Cloud Console での準備

1. **Google Cloud Console** でプロジェクトを作成
2. **Gmail API** と **Google Calendar API** を有効化
3. **OAuth 2.0 クライアント ID** を作成（デスクトップアプリ）
4. クライアント ID・シークレットを取得
5. OAuth フローで **リフレッシュトークン** を取得
6. 上記の設定に値を入力

### 活用パターン

```
朝の作業開始時：
「今日の予定を確認して、未読メールも要約して」

コード作業完了後：
「このPRの内容をチームにメールで共有して」

会議準備：
「明日の会議の議題をメールから抽出して、
 前回の会議メモと合わせてブリーフィングを作って」
```

### Slack連携との組み合わせ

```
Slack で指示
  ↓
Claude Code が Gmail/Calendar を操作
  ↓
結果を Slack に返す
```

スマホの Slack からでもメール処理や予定管理が可能になる。

---

## 7. まとめ：Claude Code エコシステム全体像

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
│  │  Slack / Gmail / Google Calendar          │    │
│  │  (MCP サーバー経由で連携)                  │    │
│  └──────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
```

---

## 更新履歴

- 2025-03-25: 初版作成
- 2025-03-25: Gmail & Google Calendar 連携セクションを追加
