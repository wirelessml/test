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

### Phase 1: 情報整理 (~半日、トークン軽め)

- [ ] maruta/joycon2-usb-presenter の C コード全文を読み解く
- [ ] BLE GATT services / characteristics / プロトコル仕様を Markdown でドキュメント化
- [ ] 入力データフォーマット (ボタン / スティック / ジャイロ / 加速度 / 光学センサー / バッテリー) を表に整理
- [ ] 既存 Switch 1 ツールから流用可能な共通要素を identify

### Phase 2: BLE 接続最小サンプル (~1 セッション)

- [ ] WinRT で Joy-Con 2 にスキャン + ペアリング + サービス列挙する C# コードを書く
- [ ] GATT characteristic を subscribe してデータダンプ
- [ ] maruta コードのプロトコル解析と照合してデータ意味を確定

### Phase 3: マウスイベント注入 (~1 セッション)

- [ ] ジャイロ + 光学センサーから X/Y デルタを計算
- [ ] SendInput でマウスカーソル移動を実装
- [ ] ボタンマッピング (ZR = 左クリック、Z = 右クリック、SR = ホイール等) を仮決定
- [ ] スティック → ホイールスクロール実装

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
