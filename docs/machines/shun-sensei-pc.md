# しゅん先生 PC

> Last updated: 2026-04-22
>
> 🎉 **4/29 16:30 完全復活**: Acer FA100 512GB NVMe Gen3 x4 へのクローン移行成功（実質 ¥10,267 はばタンPay+ 50% プレミアム適用）。CDM 3,374 MB/s で公称超え、Plextor 時代の速度に復帰。3 時間のクローン死闘の真犯人は `stornvme\StartOverride\0=0x3` だった。詳細 @docs/journal/2026-04-29.md
>
> 旧履歴: 4/22 18:20 Plextor SSD NVMe コントローラ死亡 → Seagate クローン延命 7 日 → 4/29 Acer FA100 移行

## 役割

**コワーキング据え置き新メイン作業機**（4/22 16:34〜）
- 配置: コワーキングスペース据え置き
- 主用途: Windows メイン作業機、OBS・画像処理等の重い作業向き（4/29 NVMe 移行完了で重作業も解禁、SMR HDD 制約は解消）
- **代替不可能な専用機能**: **4K UHD Blu-ray 再生** — 家庭内 (M1 MacBook Air / iPhone 15 Pro / iPad Pro 9.7 / MASU-P55) で唯一対応。Intel SGX (第 7-10 世代 Core 限定) + UHD Friendly Drive (Pioneer BDR-211JBK) + UHD 対応 iGPU + HDCP 2.2 のスタックが揃った最後の機。**Ryzen / Intel 第 11 世代以降では SGX 削除のため永久に不可**、Apple Silicon は macOS 自体が UHD BD 未対応で構造的に不可 (詳細はケース・光学ドライブセクション参照)
- 所属: 個人所有（旧: 伊丹市はりきゅう整体しゅん業務用）
- 旧名/由来: はりきゅう整体しゅん（伊丹市）の業務用 PC だったものを譲渡

## ハードウェア

- **PC 名**: DESKTOP-ATQ36KS
- **モデル**: iiyama STYLE Infinity by iiyama（2018 年頃購入 BTO デスクトップ）
- **製造元**: 株式会社ユニットコム（0570-550-884）
- **CPU**: Intel Core i7-8700K @ 3.70GHz（6C12T、第 8 世代 Coffee Lake、2017/10 リリース、95W TDP、OC 可）
- **RAM**: **2x8GB = 16GB DDR4-2666**（デュアルチャンネル動作、15.8GB 使用可能、同ロット）
- **GPU**: Intel UHD Graphics 630（iGPU のみ、dGPU なし）
- **モニター**: LG 製（型番不明、デスクトップ設置）

## ストレージ

- 合計: 2.34TB（**新 C: Acer FA100 512GB NVMe + D: Seagate 2TB SMR HDD**、4/29 移行後構成）
  - Plextor 256GB は 4/22 死亡 → 4/24 物理除去
  - 4/27 Acer FA100 購入 → 4/29 クローン移行で C: 復帰、Seagate は D: バックアップへ降格

### C: Acer SSD FA100 512GB NVMe（🎉 2026-04-29 移行成功、現用ブートドライブ）

- **モデル**: Acer FA100 512GB（M.2 2280、PCIe Gen3 x4 NVMe）
- **コントローラ**: NVM Express 1.4 対応
- **ファームウェア**: GTdf62a6
- **シリアル**: ASAD35340100405
- **健康状態**: 100%（CDM 4/29 計測時）
- **温度**: 42°C（負荷時）
- **使用容量**: 213 GB / 477 GB（クローン後）
- **TRIM**: 有効（NTFS DisableDeleteNotify=0）
- **実測速度（CrystalDiskMark 9.0.2、4/29 16:35）**:
  - SEQ1M Q8T1 R/W: **3,374.22 / 2,826.92 MB/s**（公称 3,300/2,700 を超過）
  - SEQ128K Q32T1: 3,365.46 / 2,795.35 MB/s
  - RND4K Q32T16: 1,857.87 / 1,288.90 MB/s
  - RND4K Q1T1: 57.67 / 124.36 MB/s
- **PCIe レーン**: 3.0 x4 接続確認（理論値 3,940 MB/s に対して 85% efficiency）
- **購入経緯**: 2026-04-27 18:20 大西ジム新長田で店頭価格 ¥15,400、はばタンPay+ 第 5 弾 50% プレミアム適用で**実質 ¥10,267**
- **クローン経緯**: 2026-04-29 13:45-14:30 Hasleo Backup Suite Free で Seagate HDD → Acer SSD クローン
- **起動失敗 → 復活**:
  - 14:35 0xc0000001 で起動失敗
  - 15:15 chkdsk bitmap 修復後 0x7B INACCESSIBLE_BOOT_DEVICE
  - 15:45 真犯人 `stornvme\StartOverride\0 = 0x3` 発見（Windows 隠し最適化）
  - 15:48 `reg delete` 一行で起動成功

### ~~旧 C: Plextor PX-256M8PeGN 256GB NVMe~~（🪦 4/22 死亡 → 4/24 物理除去 → 4/29 後継 Acer FA100 移行で完全交代）

**4/22 18:20 死亡、デバイス検出不可（Get-Disk から消滅）**
**4/24 朝 物理除去完了**、現物はユーザー手元で保管中

#### 現物ラベル確認（2026-04-24）

| 項目 | 値 |
|---|---|
| 正式モデル | **PX-256M8PeGN**（4/24 修正、旧記録 M9PeGN は誤り） |
| P/N | 3G01Y003119 |
| S/N | PC281010003 |
| FW | 1.03（最終版） |
| 容量 | 256GB |
| 製造日 | **2018/09/06** |
| 電源 | DC 3.3V 2.5A |
| NAND | Toshiba BiCS 3D TLC (TNBHLMBMCXBD.36V9) |
| コントローラ | Marvell 88SS1093 |
| フォームファクタ | M.2 2280 PCIe Gen3 x4 NVMe |
| 原産国 | Taiwan |

#### 生前の稼働状況
- 使用 130GB
- 健康状態「正常 66%」（寿命残 66% / 消費 34%）
- 総書込 69TB（TBW 公称 160 の 43%、余裕あり）
- 使用時間 **26,779h = 3.06 年通電**
- 製造から死亡まで **7 年 7 ヶ月経過**
- 死因: WHEA_UNCORRECTABLE_ERROR 0x124 + stornvme Event 11 → 完全応答停止
- **推定死因**: TBW 余裕あり → **経年劣化（電解コン or コントローラ半導体）** が主因

#### ブランド状況
- Plextor 事業撤退済（2024 年 KIOXIA 傘下で SSD 撤退）、サポートなし
- 現物の廃棄時は **データ完全消去 or 物理破壊**推奨（256GB に個人データ含有の可能性）

#### 現在の M.2 スロット状況
- **物理的に空**、スタンドオフ + 固定ネジは残置（紛失注意）
- 新 NVMe SSD 購入後、即装着可能な状態
- 将来の換装作業: スロット挿入 → ネジ固定 → Hasleo で Seagate → 新 SSD クローン（18 分） → BIOS Boot 順変更 → 起動、の経路が確定

### Seagate ST2000LM015-2E8174 2TB SMR HDD（旧 C: 緊急稼働 → 旧 D: バックアップ → 2026-04-26 取り外し）

- インターフェース: SATA/600
- 回転数: 5400rpm、2.5 インチ
- Hasleo クローン（4/22 17:15-17:34）により起動可能な完全複製を保持していたため、Plextor 死亡後の強制再起動で自動的に Boot Manager が Seagate にフォールバック
- 役割の変遷:
  - 〜4/22 18:20: D: バックアップドライブ
  - 4/22 18:20〜4/25: C: として緊急稼働（Plextor 死亡後の自動フォールバック、Windows 11 25H2 起動、体感 50-100 倍遅い SMR HDD ハング）
  - 4/25〜4/26: D: バックアップに復帰（SanDisk Extreme V2 USB-C SSD への OS 移行完了で C: を譲渡）
  - 4/26: 静音化のため物理取り外し
- 4/24 時点の SMART:
  - 健康状態 正常
  - 使用時間 23,722h
  - 電源投入 20,759 回
  - 温度 27°C
- バックアップイメージ: `D:\Backup\Weekly System Image\Weekly System Image.adi` = 84.9GB（4/22 18:05 作成の AOMEI システムイメージ、4/26 取り外し時に B 案: 外付け USB-SATA ケース移植 で .adi 救出）

#### 現物ラベル確認（2026-04-26）

| 項目 | 値 |
|---|---|
| 正式モデル | **ST2000LM015** |
| シリーズ | Seagate BarraCuda Compute |
| P/N | 2E8174-500 |
| S/N | WDZCZBLY |
| WWN | 5000C500B93C80A3 |
| FW | SDM1 |
| 容量 | 2TB |
| 製造日 | **2018-02-28**（製造から 8 年経過、保証切れ済み） |
| 製造拠点 | WU（中国 無錫） |
| 電源 | +5V 1.0A（2.5 インチなので +12V 不要） |
| Reg. Model | SDC003 |
| フォームファクタ | 2.5 インチ SATA、SMR |
| **PSID** | `Z6GM4PGW 0RYZMQFY AFYNZG3R 77D72Z6U` |
| 認証元 | Seagate Singapore Int'l HQ Pte. Ltd. |
| 原産国 | China |
| 認証マーク | UL E190397 / TÜV SÜD / KC MSIP-REM-STX-SDC003 / CE / RoHS |

> **PSID（Physical Secure ID）の重要性**: OPAL 自己暗号化ドライブの工場リセット用物理シリアル。紛失すると暗号消去（PSID Revert）ができなくなる。ケース封印を剥がすと保証無効化扱いになるので、**現物ラベルが手元にあるうちに記録**（4/26 撮影、本ドキュメントに永続化）。

> **2026-04-26 取り扱い決定**: B 案（外付け USB-SATA ケースに移植）を採用。Plextor 死亡時の予備復元手段として残す方針 — .adi 84.9GB の救出 + 外付け化で物理静音 + 内蔵スロット解放の 3 目的を同時達成。

## OS / ソフトウェア

- OS: Windows 11 Home **25H2**（build 26200.8037、2025/02/05 クリーンインスコ）
- Hasleo Backup Suite Free V5.6.2.1（クローン用）
- AOMEI Backupper Standard（週次システムイメージ用、毎週日曜 04:00 自動実行）

## ネットワーク

- **デュアル LAN 構成**（4/24 背面写真で確認、2x RJ45 ポート）
- ローカル IP (DHCP): **192.168.2.187** (2026-05-01 時点、過去 192.168.2.174 → 187 と変動あり、DHCP リース更新で変わる)
- MAC アドレス: `D4:25:8B:30:F5:D4` (Intel Wireless-AC 8265、Wi-Fi 5 5GHz、約 60/60 Mbps)
- インターフェース名: `irukasensei` (= いるか先生、ローマ字命名のカスタム alias)
- Wi-Fi: YKSmas318 (コワーキング MASU-p)
- ホスト名 (Windows): **DESKTOP-ATQ36KS** (デフォルト命名、変更未実施)
- Windows ユーザー名: **wirel** (Administrators グループ所属)
- **Tailscale: 不採用（5/2 朝確定）**。LAN 経由 SSH のみで運用。LAN 外（自宅・別コワーキング等）から接続したい場合は M1 を中継して Mac→Tailscale→（必要なら）別経路、しゅん先生 PC は MASU-p の同 Wi-Fi 内でのみ到達可能。masu-p55 (HP ProBook) は Tailscale 100.125.21.47 で参加してるので、必要なら masu-p55 経由 SSH ホップで間接到達は可能
- リモート操作: **SSH 設定完了 (2026-05-01 06:35 JST)**

### SSH 接続情報

- **接続コマンド (M1 Mac から)**: `ssh shun-sensei` (~/.ssh/config に alias 設定済)
- **直接コマンド**: `ssh wirel@192.168.2.187`
- 認証: 公開鍵 (ed25519、M1 の `~/.ssh/id_ed25519` を使用、公開鍵 `yuika@macbook-air-claude-desktop`)
- パスワード認証: 有効 (フォールバック、パスワードは別管理)
- sshd: Running / Automatic、OpenSSH for Windows 9.5
- ファイアウォール: OpenSSH-Server-In-TCP / Profile=Any (重要: 初期設定では Private only で外部から到達不可だったため Any に変更済)
- 公開鍵保管場所: `C:\ProgramData\ssh\administrators_authorized_keys` (Windows OpenSSH の Match Group administrators 仕様により、~/.ssh/authorized_keys ではなくこちら)
- 注意: DHCP で IP 変動あり（5/1 → 5/2 朝で変わった実績）、**Tailscale 不採用方針なので mDNS 解決一本**。mDNS hostname: `DESKTOP-ATQ36KS.local`（`dscacheutil -q host -a name DESKTOP-ATQ36KS.local` で IP 取得）。固定 IP 化はルーター側 DHCP reservation で別途対応可

### SSH 経由でのデフォルトシェル

- デフォルト: `cmd.exe` (セミコロン `;` でコマンド連結不可、`&` を使う)
- 推奨実行方式: `ssh shun-sensei 'powershell -NoProfile -Command "..."'`
- 文字化け対策: `chcp 65001` で UTF-8 化 or PowerShell 経由
- デフォルトシェルを PowerShell に変更したい場合は `C:\ProgramData\ssh\sshd_config` の `Subsystem` セクション or レジストリ `HKLM:\SOFTWARE\OpenSSH\DefaultShell` を設定

## ケース・光学ドライブ（2026-04-24 写真確認）

- **ケース**: Cooler Master 製（iiyama ブランディング貼付、Mini-Tower 級）
  - 全面メッシュパネル（エアフロー良好）
  - 天面に 5.25" 光学ドライブベイ
- **光学ドライブ**: **Pioneer BDR-211JBK**（2017 年 9 月製造、Made in China、日本市場上位モデル）
  - Pioneer Digital Design Corporation（越谷市）設計
  - 4K UHD Blu-ray 再生対応
  - BDXL 書込（最大 128GB クアッド層）
  - M-DISC 対応（1000 年保存ディスク）
  - BD 16x / DVD 24x 書込速度
  - 電源: 12V 2.2A + 5V 1.4A
  - 当時定価 ¥25,000-30,000、2026 年現在中古 ¥15,000-20,000 相当
  - **現時点で代替入手困難な希少機材**
  - **4K UHD BD 再生の動作要件 (このマシンで全要件が揃った希少構成)**:
    - CPU: i7-8700K (第 8 世代 Coffee Lake、**Intel SGX 対応**) ✓
    - iGPU: UHD Graphics 630 (HDCP 2.2 + UHD BD ハードウェアデコード対応) ✓
    - 光学ドライブ: Pioneer BDR-211JBK (UHD Friendly Drive) ✓
    - 再生ソフト: **PowerDVD 14.0.1.7320 UHDBD-OEM 版** (DD 6ch + DTS 6ch、ライセンス先 **UNITCOM PC User**、SR: MES161202-01、TR: TR170120-035) ✓ — **iiyama STYLE Infinity 2018 BTO の標準バンドル**として最初から入っていた (購入不要、再買い直し不要)。対応: Ultra HD 4K / Blu-ray / BD3D / BDXL / AVCHD / AVCREC / CPRM / Dolby TrueHD / DTS-HD / Direct 24/96 / TrueTheater / Java。アップグレード案内 (PowerDVD 24) が出るが UHD BD 再生は v14 で十分、UHDBD-OEM ライセンスのアップグレード可否は別途要確認 (一般に OEM 版から上位版への引継は不可、買い直しになる)
    - モニタ: **LG 40WP95C-W** (39.7 インチ 5K2K ウルトラワイド、Thunderbolt 4 + DP 1.4 + HDMI 2.0 ×2、全入力 **HDCP 2.2 対応** ✓) — 元 Mac 接続用、4/30 から GC313Pro 経由で Windows しゅん先生 PC へ切替
  - **CPU 換装の天井制約**: 4K UHD BD 機能を維持できる CPU は **i9-9900K まで** (第 10 世代 Comet Lake はマザボ LGA1151 v2 非対応、**第 11 世代 Rocket Lake 以降は Intel が SGX を削除したため 4K UHD BD 再生不可**)。**Ryzen への乗り換えは AMD が SGX 非対応のため永久にこの機能を失う** ← Ryzen 移行検討時の決定的な NG 根拠
- **PSU**: **FSP 500W**（型番 FSP500-50 EKEN 系列、80 PLUS 認証、Active PFC、Whisper Killer 静音設計）
  - +12V 38A (456W) 、+3.3V 24A、+5V 38A
  - **トップマウント**（旧型レイアウト、2017-2018 年の廉価〜中級 mATX ケースでは標準）
  - RTX 4060 クラス（115W 前後）までの dGPU 追加が PSU 交換なしで可能
  - RTX 4070 Ti 以上や dGPU + CPU OC 併用時は 650-750W クラスへ換装必要
- **マザーボード**: **BIOSTAR 製**（EzpReady マーキング確認、2026-04-24）
  - 有力候補: **BIOSTAR RACING Z370GT3**（mATX、デュアル LAN、EzpReady 搭載モデル）
  - 正確な型番は `wmic baseboard get product,manufacturer` で確認要（明日の実機で実行）
  - CLRTC（Clear CMOS）ジャンパ確認済、BIOS 異常時のリセット手段あり
- **CPU クーラー**: Intel 純正相当（LGA1151 stock cooler、small heatsink + 小口径ファン）
- **PCIe x16 スロット**: 空（dGPU 非搭載、iGPU のみ）
- **RAM スロット**: 2 本装着（E0D55E2F5A68 / E0D55E2F5A6A、同ロット、4/24 再読で訂正）
- **M.2 スロット**: 1 つ確認、**Acer FA100 512GB NVMe 装着中**（4/29 設置）
- ~~mSATA or M.2 モジュール 緑 PCB 2 枚重ね~~ → 4/24 朝の別角度写真で判明、正体は **RAM DIMM を斜めから見たもの**（mSATA ではない）
- **内部清浄度**: 埃堆積あり、物理作業前に清掃推奨

## I/O ポート（2026-04-24 写真確認）

### 背面
- DisplayPort × 1
- HDMI × 1
- RJ45 Ethernet × **2**（デュアル LAN、ワークステーション仕様）
- **USB 3.0 Type-C × 1**（**5 Gbps 上限**、i7-8700K + Z370 PCH ネイティブが USB 3.1 Gen 1 止まりのため）
- USB 3.0 Type-A × 2（青色、5 Gbps）

### 前面
- USB 3.0 Type-A × 2（青色、5 Gbps）
- 3.5mm ヘッドホンジャック × 1
- 3.5mm マイクジャック × 1
- 電源 LED / HDD アクセス LED

### USB 外付け SSD 速度の天井
- USB-C 接続でも **実効 ~400-500 MB/s** が上限（プロトコル制約）
- SanDisk Extreme Portable SSD（公称 1,050 MB/s）を繋いでも 10 Gbps 性能は出ない
- 将来 10 Gbps 欲しければ PCIe 増設カード（ASMedia ASM3142 系）または Z390 以降のマザボ換装が必要
- ただし Seagate HDD (100-150 MB/s) 比では **3-5 倍速**あるので SanDisk クローン作戦は有効

## 周辺機器

### キーボード: LITEON UCL111UBK1（2026-04-30 写真確認）

- **メーカー**: LITEON（台湾 OEM 大手）
- **流通**: ユニットコム経由でパソコン工房店舗から **iiyama PC バンドル品** として出荷
  - PowerDVD 14 UHDBD-OEM（UNITCOM PC User ライセンス）と同じく iiyama STYLE Infinity 2018 BTO の出荷時セット
- **配列**: 日本語 111 キー
- **接続**: USB 有線（ケーブル長約 1m）
- **スイッチ**: メンブレン
- **キーピッチ**: 19mm（フルサイズ）
- **キーストローク**: 3mm（浅め、軽タッチ）
- **サイズ**: 445 × 140 × 22mm（足展開時）
- **電源**: DC 5V 100mA（USB バスパワー）
- **S/N**: KB7443AA
- **製造**: Made in China
- **市場流通**: メルカリ・ヤフオク等で数百〜数千円、単体新品入手は困難（バンドル流通のみ）

## 変更履歴

- **2026-04-30 12:40**: 周辺機器セクション新設、付属キーボードを **LITEON UCL111UBK1** と特定（写真ラベル + Web 検索）。PowerDVD と同じく iiyama BTO バンドル品、ユニットコム/パソコン工房ルートの 2018 年出荷時セットの一部であることが確定
- **2026-04-30 12:30**: 4K UHD BD 再生スタックを完全確定 — PowerDVD 14.0.1.7320 UHDBD-OEM (UNITCOM ライセンス、iiyama BTO 標準バンドル、SR: MES161202-01) と LG 40WP95C-W モニタ (HDCP 2.2 対応) を実機スクショで確認、shun-sensei-pc.md の「要確認」記述を確定値に置換 (ユーザー提供写真ベース)
- **2026-04-30 12:20**: 4K UHD BD 再生機能を「代替不可能な専用機能」として役割セクションに昇格、CPU 換装天井 (i9-9900K まで) と Ryzen 移行不可の根拠を光学ドライブ項目に追記 (将来の機材判断ミス防止 memo、ユーザー指摘ベース)
- **2026-04-26 朝**: Seagate D: 物理取り外し（B 案: 外付け USB-SATA ケース移植）、ラベル現物撮影で全スペック記録（PSID 含む、@docs/machines/shun-sensei-pc.md の現物ラベル確認セクション参照）
- **2026-04-25**: SanDisk Extreme V2 USB-C SSD 2TB へ OS 移行完了、Windows 11 起動成功（13:18、CSM 無効 + XHCI Hand-off 有効）、SanDisk Dashboard 5.2.2.3 でヘルスモニタリング体制確立（詳細: @docs/journal/2026-04-25.md）
- **2026-04-29 16:30**: 🎉 **Acer FA100 NVMe 移行完了** — Hasleo クローン → 0xc0000001 → bcdboot 確認 → chkdsk bitmap 修復 → 0x7B → `stornvme\StartOverride\0=0x3` 削除で起動成功、CDM 3,374 MB/s で公称超え（詳細: @docs/journal/2026-04-29.md）
- **2026-04-27 18:20**: 大西ジム新長田で Acer FA100 512GB NVMe 購入、はばタンPay+ 50% プレミアムで実質 ¥10,267
- **2026-04-24 朝**: 死亡 Plextor を物理除去、ラベル確認で正式モデル **PX-256M8PeGN**（旧記録 M9PeGN は誤り）、製造 2018/09/06 判明、M.2 スロット空き状態に
- **2026-04-22 18:20**: Plextor SSD 死亡、Seagate クローンで緊急起動（詳細: @docs/journal/2026-04-22.md）
- 2026-04-22 17:34: Hasleo でクローン完成（命綱）
- 2026-04-22 16:34: コワーキングに配置転換、新メイン化
- 2025-02-05: Windows 11 Home 25H2 クリーンインストール
- 2018 年頃: ユニットコム STYLE Infinity として購入

## ~~新 SSD 購入計画~~（2026-04-27 完了、2026-04-29 移行成功）

> **以下は履歴として保存**。Acer FA100 購入と移行で計画完遂。

### 購入完了記録

- **2026-04-27 18:20**: 大西ジム新長田で Acer FA100 512GB を購入
- **店頭価格**: ¥15,400（NAND 高騰下、4/22 比 9.4% 値上げ目撃）
- **実質支払**: **¥10,267**（はばタンPay+ 第 5 弾 50% プレミアム適用）
- **目標 ¥12,000 以下達成**

### 当時の購入計画

**現在は購入保留**（2026 年 NAND 高騰、1TB NVMe が ¥20,980 から）

### 発動トリガー
- 1TB NVMe が ¥12,000 税込以下になったら発注検討
- または Seagate HDD の体感速度に耐えられなくなったら

### 候補モデル
- Hanye MN50 1TB（現最安、Amazon 直販 B0B58JKLLW）
- KIOXIA EXCERIA G2 1TB（SSD-CK1.0N3G2/N、Plextor と NAND 同系）
- Crucial P3 Plus 1TB（在庫のみ、Micron 撤退で将来確保困難）
- WD Black SN770 1TB（WDS100T3X0E、Gen4 高速）

### 換装手順（SSD 到着後）
1. しゅん先生 PC シャットダウン → ケース開ける
2. 死亡 Plextor を M.2 スロットから抜く → 新 SSD を同スロットに挿入
3. Seagate HDD から起動（今と同じ）→ Hasleo で Seagate → 新 SSD にクローン（18 分）
4. BIOS で新 SSD を Boot 1st → 再起動
5. Seagate は今後のバックアップ用 D: として継続利用

## 関連ファイル

- 運用ルール: @docs/rules/operations.md
- SSD 価格監視: @docs/routines/ssd-price-monitor.md
- Plextor 死亡詳細: @docs/journal/2026-04-22.md
- バックアップ設定詳細: @docs/journal/2026-04-22.md
