# Appfolio — クリエイティブアプリ チュートリアル動画プラットフォーム（観察）

> 観察日: 2026-04-26 23:00 JST
> 発見元: ユーザー共有 URL（@docs/journal/2026-04-26.md 22:30 セクション）
> URL: https://appfolio.one/videos
> ページタイトル: 「動画 | Appfolio」

## 何をしているサイトか

iPad / Mac のクリエイティブ系アプリ操作チュートリアル動画を集約した、日本語のサブスクリプション風ラーニングプラットフォーム（推定）。Expo（React Native Web）製の SPA で、ボトムタブナビ（動画 / マイリスト / アカウント）を持ちアプリ的な UI。

## サイト構成（2026-04-26 時点で観測）

### アプリ別アイコン行（カテゴリ）
- すべて
- Procreate / Procreate Dreams
- Goodnotes
- Canva
- 写真
- Affinity Designer
- メモ
- ファイル
- Adobe Fresco
- Notion
- Craft
- LumaFusion

### セクション1: 「無料で見れる」

| クリエイター | タイトル冒頭 |
|---|---|
| Kiemi | Google スライドで機… ページリンク… |
| amity_sensei | 文字×素材で作るモーション動画 |
| しゅえ | フレームアニメで描く手書き風テキス… |
| Nanami | フリーボード活用術！無限キャンバ… |
| amity_sensei | 手描きをベクター化！Linearity Curv… |
| しゅえ | おしゃれなマスキングテープをデザイ… |

### セクション2: 「新着セッション」

| クリエイター | タイトル冒頭 | テーマ |
|---|---|---|
| (Adobe Capture) | Adobe Capture で作るオリジナル素材… | 素材制作 |
| Akari | Pages でキッズ向けイベントチラシ制… | デザイン |
| **haru** | **毎朝のニュース収集を自動化！ChatGP…** | **AI 自動化** |
| ろっち | Pixelmator Pro で写真を劇的に変える… | 写真編集 |
| amity_sensei | 制作スピードが爆上がり！Apple Penci… | 入力デバイス |
| しゅえ | Pixelmator Pro でコラージュ作り！魅… | 写真編集 |

### ボトムナビ
- 動画（現在表示）
- マイリスト
- アカウント

## 主要クリエイター

- **amity_sensei**: 「無料で見れる」と「新着」の両方に登場、最も露出が多い。iPad クリエイティブ系の有名インフルエンサー
- **しゅえ**: 露出 3 本、フレームアニメ・マスキングテープ・Pixelmator 系
- **Nanami**: フリーボード（macOS / iPad の白板アプリ）解説
- **haru**: ChatGPT × ニュース自動化 — **AI 自動化系で唯一の作品**
- **Kiemi / Akari / ろっち**: それぞれ単発作品

## 仲側の文脈での意味

### しぶ／あい Claude Code 動画編集自動化との接続

- 同日（2026-04-26）に観測された **あい (@ikeai_minimalist) → しぶさん 動画編集の Claude Code 自動化** 文脈と整合
- Appfolio の「新着」に既に **haru「毎朝のニュース収集を自動化！ChatGP…」** という ChatGPT 業務自動化チュートリアルが存在
- → 「クリエイティブアプリのチュートリアル」プラットフォームに **AI 自動化 tutorial** が浸透し始めている兆候
- しぶ社内の Claude Code 必須研修（Reels で言及）が量産する「ディレクター視点」エンジニアが、こうしたプラットフォームのコンテンツ供給側に回る可能性

### LumaFusion をカテゴリに含む点

- LumaFusion = iPad の動画編集アプリ
- 仲が運用中の動画編集系ナレッジ（@docs/transcripts/davinci-resolve-photo-editing-transcript.md）と隣接領域
- 「動画編集 × AI 自動化（Claude Code / video-use）」を扱う tutorial がここに供給される将来は十分あり得る

### 想定読者層

- iPad / Mac で「アプリで何かを作る」志向のクリエイター層
- インフルエンサー経由で集まっている層（amity_sensei 中心）
- AI 自動化への入り口として haru 動画が機能している可能性

## 不明点・未確認

- ビジネスモデル（完全無料 / フリーミアム / サブスク）
  - 「無料で見れる」セクションの存在から **フリーミアム** の可能性が高い
  - マイリスト・アカウントタブから推察するに会員機能あり
- 運営会社・法人情報
  - HTML / フッター未確認、SPA レンダリングのため要追加調査
- 動画本数の総数
  - JS コンソール上で `scrollToIndex 420 out of 0 to 9` のエラーが出ており、最大 420 件規模の FlatList を持っている可能性
- マネタイズ（クリエイターへの還元 / 広告 / 売上）

## 追加調査するなら

1. ページ最下部までスクロールして全カテゴリ・全動画一覧を取得
2. アカウント / 料金ページ（/account, /pricing 等）の有無を確認
3. 運営者情報（特商法表記）をフッターから取得
4. YouTube に同名チャンネル "Appfolio" / "appfolio_one" 等があるか確認
5. amity_sensei の他配信先（YouTube / Instagram）と照合してプラットフォーム選択の文脈把握

## 関連ファイル

- @docs/journal/2026-04-26.md — 同日観察の本体
- @docs/transcripts/maestri-youtube-masao-transcript.md — 同テーマ系（クリエイター × AI / ツール）
- @docs/transcripts/davinci-resolve-photo-editing-transcript.md — 動画編集ツール系
- @docs/transcripts/ndl-precedent-newspaper-genealogy-transcript.md — 別ジャンル（先祖調査）但し動画ナレッジ化の同枠
- @ai-minimalist-shibu/knowledge/shibu-ai-update.md — しぶ社内 Claude Code 研修文脈
