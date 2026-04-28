# 勝間和代 voice stack 忠実再現 — MASU-P55 セットアップ

> Built: 2026-04-28 by Claude (SSH 経由、wirelessml/test リポジトリ運用下)
> Based on: 勝間和代 X 投稿 4/9〜4/28 + 4/28 オフィシャルメルマガ

## 構成

| バージョン | 構成 | 起源 |
|---|---|---|
| **V1 旧構成** | Whisper Large Turbo (Groq API) + Llama 70B 後処理 + Python トリム | 4/9〜4/18 確立 |
| **V2 新構成** | ElevenLabs Scribe + Python トリム (LLM 不要) | 4/27 朝 1,168L マニフェスト |
| **V3 比較ベンチ (歴史的価値のみ)** | GPT 120B vs Llama 70B 後処理 | 4/27 23:19 勝間予告 |
| **🎯 V4 確定構成 (採用)** | **ElevenLabs Scribe + Python トリム + 漢数字補正のみ ローカル正規表現 or Groq Llama 8B** | 4/28 13:21〜20:30 結論 + 4/29 ローカル化 |

> ⚠️ **V3 アップデート (4/28 10:15)**: 勝間本人が同日朝に **Scribe 単体 vs Whisper+GPT120B 後処理** を実機検証 → **Scribe 単体圧勝** と結論 (ID 2048933979420790843, 79L)。理由: (1) 前後文脈の精度差、(2) LLM が直しきれない元 Whisper の限界、(3) **Scribe ハルシネーションゼロ**。
>
> ✅ **V4 確定 (4/28 13:21〜20:30)**: 勝間さんは「Scribe pure stack」に LLM 後処理を残す唯一の用途として **「漢数字 → 算用数字」補正** のみを認定。「Scribeの最大の欠点の一つが、過剰な正規化で数字を全部漢数字に直したがる」(ID 2048944369282191711, 20L) → 「そこだけLLMで直してます」(ID 2049116752504820147, 13L) → 「軽いLLMのプロンプト」(ID 2049016868237918681, 6L)。
>
> 🎯 **V4 ローカル化 (4/29 06:50)**: 漢数字 → 算用数字 は決定的変換なので LLM 不要と判断、`scribe_kanjisuji_local.py` 新規実装（正規表現ベース、慣用句自動回避、8/8 ユニットテスト合格）。Groq アカウント新規作成不要、ネットワーク不要、レイテンシゼロ。Groq Llama 8B 版 `scribe_kanjisuji_fix.py` も保持（精度に不満時のフォールバック用）。
>
> このリポジトリの `gpt120b_vs_llama70b.py` は本来用途を喪失したが、再現性の記録として保持。`groq_postprocess.py` は V1 完全 LLM クレンジング用、V4 では使わない。

## ファイル一覧

```
voice-stack/
├── scripts/
│   ├── trim_clipboard.py      # 4/15 勝間原型: 半角スペース除去 + 自動ペースト
│   ├── scribe_api.py          # V2/V4: ElevenLabs Scribe 直叩き
│   ├── scribe_kanjisuji_fix.py # V4 Groq 版: 漢数字 → 算用数字 (Llama 8B、要 GROQ_API_KEY)
│   ├── scribe_kanjisuji_local.py # 🎯 V4 ローカル版: 漢数字 → 算用数字 (LLM 不要、正規表現)
│   ├── groq_whisper.py        # V1: Groq Whisper (GPU 不要)
│   ├── groq_postprocess.py    # V1: Llama 70B 全文後処理 (V4 では非推奨)
│   ├── gpt120b_vs_llama70b.py # V3: 後処理 LLM 比較 (歴史的記録)
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

# 4. V3 後処理 LLM 比較 (歴史的価値のみ、V4 では不要)
echo "えーと、これは音声入力のテストです句読点ないですけどお願いします" | python scripts\gpt120b_vs_llama70b.py

# 5. クリップボード自動トリム常駐
python scripts\trim_clipboard.py

# 🎯 V4 確定運用 (ローカル版、Groq 不要): Scribe 録音 → 漢数字補正 → クリップボード返却
python scripts\scribe_api.py --record 10 | python scripts\scribe_kanjisuji_local.py
# または既にクリップボードに Scribe 結果があれば
python scripts\scribe_kanjisuji_local.py --clipboard

# Groq Llama 8B 版（精度に不満出たらフォールバック、要 GROQ_API_KEY）
python scripts\scribe_kanjisuji_fix.py --clipboard
```

## 編集方針との整合（観察哲学）

- このセットアップは「**勝間スタックの 80% を Windows で再現**」する試み
- 残る 20% = 親指シフト習熟（数ヶ月）+ マウスコンピューター物理 + 自己破壊速度（性格）
- 仲さんの記事方針: **「真似できなさ」を実装で言語化** する素材として活用

## 関連
- 観察ログ: `~/Desktop/docs/routines/katsuma-watch.md`
- Substack 連載: 「勝間定点観察」候補 5 本（katsuma-watch 末尾参照）

