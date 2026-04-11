# RVC 声クローン マニュアル（Mac M1対応）

## 概要

RVC（Retrieval-based Voice Conversion）を使い、YouTube動画等の音声からターゲットの声モデルを学習し、任意のテキストをその声で読み上げる。

## 環境

- MacBook Air M1 8GB（macOS 26.5.0）
- Python 3.10（Homebrew）
- PyTorch 2.11.0（MPS対応）
- RVC-WebUI-MacOS: /tmp/RVC-WebUI-MacOS/

## セットアップ手順

### 1. Python 3.10 インストール

```bash
brew install python@3.10
```

### 2. RVC-WebUI-MacOS クローン

```bash
cd /tmp
git clone https://github.com/qingbo1011/RVC-WebUI-MacOS.git
cd RVC-WebUI-MacOS
```

### 3. venv作成 + PyTorch

```bash
python3.10 -m venv .venv
.venv/bin/pip install torch torchvision torchaudio
```

### 4. requirements.txt（バージョン制約を外す）

```bash
# バージョン固定を外してインストール
cat requirements.txt | sed 's/==.*//g' | grep -v "^#" | grep -v "^$" | grep -v "aria2" | grep -v fairseq > /tmp/rvc-pkgs.txt
.venv/bin/pip install $(cat /tmp/rvc-pkgs.txt | tr '\n' ' ')

# fairseqは別途（ビルドが必要）
.venv/bin/pip install fairseq
```

### 5. 依存関係の手動修正（重要）

```bash
# gradio + gradio_client（バージョンペアが重要）
.venv/bin/pip install "gradio==3.36.1" "gradio_client==0.2.7"

# omegaconf（pip 24.0以下でないとインストールできない）
.venv/bin/pip install "pip<24.1"
.venv/bin/pip install --no-deps "omegaconf==2.0.6"
.venv/bin/pip install "hydra-core==1.0.7"

# fastapi + starlette
.venv/bin/pip install "fastapi==0.99.1" "starlette==0.27.0"

# numba + numpy + llvmlite
.venv/bin/pip install --force-reinstall "numba==0.58.1" "numpy==1.24.4" "llvmlite==0.41.1"

# その他不足パッケージ
.venv/bin/pip install cffi soundfile future regex sacrebleu decorator audioread \
  pooch soxr lazy_loader msgpack platformdirs antlr4-python3-runtime==4.9.3 \
  pyparsing matplotlib aiohttp aiofiles pydantic uvicorn httpx orjson pydub \
  coloredlogs flatbuffers threadpoolctl "jinja2==3.1.2"
```

### 6. hubertモデルのダウンロード

```bash
mkdir -p assets/hubert
curl -L -o assets/hubert/hubert_base.pt \
  "https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/hubert_base.pt"
```

### 7. 事前学習モデルのダウンロード

```bash
mkdir -p assets/pretrained_v2
curl -L -o assets/pretrained_v2/f0G40k.pth \
  "https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/pretrained_v2/f0G40k.pth"
curl -L -o assets/pretrained_v2/f0D40k.pth \
  "https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/pretrained_v2/f0D40k.pth"
```

### 8. コード修正（PyTorch 2.6+対応）

#### extract_feature_print.py の先頭に追加：
```python
import torch
_original_load = torch.load
def _patched_load(*args, **kwargs):
    if 'weights_only' not in kwargs:
        kwargs['weights_only'] = False
    return _original_load(*args, **kwargs)
torch.load = _patched_load
```

#### infer/lib/train/utils.py の tostring_rgb 修正：
```python
# 修正前
data = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep="")
data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))

# 修正後
data = np.asarray(fig.canvas.buffer_rgba())[:, :, :3]
```

## 学習データの準備

### YouTube動画から音声を抽出

```bash
# yt-dlpで音声ダウンロード
yt-dlp -f "bestaudio" --extract-audio --audio-format mp3 -o "full-audio.mp3" "https://www.youtube.com/watch?v=VIDEO_ID"

# 10分間の学習用データを切り出し（クリーンな発話部分）
ffmpeg -ss 00:03:40 -i full-audio.mp3 -t 600 -ar 44100 -ac 1 datasets/TARGET/train.wav
```

### ポイント
- 学習データは**1人の声だけ**が入っている部分を選ぶ
- BGMや効果音が少ない部分が望ましい
- 10分程度で十分（3-5分でも動く）
- サンプリングレート44100Hz、モノラル

## WebUIの起動

```bash
cd /tmp/RVC-WebUI-MacOS
export PYTORCH_ENABLE_MPS_FALLBACK=1
export PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0
export KMP_DUPLICATE_LIB_OK=TRUE
export OMP_NUM_THREADS=1
.venv/bin/python infer-web.py
```

ブラウザで `http://127.0.0.1:7865` にアクセス。

## 学習手順（WebUI）

### Step 1: 基本設定
- 输入实验名: `shibu`（任意の名前）
- 目标采样率: `40k`
- 音高ガイド: `true`（歌声の場合）/ `false`（話し声の場合）
- 版本: `v2`

### Step 2a: データ処理
- 输入训练文件夹路径: `/tmp/RVC-WebUI-MacOS/datasets/shibu`
- **「处理数据」** クリック → `end preprocess` を待つ

### Step 2b: 特徴抽出
- **「特征提取」** クリック → `all-feature-done` を待つ
- M1で5-10分かかる

### Step 3: 学習
- total_epoch: `20`（話し声なら20で十分）
- batch_size: `1`（M1 8GBの場合）
- **「训练模型」** クリック
- M1で20エポック = 30分〜1時間

### 完了後
- モデルファイル: `logs/shibu/` 配下に `.pth` ファイル
- weightsフォルダ: `assets/weights/` に最終モデル

## 推論（声変換）

### WebUIで推論
1. 「模型推理」タブに移動
2. 「选择音色」でshibuモデルを選択
3. 音声ファイルをアップロード or マイク入力
4. 「转换」で変換実行

### CLIで推論
```bash
cd /tmp/RVC-WebUI-MacOS
.venv/bin/python infer/modules/vc/modules.py \
  --model logs/shibu/shibu.pth \
  --input input.wav \
  --output output.wav
```

## トラブルシューティング

| 問題 | 解決策 |
|------|--------|
| `weights_only` エラー | extract_feature_print.py にパッチ追加 |
| `tostring_rgb` エラー | utils.py の matplotlib修正 |
| `omegaconf` インストール不可 | pip < 24.1 にダウングレード |
| `gradio_client.serializing` エラー | gradio==3.36.1 + gradio_client==0.2.7 |
| `2a_f0 not found` | 音高ガイドをfalseに、またはf0ダミーファイル作成 |
| `localhost not accessible` | share=True に変更 |
| numba SystemError | numba==0.58.1 + numpy==1.24.4 + llvmlite==0.41.1 |

## 代替ツール（試行済み）

| ツール | 品質 | M1対応 | 備考 |
|--------|------|--------|------|
| **RVC** | 最高 | MPS対応 | セットアップが複雑 |
| Spark TTS | 低 | MLX対応 | 声クローン精度低い |
| Qwen3-TTS | 中 | MLX対応 | HuggingFaceログイン必要 |
| ElevenLabs | 最高 | クラウド | 声クローンは月$5 |
| VoxCPM2 | 最高 | 非対応 | NVIDIA GPU必須 |
| Kokoro TTS | - | MLX対応 | 依存関係問題で断念 |

## ファイル構成

```
/tmp/RVC-WebUI-MacOS/
├── .venv/                    ← Python 3.10 venv
├── assets/
│   ├── hubert/hubert_base.pt ← 特徴抽出モデル (180MB)
│   └── pretrained_v2/        ← 事前学習モデル (206MB)
├── datasets/shibu/            ← 学習データ
├── logs/shibu/                ← 学習ログ・中間ファイル
├── infer-web.py              ← WebUIメイン
└── infer/modules/train/       ← 学習スクリプト
```
