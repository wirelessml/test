# Switch 2 の Joy-Con を Windows のマウスにしたい (Day 1)

> 連載「Switch 2 Joy-Con を Windows でマウス化する 5 日」第 1 回
> 公開予定: 2026-05-05 以降
> 著者: 仲啓輔

## 5,000 円のドングルが 0 円になる話

Switch 2 の Joy-Con は、机の上を滑らせるとマウスとして使える。Switch 本体に挿して書類アプリやレースゲームで使うやつだ。

このマウスモード、Windows でも使えると便利だなと思った。ジャイロ + 光学センサー + スタンドにもなる絶妙な握り感。3D モデリングのナビゲーションや、PowerPoint のレーザーポインタ、何ならふつうにブラウザのスクロール用でもよさそうだ。

調べると先行例があるにはあった。

- [Davidobot/BetterJoy](https://github.com/Davidobot/BetterJoy) — Switch **1** の Joy-Con を Windows xinput 化する C# プロジェクト。Switch 2 非対応。
- [JibbSmart/JoyShockLibrary](https://github.com/JibbSmart/JoyShockLibrary) — クロスプラットフォーム C ライブラリ。これも Switch 1 まで。

Switch 2 の Joy-Con は BLE プロトコルが任天堂独自で、コミュニティが reverse engineer 中の段階。既存ツールはまだ追いついていない。

唯一見つけた現役の Switch 2 対応プロジェクトが [maruta/joycon2-usb-presenter](https://github.com/maruta/joycon2-usb-presenter)（Apache 2.0）だった。これは **nRF52840 という BLE ドングル**にファームウェアを書き込んで、Joy-Con 2 と Windows の間に挟むやり方。Joy-Con 2 ↔ nRF52840 ↔ USB HID ↔ Windows、というルートで Windows からはふつうの USB マウスに見える。

良くできている。が、5,000 円弱の専用ドングルを買ってファームを焼く必要がある。

## 「ドングル要らなくない？」

ここで素朴な疑問が出る。

**Windows は標準で BLE GATT の API（WinRT）を持っている。Joy-Con 2 と直接 Bluetooth でつなげば、ドングルなしで maruta と同じことができるんじゃないか？**

maruta のソースを読むと、やっていることは:

1. Joy-Con 2 に **BLE GATT で接続**
2. Nintendo カスタムサービスの **input notify characteristic を subscribe**
3. **enable_std / enable_ext** の 2 つのコマンドを交互に書き込む
4. 60 byte の入力パケットが届きはじめる
5. ボタン bitmap・スティック・光学センサー・ジャイロをパースして USB HID マウスとして送出

このうちドングルが必要なのは「**USB HID マウスとして OS に見せる**」部分だけ。Windows なら `SendInput` という Win32 API でユーザー空間からマウスイベントを生成できるので、**ドングルはいらない**。Windows の Bluetooth スタックで Joy-Con 2 とペアして、WinRT BLE で input を読んで、`SendInput` で OS に流し込む。**全部ソフトウェア完結**。

これがコミュニティ初の software-only Switch 2 Windows ドライバになりそうなら、書き残しておく価値がある。

## 開発環境

しゅん先生 PC（Windows 11 Insider Preview、i7-8700K + 16GB）で開発する。Mac から Tailscale + SSH でほぼ全部リモート操作できるので、Joy-Con 2 のペアリング以外は手元で作業できる。

スタックはこう:

| レイヤ | 選択 |
|---|---|
| 言語 | C# / .NET 8 |
| BLE | `Windows.Devices.Bluetooth.GenericAttributeProfile` (WinRT) |
| HID 注入 | `SendInput` Win32 API (P/Invoke) |
| 開発環境 | VS Code + C# Dev Kit |
| 配布 | `dotnet publish` の single-file exe |

VS Code を選んだのは、Visual Studio 2022 のフルセットが要らないから。dotnet build / run / test の CLI と、軽い editor + debugger があれば十分。

## Phase 1: プロトコル仕様を Markdown に書き起こす

reverse engineering プロジェクトは、参照実装のコードを読むときに「**仕様書を再構成する**」のが第一歩だ。maruta の `src/main.c` を頭から読んで、`docs/projects/joycon2-protocol.md` に英語版仕様書を書いた。要点だけ:

### GATT UUID 3 つ

| 役割 | UUID |
|---|---|
| Nintendo Service | `ab7de9be-89fe-49ad-828f-118f09df7fd0` |
| Input Notify | `ab7de9be-89fe-49ad-828f-118f09df7fd2` |
| Write (別 service) | `649d4ac9-8eb7-4e6c-af44-1ea54fe5f005` |

### Input enable コマンド

```
0x0c 0x91 0x01 0x02 0x00 0x04 0x00 0x00 0xff 0x00 0x00 0x00   # std
0x0c 0x91 0x01 0x04 0x00 0x04 0x00 0x00 0xff 0x00 0x00 0x00   # ext
```

接続後 300ms 間隔で交互に数回送る。これで 60 byte のパケットがバンバン降ってくる。

### 60 byte パケット構造

| Offset | 内容 |
|---|---|
| 4-6 | ボタン 24-bit bitmap |
| 10-15 | スティック (12-bit packed) |
| 16-19 | 光学センサー X/Y (int16 LE 累積カウンタ) |
| 54-55, 58-59 | ジャイロ X / Z (int16 LE) |

12-bit packed 部分は最初混乱したが、こう取る:

```c
uint16_t lx = p[10] | ((p[11] & 0x0f) << 8);
uint16_t ly = (p[11] >> 4) | (p[12] << 4);
```

ボタン bit position は 22 個。Y=0、X=1、B=2、A=3、SR/SL/R/ZR が 4-7、…、HOME=12、CAPT=13、**C=14（Switch 2 の新ボタン）**、十字キー DOWN/UP/RIGHT/LEFT が 16-19。

光学センサーは「絶対累積カウンタ」になっていて、毎フレーム前回値との差分を取って初めて「今このフレームでどれだけ動いたか」が分かる。これは Switch 2 のマウスモードがハードウェアレベルで「机上の総移動距離」をトラッキングしている証拠で、なかなか頭がいい。

## 次回

ここまで仕様の地図ができた。明日は **C# WinRT で実際に Joy-Con 2 とハンドシェイクしてみる**。BLE のペアリング、サービス解決、enable コマンド送信、パケット受信、パースして「ボタン押下が C# 側に届く」までの瞬間を書く。

実機で動かすと、想定外のことが必ず起きる。ペアリングしただけで Switch 2 との bond が壊れたり、Bluetooth advertisement に LocalName が含まれてなくてスキャンが効かなかったり。そういうのを書いていきたい。

Apache 2.0 で OSS 化予定。リポジトリは `wirelessml/joycon2-mouse-windows`（公開時更新）。

---

#Switch2 #JoyCon #Windows #BLE #リバースエンジニアリング #個人開発
