# ブラウザ自動化CLI比較（2026年4月時点）

情報源: @hayato_1dev のX投稿 + 各リポジトリ調査

## 総合ランキング（はやと評価）

| 順位 | ツール | 評価 |
|------|--------|------|
| 1 | dev-browser | 速さ・安定性・柔軟性のバランスが一番いい |
| 2 | agent-browser | AI特化でかなり強い |
| 3 | playwright-cli | 公式で安心だけど実測は重め |
| 4 | browser-use CLI | 定常操作は速いけど起動が荒い |

---

## 1. dev-browser（総合1位）

- **GitHub**: https://github.com/SawyerHood/dev-browser
- **作者**: Sawyer Hood
- **スター**: ~5,600
- **言語**: TypeScript
- **インストール**: `npm install -g dev-browser` → `dev-browser install`
- **最新**: v0.2.6（2026/4/1）

### 特徴
- QuickJS WASMサンドボックスでスクリプト実行（安全）
- Playwright APIをフル活用
- ページ永続化（複数スクリプト間で状態維持）
- 起動中のChromeに自動接続、またはChromium新規起動
- `--headless` モード対応

### Claude Code連携
- MCP不要。Bashツールから直接実行
- 設定: `Bash(dev-browser *)` を許可リストに追加
- エージェントに「use dev-browser」と伝えるだけ

### 使い方
```bash
dev-browser --headless <<'EOF'
const page = await browser.getPage("main");
await page.goto("https://example.com");
const title = await page.title();
console.log(title);
EOF
```

---

## 2. agent-browser（AI特化）

- **GitHub**: https://github.com/vercel-labs/agent-browser
- **作者**: Vercel Labs
- **スター**: ~28,400
- **言語**: Rust（ネイティブバイナリで高速）
- **インストール**: `npm install -g agent-browser` → `agent-browser install`
  - Homebrew: `brew install agent-browser`
  - Cargo でも可
- **最新**: v0.25.3（2025/4/7）

### 特徴
- アクセシビリティツリーベースのスナップショット（DOMの約93%トークン削減）
- 要素を @e1, @e2 等のrefで指定
- 50以上のコマンド対応
- ヘッドレスChromium / プロファイル付きChrome / クラウドリモートの3モード
- `agent-browser chat` でAI対話型操作
- Discord・VSCode・Slack対応（Electronアプリ全般）
- Playwrightより圧倒的にトークン消費が少ない

### Claude Code連携
- `.claude-plugin` ディレクトリ同梱、スキルとして統合可能

---

## 3. playwright-cli（Playwright MCP）

- **GitHub**: https://github.com/microsoft/playwright-mcp
- **作者**: Microsoft公式（Playwrightチーム）
- **スター**: ~30,500
- **パッケージ**: `@playwright/mcp`

### 特徴
- アクセシビリティツリーで操作（ビジョンモデル不要）
- Snapshot Mode（デフォルト）とVision Mode（Canvas等用）
- スナップショット 2-5KB vs スクショ 500KB-2MB

### Claude Code連携
```bash
claude mcp add playwright npx @playwright/mcp@latest
```

### 課題（「重め」の理由）
- 典型タスクで約114Kトークン消費
- 大きなページではMCPレスポンスが50K+トークンに
- 複数クライアント時のメモリ・CPU消費
- 軽量化フォーク `fast-playwright-mcp` が存在する点が重さの証左

---

## 4. browser-use CLI

- **GitHub**: https://github.com/browser-use/browser-use
- **作者**: Gregor Zunic
- **スター**: ~86,800（最多）
- **言語**: Python
- **インストール**: `pip install browser-use` → `browser-use install`
- **最新**: v0.12.6（2026/4/2）

### 特徴
- open/click/type/screenshot/state等のコマンド
- デーモン常駐でコマンド間レイテンシ約50ms
- ヘッドレス・既存プロファイル・クラウドの3モード

### Claude Code連携
```bash
claude mcp add browser-use -- uvx --from 'browser-use[cli]' browser-use --mcp
```

### 課題（「起動が荒い」の理由）
- 初回openは約3.2秒
- ページ読み込み+LLM推論で1.3秒〜9秒台のブレ
- 「見る→考える→動く」設計のため1アクション数秒

---

## うちの環境での使い分け

| 用途 | ツール | 理由 |
|------|--------|------|
| 普段使い（メイン） | dev-browser | CLAUDE.mdで設定済み。速い・安定・Bash直接実行 |
| AI特化・大規模自動化 | agent-browser | トークン効率◎、Vercel製で信頼性高い |
| 既存MCP環境 | playwright-mcp | 現在セットアップ済み（重いが安定） |

## メモ
- dev-browserは既にCLAUDE.mdでブラウザ自動化の優先ツールとして設定済み
- agent-browserは要検討（Rust製で速い、Claude Code連携が良い）
- browser-useはPython依存なので環境によっては導入しにくい
