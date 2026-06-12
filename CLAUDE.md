# プロジェクトコンテキスト

> 目標: 200-300 行。肥大化したら `skills/claude-md-diet/` スキルで再度分解。
>
> ダイエット履歴: 2026-04-22（1984 行 → ~270 行）/ 2026-06-12（内容刷新、4-5 月分を docs/archive/ へ）

## 現在の状態（2026-06-12 時点）

- **機材配置と役割ポリシー（6/12 更新）**: **Mac (M1) = Claude Code 専用＝司令塔**（持ち運び）/ **masup = Claude の委譲先 Codex ワーカー**（独立自走せず、Mac の Claude が `codex exec` で重い作業＝レビュー・監査・文字起こし・大量調査を投げる subagent。手順: @skills/delegating-to-masup-codex/）/ **しゅん先生 PC = コワーキング据え置きメイン**。※6/2 は「masup = Codex 専用（独立）」だったが 6/12 に「Claude のサポート役」へ更新（@docs/journal/2026-06-12.md 追補 3）
- **⭐ Fable 5 無料期間（〜2026-06-22）**: Claude Fable 5 が従量課金なしで利用可。**期間戦略＝「6/23 以降も残る資産」への変換に集中**（スキル・ハーネス・ドキュメント・重い執筆）。使い捨ての出力（デモ・遊び）に枠を使わない。**メニューと消化ログ: @docs/projects/fable5-assets-plan.md**（毎枠ここから取る。6/12 に 8 項目消化＋Codex レビュー 2 本並走開始）
- **直近の重要イベント**:
  - **6/11**: 就活レポート Mac 移管初日成功（04:30、83 件）＋ GVC キャリア面談を録画 v2〜v3 体制で完遂（whisper `-mc 0` で幻覚解消）（@docs/journal/2026-06-11.md）
  - **6/10**: 就活ルーチンを masup Codex → Mac LaunchAgent に完全移管。**ルール 2 本制定「時間かかりすぎ＝中止シグナル」「枠の頭で計画」**。LaunchAgent 全アンロード事故→7 個復旧（@docs/journal/2026-06-10.md）
  - **6/7**: launchd の TCC 罠（`~/Desktop` 読めず）で就活メール不達→`~/Library/Application Support/job-report/` へ移設で恒久修理。**教訓: launchd 起動物は `~/Desktop` に置かない**（@docs/journal/2026-06-07.md）
  - **5/12〜**: Reco.app の Ollama mock サーバ `com.yuika.reco-ollama-mock` が LaunchAgent で**常駐継続中**（@docs/journal/2026-05-12.md）
- **🔄 ユーザーが「続きお願いいたします」と言ったら**:
  1. このセクション＋最新の @docs/journal/YYYY-MM-DD.md を Read して文脈再構築
  2. 直前ジャーナル末尾「未完了 / 持ち越し」を確認
  3. 最優先タスクから着手、進める旨を一言告げてから実行
- **取得済の便利インフラ**（再利用可、設定不要）:
  - chrome-devtools-mcp（user scope）/ playwright / peekaboo / Gmail / Calendar / マネーフォワード MCP / codex MCP
  - IG・X はログイン済 Chrome プロファイル経由で取得可（`open -a "Google Chrome" <url>` + osascript + screencapture、MCP 無しでも可）
- **今週の優先 TODO**:
  - [ ] **Fable 5 期間の資産化**（〜6/22、上記⭐の方針で残り枠を配分）
  - [ ] **Bグループ ミニマリスト宅訪問動画 1 本目**（2 週間完走目標、@docs/projects/minimalist-visit-production.md）
  - [ ] エボルカ WEB 面談 6/15(月) 11:00（条件回答は済み。録画するなら 面談-録画.command）
  - ※ GVC 送信・整理収納 2 次申込・DMM 退会・BIOS 整理の 4 件は **6/12 ユーザー指示でトラッキング外**（BIOS 整理は不要と判断し廃止、4 月からの持ち越しを終了）
  - [ ] iPhone Safari 履歴 SQL 解析 — **Terminal に Full Disk Access 付与待ち**（システム設定→プライバシー→FDA。付与後は解析 5 分、@docs/journal/2026-06-12.md 追補 2）
  - [x] ~~scripts/ 棚卸しの削除実行~~ 完了（6/12 承認→削除 24・archive 16 実行、masup ゾンビ watchdog と shibu.stream も無効化、doctor 全緑。残=しゅん先生 PC 確認 2 件＋全機更新の残り 1 台、**6/13 起動予定** → @docs/projects/scripts-audit-2026-06-12.md）
- **⚠️ 状態不明・要本人確認**:
  - しぶコーチング応募: 締切 5/6 23:59 を超過と 5/7 ジャーナルに記録（失効扱い）
  - ~~povo 2.0 MNP~~ → ✅ **実施済みと 6/12 本人確認**。eSIM は 2026 秋に長女・結花の新 iPhone へ移行予定（@docs/reminders.md）

## 機材（詳細は @docs/machines/）

- **M1 MacBook Air 8GB**: 持ち運び用。**Claude Code 専用**（@docs/machines/m1-macbook-air.md）
- **しゅん先生 PC**: コワーキング据え置き、Windows 11 25H2、Acer FA100 NVMe（@docs/machines/shun-sensei-pc.md）
- **MASU-P55 (HP ProBook)**: コワーキングサブ、Windows + WSL2。**Codex 専用**、codex は WSL2 側（@docs/machines/masu-p55.md）
- **モバイル・周辺機器**: iPhone 15 Pro (結花)、iPad Pro 9.7 (彩羽)（@docs/machines/mobile-devices.md）

## ユーザー情報

- 仲啓輔、現在無職（雇用保険受給なし）、就活中（毎朝 04:30 自動レポート）
- ミニマムライフコスト: 約 136,288 円/月
- 国民年金: 令和 7 年度免除申請済み（5/4）、結果通知 7-8 月

## 運用ルール（最重要のみ、詳細は @docs/rules/）

1. **記事の削除や一括更新をする前は、必ず件数を教えて確認を取ること**
2. **金銭トランザクション**（発注・送金・取引）は代行しない、必ずユーザーが最終クリック
3. **読んでいないコードは変更するな** — Read で内容確認してから編集
4. **サブエージェントの成果物は必ず自分で検証してからユーザーに報告する**
5. **メモリ機能は使用しない** — 情報はすべて git 管理のドキュメントに
6. **「時間かかりすぎ」「まだ？」は中止シグナル** — 同じ重い経路を再試行せず、現状＋選択肢を一言で報告（6/10 制定）
7. **枠の頭で計画** — 新しい 5 時間枠の冒頭で「この枠のプラン」3 行提示、重い処理は枠の前半へ（6/10 制定、@docs/rules/session-setup.md）

詳細なルール:
- 一般操作: @docs/rules/operations.md
- コーディング規約: @docs/rules/coding.md
- 情報の保存方針: @docs/rules/information-storage.md
- セッション設定: @docs/rules/session-setup.md
- よく使うコマンド: @docs/rules/useful-commands.md
- Mac 常駐プロセス: @docs/rules/mac-processes.md / 教訓: @docs/rules/mac-process-lessons.md

## 最近 2 週間の作業記録（詳細は @docs/journal/YYYY-MM-DD.md）

- **2026-06-12** (金): **Fable 5 資産化デー（無料期間〜6/22 の方針実行初日）** — ①CLAUDE.md 再ダイエット（212→168 行、4-5 月分を archive index 化、povo MNP 未確認を発掘）②スキル 4 本新設＋.claude/skills 配線（journal/録画文字起こし/全機更新/Xファクトチェック）③ハーネス: SessionStart フックで「枠の頭で計画」自動化＋**launchagent-doctor 新設→初走行で実害 3 件即検出**（kanno-watch/kioxia-monitor の TCC exit126、reco-mock の port 競合）→当日修理し 9/10 健全・TCC 警告 0 ④scripts 棚卸しを masup Codex 委譲→検証 3 点訂正→**削除 20 等の提案承認待ち**＋masup ゾンビ watchdog 発見 ⑤体験報告書は**本文完成済みと判明**→レビューで要修正 2 点特定。教訓: bash の `$var`+多バイト罠×2、tar の AppleDouble 混入、「動いている LaunchAgent も TCC 時限爆弾」（@docs/journal/2026-06-12.md）
- **2026-06-11** (水): **就活レポートMac移管初日が完全成功（04:30、83件、二重送信防止も動作）＋GVCキャリア カジュアル面談を一気通貫対応** — ①前夜応募の「AIエンジニア未経験6ヶ月研修」（実体=SES＋有料スクール「キャリフリ」＋風評対策事業の新興企業）を面談32分前に分析しチートシート化。②Zoomアプリ無し→**Chromeブラウザ参加**で実施。③**録画システムv2**: 画面=screencapture -v／音声=ffmpeg(マイク+BlackHole)／Ctrl+C後に自動合成、25分39秒・4K・3.3GBを取得。④whisper文字起こしは**繰り返し幻覚を`-mc 0`で解消**。⑤面談で核心質問をぶつけ、LINE誘導をメールへ切替。次の一手=書面質問3点。⑥録画のYouTube公開希望は肖像権で止めた。⑦iPhone Safari履歴の中抜け発見→SQL解析持ち越し（@docs/journal/2026-06-11.md）
- **2026-06-10** (火): **就活ルーチンを5回改訂→masup Codexから Mac自作スクリプトへ完全移管** — 実在・勤務地検証必須化／福祉・飲食・資格必須職を恒久除外／板宿駅1km＋声を出さない在宅事務／`job-search-daily.py`+LaunchAgent 04:30 に移管（Codexクォータ・geo水増し根治）。**ルール2本制定「時間かかりすぎ=中止シグナル」「枠の頭で計画」**。iMovie=ffmpeg実証で決着、iPhone録画設定確定（4K30 HEVC/HDRオフ）。**LaunchAgent全アンロード事故を発見・7個復旧**。カレンダーのセッション1〜5廃止（@docs/journal/2026-06-10.md）
- **2026-06-07** (日): **6/8 Bグループ面談の準備仕上げ＋就活メール不達を恒久修理** — 録音=ffmpeg(本体マイク＋BlackHole)コマンド化／文字起こし=whisper.cpp `ggml-large-v3-turbo` 採用（SuperWhisper Pro は 5/28 失効、「Lifetime」は誤記と訂正）／**launchd TCC 罠**（`~/Desktop` 読めず exit126）→ `~/Library/Application Support/job-report/` へ移設で復旧（@docs/journal/2026-06-07.md）
- **2026-06-06** (土): **X返信ワークフロー＋全機アップデート＋就活案件解明** — 坂本龍佑・西宮市議「結婚減税」ツイート分析→年少扶養控除復活論で本スレ返信1＋サブ返信4。全機 claude 2.1.167 / codex 0.137.0 / gemini 0.45.2。**Bグループ株式会社/Takeruチャンネル業務委託**（ミニマリスト訪問取材・1本15,000円）を解明し面談候補日時を Gmail 返信（@docs/journal/2026-06-06.md）
- **2026-06-05** (木): **プライバシー整理＋`/remote-control`(`/rc`)学習** — 公開リポ wirelessml/test の自宅番地を伏字化／死んでいた cron 2件撤去／`~/Desktop/screenshots/` 全削除。**`/remote-control` = Claude Code v2.1.53+ の正式機能**と判明（claude.ai 中継、VPN/Tailscale 不要）。⚠️自作 `/rc`（状況報告）と名前衝突注意（@docs/journal/2026-06-05.md）
- **2026-06-02** (火): **AIエージェント環境を役割分離で大整理** — Mac=Claude Code専用 / masup=Codex専用 確定。Mac の codex remote-control 停止＋無効化、masup の OpenClaw / Antigravity / Whisper残骸削除。app-server 競合知見・WSL2 サンドボックス必須の理由を整理（@docs/journal/2026-06-02.md）

2 週間より古い記録のサマリー: @docs/archive/2026-05/index.md（5/4〜5/30）・@docs/archive/2026-04/index.md（4/8〜4/30）。ジャーナル本体は @docs/journal/ に残存

## 期限・リマインダー

全期限リスト: @docs/reminders.md

直近の重要期限:
- **2026-06-22**: **Fable 5 無料期間終了**（以降は `/model opusplan` に戻す。資産化を完了させること）
- **2026-07-31**: はばタンPay+ 第 5 弾 利用期限（残高は @docs/finance/habatan-pay-strategy.md）
- **2026-07〜08**: 国民年金免除申請の結果通知
- **2026 秋**: povo eSIM を長女・結花の新 iPhone へ移行予定（@docs/reminders.md）

## 個別プロジェクト

- **整理収納アドバイザー 1 級 2 次審査**: 図表 10 個（5/4）＋本文 9,186 字（5/5-6 Word 内で完成、6/12 レビューで要修正 2 点特定）→ @docs/projects/seiri-shu-nou-advisor-1.md ＋ seiri-shu-nou-advisor-1-draft.md
- **ミニマリスト宅訪問動画 制作 / 動画スキル向上**（Bグループ業務委託、採算度外視・2 週間で 1 本完走）: 制作メモ @docs/projects/minimalist-visit-production.md、脚本 @docs/projects/minimalist-visit-script.md、スキル向上 @docs/projects/video-skills.md
- **就活**: 毎朝 04:30 自動レポート（下記ルーチン）。直近はエボルカ WEB 面談 6/15(月) 11:00、角川は書類選考結果待ち
- **takeru-chatbot**: Claude CLI 経由 Web チャットボット＋しぶ観察ナレッジ `takeru-chatbot/knowledge/`（@docs/projects/takeru-chatbot.md）
- **takeru-video-editor**（GitHub 公開リポ名は shibu-video-editor のまま）: しぶ受講生インタビュー動画半自動編集 OSS
- **しぶエコ観察**: @docs/journal/ に日次記録
- **Substack 連載**（仲啓輔名義）: ネタ候補ストック中（「AI を理解に使う人/済ますために使う人」政治家版 6/12 等）

## 定期ルーチン（詳細は @docs/routines/）

- **就活 求人サーチ**（毎朝 04:30、LaunchAgent `com.yuika.job-search-mac` → `~/Library/Application Support/job-report/job-search-daily.py`。板宿駅 1km・資格/福祉/飲食除外・在宅事務（神戸優先）→ GitHub `wirelessml/job-hunt-reports` push → メール。「就活レポート」で最新報告。@docs/routines/job-search-daily.md）
- **MASU-p 監視**（毎日 18:12、LaunchAgent）: @docs/routines/masu-p-watch.md
- **Kioxia 整備品監視**（毎日 08:17、LaunchAgent）: @docs/routines/ssd-price-monitor.md（週次の手動 SSD 価格監視は 4/27 危機脱出により休眠）
- **kanno-watch / masup-codex-attachment-sync**: LaunchAgent 稼働中
- **🩺 LaunchAgent 健全性チェック**: `bash scripts/launchagent-doctor.sh`（6/12 新設。未ロード/実行失敗/TCC罠/期待リスト突合）。**launchd 起動物の実体は `~/Library/Application Support/<name>/`、git 正本は `scripts/`**（kanno-watch / kioxia-monitor / masu-p-watch は 6/12 移設済み）
- 廃止・休眠: セッションスケジュール（6/11 廃止）／ X 収集ルーチン（5/2 廃止）／ リモートコントロール状態報告（6/5 廃止）／ しぶ IG 毎時監視（セッション cron 前提が形骸化、必要時都度）
- **運用ルーチン（CLAUDE.md とタスク管理の二層構造）**: @docs/routines/task-management.md

## TODO リスト

- **次回 Mac 前作業（ブラウザ GUI 操作必須分）**: @docs/todos/mac-tasks.md
- ~~ElevenLabs 使い倒し~~ 終了（5/11 プラン失効）

## 情報の保存方針（要旨）

- メモリ機能は使用しない。情報はすべて git 管理のドキュメントに
- 会話中の知見は毎回 git に保存（ルーチン）
- ナレッジ: `docs/` 配下、プロジェクト・ユーザー情報: この `CLAUDE.md`

## このリポジトリについて

Claude 活用のナレッジベース。AI 関連の知見・ガイド・テンプレートを蓄積し、どの AI エージェントからでも参照できる状態を維持する。

- **AGENTS.md は CLAUDE.md の symlink**（Codex も同じ context を読む）
- **⚠️ origin は公開リポ（github.com/wirelessml/test）**。住所・認証情報・家族の個人情報は書かない（6/5 伏字化の教訓）

## リポジトリ構成

```
.
├── CLAUDE.md                      ← このファイル（プロジェクト糊）
├── AGENTS.md                      ← CLAUDE.md への symlink（Codex 用）
├── docs/
│   ├── machines/                  ← マシン別詳細
│   ├── journal/                   ← 日次作業ログ（YYYY-MM-DD.md）
│   ├── archive/                   ← 2 週間以上前のサマリー index（月次）
│   ├── routines/                  ← 定期タスク
│   ├── rules/                     ← 操作規約
│   ├── todos/                     ← 個別 TODO リスト
│   ├── projects/                  ← プロジェクト別詳細
│   └── reminders.md               ← 期限・日付リマインダー
├── skills/                        ← 運用スキル群（claude-md-diet ほか）
├── .claude/                       ← Claude Code 設定（settings / skills 配線）
├── scripts/                       ← 自動化スクリプト（LaunchAgent 実体ほか）
├── takeru-chatbot/                ← しぶチャットボット実装 + ナレッジ
└── templates/                     ← 学校プリント等のテンプレート
```

## Claude Code セッション運用

- モデル: **〜6/22 は Fable 5**（無料期間）。**6/23 以降は `/model opusplan` に戻す**
- ターミナル最前面設定: セッション開始時にユーザー案内（@docs/rules/session-setup.md）
- 週次使用量: `/usage` または StatusLine で確認
- 「枠の頭で計画」ルール: @docs/rules/session-setup.md

## 今後の見直し

- **2026-06-22**: Fable 5 期間終了。資産化の達成度を棚卸しし、モデル設定を opusplan に戻す

## 参照

- @docs/rules/ — 操作規約・コーディング規約・セッション設定
- @docs/machines/ — マシン詳細
- @docs/journal/ — 日次作業ログ
- @docs/archive/ — 古い記録のサマリー index
- @docs/routines/ — 定期タスク
- @docs/projects/ — プロジェクト別
- @docs/reminders.md — 期限リスト
- @docs/todos/ — TODO リスト
- @skills/claude-md-diet/SKILL.md — このファイルを軽量化するスキル
