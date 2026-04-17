# Claude Code CLI インストールマニュアル（MacBookNEO / M1 Mac 8GB）

本稿は **MacBookNEO（M1 MacBook Air 8GB、macOS 26.5）** に Claude Code CLI を導入する手順をまとめたもの。
2026-04-05 に実施済みの現行セットアップをリバースエンジニアリングした上で、Windows PC（MASU-P55）での教訓を反映した完全版。

**この手順は人間が手動で実行することも、AI エージェント（Claude Desktop Code mode / Codex Computer Use / Manus My Computer）に依頼して自動実行させることも可能です。** エージェントに依頼する場合は次節 0 のプロンプト例を使用。

---

## 0. AI エージェントへの依頼（新規 Mac セットアップ時）

MacBookNEO で **Claude Desktop / Codex / Manus** のいずれかを先に起動して本人がサインイン済みなら、下記プロンプトをそのまま貼ってインストールを一任できる。

### 0.1 共通プロンプト（どのエージェントでも使える）

```
https://wirelessml.github.io/test/docs/claude-code-install-macbookneo.html
の手順に従って、この Mac に Claude Code CLI を**スタンドアロン版で**インストールしてください。

必須ルール:
1. npm 版は絶対に入れない（§2.3）。
2. パスは ~/.local/bin/claude、データは ~/.local/share/claude に置く（§3.1）。
3. OAuth 認証は私が手動でブラウザに入力するので、claude コマンド初回起動までやったら待機してください（§4.1〜4.2）。
4. `~/.claude/settings.json` は §5.1 の現行内容をそのまま書き込んでください（`CLAUDE_CODE_DISABLE_1M_CONTEXT` は**削除**したまま）。
5. インストール後に `claude --version` と `claude doctor` の出力を私に見せてください。

途中で権限ダイアログが出たら止めて私に確認してください。シェル操作は可能な限り最小限の承認範囲で。
```

### 0.2 エージェント別の補足

- **Manus（My Computer）**: 自律実行が最も得意。上記プロンプトをそのまま投げれば、Terminal 起動 → `curl` 実行 → 認証前ステップまで完走する想定。
- **Codex（Computer Use）**: Terminal.app を事前に「常に許可するアプリ」へ追加しておくと都度承認ダイアログが減る（§11 相当、本手順内では不要）。
- **Claude Desktop Code mode**: ローカル Mac を操作する場合は SSH 越しが基本のため、自機を `localhost` SSH 先として登録するか、代わりにメイン会話でコマンドを出してもらって手動コピペする運用が無難。

### 0.3 エージェント実行時の最小コマンド列（監視用）

エージェントが何を打っているか確認したいときの対応。下記5行で認証直前まで到達する。

```bash
curl -fsSL https://claude.ai/install.sh | bash
export PATH="$HOME/.local/bin:$PATH"
claude --version
mkdir -p ~/.claude
# settings.json は §5.1 から転記
```

認証以降（§4.2）は人間が手動で行う前提。

---

## 1. 概要

| 項目 | 値 |
|---|---|
| **インストール方式** | **スタンドアロン版（native）推奨** — npm版はメモリ事故・更新競合のリスクあり |
| **バイナリ場所** | `~/.local/bin/claude` → `~/.local/share/claude/versions/<VERSION>` |
| **設定ディレクトリ** | `~/.claude/`（共通）/ `~/.claude.json`（プロジェクト別） |
| **認証方式** | Claude Pro / Max OAuth（Keychain保存）or `ANTHROPIC_API_KEY` |
| **現行版** | 2.1.112（2026-04-17 時点） |
| **初回起動** | 2026-04-04T22:30 UTC（= 2026-04-05 07:30 JST）|

### 選定根拠（スタンドアロン版）

- **npm版のリスク**:
  - グローバルインストールで `@anthropic-ai/claude-code` が `node_modules` に依存 → Node.js 更新・`npm cache clean` 等の副作用で壊れる
  - Windows PC（MASU-P55）で「npm版とスタンドアロン版が共存 → 自動更新が競合」の事故実績（2026-04-14対応済）
  - M1 8GB では npm run時の Node.js プロセスが余計なRAMを食う
- **スタンドアロン版の利点**:
  - 単一バイナリ（約200MB）、依存なし
  - `autoUpdates: false` でも、CLIがバックグラウンドで新版をDL → 次回起動時に symlink 差し替え
  - アンインストールは `rm -rf ~/.local/share/claude ~/.local/bin/claude ~/.claude ~/.claude.json` だけ

---

## 2. 前提条件

### 2.1 必須

```bash
# macOS バージョン
sw_vers -productVersion   # 26.5 以上が望ましい（12以上なら動く）

# アーキテクチャ
uname -m                   # arm64（M1 Mac）

# shell
echo $SHELL                # zsh（Macデフォルト）
```

### 2.2 推奨（入れておくと便利）

- **Homebrew 5.x**: `brew --version` — `brew install cloudflared` 等の補助ツール用。必須ではない
- **Node.js 20+**: `node -v` — MCP サーバーの一部が Node.js 系。現環境 v22.15.0
- **Git 2.x**: `git --version` — Claude Code が自動的にgit状態を拾う
- **gh CLI 2.x**: `gh --version` — GitHub操作を Claude Code から呼ぶとき便利
- **PATH確認**: `~/.local/bin` が PATH に含まれていること
  ```bash
  echo $PATH | tr ':' '\n' | grep -q "$HOME/.local/bin" && echo OK || echo MISSING
  ```
  無ければ `~/.zshrc` に追記:
  ```bash
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
  source ~/.zshrc
  ```

### 2.3 絶対に避けるもの

- **`sudo npm install -g @anthropic-ai/claude-code`** — 使うな。システム領域に入ると更新不能になる
- **複数ユーザーで共有する導入**（例: `/usr/local/bin` へのコピー）— 設定衝突の温床

---

## 3. インストール

### 3.1 公式インストーラ（スタンドアロン版）

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

実行内容:
1. macOS/Linux を検出
2. `~/.local/share/claude/versions/<LATEST>` にバイナリを配置
3. `~/.local/bin/claude` → 最新版への symlink を作成
4. shell プロファイル（`~/.zshrc`）に PATH を追記（既に通っていればスキップ）

**所要時間**: 約30秒（200MB DL）

### 3.2 確認

```bash
which claude              # /Users/yuika/.local/bin/claude
claude --version          # 2.1.112 (Claude Code)
ls -la ~/.local/share/claude/versions/
# -rwxr-xr-x  1 yuika  staff  203956832 Apr 17 05:02 2.1.112
```

### 3.3 代替: Homebrew 経由（非推奨）

```bash
brew install claude-ai/tap/claude  # ※2026-04 時点で公式 tap は未提供
```

→ **使わない**。公式インストーラに従うこと。

---

## 4. 初回起動・認証

### 4.1 起動

```bash
cd ~/Desktop           # 作業ディレクトリへ
claude                 # 対話セッション開始
```

### 4.2 認証（Claude Max 契約済みの場合）

1. `/login` コマンド or 起動時プロンプトで OAuth URL が表示される
2. ブラウザで `https://console.anthropic.com/oauth/authorize?...` が開く
3. claude.ai アカウント（`wirelessml@gmail.com`）でログイン
4. 「Claude Code がアクセスを要求しています」→ **許可**
5. ブラウザに `localhost:XXXXX` へリダイレクト → CLI に戻り認証完了
6. **Keychain に OAuth トークンが保存される**（サービス名: `Claude Code-credentials`）

### 4.3 API キー認証（Max 契約を使わない場合のみ）

```bash
export ANTHROPIC_API_KEY="sk-ant-..."  # ~/.zshrc に追記
claude  # API キー認証モードで起動
```

※ Max 契約があるなら OAuth のほうが安い（週次リミット内は無料感覚）

### 4.4 認証状態の確認

```bash
claude /login status   # 対話セッション内で実行
# → "Logged in as wirelessml@gmail.com (Max plan)"
```

---

## 5. 推奨設定（`~/.claude/settings.json`）

### 5.1 現行の設定内容

```json
{
  "env": {
    "CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1",
    "CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING": "1",
    "CLAUDE_CODE_SUBAGENT_MODEL": "sonnet"
  },
  "permissions": {
    "allow": ["*"]
  },
  "enabledPlugins": {
    "claude-mem@thedotmack": true,
    "code-review@claude-plugins-official": true,
    "github@claude-plugins-official": true,
    "frontend-design@claude-plugins-official": true,
    "superpowers@claude-plugins-official": true,
    "ui-ux-pro-max@ui-ux-pro-max-skill": true
  },
  "effortLevel": "high",
  "showThinkingSummaries": true,
  "skipDangerousModePermissionPrompt": true,
  "bypassPermissions": true
}
```

### 5.2 各設定の意味

| キー | 意味 | 本機設定 |
|---|---|---|
| `CLAUDE_CODE_DISABLE_AUTO_MEMORY` | `~/.claude/projects/*/memory/` 自動メモリを無効化（git管理を優先） | `1` |
| `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING` | Opus 4.7 の適応的思考を固定化 | `1` |
| `CLAUDE_CODE_SUBAGENT_MODEL` | サブエージェントの既定モデル | `sonnet` |
| `permissions.allow: ["*"]` | 全ツール自動許可（プロンプト省略） | 有効 |
| `effortLevel` | 思考深度（low/medium/high/xhigh/max） | `high` |
| `showThinkingSummaries` | 思考要約を表示 | `true` |
| `bypassPermissions` | 危険モード常時有効 | `true` |
| `skipDangerousModePermissionPrompt` | 危険モードの確認プロンプト省略 | `true` |

### 5.3 1M context を有効化（Max プラン向け）

**削除済み**（2026-04-17）：以前は `CLAUDE_CODE_DISABLE_1M_CONTEXT` を設定していたが、削除して 1M 有効化。
`settings.json` に**含めない**ことで既定の 1M が効く。

```json
// ❌ これは書かない
"env": { "CLAUDE_CODE_DISABLE_1M_CONTEXT": "1" }
```

### 5.4 プラグイン・マーケットプレイス

```json
"extraKnownMarketplaces": {
  "thedotmack": { "source": { "source": "github", "repo": "thedotmack/claude-mem" } },
  "ui-ux-pro-max-skill": { "source": { "source": "github", "repo": "nextlevelbuilder/ui-ux-pro-max-skill" } }
}
```

追加する場合:
```bash
claude /plugin install <marketplace>:<plugin-id>
```

---

## 6. プロジェクト別設定（`~/.claude.json`）

### 6.1 構造

```json
{
  "installMethod": "native",
  "autoUpdates": false,
  "theme": "dark-ansi",
  "firstStartTime": "2026-04-04T22:30:41.651Z",
  "claudeCodeFirstTokenDate": "2026-02-28T23:46:48.733765Z",
  "userID": "b53efdc4e56621dd02b061487d61b023f08745bd5211dfd851d1fefa7af5c8a0",
  "projects": {
    "/Users/yuika/Desktop": {
      "mcpServers": { ... },
      "history": [...]
    }
  }
}
```

### 6.2 MCP サーバー登録（例）

```bash
# chrome-devtools MCP（ブラウザ制御）
claude mcp add chrome-devtools --url https://chrome-devtools.example/sse

# google-photos MCP（カスタム）
claude mcp add google-photos -- node /path/to/google-photos-mcp/index.js \
  --env GOOGLE_PHOTOS_TOKENS_PATH=/Users/yuika/Desktop/google-photos-mcp/tokens.json

# computer-use MCP
claude mcp add computer-use -- python3 /path/to/computer-use-server.py
```

登録後は `claude /mcp` で接続確認。

### 6.3 MCPサーバーを**削除**する場合（メモリ節約）

2026-04-17 12:00 に実施済み：
- User-scope（`~/.claude.json` の `mcpServers`）から削除: `context7`, `notebooklm-mcp`, `voicemode`
- Desktop project-scope から削除: `chrome-devtools`, `google-photos`, `playwright`
- バックアップ: `~/.claude.json.bak.20260417-1215`

```bash
# 個別削除
claude mcp remove <name>

# 一括確認
claude mcp list
```

---

## 7. モデル選択・コンテキスト

### 7.1 利用可能モデル（2026-04時点）

| モデル | ID | 用途 | 料金感（Max枠消費） |
|---|---|---|---|
| **Opus 4.7 (1M)** | `claude-opus-4-7[1m]` | メイン、複雑タスク | 重い（Max週次で上限接触） |
| **Opus 4.7 (default)** | `claude-opus-4-7` | 一般タスク | 中〜重 |
| **Sonnet 4.6** | `claude-sonnet-4-6` | サブエージェント | 軽 |
| **Haiku 4.5** | `claude-haiku-4-5-20251001` | 高頻度・軽作業 | 最軽 |

### 7.2 モデル切替

```bash
# セッション内で切替
/model opus
/model opusplan   # Opus思考 + Sonnet実行（推奨）
/model sonnet
/model haiku

# 起動時に指定
claude --model opus
claude --model claude-opus-4-7
```

### 7.3 `/model opusplan` の意味

- **思考（計画・推論）** = Opus 4.7（高品質）
- **実行（ツール呼び出し）** = Sonnet 4.6（高速・低コスト）
- Max プランのリミット消費を抑えつつ、計画精度を保つ設定
- **本機の標準運用**

---

## 8. よく使うコマンド

### 8.1 対話セッション内スラッシュコマンド

| コマンド | 用途 |
|---|---|
| `/model <name>` | モデル切替 |
| `/mcp` | MCP 接続確認 |
| `/skill` | スキル一覧 |
| `/login status` | 認証状態確認 |
| `/logout` | ログアウト |
| `/plugin install <id>` | プラグイン追加 |
| `/fast` | 高速モード（Opus 4.6 のみ） |
| `/rc` | リモートコントロール（本環境固有） |
| `/btw` | Side chat |
| `Esc` 2回 | 会話履歴から1ターン前へ戻る |

### 8.2 起動オプション

```bash
claude -c                              # 直前セッションを継続
claude --continue                      # 同上
claude --fork-session -c               # 継続+新セッションID
claude -p "質問"                       # 一問一答モード（非対話）
claude --add-dir /path/to/other        # 追加ディレクトリを許可
claude --bare                          # 最小モード（hook/LSP/plugin無効）
claude --model opus --effort max       # 明示指定
```

### 8.3 ログ・セッション確認

```bash
# セッションログ
ls -lt ~/.claude/projects/-Users-yuika-Desktop/*.jsonl | head

# shell snapshots
ls ~/.claude/shell-snapshots/

# debug ログ
ls ~/.claude/debug/

# 認証情報（中身は見ない）
ls -la ~/.claude/.credentials.json
```

---

## 9. アップデート

### 9.1 自動更新の挙動

- `autoUpdates: false` でも CLI 内部で新版チェック → バックグラウンドDL
- 新版は `~/.local/share/claude/versions/X.Y.Z` に配置
- **次回起動時に symlink が最新へ差し替わる**
- 過去バージョン 2〜3世代は残存、それ以前は自動削除

### 9.2 手動確認

```bash
# 現在バージョン
claude --version

# 利用可能な全バージョン
ls ~/.local/share/claude/versions/

# symlink 確認
ls -la ~/.local/bin/claude
```

### 9.3 強制アップデート

```bash
# 公式インストーラを再実行
curl -fsSL https://claude.ai/install.sh | bash
```

### 9.4 ダウングレード（2世代前に戻す）

```bash
# 例: 2.1.112 → 2.1.110 へ戻す
ln -sf ~/.local/share/claude/versions/2.1.110 ~/.local/bin/claude
claude --version   # 2.1.110 を確認
```

---

## 10. トラブルシュート

### 10.1 `claude: command not found`

- PATH 設定漏れ: `export PATH="$HOME/.local/bin:$PATH"` を `~/.zshrc` に追加
- shell 再起動: `source ~/.zshrc` または新しいターミナル

### 10.2 OAuth 認証が通らない

- Keychain ロック: `security unlock-keychain ~/Library/Keychains/login.keychain-db`
- トークン破損: `rm ~/.claude/.credentials.json` → 再`/login`
- ブラウザがローカルに戻れない: Safari で localhost リダイレクトを許可

### 10.3 起動時に Bun クラッシュ（Segmentation fault）

**Windows PC（MASU-P55）で発生、Mac でも稀にあり**:
- 原因: メモリ不足（M1 8GB で他アプリ多い状態）
- 対処: OBS / Claude Desktop / Chrome を終了 → 再起動
- 恒久対策: **Claude Desktop を常用しない**（本環境は 4/14 で停止済）

### 10.4 1M context が効かない

- `~/.claude/settings.json` の `env` から `CLAUDE_CODE_DISABLE_1M_CONTEXT` を**削除**
- **環境変数は起動時に読まれる** → 既存セッションは影響なし、新セッションから有効化
- 確認: 起動時の環境情報に `Opus 4.7 (1M context)` と表示されれば OK

### 10.5 MCP サーバーが接続失敗

```bash
claude /mcp   # 各サーバーの状態確認
claude --mcp-debug   # デバッグモード起動
```

- STDIOモードの MCP で `.env` 読み込み失敗 → MCP 側の `dotenv.config()` に `__dirname` ベースの path を指定（本環境の google-photos-mcp で対応済）

### 10.6 "Claude Code Usage Limit Reached"

- Max プランの週次/月次リミット到達
- 対処:
  - 待つ（週次は毎週木曜リセット）
  - `claude --model sonnet` で軽いモデルに切替
  - `/model opusplan` で消費を抑える
  - 最終手段: API キー認証へ切替（従量課金）

### 10.7 セッションが固まる

```bash
# Claude プロセスを確認
ps aux | grep -i claude | grep -v grep

# 固まったセッションを kill
pkill -f "claude$"
```

---

## 11. プラグイン・スキル運用

### 11.1 現在有効なプラグイン

```json
"enabledPlugins": {
  "claude-mem@thedotmack": true,                       // セッション横断メモリ検索
  "code-review@claude-plugins-official": true,         // PR レビュー
  "github@claude-plugins-official": true,              // GitHub 統合
  "frontend-design@claude-plugins-official": true,     // UI設計
  "superpowers@claude-plugins-official": true,         // ブレスト・デバッグ等
  "ui-ux-pro-max@ui-ux-pro-max-skill": true            // UI/UX 特化
}
```

### 11.2 よく使うスキル

| スキル | 用途 |
|---|---|
| `mem-search` | 過去セッション検索 |
| `make-plan` → `do` | 多段実装 |
| `video-use` | 動画編集 |
| `agent-reach` | Web/SNS 調査 |
| `superpowers:brainstorming` | 要件探索 |
| `superpowers:systematic-debugging` | デバッグ |

### 11.3 プラグイン追加

```bash
# マーケット経由
claude /plugin install <marketplace>:<plugin-id>

# カスタムマーケット追加
# settings.json の extraKnownMarketplaces に追記 → 再起動
```

---

## 12. アンインストール

### 12.1 完全アンインストール

```bash
# バイナリ削除
rm -rf ~/.local/share/claude
rm ~/.local/bin/claude

# 設定・セッション削除
rm -rf ~/.claude
rm ~/.claude.json

# Keychain からトークン削除
security delete-generic-password -s "Claude Code-credentials"

# PATH 設定を ~/.zshrc から手動削除
```

### 12.2 設定だけリセット（再インストール準備）

```bash
# バックアップを作成
cp ~/.claude/settings.json ~/.claude/settings.json.bak
cp ~/.claude.json ~/.claude.json.bak

# リセット
rm ~/.claude/settings.json
rm ~/.claude.json

# 次回起動時にオンボーディングが走る
```

---

## 13. 推奨運用ルーチン

1. **セッション開始時**:
   - `/model opusplan` で実行モデル確認
   - `/rc` でリモートコントロール報告（本環境固有）
2. **作業中**:
   - `claude-mem` スキルで過去知見を参照
   - MCP は必要最小限のみ接続（メモリ節約）
3. **セッション終了時**:
   - `git add -A && git commit` で CLAUDE.md 等を保存
   - 重い MCP は `claude /mcp remove` で外す
4. **週次メンテ**:
   - `~/.local/share/claude/versions/` の古いバイナリ確認
   - `~/.claude/projects/*/` のセッションログ肥大化チェック

---

## 14. 参考: Windows PC（MASU-P55）との比較

| 項目 | MacBookNEO | MASU-P55 |
|---|---|---|
| OS | macOS 26.5 | Windows 11 25H2 |
| バージョン | 2.1.112 | 2.1.105（2026-04-14 時点） |
| 方式 | standalone (native) | standalone (npm版は削除・ブロック済) |
| 自動更新 | 内部機構（autoUpdates:false） | タスクスケジューラ（毎日0:00） |
| 認証 | Keychain | Windows 資格情報マネージャー |
| SSH | 不要（ローカル） | `gci_admin@100.125.21.47:22`（Tailscale経由）|
| WSL | N/A | WSL Ubuntu 24.04 + portproxy 0.0.0.0:2222 |

---

## 15. 参考リンク

- 公式インストーラ: https://claude.ai/install.sh
- Claude Code ドキュメント: `claude --help`
- 本環境の関連ドキュメント:
  - `docs/claude-code-tips-2025.md` — 活用Tips
  - `docs/claude-computer-use-guide.md` — Computer Use MCP
  - `docs/claude-notebooklm-integration.md` — NotebookLM 連携
  - `youtube-live-manual.md` — Windows→Mac 配信マニュアル
  - `CLAUDE.md` — プロジェクト全体コンテキスト

---

**作成日**: 2026-04-17
**対象機**: MacBookNEO（M1 MacBook Air 8GB, macOS 26.5）
**現行バージョン**: Claude Code 2.1.112
**初回起動**: 2026-04-05 07:30 JST
