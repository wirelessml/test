# Plextor が死んでから 7 日、新 SSD にクローンしたら Windows が起動しなくなって 3 時間ハマった話

> 真犯人は「StartOverride」というレジストリの 1 行だった

---

4/22 の夕方、コワーキングスペースに置いてあるしゅん先生 PC（Windows 11 メイン作業機）の Plextor PX-256M8PeGN 256GB が突然死した。NVMe コントローラごと逝ったので、再起動しても BIOS から見えない完全沈黙。2 時間前に作っていたクローン HDD が命綱になり、Seagate ST2000LM015（SMR の 2TB HDD）から起動して延命運用に入った。

それから 7 日。延命中の HDD は遅かった。SMR の宿命でランダム書き込みが秒単位でハングする。Visual Studio Code を開くだけで 30 秒、Chrome のタブを 5 個開くと 1 分プチフリーズ。「速度のために金を払う」という当たり前のありがたさを噛みしめる毎日だった。

4/27 月曜。兵庫県の **はばタンPay+ 第 5 弾 50% プレミアム**（5,000 円で 7,500 円分使える地域通貨）を使って、新長田の大西ジムで **Acer FA100 512GB**（M.2 NVMe Gen3 x4）を購入。店頭価格 ¥15,400 → 実質 ¥10,267。2026 年の NAND 高騰下で、512GB NVMe を 1 万円で買えたのは奇跡的だった。

そして 4/29 の朝、ようやくクローン作業に着手した。

ここから 3 時間の死闘が始まる。

---

## 第 1 の罠: 0xc0000001

Hasleo Backup Suite Free でディスククローン（Seagate HDD → Acer NVMe SSD）を実行。完了まで 1 時間ちょっと。BIOS で起動順序を変えて、Acer SSD #1 に設定。再起動。

GIGABYTE のロゴが消えた瞬間、画面に出たのは見慣れた青色のリカバリ画面だった。

```
Recovery
Your PC couldn't start properly
Error code: 0xc0000001
```

`0xc0000001` は「起動に必要な何かが読めない」という汎用エラーコード。winload.efi 経由の Windows ローダーまでは到達してるが、その先で詰まっている。

### bcdboot で BCD を書き直す

BCD（Boot Configuration Data）が新 SSD の構成を正しく指していない可能性がある。Hasleo の WinPE（クローンソフトに付属する救援環境）に入って、`bcdedit` で BCD の中身を確認する。

```
bcdedit /store Z:\EFI\Microsoft\Boot\BCD /enum
```

結果は意外なものだった。BCD は **すでに正しく** 新 SSD の D:\Windows を指していた。`device partition=D:`、`osdevice partition=D:`、`path \Windows\system32\winload.efi`。すべて整合的。

つまり 0xc0000001 の原因は BCD ではなく、それより手前の段階にある。

### chkdsk が地味に効いた

クローンの整合性を確認するために `chkdsk D: /f` を流す。出力の中にこの一行があった。

```
ボリュームビットマップエラーを修正しました
```

ホットクローン（Windows が動いている状態でのクローン）で発生しがちな、ファイルシステムのアロケーション情報の不整合。`chkdsk` がそれを修復してくれた。「これで治ったのでは？」と一縷の希望を抱いて再起動したら、症状は変わったが治っていなかった。

---

## 第 2 の罠: INACCESSIBLE_BOOT_DEVICE (0x7B)

今度は **緑色の BSOD** が出た。Windows Insider Preview だと BSOD が緑色になる。

```
Stop code: INACCESSIBLE_BOOT_DEVICE (0x7B)
```

進歩はあった。0xc0000001 は「起動の前段で死亡」だが、0x7B は「カーネルは起動した、でも起動デバイスが見つからない」だ。一段深い場所に来た。

カーネルが boot device を認識できない症状でググると、99% の記事が「ストレージドライバ問題」と書いている。Acer FA100 は M.2 NVMe、旧 Seagate は SATA HDD。**コントローラが違う**。クローン元の Windows は SATA AHCI を boot start に設定していて、NVMe ドライバ（`stornvme.sys`）は manual start のままになっている。これで NVMe SSD から起動できるわけがない。

### 容疑者: stornvme の Start 値

WinPE に戻って、オフラインレジストリを編集する。`reg load` で D:\Windows\System32\config\SYSTEM をマウントし、ドライバの起動設定を確認。

```
reg query "HKLM\OFFSYS\ControlSet001\Services\stornvme" /v Start
→ Start    REG_DWORD    0x0
```

**Start=0x0**（boot start）。ドライバは boot 時にロードする設定になっている。

「あれ？じゃあ何が問題なんだ」

storahci も Start=0x0、iaStorAVC（古い Intel RST）は不在、Select\Current=0x1（ControlSet001 が活性）、すべて健全。なのに 0x7B が出る。原因がわからない。

---

## 第 3 の真犯人: StartOverride

そのとき、ふとした思い付きで `StartOverride` を確認した。

```
reg query "HKLM\OFFSYS\ControlSet001\Services\stornvme\StartOverride"
→ 0    REG_DWORD    0x3
```

**StartOverride\0 = 0x3**。

これだ。

### Windows の隠し最適化機構

`StartOverride` は Windows の隠れた起動最適化機構で、`Start` 値を **boot 時にオーバーライドする**。`Start=0x0`（boot start）と設定しても、`StartOverride\0=0x3` があれば実際の起動時には manual start に降格される。Windows はインストール時や運用中に「このドライバは boot start で読み込まなくても問題ない」と判断したとき、勝手にこの値を書き込んで起動を最適化する。

旧 Plextor 環境では、Windows は SATA HDD と Plextor の NVMe SSD の両方で動いていた可能性が高い。途中で Plextor が起動ドライブとして認識された後、SATA からの起動に切り替わった瞬間、Windows は「NVMe ドライバは早期にロードする必要がない」と判断して `stornvme\StartOverride\0=0x3` を書き込んだ。

これは旧環境では正しい最適化だった。SATA HDD から起動するなら、NVMe ドライバを boot start で読み込む必要はない。

ところが今回、新 SSD は **完全に NVMe Direct PCIe** だ。SATA を経由しない。だから NVMe ドライバが boot 時にロードされないと、カーネルは起動デバイスを見つけられない。**StartOverride 1 行が、クローン後の Windows の boot を完全に殺していた**。

### 修正コマンド: たった 1 行

```
reg delete "HKLM\OFFSYS\ControlSet001\Services\stornvme\StartOverride" /f
```

これでハイブをアンロードして再起動。

緊張の瞬間。GIGABYTE のロゴが消えて、Windows のスピンアイコンが回転を始めた。BSOD は出ない。緑色も青色も出ない。ロックスクリーンが、何事もなかったかのように、表示された。

3 時間の死闘の終わり。

---

## 結果: Plextor 時代より 1.5 倍速い、しかも Gen3 の天井に到達

起動した Windows で CrystalDiskMark を走らせた結果がこれ。

```
SEQ1M Q8T1     Read  3374.22 MB/s  Write  2826.92 MB/s
SEQ128K Q32T1  Read  3365.46 MB/s  Write  2795.35 MB/s
RND4K Q32T16   Read  1857.87 MB/s  Write  1288.90 MB/s
RND4K Q1T1     Read    57.67 MB/s  Write   124.36 MB/s
```

公称値（Read 3,300 / Write 2,700）を超えている。PCIe 3.0 x4 の理論上限 3,940 MB/s に対して 85% efficiency。コントローラ性能を限界まで使い切っている。

最初は「Plextor 時代の速度に復帰」とだけ書こうとしていたが、生前の Plextor PX-256M8PeGN（2018 年製）の公称値を引き直したら **2,300 MB/s** だった。Acer FA100 の実測 **3,374 MB/s** は、Plextor 時代より **1.5 倍速い**。

| | Plextor PX-256M8PeGN (2018) | Acer FA100 (2025) | 倍率 |
|---|---|---|---|
| 公称 SEQ Read | 2,300 MB/s | 3,300 MB/s | 1.43 倍 |
| 実測 SEQ Read | （生前記録なし） | 3,374 MB/s | **1.47 倍** |

両方とも **PCIe Gen3 x4 NVMe**。同じレーン規格のまま、5 年で NAND とコントローラが進化して Gen3 x4 の理論天井 (3,940 MB/s) に **85% efficiency** で到達した、という話。

### なぜ Gen4 SSD を買わないのか: マザボの Z370 ガラスの天井

ここで重要なのは、しゅん先生 PC のマザボが **Intel Z370 (2017 年 Q4)** ということだ。Z370 は Gen3 までしか対応していない。Gen4 サポートは Intel 11th Gen / Z490 以降か、AMD なら X570 以降が必要になる。

つまり PS5 用の Gen4 SSD（7,000 MB/s クラス）を買っても、このスロットでは **3,500 MB/s で頭打ち**になる。Gen4 SSD は Gen3 スロットに挿すと自動でダウンクロックする後方互換仕様なので、お金を払って Gen4 を買っても性能は出ない。

7 年前の i7-8700K + Z370 のマザボには **Gen3 のガラスの天井**がある。マザボごと買い替える（数万円コース）以外、この天井は破れない。

裏返せば、その天井の手前まで使い切る Gen3 NVMe を選べば、マザボ買い替えなしで体感速度は 1.5 倍になる。Acer FA100 の Gen3 実測 3,374 MB/s は、まさにそのスイートスポットに当たる。

### 旧 SMR HDD（延命中）との比較

旧 Seagate ST2000LM015（延命中の SMR HDD）と並べると桁が変わる:

| 項目 | 延命中 HDD | 新 SSD | 倍率 |
|---|---|---|---|
| SEQ Read | ~120 MB/s | 3,374 | **28 倍** |
| SEQ Write | ~80 MB/s | 2,827 | **35 倍** |
| RND4K Q1T1 R | ~0.5 MB/s | 57.67 | **115 倍** |
| RND4K Q1T1 W | ~0.7 MB/s | 124.36 | **177 倍** |

体感で一番効くのは **RND4K Q1T1**（OS の応答性 = アプリ起動・ブラウザ・エクスプローラの全部）。100 倍以上の差は、人類が知覚できるレベルで「ヌルっ」と動くようになる。

---

## 教訓: クローン失敗時、検索しても出てこない真犯人

ネットで「クローン後 Windows 起動しない 0x7B」と検索すると、大半の記事は次のどれかを書いている。

1. ストレージドライバを `Start=0` に設定しろ
2. AHCI モードと RAID モードを BIOS で切り替えろ
3. クローンソフトの「Universal Restore」機能を使え
4. レジストリ書き換えではなく再インストールしろ

どれも一見正しいが、**StartOverride まで言及している記事は皆無に近い**。Windows の Boot Configuration の隠れた最適化機構なので、Microsoft 自身もまともにドキュメント化していない。

今回の症状は次のすべてを満たしていた:

- BCD は完璧に正しい
- stornvme.sys は実在する
- stornvme の Start = 0x0（boot start）に設定済み
- それでも boot 時にドライバがロードされない
- その結果 0x7B が出る

この組み合わせが起きたとき、容疑者は `StartOverride` 一択だ。

```
reg query "HKLM\OFFSYS\ControlSet001\Services\stornvme\StartOverride"
```

ここに `0 = 0x3` が出たらビンゴ。`reg delete` で消せば boot 時に Start=0 が効くようになって、NVMe ドライバが正しくロードされる。

クローン失敗で 3 時間溶かしたあとに見えた風景なので、今後 NVMe へのクローンで詰む人のために残しておく。

---

## 7 日連続 SSD 記事の総決算

このシリーズの完結編として、Plextor 死亡から復活までのタイムラインを整理しておく。

| 日付 | イベント |
|---|---|
| 4/22 18:20 | Plextor PX-256M8PeGN 256GB 突然死、NVMe コントローラ障害 |
| 4/22-4/29 | Seagate ST2000LM015（SMR HDD）で延命運用、激遅 |
| 4/24 | はばタンPay+ 第 5 弾発表、50% プレミアム適用可 |
| 4/25 | SanDisk USB-C SSD で BIOS と 6 時間半殴り合い、起動成功 |
| 4/27 18:20 | 大西ジム新長田で Acer FA100 512GB 購入、実質 ¥10,267 |
| 4/29 朝 | クローン実行、0xc0000001 → bcdboot → 0x7B → 3 時間死闘 |
| 4/29 16:30 | StartOverride 削除、Windows 起動成功 |
| 4/29 16:45 | CrystalDiskMark 3374 MB/s、Plextor 時代より 1.5 倍速 |

実質コスト: **¥10,267**（はばタンPay+ 50% プレミアム適用後の Acer FA100 価格）

これで 2026 年 NAND 高騰の SSD 危機を、しゅん先生 PC 単位で完全突破した。Plextor 時代の速度に戻ったというよりは、容量 2 倍 + 速度 1.5 倍の **完全アップグレード**だ。同じ Gen3 x4 のレーンの中で、5 年分の NAND・コントローラ進化が天井まで使い切れるようになった、という話でもある。

3 時間の死闘の見返りとして、レジストリの隠れた地雷ひとつぶんの知見が手に入った。次に NVMe にクローンするときには、5 分で終わるだろう。

そして次に Windows が起動しなくなった人にも、この記事が 5 分で済む情報を提供できればいい。
