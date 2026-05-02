# Joy-Con 2 Windows マウス化ドライバ開発

> 開始予定: 2026-05-02 以降 (5/1 23:52 JST 週次クォータリセット後の余裕枠で着手)
> 開発機: しゅん先生 PC (Windows 11 Insider Preview、i7-8700K + 16GB)
> リモート: M1 Mac から `ssh shun-sensei` で操作可能

## 目的

Switch 2 の Joy-Con (右) を Windows PC のワイヤレスマウス + キーボードコントローラーとして使う。**dongle (nRF52840 等) を使わず、Windows 標準 Bluetooth で直接ペアリング**する software-only 実装を狙う。

## 動機

- Switch 2 Joy-Con には光学センサー + ジャイロ + マウスモードが搭載されている (純正ハードウェア)
- しかし Switch 2 Joy-Con の BLE プロトコルは任天堂独自で reverse engineered 段階
- 既存の Windows 用 Joy-Con ツール (BetterJoyForCemu / JoyShockLibrary) は **Switch 1 専用**、Switch 2 非対応
- maruta/joycon2-usb-presenter (Apache 2.0) は nRF52840 dongle ファームウェアとして Switch 2 BLE 解析を実装済 = **解析結果を C# に移植すれば dongle 不要**
- コミュニティ初の software-only Windows ドライバになる可能性

## 技術スタック

| レイヤ | 選択 |
|---|---|
| 言語 | C# / .NET 8 |
| BLE 接続 | WinRT Bluetooth LE API (`Windows.Devices.Bluetooth.GenericAttributeProfile`) |
| HID 注入 | SendInput Win32 API (簡易版 V1) → Interception driver (V2 ゲーム対応版) |
| GUI | WPF (VS Code でも開発可、WinUI 3 は VS Code 不向きなので除外) or **Avalonia UI** (XAML、VS Code 開発向き) |
| 配布 | single-file exe (`dotnet publish -r win-x64 -p:PublishSingleFile=true`) |
| 開発環境 | **VS Code + C# Dev Kit + .NET 8 SDK** (Visual Studio 2022 不要、軽量路線) |
| ビルド/実行 | `dotnet build` / `dotnet run` / `dotnet test` (CLI 完結、VS Code は editor + debugger として使う) |

## 参考プロジェクト

| 名 | 役割 | URL |
|---|---|---|
| maruta/joycon2-usb-presenter | Switch 2 BLE プロトコル解析の C 実装 (Apache 2.0) | https://github.com/maruta/joycon2-usb-presenter |
| Davidobot/BetterJoy | Switch 1 Joy-Con Windows xinput 化 (C#) | https://github.com/Davidobot/BetterJoy |
| JibbSmart/JoyShockLibrary | クロス PF C ライブラリ | https://github.com/JibbSmart/JoyShockLibrary |
| oblitum/Interception | キーボード/マウスイベント注入 driver | https://github.com/oblitum/Interception |
| vJoy | 仮想ジョイスティック driver | http://vjoystick.sourceforge.net/ |

## マイルストーン

### Phase 1: 情報整理 (~半日、トークン軽め) ✅ 5/2 11:25 完了

- [x] maruta/joycon2-usb-presenter の C コード全文を読み解く
- [x] BLE GATT services / characteristics / プロトコル仕様を Markdown でドキュメント化 → `docs/projects/joycon2-protocol.md`
- [x] 入力データフォーマット (ボタン / スティック / ジャイロ / 加速度 / 光学センサー / バッテリー) を表に整理
- [x] C# WinRT API mapping 草案

主要発見:
- Service UUID `ab7de9be-89fe-49ad-828f-118f09df7fd0`
- Input notify `ab7de9be-89fe-49ad-828f-118f09df7fd2`
- Write char `649d4ac9-8eb7-4e6c-af44-1ea54fe5f005` (別 service)
- Input enable コマンド: enable_std + enable_ext を交互送信 (12 bytes ずつ、300ms 間隔)
- Input packet: 60 bytes、ボタン bytes 4-6、スティック 12-bit packed bytes 10-15、光学 X/Y bytes 16-19、ジャイロ X/Z bytes 54-55/58-59
- ボタン bit 22 個 (JC_Y=0 〜 JC_L_SL=21)

### Phase 2: BLE 接続最小サンプル (~1 セッション)

- [x] WinRT で Joy-Con 2 にスキャン + サービス列挙する C# コードを書く（Phase 2 scaffold、5/2 11:35 完了）
- [x] dotnet build 成功（しゅん先生 PC、net8.0-windows10.0.19041.0、0 警告 0 エラー、4.35s）
- [x] **Joy-Con 2 ペアリング実機検証**（5/2 11:59 成功）
- [x] GATT characteristic を subscribe してデータダンプ確認
- [x] enable_std/ext 送信 → 60 byte パケット受信を確認
- [x] InputPacket.cs のパース結果（ボタン・スティック・光学・ジャイロ）が maruta コードと一致するか照合 → **完全一致**

5/2 12:00 実機検証ログ要点 (test-logs/phase2-first-success-2026-0502-1200.log):
- service `ab7de9be-...-fd0` 解決成功
- input notify char `ab7de9be-...-fd2` 解決成功
- write char `649d4ac9-...-f005` 解決成功（同 service 内に存在 = README とは違う、Joy-Con 2 側で実際は同じ service に集約）
- notify subscribe Success
- enable_std/ext 6 回送信全 Success
- 右スティック L=(2047,2047) R=(2063,2007) ← 中央値（StickCenter=2048 と一致）
- R_SL ボタン押下: btn=0x000020 (bit 5、JC_R_SL=5 一致)
- R ボタン押下: btn=0x000040 (bit 6、JC_R=6 一致)
- 光学センサー 机上スライド: opt=(-4544,-2503) optD=(-40,-352) ← 12-bit packed + diff 計算完璧
- ジャイロ振る: gyro=(896, 234) ← int16 LE 正常パース

ハマった点 (Phase 2 実機検証中):
1. Joy-Con 2 advertisement に LocalName/ServiceUuid 含まれない → scan ベース検出は不可
2. Windows BT 設定で paired すれば DeviceInformation.FindAllAsync で取得可
3. Paired 状態で BluetoothLEDevice.FromIdAsync 経由が成功パス
4. 過去ペア「Bluetooth LE Device c8...」(C8:48:05:25:71:27) は実は Joy-Con 2 だった（Windows が name 解決した後「Joy-Con 2 (R)」と表示）
5. SSH Services session では stdout 不可視 → File ベースのログ出力に切替 (LogPath = ~/joycon2-run.log)

成果物 (5/2 11:35 時点):
- `scripts/joycon2-mouse-windows/joycon2-mouse-windows.csproj` (.NET 8 + Windows 10 BLE API)
- `scripts/joycon2-mouse-windows/Protocol.cs` (UUIDs, enable コマンド, ボタン bit position)
- `scripts/joycon2-mouse-windows/InputPacket.cs` (60 byte パケット parse + 光学差分 tracker)
- `scripts/joycon2-mouse-windows/Program.cs` (scan → connect → subscribe → enable → dump、コンソールアプリ entry)
- `scripts/joycon2-mouse-windows/README.md`
- しゅん先生 PC `C:\Users\wirel\joycon2-mouse-windows\` に SCP 済 + ビルド済

### Phase 3: マウスイベント注入 (~1 セッション)

#### Phase 3 scaffold (5/3 朝、Mac 側で書ききった分)

しゅん先生 PC を起動する前に Mac 側で書けるコードを完成させた:

- [x] `scripts/joycon2-mouse-windows/MouseInjector.cs` 新規作成 — Win32 `SendInput` の P/Invoke 薄ラッパー (move/click/wheel V/H)
- [x] `scripts/joycon2-mouse-windows/DeltaMapper.cs` 新規作成 — gyro + 光学 + スティック → mouse delta + wheel notch + click edge への変換ロジック (状態保持あり)
- [x] `Program.cs` を Phase 3 対応に拡張: `--mouse` CLI フラグ + HOME ボタンランタイム toggle + OnInputNotify で MouseInjector 呼び出し
- [x] チューニング定数を Phase 2 ログ実測値ベースで決定 (GyroDeadzone=50、StickDeadzone=250、OpticalDeltaClip=200 等)
- [x] `LICENSE` (Apache 2.0)・`NOTICE` (上流謝辞)・`README.md` (Phase 3 マッピング表反映) 整備
- [ ] **しゅん先生 PC で `dotnet build` 通すこと** (Mac は `net8.0-windows10.0.19041.0` ターゲットなので build 不可)
- [ ] **実機でカーソル動作確認** (光学スライド・ジャイロ・クリック・ホイール)
- [ ] チューニング微調整 (実機感触に応じて divisor / deadzone 調整)

#### マウスマッピング (暫定)

| Joy-Con 入力 | Windows 操作 |
|---|---|
| 光学センサー (机上スライド) | カーソル移動 (常時) |
| ジャイロ (空中) | カーソル移動 (ZR/R/L/SL/SR 押下中のみ gating) |
| ZR | 左クリック |
| R | 右クリック |
| R スティック押し込み | 中クリック |
| R スティック傾き Y/X | ホイール 縦/横 |
| HOME | マウス注入 ON/OFF トグル (緊急停止) |

#### 検証チェックリスト (しゅん先生 PC 起動後)

```powershell
# Mac 側で push 済 → しゅん先生 PC で pull
ssh shun-sensei
cd C:\Users\wirel\joycon2-mouse-windows
git pull   # or: scp で再同期
dotnet build
dotnet run                # まず dump only で動作確認
dotnet run -- --mouse     # マウス注入 ON
```

検証項目:
- [ ] dotnet build が 0 警告 0 エラー (新規 .cs 2 ファイル + Program.cs 改変)
- [ ] dump モード (`dotnet run`) は Phase 2 と同じ挙動
- [ ] `--mouse` で起動 → 机上スライドでカーソル動く
- [ ] ZR で左クリック (notepad で文字選択できる)
- [ ] R で右クリック (コンテキストメニュー出る)
- [ ] R スティック上下でスクロール
- [ ] HOME ボタンで一時停止できる
- [ ] Ctrl+C で正常終了

#### 既知のリスク

- **キャリブレーションなし**: スティック center が個体差で ±20 ずれる (Phase 2 で実測)。最初の数フレームで center を sample する init 処理を Phase 3 後半で入れるか検討
- **BLE notify 抜けによる暴走**: SSH 越しに見えた光学 delta 2000+ をそのまま注入するとカーソルが画面外に飛ぶ。`OpticalDeltaClip=200` で抑止しているが、より長い欠測には未対応
- **gyro 軸の符号**: maruta コードに合わせて反転しているが、実機で逆方向に動いたら符号反転で対応

### Phase 4: GUI + タスクトレイ常駐 (~1 セッション)

- [ ] WinUI 3 で設定 GUI 作成 (キーマッピング、感度、ジャイロ ON/OFF)
- [ ] タスクトレイアイコン + 右クリックメニュー
- [ ] 自動起動オプション

### Phase 5: 配布 + ドキュメント (~半セッション)

- [ ] GitHub リポジトリ作成 (`wirelessml/joycon2-mouse-windows` 仮)
- [ ] README.md + LICENSE (MIT or Apache 2.0)
- [ ] single-file exe ビルド + Release 配布

## Substack 連載素材化

各 Phase 完了ごとに Substack note 投稿:
1. 「Switch 2 Joy-Con のマウスモードを Windows で動かしたい (Day 1)」 — 動機 + 先行調査 + プロトコル整理
2. 「Joy-Con 2 と Bluetooth でハンドシェイクする (Day 2)」 — WinRT BLE ペアリング成功の瞬間
3. 「ジャイロセンサーから 1px のずれを取り出す (Day 3)」 — マウスデルタ計算の試行錯誤
4. 「タスクトレイで常駐させる (Day 4)」 — GUI 化
5. 「OSS として公開した (Day 5)」 — リポジトリ公開 + 反応

= 連載「Switch 2 Joy-Con を Windows でマウス化する 5 日」として 4/28-5/10 SEO ピーク中の素材になる可能性。

## 物理準備 (Claude 起動前にやっておくこと、しゅん先生 PC 上で実行)

```powershell
# VS Code + .NET 8 SDK を winget で一括インストール
winget install Microsoft.VisualStudioCode -e --accept-source-agreements --accept-package-agreements
winget install Microsoft.DotNet.SDK.8 -e --accept-source-agreements --accept-package-agreements

# VS Code 必須拡張機能
code --install-extension ms-dotnettools.csdevkit
code --install-extension ms-dotnettools.csharp
code --install-extension ms-dotnettools.vscode-dotnet-runtime

# あると便利な拡張
code --install-extension eamodio.gitlens
code --install-extension yzhang.markdown-all-in-one
code --install-extension AvaloniaTeam.vscode-avalonia   # Avalonia UI 採用時のみ
```

- [ ] 上記コマンドを M1 から `ssh shun-sensei` 経由で実行 (VS Code GUI 操作不要)
- [ ] `dotnet --version` で 8.x 確認
- [ ] `code --version` で VS Code バージョン確認
- [ ] Joy-Con 2 充電 + Switch 2 から切断 (ペアリング解除)
- [ ] Joy-Con 2 の BLE 広告モード確認 (シンクロボタン長押し → LED 流れる状態)

## トークン予算試算

| Phase | Opus 4.7 想定 | Sonnet 4.6 補助 |
|---|---:|---:|
| 1 (情報整理) | ~30k | - |
| 2 (BLE 接続) | ~50k (試行錯誤含む) | - |
| 3 (マウス注入) | ~50k | ~10k (テスト support) |
| 4 (GUI) | ~30k | ~20k (UI コード補助) |
| 5 (配布) | ~10k | - |
| **合計** | **~170k** | **~30k** |

= 週次クォータの 50-70% 規模、3-5 日で完了見込み。1 リセットでは収まらないため、5/2 から始めて週末跨ぎ。

## リスクと回避

| リスク | 対策 |
|---|---|
| BLE プロトコルが maruta コードと違う (Joy-Con 2 ファーム更新等) | 実機でデータダンプして検証、必要なら再解析 |
| WinRT BLE が不安定 (Windows 11 Insider Preview) | 安定版 Windows 11 でも動作確認、必要なら Windows API ベースに切り替え |
| 任天堂規約・ToS 抵触可能性 | 個人利用限定、reverse engineering は法的に grey、配布時は disclaimer |
| 開発中にトークン枯渇 | Phase 単位で commit + push、リセット待機 |

## ロードマップ (案)

```
5/1 23:52  クォータリセット
5/2 朝     Phase 1 着手 (情報整理)
5/2 夕     Phase 2 着手 (BLE 接続)
5/3        Phase 3 (マウス注入)
5/4        Phase 4 (GUI)
5/5        Phase 5 (配布) + Substack 連載 1-2 回投稿
5/6-7      連載 3-5 回投稿、反応観察、追記改善
```

## 関連ファイル

- 動機ツイート: maruta/joycon2-usb-presenter (4/30 ユーザーが共有)
- しゅん先生 PC SSH: @docs/machines/shun-sensei-pc.md
- 開発ロケーション (予定): `~/Desktop/joycon2-mouse-windows/` (M1) or `C:\Users\wirel\source\repos\joycon2-mouse-windows\` (Windows)
