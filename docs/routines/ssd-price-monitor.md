## 定期タスク（毎週/毎月の継続監視）

### SSD 価格監視（しゅん先生 PC 用 NVMe SSD 買い替え待ち）

**状況**: 2026 年 NAND 高騰で 1TB NVMe が ¥20,980 から。4/22 Plextor 死亡後、Seagate SMR HDD で延命運用中。

**チェック頻度**: **毎週月曜 or 金曜**（セッション 1 / 9:00 枠で実施）+ **自動日次監視**（下記 Kioxia 整備品ウォッチ）

**監視 URL 3 点セット**:
1. **gazlog.jp SSD 価格グラフ**（毎日更新）: https://gazlog.jp/entry/nvmessd-price-daily-chart/
2. **価格.com Crucial P3 Plus 1TB**: https://kakaku.com/item/K0001595428/
3. **Amazon.co.jp NVMe 1TB 価格順**: https://www.amazon.co.jp/s?k=NVMe+SSD+1TB+M.2+2280&s=price-asc-rank

**購入発動トリガー**:
- **1TB NVMe が ¥12,000 税込以下** → 発注検討
- 500GB が ¥8,000 以下なら容量縮小で検討
- または **Seagate HDD の体感速度に耐えられなくなったら**どの価格でも発注（緊急時）

**候補モデル**（価格回復時の選択肢）:
- Hanye MN50 1TB（現最安 ¥20,980、Amazon 直販 B0B58JKLLW）
- KIOXIA EXCERIA G2 1TB（SSD-CK1.0N3G2/N、Plextor と NAND 同系）
- Crucial P3 Plus 1TB（在庫のみ、Micron 撤退で将来確保困難）
- WD Black SN770 1TB（WDS100T3X0E、Gen4 高速）

**監視すべき業界ニュース**:
- NAND 減産終了 or 生産ライン稼働開始のプレスリリース
- Micron / KIOXIA / Samsung / SanDisk / SK Hynix の四半期決算（供給計画）
- TrendForce / TechInsights の NAND 価格予測レポート

---

### 🔥 Kioxia KBG40ZNS256G 整備品 自動監視（4/23〜）

**対象**: [Amazon.co.jp B0F3N6ND7K](https://www.amazon.co.jp/dp/B0F3N6ND7K)
- Kioxia 256GB M.2 2230/2280 両対応、PCIe Gen3 x4 NVMe 整備済み品
- Amazon Renewed 90 日保証、**非常に良い** ランク（4/23 初回確認）
- 現価 **¥5,990 税込**、過去 1 ヶ月 200 点以上売れてる、評価 4.1/5（158 レビュー）

**動機**: しゅん先生 PC への緊急避難用。¥5,000 以下になれば即発注、現価でも条件次第で買い検討。

**自動監視メカニズム（二層）**:

1. **LaunchAgent（macOS、OS レベル、最強）**
   - plist: `~/Library/LaunchAgents/com.yuika.amazon-kioxia-monitor.plist`
   - スクリプト: `/Users/yuika/Desktop/scripts/amazon-kioxia-monitor.sh`
   - 実行時刻: 毎日 **08:17 JST**
   - 出力ログ: `/Users/yuika/Desktop/docs/routines/kioxia-monitor-log.md` に追記
   - エラーログ: `/tmp/amazon-kioxia-launchd-error.log`
   - Mac 起動中なら常時動作、Claude Code 不要で走る

2. **CronCreate（Claude Code セッション内、念のため）**
   - Job ID: `9f29798b`（本セッション中のみ、7 日で自動消滅）
   - WebFetch 経由で Amazon 確認、チャットに報告

**発動条件**:
- 価格 **¥5,000 以下** → 🚨 ALERT
- 在庫切れ（OUT_OF_STOCK） → 🚨 ALERT

**収集項目**:
- 価格（税込、JSON `priceAmount` 優先、HTML `a-price-whole` フォールバック）
- 在庫状態（`primary-availability-message` で判定）
- 状態ランク（ほぼ新品 / 非常に良い / 良い / 可）
- 星評価 / レビュー数

**ログ**: @docs/routines/kioxia-monitor-log.md

### 手動で監視したい時

```bash
# 即時実行
/Users/yuika/Desktop/scripts/amazon-kioxia-monitor.sh

# ログ確認
tail -30 /Users/yuika/Desktop/docs/routines/kioxia-monitor-log.md

# LaunchAgent 状態確認
launchctl list | grep yuika
```

### LaunchAgent 停止・削除

```bash
# 停止（plist は残す）
launchctl unload ~/Library/LaunchAgents/com.yuika.amazon-kioxia-monitor.plist

# 完全削除
launchctl unload ~/Library/LaunchAgents/com.yuika.amazon-kioxia-monitor.plist
rm ~/Library/LaunchAgents/com.yuika.amazon-kioxia-monitor.plist
```

### スクリプト改善 TODO

- [ ] 星評価・レビュー数のパース改善（現在 unknown が返る）
- [ ] Gmail 下書き連携（ALERT 発動時に自動下書き作成）
- [ ] 他の候補商品（Hanye MN50 1TB B0B58JKLLW 等）への拡張
- [ ] 価格履歴グラフ生成（matplotlib などで）
