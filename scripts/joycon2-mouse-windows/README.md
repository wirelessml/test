# Joy-Con 2 Mouse for Windows

> Switch 2 Joy-Con (左右) を Windows のワイヤレスマウス + キーボードコントローラーとして使う。
> **dongle 不要**（nRF52840 等）、Windows 標準 Bluetooth で直接ペアリング。
>
> 開発: 2026-05-02 開始 / Apache License 2.0

## ステータス

- [x] **Phase 1**: BLE プロトコル解析・ドキュメント化（5/2 11:25 完了）→ `docs/projects/joycon2-protocol.md`
- [x] **Phase 2**: BLE 接続実機検証（5/2 11:59 成功）→ `test-logs/phase2-first-success-2026-0502-1200.log`
- [x] **Phase 3 scaffold**: SendInput マウス注入コード（Mac 側 5/3 朝書き、しゅん先生 PC で build/test 待ち）
- [ ] Phase 3 実機検証: マウスが実際に動くか
- [ ] Phase 4: GUI + タスクトレイ常駐 (WPF or Avalonia)
- [ ] Phase 5: 配布 (single-file exe, GitHub release)

## ファイル構成

```
joycon2-mouse-windows/
├── joycon2-mouse-windows.csproj   # .NET 8 + Windows 10 BLE API
├── Protocol.cs                     # GATT UUID, enable コマンド, ボタン bit position
├── InputPacket.cs                  # 60 byte パケット parse + 光学センサー差分計算
├── DeltaMapper.cs                  # gyro + 光学 + スティック → mouse delta + wheel + click edge
├── MouseInjector.cs                # SendInput Win32 API ラッパー
├── Program.cs                      # entry: scan → connect → subscribe → enable → 注入 or dump
├── LICENSE                         # Apache 2.0
├── NOTICE                          # 上流 reverse engineering プロジェクト謝辞
├── README.md
└── test-logs/                      # 実機検証ログ
```

## ビルド・実行（しゅん先生 PC、SSH 経由）

```powershell
# Mac から SCP で同期
scp -r /Users/yuika/Desktop/scripts/joycon2-mouse-windows wirel@desktop-atq36ks.local:./

# しゅん先生で build
ssh shun-sensei
cd C:\Users\wirel\joycon2-mouse-windows
dotnet build

# dump only (Phase 2 互換、安全に検証)
dotnet run

# マウス注入 ON で起動 (Phase 3)
dotnet run -- --mouse
```

⚠️ **マウス注入を ON にすると、Joy-Con を動かしただけでカーソルが動きます。**
**HOME ボタンで ON/OFF をトグルできます (緊急停止用)。**
Ctrl+C は通常通り効きます。

## マウスマッピング (Phase 3 暫定仕様)

| Joy-Con 入力 | Windows マウス操作 | 備考 |
|---|---|---|
| **光学センサー** (机上スライド) | カーソル移動 | 常時有効、X/Y を `OPTICAL_DIVISOR=4` で除算 |
| **ジャイロ** (空中で振る) | カーソル移動 | **トリガー (ZR/R/L) or 側面 SL/SR 押下中のみ有効** |
| **ZR ボタン** | 左クリック | edge detection で down/up |
| **R ボタン** | 右クリック | |
| **R スティック押し込み (RJ)** | 中クリック | |
| **R スティック傾き** | ホイール スクロール | Y → 縦、X → 横、deadzone 250 |
| **HOME ボタン** | マウス注入 toggle | **緊急停止スイッチ** |
| その他ボタン | 未マッピング | Phase 4 で GUI 経由カスタマイズ予定 |

### チューニング定数 (`DeltaMapper.cs` の public const)

| 定数 | 値 | 根拠 |
|---|---|---|
| `GyroDeadzone` | 50 | Phase 2 ログ実測 noise floor ~14 |
| `GyroDivisor` | 30 | 鈍さ調整 (大きいほど鈍い) |
| `OpticalDivisor` | 4 | 光学センサーは細かい |
| `OpticalDeltaClip` | 200 | BLE notify 抜けで稀に巨大 delta が出る対策 |
| `StickDeadzone` | 250 | 個体差で center が ±20 ずれるため広め |
| `StickWheelDivisor` | 8000 | スティック → 1 notch までの蓄積量 |

## 物理準備（Joy-Con 2 ペアリング、Phase 2/3 実機検証時）

⚠️ **重要**: ペアリングすると Joy-Con 2 と Switch 2 の bond が無効化される。Switch 2 で再ペア必要。

1. Switch 2 で「設定 → コントローラー → コントローラーの切断」で Joy-Con 2 切断
2. Joy-Con 2 側面の **SYNC ボタン**を ~5 秒長押し → Player LED が流れる
3. Windows 設定 → Bluetooth で「Joy-Con 2 (R)」を追加
4. `dotnet run` 実行 → 自動でペア済リストから検出して接続
5. 終了後、Switch 2 のコントローラー登録画面で再ペア

## 設計選択

| 項目 | 選択 | 理由 |
|---|---|---|
| 言語 | C# / .NET 8 | WinRT BLE API への native アクセス、Windows 配布が単一 exe で済む |
| BLE | `Windows.Devices.Bluetooth.GenericAttributeProfile` | OS 標準、driver 追加不要 |
| マウス注入 | `SendInput` Win32 API | OS 標準、driver 追加不要。ゲーム対応は Phase 5 で Interception 検討 |
| GUI | TBD（Phase 4）| WPF or Avalonia UI |
| 配布 | `dotnet publish -r win-x64 -p:PublishSingleFile=true` | 単一 exe、依存ランタイム同梱可 |

## 参考プロジェクト

- [maruta/joycon2-usb-presenter](https://github.com/maruta/joycon2-usb-presenter) (Apache 2.0): Joy-Con 2 BLE プロトコルの C 実装。本プロジェクトはこの解析結果を C# に移植
- [Nohzockt/Switch2-Controllers](https://github.com/Nohzockt/Switch2-Controllers): BLE スキャン + ボタン bitmap + スティック layout
- [seitanmen/Joycon2forMac](https://github.com/seitanmen/Joycon2forMac): input-enable コマンドシーケンス
- [Misaka10571/joycon2-connector](https://github.com/Misaka10571/joycon2-connector): write characteristic UUID、IMU/optical/LED フォーマット
- [Davidobot/BetterJoy](https://github.com/Davidobot/BetterJoy): Switch 1 Joy-Con xinput 化（C#、参考になる）

## ライセンス

Apache License 2.0（maruta との互換性、reverse engineered protocol の上で成り立つため明示的に派生物として位置づけ）

## 商標表示

Nintendo / Switch / Joy-Con は任天堂株式会社の商標。本プロジェクトは独立した非公式作品で、任天堂とは関連・支援・後援関係にない。
