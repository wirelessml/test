# MASU-P55 物理着席日にやる作業

> SSH では完結できない、物理キーボード + GUI 操作が必要な手順を集約。

## チェックリスト（推奨実施順）

### 0. 事前確認（SSH 構築済み事項、4/28 09:48 完了）

| 項目 | 状態 |
|---|---|
| Python 3.12 | ✅ インストール済 |
| pip 主要 SDK | ✅ groq / elevenlabs / anthropic / google-genai / openai / browser-use |
| pyperclip / keyboard / sounddevice / numpy | ✅ 4/28 セッションで追加 |
| `~/voice-stack/scripts/` 7 スクリプト | ✅ 配置済 |
| マイクデバイス | ✅ 20 個検出、デフォルト = `マイク配列 (Intel SST)` ch=2 sr=44100 |
| `chcp 65001` (UTF-8) 設定 | ⚠️ ターミナルごとに必要、永続化推奨 |

### 1. SuperWhisper Windows 版インストール（v1.3.9 確認、x64 / ARM64）

- [ ] https://superwhisper.com/ をブラウザで開く（DL は JS 動的、SSH では取得不可）
- [ ] 「Download for Windows」ボタン → **x64** を選択（HP ProBook は x64）
- [ ] `C:\Users\gci_admin\voice-stack\downloads\` に保存
- [ ] インストール実行
- [ ] 起動後、設定で **Scribe (実験モデル)** をオンにする
- [ ] ホットキー設定: **左 Alt** に割り当て（勝間 4/11 ツイート準拠）
- [ ] **自動ペースト OFF**（重要、Python トリム → ペーストの順番を変えるため）
- [ ] 設定 → 言語 → **日本語** 固定
- [ ] ElevenLabs API キー貼付け

### 2. Google 日本語入力インストール

- [ ] `C:\Users\gci_admin\voice-stack\downloads\` に `googlejapaneseinput-installer.exe` あるか確認
- [ ] ない場合: https://www.google.co.jp/ime/ から DL
- [ ] インストール → デフォルト IME に設定
- [ ] 設定で **MS-IME 互換** を一旦選択（YamabukiR と相性が良い）

### 3. YamabukiR (親指シフトエミュレータ) インストール

> 勝間さんと同じ構成 (4/16 19:04 ツイート)

- [ ] `C:\Users\gci_admin\voice-stack\downloads\yamabuki_r_xxx.zip` 確認
- [ ] ない場合: http://www6.atwiki.jp/yamabuki/ から DL
- [ ] 適当なディレクトリに展開（例: `C:\Tools\YamabukiR\`）
- [ ] `YamabukiR.exe` を管理者権限で実行
- [ ] 親指シフト (NICOLA) 配列定義ファイルを読み込み
- [ ] スタートアップに登録（自動起動）
- [ ] **テスト**: 「いう」を SK + DJ で打って正しく入力されるか確認
  - S+K = い (右親指 + S)
  - D+J = う (左親指 + J)

### 4. 環境変数永続設定

PowerShell 管理者権限で:

```powershell
setx ELEVENLABS_API_KEY "sk_..."
setx GROQ_API_KEY "gsk_..."
setx GEMINI_API_KEY "AIza..."
```

新しいターミナルで反映確認:
```powershell
echo $env:ELEVENLABS_API_KEY
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
| **B. SuperWhisper + Scribe** | 左 Alt 押下中に「テスト録音です」と発話 → 離す → 自動転写 → クリップボード → trim_clipboard.py が自動ペースト |
| **C. 無変換キー Groq** | 無変換押下中に発話 → 離す → Groq Whisper で転写 → ペースト |
| **D. V3 比較** | テキスト入力 → GPT 120B vs Llama 70B 後処理結果並べて確認 |

### 7. ハードウェア確認（HP ProBook 制約）

- [ ] スペースキーの長さ確認（マウスコンピューターより長い可能性、親指シフトのフィーリング差を観察）
- [ ] 変換キーの位置確認（M の真下にあるか）
- [ ] マイクの感度確認（ノイズ環境で Scribe がどこまで耐えるか）

## SSH では未完了の項目

| 項目 | 理由 |
|---|---|
| インストーラーの実行 | UAC ダイアログ + GUI ウィザード |
| IME の選択 | システム設定の GUI |
| SuperWhisper 設定 | GUI ホットキー設定 |
| 親指シフト習得 | 物理練習が必要（数週間〜数ヶ月） |
| マイクテスト | 物理音声入力 |

## 完了後の Substack 記事化

このセットアップ日記そのものが記事ネタ:
- タイトル候補: 「勝間和代の voice stack を SSH と物理着席で 1 日かけて再現してみた」
- 構成: SSH パート（80%）→ 物理パート（20%）→ できなかったこと → 編集方針への含意
