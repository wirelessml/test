# しゅん先生 PC

> Last updated: 2026-04-22
>
> 🚨 **4/22 18:20 緊急事態発生**: Plextor SSD が NVMe コントローラエラーで完全死亡、Seagate クローンに自動フォールバック起動中（詳細は @docs/journal/2026-04-22.md）

## 役割

**コワーキング据え置き新メイン作業機**（4/22 16:34〜）
- 配置: コワーキングスペース据え置き
- 主用途: Windows メイン作業機、OBS・画像処理等の重い作業向き（※ ただし新 SSD 換装まで SMR HDD 起動のため重い作業は保留）
- 所属: 個人所有（旧: 伊丹市はりきゅう整体しゅん業務用）
- 旧名/由来: はりきゅう整体しゅん（伊丹市）の業務用 PC だったものを譲渡

## ハードウェア

- **PC 名**: DESKTOP-ATQ36KS
- **モデル**: iiyama STYLE Infinity by iiyama（2018 年頃購入 BTO デスクトップ）
- **製造元**: 株式会社ユニットコム（0570-550-884）
- **CPU**: Intel Core i7-8700K @ 3.70GHz（6C12T、第 8 世代 Coffee Lake、2017/10 リリース、95W TDP、OC 可）
- **RAM**: 16GB DDR4-2666（15.8GB 使用可能）
- **GPU**: Intel UHD Graphics 630（iGPU のみ、dGPU なし）
- **モニター**: LG 製（型番不明、デスクトップ設置）

## ストレージ

- 合計: 2.05TB → **1.82TB**（Plextor 256GB 死亡により喪失、Seagate 2TB のみ稼働）

### ~~C: Plextor PX-256M8PeGN 256GB NVMe~~（🪦 死亡 → 4/24 物理除去）

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

### C:（現在） = 旧 D: の Seagate ST2000LM015-2E8174 2TB SMR HDD

- インターフェース: SATA/600
- 回転数: 5400rpm、2.5 インチ
- Hasleo クローン（4/22 17:15-17:34）により起動可能な完全複製を保持していたため、Plextor 死亡後の強制再起動で自動的に Boot Manager が Seagate にフォールバック
- 現在の状態:
  - Windows 11 25H2 が Seagate から稼働中
  - 体感 50-100 倍遅い（SMR HDD 特性）
  - 健康状態 正常
  - 使用時間 23,722h
  - 電源投入 20,759 回
  - 温度 27°C
- バックアップイメージ: `C:\Backup\Weekly System Image\Weekly System Image.adi` = 82.94GB（4/22 18:05 作成の AOMEI システムイメージ）

## OS / ソフトウェア

- OS: Windows 11 Home **25H2**（build 26200.8037、2025/02/05 クリーンインスコ）
- Hasleo Backup Suite Free V5.6.2.1（クローン用）
- AOMEI Backupper Standard（週次システムイメージ用、毎週日曜 04:00 自動実行）

## ネットワーク

- **デュアル LAN 構成**（4/24 背面写真で確認、2x RJ45 ポート）
- Tailscale: 未導入（今後設定予定）
- リモート操作: SSH 未設定

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
- **PSU**: **FSP 500W**（型番 FSP500-50 EKEN 系列、80 PLUS 認証、Active PFC、Whisper Killer 静音設計）
  - +12V 38A (456W) 、+3.3V 24A、+5V 38A
  - **トップマウント**（旧型レイアウト、2017-2018 年の廉価〜中級 mATX ケースでは標準）
  - RTX 4060 クラス（115W 前後）までの dGPU 追加が PSU 交換なしで可能
  - RTX 4070 Ti 以上や dGPU + CPU OC 併用時は 650-750W クラスへ換装必要
- **CPU クーラー**: Intel 純正相当（LGA1151 stock cooler、small heatsink + 小口径ファン）
- **PCIe x16 スロット**: 空（dGPU 非搭載、iGPU のみ）
- **RAM スロット**: 2 本装着（E0035E2F5A6A / E0035E2F5A6B、同ロット）
- **M.2 スロット**: 1 つ確認、**現在空**（旧 Plextor PX-256M8PeGN が 4/24 除去済）
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

## 変更履歴

- **2026-04-24 朝**: 死亡 Plextor を物理除去、ラベル確認で正式モデル **PX-256M8PeGN**（旧記録 M9PeGN は誤り）、製造 2018/09/06 判明、M.2 スロット空き状態に
- **2026-04-22 18:20**: Plextor SSD 死亡、Seagate クローンで緊急起動（詳細: @docs/journal/2026-04-22.md）
- 2026-04-22 17:34: Hasleo でクローン完成（命綱）
- 2026-04-22 16:34: コワーキングに配置転換、新メイン化
- 2025-02-05: Windows 11 Home 25H2 クリーンインストール
- 2018 年頃: ユニットコム STYLE Infinity として購入

## 新 SSD 購入計画

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
