# Joy-Con 2 Mouse for Windows

> Switch 2 Joy-Con (左右) を Windows のワイヤレスマウス + キーボードコントローラーとして使う。
> **dongle 不要**（nRF52840 等）、Windows 標準 Bluetooth で直接ペアリング。
>
> 開発: 2026-05-02 開始、Apache 2.0 を予定（コードは MIT or Apache 2.0、最終決定 Phase 5 で）

## ステータス

- [x] **Phase 1**: BLE プロトコル解析・ドキュメント化（5/2 11:25 完了）→ `docs/projects/joycon2-protocol.md`
- [x] **Phase 2 scaffold**: スキャン + 接続 + subscribe + enable + dump の最小サンプル（コンパイル可、実機未検証）
- [ ] Phase 2 実機検証: Joy-Con 2 ペアリングして動作確認
- [ ] Phase 3: マウスイベント注入 (SendInput)
- [ ] Phase 4: GUI + タスクトレイ常駐 (WPF or Avalonia)
- [ ] Phase 5: 配布 (single-file exe, GitHub release)

## ファイル構成

```
joycon2-mouse-windows/
├── joycon2-mouse-windows.csproj  # .NET 8 + Windows 10 BLE API
├── Protocol.cs                    # GATT UUID, enable コマンド, ボタン bit position
├── InputPacket.cs                 # 60 byte パケット parse + 光学センサー差分計算
├── Program.cs                     # entry: scan → connect → subscribe → dump
└── README.md
```

## ビルド・実行（しゅん先生 PC、SSH 経由）

```powershell
# Mac から SCP
scp -r /Users/yuika/Desktop/scripts/joycon2-mouse-windows wirel@desktop-atq36ks.local:./

# しゅん先生で build + run
ssh shun-sensei
cd C:\Users\wirel\joycon2-mouse-windows
dotnet build
dotnet run
```

## 必要な物理準備（Joy-Con 2 ペアリング、Phase 2 実機検証時）

⚠️ **重要**: ペアリングすると Joy-Con 2 と Switch 2 の bond が無効化される。Switch 2 で再ペア必要。

1. Switch 2 で「設定 → コントローラー → コントローラーの切断」で Joy-Con 2 切断
2. Joy-Con 2 側面の **SYNC ボタン**を ~5 秒長押し → Player LED が流れる
3. Windows 側で `dotnet run` 実行（自動で BLE スキャン → Joy-Con 2 検出 → ペア）
4. 接続成功すると input notify がコンソールに dump される
5. 終了後、Switch 2 のコントローラー登録画面で再ペア

## 設計選択

| 項目 | 選択 | 理由 |
|---|---|---|
| 言語 | C# / .NET 8 | WinRT BLE API への native アクセス、Windows 配布が単一 exe で済む |
| BLE | `Windows.Devices.Bluetooth.GenericAttributeProfile` | OS 標準、driver 追加不要 |
| マウス注入 | `SendInput` Win32 API（Phase 3）| Interception driver は Phase 5 でゲーム対応用に検討 |
| GUI | TBD（Phase 4）| WPF or Avalonia UI（VS Code で開発しやすい方）|
| 配布 | `dotnet publish -r win-x64 -p:PublishSingleFile=true` | 単一 exe、依存ランタイム同梱可 |

## 参考プロジェクト

- [maruta/joycon2-usb-presenter](https://github.com/maruta/joycon2-usb-presenter) (Apache 2.0): Joy-Con 2 BLE プロトコルの C 実装。本プロジェクトはこの解析結果を C# に移植
- [Nohzockt/Switch2-Controllers](https://github.com/Nohzockt/Switch2-Controllers): BLE スキャン + ボタン bitmap + スティック layout
- [seitanmen/Joycon2forMac](https://github.com/seitanmen/Joycon2forMac): input-enable コマンドシーケンス
- [Misaka10571/joycon2-connector](https://github.com/Misaka10571/joycon2-connector): write characteristic UUID、IMU/optical/LED フォーマット
- [Davidobot/BetterJoy](https://github.com/Davidobot/BetterJoy): Switch 1 Joy-Con xinput 化（C#、参考になる）

## ライセンス予定

Apache 2.0（maruta との互換性、reverse engineered protocol の上で成り立つため明示的に派生物として位置づけ）

## 商標表示

Nintendo / Switch / Joy-Con は任天堂株式会社の商標。本プロジェクトは独立した非公式作品で、任天堂とは関連・支援・後援関係にない。
