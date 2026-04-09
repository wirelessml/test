# 動画編集ワークフロー マニュアル

## 概要

YouTube動画から特定の場面を抽出し、宣伝パートを合成して1本の動画にまとめる手順。
2026/4/9に実施した「しぶ自己語りダイジェスト」の制作過程を元に作成。

## 必要環境

```bash
# ffmpeg（ARM64静的バイナリ、Homebrewなしで導入）
~/local/bin/ffmpeg

# yt-dlp（deno版、JSチャレンジ対応）
~/yt-dlp
# PATH に ~/.deno/bin を含める

# Python 3 + pydub
pip3 install --user pydub
```

## 全体フロー

```
1. 字幕取得 → 2. 場面特定 → 3. 動画ダウンロード → 4. 場面切り出し
→ 5. 宣伝パート取得 → 6. 合成 → 7. Web圧縮 → 8. HTML公開
```

---

## Step 1: YouTube字幕取得

```bash
PATH="$HOME/.deno/bin:$PATH" ~/yt-dlp \
  --write-auto-sub --sub-lang ja --sub-format srt \
  --skip-download \
  -o "保存先/yt-VIDEO_ID" \
  "https://www.youtube.com/watch?v=VIDEO_ID"
```

- 自動字幕（音声認識）が取得される
- 誤変換が多いので文脈から補正が必要
- 出力: `.ja.srt` ファイル（SRT形式）

## Step 2: 場面の特定

### キーワード検索

```bash
# Grepツールで関連キーワードを検索
grep -n "キーワード1|キーワード2" yt-VIDEO_ID.ja.srt
```

### タイムスタンプの記録

SRTファイルの時間表記から、各場面の開始・終了時刻を記録:

```
場面1: 15:42 〜 17:35 （タイトル）
場面2: 20:53 〜 22:10 （タイトル）
...
```

**注意**: 自動字幕のタイムスタンプは数秒ずれることがある。少し余裕を持たせる。

## Step 3: 動画ダウンロード

```bash
# 720pでダウンロード（容量と画質のバランス）
PATH="$HOME/.deno/bin:$PATH" ~/yt-dlp \
  -f "bestvideo[height<=720]+bestaudio/best[height<=720]" \
  -o "/tmp/yt-VIDEO_ID.%(ext)s" \
  "https://www.youtube.com/watch?v=VIDEO_ID"
```

### 音声コーデックの注意

- YouTube動画はOpus音声のwebmで配信されることが多い
- Opusはffmpegのシーク（`-ss`）と相性が悪く音声欠落の原因になる
- **対策**: h264+AACフォーマットを明示指定:

```bash
# 音声の確実な取得が必要な場合
~/yt-dlp \
  -f "bestvideo[height<=720][vcodec^=avc]+bestaudio[acodec^=mp4a]/best[height<=720]" \
  ...
```

## Step 4: 場面の切り出しと連結

### Pythonスクリプト方式（推奨）

```python
SEGMENTS = [
    ("15:42", "17:35", "タイトル1"),
    ("20:53", "22:10", "タイトル2"),
    # ...
]
```

各セグメントをmpegts形式で個別書き出し → concatで連結:

```bash
# 個別セグメント書き出し
ffmpeg -y -ss START -to END -i input.webm \
  -c:v libx264 -preset fast -crf 23 \
  -c:a aac -b:a 128k \
  -f mpegts segment_01.ts

# 連結
echo "file 'segment_01.ts'" > files.txt
echo "file 'segment_02.ts'" >> files.txt
ffmpeg -y -f concat -safe 0 -i files.txt \
  -c:v libx264 -preset fast -crf 23 \
  -c:a aac -b:a 128k \
  output.mp4
```

### jetcut.py（自動ジェットカット）

無音部分を自動カットする場合:

```bash
python3 ai-minimalist-shibu/src/jetcut.py input.mp4 \
  --silence-thresh -35 \  # 無音判定閾値（dB）
  --min-silence 0.4 \     # 最小無音長（秒）
  --padding 0.1            # カット前後の余白（秒）
```

## Step 5: 使い回し宣伝パートの取得

しぶチャンネルの片付け動画は冒頭と末尾に定型の宣伝がある。

### 宣伝パートの構造（2026年4月時点）

**冒頭（約1分）**:
- 「お知らせがあります」
- 公式LINE宣伝 + 13個の無料特典紹介
- 「概要欄からお願いします。動画本編にどうぞ」

**末尾（約1分）**:
- コーチング募集案内（全国無料、不定期）
- チャンネル登録 + SNSフォロー依頼
- 公式LINE再告知 + QRコード案内

### 取得方法

```bash
# 冒頭宣伝（元動画の4:08〜5:15あたり）
~/yt-dlp -f "bestvideo[height<=720][vcodec^=avc]+bestaudio[acodec^=mp4a]..." \
  --download-sections "*4:08-5:15" \
  -o "/tmp/intro.%(ext)s" "URL"

# 末尾宣伝（元動画の最後1分）
~/yt-dlp -f "bestvideo[height<=720][vcodec^=avc]+bestaudio[acodec^=mp4a]..." \
  --download-sections "*4:23:40-4:24:42" \
  -o "/tmp/outro.%(ext)s" "URL"
```

**重要**: 必ず `vcodec^=avc` + `acodec^=mp4a` を指定。Opus音声だとシーク時に音声が欠落する。

### 宣伝パートの特定方法

1. フル字幕を取得
2. 以下のキーワードで検索:
   - 冒頭: `公式LINE`, `概要欄`, `プレゼント`, `動画本編にどうぞ`
   - 末尾: `チャンネル登録`, `コーチング`, `概要欄`, `QRコード`
3. 前後数秒の余裕を持ってタイムスタンプを決定

## Step 6: 合成（イントロ + 本編 + アウトロ）

```bash
FFMPEG=~/local/bin/ffmpeg
TMPDIR=$(mktemp -d)

# 各パーツをmpegts形式に変換
$FFMPEG -y -i intro.mp4 -c:v libx264 -preset fast -crf 23 \
  -c:a aac -b:a 128k -ar 44100 -f mpegts "$TMPDIR/intro.ts"

$FFMPEG -y -i main.mp4 -c:v libx264 -preset fast -crf 23 \
  -c:a aac -b:a 128k -ar 44100 -f mpegts "$TMPDIR/main.ts"

$FFMPEG -y -i outro.mp4 -c:v libx264 -preset fast -crf 23 \
  -c:a aac -b:a 128k -ar 44100 -f mpegts "$TMPDIR/outro.ts"

# 連結
cat > "$TMPDIR/files.txt" << EOF
file '$TMPDIR/intro.ts'
file '$TMPDIR/main.ts'
file '$TMPDIR/outro.ts'
EOF

$FFMPEG -y -f concat -safe 0 -i "$TMPDIR/files.txt" \
  -c:v libx264 -preset fast -crf 23 -c:a aac -b:a 128k \
  output_complete.mp4
```

### 注意点

- `-ar 44100` を全パーツで統一（サンプルレートの不一致で音ズレ防止）
- mpegts形式を中間フォーマットに使う（mp4のconcatより安定）
- 解像度が異なるソースを混ぜる場合は `-vf "scale=1280:720"` を追加

## Step 7: Web用圧縮

GitHub Pagesの100MBファイル制限に対応:

```bash
$FFMPEG -y -i output_complete.mp4 \
  -c:v libx264 -preset slow -crf 28 \
  -vf "scale=640:-2" \
  -c:a aac -b:a 96k \
  output_web.mp4
```

| パラメータ | 値 | 説明 |
|-----------|-----|------|
| preset | slow | 圧縮効率優先（エンコード時間は増加） |
| crf | 28 | 品質（数値が大きいほど小さいが劣化、23がデフォルト） |
| scale | 640:-2 | 横640px（アスペクト比維持、偶数保証） |
| audio | 96k | 音声ビットレート（視聴には十分） |

目安: 23分の動画 → 116MB（フル品質）→ 38MB（Web版）

## Step 8: チャプター付きHTMLプレーヤー

```javascript
// チャプター定義
const chapters = [
  { time: 0,    title: "冒頭宣伝" },
  { time: 67,   title: "場面1" },
  // ...
];

// シーク関数
function seekTo(seconds) {
  document.getElementById('player').currentTime = seconds;
  document.getElementById('player').play();
}

// 再生中チャプターのハイライト
player.addEventListener('timeupdate', () => {
  // 現在時刻に対応するチャプターをactive表示
});
```

公開: `git add` → `git push` → GitHub Pages

---

## トラブルシューティング

### 音声が欠落する
- **原因**: Opus音声のwebmファイルでffmpegシーク（`-ss`）が失敗
- **対策**: yt-dlpで `vcodec^=avc` + `acodec^=mp4a` を指定してh264+AAC形式で取得

### concatで映像が乱れる
- **原因**: 異なるコーデック・解像度・FPSのファイルを直接連結
- **対策**: 全ファイルを同一設定でmpegts形式にエンコードしてからconcat

### ffmpegがCPUアーキテクチャエラー
- **原因**: Intel版バイナリをApple Silicon Macで実行
- **対策**: ARM64版を取得（`file ffmpeg` で `arm64` を確認）

### yt-dlpでIP制限エラー
- **原因**: YouTubeのbot検出
- **対策**: deno版yt-dlpを使用（JSチャレンジ自動解決）

### GitHubにpushできない（100MB制限）
- **対策**: Web版（640p, CRF 28）に圧縮して100MB以下にする

---

## 制作実績

### しぶ自己語りダイジェスト（2026/4/9）

| 項目 | 値 |
|------|-----|
| 元動画 | 1時間12分（2oySXA967II） |
| 宣伝パート元 | 4時間24分（Q3QCsNfmiM0、最新片付け動画） |
| 完成動画 | 23:51 |
| 場面数 | 9場面 + 冒頭宣伝 + 末尾宣伝 |
| フル品質 | 116MB（720p） |
| Web版 | 38MB（640p） |
| 公開URL | ai-minimalist-shibu/shibu-self-talk.html |
