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
- **今週の優先 TODO**:
  - [x] ~~SSD 価格監視~~ 完了（4/27 Acer FA100 購入で危機脱出、ルーチン継続は不要）
  - [x] ~~しゅん先生 PC を SMR HDD で延命運用~~ 完了（4/29 NVMe 移行で延命終了）
  - [x] ~~4/29 NVMe クローン死闘記事の Substack 本編 publish~~ ボツ（5/1 夜決定、Notes だけで完結、本編は書かない）
  - [x] ~~旧 Seagate ST2000LM015 の処遇決定（外付け USB-SATA ケース化 or 内蔵 D: 維持 or 廃棄）~~ ボツ（5/2 朝決定、しばらく現状維持）
  - [ ] BIOS 整理（CSM 無効化 + 旧 HDD の Boot Manager エントリ削除）
  - [x] ~~4/30 GC313Pro 物理セットアップ + UVC ビューワ実装~~ 完了（USB-C 2 本のみで Mac → GC313Pro → Windows しゅん先生 PC → LG モニタ確立、HDMI 不要。Python + OpenCV 自作ビューワは Windows 標準カメラアプリで代替可能と判明し不要に。詳細 @docs/journal/2026-04-30.md）
  - [ ] **Joy-Con 2 Windows マウス化ドライバ開発**（5/2 11:22 復活 — 5/2 朝にボツしたが、doda 提出完了 + しゅん先生 PC 環境整備済 + ブラウザ自動化基盤確立で着手余裕できた。Phase 1（maruta/joycon2-usb-presenter ソース解析 + プロトコル文書化）開始。詳細 @docs/projects/joycon2-windows-driver.md）
  - [x] ~~sniffnet 1.5.0 実機検証~~ 環境構築完了（5/2 朝、Wireshark 4.6.5 cask 同時導入で ChmodBPF helper / access_bpf グループ / `/dev/bpf*` 権限解放、sudo なしで sniffnet・tshark・Wireshark.app・dumpcap 全部動く。tshark でテストキャプチャ成功、Anthropic API 通信見えた。実観察ネタ (YKSmas318 / Tailscale Funnel / しぶチャット / Substack 軽量監視記事) は今後随時）

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
