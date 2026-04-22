## セッション設定

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
- セッション開始時に `/model opusplan` を実行する（思考=Opus、実行=Sonnetの自動切り替え）

