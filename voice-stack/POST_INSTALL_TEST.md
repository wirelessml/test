# 退館後 / 自宅用 動作テスト手順（4/29 着席後）

> 着席日 (2026-04-29 06:30〜07:00 JST) のセットアップ完了状態。コワーキング有人のためマイクテストは未実施。退館後 or 自宅で以下を実行して voice stack の最終動作確認。

## 着席日完了事項（マイクなしで確認済）

| 項目 | 状態 |
|---|---|
| Python 3.12.10 + 主要 SDK | ✅ |
| 10 スクリプト配置 | ✅ |
| ELEVENLABS_API_KEY 永続化 | ✅ (starter tier) |
| ElevenLabs API 接続検証 | ✅ |
| `scribe_kanjisuji_local.py` ユニットテスト | ✅ 8/8 PASS |
| クリップボード経由 漢数字変換 | ✅ 27c → 25c |
| SuperWhisper Windows インストール | ✅ |
| SuperWhisper 設定 | ✅ S1-Voice / Japanese / Voice / Push to Talk: Alt / Auto paste: Off |
| SuperWhisper プロセス稼働 | ✅ Console session 1 |

## マイクテスト手順（人がいない環境で）

### 1. 環境変数を新セッションに反映

PowerShell を再起動 or 以下で環境変数を読み込み:

```powershell
$env:ELEVENLABS_API_KEY = [Environment]::GetEnvironmentVariable("ELEVENLABS_API_KEY", "User")
echo $env:ELEVENLABS_API_KEY  # sk_... が出れば OK
```

### 2. SuperWhisper 単体テスト

メモ帳など何かテキストエディタを開いて:

1. **左 Alt 長押し**
2. 「テストです、二千二十六年四月二十九日」と発話
3. **Alt 離す**
4. 数秒待機（クラウド転写）
5. クリップボードに転写結果が入る（自動ペーストは Off にしてあるので貼り付けはされない）
6. 確認:
   ```powershell
   Get-Clipboard
   ```

### 3. 漢数字補正テスト

```powershell
python C:\Users\gci_admin\voice-stack\scripts\scribe_kanjisuji_local.py --clipboard
Get-Clipboard
```

期待動作:
- BEFORE: `テストです、二千二十六年四月二十九日`
- AFTER: `テストです、2026年4月29日`

### 4. End-to-End フロー

1. テキストエディタでカーソル設置
2. **左 Alt 長押し → 発話 → 離す**
3. クリップボードに転写結果が入るまで待機（~3 秒）
4. PowerShell から:
   ```powershell
   python C:\Users\gci_admin\voice-stack\scripts\scribe_kanjisuji_local.py --clipboard
   ```
5. テキストエディタで `Ctrl+V` で貼り付け（漢数字補正済テキスト）

## 自動化（運用開始時）

### A. trim_clipboard.py を常駐（先頭半角スペース自動除去 + 自動ペースト）

```powershell
# 別ターミナルで起動
python C:\Users\gci_admin\voice-stack\scripts\trim_clipboard.py
```

これで Alt 長押し → 発話 → 離す → 自動でカーソル位置に貼り付けられる。

### B. 漢数字補正もパイプライン化（必要なら）

trim_clipboard.py を改造して trim 後に scribe_kanjisuji_local.convert() を呼ぶようにする。

## トラブルシューティング

### マイクが認識されない

```powershell
python C:\Users\gci_admin\voice-stack\scripts\test_audio.py
```

→ デフォルトデバイス確認、`マイク配列 (Intel SST)` ch=2 sr=44100 が正常。

### SuperWhisper が反応しない

- タスクマネージャで Superwhisper.exe が動いてるか確認
- `Get-Process superwhisper`
- 動いてなければ手動起動: `C:\Users\gci_admin\AppData\Local\superwhisper\Superwhisper.exe`

### 転写精度が悪い

S1-Voice → Ultra や Nova 3 に切替試す（Modes → Default → Voice Model）。

## 観察哲学（編集方針）

勝間和代の voice stack を **物理コピー**するのではなく、**追体験して理解する**のが目的。
- S1-Voice は Mac の Scribe と完全一致しない可能性あり、その差を観察する
- 漢数字補正もローカル正規表現で済むという発見そのものが Substack 記事ネタ
- 4/29 朝の SSH セットアップ → 着席日設定 → 退館後テストの 3 段階プロセスも記録価値あり
