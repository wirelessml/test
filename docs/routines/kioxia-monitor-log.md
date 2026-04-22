# Amazon Kioxia KBG40ZNS256G 整備品 監視ログ

**監視対象**: [Kioxia NVMe PCIe SSD 256GB M.2 2230/2280 KBG40ZNS256G 整備済み品](https://www.amazon.co.jp/dp/B0F3N6ND7K)

**監視頻度**: 毎日 08:17 JST（Mac cron 自動実行）

**発動条件**:
- 価格が **¥5,000 以下**に下がったら → ALERT
- 在庫切れになったら → ALERT

**ログ形式**: 以下に時刻順で追記（最新は末尾）

---

## 2026-04-23 05:30:00 JST (初回手動記録)
- 価格: ¥5,990 税込
- 在庫: IN_STOCK
- 状態ランク: Amazon Renewed（認定整備済み）
- 評価: 4.1 / 5（158 レビュー）
- 販売数: 過去 1 ヶ月で 200 点以上
- URL: https://www.amazon.co.jp/dp/B0F3N6ND7K

## 2026-04-23 05:39:37 JST
- 価格: ¥5990 税込
- 在庫: IN_STOCK
- 状態: Amazon Renewed（認定整備済み） / 非常に良い
- 評価: unknown / 5 (unknown レビュー)

## 2026-04-23 08:49:01 JST
- 価格: ¥5990 税込
- 在庫: IN_STOCK
- 状態: Amazon Renewed（認定整備済み） / 非常に良い
- 評価: unknown / 5 (unknown レビュー)
- 備考: スクリプト動作確認用（評価・レビュー数パターン未実装時）

## 2026-04-23 08:51 JST — **CronCreate からの実行**（WebFetch フォールバック: curl）
- 価格: **¥5,990** 税込（変動なし）
- 在庫: **IN_STOCK**
- 状態: **Amazon Renewed（認定整備済み） / 非常に良い**（変動なし）
- 評価: **4.1 / 5**
- レビュー: **159 件**（前回 05:30 時点 158 件から **+1**）
- 発動条件: 該当なし（¥5,000 超え、在庫あり）
- ソース: `curl` で取得、`priceAmount` / `title="5つ星のうち4.1"` / `aria-label="159 レビュー"` パターンでパース
