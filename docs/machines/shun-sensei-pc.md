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

### ~~C: Plextor PX-256M9PeGN 256GB NVMe~~（🪦 死亡）

**4/22 18:20 死亡、デバイス検出不可（Get-Disk から消滅）**

- 死因: WHEA_UNCORRECTABLE_ERROR 0x124 + stornvme Event 11 → 完全応答停止
- 生前の状態:
  - 使用 130GB
  - 健康状態「正常 66%」（寿命残 66% / 消費 34%）
  - 総書込 69TB
  - 使用時間 26,779h
  - ファーム 1.03 最終版
- ブランド状況: Plextor 事業撤退済（2024 年 KIOXIA 傘下で SSD 撤退）、サポートなし

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

- Tailscale: 未導入（今後設定予定）
- リモート操作: SSH 未設定

## 変更履歴

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
