# 勝間和代 voice stack 忠実再現 — MASU-P55 セットアップ

> Built: 2026-04-28 by Claude (SSH 経由、wirelessml/test リポジトリ運用下)
> Based on: 勝間和代 X 投稿 4/9〜4/28 + 4/28 オフィシャルメルマガ

## 構成

| バージョン | 構成 | 起源 |
|---|---|---|
| **V1 旧構成** | Whisper Large Turbo (Groq API) + Llama 70B 後処理 + Python トリム | 4/9〜4/18 確立 |
| **V2 新構成 (現行マニフェスト)** | **ElevenLabs Scribe** + Python トリム (LLM 不要) | 4/27 朝 1,168L マニフェスト |
| **V3 比較中** | GPT 120B vs Llama 70B 後処理ベンチ | 4/27 23:19 勝間予告 |

## ファイル一覧

```
voice-stack/
├── scripts/
│   ├── trim_clipboard.py      # 4/15 勝間原型: 半角スペース除去 + 自動ペースト
│   ├── scribe_api.py          # V2: ElevenLabs Scribe 直叩き
│   ├── groq_whisper.py        # V1: Groq Whisper (GPU 不要)
│   ├── groq_postprocess.py    # V1: Llama 70B 後処理
│   ├── gpt120b_vs_llama70b.py # V3: 後処理 LLM 比較
│   └── keybind_voice.py       # 無変換キー = Groq 録音→転写→ペースト
├── config/                    # YamabukiR 親指シフト設定など
├── downloads/                 # SuperWhisper / Google IME / YamabukiR インストーラー
├── samples/                   # テスト用 WAV
├── logs/                      # 実行ログ
├── .env.example
├── README.md
└── physical_setup.md          # 物理着席日にやること
```

## クイックスタート（API キー設定後）

```powershell
# 1. 環境変数設定
$env:ELEVENLABS_API_KEY = "sk_..."
$env:GROQ_API_KEY = "gsk_..."

# 2. 動作確認
python scripts\scribe_api.py --check
python scripts\groq_whisper.py --check
python scripts\groq_postprocess.py --check

# 3. V2 Scribe で 10 秒録音→転写
python scripts\scribe_api.py --record 10

# 4. V3 後処理 LLM 比較
echo "えーと、これは音声入力のテストです句読点ないですけどお願いします" | python scripts\gpt120b_vs_llama70b.py

# 5. クリップボード自動トリム常駐
python scripts\trim_clipboard.py
```

## 編集方針との整合（観察哲学）

- このセットアップは「**勝間スタックの 80% を Windows で再現**」する試み
- 残る 20% = 親指シフト習熟（数ヶ月）+ マウスコンピューター物理 + 自己破壊速度（性格）
- 仲さんの記事方針: **「真似できなさ」を実装で言語化** する素材として活用

## 関連
- 観察ログ: `~/Desktop/docs/routines/katsuma-watch.md`
- Substack 連載: 「勝間定点観察」候補 5 本（katsuma-watch 末尾参照）

