# SanDisk Extreme Portable SSD (USB-C) でしゅん先生 PC をクローン起動する手順書

> 作成: 2026-04-23、**2026-04-24 実機確認により 1TB → 2TB に訂正**
> 対象 PC: しゅん先生 PC（DESKTOP-ATQ36KS / iiyama STYLE Infinity、Windows 11 25H2）
> 現状: Plextor NVMe SSD 死亡 → Seagate SMR HDD で緊急起動中（激遅）
> 目的: 手持ちの **SanDisk Extreme Portable SSD 2TB (SDSSDE61-2T00, USB-C)** を活用し、体感 **3-5 倍速**の起動環境に移行（しゅん先生 PC の USB-C は USB 3.0 Gen 1 = 5 Gbps 上限のため）
> 投資: ¥0（既存機材のみ、新規購入不要）
> 所要時間: **40-60 分**（Phase 1-4 計） + ファームウェア確認 **15 分**

## 前提条件チェックリスト

作業開始前に確認:

- [ ] **しゅん先生 PC が Windows 11 で起動できている**（現状 Seagate HDD から起動中）
- [ ] **SanDisk Extreme Portable SSD 2TB**（**型番 SDSSDE61-2T00**、S/N 25219B405582）が手元にある
- [ ] **付属の USB-C to USB-C ケーブル**、または USB-C to USB-A ケーブルが手元にある
- [ ] **しゅん先生 PC の USB-C ポート**または **USB 3.0 (青色) ポート**が空いている
- [ ] **SanDisk 内の重要データは退避済み**（クローンで全削除される）
- [ ] **Hasleo Backup Suite Free** インストール済み（4/22 導入済み、C:\Program Files\Hasleo Backup Suite\）
- [ ] **⚠ SanDisk Dashboard でファームウェアが最新版**（SDSSDE61 2TB はデータ消失リコール対象モデル、下記 Phase 0-0 参照）
- [ ] **30-60 分の作業時間**を確保

## Phase 0-0-prep: 内部清掃（オプション、10 分）

4/24 内部写真で **埃堆積を確認**。蓋を開けるなら同時に清掃推奨:

- エアダスター（缶 or 電動ブロワー）で:
  - CPU クーラーファン（特に重要）
  - ケース底面・メッシュパネル
  - 電源ユニット吸気口
  - メモリスロット周辺
- ケース外側は固く絞った布で拭く
- **静電気対策**: 作業前に金属製の何かに触れて放電、または帯電防止リストバンド使用

## Phase 0-0: ファームウェア確認（⚠ 必須、15 分）

**理由**: 本機（SDSSDE61-2T00、2TB）は 2023 年の SanDisk Extreme Portable SSD データ消失リコールの **主要対象モデル**。S/N から 2025 年 8 月頃製造と推定（25219 = 2025 年 219 日目）されるため修正済み FW が初期搭載されている可能性が高いが、**クローン先として数百 GB の重要データを載せる前に必ず検証**。

### 0-0-1. SanDisk Dashboard インストール & FW チェック

1. SanDisk 公式サイトから SanDisk Dashboard をダウンロード
   - `https://www.westerndigital.com/support/downloads/sandisk-dashboard` （実 URL は作業当日に公式検索）
2. インストール後起動、SanDisk SSD を USB-C 接続
3. **Tools** → **Firmware Update** を確認
4. 推奨: **ファームウェアが 2023/08 以降リリース版**であること
   - 旧 FW の場合は「Update」をクリック（5-10 分、完了まで未通電切断厳禁）
   - 更新前にバックアップが望ましいが、この SSD はクローン先なので現状データ退避のみで可

### 0-0-2. SMART 値確認

```powershell
# CrystalDiskInfo or smartctl で健康状態確認
# USB 3.2 Gen 2 経由で SMART が読める機種（SDSSDE61）であることを確認
```

**期待**: 新品同様（Reallocated Sectors = 0、Power-On Hours 低、Percentage Used 低）
**NG サイン**: Reallocated Sectors > 0 → 返品・別 SSD 使用推奨

## Phase 0: 事前準備（10 分）

### 0-1. SanDisk 内のデータ退避

```powershell
# PowerShell 管理者で現状確認
Get-Disk | Format-Table Number, FriendlyName, Size, BusType

# SanDisk が D: or E: として認識されたらその中身を確認
Get-ChildItem E:\ -Force | Select Name, Length | Format-Table
```

**重要データあれば別の場所へコピー**（Seagate の空き領域、OneDrive、別の USB メモリ等）。SanDisk は Phase 2 で完全消去されます。

### 0-2. しゅん先生 PC のスペック再確認

```powershell
# USB ポート構成確認
Get-PnpDevice -Class USB -Status OK | Select FriendlyName, InstanceId | Format-Table

# BIOS バージョン確認（後で BIOS 起動設定参照用）
Get-CimInstance Win32_BIOS | Select Manufacturer, Name, Version
```

**期待**: 
- 背面に USB 3.0/3.1/3.2 ポート（青色コネクタ）が複数ある
- USB-C ポートは前面か背面に 1-2 個（2018 年 PC だと USB-C は少ない可能性）

### 0-3. USB-C ケーブル品質の確認

**SanDisk Extreme Portable は USB 3.2 Gen 2 (10 Gbps) 対応**。ケーブルが古い USB 2.0 対応品だと **~40 MB/s まで速度低下**して意味ない。

付属ケーブル使用推奨、またはケーブル側面に「**USB 3.0**」「**10Gbps**」「**Gen 2**」表記があるもの。

```powershell
# 接続後の実効速度確認（SanDisk 認識済み前提）
# Phase 1 完了後に実行
winsat disk -drive E
```

出力で「**Sequential Read** が 500 MB/s 以上**」なら USB 3.0+ で正常認識。**100 MB/s 以下**なら USB 2.0 接続になってる → ケーブル交換 or 別ポート。

## Phase 1: SanDisk 接続と認識確認（5 分）

### 1-1. 物理接続

**推奨接続方法**:
1. しゅん先生 PC の **背面の USB 3.0/3.1 ポート**（青色 or 黒色で「SS」マーク）に接続
2. または **USB-C ポート**（あれば）
3. **前面ポート非推奨**（ケーブルに引っ掛けやすい）

### 1-2. 認識確認

```powershell
# 全ディスク確認
Get-Disk | Format-Table Number, FriendlyName, BusType, Size, PartitionStyle

# USB 接続の確認
Get-Disk | Where BusType -eq "USB" | Format-Table
```

**期待結果**:
```
Number FriendlyName              BusType  Size             PartitionStyle
------ ------------              -------  ----             --------------
     0 ST2000LM015-2E8174        SATA     2000398934016    GPT
     1 SanDisk Extreme Portable  USB      2000398934016    GPT or MBR
```

注: Seagate と SanDisk がほぼ**同容量（2TB）**なので、クローン後のパーティション縮小は不要。

認識されない場合:
- ケーブルを抜き差し
- 別の USB ポートに変更
- SanDisk 自体を別 PC（Mac 等）で確認して物理障害チェック

### 1-3. 速度ベンチマーク（オプション）

```powershell
# WinSAT でディスク速度測定
winsat disk -drive E
```

**期待**（本機しゅん先生 PC は **USB 3.0 Type-C = 5 Gbps 制限**、i7-8700K + Z370 世代の PCH ネイティブ制約のため）:
- **Sequential Read 400-500 MB/s**（実効）
- SanDisk 公称 1,050 MB/s は 10 Gbps ポート経由必要、本機では出ない
- それでも Seagate SMR HDD (100-150 MB/s) 比で **3-5 倍速**。体感メリット十分

## Phase 2: Hasleo Backup Suite でクローン実行（15-25 分）

### 2-1. Hasleo Backup Suite 起動

スタートメニュー → 「Hasleo Backup Suite Free」→ 起動

または:
```powershell
Start-Process "C:\Program Files\Hasleo Backup Suite\HaBackupSuite.exe"
```

### 2-2. ディスククローン設定

1. 左サイドバー **クローン** アイコン（ディスク二重）をクリック
2. **ディスククローン** を選択
3. **ソースディスク選択**:
   - **Disk 0: ST2000LM015**（2TB、現 C: の Seagate）を選択
   - 注意: しゅん先生 PC の Windows が入っているディスクを選ぶ
4. **次へ**
5. **ターゲットディスク選択**:
   - **Disk 1: SanDisk Extreme Portable**（**2TB**、USB）を選択
   - 警告: 「ターゲットディスクのデータは削除されます」→ **はい**
6. **次へ**
7. **操作概要**:
   - ☑ **4K アライメント**（SSD 最適化）→ **ON**
   - ☑ **セクター単位のクローン** → **OFF 推奨**（同容量だが OFF で十分。ON にすると 2TB 全域を読み書きするため所要時間大幅増）
   - ☐ **MBR としてクローン** → **OFF**（GPT 維持）
8. **「続行」**

### 2-3. 容量について

**本機は同容量クローン**: Seagate 2TB → SanDisk **2TB** = 容量調整不要。
- Seagate 現使用: ~130GB（C: 実データ）
- SanDisk 2TB: Windows パーティションはほぼそのままのサイズ（空き容量 ~1.87TB を後で活用可能）
- クローン後パーティション拡張/縮小は任意（デフォルト配置で問題なし）

### 2-4. クローン開始

「開始」クリック → 最終確認 → **はい**

**進捗表示**:
- ファイルシステムチェック: 1-2 分
- 複製中: 10-20 分（USB 3.2 Gen 2 で 130GB 書込、~1000 MB/s 理論値）
- 完了画面: 「操作は正常に完了しました」

**所要時間予想**: **15-20 分**（4/22 に Hasleo で Plextor → Seagate クローン 18 分、今回は書込先が USB SSD なので似た時間）

### 2-5. クローン完了確認

```powershell
Get-Partition | Where DiskNumber -eq 1 | Format-Table DriveLetter, Size, Type
```

**期待**:
```
DriveLetter  Size           Type
-----------  ----           ----
            104857600      System      # EFI
            16777216       Reserved    # MSR
E           ~990GB         Basic       # Windows クローン (ドライブレター任意)
            943718400      Recovery
```

## Phase 3: BIOS 起動順変更（10 分）

### 3-1. シャットダウンして BIOS 起動

1. Windows 完全シャットダウン（高速起動無効推奨）
   ```powershell
   shutdown /s /t 0 /f
   ```
2. 電源投入直後から **Delete キー連打**（iiyama BTO の多くは Del）
3. BIOS 画面が出ない場合は **F2** も試す
4. 起動して Windows が出たら、Shift + 再起動 → 詳細オプション → UEFI ファームウェア設定 でも BIOS 入れる

### 3-2. Boot Priority 変更

BIOS 画面で:
1. **Boot** タブ（または Boot Priority / Boot Order メニュー）へ移動
2. 現在の順序:
   ```
   Boot Option #1: Windows Boot Manager (Seagate ST2000LM015)
   Boot Option #2: (空 or 他)
   ```
3. **Boot Option #1 を USB に変更**:
   - **Windows Boot Manager (SanDisk Extreme Portable)** or
   - **UEFI: SanDisk Extreme Portable**
4. **Boot Option #2 に Seagate を後退**（緊急時のフォールバック）
5. **F10 → Save & Exit** → **Yes**

### 3-3. USB 起動確認

BIOS 再起動後:
1. Windows 11 ロゴが表示
2. 「読み込んでいます...」→ **SanDisk 経由で起動開始**
3. 通常は Seagate よりも**速くロゴが出る**（SSD の速度メリット）
4. ログイン画面 → パスワード入力 → デスクトップ

**初回起動の特徴**:
- **30 秒-1 分で起動**（Seagate は 3-5 分だった）
- 「新しいデバイスを設定しています」的な通知が出る可能性（無視）
- Windows が「内部ディスクと異なる」と判断してドライバ再認識することあり

### 3-4. 起動後の確認

```powershell
# 現在起動ディスクを確認
Get-CimInstance Win32_OperatingSystem | Select SystemDrive
bcdedit /enum | Select-String "device|osdevice"

# ディスク一覧（SanDisk が C: に昇格しているはず）
Get-Disk | Format-Table Number, FriendlyName, BusType
```

**期待**:
- `osdevice: partition=C:` （SanDisk = C:）
- 元 Seagate は **D:** or **E:** などで見える（2TB）
- Windows は自分が C: と認識（OS は常に自分を C: にする）

## Phase 4: 運用上の注意（今後の作業）

### 4-1. USB 接続を常時維持する運用ルール

**絶対やってはいけないこと**:
- ❌ USB-C ケーブルを電源 ON のまま抜く（瞬時に OS ブルースクリーン）
- ❌ PC 背面の整理中に USB-C ケーブルを強く引っ張る
- ❌ SanDisk 本体を持ち歩く（しゅん先生 PC が起動不能になる）
- ❌ Windows で「ハードウェアの安全な取り外し」を実行

**推奨**:
- ✅ **USB-C ケーブルを背面ポートに固定**（タイラップや結束バンドで本体に緊結）
- ✅ **SanDisk 本体も PC 背面に固定**（両面テープ or マグネット）
- ✅ シャットダウン時のみ取り外し可

### 4-2. 万一切断した場合の復旧

**シナリオ**: 作業中に USB-C ケーブル抜けて Windows クラッシュ

**復旧手順**:
1. SanDisk 再接続
2. PC 強制再起動（電源長押し）
3. BIOS で USB 起動確認
4. Windows が自動修復モードに入ったら放置 → 正常起動に戻る
5. それでもダメなら **Boot Priority を Seagate に戻す** → Seagate から緊急起動（遅いが動く）

### 4-3. バックアップ戦略

**新しい防御層**:
- C: SanDisk USB SSD（現メイン、高速）
- D: Seagate HDD（旧 C: 全データ保持、緊急時のフォールバック起動可能）
- `D:\Backup\Weekly System Image.adi`（4/22 作成のシステムイメージ、82.94GB）
- AOMEI 週次バックアップ継続（既設定、毎週日曜 04:00）

**SanDisk 死亡時**:
- Seagate からの起動に戻す（BIOS 設定変更のみ、1 分）
- 元のクローン状態に復帰

## Phase 5: 検証テスト（10 分）

### 5-1. 体感速度比較

以下を実測して旧 Seagate 起動時と比較:

```powershell
# 起動時間計測
Get-CimInstance Win32_OperatingSystem | Select LastBootUpTime
# 手動ストップウォッチで「電源 ON → デスクトップ表示」の時間

# ディスク速度
winsat disk -drive C

# ブラウザ起動時間（手動計測）
# Brave / Chrome / Edge
```

**期待値**:
| 項目 | Seagate SMR HDD | SanDisk USB-C | 改善倍率 |
|---|---|---|---|
| Windows 起動（電源 → デスクトップ） | 3-5 分 | **30 秒-1 分** | 5-10x |
| Brave 起動 | 20-40 秒 | **2-5 秒** | 8x |
| PowerShell 起動 | 5-10 秒 | **1-2 秒** | 5x |
| File Explorer 立ち上げ | 3-8 秒 | **即時** | 10x |
| アプリインストール | 数分 | 数十秒 | 5-10x |

### 5-2. 安定性テスト

**1 時間運用テスト**:
- 通常の作業（ブラウザ、ファイル操作、PowerShell）を 1 時間実施
- **切断・クラッシュなし**か確認
- Event Viewer で USB 関連のエラーログなし確認
```powershell
Get-WinEvent -LogName System -MaxEvents 50 | 
  Where LevelDisplayName -match "Error|Critical" | 
  Where Message -match "USB|disk" | 
  Format-Table TimeCreated, Id, Message -AutoSize
```

## Phase 6: ロールバック手順（必要時）

SanDisk USB クローンで問題が発生した場合、Seagate 起動に戻す:

1. PC シャットダウン
2. 電源 ON → Del 連打 → BIOS
3. Boot Priority **Boot Option #1** を **Seagate ST2000LM015** に戻す
4. F10 → Save & Exit
5. Seagate 起動に復帰（SMR 速度に戻るが動く）

SanDisk はデータがクローン状態のまま残るので、後日再挑戦可能。

## 判断基準: この手順で運用継続するか

### ✅ 継続推奨
- 1 時間運用テスト問題なし
- 体感速度が明らかに改善
- ケーブル引っ掛けのリスク低い配置

### ❌ 運用中止 → GEO / Kioxia 購入ルート
- USB 切断が頻発
- 速度が期待ほど出ない（~200 MB/s 以下）
- Windows が不安定化

## 想定されるトラブル一覧

| 症状 | 原因 | 対応 |
|---|---|---|
| BIOS で SanDisk が起動候補に出ない | UEFI 未対応な FAT32 起動形式 | Rufus で UEFI 対応再クローン or GPT 変換 |
| 起動が遅い（Seagate と同等） | USB 2.0 ポート接続 | USB 3.0 (青色) or USB-C ポートに変更 |
| ランダムフリーズ | USB コントローラ相性 | 背面ポートに固定、前面避ける |
| Windows ライセンス認証警告 | ハード変更検知 | Microsoft アカウントで再認証 |
| クローン中に容量エラー | セクター単位 ON のまま | OFF にして再実行 |
| 完了後デスクトップが真っ黒 | ドライバ未ロード | セーフモード起動 → ドライバ更新 |

## 関連ファイル

- しゅん先生 PC 詳細: @docs/machines/shun-sensei-pc.md
- 4/22 Hasleo Plextor→Seagate クローン実績: @docs/journal/2026-04-22.md
- SSD 価格監視: @docs/routines/ssd-price-monitor.md
- バックアップ運用全体: @docs/journal/2026-04-22.md

## 総所要時間目安

- Phase 0: 10 分
- Phase 1: 5 分
- Phase 2: **15-25 分**（クローン本体）
- Phase 3: 10 分
- Phase 4: 継続運用（即時）
- Phase 5: 10 分
- **合計**: **50-60 分**

## 成功時の継続運用

SanDisk USB-C クローン運用が成立すれば:
- **新 SSD 購入判断を遅らせられる**（GEO / Kioxia の価格待ちがさらに可能）
- **NAND 価格の急落**を待てる（2026 Q3-Q4 の供給改善観察）
- しゅん先生 PC が**実用 Speed**で使える状態を維持
- Substack ネタ追加: 「SSD 死亡 → USB-C 外付けで運用」

## 注意: SanDisk Extreme 特有のリスク

**⚠ 本機 SDSSDE61-2T00 (2TB) はリコール主要対象モデル** — 以下を必ず理解してから進める

**2022-2023 年の SanDisk Extreme Portable SSD データ消失リコール問題**:
- **主に 4TB / 2TB モデルで発生（本機はこれに該当）**
- ファームウェア不具合で突然データ消失事例
- SanDisk / WD が修正ファームウェアを公開、集団訴訟に発展
- 本機 S/N 25219B405582 は 2025 年 8 月製造推定 → **修正 FW 出荷済みの可能性高**だが、**Phase 0-0 で必ず FW バージョン確認**

対策（必須）:
- **Phase 0-0 のファームウェア確認を省略しない**
- **Seagate HDD を即時取り外さない**（D: として常時マウント、緊急フォールバック維持）
- AOMEI 週次イメージを Seagate に継続保存（二重防御）
- 万一 SanDisk 死亡しても Seagate からの起動に戻せる体制を維持
- **重要データの単独保存は避ける**（DropBox / Google Drive / NAS 等との多重化）
- **定期的に SMART 値を監視**（月 1 回推奨、Reallocated / Pending Sectors をチェック）
