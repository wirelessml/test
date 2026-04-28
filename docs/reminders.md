## リマインダー（セッション開始時に日付を確認し、該当日に通知すること）

- **2026/04/29（水）コワーキング着席日**: ✅ **勝間 voice stack 物理セットアップ完了（06:30〜07:45）** — 詳細 @docs/journal/2026-04-29.md
  - SSH で Python 12 ファイル配置 + ElevenLabs キー Mac→Win 流用永続化（starter tier、7,528/40,000 chars）
  - SuperWhisper Windows v1.3.9 インストール + 設定（S1-Voice / Japanese / Push to Talk Alt / Auto paste Off）
  - **重要発見**: Scribe は SW Free 枠で不可（Pro 限定）、勝間 4/27 18:17 の「SW 買い切り、Scribe 課金なし」は Lifetime + BYO key の意
  - **V4 ピボット**: Python 自前で `keybind_scribe.py`（無変換キー = ElevenLabs Scribe 直叩き）+ ローカル漢数字補正で **$0/月構成**確定
  - 退館後 / 自宅で実施: マイクテスト + V4 vs SW S1-Voice 精度比較 + start_voice_stack.bat 自動起動登録
  - スコープ外確定: YamabukiR / Google IME / Groq / Gemini / SW Pro 課金 すべて不要


- **2026/04/26（日）**: **Claude for Word 集中日（最優先・4/25 から順延）**
  - 9:00 セッション: Claude for Word アドインの状況確認 + 定款整形 Saved Prompt 設計・実機テスト
  - 14:00 セッション: Substack 記事「Claude for Word リリース 2 週間、定款整形が秒で終わった日」3,000-4,000 字を書き上げ
  - 19:00 セッション: 推敲 → **投稿**（SEO ピーク 4/24-5/5 前半に滑り込み）
  - Anthropic 公式 Word アドイン（2026-04-10 リリース、4/22 Pro/Max 対応拡大、Pro $20 で利用可）
  - 投稿先: Substack（仲啓輔名義）
  - 物理作業（HDD 切断・GC313Pro）は 4/27 に移動

- **2026/04/27（月）実績追記（18:20）**: ✅ **SSD 購入完了** — 大西ジム新長田で Acer FA100 512GB Gen3 を **はばタンPay+ 第 5 弾 50% プレミアム適用、実質 ¥10,267** で購入（目標 ¥12,000 以下達成）。エディオン西代は PS5 用 ADATA Gen4 ¥25,800 のみで見送り。値札 ¥14,080 → 実販売 ¥15,400 の **9.4% 値上げを目撃** = NAND 高騰の現場確認。**Substack ノート投稿済み**（仲啓輔名義、393 字、18:20）。**4/30 はばタンPay+ プランは別用途（外付け USB-SATA ケース / 食料 / 日用品 等）に転用可能**。
- **2026/04/27（月）夕方追加**: **17:00 エディオン西代 → 18:00 新長田（ケーズデンキ or 大西ジム）で SSD 下見**（本番購入は 4/30 のはばタンPay+ 50% プレミアム狙い、今日は価格・在庫・加盟確認のみ）
  - **目的**:
    1. 1TB NVMe M.2 2280 の表示価格を実機で確認（目標 ¥14,000 以下、発動 ¥12,000 以下）
    2. **大西ジム新長田のはばタンPay+ 加盟有無を直接確認**（4/30 計画で「要確認」と保留してた最大の不明点）
    3. ¥14,000 以下の即売り出物があれば 4/30 待たずに買う判断もあり
  - **候補モデル**: Crucial P3 Plus 1TB / Hanye MN50 1TB / KIOXIA EXCERIA G2 / WD Black SN770 / SAMSUNG 990 EVO Plus
  - **チェックリスト**:
    - 表示価格、ブランド、在庫数
    - レジ周辺の はばタンPay+ ステッカー or 店員に直接質問
    - 特売 / 数量限定品の張り紙
  - **持参**: iPhone（はばタンPay+ アプリ + Apple Notes でメモ）、出発前に残高・加盟確認
  - **4/26 の HIKVISION 中古 128GB ¥4,400 観察**との対比検討
  - 詳細 @docs/journal/2026-04-27.md

- **2026/04/27（月）追記**: 4/26 夜〜4/27 早朝のピボット — pdf-reader を **GitHub 公開（wirelessml/pdf-reader）+ Tailscale Funnel で世界公開（https://macbook-air.tail70852b.ts.net）**。`/asmr` `/ssd` `/typing` 3 ページ稼働中、`/api/chat` は環境変数未設定で 500 安全死亡。詳細 @docs/journal/2026-04-27.md。下記の物理作業は 4/27 残り時間 or 4/28 以降にスライド。

- **2026/04/27（月）**: **物理作業 2 本立て + SSD 価格監視ルーチン**
  - **① しゅん先生 PC の Seagate ST2000LM015 (D:) を物理的に切断**
    - 静音化目的（HDD スピン音をゼロに、SSD ブート単独運用へ）
    - 作業内容: シャットダウン → ケース開ける → SATA データケーブル + 電源ケーブル抜く → ケース閉じる → SanDisk SSD 単独起動確認
    - **重要**: D:\Backup\Weekly System Image.adi (84.9GB、4/22 AOMEI 作成) の扱い決定が事前必要
      - A) HDD 完全切断 → .adi 失う
      - **B) 外付け USB-SATA ケースに移植 → .adi 救出可、推奨**
      - C) 内蔵のまま BIOS で SATA 無効化 → .adi 残る、物理静音は不完全
    - 必要な道具: プラスドライバー、(B 案なら) 外付け USB-SATA ケース
    - 4/25 までに 1 分スピンダウン設定済み (powercfg /change disk-timeout-ac 1)
    - Plextor 死亡時の予備として残す方針 → 完全廃棄ではなく外付け化が筋
  - **② GC313Pro 作業**（AVerMedia ELITE GO、100W 急速充電 + 1080p60 キャプチャ）
    - 内容未確定（A: FW 更新 / B: Switch 2 キャプチャ実機 / C: MASU-p 配信ルート確立 / D: しぶ配信システム組み込み）
    - 詳細手順: @docs/gc313pro-user-guide-ja.html
  - **③ SSD 価格監視ルーチン**（毎週月曜、@docs/routines/ssd-price-monitor.md）

- **2026/04/28（火）**: **Substack 第 2 弾投稿 — SSD ブートバトル記事**
  - タイトル「Plextor が死んでから 72 時間、USB-C SSD で Windows を蘇らせるために BIOS と 6 時間半殴り合った話」
  - ドラフト: @docs/substack/2026-04-25-sandisk-usb-c-boot-battle-substack-ready.md
  - 4/26 Word 記事から中 1 日空けて連投感を出す
  - SEO ピーク 4/24-5/5 の中盤狙い

- **2026/04/25（土）**: **2 本立てスケジュール（実績）**
  - ✅ **午前〜午後**: SanDisk USB-C SSD クローン完了、BIOS 地獄突破（CSM 無効 + XHCI Hand-off 有効）→ 13:18 Windows 11 起動成功 + SanDisk Dashboard 5.2.2.3 でヘルスモニタリング体制確立
  - ⏸️ **14:00-17:00 予定の Claude for Word 作業 → 4/26 に順延**
  - ✅ **18:35〜**: SSD ブートバトル Substack 記事ドラフト + ready 版完成（@docs/substack/2026-04-25-sandisk-usb-c-boot-battle-substack-ready.md）→ 4/28 投稿予定
  - その他達成: 維新の嵐 1998 復活 / Mac↔Windows Claude 協働 / HDD 騒音 3 要素対策完了


- ~~**2026/04/19**: YouTubeプレミアムを解約する~~ ✅ 4/18 10:45 解除済（Y!mobile バリュー特典 YouTube Premium、2026/4/20 まで利用可能）
- **2026/04/21**: Y!mobile Netflixセット 自動解約発効日（3/21 加入 + 翌月同日ルール、以降 Netflix 視聴不可、追加対応不要）
- **2026/04/30**: Microsoft 365 Copilot Business 解約予定日（admin.cloud.microsoft で「有効期限切れ時にキャンセル」選択済、SUMA-p アカウント、MCA）— 当日以降にサブスクリプション一覧から消失していることを確認
- **2026/04/30（木）10:00-13:00**: **SSD 購入 長田区 3 店ラウンド（徒歩、はばタンPay+ 活用）**
  - ルート: ケーズデンキ新長田 → 大西ジム新長田 → エディオン西代（ラスト）
  - **はばタンPay+ 第 5 弾 50% プレミアム活用**（1 口 7,500 円を 5,000 円で購入、最大 4 口）
  - 利用期間: 2026-04-24 〜 2026-07-31、兵庫県民限定
  - 3 店とも はばタンPay+ 加盟想定（大西は要確認）
  - 総徒歩約 1.5km、2.5-3 時間で完了
  - 目標: 表示 ¥14,000 以下の 1TB NVMe、実質 ¥10,000 前後で入手（28-33% 実質値引）
  - 前日までに: 残高確認、未チャージなら 6/30 までにチャージ、大西の加盟有無確認
  - Google Calendar 登録済、詳細 @docs/routines/ssd-price-monitor.md
- **2026/05/11**: ElevenLabs Starter プラン失効（声クローン・Scribe 使用不可に）— それまでに使い倒す
- **2026/05/20 前後**: Y!mobile 151 に電話で最終確認（5月中 MNP 転出で 6月請求なし、を確認）
- **2026/05/29（木）〜5/30（金）**: **povo 2.0 へ MNP ワンストップ転出**（080-3108-7536 番号維持、Y!mobile 自動解約）
  - povo2.0 アプリ → MNP ワンストップ → ワイモバイル選択 → My Y!mobile 認証 → eSIM 発行 → iPhone 15 Pro 開通
  - 受付時間 9:30〜20:00（当日開通条件）、所要時間 最短15分
  - povo 事務手数料 0円、eSIM 発行 0円、基本料 0円/月（必要時のみトッピング購入）
  - Y!mobile は povo 開通と同時に自動解約（月途中でも日割りなし、満額だが割引で 0円）

### Y!mobile SIM トライアル 契約まとめ（pirosi80）

- 加入日: 2026/3/21、プラン: シンプル3M（eSIM、クレカ払い）
- Web 受注番号: YWO0000008576583
- **3ヶ月無料期間**: 3月（日割り）/ 4月 / 5月 ← 5月内に解約しないと 6月から満額 4,158円
- 3月請求: **-809円 クレジット**（Netflixキャンペーン調整分）
- 4月請求: 4/1–4/18 までの途中集計 4,099円（割引反映前、月末で 0円近くまで下がる想定）
- Netflixセット: 4/18 解約申込済、4/21 発効予定
- YouTube Premium バリュー特典: 4/18 解除済、4/20 まで利用可能

