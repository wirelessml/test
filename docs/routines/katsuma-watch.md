# 勝間和代 X 監視ルーチン

> 開始日: 2026-04-27
> 動機: 4/27 早朝の voice stack 4 連投で「Scribe 採用 + ノイズ耐性」を発信、仲さんの voice stack 比較記事ネタに直結。今後も同種の高密度な技術発信が続く可能性が高いため、定常監視する。

## 対象アカウント

- **@kazuyo_k**（勝間和代、認証済み）
- 投稿頻度: 1 日数十件、技術系 / 家電 / ライフハック / 政治 / ツーリング多岐
- 直近フォロワー数: 未確認

## 監視タイミング

- **各 Claude Code セッション開始時**（9/14/19/0/5 時 JST）
- 重要トリガー: voice/AI/マシン関連のキーワードを含む新規投稿があれば**重点解析**

## 取得コマンド

```bash
# agent-reach の twitter CLI 経由（Cookie 取得済み、@minimalistneko 認証）
twitter -c user-posts kazuyo_k > /tmp/kazuyo_k-latest.json

# 前回比 diff
diff /tmp/kazuyo_k-prev.json /tmp/kazuyo_k-latest.json | grep '"text"'

# 重要キーワードフィルタ
twitter -c user-posts kazuyo_k | python3 -c "
import json, sys, re
posts = json.loads(sys.stdin.read())
high = re.compile(r'Whisper|Scribe|SuperWhisper|音声入力|LLM|Gemma|Claude|Codex|Gemini|VRAM|GPU|NPU|ゲーミングノート|AC アダプター')
for p in posts:
    if high.search(p['text']):
        print(f\"[{p['time']}] ({p['likes']} likes) {p['text'][:100]}\")
"
```

## キーワードフィルタ（優先度別）

**高優先**（音声入力 / LLM 周辺、即解析）:
- Whisper / Scribe / SuperWhisper / Aqua Voice / Typeless
- 音声入力 / 音声認識 / 文字起こし / Transcribe
- LLM / Gemma / Claude / Gemini / GPT / Codex
- AI / API
- ノイズ / 騒音 / カフェ / スタバ / サンマルク（音声入力環境関連）

**中優先**（マシン / ハード）:
- ゲーミングノート / ノート PC / MacBook
- AC アダプター / PD / 電源 / 純正
- VRAM / GPU / NPU / メモリ
- Pixel / Android / iPhone（音声入力との関連で）

**低優先**（ライフスタイル、Substack ネタには弱い）:
- 家電 / コストコ / スタバ系（飲食）
- ツーリング / 自転車

## 観察ログ運用

### 重要発信を見つけたら以下に追記:

`docs/journal/YYYY-MM-DD.md` の **「勝間 X 観察」**セクション

形式:
```markdown
### HH:MM 勝間 @kazuyo_k 投稿: <要点>

> （引用、800 字まで）

**観察**:
- <仲さんの voice stack 比較記事への影響>
- <時系列での思考プロセス>
- <他の発信者との接続>

**Substack ネタ価値**: 高 / 中 / 低
```

### Substack ネタとして温める場合:

`docs/substack-ideas/katsuma-<topic>.md` に下書き

## 過去の重要発信ログ

### 2026-04-19 公開 安野貴博との 51 分対談

YouTube `wX6vePiwEGw`、20 万再生。25:49〜32:37 が音声入力章。

- Whisper クラウド + Gemma 12B ローカル整形
- SuperWhisper 買い切り採用
- 執筆 4,000 字／日のための環境
- 「F1 レーサー的キワキワチューニング」（安野評）

### 2026-04-23 23:50 ゲーミングノート電源

> ゲーミングノートで持ち歩く電源も、結局 PD の 100W を止めて、純正の 210W の AC アダプターにしたら、パフォーマンスモードでも電池を心配せずに気持ちよく動かせる

- 仲さんと同種マシン（Win ゲーミングノート）使用確認
- パフォーマンスモード重視、PD では不足

### 2026-04-26 07:05 AI と思考整理

> AI との対話でジレンマを整理する。ここ数年で物事を考えるのがとても楽になりました

- AI を「思考補助」として使う哲学（出力ではなく整理）

### 2026-04-27 00:11〜03:27 voice stack 4 連投

詳細: @docs/journal/2026-04-27.md

- **00:11** スタバでは音声入力目立つ問題提起（90 likes）
- **02:46** Scribe 単体で十分、LLM 不要（32 likes）
- **02:50** SuperWhisper モデル選択で Scribe（11 likes）
- **03:27** Scribe ノイズ耐性、Android 自作検討（1 likes）

### 2026-04-27 当日告知

- **10:10-10:25 J-Wave STEPONE 生出演**（4/26 23:52 告知、17 likes）

## TODO

- [ ] J-Wave STEPONE（4/27 10:10-10:25）を radiko で確認、voice stack 発言があるか
- [ ] 30 分後（〜10:00 JST）に再 fetch、03:27 続編がないか確認
- [ ] cron / LaunchAgent でセッション開始時自動 fetch する仕組み化（後日）
- [ ] Substack 記事「勝間 voice stack の 100 時間進化」候補（4/19 → 4/27 の変化）
