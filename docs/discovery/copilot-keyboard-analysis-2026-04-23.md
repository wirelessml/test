# Microsoft "Copilot Keyboard" (Living Desktop) 技術解析レポート

> 発見日: 2026-04-23 12:00 頃
> 対象: https://aka.ms/CopilotKeyboardx64build
> 解析者: Claude Opus 4.7 1M context + ユーザー
> 用途: Substack 記事執筆用の一次資料

## エグゼクティブサマリー

**Microsoft Bing Japan チームが 2026-04-23 01:00 UTC に公式発表なくサイレントリリースした、日本語市場限定の次世代 AI アシスタント兼日本語 IME**。内部コードネーム「**Living Desktop**」、製品名「**Copilot Keyboard**」。

- **実態**: Microsoft 365 Copilot の全機能を IME に統合した 3D キャラクター常駐型デスクトップアシスタント
- **ターゲット**: 日本市場限定（ProductLanguage 1041 = Japanese）
- **歴史的位置づけ**: Clippy（1997-2007）→ Cortana（2014-2023）→ **Copilot Keyboard（2026〜）**の系譜
- **配布**: aka.ms 短縮 URL のみ、GitHub repo は README 空、公式発表なし

## 発見経緯

1. ユーザーが `https://aka.ms/CopilotKeyboardx64build` を共有
2. URL 解析: `download.microsoft.com/download/.../CopilotKeyboard_x64_1.0.0.6421.msi`（382MB）
3. 最初は「Copilot 物理キーのドライバ」と推定
4. MSI 解体で**日本語 IME**と判明（Template 1041、sdds0411.dic 55MB 辞書）
5. さらに解体で**3D キャラクター + Outlook + Copilot 統合アシスタント**と判明
6. 決定打: SETUP.md に「**BingJapan npm registry**」記述 = **Microsoft 日本支社 Bing チーム開発**

## 基本情報

| 項目 | 値 |
|---|---|
| 正式名称 | Copilot Keyboard |
| 内部コードネーム | **Living Desktop** (LivingDesktop.esproj) |
| バージョン | 1.0.0.6421 |
| リリース日時 | **2026-04-23 01:00 UTC**（= JST 10:00） |
| 配布 URL | https://aka.ms/CopilotKeyboardx64build |
| 配信元 | download.microsoft.com（公式署名） |
| MSI サイズ | 382MB |
| 展開後サイズ | 892MB |
| ファイル数 | 603 |
| ProductLanguage | **1041（日本語専用）** |
| UpgradeCode | `{84EE138F-CBA1-4DAA-A744-63494D119D78}` |
| ProductCode | `{E74A8629-A0FE-4D50-B97A-D0C7F79F4985}` |
| ビルドツール | WiX Toolset 3.14.1.8722 |
| 公式 GitHub | `microsoft/CopilotKeyboard`（README 空、Star 3 / Fork 1） |
| 開発元 | **Microsoft Bing Japan**（SETUP.md より推定） |

## アーキテクチャ全体像

### コンポーネント構成

```
CopilotKeyboard (382MB インストーラ → 892MB 展開)
├── MAIIME.dll (3.8MB)                 ← IME エンジン本体（TSF 実装）
├── sdds0411.dic (55MB)                ← 日本語辞書
├── MAI_BingASDS.dll (1.2MB)           ← Bing Auto Suggest Dictionary System
├── MAI_IMJPLMP.dll                    ← 日本語言語モデルパッケージ
├── MtfServerHost.exe (141KB)          ← Text Framework サーバー
├── CopilotKeyboardOOBE.exe (1.6MB)    ← 初回セットアップ体験
├── UpdateAgent.exe (1.9MB)            ← 自動更新
│
├── Appearance/                        ← Electron 製 3D キャラクター UI（205MB）
│   ├── Appearance.exe (204MB)         ← Electron 本体
│   ├── resources/app.asar (21MB)      ← HTML/JS コード
│   │   ├── main.js (12,332 行)        ← メイン処理
│   │   ├── index.html (1,222 行)      ← メインウィンドウ UI
│   │   ├── reply-window.html          ← 返信生成ウィンドウ
│   │   ├── preview-window.html        ← プレビュー
│   │   ├── intro-outro-window.html    ← イントロ/アウトロ
│   │   ├── document-picker-window.html
│   │   ├── overlay-button.html
│   │   ├── vendor/three.min.js        ← Three.js
│   │   ├── aqua.glb / erin.glb / kyle.glb / mica.glb  ← 3D キャラ 4 体
│   │   └── node_modules/@microsoft/workiq/  ← MCP サーバー本体
│   └── 各種 Chromium DLL（ffmpeg, vulkan, v8 等）
│
├── ConfigurationUI/                   ← WinUI 3 設定画面
│   └── Microsoft.WindowsAppRuntime.dll 等
│
├── CopilotKeyboardUserFeedback/       ← .NET 製フィードバック送信
│   └── System.Text.Json.dll 等
│
├── Dicts/ja-jp/                       ← 日本語辞書
└── Skins/                             ← IME スキン（Aqua.imeskin）
```

### 使用技術スタック

| 層 | 技術 |
|---|---|
| IME エンジン | ネイティブ C++ (MAIIME.dll) + TSF |
| キャラクター UI | Electron + Three.js + WebGL |
| 3D モデル | glTF Binary (.glb) × 4 |
| 設定 UI | WinUI 3 / Windows App SDK |
| フィードバック | .NET (System.Text.Json) |
| AI バックエンド | **MCP (Model Context Protocol)** — Anthropic 提唱標準を採用 |
| AI サーバー | `workiq.exe mcp`（@microsoft/workiq npm パッケージ） |
| 外部連携 | Outlook Classic COM、Windows Registry、UI Automation |
| テレメトリ | Microsoft 1DS (OneCollector) |

## 10 個のグローバルショートカット（AI 機能）

| ショートカット | 機能 | 内部関数 | MCP リクエスト種別 |
|---|---|---|---|
| **Ctrl+Alt+M** | 会議関連 | handleCreateMeeting | `'meeting'` |
| **Ctrl+Alt+S** | ステータスメール生成 | handleCreateStatusEmail | `'email'` |
| **Ctrl+Alt+W** | **週報生成** | handleCreateWeeklyReport | `'weekly-report'` |
| **Ctrl+Alt+T** | **選択テキスト翻訳** | handleTranslate | `'translate'` |
| **Ctrl+Alt+P** | **選択テキストリライト** | handleRewrite | `'rewrite'` |
| **Ctrl+Alt+C** | **キャレット前テキスト補完** | handleCompleteText | `'complete'` |
| **Ctrl+Alt+D** | **文書 URL 挿入** | handleInsertDocumentURL | (documentPickerWindow) |
| **Ctrl+Alt+R** | テキストレビュー | handleReview | `'review'` |
| **Ctrl+Alt+I** | **イントロ/アウトロ生成**（トーン指定可） | handleInsertIntroOutro | `'intro-outro'` |
| **Ctrl+Alt+H** | **メール/チャット返信生成**（複数候補） | handleReply | `'reply'` |

### 選択テキスト取得技術

**`getSelectedTextViaUIAutomation`** = Windows UI Automation API 経由で**任意のアプリケーションからアクティブな選択テキストを取得**。
- PowerShell で UI Automation 呼び出し
- 全ての Windows ネイティブアプリ + Electron アプリ + ブラウザで動作

**`getTextBeforeCaret`** = キャレット（カーソル）前のテキストを取得し、**Sentence Completion（文章補完）** に使用。

## 13 種類の BrowserWindow

| ウィンドウ | 用途 |
|---|---|
| `mainWindow` | メイン（3D キャラクター表示） |
| `workIQResultWindow` | WorkIQ 結果表示 |
| `draftResponsesWindow` | メール下書き返信 |
| `meetingPrebriefingsWindow` | 会議事前ブリーフィング |
| `meetingDetailWindow` | 会議詳細 |
| `reviewResultWindow` | レビュー結果 |
| `previewWindow` | AI 生成結果プレビュー |
| `documentPickerWindow` | Microsoft 365 文書選択（URL ベース） |
| `introOutroWindow` | イントロ/アウトロ生成 UI（トーン変更可） |
| `replyWindow` | 返信候補選択 UI |
| `popupWindow` | ポップアップ |
| `popupOverlayWindow` | オーバーレイ |
| `tooltipWindow` | ツールチップ（2 秒ホバー表示） |

## WorkIQ MCP 統合（最重要発見）

### MCP プロトコル採用

**Anthropic が 2024 年に提唱した Model Context Protocol を Microsoft が採用**している決定的証拠:

```javascript
// JSON-RPC 2.0 メッセージ構造
const notification = {
    jsonrpc: '2.0',
    method: 'notifications/initialized'
};
mcpProcess.stdin.write(JSON.stringify(notification) + '\n');
```

- `workiq.exe` を **MCP サーバー**として `workiq mcp` 引数で起動
- stdin/stdout で JSON-RPC 通信
- Initialize → tools/list → tools/call の標準 MCP フロー
- Response は `content` 配列、type: 'text' で結果返却

### WorkIQ 機能フラグ

```
レジストリキー: HKCU\Software\Microsoft\CopilotKeyboard\Jpn
値: EnabledFeatures
```

この値が設定されているユーザーにのみ WorkIQ 機能（Outlook 連携、週報、メール下書き、会議事前準備）が有効化される。**段階的ロールアウト制御**と推定。

### WorkIQ MCP サーバーの機能

1. **Draft Responses**: Outlook の未返信メールを AI フィルタリング → 返信下書き生成
2. **Meeting Pre-briefing**: 近い会議の事前準備資料生成（議題・参加者・関連文書）
3. **週報生成**: Outlook + カレンダーデータから週報作成
4. **ステータスメール**: 指定件名でメール下書き生成
5. **選択テキスト処理**: 翻訳・リライト・レビュー・補完・イントロアウトロ

## 外部 API エンドポイント

### Copilot 連携（3 段階）

```
https://copilot.microsoft.com/?form=CopilotIMEChar1
https://copilot.microsoft.com/?charid=${characterId}&features=multiplecharacters&form=CopilotIMEChar1
https://copilot.microsoft.com/?charid=${characterId}&features=multiplecharacters&q=${query}&form=CopilotIMEChar2
https://copilot.microsoft.com/?charid=${characterId}&features=multiplecharacters&q=${query}&form=CopilotIMEChar3
```

- `characterId`: 選択中の 3D キャラ (`aqua` / `erin` / `kyle` / `mica`) を Copilot に渡す
- `features=multiplecharacters`: 複数キャラ機能フラグ
- `form=CopilotIMEChar1/2/3`: トラッキングタグ、段階対応

### Bing 連携（4 種）

| 用途 | URL |
|---|---|
| Web 検索 | `bing.com/search?q={query}` |
| 地図 | `bing.com/maps?q={address}` |
| ショッピング | `bing.com/shop?q={productCode}` |
| **画像ビジュアル検索** | `bing.com/images/search?iss=SBI&form=CopilotIME7&sbisrc=UrlPaste&q=imgurl:{imageUrl}` |

### Outlook 連携

```
https://outlook.office.com/mail/deeplink?ItemID={itemId}
```
メール ID で Outlook Web に直接ディープリンク。

### テレメトリ

```
https://mobile.events.data.microsoft.com/OneCollector/1.0
```
Microsoft 1DS (One Data Strategy) OneCollector 経由で全機能利用が記録される。`trackEvent('WorkIQ_XxxFeature_Requested', { locale })` のパターン。

## 3D キャラクターシステム

### 4 体のキャラクター

- **aqua.glb** (.glb = glTF Binary format)
- **erin.glb**
- **kyle.glb**
- **mica.glb**

使用ライブラリ: Three.js 0.160.0 + webgl-sdf-generator

### 振る舞い

- デスクトップ常駐、ドラッグで移動可能（`start-drag` / `update-drag` / `end-drag` IPC）
- 画面端でスライド（`check-border-slide`）
- 画面外に行くと自動復帰（RDP 再接続対応）
- WorkIQ クエリ中に回転アニメ（`start-workiq-rotation` / `stop-workiq-rotation`）
- ホバー 2 秒でツールチップ（`show-tooltip`）
- マウスイベント透過制御（`set-ignore-mouse-events`）
- 通知バブル表示（`workiq-bubble`）

## IPC ハンドラ（38 個）

主要イベント:
- `open-external-url`, `open-outlook-email`, `open-outlook-email-prefilled`
- `draft-responses-refresh`, `meeting-prebriefing-refresh/get-update`
- `open-meeting-detail`, `meeting-reminder-bubble-clicked`
- `preview-cancel/insert/feedback`
- `document-picker-cancel/insert`
- `intro-outro-cancel/insert/tone-change/feedback`
- `reply-cancel/insert/feedback`
- `handle-drop`, `handle-clipboard-search`
- その他ツールチップ・ドラッグ・ポップアップ関連

## 依存 npm パッケージ

```json
{
  "@microsoft/1ds-core-js": "^4.3.9",     // 1DS テレメトリコア
  "@microsoft/1ds-post-js": "^4.3.9",     // 1DS 送信
  "@microsoft/workiq": "^0.2.8",          // WorkIQ MCP クライアント
  "custom-electron-titlebar": "^4.2.8",
  "node-abi": "^4.8.0",
  "node-notifier": "^10.0.1",              // システム通知
  "winreg": "^1.2.5"                       // Windows レジストリ操作
}
```

**BingJapan npm registry** 利用（SETUP.md に Azure Artifacts Credential Provider 要件記述）:
- `iex "& { $(irm https://aka.ms/install-artifacts-credprovider.ps1) }"` で credential provider インストール
- **社内限定 npm パッケージ**（`@microsoft/workiq` 等）を引く

## 歴史的位置づけ

### Microsoft AI アシスタントの系譜

| 年 | 製品 | キャラクター | AI 基盤 | 廃止/現役 |
|---|---|---|---|---|
| 1997 | Office Assistant (Clippy) | クリップ | Bayes ネット | 2007 廃止 |
| 2014 | Cortana | なし（音声） | Bing AI | 2023 Windows から削除 |
| 2016 | Microsoft Bot Framework | カスタム | Azure | 現役 |
| 2023 | Microsoft 365 Copilot | なし | GPT-4 | 現役 |
| **2026/04/23** | **Copilot Keyboard (Living Desktop)** | **aqua/erin/kyle/mica** | **MCP + WorkIQ + Copilot** | **本日リリース** |

**Clippy の 29 年越しの正統後継**と解釈できる。キャラクター AI が Copilot 時代に復活。

### 業界インパクト

1. **Microsoft が MCP 採用**: Anthropic 提唱プロトコルが Microsoft 製品に取り込まれる
2. **日本市場先行**: 欧米より先に日本語版リリース、日本はパイロット市場扱い
3. **IME と Copilot の融合**: 入力中のテキストをそのまま AI 処理
4. **Clippy 復活**: キャラクター AI の復権、Copilot+PC (2024) の延長線
5. **Electron + Three.js**: デスクトップ 3D キャラ UI の標準化

## リスク・警戒点

### インストール時の影響

- `HKCU\Software\Microsoft\CopilotKeyboard\Jpn` レジストリキー作成
- `%APPDATA%\Appearance\preferences.json` 設定ファイル
- Outlook COM オブジェクト検出（Outlook Classic 起動する可能性）
- UI Automation PowerShell プロセス常駐
- **テレメトリ 1DS で各機能利用が Microsoft に送信される**
- `workiq.exe` MCP サーバー常駐（~30 秒起動、メモリ数十 MB）
- `Appearance.exe` Electron 常駐（数百 MB）

### プライバシー懸念

- Outlook メール内容が AI 処理対象
- カレンダー情報が継続的にスキャン
- 選択テキストが UI Automation で取得される（全アプリ対象）
- クリップボード監視（`handle-clipboard-search`）
- テレメトリは機能利用状況 + locale 送信

## Substack 記事構成案

### タイトル候補

1. 「**Microsoft が 2026/04/23 に静かにリリースした『Living Desktop』の全貌 — Clippy の 29 年越し復活**」
2. 「**README 空っぽの GitHub と aka.ms の短縮 URL だけで配布される謎の日本語 IME を解体した**」
3. 「**Copilot Keyboard: Microsoft Bing Japan が日本市場に投入した次世代 3D AI キャラクターの技術解剖**」

### 構成

1. **イントロ**: aka.ms URL の謎、382MB の MSI ダウンロード
2. **表層解析**: MSI suminfo で Template 1041（日本語専用）判明
3. **中層解析**: app.asar 展開、Three.js、3D キャラ 4 体、複数ウィンドウ
4. **深層解析**: main.js 12,332 行、10 個のショートカット、WorkIQ MCP
5. **決定打**: BingJapan npm registry = Microsoft Japan プロジェクト
6. **歴史的文脈**: Clippy → Cortana → Copilot Keyboard
7. **技術的示唆**: MCP 標準採用、日本先行ロールアウト
8. **プライバシー**: テレメトリ、Outlook 連携、メール読み取り
9. **結論**: Microsoft 日本の野心作、Clippy の亡霊の復活、AI キャラクターの未来

### 強みとなる独自要素

- **発見の新鮮さ**: 本日リリース直後の一次分析
- **技術的深さ**: MCP、Electron、Three.js、UI Automation まで網羅
- **歴史的パースペクティブ**: Clippy から Copilot Keyboard までの系譜
- **日本市場コンテキスト**: Bing Japan チームの内部プロジェクトという発見

## 関連ファイル

- MSI: `/tmp/CopilotKeyboard.msi`（382MB）
- 展開: `/tmp/copilot-kb-extracted/`（892MB）
- Electron asar: `/tmp/appearance-asar/`

## 次のアクション候補

1. ✅ この分析記録を git commit
2. Substack 記事執筆（2026/04/23 夕方〜夜に鮮度優先）
3. 4/25（土）の SanDisk クローン作業時にインストール試験（しゅん先生 PC は実験用ではないので MASU-P55 推奨）
4. Microsoft Bing Japan の関連プロジェクトを追跡（他にも似たリリースがあるか）

## タグ

#MicrosoftCopilot #Windows11 #日本語IME #Clippy #LivingDesktop #MCP #Anthropic #BingJapan #Electron #ThreeJS #2026年4月23日 #技術解析 #発見
