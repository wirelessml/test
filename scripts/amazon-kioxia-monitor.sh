#!/bin/bash
# Amazon Kioxia KBG40ZNS256G 整備品 定期監視スクリプト
# ASIN: B0F3N6ND7K
# 実行: 毎日 08:17 JST (LaunchAgent)
# ログ: docs/routines/kioxia-monitor-log.md (append-only)
# 発動: 価格 ¥5,000 以下 or 在庫切れ検出時

set -uo pipefail  # -e 外す（パース失敗してもログ追記を優先）

ASIN="B0F3N6ND7K"
PRODUCT_URL="https://www.amazon.co.jp/dp/${ASIN}"
LOG_FILE="/Users/yuika/Desktop/docs/routines/kioxia-monitor-log.md"
TMP_FILE="/tmp/amazon-kioxia-$(date +%Y%m%d-%H%M).html"
TIMESTAMP="$(date '+%Y-%m-%d %H:%M:%S JST')"

UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15'

# Amazon ページ取得
curl -sSL \
  -H "User-Agent: ${UA}" \
  -H "Accept-Language: ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7" \
  --compressed \
  -o "${TMP_FILE}" \
  "${PRODUCT_URL}" 2>/dev/null

HTTP_SIZE=$(stat -f%z "${TMP_FILE}" 2>/dev/null || echo 0)

if [ "${HTTP_SIZE}" -lt 10000 ]; then
  {
    echo ""
    echo "## ${TIMESTAMP}"
    echo "- 取得失敗（HTML サイズ ${HTTP_SIZE} bytes、Amazon block の可能性）"
  } >> "${LOG_FILE}"
  exit 1
fi

# 価格抽出（JSON の priceAmount を優先、フォールバックで a-price-whole）
PRICE=$(grep -oE '"priceAmount":[0-9]+' "${TMP_FILE}" | head -1 | grep -oE '[0-9]+')
if [ -z "${PRICE}" ]; then
  PRICE=$(grep -oE 'a-price-whole">[0-9,]+' "${TMP_FILE}" | head -1 | grep -oE '[0-9,]+' | tr -d ',')
fi
[ -z "${PRICE}" ] && PRICE="unknown"

# 在庫状態
IN_STOCK="unknown"
if grep -qE 'primary-availability-message.*在庫あり' "${TMP_FILE}"; then
  IN_STOCK="IN_STOCK"
elif grep -qE '在庫切れ|現在お取り扱いできません' "${TMP_FILE}"; then
  IN_STOCK="OUT_OF_STOCK"
fi

# 整備済み / 状態ランク
CONDITION="unknown"
if grep -qE 'Amazon Renewed|整備済み' "${TMP_FILE}"; then
  CONDITION="Amazon Renewed（認定整備済み）"
fi
RANK_EXTRA=$(grep -oE '(ほぼ新品|非常に良い|良い)' "${TMP_FILE}" | head -1)
[ -n "${RANK_EXTRA}" ] && CONDITION="${CONDITION} / ${RANK_EXTRA}"

# 星評価（aria-label='星評価 X.X'）
RATING=$(grep -oE '星5つ中の[0-9]\.[0-9]' "${TMP_FILE}" | head -1 | grep -oE '[0-9]\.[0-9]')
if [ -z "${RATING}" ]; then
  RATING=$(grep -oE '"ratingValue":"[0-9]\.[0-9]"' "${TMP_FILE}" | head -1 | grep -oE '[0-9]\.[0-9]')
fi
[ -z "${RATING}" ] && RATING="unknown"

# レビュー数
REVIEWS=$(grep -oE '"reviewCount":"?[0-9]+"?' "${TMP_FILE}" | head -1 | grep -oE '[0-9]+')
if [ -z "${REVIEWS}" ]; then
  REVIEWS=$(grep -oE '[0-9,]+個の評価' "${TMP_FILE}" | head -1 | grep -oE '[0-9,]+' | tr -d ',')
fi
[ -z "${REVIEWS}" ] && REVIEWS="unknown"

# ログ追記
{
  echo ""
  echo "## ${TIMESTAMP}"
  echo "- 価格: ¥${PRICE} 税込"
  echo "- 在庫: ${IN_STOCK}"
  echo "- 状態: ${CONDITION}"
  echo "- 評価: ${RATING} / 5 (${REVIEWS} レビュー)"
} >> "${LOG_FILE}"

# 発動条件チェック
ALERT=""
if [ "${PRICE}" != "unknown" ] && [ "${PRICE}" -le 5000 ] 2>/dev/null; then
  ALERT="PRICE_DROP: ¥${PRICE} (≤ ¥5,000)"
fi
if [ "${IN_STOCK}" = "OUT_OF_STOCK" ]; then
  ALERT="${ALERT}${ALERT:+ / }OUT_OF_STOCK"
fi

if [ -n "${ALERT}" ]; then
  {
    echo ""
    echo "### 🚨 ALERT: ${ALERT}"
    echo "- タイムスタンプ: ${TIMESTAMP}"
    echo "- 対応: ${PRODUCT_URL} を確認、発注検討"
  } >> "${LOG_FILE}"
fi

# tmp ファイル削除（24時間以上前のもの）
find /tmp -name 'amazon-kioxia-*.html' -mtime +1 -delete 2>/dev/null || true

exit 0
