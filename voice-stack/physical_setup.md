# MASU-P55 物理着席日にやる作業

> SSH では完結できない、物理キーボード + GUI 操作が必要な手順を集約。

## チェックリスト（推奨実施順）

### 0. 事前確認（SSH 構築済み事項、4/28 09:48 〜 4/29 06:24 完了）

| 項目 | 状態 |
|---|---|
| Python 3.12.10 | ✅ インストール済 (4/28) |
| pip 主要 SDK | ✅ groq 1.0.0 / elevenlabs 2.42.0 / anthropic 0.76.0 / google-genai 1.65.0 / openai 2.16.0 / browser-use 0.12.2 |
| pyperclip 1.11.0 / keyboard 0.13.5 / sounddevice 0.5.5 / numpy 2.4.4 | ✅ 4/28 セッションで追加 |
| `~/voice-stack/scripts/` **8 スクリプト** | ✅ 配置済（4/29 06:23 `scribe_kanjisuji_fix.py` 追加） |
| `~/voice-stack/downloads/GoogleJapaneseInputSetup.exe` (11.5MB) | ✅ 4/29 06:22 SSH 経由 DL 完了 |
| マイクデバイス | ✅ 20 個検出、デフォルト = `マイク配列 (Intel SST)` ch=2 sr=44100 |
| `chcp 65001` (UTF-8) 設定 | ⚠️ ターミナルごとに必要、永続化推奨 |

#### 🎯 V4 確定構成（4/28 13:21〜20:30 勝間結論）

「Scribe pure stack + 漢数字補正のみ Groq Llama 8B」が現時点の正解。`scribe_kanjisuji_fix.py` がその専用スクリプト。詳細は @README.md V4 セクション。

### 1. SuperWhisper Windows 版インストール（v1.3.9 確認、x64 / ARM64）

> 4/29 06:20 SSH DL 試行: superwhisper.com の DL は JS で動的生成 + Vercel 経由のため、curl/Invoke-WebRequest では実行ファイル URL が取得不可。**着席時に GUI ブラウザで手動 DL 必須**。

- [ ] ブラウザで https://superwhisper.com/download を開く
- [ ] 「Download for Windows」ボタン → **x64** を選択（HP ProBook は x64）
- [ ] `C:\Users\gci_admin\voice-stack\downloads\` に保存
- [ ] インストール実行
- [ ] 起動後、設定で **Scribe (実験モデル)** をオンにする
- [ ] ホットキー設定: **左 Alt** に割り当て（勝間 4/11 ツイート準拠）
- [ ] **自動ペースト OFF**（重要、Python トリム → ペーストの順番を変えるため）
- [ ] 設定 → 言語 → **日本語** 固定
- [ ] ElevenLabs API キー貼付け
- [ ] 🎯 V4 確定構成のため: SuperWhisper 内で **Scribe を選択**、Whisper モデルは無効化推奨

### 2. Google 日本語入力インストール

- [x] ✅ **4/29 06:22 SSH DL 完了**: `C:\Users\gci_admin\voice-stack\downloads\GoogleJapaneseInputSetup.exe` (11.5MB)
  - 入手元: `https://dl.google.com/japanese-ime/GoogleJapaneseInputSetup.exe`（直リンク確認済）
- [ ] エクスプローラから `GoogleJapaneseInputSetup.exe` をダブルクリックでインストール
- [ ] インストール → デフォルト IME に設定
- [ ] 設定で **MS-IME 互換** を一旦選択（YamabukiR と相性が良い）

### 3. YamabukiR (親指シフトエミュレータ) インストール

> 勝間さんと同じ構成 (4/16 19:04 ツイート、4/28 02:24 「YamabukiRです。Google日本語入力で十分に親指シフトになります」再確認)

> 4/29 06:21 SSH DL 試行: atwiki.jp が Cloudflare チャレンジで JS 認証必須、SSH 経由 DL 不可。**着席時に GUI ブラウザで手動 DL 必須**。

- [ ] ブラウザで https://atwiki.jp/yamabuki/pages/15.html を開く（CF チャレンジを通す）
- [ ] 最新版 `yamabuki_r_xxx.zip` を DL → `C:\Users\gci_admin\voice-stack\downloads\` に保存
- [ ] 適当なディレクトリに展開（例: `C:\Tools\YamabukiR\`）
- [ ] `YamabukiR.exe` を管理者権限で実行
- [ ] 親指シフト (NICOLA) 配列定義ファイルを読み込み
- [ ] スタートアップに登録（自動起動）
- [ ] **テスト**: 「いう」を SK + DJ で打って正しく入力されるか確認
  - S+K = い (右親指 + S)
  - D+J = う (左親指 + J)

### 4. 環境変数永続設定

> 4/29 06:24 SSH 確認: `ELEVENLABS_API_KEY` / `GROQ_API_KEY` / `GEMINI_API_KEY` すべて未設定。サインアップが必要。

#### 4-1. ブラウザでサインアップ + キー取得（着席必須）

| サービス | サインアップ URL | 取得画面 | 無料枠 |
|---|---|---|---|
| ElevenLabs | https://elevenlabs.io/sign-up | https://elevenlabs.io/app/settings/api-keys | Free 10k credits/月、Scribe 利用可（Starter $5 で 30k credits） |
| Groq | https://console.groq.com/login | https://console.groq.com/keys | Free 14.4k req/日、Llama 3.1 8B Instant 制限緩い |
| Gemini (任意) | https://aistudio.google.com/ | https://aistudio.google.com/app/apikey | Free 1.5k req/日、コーディング支援用途 |

#### 4-2. ヘルパースクリプトで一括設定

```powershell
# 4/29 06:26 SSH 配置済の対話型スクリプトを実行
powershell -ExecutionPolicy Bypass -File C:\Users\gci_admin\voice-stack\scripts\setup_api_keys.ps1
```

各キーをコピペで入力、永続化（HKCU\Environment）まで自動。

#### 4-3. 新しいターミナルで反映確認

```powershell
echo $env:ELEVENLABS_API_KEY  # sk_... が表示されれば OK
echo $env:GROQ_API_KEY        # gsk_... が表示されれば OK
python C:\Users\gci_admin\voice-stack\scripts\scribe_api.py --check
python C:\Users\gci_admin\voice-stack\scripts\scribe_kanjisuji_fix.py --check
```

### 5. キーバインド常駐起動

```powershell
# 無変換キーで Groq 録音
python C:\Users\gci_admin\voice-stack\scripts\keybind_voice.py
```

別ターミナルで:
```powershell
# クリップボード自動トリム
python C:\Users\gci_admin\voice-stack\scripts\trim_clipboard.py
```

両方を Windows のスタートアップに登録すれば自動起動。

### 6. End-to-End 動作確認

| シナリオ | 期待動作 |
|---|---|
| **A. 親指シフトで日本語入力** | YamabukiR + Google 日本語入力で「こんにちは」を NICOLA 配列で打って表示 |
| **B. SuperWhisper + Scribe (V2/V4)** | 左 Alt 押下中に「テスト録音です」と発話 → 離す → 自動転写 → クリップボード → trim_clipboard.py が自動ペースト |
| **C. 無変換キー Groq** | 無変換押下中に発話 → 離す → Groq Whisper で転写 → ペースト |
| **D. V3 比較** | テキスト入力 → GPT 120B vs Llama 70B 後処理結果並べて確認（歴史的記録、V4 では不要） |
| **🎯 E. V4 漢数字補正フロー** | Scribe 出力「二千二十六年四月二十九日」をクリップボードへ → `python scripts\scribe_kanjisuji_fix.py --clipboard` → 「2026年4月29日」に変換 |

### 7. ハードウェア確認（HP ProBook 制約）

- [ ] スペースキーの長さ確認（マウスコンピューターより長い可能性、親指シフトのフィーリング差を観察）
- [ ] 変換キーの位置確認（M の真下にあるか）
- [ ] マイクの感度確認（ノイズ環境で Scribe がどこまで耐えるか）

## SSH では未完了の項目（4/29 06:30 時点）

| 項目 | 理由 | 着席時の所要 |
|---|---|---|
| **SuperWhisper 本体 DL** | superwhisper.com が JS 認証 | 5 分 |
| **YamabukiR 本体 DL** | atwiki.jp が Cloudflare チャレンジ | 3 分 |
| **インストーラーの実行 (3 本)** | UAC ダイアログ + GUI ウィザード | 各 3-5 分 |
| **IME の選択** | システム設定の GUI | 1 分 |
| **SuperWhisper 設定** | Scribe ON / 左 Alt / 自動ペースト OFF / 日本語固定 | 5 分 |
| **API キー サインアップ × 3** | ElevenLabs / Groq / Gemini ブラウザ認証 | 各 3-5 分 |
| **`setup_api_keys.ps1` 実行** | キーを対話で貼付け | 2 分 |
| **親指シフト習得** | 物理練習が必要（数週間〜数ヶ月） | 継続 |
| **マイクテスト** | 物理音声入力（コワーキング有人時は禁止） | 環境次第 |

### 着席時の推奨実施順（最短ルート、〜45 分）

1. **(5 分)** SuperWhisper DL → インストール
2. **(3 分)** Google IME インストール（DL は SSH で完了済）
3. **(3 分)** YamabukiR DL → 展開
4. **(15 分)** ElevenLabs / Groq サインアップ → キー取得
5. **(2 分)** `setup_api_keys.ps1` 実行で永続化
6. **(5 分)** SuperWhisper 設定（Scribe / 左 Alt / 自動ペースト OFF / 日本語）
7. **(3 分)** 動作確認（V4 シナリオ E：漢数字補正）
8. **(残り)** 親指シフト触り始め

## 完了後の Substack 記事化

このセットアップ日記そのものが記事ネタ:
- タイトル候補: 「勝間和代の voice stack を SSH と物理着席で 1 日かけて再現してみた」
- 構成: SSH パート（80%）→ 物理パート（20%）→ できなかったこと → 編集方針への含意
