# Plextor が死んでから 72 時間、USB-C SSD で Windows を蘇らせるために BIOS と 6 時間半殴り合った話

---

## 発端は 4 月 22 日の深夜だった

3 日前の話だ。コワーキングスペースに据え置きしているメイン機 — 通称「しゅん先生 PC」— の Plextor M9PG+ 1TB が、突然死した。

NVMe コントローラ障害。前触れゼロ。SMART は健康満点を最後の瞬間まで返していた。救いは、その 2 時間前にたまたま AOMEI Backupper で Seagate ST2000LM015 (SMR HDD) にクローンを取っていたことだった。クローンが命綱になり、Seagate から起動して延命運用に入った。

ただし SMR HDD は遅い。書き込みが詰まると 2 分間ハングする。Windows Update が走ると死んだフリをする。ファイルコピーすら気が遠くなる。「とりあえず動いている」だけの状態だった。

NAND フラッシュ価格は 2026 年に入ってから高騰している。1TB NVMe が ¥20,980 から。Plextor と同等のものを買い直す気にはなれない。

そこで思い出したのが、引き出しに眠っていた **SanDisk Extreme V2 Portable SSD 2TB**（USB-C、2025 年 8 月製造）だった。

「USB-C SSD から Windows ブートできるなら、これで延命できるんじゃないか？」

技術的には可能なはずだ。Microsoft も「Windows To Go」の文脈で USB ブートを公式にサポートしていた時代があった（廃止されたが）。世の中には「外付け SSD から起動する Windows」というジャンルがちゃんと存在する。

朝 6 時 37 分。手を動かし始めた。

---

## 第一層: クローンと Boot Critical 化

まず Plextor → SanDisk USB-C SSD への引っ越し。Clonezilla Live Stable で内蔵 SSD を USB-C SSD にまるごと書き写す。これは 1 時間ほどで終わった。

問題はその後だ。Windows は内蔵ストレージから起動する前提で組まれているので、USB バスから起動するためには **OS 側にも「自分は USB から起動する」と教える必要がある**。

具体的には次の手順を踏んだ:

- Windows USB Services の `Start=0`（Boot Critical）化
- USB Driver の Boot Critical 化
- レジストリの `PortableOperatingSystem` フラグセット
- `BCD Rebuild`（Boot Configuration Data の再生成）
- `MountedDevices` レジストリリセット

これは「USB バスを起動最初期段階で初期化しろ」と Windows に強制する作業だ。普段は内蔵 SATA / NVMe しか相手にしない USB スタックを、ブートストラップの一部に格上げする。

ここまでは 11 時 38 分に完了した。約 5 時間。レジストリを叩く順番ひとつ間違えるとやり直しになる地味な作業を、ひたすら積み上げる時間。

---

## 第二層: 物理層の沈黙

そして本番が始まった。**BIOS 設定**だ。

しゅん先生 PC のマザーボードは GIGABYTE Z370N WIFI（2017 年）。Intel 第 8 世代 Core i7-8700K 用。9 年前のボードだ。BIOS は UEFI 対応だが、設定項目が膨大で、USB-C SSD ブートを通すには複数の設定を「正解」に揃える必要がある。

12:07、最初の試行。ブートメニューに USB-C SSD は出るのに、選択しても画面が真っ黒のまま戻ってくる。BIOS POST すら通らない瞬間もある。

12:30、BIOS アップデートを検討。WinToUSB（USB ブート専用 Windows を作るツール）への乗り換えも検討。「これは詰みかもしれない」という空気が流れる。

13:02、転機が来た。BIOS の片隅に **CSM サポート（Compatibility Support Module）** という設定を発見した。CSM は古い MBR 形式の OS と UEFI を共存させるための互換レイヤーだ。これが「有効」になっていた。

UEFI ブートの GPT パーティションでクローンを作っているのに、CSM が有効だと BIOS が「どっちで起動すればいい？」と迷子になる。**CSM 無効化、UEFI Only に固定**。

進展はあった。だがまだ起動しない。

13:07、もうひとつの設定にたどり着いた。

> **XHCI Hand-off — Disabled**

XHCI Hand-off は、BIOS が握っていた USB 3.0 コントローラの所有権を OS に「引き渡す」機能だ。これが無効だと、BIOS は USB-C デバイスを「BIOS 専用」のまま握り続け、OS から見えなくなる。

つまり、**BIOS POST 中はブートメニューに USB-C SSD が見えていたのに、Windows ブートローダが起動した瞬間に USB バスごと消失していた**。これが root cause だった。

XHCI Hand-off を有効化。Secure Boot の Violation 検証も済ませて、構成確定。

---

## 13:18 — 起動成功

**6 時間 41 分**。Windows 11 のロゴが、SanDisk Extreme V2 から立ち上がった。

GIGABYTE Z370N WIFI で USB-C SSD からブートする条件は、最終的にこうなった:

| 設定項目 | 必須値 | 役割 |
|---|---|---|
| CSM サポート | **無効** | UEFI のみに固定 |
| XHCI Hand-off | **有効** | USB-C を OS に引き渡す（最重要） |
| Secure Boot | 適切な署名 boot loader | 改ざん防止 |

XHCI Hand-off 一行で 6 時間溶けた、と言っても過言ではない。BIOS の設定項目は 100 を超える。そのうちのひとつが、USB-C SSD ブートの根幹を握っていた。古いマザーボードの BIOS 設定にデフォルトで罠が仕込まれているわけだが、そもそも 2017 年のボードに「USB-C SSD からブートする想定」がなかったというだけの話だ。

これで終わったと思った。

---

## 二次戦: ファームウェアの壁

起動成功の余韻もそこそこに、ヘルスチェックのために **CrystalDiskInfo 9.8.0** を立ち上げた。SSD の SMART 値を読んで寿命と異常を確認する、Windows 環境の事実上の標準ツールだ。

画面を見る。

> Seagate ST2000LM015（D: ドライブ）— 表示される
> SanDisk Extreme V2（C: ドライブ）— **表示されない**

C: ドライブは今まさに OS が走っている SSD だ。それが認識されない。

理由はすぐに見当がついた。SanDisk Extreme V2 の中身は、**ASMedia ASM2362 USB-NVMe ブリッジ + 内部 NVMe SSD** という構成になっている。USB の向こうに NVMe SSD がいて、ブリッジ IC が翻訳している。

NVMe の SMART 取得は **NVMe Admin Command** という独自プロトコルで行う。USB Mass Storage の SCSI コマンドではない。だから USB を介す場合、ブリッジ IC が「SCSI コマンドを NVMe Admin Command に翻訳する」（SAT, SCSI/ATA Translation）役目を果たす必要がある。

ところが ASM2362 の SAT 実装は独自仕様で、汎用ツールから素直に SMART が取れないことで有名だ。USB Mass Storage / UAS のデータ転送は完璧、だが SMART だけ詰まる。

---

## 第三層: CrystalDiskInfo 設定地獄

CrystalDiskInfo には「これでもか」というほど USB-NVMe ブリッジ対応のツマミが並んでいる。**3 段階の有効化が必要**だ。

```
機能 → 上級者向け機能
  ├── アドバンスドディスクサーチ              [ON]
  ├── ATA_PASS_THROUGH                        [ON]
  ├── USB/IEEE 1394                            [ON] ← 本命と思われた
  └── USB/IEEE 1394 配下の翻訳ドライバ
      ├── SCSI_ATA_TRANSLATION (SAT)         [ON]
      ├── I-O DATA / Sunplus / Logitec        [ON]
      ├── Prolific / JMicron / Cypress        [ON]
      ├── ASMedia ASM1352R                    [ON]
      ├── Realtek RTL9220DP                    [ON]
      ├── JMicron JMS56X / JM839X / JMS586    [ON]
      ├── USB Memory (SAT)                     [ON]
      ├── SCSI_NVME_TRANSLATION (ASMedia/Phison) [ON] ← ASM2362 担当
      └── SCSI_NVME_TRANSLATION (Realtek)     [ON]
```

全部 ON にした。**それでも SanDisk Extreme V2 は出てこない**。

CrystalDiskInfo のバージョン履歴を遡ってみた。USB-NVMe ブリッジ対応は地道に拡張されてきている:

- 8.1.0 Beta1: ASMedia ASM2362 サポート改善
- 9.5.0 (2024-11): JMicron JMS586 強化
- 9.6.0 (2025-02): Phison USB-NVMe ブリッジ追加
- 9.7.0 (2025-06): Realtek RTL9220DP 修正
- 9.7.1 (2025-07): SanDisk SSDs サポート拡張
- 9.7.2 (2025-08): Seagate SSD 強化
- **9.8.0 (2026-02): バグ修正のみ ← いま使ってる版**

最新版の 9.8.0 を使っていた。「アップグレードで解決」の道は閉ざされていた。

---

## 14:15 — SanDisk Dashboard が 3 分で全部解決した

打開策は意外な場所にあった。**SanDisk 公式ツールの SanDisk Dashboard**。

公式ドキュメントには「外付けドライブの一部は非対応」と書いてある。Extreme V2 が対応リストに載っているかは明示されていなかった。博打。

Online Installer をダウンロード:

```
https://sddashboarddownloads.sandisk.com/wdDashboard/DashboardSetup.exe
```

3.1MB。3 秒でダウンロード。インストール。起動。

> **SanDisk Extreme 55DD（C: ドライブ）が即座に認識**

| 項目 | 値 |
|---|---|
| モデル | Extreme 55DD |
| 容量 | 2000.40 GB（2TB） |
| ファームウェア | **0010（最新）** |
| 健康状態 | **Normal** |
| 使用済み | 243.68 GB（12.2%） |
| TRIM | ✅ 有効 + 自動スケジュール |
| 書き込みキャッシュ | ✅ 有効（パフォーマンス向上モード） |

**3 分**。先ほどまで 1 時間格闘していた問題が、3 分で終わった。

ただし、温度センサーとインターフェース速度だけは「Failed to Load」「このデバイスではサポート対象外」と表示された。これは ASM2362 のファームウェア側の制約で、NVMe Get Log Page 経由でセンサー値を渡してこない仕様らしい。**どのツールを使っても物理的に取れない**。健康状態が Normal を出してくれるなら、温度ぐらいは妥協する。

---

## 学んだこと

72 時間でひととおり終わった。学びを残しておく。

**1. ASMedia ASM2362 USB-NVMe ブリッジの SMART は専用ツール必須**

CrystalDiskInfo 9.8.0（最新）を完全武装しても認識しない。smartmontools の `-d sntasmedia` も成功率は低いと報告されている。**SanDisk Dashboard が唯一の正解**。独自プロトコルで ASM2362 と通信する。汎用ツールでは越えられない壁がある。

**2. GIGABYTE Z370N WIFI で USB-C SSD ブートする条件**

CSM 無効 + XHCI Hand-off 有効 + Secure Boot 適切な署名。**XHCI Hand-off が一行で 6 時間溶かす犯人**。古いマザーボードで USB-C ブートを試す人へ、これだけは先に確認してほしい。

**3. Windows USB ドライバ Boot Critical 化は地道な積み重ね**

`Start=0` 設定 + USB Driver Boot Critical + `PortableOperatingSystem` フラグ + `BCD Rebuild` + `MountedDevices` リセット。これを順番通りやれば USB-C SSD ブートは通る。順番が大事。

**4. CrystalDiskInfo の USB バス検出には 3 段階の有効化が必要**

「アドバンスドディスクサーチ」+「USB/IEEE 1394」+「翻訳ドライバ全部 ON」。ただしブリッジ FW が独自プロトコルだと、これでも結局取れない。

**5. メーカー純正ツールは最後の砦**

汎用ツールが万能だと思い込まないこと。ブリッジ IC の独自実装には、メーカー純正ツールが独自プロトコルで応じる、という構図がある。Crucial には Storage Executive、Samsung には Magician、SanDisk には Dashboard。

---

## いちばん時間を食ったのは、OS よりも下の層だった

7 時間半の内訳を振り返ると、結論はひとつしかない。**時間を食ったのは全部、OS よりも下の層**だった。

第二層の BIOS 地獄 — XHCI Hand-off は OS からは触れないハードウェアの所有権スイッチだ。Windows がどれだけ正しく組まれていても、BIOS が USB バスを握ったままなら OS には届かない。OS から見えない層で沈黙されると、ソフトウェア側からは原因が特定できない。「動かない」という事実だけが残り、消去法で BIOS の 100 を超える設定項目を一つずつ試すしかなくなる。

二次戦の CDI も同じ構造だ。ASMedia ASM2362 のファームウェアが NVMe Admin Command を独自プロトコルでしか受け付けない。CrystalDiskInfo がどれだけ翻訳ドライバを増やしても、ブリッジ IC の FW が応じなければ会話が成立しない。ソフトの設定ツマミを全部 ON にして 1 時間溶かしたあと、メーカー純正ツールが 3 分で会話を成立させた。

ソフトウェアの問題はソフトウェアで殴り倒せる。ログを取って、コードを読んで、設定を変えて、再現させる。だが物理層とファームウェア層は黙って時間を食う。原因が見えないまま、消去法と試行錯誤で時間が溶けていく。**物理的な問題が、いちばん時間がかかる**。3 日かけて学んだのは、結局それだった。

---

## エピローグ

Plextor が死んだ 4 月 22 日深夜から 72 時間後、しゅん先生 PC は SanDisk Extreme V2 から Windows 11 を起動し、SMART ヘルスを正常表示する状態に復帰した。Seagate HDD は D: ドライブとしてバックアップ専用に降格。重い書き込みが詰まる SMR HDD ハングからも解放された。

体感速度は 3 〜 5 倍。USB-C 接続だが、Gen 2x1（10Gbps）の帯域は内蔵 SATA SSD を上回る。Plextor 同等の NVMe 内蔵 SSD を新品で買い直す費用はゼロ。

NAND 高騰の 2026 年に、引き出しに眠っていた USB-C SSD で延命できた。BIOS の罠と USB-NVMe ブリッジの SAT 翻訳問題に 7 時間半溶けたが、明日壊れても外付けケースから別の PC に繋ぎ直せる構成だ。内蔵 SSD よりむしろ可用性が高い。

死んだ Plextor は今も机の上に置いてある。NAND が高すぎる間は、こいつを買い直さずに済ませる工夫を続ける。

---

> **仲啓輔**
> 神戸でひとり開業を準備中。AI と古い PC とテキスト編集者の話を書いています。
> 前作: [Plextor が死ぬ 2 時間前にクローンを作った話](#)（4/22）
