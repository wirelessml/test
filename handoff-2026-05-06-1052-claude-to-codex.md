# Claude Code → Codex 引き継ぎ書

> **作成**: 2026-05-06 (水・振替休日) 10:52 JST
> **発行元**: Claude Code (Opus 4.7 1M, Mac M1 8GB)
> **送り先**: Codex (新規課金)
> **理由**: 負荷分散
> **形式**: Codex に「このファイルを読んで」と指示すれば文脈再構築可能

---

## 0. 立ち上げ手順 (Codex 側で最初にやること)

```bash
# 1. このリポジトリを把握する
cat /Users/yuika/Desktop/CLAUDE.md           # プロジェクト糊 (~270 行)
cat /Users/yuika/Desktop/docs/journal/2026-05-06.md  # 本日のフルログ
cat /Users/yuika/Desktop/handoff-2026-05-06-1052-claude-to-codex.md  # この引き継ぎ書

# 2. 現状確認
git status   # 未コミット差分を把握
git log -10  # 直近のコミット履歴

# 3. ユーザー情報 (仲氏結成)
# CLAUDE.md の「ユーザー情報」「機材」セクション参照
```

---

## 1. 仲氏プロファイル (要点のみ、詳細は CLAUDE.md)

- **氏名**: 仲啓輔 (50 歳、無職、雇用保険受給なし)
- **筆名**: 仲啓輔 (Substack)、@minimalistneko (X)、wirelessml (GitHub)
- **家族**: 妻 + 長女 結花 (12 歳/小 6) + 次女 彩羽 (10 歳/小 4) = 4 人
- **居住**: 神戸市須磨区養老町 1-5-7 カムール養老 101 (公開ファイルには書かない)
- **ミニマムライフコスト**: 約 ¥136,288/月 (一人当たり ¥34,072)
- **メイン作業**: コワーキング MASU-p (神戸市須磨区板宿) 据え置きしゅん先生 PC + 持ち運び M1 MacBook Air
- **メールアドレス**: wirelessml@gmail.com (主)

---

## 2. 機材 3 台構成

| 機材 | 役割 | OS / スペック |
|---|---|---|
| **M1 MacBook Air 8GB** | 持ち運び・司令塔 | macOS Darwin 25.5.0 |
| **しゅん先生 PC** | コワーキング据え置きメイン | Windows 11 25H2 Experimental Channel Build 26300.8346, Intel i7-8700K, 16GB, Acer FA100 NVMe 512GB (4/29 移行) |
| **MASU-P55 (HP ProBook)** | コワーキングサブ | Windows 11 25H2 GA, WSL2 Ubuntu, OpenClaw 稼働 |

詳細: `docs/machines/*.md`

---

## 3. 本セッション (Claude Code 側) の完了事項

### 3.1 なかそにー Instagram 状態確認 (5/6 7:51〜10:50)

**プロフィール変化**:
- 投稿 635 件 (不変)
- フォロワー 2.8 万 (不変)
- フォロー中 **668 → 676 人** (+8、20 分間)
- ハイライト「note」1 つ (不変、固定)
- アクティブストーリー無 (`stories/<user>/` が profile に redirect)

**投稿 12 件 URL 全取得**:

| # | shortcode | 概要 |
|---|---|---|
| 1 | DUu_OQok27b | MY Profile (自己紹介、ピン留め推定) |
| 2 | DX9FnIfCRFi | ミニマルライフコスト 7.5 万円 (5/6 朝既分析) |
| 3 | DX6g-WGCXM9 | **Less is Moreなマインドセット✍️** (5/4 20:00 JST) |
| 4 | DX38H8UiZbH | **朝活が続かない自分を責めない話** (5/3 20:00 JST) |
| 5-12 | DX1c3uBpjTY 等 | reel/post 混合、概要未取得 |

スクショ保存: `ai-minimalist-shibu/knowledge/screenshots/nakasoniii-2026-05-06/post3-DX6g-WGCXM9.png` / `post4-DX38H8UiZbH.png`

ジャーナル追記: `docs/journal/2026-05-06.md` 末尾の「追補 7」

### 3.2 勝間和代 X 投稿確認 (5/5 21:25)

URL: <https://x.com/kazuyo_k/status/2051775214359568393>

> 「SuperWhisperを使ってるのは同じですが、WhisperモデルはOpenAIのWhisperからElevenLabのScribeにしています。こっちの方がさらに優秀。」

**意義**: 仲氏が 4/29 16:30 にコワーキングで物理セットアップした **SuperWhisper + ElevenLabs Scribe (BYO key, $0/月) 構成**は、勝間本人の 5/5 公式言及と完全一致。仲氏の判断が 6 日先取り。

### 3.3 学んだこと (重要発見)

1. **🚨 chrome-devtools-mcp は macOS Chrome の Default プロファイル共有**: cookie/session が共有されるため IG / X / Threads などログイン状態保持。`evaluate_script` で DOM 直接抽出が圧倒的に効率的。代替ルート (osascript + screencapture) は不要に。
2. IG profile は SSR で grid を含まない (lazy load)
3. stories URL は active が無いと profile redirect
4. cliclick で Chrome window に hover 可能 (computer-use の tier "read" 制限と独立)

---

## 4. 持ち越しタスク (Codex で続行候補)

### A. なかそにー深掘り (低優先・任意)

- [ ] 投稿 3 (DX6g-WGCXM9) caption 全文展開 (「続きを読む」クリック → 全文抽出)
- [ ] 投稿 4 (DX38H8UiZbH) caption 全文展開 (同上)
- [ ] 残り投稿 5-12 (DX1c3uBpjTY ~ DT-LAMbE74M) の概要取得
- [ ] note.com/nakasoniii のブログ確認 (本人の長文記事)
- [ ] Threads @nakasoniii_minimal の最新投稿確認
- [ ] `ai-minimalist-shibu/knowledge/nakasoniii-snapshot.md` 専用ファイル新規作成 (minimalist-jun-snapshot.txt パターン)

**実行時のヒント**:
```bash
# Codex から直接 IG にアクセスする場合 (login 状態が必要)
# - Mac 上の Chrome Default プロファイル経由が確実
# - chrome-devtools-mcp をインストール済み (`claude mcp add` 同等の Codex 対応 MCP がある場合)
# - もしくは `open -a "Google Chrome" "<URL>"` + osascript で navigate + screencapture
```

### B. 期限ありタスク (高優先)

- [ ] **🔥 しぶコーチング応募フォーム送信** (締切 **本日 5/6 23:59**)
  - Google Forms 入力済、写真 10 枚撮影済、残り「アップロード + 送信ボタン」のみ
  - 詳細: `docs/journal/2026-05-04.md`
- [ ] 整理収納アドバイザー 1 級 2 次試験申込 (5/7 以降、ハウスキーピング協会 HP)
  - CBT 受験 / 2021-06-10 / 受験地域 入力
  - 1 次合格有効期限の協会確認
  - 詳細: `docs/projects/seiri-shu-nou-advisor-1.md`
- [ ] 体験報告書 本文 10 ページ執筆 (Word + Claude for Word、3 週間想定)
  - Saved Prompt 設計済 (`docs/projects/seiri-shu-nou-advisor-1.md`)
  - 表紙・図表 10 個全完成済 (`~/Desktop/*.html`)

### C. Substack 連投ネタ (中優先)

仲氏は Substack 「仲啓輔」名義で発信中。連投候補:

1. 「Microsoft が 30 年前を AI で蘇らせる 2026 年春」シリーズ
   - edit コマンド再降臨 (Rust + Windows 25H2 標準バンドル)
   - イルカのカイル AI 化復活 (Copilot Keyboard)
2. 「勝間 voice stack を 6 日先取りした話」 (今日の発見)
3. 「なかそにー: 朝活ミニマリスト 28K の月 7.5 万円生活」 (3 者比較ネタ)
4. 「Tailscale なしで SSH 復活」 (masu-p55 LAN 経路)
5. 「Windows 11 が ARM と x86 で別れた日」 (26H1 = Bromine)
6. 「@hoshino_aisales ファクトチェック 2 連発」 (Artifacts + Projects RAG)

詳細: `docs/journal/2026-05-06.md` の「Substack ネタ集」+ 過去ジャーナル

### D. 物理タスク (コワーキング着席時)

- [ ] masu-p55 のカイル表示確認 (再ログオンで Appearance.exe 自動起動)
- [ ] BIOS 整理 (CSM 無効化 + 旧 HDD の Boot Manager エントリ削除)

---

## 5. 利用可能リソース

### 5.1 開発環境

| ツール | バージョン | 用途 |
|---|---|---|
| Claude Code CLI | v2.1.128 (3 台統一) | このセッション |
| **Codex (新規)** | — | **引き継ぎ先 (これから稼働)** |
| Manus | v1.5.3 | 自律タスク (普段は閉じる) |
| Claude for Word | Anthropic 公式アドイン | 体験報告書執筆 |
| microsoft/edit | v2.0.0 (3 台統一) | CLI エディタ |
| SuperWhisper | Pro Lifetime | 音声入力 |
| ElevenLabs Scribe | Starter (5/11 失効) | Whisper モデル代替 |
| yt-dlp / ffmpeg / deno | 全機統一済 | YouTube 字幕 / 動画 DL |

### 5.2 MCP サーバー (Mac、user scope 永続)

- chrome-devtools-mcp (CLI 設置済、Chrome Default プロファイル共有)
- playwright
- peekaboo
- claude-mem mcp-search (観察記録 DB)
- Gmail / Google Calendar (claude.ai connector)
- マネーフォワード会計

### 5.3 Mac CLI

- `cliclick` (homebrew) — マウス制御 (computer-use の tier 制限と独立)
- `osascript` — Chrome navigate (`tell application "Google Chrome" to set URL of active tab of front window to "..."`)
- `screencapture -R x,y,w,h` — 領域キャプチャ (Retina 2x になる)
- `gh` (GitHub CLI) — Issue/PR 管理
- `agent-browser` — Rust 高速ブラウザ自動化 (要 supervisor 完全停止: `pkill -9 -f "agent-browser-darwin"`)

### 5.4 ナレッジベース

| 場所 | 内容 |
|---|---|
| `CLAUDE.md` | プロジェクト糊、ユーザー情報、運用ルール |
| `docs/journal/YYYY-MM-DD.md` | 日次作業ログ (今日: 2026-05-06.md、追補 7 まで) |
| `docs/machines/` | M1/しゅん先生 PC/MASU-P55 詳細 |
| `docs/projects/` | 整理収納 1 級・しぶ chatbot 等 |
| `docs/rules/` | 操作規約・コーディング規約・情報保存方針 |
| `docs/reminders.md` | 期限・解約日 |
| `ai-minimalist-shibu/knowledge/` | しぶエコ観察ナレッジ (人物相関・FAQ・参照動画・ミニマルライフコスト 3 者比較) |

---

## 6. 重要な運用ルール (CLAUDE.md 抜粋)

1. **記事の削除や一括更新前は件数を報告して確認** (それ以外は確認不要)
2. **金銭トランザクション (発注・送金・取引) は代行しない** — 必ず仲氏が最終クリック
3. **読んでいないコードは変更するな** — Read で内容確認してから編集
4. **サブエージェント成果物は必ず自分で検証してから報告** — 丸投げ禁止
5. **メモリ機能は使用しない** — 情報はすべて git 管理ドキュメントに
6. **Gmail ラベル/フィルタは作らない** — 検索クエリベース運用 (4/28 確定)
7. **会話中の知見は毎回 git に保存する**
8. **セッション開始時にターミナル最前面化** (SkyLight Python ワンライナー、`docs/rules/session-setup.md`)
9. **しぶ・なかそにー 等の固有名詞には敬意を持って観察する** (アンチではなく中立観察者として)

---

## 7. ユーザー (仲氏) との会話スタイル

- 日本語で短く、要点を箇条書き or テーブルで
- 確認が必要なときは件数 + 影響範囲を明示
- 提案は 2-3 個の選択肢で出して指示を仰ぐ
- 進捗は「✅完了」「📝進行中」「⏸️持ち越し」で記号統一
- 仲氏は意思決定が早く具体的、回りくどい説明は不要

---

## 8. 直近で仲氏が興味を持っている対象

- **なかそにー** (Instagram @nakasoniii_minimal、note.com/nakasoniii) — しぶエコ周辺の朝活ミニマリスト、5/6 朝に発見
- **しぶ** (@minimalist_sibu / sibu_minimalist) — メイン観察対象、5/6 23:59 締切でコーチング応募中
- **勝間和代** voice stack — SuperWhisper + ElevenLabs Scribe 戦略の確証
- **microsoft/edit + Copilot Keyboard / カイル** — Microsoft 30 年前リバイバル
- **整理収納 1 級 2 次審査** — 体験報告書執筆中 (Word + Artifact 図表 10 個完成)
- **Substack 連載** — 仲啓輔名義で連投候補

---

## 9. Claude Code 側で続けるか不明な作業 (Codex に渡したいかは仲氏次第)

このセッション (Claude Code) は引き継ぎ完了で待機状態に入る。仲氏が:
- 「Claude は終了で OK」 → このセッションを閉じる
- 「Claude も並行で X やって」 → 別タスク振り分け
- 「Claude は休憩、Codex 主導」 → 待機継続

を選んで指示。

---

## 10. 引き継ぎ書投入手順 (仲氏向け)

1. Codex Desktop App を起動 (`open -a Codex` または Dock から)
2. 新規セッション開始
3. 以下のいずれか:
   - **A. 全文貼り付け**: このファイルを Cmd+A → Cmd+C → Codex に Cmd+V
   - **B. ファイル参照**: 「このファイルを読んでから始めて: `/Users/yuika/Desktop/handoff-2026-05-06-1052-claude-to-codex.md`」と指示
4. Codex が文脈再構築 → 続行

---

**以上、引き継ぎ完了。Codex でも仲氏の作業を質高く支援してください。** 🤝
