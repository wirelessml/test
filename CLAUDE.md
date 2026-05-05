# プロジェクトコンテキスト

> 目標: 200-300 行。肥大化したら `skills/claude-md-diet/` スキルで再度分解。
>
> 最終ダイエット: 2026-04-22（1984 行 → ~270 行）

## 現在の状態（2026-04-22 時点）

- **メイン作業機配置**（4/22 16:34〜 大規模再編）:
  - M1 MacBook Air = **持ち運び用**（外出先・自宅・コワーキング移動）
  - しゅん先生 PC = **コワーキング据え置き新メイン**（4/29 16:30 Acer FA100 NVMe 移行成功、Plextor 時代の速度復帰）
  - MASU-P55 (HP ProBook) = コワーキングサブ、WSL2 で OpenClaw 稼働
- **直近の重要イベント**:
  - 🚨 **4/22 18:20**: しゅん先生 PC の Plextor SSD が NVMe コントローラ障害で完全死亡、2 時間前に作ったクローンが命綱に（詳細: @docs/journal/2026-04-22.md）
  - 4/22 19:40: Substack ノートに「SSD 突然死 → クローン復活 → NAND 高騰で買い替え不可」投稿
  - 4/27 18:20: Acer FA100 512GB を はばタンPay+ 50% プレミアムで実質 ¥10,267 購入
  - 🎉 **4/29 16:30**: しゅん先生 PC が Acer FA100 NVMe SSD で完全復活、3 時間のクローン死闘後 `stornvme\StartOverride\0=0x3` 削除で起動成功、CDM 3,374 MB/s（Plextor 時代に復帰）
- **🔄 ユーザーが「続きお願いいたします」と言ったら、以下を順番に実行する (2026-05-06 設定)**:
  1. **このセクションの「現在の状態」+ @docs/journal/2026-05-06.md 冒頭を Read**して文脈を再構築
  2. ユーザーに対して「Chrome DevTools MCP 復活ルートを進めますね」と一言告げる
  3. **`/plugin`** を案内して **chrome-devtools-mcp を install / enable** してもらう
  4. **Chrome を remote-debug 起動**:
     ```bash
     "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
       --remote-debugging-port=9222 \
       --user-data-dir="$HOME/Library/Application Support/Google/Chrome/Default" &
     ```
  5. `mcp__chrome-devtools__list_pages` で Chrome タブ確認 → Instagram (@minimalist_sibu) ログイン状態確認
  6. **持ち越しタスク**: <https://www.instagram.com/p/DX9FnIfCRFi/?img_index=9> へ navigate → **9 枚目を取得して分析**（しぶ Instagram 投稿の可能性大、文脈は ai-minimalist-shibu/knowledge/ 参照）
  7. 分析結果をユーザーに提示 → ナレッジ更新 / Substack ネタ判定
  - **直前の主要成果**（再起動前セッション 2026-05-05〜06）:
    - Word 体験報告書 4 件修正完了（P3/P4/P5/P9）
    - Claude Code 全 3 台 v2.1.128 統一
    - microsoft/edit v2.0.0 全 3 台 + Windows 25H2 System32 バンドル発見
    - Windows 11 26H1 = ARM Snapdragon X2 専用
    - masu-p55 LAN SSH 経路確立（`ssh masu-p55` で gci_admin 接続可）
    - 🐬 CopilotKeyboard / イルカのカイル発見・masu-p55 Kyle.imeskin 切替済
    - 黒田蒲鉾: 店頭 ◯ / くろかま家 ✗ の構造判明
    - X 投稿 5/5 21:45 ID 2051578751096672581
  - **詳細とフルログは @docs/journal/2026-05-06.md**
- **今週の優先 TODO**:
  - [x] ~~SSD 価格監視~~ 完了（4/27 Acer FA100 購入で危機脱出、ルーチン継続は不要）
  - [x] ~~しゅん先生 PC を SMR HDD で延命運用~~ 完了（4/29 NVMe 移行で延命終了）
  - [x] ~~4/29 NVMe クローン死闘記事の Substack 本編 publish~~ ボツ（5/1 夜決定、Notes だけで完結、本編は書かない）
  - [x] ~~旧 Seagate ST2000LM015 の処遇決定（外付け USB-SATA ケース化 or 内蔵 D: 維持 or 廃棄）~~ ボツ（5/2 朝決定、しばらく現状維持）
  - [ ] BIOS 整理（CSM 無効化 + 旧 HDD の Boot Manager エントリ削除）
  - [x] ~~4/30 GC313Pro 物理セットアップ + UVC ビューワ実装~~ 完了（USB-C 2 本のみで Mac → GC313Pro → Windows しゅん先生 PC → LG モニタ確立、HDMI 不要。Python + OpenCV 自作ビューワは Windows 標準カメラアプリで代替可能と判明し不要に。詳細 @docs/journal/2026-04-30.md）
  - [x] ~~**Joy-Con 2 Windows マウス化ドライバ開発**~~ **完全ボツ**（5/3 朝決定、Phase 1+2 完了 + Phase 3 scaffold 完成済も、実機検証で Joy-Con 2 (R) が BLE advertisement 出さず接続不能。Mac でも Windows でも検出不可 = Joy-Con 2 ハードウェア / バッテリー問題と切り分け、これ以上の調査コスト見合わず断念。Mac 側コード・ドキュメント・Substack ドラフトは削除、しゅん先生 PC 側ファイルは保持。詳細経緯 @docs/journal/2026-05-03.md 追補 1）
  - [x] ~~sniffnet 1.5.0 実機検証~~ 環境構築完了（5/2 朝、Wireshark 4.6.5 cask 同時導入で ChmodBPF helper / access_bpf グループ / `/dev/bpf*` 権限解放、sudo なしで sniffnet・tshark・Wireshark.app・dumpcap 全部動く。tshark でテストキャプチャ成功、Anthropic API 通信見えた。実観察ネタ (YKSmas318 / Tailscale Funnel / しぶチャット / Substack 軽量監視記事) は今後随時）
  - [x] ~~**国民年金 令和 7 年度免除申請**~~ 完了（5/4 03:53 マイナポータル経由、5 種類全チェック、結果通知 7-8 月、4-6 月分の納付書は審査中ストップ）
  - [x] ~~**整理収納アドバイザー 1 級 体験報告書 Artifact 図表 10 個**~~ 完了（5/4 09:30-10:32 で全完成、A 評価 90 点+、`~/Desktop/*.html`、@docs/projects/seiri-shu-nou-advisor-1.md）
  - [ ] **しぶコーチング応募フォーム 送信**（写真 10 枚撮影完了済、アップロード + 送信ボタン待ち、**締切 5/6 23:59**）
  - [ ] **整理収納アドバイザー 1 級 2 次試験申込**（協会 HP で受付確認、5/7 以降 + CBT 受験/2021-06-10/受験地域 入力）
  - [ ] **体験報告書 本文 10 ページ執筆**（Word + Claude for Word、Saved Prompt 適用、3 週間想定）
  - [ ] BIOS 整理（CSM 無効化 + 旧 HDD の Boot Manager エントリ削除）

## 機材（詳細は @docs/machines/）

- **M1 MacBook Air 8GB**: 持ち運び用、モバイル作業機（@docs/machines/m1-macbook-air.md）
- **しゅん先生 PC**: コワーキング据え置き、Windows 11 25H2、4/29 Acer FA100 NVMe 移行完了で Plextor 時代の速度復帰（@docs/machines/shun-sensei-pc.md）
- **MASU-P55 (HP ProBook)**: コワーキングサブ、Windows + WSL2 Ubuntu で OpenClaw 稼働（@docs/machines/masu-p55.md）
- **モバイル・周辺機器**: iPhone 15 Pro (結花)、iPad Pro 9.7 (彩羽)、テレビ・モニター（@docs/machines/mobile-devices.md）

## ユーザー情報

- 現在無職（雇用保険受給なし）
- ミニマムライフコスト: 約 136,288 円/月
- 国民年金: 17,920 円/月（免除申請予定）

## 運用ルール（最重要のみ、詳細は @docs/rules/）

1. **記事の削除や一括更新をする前は、必ず件数を教えて確認を取ること**
2. **金銭トランザクション**（発注・送金・取引）は代行しない、必ずユーザーが最終クリック
3. **読んでいないコードは変更するな** — Read で内容確認してから編集
4. **サブエージェントの成果物は必ず自分で検証してからユーザーに報告する**
5. **メモリ機能は使用しない** — 情報はすべて git 管理のドキュメントに

詳細なルール:
- 一般操作: @docs/rules/operations.md
- コーディング規約: @docs/rules/coding.md
- 情報の保存方針: @docs/rules/information-storage.md
- セッション設定（ターミナル最前面・モデル選択等）: @docs/rules/session-setup.md
- よく使うコマンド: @docs/rules/useful-commands.md
- Mac 常駐プロセス: @docs/rules/mac-processes.md
- Mac プロセス管理教訓: @docs/rules/mac-process-lessons.md

## 最近 2 週間の作業記録（詳細は @docs/journal/YYYY-MM-DD.md）

- **2026-05-06** (水、振替休日): **Word 体験報告書 4 件修正完了** (P3 ペルソナ削減 / P4 軸書き換え / P5 士業除去 / P9 数値統一) + **Claude Code 全 3 台 v2.1.128 統一** + **microsoft/edit v2.0.0 全 3 台インストール** (Windows 25H2 が System32 に v1.2.1 をバンドル発見) + **Windows 11 26H1 = ARM Snapdragon X2 専用判明** (しゅん先生 PC は永続的に 25H2 ライン Experimental Channel Build 26300.8346) + **masu-p55 LAN SSH 経路確立** (Tailscale offline 中も `ssh masu-p55` で到達可、 ssh config 追記済) + **🐬 CopilotKeyboard / イルカのカイル発見** (Office 97 の 23 年ぶり AI 化復活、しゅん先生 PC 表示中、masu-p55 もレジストリ Kyle.imeskin に切替済) + **黒田蒲鉾の真相**（店頭販売 ◯ / くろかま家 居酒屋 ✗ の事業所単位加盟構造）+ **X 投稿 5/5 21:45** (@minimalistneko、 ID 2051578751096672581、斎藤知事+増山県議への「教えてくれなかった」ツイート) + Algrow / OpenReel / OpenScreen / Recordly / @hoshino_aisales 等の動画 OSS / AI トレンド観察 + チョン・サラ漢字調査（嵐のような結婚生活 DramaBox）+ **次セッション持ち越し**: IG 投稿 9 枚目分析 + Chrome DevTools MCP 復活（@docs/journal/2026-05-06.md）
- **2026-05-04** (月、みどりの日): **国民年金 令和 7 年度免除申請完了** (03:53 マイナポータル、5 種類全チェック、結果 7-8 月) + **整理収納アドバイザー 1 級 2 次審査体験報告書 Artifact 図表 10 個全完成** (Mobile Dispatch Sonnet 4.6 経由、A 評価 90 点+、`~/Desktop/*.html`) + 構成案 docs 新規作成 (`docs/projects/seiri-shu-nou-advisor-1.md`) + 戦略確定 (タイトル C「次世代整理収納サポート」/ 提案編 / AI 概念のみ実装ナシ / ブランド名完全伏せ / Word + Claude for Word + Artifacts ハイブリッド) + しぶ動画 TRr6gtjHECM のコア発言「物・お金・デジタル」を 3 軸モデル化 + しぶ応募 写真 10 枚撮影完了 (フォーム送信は 5/6 23:59 締切) + AI 系 X 投稿 7+ 件ファクトチェック (ごくう / すみか / Claude Code Studio / ほしの / 遠藤太一 / 木内翔大 / kumara) + 認識訂正 2 点 (Codex Mac Desktop App = 真の Computer Use、Claude for Word = Word 執筆相性最強) + Dispatch モデル制約 app.asar 直接調査 (Sonnet 4.6 + Opus 4.6 の 2 択、Opus 4.7 はアプリ未対応) + フィッシングメール識別 (年金機構騙り pirosi80 4 通目) + Voice-Pro 発見 (ElevenLabs 5/11 失効対策候補) + 家族構成 context 修正 (結花 12 = 長女 / 彩羽 10 = 次女、両方公立進学予定)（@docs/journal/2026-05-04.md、@docs/projects/seiri-shu-nou-advisor-1.md）
- **2026-04-30**: GC313Pro 物理セットアップ完了 (USB-C 2 本のみで Mac→GC313Pro→Windows しゅん先生 PC、HDMI 不要) + UVC ビューワ自作不要が判明 (Windows 標準カメラアプリで完結) + YouTube Live 配信停止しローカル表示へ切替 + 午前に Remote Control 失敗の RCA → claude-obsidian v1.4.3 の SessionStart prompt hook 削除 (Claude Code 2.1.123 の `ToolUseContext is required for prompt hooks` 内部バグ回避、機能損失ゼロ) + 上流 2 リポにバグ報告コメント追加 (anthropics/claude-code#48508 + AgriciDaniel/claude-obsidian#7) + 2 週間後の自動フォローアップ agent (trig_011Z6wQomq29fguPfP6nAeKr) 仕込み + しゅん先生 PC の 4K UHD BD 再生スタックを完全確定 (PowerDVD 14.0.1.7320 UHDBD-OEM + LG 40WP95C-W、iiyama BTO 標準バンドル判明、Ryzen / Intel 第 11 世代以降への CPU 換装 NG 根拠完成) + 午後に Karabiner-Elements v15.9.0 導入で写真の片手キーパッド HCT (Hengchangtong VID49396/PID9) に Conductor Studio 風 3 ルール (Caps+WASD→矢印 / 左Alt+1-6→F1-F6 / F+G→Cmd+Tab) 実装 + Anthropic 4/28 リリースの Autodesk Fusion connector 経由で Fusion 360 Personal Use (¥0) セットアップ着手 (ハブ作成画面で再起動中断) + IT navi の Pro Opus 4.7 制限オーバー不満ツイートに @minimalistneko 名義でリプライ投稿（@docs/journal/2026-04-30.md、@docs/machines/shun-sensei-pc.md）
- **2026-04-29**: 勝間 voice stack 物理セットアップ完了 (V4→V5、SuperWhisper Pro Lifetime + Scribe) **+ 午後しゅん先生 PC を Acer FA100 NVMe に移行 → クローン後 0xc0000001/0x7B で 3 時間死闘 → `stornvme\StartOverride\0=0x3` 削除で起動成功、CDM 3,374 MB/s** + Substack 記事ドラフト作成 + Notes 投稿（@docs/journal/2026-04-29.md）
- **2026-04-23**: Kioxia 整備品自動監視実装（LaunchAgent 毎日 08:17 JST）+ Intel X25-M G1 80GB 発掘 + しぶ 4/22 動画分析 → りくと編集チーム統括ディレクター昇格判明（72 時間ジャーニー更新）+ pirosi80 フィッシング 3 通目（@docs/journal/2026-04-23.md）
- **2026-04-22**: しゅん先生 PC バックアップ実装 + Plextor SSD 死亡 + Seagate クローン救出劇 + SSD 市場高騰調査 + claude-md-diet スキル作成 + CLAUDE.md リファクタ（@docs/journal/2026-04-22.md）
- **2026-04-21**: しぶ AI研修 2 日目ストーリーで人物特定訂正 + MASU-p 共有 HP ProBook で GC313Pro セットアップ完了（@docs/journal/2026-04-21.md）
- **2026-04-20**: Claude Design 本番化 + Google Workspace CLI 導入 + マルチツール一気導入 + しぶエコ人物特定（@docs/journal/2026-04-20.md）
- **2026-04-18 夜〜4/19 朝**: AI 自動ゲームプレイ研究 3段階実験 + VoiceBox 発見（@docs/journal/2026-04-18-night.md）
- **2026-04-18**: 5 セッション分の記録（F5 送信キー検証、Chrome MCP、MUZINA Discord、Crown & Coin デモ、午前作業、早朝 GHFS）（@docs/journal/2026-04-18.md）
- **2026-04-17**: Opus 4.7 切替 + Codex Mac インストール + iPhone SSH（@docs/journal/2026-04-17.md）
- **2026-04-16**: Windows XP SP3 VM セットアップ（@docs/journal/2026-04-16.md）
- **2026-04-15**: 毎朝 TODO 配信 + Copilot CLI 導入 + Dataverse 管理者昇格（@docs/journal/2026-04-15.md）
- **2026-04-14**: Maestri インストール + Windows SSH 統一 + BGM 変更 + しぶ配信システム v3（@docs/journal/2026-04-14.md）
- **2026-04-13**: gh CLI 再認証 + pytchat 切替 + OBS 画面キャプチャ（@docs/journal/2026-04-13.md）

2 週間より古い記録: @docs/archive/2026-04/（4/8〜4/12 を収録）

## 期限・リマインダー

全期限リスト: @docs/reminders.md

次の 2 週間の重要期限:
- **2026-04-30**: Microsoft 365 Copilot Business 解約予定日（admin.cloud.microsoft で「有効期限切れ時にキャンセル」選択済）
- **2026-05-06 23:59**: 太閤立志伝V DX Switch eShop セール終了（¥2,970、検討中）
- **2026-05-11**: ElevenLabs Starter プラン失効
- **2026-05-20 前後**: Y!mobile 151 に電話で最終確認
- **2026-05-29〜5/30**: povo 2.0 へ MNP ワンストップ転出

## 個別プロジェクト

- **AIミニマリストしぶ チャットサーバー**: Claude CLI 経由の Web チャットボット（@docs/projects/shibu-chatbot.md）
- **shibu-video-editor**: しぶ受講生インタビュー動画 Claude API 半自動編集 OSS（4/26 公開、`/Users/yuika/Desktop/shibu-video-editor/`、https://github.com/wirelessml/shibu-video-editor、MIT、Python 1,451 行 + 12 unit tests）
- **整理収納アドバイザー 1 級 2 次審査** (2021/06/10 1 次合格、5/4 構成案策定 + Artifact 図表 10 個完成): @docs/projects/seiri-shu-nou-advisor-1.md
- **しぶコーチング応募** (5/4 写真撮影完了、フォーム送信は 5/6 23:59 締切): @docs/journal/2026-05-04.md 参照
- **しぶエコ観察**: @docs/journal/ に日次で記録、関連ナレッジは `ai-minimalist-shibu/knowledge/`
- **Substack 連載**: 仲啓輔名義、4/22 時点で「SSD 突然死」ネタ投稿済み

## 定期ルーチン（詳細は @docs/routines/）

- **SSD 価格監視**（毎週月曜、しゅん先生 PC 用 NVMe 買い替え待ち）: @docs/routines/ssd-price-monitor.md
- **Claude Code セッションスケジュール**（9/14/19/0/5 時 JST、毎日）: @docs/routines/session-schedule.md
- ~~**X 情報収集ルーチン**（各セッション毎）: @docs/x-daily-briefing.md~~ **廃止（5/2 朝決定）**。各セッションで X 巡回するルーチンは終了、必要時に都度判断して `twitter -c feed` 実行
- **しぶ Instagram 監視**（毎時 17 分）: @docs/routines/instagram-watch.md
- **MASU-p 監視**（毎日 18:12 JST、LaunchAgent）: @docs/routines/masu-p-watch.md
- **リモートコントロール状態報告**（毎時 33 分）: @docs/routines/remote-control-report.md
- **運用ルーチン（CLAUDE.md とタスク管理の二層構造）**: @docs/routines/task-management.md

## TODO リスト

- **次回 Mac 前作業（ブラウザ GUI 操作必須分）**: @docs/todos/mac-tasks.md（残存分: YouTube プレミアム解約、維新の嵐 CD インストール、Switch 2 キャプチャ、iPhone VNC 等）
- **ElevenLabs 使い倒し（〜5/11）**: @docs/todos/elevenlabs.md（残クレジット 32,472+、D→A→B→C の順で実行）

## 情報の保存方針（要旨）

- メモリ機能は使用しない
- 情報はすべて git 管理のドキュメントに書く
- 会話中の知見は毎回 git に保存（ルーチン）
- ナレッジ: `docs/` 配下、プロジェクト情報・ユーザー情報: この `CLAUDE.md`

## このリポジトリについて

Claude 活用のナレッジベース。AI 関連の知見・ガイド・テンプレートを蓄積し、どの AI エージェントからでも参照できる状態を維持する。

## リポジトリ構成

```
.
├── CLAUDE.md                      ← このファイル（プロジェクト糊、~270 行）
├── docs/
│   ├── machines/                  ← マシン別詳細（M1 / しゅん先生 PC / MASU-P55 / モバイル）
│   ├── journal/                   ← 日次作業ログ（YYYY-MM-DD.md）
│   ├── archive/                   ← 2 週間以上前の記録（月次）
│   ├── routines/                  ← 定期タスク（SSD 監視 / X 収集 / Instagram 等）
│   ├── rules/                     ← 操作規約（operations / coding / session-setup 等）
│   ├── todos/                     ← 個別 TODO リスト
│   ├── projects/                  ← プロジェクト別詳細
│   ├── reminders.md               ← 期限・日付リマインダー
│   └── <その他ガイド.md>           ← Claude Code Tips、Computer Use ガイド等
├── skills/
│   └── claude-md-diet/            ← CLAUDE.md ダイエット用スキル
├── ai-minimalist-shibu/           ← しぶチャットボット実装 + ナレッジ
├── templates/                     ← 学校プリント等のテンプレート
└── screenshots/                   ← 定時報告スクリーンショット
```

## Claude Code セッション運用

- モデル: セッション開始時に `/model opusplan`
- ターミナル最前面設定: セッション開始時にユーザー案内（@docs/rules/session-setup.md）
- 週次使用量: `/usage` または StatusLine で確認
- セッションスケジュール: 1 日 5 回（9/14/19/0/5 時 JST）

## 今後の見直し

- **4/18 10:00**: 5 セッション/日スケジュールの運用見直し（実施済みだが継続課題として観察）

## 参照

- @docs/rules/ — 操作規約・コーディング規約・セッション設定
- @docs/machines/ — マシン詳細
- @docs/journal/ — 日次作業ログ
- @docs/archive/ — 古い完了記録
- @docs/routines/ — 定期タスク
- @docs/projects/ — プロジェクト別
- @docs/reminders.md — 期限リスト
- @docs/todos/ — TODO リスト
- @skills/claude-md-diet/SKILL.md — このファイルを軽量化するスキル
