# Microsoft が今朝 1 時にこっそり投下した「Living Desktop」を解体したら、Clippy の亡霊と Anthropic 標準が出てきた

---

## 発端は一本の短縮 URL

> 「https://aka.ms/CopilotKeyboardx64build」

2026 年 4 月 23 日の朝、友人が一本の URL を送ってきた。Microsoft の公式短縮 URL サービス `aka.ms` で、ドメインを見る限り間違いなく本物の Microsoft が管理している。だが、そこから何が降ってくるのかは誰も書いていない。

リダイレクト先は `download.microsoft.com` の直接ダウンロード。ファイル名は `CopilotKeyboard_x64_1.0.0.6421.msi`、サイズは **382MB**。リリース時刻を見ると **2026-04-23 01:00 UTC** = 日本時間の朝 10 時ちょうど。たった数時間前に公開されたばかりのバイナリだ。

GitHub に `microsoft/CopilotKeyboard` というリポジトリは存在するが、README は一行「# CopilotKeyboard」だけ。説明も、タグも、ウェブサイトも、リリースノートも、**すべて空**。スター 3、フォーク 1。事実上の**隠しリポジトリ**。

Google 検索しても 2026 年 4 月 23 日朝の時点でこれを取り上げた記事は皆無。「Microsoft が、今朝、何か、こっそり公開した」以上の情報がどこにもない。

火がついた。**解剖してみることにした**。

---

## 第一層: MSI を開く

MSI ファイルの `SummaryInformation` を `msiinfo` で覗くと、まず目を引いたのが次の一行。

```
Template: x64;1041
```

**1041 は LCID (Locale ID) の 0x0411 = 日本語**。つまりこの製品は最初から**日本市場限定**で配布されている。`ProductLanguage: 1041` も一致。ProductName は "Copilot Keyboard"、Manufacturer は Microsoft Corporation。公式製品確定。

製品の中身一覧を出すと、いかにも IME らしいファイルが並んでいる。

- **MAIIME.dll** (3.8MB) — Microsoft AI IME、変換エンジン本体
- **sdds0411.dic** (55MB) — 巨大な日本語辞書（ファイル名の 0411 もやっぱり日本語 LCID）
- **MAI_BingASDS.dll** (1.2MB) — Bing Auto Suggest Dictionary System
- **MAI_IMJPLMP.dll** — 日本語言語モデルパッケージ
- **MtfServerHost.exe** — Microsoft Text Framework サーバー
- **CopilotKeyboardOOBE.exe** — 初回起動体験 (Out-of-Box Experience)
- **Aqua.imeskin** — カスタマイズ可能な **IME スキン**

ここまでで頭に浮かんだのは「**Microsoft が次世代の日本語 IME を出したのか**」という仮説。MS-IME の後継か、ATOK / Google 日本語入力への対抗か。十分に面白い話だ。

ところが、この仮説は **第二層で完全に崩壊する**。

---

## 第二層: Electron の中身を剥く

MSI を全展開すると 892MB、603 ファイルになる。そのうち **205MB を占める巨大な実行ファイル**が目に入った。

```
Appearance.exe (204MB)
resources/
├── app.asar (21MB)  ← Electron のアプリコード
└── app.asar.unpacked/
```

**Electron 製アプリだ**。しかも ffmpeg.dll、vulkan-1.dll、v8_context_snapshot.bin といった Chromium の DLL 一式が付随する本格派。IME のフロントエンドにしてはやりすぎている。

`@electron/asar` で `app.asar` を展開すると、トップレベルファイルに目が釘付けになった。

```
aqua.glb
erin.glb
kyle.glb
mica.glb
vendor/three.min.js
LivingDesktop.esproj
```

**.glb は glTF Binary**（3D モデルのバイナリ形式）。Three.js を載せて WebGL で 3D キャラクターを 4 体描画している。さらに **プロジェクトファイル名が `LivingDesktop.esproj`**。内部コードネームが「**Living Desktop**」であることが、ここで確定した。

「これは IME じゃない。**3D キャラクターが常駐するデスクトップアシスタント**だ」と理解した瞬間、記憶の底から一つのキャラクターが浮かび上がってきた。

**Clippy**。

---

## 第三層: main.js 12,332 行の中身

`main.js` 12,332 行を読み解いた結果、この製品の機能セットが浮かび上がった。

**10 個のグローバルショートカット**がレジストリに登録される。

- **Ctrl+Alt+M** — 会議関連（Meeting）
- **Ctrl+Alt+S** — ステータスメール生成
- **Ctrl+Alt+W** — **週報自動生成**
- **Ctrl+Alt+T** — **選択テキストを翻訳**
- **Ctrl+Alt+P** — **選択テキストをリライト**
- **Ctrl+Alt+C** — **キャレット前テキストを補完**
- **Ctrl+Alt+D** — 文書 URL 挿入
- **Ctrl+Alt+R** — テキストレビュー
- **Ctrl+Alt+I** — **イントロ・アウトロ生成（トーン指定可）**
- **Ctrl+Alt+H** — **メール/チャット返信生成（複数候補）**

しかも選択テキストの取得は **UI Automation API** 経由。つまり Word でも Slack でもブラウザでも、**Windows の全アプリでアクティブに選択されているテキスト**を IME が読み取って処理できる。

AI アシスタント UI は **13 種類のサブウィンドウ**で構成され、プレビュー、返信候補選択、イントロアウトロ、会議ブリーフィング、会議詳細、ドキュメントピッカーなどが用途別に用意されている。

そして最終盤で、私は**想定外のキーワード**に出会った。

---

## 第四層: MCP

コードを読み進めると、こんな記述に行き当たる。

```javascript
const notification = {
    jsonrpc: '2.0',
    method: 'notifications/initialized'
};
mcpProcess.stdin.write(JSON.stringify(notification) + '\n');
```

**JSON-RPC 2.0**。`notifications/initialized`。加えて、コメントと変数名に何度も `MCP` という文字列が現れる。

`workiq.exe` を `workiq mcp` という引数で起動し、stdin/stdout で JSON-RPC 通信している。これは紛れもなく **Model Context Protocol**、Anthropic が 2024 年 11 月に提唱した AI エージェント向け標準プロトコルの実装だ。

つまり、**Microsoft は自社の AI アシスタントの中核プロトコルとして、競合 Anthropic が提唱した標準を採用している**。

2024 年の MCP 公開時、Microsoft は公式には反応を示さなかった。しかし水面下では、Bing Japan チームが MCP を内部実装に取り込み、2026 年 4 月の今朝、日本市場向けプロダクトとしてリリースした。

業界の力関係を示す、静かだが決定的な一手。

---

## 第五層: 誰が作ったのか

SETUP.md という開発者向けドキュメントが asar の中に残されていた。Microsoft の内部開発者が参照するはずの、本来は外部に出ないはずのメモ。そこにはこう書かれていた。

> ```
> 4. Azure Artifacts Credential Provider (for internal npm packages)
>    - This is required to access the BingJapan npm registry
> ```

**BingJapan npm registry**。Microsoft 日本支社の Bing チームが保有する社内専用の npm パッケージ配布基盤。`@microsoft/workiq`（本製品の MCP サーバー）もここから配布されている。

これでパズルが全部埋まった。

- **開発元**: Microsoft Bing Japan
- **対象市場**: 日本（ProductLanguage 1041）
- **製品名**: Copilot Keyboard
- **内部コードネーム**: Living Desktop
- **配布形態**: サイレントリリース、日本市場先行
- **AI 基盤**: Anthropic 標準の MCP + WorkIQ サーバー
- **UI**: 3D キャラクター（Three.js）+ Electron
- **機能**: Microsoft 365 Copilot 全部乗せ + Outlook 統合 + 日本語 IME

---

## 歴史的文脈: Clippy の 29 年越しの復活

Microsoft の AI アシスタントの系譜を並べると、本製品の歴史的位置づけが見えてくる。

- **1997** — Office Assistant "Clippy"（「お手伝いします」で有名になったクリップ）
- **2007** — Clippy 退役、世界中のオフィスワーカーが拍手
- **2014** — Cortana 登場（音声アシスタント、キャラクターなし）
- **2023** — Cortana、Windows から削除
- **2023** — Microsoft 365 Copilot 登場（AI、キャラクターなし）
- **2024** — Copilot+PC（ハードウェア側の AI 統合）
- **2026/04/23** — **Copilot Keyboard / Living Desktop**（本日）

29 年。Clippy が退役してから 19 年。Microsoft は AI キャラクター路線から一度完全撤退したあと、日本市場でひっそりと**キャラクター AI を復活させた**ことになる。

しかも、Clippy が「押し付けがましい」と嫌われた反省を踏まえて、今回の 4 体（aqua/erin/kyle/mica）はドラッグで動かせ、画面端でスライドし、2 秒ホバーで初めてツールチップが出る。UX は大きく洗練されている。

---

## 技術的示唆

### 1. Microsoft が MCP を採用した

これは **AI プロトコル標準化の大きな転換点**。Anthropic が提唱した MCP が、競合 Microsoft の製品に統合された。2025 年中に OpenAI、Google、その他多くのツールベンダーが MCP をサポートし、2026 年 4 月時点で事実上の業界標準化している流れの一部だが、**Microsoft の実装例が公に表に出たのはこれが恐らく最初**。

### 2. 日本市場が先行ロールアウトの場になった

Cortana が日本で終了、Copilot が英語圏優先だったこれまでの流れを覆し、**日本が AI UX 実験の先行市場**になっている。理由は推測になるが、日本語という言語的独自性、Outlook + Office の高い普及率、キャラクター文化への親和性など、複数の要因が考えられる。

### 3. 日本語 IME と AI エージェントの融合

ATOK も MS-IME も Google 日本語入力も、最終的には「変換候補の精度」を競ってきた。本製品はそこを突破し、**入力中のテキストそのものを AI 処理の入り口**にした。Ctrl+Alt+T で翻訳、Ctrl+Alt+P でリライト、Ctrl+Alt+C で補完。IME は変換装置から**執筆支援ハブ**に進化する。

---

## プライバシーの不安要素

インストール前に知っておくべきこと。

- **テレメトリ**: Microsoft 1DS (OneCollector) に `trackEvent('WorkIQ_XxxFeature_Requested')` で各機能の利用状況 + locale が送信される
- **Outlook 読み取り**: COM オブジェクト経由でメール本文にアクセス、AI 処理に使用
- **UI Automation**: 全アプリの選択テキストを取得可能
- **クリップボード監視**: 常時
- **段階的ロールアウト**: `HKCU\Software\Microsoft\CopilotKeyboard\Jpn\EnabledFeatures` レジストリキーが設定されたユーザーのみ WorkIQ 機能が有効（= A/B テスト中の可能性）

機能の便利さと、Microsoft がどこまでデータを見るかのトレードオフ。現時点で日本語による利用規約・プライバシーポリシーの公式文書は未公開（少なくとも aka.ms からは届かない）。

---

## 結び

2026 年 4 月 23 日の朝、Microsoft は日本語ユーザーに向けて、Clippy の亡霊と Copilot の頭脳と Anthropic の標準プロトコルを一つの Electron アプリに詰め込み、**誰にも告知せず投下した**。

プレスリリースなし。公式ブログなし。GitHub の README は空。Twitter での発表もない。

「見つけた人は勝手に使ってね。動作するから」

この配布の仕方が意図的なら、**日本市場での静かなユーザーテスト**が目的なのだろう。日本 IT 業界がこれを一ヶ月後に発見する頃には、Microsoft はフィードバックを集め、次のリリースに反映しているはずだ。

もし意図的でなければ、Bing Japan チームのだれかが **aka.ms を早すぎるタイミングで有効化**してしまったのかもしれない。

どちらにせよ、**あなたはこの記事を読んだ時点で、日本のテック界隈の 0.01% に入る早期発見者**になった。3D キャラクターが Windows デスクトップに復活する時代の幕開けを、朝のコーヒーを飲みながら一緒に見届けてくれてありがとう。

---

## 技術詳細の完全版

GitHub の `wirelessml/test` リポジトリに、MSI 解体・Electron 展開・main.js 12,332 行の分析結果を 351 行の技術メモとして公開している。興味ある人はどうぞ。

→ [技術解析メモ（GitHub）](https://github.com/wirelessml/test/blob/main/docs/discovery/copilot-keyboard-analysis-2026-04-23.md)

## 取扱注意

本記事はリバースエンジニアリングの結果であり、Microsoft の公式見解ではない。MSI のダウンロード・解体は研究・学習目的で行い、動作検証は自己責任で。本番環境へのインストールは、プライバシーリスクを理解した上で判断を。

本記事の解釈・推測部分（「日本先行パイロットの可能性」など）は証拠からの推論であり、Microsoft 内部の正確な意図ではない可能性がある。
