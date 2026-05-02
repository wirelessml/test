# Switch 2 Joy-Con BLE プロトコル仕様 (Phase 1 deliverable)

> 出典: maruta/joycon2-usb-presenter (Apache 2.0) の README.md + src/main.c 解析
> 上流参照: Nohzockt/Switch2-Controllers (button bitmap + stick layout) + seitanmen/Joycon2forMac (input-enable sequence) + Misaka10571/joycon2-connector (write UUID + IMU/optical/LED format)
> ステータス: コミュニティ reverse-engineered、Joy-Con 2 ファーム更新で変わる可能性あり

## 1. GATT Services / Characteristics

すべて 128-bit カスタム UUID。Standard service UUID ではない。

| 役割 | UUID |
|---|---|
| **Nintendo Service** | `ab7de9be-89fe-49ad-828f-118f09df7fd0` |
| **Input Notify Characteristic** | `ab7de9be-89fe-49ad-828f-118f09df7fd2` |
| **Write Characteristic**（別 service 内）| `649d4ac9-8eb7-4e6c-af44-1ea54fe5f005` |

C# WinRT 対応:
```csharp
var serviceUuid  = new Guid("ab7de9be-89fe-49ad-828f-118f09df7fd0");
var inputUuid    = new Guid("ab7de9be-89fe-49ad-828f-118f09df7fd2");
var writeUuid    = new Guid("649d4ac9-8eb7-4e6c-af44-1ea54fe5f005");
```

## 2. ペアリング手順

1. **Joy-Con 2 を Switch 2 から切断**（推奨: Settings → Controllers → Disconnect Controllers）
2. **Joy-Con 2 側面の SYNC ボタン**を 約 5 秒長押し → Player LED が流れる（pairing mode）
3. ホスト（Windows）側で BLE スキャン → Joy-Con 2 検出 → ペア → Connect
4. 接続後 約 3 秒で input subscription / enable コマンド送信

⚠️ **注意**: 一度ペア後は Switch 2 との bond が無効化される。Switch 2 で再ペア必要。

## 3. Input Enable Sequence

ペア接続成功後、Write Characteristic に送信する初期化コマンド。**enable_std と enable_ext を交互に、約 300ms 間隔で数回送信**するのが安全（maruta コードでは交互送信ループ）。

### enable_std (12 bytes)
```
0x0c 0x91 0x01 0x02 0x00 0x04 0x00 0x00 0xff 0x00 0x00 0x00
```

### enable_ext (12 bytes)
```
0x0c 0x91 0x01 0x04 0x00 0x04 0x00 0x00 0xff 0x00 0x00 0x00
```

**送信方法**: `bt_gatt_write_without_response`（C 側）= **WriteWithoutResponse** モード（C# WinRT では `GattWriteOption.WriteWithoutResponse`）

C# 例:
```csharp
var enableStd = new byte[] { 0x0c, 0x91, 0x01, 0x02, 0x00, 0x04, 0x00, 0x00, 0xff, 0x00, 0x00, 0x00 };
await writeChar.WriteValueWithResultAsync(
    enableStd.AsBuffer(),
    GattWriteOption.WriteWithoutResponse);
```

## 4. Input Notify Packet Layout

Input Notify Characteristic に subscribe → BLE GATT Notify で push される。**最低 60 bytes**。

| Offset | Size | 内容 |
|---|---|---|
| 0-3 | 4 | header / sequence (未解析) |
| **4-6** | **3** | **ボタン bitmap (24 bit valid)** |
| 7 | 1 | status flags |
| 8-9 | 2 | (未解析) |
| **10-12** | **3** | **左スティック (12-bit packed: lx + ly)** |
| **13-15** | **3** | **右スティック (12-bit packed: rx + ry)** |
| **16-17** | **2** | **光学センサー X (int16 LE、絶対累積カウンタ)** |
| **18-19** | **2** | **光学センサー Y (int16 LE、絶対累積カウンタ)** |
| 20-53 | 34 | IMU データ (加速度、ジャイロ Y 等、未使用ある) |
| **54-55** | **2** | **ジャイロ X (int16 LE)** |
| 56-57 | 2 | ジャイロ Y (int16 LE、未使用) |
| **58-59** | **2** | **ジャイロ Z (int16 LE)** |

### スティック値の取り出し方

スティック値は 12-bit、3 bytes に X と Y がパックされる:

```c
uint16_t lx = p[10] | ((p[11] & 0x0f) << 8);      // 12-bit
uint16_t ly = (p[11] >> 4) | (p[12] << 4);        // 12-bit
uint16_t rx = p[13] | ((p[14] & 0x0f) << 8);
uint16_t ry = (p[14] >> 4) | (p[15] << 4);
```

中央値（neutral）は ~2048（12-bit のセンター）想定。**STICK_CENTER ≈ 2048**、**STICK_WHEEL_THRESH** で deadzone 設定。

### 光学センサーの差分計算

光学センサーは絶対累積カウンタ（int16 だが ring buffer 的に wrap する想定）なので、毎フレーム前回値との差分を取る:

```c
static int16_t prev_opt_x, prev_opt_y;
int16_t opt_x = (int16_t)sys_get_le16(&p[16]);
int16_t opt_y = (int16_t)sys_get_le16(&p[18]);
int16_t opt_dx = opt_x - prev_opt_x;
int16_t opt_dy = opt_y - prev_opt_y;
prev_opt_x = opt_x; prev_opt_y = opt_y;
```

初回は seed が必要（前回値なしなので 0 で初期化）。

## 5. ボタン bit position (JC_*)

24-bit bitmap (bytes 4-6 から little-endian で読み取り、0xffffff マスク)。

| bit | 名前 | 物理ボタン |
|---|---|---|
| 0 | JC_Y | Y |
| 1 | JC_X | X |
| 2 | JC_B | B |
| 3 | JC_A | A |
| 4 | JC_R_SR | 右側面 SR |
| 5 | JC_R_SL | 右側面 SL |
| 6 | JC_R | R |
| 7 | JC_ZR | ZR |
| 8 | JC_MINUS | - |
| 9 | JC_PLUS | + |
| 10 | JC_RJ | 右スティック押し込み |
| 11 | JC_LJ | 左スティック押し込み |
| 12 | JC_HOME | HOME |
| 13 | JC_CAPT | キャプチャ |
| 14 | JC_C | C ボタン (Switch 2 新ボタン) |
| 15 | (reserved) | — |
| 16 | JC_DOWN | ↓ |
| 17 | JC_UP | ↑ |
| 18 | JC_RIGHT | → |
| 19 | JC_LEFT | ← |
| 20 | JC_L_SR | 左側面 SR |
| 21 | JC_L_SL | 左側面 SL |
| 22-23 | (reserved) | — |

C# 取り出し:
```csharp
uint btn = (uint)(packet[4] | (packet[5] << 8) | (packet[6] << 16));
bool zrPressed = (btn & (1u << 7)) != 0;  // JC_ZR
```

## 6. Player LED Command (Write Characteristic)

12 bytes、Misaka10571/joycon2-connector 由来:

```
0x09 0x91 0x01 0x07 0x00 0x04 0x00 0x00 [mask] 0x00 0x00 0x00
```

[mask] は LED 点灯 bit:
- 0x01: LED1 (player 1 indicator)
- 0x02: LED2
- 0x04: LED3
- 0x08: LED4

複数同時点灯は OR で組み合わせ。

## 7. マッピング設計（maruta dongle 既定）

### キーボード
| Joy-Con 入力 | キー |
|---|---|
| RIGHT, A | → (0x4F) |
| LEFT, Y | ← (0x50) |
| DOWN, B | ↓ (0x51) |
| UP, X | ↑ (0x52) |
| MINUS, PLUS | P (0x13) |
| CAPT, C | E (0x08) |

### マウスボタン
| Joy-Con 入力 | アクション |
|---|---|
| ZR, ZL | 左クリック |
| R, L | 右クリック |
| RJ, LJ (スティック押し込み) | 中クリック |

### カーソル制御（gyro + 光学の和）

**両方を加算**して使う設計:
- **ジャイロ pointing**: 側面 SL/SR or クリックボタンを押している時のみ有効（gate 必要）
  - ジャイロ X 軸 → 縦移動（反転）
  - ジャイロ Z 軸 → 横移動（反転）
- **光学センサー**: 常時有効、机上をスライドさせると動く

C# 疑似コード:
```csharp
int dx = 0, dy = 0;
bool gyroGated = (btn & ((1u << JC_L_SL) | (1u << JC_L_SR) | (1u << JC_R_SL) | (1u << JC_R_SR) | (1u << JC_ZR) | (1u << JC_ZL) | (1u << JC_R) | (1u << JC_L))) != 0;

if (gyroGated)
{
    if (Math.Abs(gx) > GYRO_DEADZONE) dy += -gx / GYRO_DIVISOR;
    if (Math.Abs(gz) > GYRO_DEADZONE) dx += -gz / GYRO_DIVISOR;
}

dx += opt_dx / OPTICAL_DIVISOR;
dy += opt_dy / OPTICAL_DIVISOR;

// SendInput で dx, dy 注入
```

### スクロール
両スティックの X/Y → ホイール（X = 横、Y = 縦）。傾き量に比例した速度。

### レーザーポインタモード（toggle）
L_SL / R_SR の edge-press でトグル。ON 中は左クリック / ホイール時に Ctrl を自動 hold。

## 8. C# / .NET 8 / WinRT 実装ポイント

| 機能 | API |
|---|---|
| BLE スキャン | `Windows.Devices.Bluetooth.Advertisement.BluetoothLEAdvertisementWatcher` |
| デバイス取得 | `BluetoothLEDevice.FromBluetoothAddressAsync` |
| Service 取得 | `device.GetGattServicesForUuidAsync(serviceUuid)` |
| Char 取得 | `service.GetCharacteristicsForUuidAsync(...)` |
| Notify subscribe | `char.WriteClientCharacteristicConfigurationDescriptorAsync(GattClientCharacteristicConfigurationDescriptorValue.Notify)` + `char.ValueChanged += handler` |
| Write w/o response | `char.WriteValueWithResultAsync(buffer, GattWriteOption.WriteWithoutResponse)` |
| マウス注入 | `SendInput` Win32 API（P/Invoke）|

## 9. リスクと未解明箇所

- byte 0-3 の header / sequence: 解析されてない、おそらく packet sequence number。再送・順序判定不要なら無視可
- byte 7 status flags: バッテリー状態 / 接続種別 / 充電中フラグ等が入る可能性
- byte 8-9: 未解析
- IMU データ全体（bytes 20-53）: 加速度・ジャイロ Y は未使用、解析すれば IMU フル活用も可能
- 光学センサーの**サンプリングレート / wrap 挙動**: 詳細不明、要実機検証
- ファーム更新による互換性破壊: Joy-Con 2 はまだ新しい、Nintendo がファーム更新で BLE 仕様を変える可能性

## 10. Phase 1 完了基準

- [x] Service / Characteristic UUID 3 つ判明
- [x] ペアリング手順把握
- [x] Input enable コマンド byte 列確定
- [x] Input notify packet layout 完全マッピング (60 bytes 中の主要 offset)
- [x] ボタン bit position 22 個 + JC_*
- [x] Player LED コマンド format
- [x] スティック値の 12-bit 取り出し計算
- [x] 光学センサーの diff 取り方
- [x] ジャイロ axis の意味
- [x] C# WinRT API mapping 草案

→ **Phase 1 終了、Phase 2 (BLE 接続最小 C# サンプル) に進める**

## 関連ファイル

- `/tmp/joycon2-research/maruta-src/main.c`（参考実装、ローカル保管）
- `/tmp/joycon2-research/README.md`（参考実装ドキュメント）
- `docs/projects/joycon2-windows-driver.md`（プロジェクト全体計画）
