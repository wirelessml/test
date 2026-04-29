# NVMe SSD クローン後 0x7B が出たら StartOverride を疑え（実戦復旧手順）

> **作成**: 2026-04-29 / **検証環境**: しゅん先生 PC (Windows 11 Insider 25H2 / GIGABYTE Z370 / Plextor → Acer FA100)
>
> **概要**: NVMe SSD への OS クローン後、Windows が 0xc0000001 / 0x7B INACCESSIBLE_BOOT_DEVICE で起動しない問題の根治手順。検索しても出てこない真犯人 `StartOverride` への対応を含む。

---

## 症状

クローン直後の挙動パターン:

| Stop Code | 段階 | 意味 |
|---|---|---|
| `0xc0000001` | bootmgr / winload | 起動に必要な何かが読めない（汎用） |
| `0x7B INACCESSIBLE_BOOT_DEVICE` | カーネル初期化 | NTOSKRNL は起動したが起動デバイスが見えない |

**0xc0000001 → 0x7B の遷移**は「bcdboot で BCD 整備済み、winload は読めるが kernel が disk を取れない」という典型的な**ストレージドライバの起動順序問題**。

---

## 前提

- クローンソフトを問わない（Hasleo / Macrium / EaseUS / AOMEI 等共通）
- 旧ドライブ（クローン元）が SATA HDD/SSD、新ドライブ（クローン先）が **M.2 NVMe** の場合に高頻度発生
- 旧ドライブが NVMe → 新ドライブが NVMe でも発生する可能性あり（コントローラ違いで）

---

## 復旧フロー（推奨順序）

### 0. WinPE 環境を用意

USB の Hasleo Backup Suite Free（`X:\Program Files\Hasleo Backup Suite\bin>` 形式の cmd プロンプト）か、Windows インストールメディアの「コンピュータの修復 → コマンドプロンプト」で WinPE に入る。

Hasleo の場合、クローンソフトが起動ドライブにオンディスク救援環境を仕込んでくれているので、**USB なしで F12 → boot menu → Windows PE (Hasleo Backup Suite)** で入れることが多い。

### 1. ボリューム特定

```cmd
diskpart
list disk      # サイズで判別: 旧 HDD と新 SSD の物理ディスクを確認
list vol       # NTFS で Windows と書いてあるのが Win パーティション
exit
```

WinPE では C: が WinPE 自身、Windows パーティションは通常 D: 以降に当たる。**新 SSD の Windows パーティションのレターを記憶**（以下では D: と仮定）。

### 2. クローン整合性確認

```cmd
dir D:\Windows\System32\winload.efi
dir D:\Windows\System32\config\SAM
dir D:\Windows\System32\config\SYSTEM
```

3 つとも存在すればクローン本体は OK。

### 3. BCD の確認

EFI パーティション（FAT32 100MB SYSTEM）に diskpart でレターを振る:

```cmd
diskpart
list vol
select volume <新 SSD の SYSTEM 100MB のボリューム番号>
assign letter=Z
exit

bcdedit /store Z:\EFI\Microsoft\Boot\BCD /enum
```

確認ポイント:
- `Windows Boot Loader` セクションの `device` `osdevice` `path` が新 SSD の Windows を指してる
- `path` が `\Windows\system32\winload.efi`

**正しく指してても 0xc0000001 が出ることがある**（その場合 BCD は無罪、ストレージドライバの起動問題に進む）。

不整合なら:

```cmd
bcdboot D:\Windows /s Z: /f UEFI /l ja-jp
```

で BCD を上書き。

### 4. ファイルシステム整合性チェック

ホットクローン（実行中の Windows をクローン）すると bitmap 不整合が発生しがち:

```cmd
chkdsk D: /f
```

`/r` は時間かかるので最初は `/f` だけでよい。「ボリュームビットマップエラーを修正しました」が出たら朗報、これだけで治ることもある。

### 5. ストレージドライバの Start 値確認

ここからが本題。レジストリのオフラインハイブをマウントして検査:

```cmd
reg load HKLM\OFFSYS D:\Windows\System32\config\SYSTEM

reg query "HKLM\OFFSYS\ControlSet001\Services\stornvme" /v Start
reg query "HKLM\OFFSYS\ControlSet001\Services\storahci" /v Start
reg query "HKLM\OFFSYS\Select" /v Current
```

期待値:
- `stornvme` Start = `0x0`（boot start）
- `storahci` Start = `0x0`
- `Select\Current` = `0x1`（→ ControlSet001 が活性、`0x2` なら ControlSet002 を編集する）

### 6. 真犯人 `StartOverride` を確認 ← ここが肝

**Start=0x0 でも StartOverride が降格させていることがある。**

```cmd
reg query "HKLM\OFFSYS\ControlSet001\Services\stornvme\StartOverride"
reg query "HKLM\OFFSYS\ControlSet001\Services\storahci\StartOverride"
```

**`0 = 0x3` が出たら確定**。これが Start を上書きしてドライバを manual start に降格させてる。

### 7. 修正（コピペで実行）

```cmd
reg delete "HKLM\OFFSYS\ControlSet001\Services\stornvme\StartOverride" /f
reg delete "HKLM\OFFSYS\ControlSet001\Services\storahci\StartOverride" /f

:: ControlSet002 が存在する場合の保険
reg delete "HKLM\OFFSYS\ControlSet002\Services\stornvme\StartOverride" /f
reg delete "HKLM\OFFSYS\ControlSet002\Services\storahci\StartOverride" /f
```

「指定されたレジストリキーまたは値が見つかりませんでした」エラーは無視（無いだけ）。

### 8. ドライバ .sys ファイル不在のゴミ設定を無効化

クローン元 Windows に登録されてるが .sys ファイルが存在しないドライバは boot 時にロード試行で詰まる。代表的なのは Intel RST 残骸:

```cmd
dir D:\Windows\System32\drivers\iaStorE.sys
```

**ファイルが見つからない**場合:

```cmd
reg add "HKLM\OFFSYS\ControlSet001\Services\iaStorE" /v Start /t REG_DWORD /d 0x4 /f
reg add "HKLM\OFFSYS\ControlSet002\Services\iaStorE" /v Start /t REG_DWORD /d 0x4 /f
```

`0x4` = disabled。

### 9. ハイブをアンロード

```cmd
reg unload HKLM\OFFSYS
```

「正常に完了しました」が出れば OK。

### 10. 再起動して起動テスト

```cmd
exit
```

→ PC 再起動 → BIOS / F12 で新 SSD の Windows Boot Manager を選択 → Windows 起動

---

## StartOverride とは何か（解説）

`HKLM\SYSTEM\ControlSet001\Services\<ドライバ名>\StartOverride\<index>` は Windows の **起動最適化機構**。

- `Start` 値（0=boot / 1=system / 2=auto / 3=manual / 4=disabled）に対し、起動時に `StartOverride\<index>` がオーバーライドする
- Windows は運用中に「このドライバは boot start で読み込まなくても問題ない」と自己判断したとき、勝手にこの値を書き込む
- たとえば SATA HDD から起動してた間、NVMe ドライバ `stornvme` は不要なので `StartOverride\0=3`（manual）に降格される
- これは旧環境では正しい最適化だったが、**クローン先が NVMe Direct PCIe になった瞬間に有害**

Microsoft 公式ドキュメントでこの挙動を明示している箇所はほぼない（`Demand Start Override` として一部 Driver Verifier 関連で言及があるのみ）。だから検索しても引っかからない。

---

## ググっても出てこないのはなぜか

ネットの「クローン後起動しない 0x7B」記事の 99% は次のどれかを書いてる:

1. ストレージドライバを `Start=0` に設定しろ
2. AHCI モードと RAID モードを BIOS で切り替えろ
3. クローンソフトの「Universal Restore」機能を使え
4. レジストリ書き換えではなく再インストールしろ

**StartOverride まで言及してる記事は皆無に近い**。Windows の Boot Configuration の隠れた最適化機構なので、Microsoft 自身もまともにドキュメント化してない。

「Start=0 にしたのに起動しない」と言う人は、StartOverride を疑うべき。

---

## 関連

- 4/29 実戦記録: @docs/journal/2026-04-29.md
- Substack 記事ドラフト: @docs/substack/2026-04-29-nvme-clone-startoverride-substack-ready.md
- 前作（USB-C SSD ブート編）: @docs/guides/sandisk-usb-c-clone-guide.md
- しゅん先生 PC（適用先機材）: @docs/machines/shun-sensei-pc.md
