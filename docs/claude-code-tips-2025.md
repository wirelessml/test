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

## 7. Claude Code Schedule（自動タスク実行）

### 概要

指定した時間間隔で、Claude がリポジトリに対して自動的にタスクを実行する機能。**PCもサーバーも不要**。

### 何がすごいのか

| 特徴 | 内容 |
|------|------|
| **PC不要** | Anthropicのクラウド上でサンドボックスが起動。PCの電源を切っていても、寝ていても動く |
| **サーバーレス** | EC2/VPS不要。インフラ管理ゼロ。終わったらサンドボックスは消える |
| **API代金不要** | Pro プラン（$20/月）に含まれる。API従量課金なら20万円以上かかる処理もゼロ |
| **セットアップ** | GitHub リポジトリ + CLAUDE.md だけ。CI/CD設定もDockerfileも不要 |

### 対応プラン

Pro / Max / Team / Enterprise すべて対応。Claude Code で開発しているなら**追加費用ゼロ**。

### 実践例：CS対応とバグ修正の全自動化

```
Schedule（定期実行）
    ↓
サポートチケットを検出
    ↓
バグの原因を特定
    ↓
コード修正 → コミット → 自動返信（resolve）
    ↓
Slackにレポートを通知
```

**実際の自動対応レポート例：**

```markdown
## サポートチケット処理サマリー (2026-03-26)

### チケット1: 日記データの不具合
- アクション: バグ修正 + 自動返信 (resolve)
- 内容: 2月24日以前の日記が表示されない不具合。
  初回ロード時に最新30件を取得し、含まれる全月を
  「フェッチ済み」とマークするため、境界月の古い
  エントリが追加読み込みされなかった。
- コード修正: `app/[locale]/journal/page.tsx`
- コミット: 86c620e (main)
```

チケット受付 → バグ特定 → コード修正 → ユーザーへ返信 → Slack報告まで**全自動・人間の介入ゼロ**。

### CS自動対応のAPI設計

シンプルな3エンドポイント構成：

```
Schedule（定期実行）
    ↓
GET  /api/cron/support-tickets
    ↓ 未対応チケット + FAQ一覧を取得
    ↓
Claude が内容を分析・コード修正が必要か判断
    ↓
├── コード修正必要 → POST /api/cron/github-proxy（バグ修正・コミット）
├── FAQ で対応可能 → POST /api/cron/support-reply（自動返信）
└── 判断できない   → POST /api/cron/support-reply（エスカレーション）
```

| エンドポイント | メソッド | 役割 |
|---------------|----------|------|
| `/api/cron/support-tickets` | GET | 未対応チケット + FAQ一覧を返す |
| `/api/cron/support-reply` | POST | チケットに返信 or エスカレーション |
| `/api/cron/github-proxy` | POST | GitHub API のプロキシ（コード読み書き用） |

```typescript
// /api/cron/support-tickets/route.ts の例
export async function GET(req: Request) {
  // cron secret で認証（不正アクセス防止）
  if (req.headers.get('x-cron-secret') !== process.env.CRON_SECRET) {
    return Response.json({ error: 'Unauthorized' }, { status: 401 });
  }

  // 未対応のチケットを取得
  const tickets = await db.supportTicket.findMany({
    where: { status: 'open' },
    include: { messages: true },
  });

  // FAQ一覧を取得（Claude が回答に使う）
  const faq = await db.faq.findMany();

  return Response.json({ tickets, faq });
}
```

```typescript
// /api/cron/github-proxy/route.ts の例
export async function POST(req: Request) {
  if (req.headers.get('x-cron-secret') !== process.env.CRON_SECRET) {
    return Response.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const { action, ...params } = await req.json();

  // action: 'read_file' | 'list_files' | 'commit_file' | 'create_branch' | ...
  const result = await githubApi(action, params);
  return Response.json(result);
}
```

**ポイント**：
- `x-cron-secret` ヘッダーで認証（Schedule からのアクセスのみ許可）
- FAQ をセットで返すことで、Claude が既存の回答パターンを参照して返信
- チケットに `messages` を含めることで、過去のやり取りも考慮した返信が可能
- `github-proxy` で Claude がコードの読み書き・コミットまで実行可能（バグ修正の全自動化）

### その他の活用例

| ユースケース | 説明 |
|-------------|------|
| **定期コードレビュー** | 毎日PRをチェックしてレビューコメント |
| **依存関係の更新** | 週1でパッケージ更新チェック＆PR作成 |
| **セキュリティスキャン** | 定期的に脆弱性をスキャン＆修正 |
| **ドキュメント更新** | コード変更に合わせてドキュメント自動更新 |
| **CS対応** | サポートチケットの自動対応＆バグ修正 |

### セットアップ

Claude Code に一言伝えるだけ：

```
「このリポジトリで毎時サポートチケットを確認して対応する
 スケジュールを作って（schedule機能で）。
 環境変数に CRON_SECRET を設定して。」
```

### CLAUDE.md の指示書テンプレート

CLAUDE.md に以下のような自然言語の指示を書くだけで、Schedule が自動実行する：

```markdown
# CLAUDE.md
## サポート自動対応（Schedule 用）

### 毎時やること

1. サポートチケット確認
   WebFetch で GET https://yourapp.vercel.app/api/cron/support-tickets を叩く。
   ヘッダー: x-cron-secret: （環境変数 CRON_SECRET）

2. 各チケットを判断
   - FAQ で答えられる → 返信文を作成 → POST /api/cron/support-reply
   - バグの可能性 → ソースコードを読んで原因特定 → 修正コミット
     → ユーザーに修正完了の返信
   - 返金/解約/課金系 → エスカレーション（管理者にメール通知）
```

**CI/CD設定もコードも不要。自然言語の指示書だけで全自動化が動く。**

### CLAUDE.md テンプレート例2：PR自動レビュー

```markdown
# CLAUDE.md
## PR自動レビュー（Schedule 用）

### 毎時やること：PRレビュー
1. WebFetch で GitHub API を叩き、open な PR 一覧を取得
2. 各 PR の diff を取得し、以下の観点でレビュー：
   - セキュリティ（SQL injection, XSS, 認証漏れ）
   - パフォーマンス（N+1クエリ, 不要な再レンダリング）
   - ロジックバグ（境界値, null チェック漏れ）
3. 指摘がある場合、PR にコメントを投稿
```

### PR自動レビューのAPI実装例

```typescript
// /api/cron/github-reviews/route.ts
export async function GET(req: Request) {
  // open な PR を返す
  const pulls = await fetch(
    'https://api.github.com/repos/you/app/pulls?state=open',
    { headers: { Authorization: `token ${process.env.GITHUB_PAT}` } }
  ).then(r => r.json());

  return Response.json({ pulls });
}

export async function POST(req: Request) {
  // レビューコメントを投稿
  const { pull_number, body } = await req.json();
  await fetch(
    `https://api.github.com/repos/you/app/pulls/${pull_number}/reviews`,
    {
      method: 'POST',
      headers: { Authorization: `token ${process.env.GITHUB_PAT}` },
      body: JSON.stringify({ body, event: 'COMMENT' }),
    }
  );
  return Response.json({ ok: true });
}
```

| エンドポイント | メソッド | 役割 |
|---------------|----------|------|
| `/api/cron/github-reviews` | GET | open な PR 一覧を返す |
| `/api/cron/github-reviews` | POST | PR にレビューコメントを投稿 |

**必要な環境変数**: `GITHUB_PAT`（GitHub Personal Access Token）

### CLAUDE.md テンプレート例3：X（Twitter）自動投稿

```markdown
# CLAUDE.md
## X 自動投稿（Schedule 用）

### 毎日やること：X 投稿
1. git log で直近24時間のコミットを確認
2. ユーザーに価値がある変更があれば、投稿文を作成
   - 140字以内、カジュアルなトーン
   - 関連するハッシュタグを2-3個
3. WebFetch で POST /api/cron/post-tweet に送信
```

開発の進捗を自動で発信。マーケティングも Schedule で自動化できる。

```typescript
// /api/cron/post-tweet/route.ts
export async function POST(req: Request) {
  const { text } = await req.json();

  await fetch('https://api.twitter.com/2/tweets', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${process.env.TWITTER_BEARER}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ text }),
  });

  return Response.json({ ok: true });
}
```

**必要な環境変数**: `TWITTER_BEARER`（Twitter API Bearer Token）

### CLAUDE.md テンプレート例4：広告運用の自動最適化

```markdown
# CLAUDE.md
## 広告運用自動化（Schedule 用）

### 毎時やること：広告運用
1. WebFetch で GET /api/cron/ad-performance を叩く
2. 各キャンペーンの CTR, CPA, ROAS を確認
3. 判断と実行：
   - CTR が過去7日平均の50%以下 → クリエイティブを自動差し替え
   - CPA が目標の150%超 → キャンペーンを一時停止
   - ROAS が1.0未満 → 即座に配信停止
4. 実行した内容を POST /api/cron/slack-notify で Slack に報告
```

| 指標 | 閾値 | アクション |
|------|------|-----------|
| CTR | 過去7日平均の50%以下 | クリエイティブ差し替え |
| CPA | 目標の150%超 | キャンペーン一時停止 |
| ROAS | 1.0未満 | 即座に配信停止 |

広告費の無駄遣いを24時間自動で監視。人間が寝ている間も異常を検知して即対応。

```typescript
// /api/cron/ad-operations/route.ts
export async function GET(req: Request) {
  // Google Ads API からキャンペーンデータ取得
  const campaigns = await googleAdsClient.report({
    query: `SELECT campaign.name, campaign.id, metrics.clicks,
            metrics.impressions, metrics.cost_micros, metrics.conversions
            FROM campaign WHERE segments.date DURING LAST_7_DAYS`,
  });

  return Response.json({
    campaigns: campaigns.map(c => ({
      id: c.campaign.id,
      name: c.campaign.name,
      ctr: c.metrics.clicks / c.metrics.impressions,
      cpa: c.metrics.cost_micros / 1e6 / c.metrics.conversions,
      roas: c.metrics.conversions_value / (c.metrics.cost_micros / 1e6),
    })),
  });
}

export async function POST(req: Request) {
  const { action, campaignId, creativeId } = await req.json();

  if (action === 'pause') {
    // キャンペーンを一時停止
    await googleAdsClient.campaigns.update({
      campaignId, status: 'PAUSED',
    });
  } else if (action === 'swap_creative') {
    // クリエイティブを差し替え
    await googleAdsClient.adGroupAds.update({
      campaignId, adId: creativeId, status: 'ENABLED',
    });
  }

  return Response.json({ ok: true });
}
```

| エンドポイント | メソッド | 役割 |
|---------------|----------|------|
| `/api/cron/ad-operations` | GET | キャンペーンの CTR/CPA/ROAS を返す |
| `/api/cron/ad-operations` | POST | 一時停止 or クリエイティブ差し替え |

**必要な環境変数**: Google Ads API の認証情報

### CLAUDE.md テンプレート例5：アプリレビュー自動対応

```markdown
# CLAUDE.md
## アプリレビュー対応（Schedule 用）

### 毎日やること：レビュー対応
1. WebFetch で GET /api/cron/app-reviews を叩く
2. 星3以下のレビューに対して：
   - 問題の内容を分類（バグ / 要望 / 使い方の誤解）
   - バグなら修正も行う
   - 丁寧で共感的な返信文を作成
3. POST /api/cron/reply-review で返信を送信
```

| 分類 | アクション |
|------|-----------|
| **バグ** | コード修正 → コミット → 修正完了の返信 |
| **要望** | GitHub Issue を作成 → 検討中の返信 |
| **使い方の誤解** | 正しい使い方を案内する返信 |

低評価レビューを放置すると評価が下がり続ける。自動対応で即座にフォローすることでユーザーの印象を改善。

```typescript
// /api/cron/app-reviews/route.ts
export async function GET(req: Request) {
  // App Store Connect API でレビュー取得
  const reviews = await fetch(
    `https://api.appstoreconnect.apple.com/v1/apps/${APP_ID}/customerReviews`,
    { headers: { Authorization: `Bearer ${generateJWT()}` } }
  ).then(r => r.json());

  // 未返信 & 星3以下をフィルタ
  const unreplied = reviews.data.filter(
    (r: any) => r.attributes.rating <= 3 && !r.relationships.response.data
  );

  return Response.json({ reviews: unreplied });
}
```

| エンドポイント | メソッド | 役割 |
|---------------|----------|------|
| `/api/cron/app-reviews` | GET | 未返信 & 星3以下のレビューを返す |
| `/api/cron/reply-review` | POST | レビューに返信を送信 |

**必要な環境変数**: App Store Connect API の認証情報（JWT生成用）

### トリガーの管理

Schedule で作成されたトリガーは以下のURLで管理できる：

```
https://claude.ai/code/scheduled/（トリガーID）
```

確認できること：実行履歴、次回実行予定、トリガーの編集・停止・削除、ログ

### CLAUDE.md テンプレート例6：Grok X検索で競合・業界モニタリング

xAI API（Grok）を使えば、X のリアルタイム検索を Schedule で自動化できる。

**xAI API セットアップ**：
1. https://console.x.ai/ にアクセス
2. X アカウントでサインイン
3. 「Create your first API key」から API キーを発行

```markdown
# CLAUDE.md
## 競合・業界モニタリング（Schedule 用）

### 毎日やること：X 検索 & レポート
1. xAI API（Grok）で以下のキーワードを X 検索
   - 自社プロダクト名・競合名
   - 業界トレンドキーワード
2. 重要な投稿をピックアップ（バズってる投稿、ネガティブな言及）
3. 日次レポートを作成し POST /api/cron/slack-notify で Slack に通知
```

**必要な環境変数**: `XAI_API_KEY`（xAI API キー）

---

## 8. feature-dev プラグイン（設計フェーズの自動化）

### 概要

Anthropic公式プラグイン。インストール数 131,475件超。コードを書く前に「何を、なぜ、どう作るか」をAIが整理してくれる。

### 7フェーズの自律実行

```
/feature-dev を起動
    ↓
1. 既存コードの発見
2. コードベースの探索
3. 要件の明確化
4. アーキテクチャ設計
5. 実装
6. 品質レビュー
7. 最終サマリー
```

### 3つの専門エージェント

| エージェント | 役割 |
|-------------|------|
| **code-explorer** | 既存コードのパターンを解析 |
| **code-architect** | 実装アプローチを比較・提案 |
| **code-reviewer** | バグ・セキュリティ・規約違反を信頼度スコア付きで検出 |

3つのエージェントが**並列**で動作するため高速。

### なぜ重要か

> 間違った設計を速く実装しても意味がない。
> 正しい設計を最初から定義できれば、実装は半分以下の時間で終わる。

- ソロ開発者でもチーム開発並みのレビュープロセスが走る
- 「コードを書く速さ」より「設計の正確さ」で競争する時代
- AIコーディングの競争は「速い実装」から「正しい設計を素早く固める」へ移行

---

## 9. dev-browser（Playwright ベースのブラウザ操作）

### 概要

Claude Code のエージェントに Playwright ベースのブラウザ操作を追加する CLI ツール。`npm install` して使える。

### 特徴

| 特徴 | 内容 |
|------|------|
| **Playwright API** | スクショに頼らず DOM ベースで操作（Computer Use より高速・正確） |
| **QuickJS WASM サンドボックス** | 安全に実行される |
| **状態保持** | ページの状態が保持されるため、複数ステップの操作を継続可能 |
| **snapshotForAI** | AI 向けに最適化されたスナップショットを返す |

### ブラウザ操作ツール比較

| ツール | 方式 | 速度 | 精度 | 用途 |
|--------|------|------|------|------|
| Computer Use | スクショ→判断 | 遅い | 視覚依存 | 動的・探索的 |
| pyautogui | 座標/画像マッチ | 速い | 座標依存 | 定型繰り返し |
| **dev-browser** | Playwright API | 速い | DOM依存で正確 | 開発中のブラウザ確認・テスト自動化 |

### 使い方

```bash
# インストール
npm install -g dev-browser
dev-browser install  # Playwright + Chromium をセットアップ
```

**GitHub**: github.com/SawyerHood/dev-browser

### Claude Code との統合

```jsonc
// .claude/settings.json に追加（毎回の確認をスキップ）
{
  "permissions": {
    "allow": [
      "Bash(dev-browser *)"
    ]
  }
}
```

### 利用可能なAPI

| グローバルオブジェクト | 用途 |
|----------------------|------|
| `browser.getPage()` | ページを取得 |
| `browser.listPages()` | 全ページ一覧 |
| `saveScreenshot()` | スクリーンショット保存 |
| `page.goto()` | URL遷移 |
| `page.click()` | クリック |
| `page.fill()` | フォーム入力 |

スクリプトは QuickJS WASM サンドボックス内で実行されるため、ホスト環境へのアクセスはなく安全。

開発中に「ブラウザ開いて確認して」を口頭で頼む感覚で使える。

---

## 10. Claude Code on the Web（ブラウザ版）

### 概要

Claude Code がブラウザ上で動作する。PCにターミナルがなくても、スマホからでもClaude Codeが使える。

**アクセス**: https://claude.ai/code

### 主要機能

#### Auto-fix PR（PRの自動修正）— "PRを出して寝る"が現実に

Claude が PR を監視し、CI の失敗やレビューコメントを自動で修正・push する。Auto-merge と組み合わせれば「朝起きたらPRが片付いてる」世界。

```
従来：PR出す → CI落ちる → ログ読む → 直す → push → また落ちる → 直す → …

Auto-fix：PR出す → Auto-fix ON → 寝る → 朝グリーン
```

**有効化方法**：
1. claude.ai/code でリポジトリを開く
2. PR を選択
3. 「Auto-fix」トグルを ON にする
4. （推奨）Auto-merge も ON にすると、全チェック通過後に自動マージ

**対応するトリガー**：
- CI/CD の失敗（テスト失敗、lint エラー、ビルドエラー）
- レビューコメント（修正リクエスト）

**3段階の判定ロジック（暴走しない設計）**：

| 判定 | 例 | アクション |
|------|-----|-----------|
| **明確な修正** | テスト期待値のずれ、lint エラー | 自動 push |
| **曖昧な要求** | 設計判断を伴うもの | 人間に確認 |
| **重複イベント** | 同じ CI 失敗の連続通知 | スキップ |

レビューコメントへの返信も Claude が自動で行うが、投稿はあなたの **GitHub アカウント名義**（"Claude Code" ラベル付き）。証跡がちゃんと残る。

**`--remote` との組み合わせ**：`claude --remote` でクラウド実行すれば、PCを閉じても fix が走り続ける。モバイルアプリからも進捗確認・指示が可能。

**競合との比較**：

| ツール | アプローチ | 自動修正 |
|--------|-----------|---------|
| **Claude Code Auto-fix** | 検知→分析→修正→push→CI再実行を自動完結 | 完全自動 |
| GitHub Copilot Autofix | 行単位の提案→人間が承認 | 半自動 |
| Cursor BugBot | 問題検出が中心 | 限定的 |

**個人開発者へのインパクト**：CI修正に30分取られるのは個人開発では致命的。Auto-fix が軽微な CI 失敗を自動処理するだけで、その30分を機能開発に回せる。

**注意点**：
- 対応プラン：Pro / Max / Team / Enterprise
- トークン消費は通常の Claude Code 利用と共有
- 大量の PR を並列 fix するとレートリミットに注意

#### `--remote` フラグ（ターミナル → Web に移行）

ローカルのターミナルで開始したセッションを Web に引き継げる。

```bash
# ローカルで開始
claude --remote

# URLが発行される → ブラウザで開いて続行
```

長時間かかるタスクをローカルで始めて、PCを閉じてスマホから監視・続行できる。

#### `/teleport`（Web → ターミナルに移行）

Web で作業中のセッションをローカルターミナルに引き継ぐ。逆方向の移行。

```
Web で作業中
    ↓
/teleport コマンドを実行
    ↓
ローカルターミナルで続行
```

### クラウド環境

Web 版の Claude Code はクラウドのサンドボックス環境で動作する。

#### セットアップスクリプト

リポジトリに `.claude/setup.sh` を配置すると、クラウド環境の初回起動時に自動実行される。

```bash
# .claude/setup.sh の例
#!/bin/bash
npm install
pip install -r requirements.txt
```

#### SessionStart フック

`.claude/settings.json` の `hooks` で `SessionStart` イベントにコマンドを設定できる。

```jsonc
// .claude/settings.json
{
  "hooks": {
    "SessionStart": [
      {
        "command": "npm install && npm run build"
      }
    ]
  }
}
```

#### ネットワークアクセス

クラウド環境からは外部APIへのアクセスが可能。ただし、セキュリティのためサンドボックス化されている。

### セキュリティと分離

- 各セッションは独立したサンドボックスで実行
- リポジトリのクローンは読み取り専用ではなく、変更・コミット・プッシュが可能
- 環境変数はプロジェクト設定で管理
- セッション終了後にサンドボックスは破棄される

### 使い分け

| シナリオ | 推奨環境 |
|---------|---------|
| PCで本格的に開発 | ローカルターミナル |
| スマホから PR 修正 | Web 版 (auto-fix) |
| 長時間タスクの実行 | `--remote` → Web で監視 |
| 外出先からコードレビュー | Web 版 |
| CI 修正の自動化 | Web 版 (auto-fix) |

---

## 11. git worktree はAIが自動管理する時代

### 従来の問題

`git worktree` は並行開発に便利だが、手動管理が面倒だった：

```bash
# 従来：人間が手動で管理
git worktree add ../feature-branch feature-branch
# 作業後...
git worktree remove ../feature-branch
git worktree prune
```

ブランチごとにディレクトリを作り、終わったら cleanup する——この手間が地味に積み重なる。

### 現在：AIが自動で活用・管理

| ツール | worktree の扱い |
|--------|----------------|
| **Codex** | 並行タスクで自動的に worktree を作成・活用 |
| **Claude Code** | サブエージェントが worktree を使って並行実行 |
| **Windsurf** | 別の方向性で独自に活用 |

- **作成**: 並行タスク実行時に AI が自動で worktree を作成
- **活用**: 複数ブランチの作業を同時並行で実行
- **cleanup**: 作業完了後に AI が自動で片付け

> `git worktree` コマンドを人間が打つ必要がなくなった。AI が裏で勝手にいい感じに使ってくれる。

### なぜ重要か

- 並行開発の速度が上がる（複数PRを同時に作業可能）
- worktree の作成・削除・prune を意識しなくてよい
- AI にとっては「ファイルシステムの衝突を避けて並行作業する」ための自然な手段

---

## 12. マルチエージェントハーネス設計（Anthropic 公式ブログ）

### 概要

Anthropic が公開した「Harness design for long-running application development」。1〜4文の簡潔なアイデアから、人間の介入なしで約6時間で完全なフルスタックアプリを自動構築する方法。

**出典**: Anthropic Engineering Blog（2026年3月24日）

### GAN 着想の3エージェント構成

```
ユーザーの一言（例: 「2Dレトロゲームメーカーを作成」）
    ↓
┌──────────────────┐
│  Planner（計画者） │  → 1〜4文を16機能の完全な製品仕様に展開
└────────┬─────────┘
         ↓
┌──────────────────┐
│ Generator（生成者）│  → 機能を1つずつ実装（React + Vite + FastAPI + SQLite）
└────────┬─────────┘
         ↓
┌──────────────────┐
│ Evaluator（評価者）│  → Playwright で実際にクリックして検証
└────────┬─────────┘
         ↓ 失敗なら
    Generator に戻る（自動修正ループ）
```

### 各エージェントの役割

| エージェント | 役割 | 詳細 |
|-------------|------|------|
| **Planner** | 仕様展開 | 簡潔なプロンプトをプロジェクト概要・ターゲットユーザー・10スプリントの完全仕様に自動展開。仕様は意図的に高レベルに保ち、詳細は後段で決定 |
| **Generator** | 実装 | 機能を1つずつ選択して実装。各実装後にセルフ評価。Git でバージョン管理 |
| **Evaluator** | 品質検証 | Playwright でユーザーのようにUI操作・API テスト・DB 状態確認。問題を特定して Generator にフィードバック |

### Evaluator が検出する問題の例

```
✗ 矩形塗りつぶしツールが、ドラッグ開始/終了点にのみタイルを配置
  （意図はドラッグ領域全体を塗りつぶす）

✗ 削除キーハンドラが複合条件を要求、ただしクリックで一部だけ設定される

✗ FastAPIルートのマッチング順序エラー
  （'reorder'が整数パラメータとして解釈される）

✗ オーディオ録音はスタブのみ
  （ボタン切り替えだが実際のマイク入力なし）
```

### 単一エージェント vs フルハーネスの比較

| 項目 | 単一エージェント | フルハーネス |
|------|-----------------|------------|
| 実行時間 | 20分 | 6時間 |
| コスト | $9 | $200 |
| 機能 | 基本エディタ（バグ多数） | 完全な機能セット |
| ゲームプレイ | **完全に壊れている** | **実際にプレイ可能** |

### DAW（デジタルオーディオワークステーション）の実例（V2 / Opus 4.6）

| フェーズ | 実行時間 | コスト |
|---------|---------|-------|
| Planner | 4.7分 | $0.46 |
| Build R1 | 2時間7分 | $71.08 |
| QA R1 | 8.8分 | $3.24 |
| Build R2 | 1時間2分 | $36.89 |
| QA R2 | 6.8分 | $3.09 |
| Build R3 | 10.9分 | $5.88 |
| QA R3 | 9.6分 | $4.06 |
| **合計** | **3時間50分** | **$124.70** |

3ラウンドの Build → QA サイクルで自動的に品質が収束。

### 主要な失敗モードと対策

| 失敗モード | 内容 | 対策 |
|-----------|------|------|
| **コンテキスト喪失** | タスクが長いほど一貫性が低下 | コンテキストリセット（圧縮より有効） |
| **コンテキスト不安** | 文脈限界に近づくと早期に作業終了 | リセットで「不安」を解消 |
| **自己評価偏向** | 自分の出力を楽観的に評価 | 別エージェント（Evaluator）による評価 |

> **重要な教訓**：「Claude はデフォルトでは貧弱な QA エージェント。自分の出力を褒める傾向がある」。複数ラウンドのプロンプト調整で改善。

### フロントエンドデザインの評価基準

| 基準 | 内容 | 重み |
|------|------|-----|
| Design Quality | 色・タイポ・レイアウトの統一性 | 高 |
| Originality | カスタム決定・テンプレート回避 | 高 |
| Craft | 技術実行・間隔・色調和 | 中 |
| Functionality | ユーザビリティ | 中 |

デザインループは 5〜15回の反復で、スコアが伸びない場合は美学的方向を完全に転換する。

### ハーネス設計の原則

> 「最も単純な解決策を見つけ、必要になるまで複雑性を増やさない。
> 新モデル登場時にハーネスを再検査し、負荷を掛けていないコンポーネントを削除する。」

- V1（Opus 4.5）：スプリント分割 + 契約交渉が必要だった
- V2（Opus 4.6）：モデル改善によりスプリント構成を**廃止**。単一の長時間実行で対応可能に
- **AI エンジニアの役割**は「次の新しい組み合わせを常に見つけること」

---

## 13. まとめ：Claude Code エコシステム全体像

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
│  │ Computer │  │ pyautogui│  │ dev-browser   │  │
│  │ Use      │  │ (定型)   │  │ (Playwright)  │  │
│  │ (動的)   │  │          │  │               │  │
│  └──────────┘  └──────────┘  └───────────────┘  │
│                                                   │
│  ┌──────────┐  ┌──────────────────────────────┐  │
│  │Subcon-   │  │ feature-dev (設計自動化)      │  │
│  │scious    │  │ explorer/architect/reviewer   │  │
│  └──────────┘  └──────────────────────────────┘  │
│                                                   │
│  ┌──────────────────────────────────────────┐    │
│  │  Schedule (自動タスク実行・PC不要)         │    │
│  └──────────────────────────────────────────┘    │
│                                                   │
│  ┌──────────────────────────────────────────┐    │
│  │  Slack / Gmail / Google Calendar          │    │
│  │  (MCP サーバー経由で連携)                  │    │
│  └──────────────────────────────────────────┘    │
│                                                   │
│  ┌──────────────────────────────────────────┐    │
│  │  Claude Code on the Web                    │    │
│  │  auto-fix / --remote / /teleport           │    │
│  └──────────────────────────────────────────┘    │
│                                                   │
│  ┌──────────────────────────────────────────┐    │
│  │  マルチエージェントハーネス                  │    │
│  │  Planner / Generator / Evaluator           │    │
│  └──────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
```

---

## 更新履歴

- 2025-03-25: 初版作成
- 2025-03-25: Gmail & Google Calendar 連携セクションを追加
- 2025-03-26: Claude Code Schedule（自動タスク実行）セクションを追加
- 2025-03-27: feature-dev プラグイン、dev-browser セクションを追加
- 2025-03-27: Claude Code on the Web（ブラウザ版）セクションを追加
- 2025-03-27: マルチエージェントハーネス設計（Anthropic公式ブログ）セクションを追加
- 2025-03-27: git worktree AI自動管理セクションを追加
- 2026-03-30: 隠れた便利機能15選、プランモード活用法を追加

---

## 14. 隠れた便利機能15選

あまり知られていないが強力な機能一覧。

### モバイル・クロスデバイス

| 機能 | 説明 |
|------|------|
| モバイルアプリ | Codeタブから使用可能 |
| `/teleport` / `claude --teleport` | セッションをモバイル・Web・デスクトップ・ターミナル間で移動 |
| `/remote-control` | リモートコントロール（全セッション有効化可能） |

### 自動化・スケジュール

| 機能 | 説明 |
|------|------|
| `/loop` | ワークフローをSkillsにしてループ化（例: `/loop 5m /foo`） |
| `/schedule` | cron式で定期実行をスケジュール |
| Hooks | エージェントのライフサイクルにロジック挿入 |
| Cowork Dispatch | Desktopアプリの遠隔操作 |

### 開発ツール

| 機能 | 説明 |
|------|------|
| Chrome拡張機能 | フロントエンド開発支援 |
| 内蔵ブラウザ | DesktopアプリでWebサーバー自動起動＆テスト |
| `claude -w` | git worktreeで複数のClaudeを並列稼働 |
| `/batch` | 大量の変更を並列処理（大規模マイグレーション向け） |
| `--bare` | SDK起動を最大10倍高速化 |
| `--add-dir` / `/add-dir` | 他のフォルダを追加（権限も自動付与） |
| `--agent=名前` | `.claude/agents`に独自Agent定義、カスタムプロンプト＆ツールセット |

### セッション管理

| 機能 | 説明 |
|------|------|
| `/branch` | セッションをfork（CLIなら `claude --resume <id> --fork-session`） |
| `/btw` | メイン作業を止めずに横で素早く質問 |
| `/voice` | 音声入力（CLIはスペースバー長押し、Desktopは音声ボタン、iOSはdictation） |

---

## 15. プランモード活用法

### 問題

いきなり実行させると見当違いの方向に進んで全部やり直しになるケースがある。

### 正解の手順

1. **プランモードで計画だけ出させる** — ファイルは一切触らせない
2. **計画を確認して「これでいい」と承認**
3. **承認してから初めて実行**

これだけで手戻りがほぼゼロになる。

### CLAUDE.md に自動化ルールを書く

```markdown
# 作業ルール
- 新しいタスクを開始する前に、必ずプランモードで計画を提示すること
- 計画が承認されるまでファイルの変更は行わないこと
```

CLAUDE.mdにこのルールを書いておくと、毎回自動的にプランモードから入るようになる。

### 効果

- **手戻りほぼゼロ**
- **作業速度が体感2倍**
- 方向性の間違いを事前に防げる

---

## 16. ターミナル vs デスクトップアプリ：速度とトークン効率

### 結論

**ターミナル（CLI）で動かした方が実行スピードが速く、トークン消費が少ない。**

### デスクトップアプリとの比較

| 項目 | ターミナル（CLI） | デスクトップアプリ |
|------|-----------------|------------------|
| 実行スピード | 速い | やや遅い |
| トークン消費 | 少ない | 多い（UI描画分のオーバーヘッド） |
| 慣れ | 必要 | 初心者向き |
| 推奨 | 慣れてきたら | 最初はこちら |

### 推奨ステップ

1. **初心者**: デスクトップアプリで慣れる
2. **慣れてきたら**: Antigravityでターミナルを使う、またはPCで直接ターミナルからClaudeを呼び出す
3. **上級者**: `--bare` フラグで起動高速化、`-w` でworktree並列稼働

---

## 17. ccsl（Claude Code Status Line）— コンテキスト使用率の可視化

### 問題

長時間セッションでコンテキストが肥大すると精度が落ちる。しかし使用率が見えないため、いつリセットすべかわからない。

### 解決策：ccsl を導入

GitHub: https://github.com/usedhonda/statusline

**表示内容（4行のステータスライン）：**

| 行 | 内容 |
|----|------|
| 1行目 | モデル名・Gitブランチ・ディレクトリ・メッセージ数・変更行数・コスト |
| 2行目 | **コンテキストウィンドウ使用率**（プログレスバー付き） |
| 3行目 | 過去5時間のセッション利用状況・トークン数 |
| 4行目 | 週単位の使用パターン・予算残額 |

**コンテキスト警告：**
- **80%超え**: 黄色警告 → **強制リセット推奨**
- **90%超え**: 赤色警告 → 精度低下が顕著

### インストール

```bash
# Homebrew（推奨）
brew install usedhonda/tap/ccsl

# pip
pip install ccsl
```

### 運用ルール

- コンテキスト使用率を常に可視化
- **80%超えたら強制リセット**（新しいセッションを開始）
- これにより精度低下を防ぎ、トークンの無駄遣いも回避

## 18. /rc（Remote Control）— iPhoneからCLIを遠隔操作

### 問題

Mac で Claude Code CLI を起動中、手元の iPhone から操作を続けたい。
SSH の設定は面倒で、Desktop アプリの Cowork/Dispatch は CLI とは別機能。

### 解決策：/rc コマンド

Claude Code CLI 内蔵のリモートコントロール機能。コマンド1つでセッション共有。

**手順：**
1. Mac の **Terminal.app** で `claude` を起動
2. `/rc` と入力（`/remote-control` の省略形）
3. セッション URL と QR コードが表示される
4. iPhone の Claude アプリで QR コードをスキャン
5. そのまま操作可能（Computer Use 含む）

**主な特徴：**

| 項目 | 詳細 |
|------|------|
| 会話履歴 | 引き継がれる |
| セットアップ | `/rc` と入力するだけ |
| 外出先から | 接続可能（Wi-Fi不問） |
| 名前付きセッション | `/rc プロジェクト名` |
| 全セッション有効化 | `/config` で設定可能 |

**要件：** Pro / Max / Team / Enterprise プラン、v2.1.51 以降

**他の方法との比較：**

| 方法 | 手軽さ | 外出先 | Computer Use | 会話引継ぎ |
|------|--------|--------|-------------|-----------|
| **/rc** | ★★★ | ✅ | ✅ | ✅ |
| SSH | ★★ | △ | ✅ | ❌ |
| Web版(claude.ai/code) | ★★★ | ✅ | ❌ | ❌ |
| Dispatch(Desktop) | ★★ | ✅ | ✅ | ❌ |

### 注意点

- 初回は `/mcp` に computer-use が表示されない場合がある → Terminal.app で一度有効化すれば、以降は Cursor 内でも利用可能
- **Cursor でも Computer Use + /rc の両方が動作することを確認済み**（2026年4月5日）
