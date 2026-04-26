# Microsoft 365 Copilot Researcher：GPT × Claude の Critique / Model Council 比較

> 一次情報の取得日: 2026-04-26
> ソース記事: <https://qiita.com/Oyu3m/items/4ce133a69433d386507d>
> 著者: @Oyu3m（お ゆ）／ Qiita / 2026-04-26 公開
> 入手経路: X（Twitter）共有リンク
> 関連既存ドキュメント: @docs/m365-copilot-claude-opus.md（M365 Copilot **Chat** 側の話、4/14 時点、Opus 4.6 採用記録）

## TL;DR

- M365 Copilot の **Researcher**（推論専用エージェント）が **Frontier プレビュー** で GPT 単体に加え、Claude 並列・直列の 2 モードを選べるようになった
- 切替メニューは「自動（Critique）」「Model Council」「単一モデル」の 3 系統
- **Critique = GPT 下書き → Claude 査読**、 **Model Council = GPT/Claude 同時推論 → 一致点 / 相違点 / 独自知見の要約**
- 著者のスループット観察: **「GPT がスピード重視」と公式説明されているが Model Council で先に終わるのは Claude のほうが多い** という重要な逆説
- 著者の感想は「『自動』でええやん、と思っていたが、それぞれ特色や使いどころが理解できてよかった」

## Researcher とは何か

- **Researcher**: M365 Copilot の推論専用エージェント。長時間・深い分析向け
- 従来は GPT モデル単体（Researcher の中身は OpenAI o3 系統と推測されてきた）
- 今回プレビュー機能として **Anthropic Claude が並列・直列で同居** する選択肢が追加された
- 名指しのモデル ID は非公表。著者は **「GPT-5.4」「Opus 4.7」を推測前提として明示** し検証
- **Frontier（プレビュー）扱い**で、テナント管理者により有効/無効化されている可能性あり（=自分が見えてない可能性も含めての注意喚起）

## 3 モードの仕様まとめ

切替画面に出る 3 系統。著者がまとめた特性を表に整理:

| モード | 処理 | 強み | 注意点 |
|---|---|---|---|
| **GPT 単体** | 単一推論 | 即答性・コスト効率・大量処理。Outlook/Teams/SPO/OneDrive/Planner と Web を高速統合 | 長期推論で抜けが出る。確認質問を省略して即答する傾向 |
| **Claude 単体** | 単一推論 | 段階的な深い推論、自己検証、長文コンテキスト、構造化、矛盾検出 | 出力が長く詳細寄り、曖昧プロンプトで質問返しが入って遅くなる、**処理コストが GPT 比 1.6〜2 倍** |
| **Critique（自動 / 直列）** | GPT で下書き → Claude が構成・完全性を査読 | 信頼性最重要のレポート。出典付与、再作業削減 | 応答時間 約 2 倍。単純タスクには過剰品質 |
| **Model Council（並列）** | GPT と Claude が同時に推論 → 一致点 / 相違点 / 独自知見を要約でハイライト | 複雑な意思決定、抜け漏れ防止、複数視点合成 | レポート 2 本＋要約で情報量過多、シンプルな問いには冗長 |

### Work IQ（M365 内部データへの参照）との連携

著者の表では各モードに「Work IQ で実現できること」が具体的に書かれている:

- GPT 単体 → 議事録要約、メール返信ドラフト、提案書初稿、ブレスト
- Claude 単体 → 数十万文字規模の契約書・規程の横断分析、リスク条項精査、複雑経緯の段階整理
- Critique → 役員向け四半期レビュー、社外提出文書、監査対応資料、法務・コンプライアンス分析
- Model Council → 新規事業検討、M&A 評価、複数プラン比較、合意形成プロセス

## 検証フロー（著者がモデルに投げた指示の骨格）

1. 「自分は GPT/Claude どっち？」と自己申告させる
2. それぞれに自分の得意・苦手を言わせる
3. 相手モデルを観察させる
4. お互いのズレを確認させる
5. どっちにどう任せると安心か、考えさせる
6. Researcher でどのモデルを使い分けるかをまとめさせる

著者はプロンプト本文は超長いとして掲載せず、上記の 6 ステップに圧縮して紹介。

## 著者の所見（重要な発見）

- **逆説**: 「GPT はスピード重視」と公式説明があるのに、 **Model Council で先に終わるのは Claude のことがほとんど**（=実装の挙動と公式キャラ付けがズレている）
- 「自動（=Critique）でええやん」と思って入っていったが、3 モードを比べると **使いどころが分かれる** ことが見えた、という体験談
- 「Model Council は同じ指示への GPT/Claude の差分が観察しやすい」 → **AI モデル比較ツールとして遊べる** ことを推奨

## コスト・速度観察

| 観点 | 著者の言及 |
|---|---|
| Claude 単体 | 「処理コストが高め（**GPT 比 約 1.6〜2 倍**）」 |
| Critique | 「2 モデル分の処理で応答に時間（**通常の約 2 倍**）」 |
| Model Council | 「2 レポート＋要約で情報量が多く、処理時間・コストも増加」 |

具体的なトークン数 / ドル換算は記事内に**なし**。

## 自分のコンテキストでの示唆

### 1. 4/30 の M365 Copilot Business 解約予定との関係

- CLAUDE.md / @docs/reminders.md に **2026-04-30 Microsoft 365 Copilot Business 解約予定**（admin.cloud.microsoft で「有効期限切れ時にキャンセル」選択済）が登録されている
- 解約を実行すると **この Researcher / Critique / Model Council 機能を試す機会も同時に消える**
- ただし **Frontier プレビュー** 扱いなので、 Business プランで自分のテナントに来ているかは別問題（要確認）
- 4/30 までに admin.cloud.microsoft で **Researcher の Frontier 設定が有効化されているか** を一度見る価値がある（記事内にも「管理者により制御」の注意あり）

### 2. 自分の AI モデル比較スタックとの照合

- Claude Code 内の Opus 4.7 + Sonnet 4.6 の使い分け（思考=Opus、実行=Sonnet）と、Researcher の Critique（GPT 下書き → Claude 査読）は **直列パイプライン思想として近い**
- ただし Researcher は **モデル間で査読する** 設計、自分のローカルは **同社内（Anthropic）のサイズ違いで分担** という構造の差がある
- 「Model Council 並列」相当のことは、 個人運用では **Mac 側 Claude Code と Windows 側 Claude Code の Inter-AI Chat**（4/25 構築、pdf-reader 内）で擬似的にやっている

### 3. AI モデルベンチマークとしての面白さ

- 同一プロンプト ×（GPT, Claude）の **同時推論結果差分** が見やすいのは確かに価値が高い
- これは Substack ネタにできる: 「M365 Copilot Researcher で GPT と Claude を Model Council にかけてみたら、公式説明と挙動が違った」みたいな切り口

## 残った疑問・検証ポイント

- [ ] **モデル ID の正体**（GPT-5.4 / Opus 4.7 は本当か？）— Microsoft 公式で M365 Copilot のモデル ID を出す慣習がないので、検証は X / Anthropic API ログ照合等で
- [ ] **Frontier プレビューの一般展開時期**（Business / Enterprise / Education のどこまで来るか）
- [ ] **Researcher の Claude 連携で利用される Anthropic API はどのテナントの請求？** — Microsoft 側持ちなのか、ユーザーテナントの API 経由なのか
- [ ] **Work IQ（SPO / Teams / Outlook 統合）が Claude にも完全に開放されているか** — GPT 経由に比べて参照精度が同等か
- [ ] **Model Council の「先に終わるのは Claude」現象の再現性** — タスク種別・プロンプト長で挙動が変わるかは追加検証余地
- [ ] **コスト**: 著者は「GPT 比 1.6〜2 倍」とだけ書いているが、ユーザー側 Copilot ライセンス（$30/月）から見るとサブスク型なので**ユーザー請求は変わらない**はず。1.6〜2x はおそらく Microsoft の内部原価論

## 関連ドキュメント

- @docs/m365-copilot-claude-opus.md — 4/14 時点の M365 Copilot **Chat** + Opus 4.6 一次情報（Chat と Researcher は別機能）
- @docs/m365-copilot-cowork-opus47-autonomous-replan.md — **Cowork** × Opus 4.7 の自律再計画挙動（Researcher = 深い調査 / Cowork = 長時間自律実装、対比対象）
- @docs/journal/2026-04-26.md — 本記事を取り込んだセッションログ
- @docs/x-daily-briefing.md — Anthropic / OpenAI の動きを並べて追っているデイリーログ
- @docs/reminders.md — 2026-04-30 M365 Copilot Business 解約予定

## タグ

#m365-copilot #researcher #claude #gpt #critique #model-council #ai-comparison #qiita-source
