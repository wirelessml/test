# Apple Vision Pro 監視ルーチン

> 開始日: 2026-04-27
> 動機: 仲さんがミニマリストしぶに Vision Pro を推奨済み、しぶは 4/8 動画で実用を確認（テスラ車内 × Vision Pro = 動く仕事部屋）。Vision Air 中止 / Tim Cook 退任 / John Ternus CEO 9 月就任 など 2026-2028 にかけて Vision Pro エコシステムの重要転換期。仲さんの推奨責任 + Substack ネタ追跡として定常監視する。

## 対象 3 系統

### 1. Apple 本体・業界ニュース
- 公式: Apple Newsroom（visionOS / Vision Pro リリース）
- メディア: 9to5Mac, MacRumors, The Verge, Bloomberg
- アナリスト: Mark Gurman（Bloomberg）, Ming-Chi Kuo

### 2. しぶ自身の Vision Pro 活用
- Instagram: @minimalist_sibu（既存ルーチン instagram-watch.md と統合）
- YouTube: しぶ本人チャンネル + Yusuke Okawa（@yusukeokawa）等のコラボ動画
- Substack / blog: しぶ系の長文発信

### 3. 関連早期採用者・コラボレーター
- @yusukeokawa（4/8 ルームツアー動画作者、Vision Pro 議論）
- @kioku_sansaku（Yusuke の inspiration 元）
- @minimalist__jun（しぶ系派生、AI 触り始め）
- @nam.____t（カフェコーディング、ミニマリスト系）
- 勝間和代 @kazuyo_k は別ルーチン katsuma-watch.md（Vision Pro より voice stack 主軸）

## 監視タイミング

- **各 Claude Code セッション開始時**（9/14/19/0/5 時 JST、既存 instagram-watch ルーチンと併走）
- **重要トリガー**: Vision Pro 関連の新規発信があれば重点解析

## 取得コマンド例

### しぶ Instagram ストーリー
```bash
# 既存 chrome-devtools-mcp ログイン状態で
# instagram-watch.md ルーチンと統合
```

### Yusuke Okawa YouTube 新規動画
```bash
# yt-dlp で channel 一覧取得
~/yt-dlp --dump-single-json --flat-playlist \
  https://www.youtube.com/@YusukeOkawa | \
  python3 -c "import json,sys; d=json.load(sys.stdin); [print(e['title'], e['url']) for e in d['entries'][:10]]"
```

### Apple Vision Pro 関連ニュース
```bash
# WebSearch via Claude Code (現セッション内)
# キーワード: "Apple Vision Pro 2026" "Vision Air" "John Ternus" "visionOS"
```

### X 監視
```bash
# しぶ + 関連アカウント
twitter -c user-posts minimalist_sibu | grep -E "Vision|VR|ヘッドセット|空間"
twitter -c user-posts yusukeokawa | grep -E "Vision|VR|しぶ"
```

## キーワードフィルタ

**高優先**（即解析）:
- Vision Pro / VisionPro / ビジョンプロ / ビジョン
- Vision Air（中止確定だが復活ニュース要監視）
- visionOS / visionOS 27
- John Ternus
- Tim Cook 退任 / 後継
- Apple ヘッドセット / 空間コンピューティング
- AVP（Apple Vision Pro 略）
- 立体動画 / 没入

**中優先**（背景情報）:
- AR / VR / XR 一般
- Meta Quest（競合動向）
- visionOS アプリ（Claude Code on Vision、Final Cut Pro on Vision 等）
- Vision Pro の重量 / 不快感 / バッテリー

**低優先**（ライフスタイル系）:
- テスラ車中泊 + Vision Pro 系コンテンツ全般
- ミニマリスト × ガジェット投資

## 重要マイルストーン（カレンダー）

| 日付 | イベント | 出典 |
|---|---|---|
| **2026-04-25** | Vision Air 中止確定報道（9to5Mac） | https://9to5mac.com/2026/04/25/vision-pro-improvements-under-new-leadership-john-ternus/ |
| **2026-04-08** | しぶ × Yusuke Okawa「新居？究極のミニマリスト空間」公開（66K 再生） | https://youtu.be/ukfCg8ZgMjA |
| **2026-09**（推定） | John Ternus CEO 就任（Tim Cook 退任） | 9to5Mac 4/25 |
| **2026 後半**（推定） | visionOS 27 リリース | 9to5Mac 4/25 |
| **2028 以降**（推定） | Ternus 体制での Vision Pro 抜本改革 | 9to5Mac 4/25 |

## 観察ログ運用

### 重要発信を見つけたら以下に追記:

`docs/journal/YYYY-MM-DD.md` の **「Vision Pro 観察」**セクション

形式:
```markdown
### HH:MM Vision Pro 観察: <要点>

- 発信者: <誰>
- 媒体: <X / Instagram / YouTube / 9to5Mac 等>
- 内容: <要点>
- しぶ推奨責任への影響: 増 / 減 / 中立
- Substack ネタ価値: 高 / 中 / 低
```

## 過去の重要発信ログ

### 2026-04-08 しぶ × Yusuke Okawa「ルームツアー」（Vision Pro 実用確認）

YouTube `ukfCg8ZgMjA`、66,634 views / 1,264 likes、39:39。
Yusuke Okawa（@yusukeokawa）が しぶの新居（テスラ モデル Y 車内）を取材した動画。
22:21〜25:43 で Vision Pro 議論。

**しぶ本人の Vision Pro 関連発言**:
- 22:21 「ビジョンプロ来ました」
- 22:35 「これは本当に 10 年先...5 年先の人です」
- 22:43 「これで作業環境拡張できるから僕の動く仕事部屋」
- 22:54 「行った先々で景色に気を取られる時、これでこもって作業できる」
- 23:14 「これ使えば映画とかも本当プロジェクターはなくても」
- 23:18 「テスラのオーディオで大音響聞くともうマジで映画感」

**Yusuke Okawa の評**:
- 22:51 「し君...好きになりました（笑）」
- 23:36 「ミニマリストのまさにしぶ君だからできる技」
- 23:44 「テクノロジーの力でミニマリスト生活ができてる」

**しぶの居住完全構造**（動画と Yusuke 4/10 ツイートから判明）:
- 主住居: **テスラ モデル Y**（モデル 3 → Y へ乗換、車中泊しやすさ理由）
- 法的住所: **家賃 3 万円のミニマルアパート**（住民票用、1 ヶ月帰ってない）
- 作業環境: **Apple Vision Pro**（動く仕事部屋）
- 月総生活費: **6 万円**（家賃 3 + 諸費用 3）

→ **仲さんの Vision Pro 推奨は完全的中、しぶは推奨を哲学に統合済み**。

### 2026-04-10 02:28 Yusuke Okawa プロモツイート

> 一人暮らし、家賃3万、ミニマリスト
- 469 likes / 20 RTs
- 動画リンク + inspired by @kioku_sansaku 言及

### 2026-04-25 9to5Mac「Vision Air 中止 + Ternus 体制」

Michael Burkhardt（9to5Mac Weekend Editor）4/25 公開。

主要ポイント:
- Tim Cook 体制での「確信の欠如」が Vision Pro 不振の原因
- John Ternus は当初反対派、現在は楽観路線、9 月 CEO 就任予定
- **Vision Air（廉価軽量版）中止**
- visionOS 27 進行中だが本格改革は 2028 年以降
- ハード重量・ストリーミングアプリ未対応・タイピング/音声入力未熟が継続課題

仲さんの推奨責任への影響: **中立**（しぶは既に持ってて活用してる、Vision Air が出ても出なくても影響なし）

## TODO

- [ ] Yusuke Okawa の YouTube チャンネル新規動画自動チェック（cron / LaunchAgent）
- [ ] しぶの Substack 連載があれば購読、Vision Pro 関連投稿を待つ
- [ ] @kioku_sansaku アカウントのプロファイル調査（Yusuke の inspiration 元）
- [ ] 勝間 voice stack / Scribe との交差点（Vision Pro 上での音声入力）を Substack ネタ候補に
- [ ] Substack 記事「ミニマリストしぶの Vision Pro は『動く仕事部屋』だった」を 4/29 以降に書く（4/8 動画 + 4/25 9to5Mac の対比）
