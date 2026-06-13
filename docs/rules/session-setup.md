## セッション設定

### 🕐 「枠の頭で計画」ルール（2026-06-11 制定）

> 🤖 **2026-06-12 自動化**: SessionStart フック（`.claude/settings.json` → `scripts/session-start-brief.sh`）が、セッション開始時に現在時刻＋このルールのリマインド＋最新ジャーナルの「未完了/持ち越し」を自動注入する。Claude の記憶頼みから設定駆動に昇格。

Claude のレート制限は**最初のメッセージから始まる 5 時間のローリング枠**。固定時刻のカレンダー予定（旧セッションスケジュール、6/11 廃止）ではなく、枠単位で計画する。

1. **セッション接続時（＝新しい 5 時間枠の始まり）に、Claude が冒頭で「この枠のプラン」を 3 行で提示する**
   - この枠の優先タスク（1〜2 個）
   - 重い処理（GUI 自動化・大量走査・長い調査）の有無 → あるなら**枠の前半に配置**
   - 前の枠からの持ち越し
2. **重い作業に入る前に残り枠を意識する**。枠の残りが薄いときは着手前に申告し、次の枠に回す判断を仰ぐ（操作ルール「時間かかりすぎ＝中止シグナル」とセットで運用）
3. 無人時間帯の定型処理（就活レポート 04:30 等）は LaunchAgent が担うため計画不要。計画対象は「ユーザーと Claude が一緒に動く枠」のみ
4. 背景: 2026-06-10 に iMovie テスト中に枠を使い切り 30 分以上停止した教訓（@docs/journal/2026-06-10 参照）

- **セッション開始時にターミナルを常に最前面に設定する**（ユーザーに案内して実行）
  - SkyLight プライベートAPIでウィンドウレベルをフローティング（3）に設定
  - コマンド:
    ```bash
    /usr/bin/python3 -c "
    import ctypes
    sl = ctypes.CDLL('/System/Library/PrivateFrameworks/SkyLight.framework/SkyLight')
    SLSMainConnectionID = sl.SLSMainConnectionID
    SLSMainConnectionID.restype = ctypes.c_uint32
    SLSSetWindowLevel = sl.SLSSetWindowLevel
    SLSSetWindowLevel.argtypes = [ctypes.c_uint32, ctypes.c_uint32, ctypes.c_int32]
    SLSSetWindowLevel.restype = ctypes.c_int32
    conn = SLSMainConnectionID()
    import subprocess
    r = subprocess.run(['osascript', '-e', 'tell application \"Terminal\" to get id of every window'], capture_output=True, text=True)
    for wid in r.stdout.strip().split(', '):
        if wid.strip():
            result = SLSSetWindowLevel(conn, int(wid.strip()), 3)
            print(f'Window {wid}: level=3 (floating), result={result}')
    "
    ```
  - ウィンドウを閉じて再度開くとリセットされるため、毎セッション実行が必要
  - 元に戻す場合はレベルを0に設定
- **🚫 モデル切替禁止（2026-06-13 ユーザー指示）**: 〜6/22 の Fable 5 無料期間中は **`/model` を実行しない・提案しない**（`~/.claude/settings.json` に `"model": "claude-fable-5"` で固定済み）。6/23 以降にユーザー確認の上で `/model opusplan`（思考=Opus、実行=Sonnetの自動切り替え）に戻す

