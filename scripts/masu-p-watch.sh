#!/bin/bash
# MASU-p (神戸市須磨区板宿コワーキング) サイト + Instagram 毎日監視
# 実行: 毎日 08:23 JST (LaunchAgent)
# ログ: docs/routines/masu-p-watch-log.md (append-only)
# スナップショット: docs/routines/masu-p-snapshots/ (差分比較用)
# 発動: ページ HTML / Instagram メタタグに変化があった場合

set -uo pipefail

ROOT="/Users/yuika/Desktop"
WEB_URL="https://masu-p.com/"
IG_URL="https://www.instagram.com/masup_official/"
LOG_FILE="${ROOT}/docs/routines/masu-p-watch-log.md"
SNAP_DIR="${ROOT}/docs/routines/masu-p-snapshots"
TIMESTAMP="$(date '+%Y-%m-%d %H:%M:%S JST')"
DATE_TAG="$(date '+%Y%m%d-%H%M')"

UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15'

mkdir -p "${SNAP_DIR}"

# --- masu-p.com 取得 ---
WEB_TMP="/tmp/masu-p-web-${DATE_TAG}.html"
curl -sSL -H "User-Agent: ${UA}" -H "Accept-Language: ja-JP,ja;q=0.9" --compressed \
  -o "${WEB_TMP}" "${WEB_URL}" 2>/dev/null

WEB_SIZE=$(stat -f%z "${WEB_TMP}" 2>/dev/null || echo 0)

# 本文だけ抽出して hash 化 (script/style/動的部分は除外)
# perl -0777 でファイル全体スラープ → 多行 regex
WEB_BODY=$(perl -0777 -ne '
  s|<script\b[^>]*>.*?</script>||gs;
  s|<style\b[^>]*>.*?</style>||gs;
  s|<!--.*?-->||gs;
  if (m|<body[^>]*>(.*)</body>|s) { print $1; }
' "${WEB_TMP}" 2>/dev/null)
WEB_HASH=$(printf '%s' "${WEB_BODY}" | shasum -a 256 | awk '{print $1}')

# 公開告知/最新更新の候補抽出 (h1/h2/h3 + 段落テキスト最大 30)
WEB_HEADLINES=$(printf '%s' "${WEB_BODY}" \
  | perl -0777 -ne 'while(m|<h[1-4][^>]*>(.*?)</h[1-4]>|gs){ my $t=$1; $t=~s/<[^>]+>//g; $t=~s/^\s+|\s+$//g; print "$t\n" if $t; }' \
  | head -30 \
  | sort -u)

# --- Instagram 取得 (公開メタタグのみ) ---
IG_TMP="/tmp/masu-p-ig-${DATE_TAG}.html"
curl -sSL -H "User-Agent: ${UA}" -H "Accept-Language: ja-JP,ja;q=0.9" --compressed \
  -o "${IG_TMP}" "${IG_URL}" 2>/dev/null

IG_SIZE=$(stat -f%z "${IG_TMP}" 2>/dev/null || echo 0)

# og:description (bio + 投稿サマリー), og:image (最新投稿画像 URL)
IG_DESC=$(grep -oE '<meta property="og:description" content="[^"]*"' "${IG_TMP}" 2>/dev/null \
  | sed 's/<meta property="og:description" content="\([^"]*\)"/\1/' | head -1)
IG_IMG=$(grep -oE '<meta property="og:image" content="[^"]*"' "${IG_TMP}" 2>/dev/null \
  | sed 's/<meta property="og:image" content="\([^"]*\)"/\1/' | head -1)
# 画像 URL は CDN ハッシュ部分が変わるので、URL の最後の path component の prefix だけ取り出す
IG_IMG_KEY=$(echo "${IG_IMG}" | grep -oE '[0-9]+_[0-9]+_[0-9]+_[a-z]+' | head -1)
IG_HASH=$(echo "${IG_DESC}|${IG_IMG_KEY}" | shasum -a 256 | awk '{print $1}')

# --- 前回スナップショットと比較 ---
PREV_WEB_HASH_FILE="${SNAP_DIR}/web-latest.hash"
PREV_IG_HASH_FILE="${SNAP_DIR}/ig-latest.hash"

PREV_WEB_HASH=$(cat "${PREV_WEB_HASH_FILE}" 2>/dev/null || echo "INITIAL")
PREV_IG_HASH=$(cat "${PREV_IG_HASH_FILE}" 2>/dev/null || echo "INITIAL")

WEB_STATUS="unchanged"
IG_STATUS="unchanged"
ANY_CHANGE=0

if [ "${WEB_SIZE}" -lt 1000 ]; then
  WEB_STATUS="fetch-fail (size=${WEB_SIZE})"
elif [ "${PREV_WEB_HASH}" = "INITIAL" ]; then
  WEB_STATUS="baseline"
  ANY_CHANGE=1
elif [ "${PREV_WEB_HASH}" != "${WEB_HASH}" ]; then
  WEB_STATUS="🚨 CHANGED"
  ANY_CHANGE=1
fi

if [ "${IG_SIZE}" -lt 1000 ]; then
  IG_STATUS="fetch-fail (size=${IG_SIZE})"
elif [ "${PREV_IG_HASH}" = "INITIAL" ]; then
  IG_STATUS="baseline"
  ANY_CHANGE=1
elif [ "${PREV_IG_HASH}" != "${IG_HASH}" ]; then
  IG_STATUS="🚨 CHANGED"
  ANY_CHANGE=1
fi

# --- ハッシュ更新 (変化があったときのみ) ---
if [ "${WEB_STATUS}" != "unchanged" ] && [ "${WEB_SIZE}" -ge 1000 ]; then
  echo "${WEB_HASH}" > "${PREV_WEB_HASH_FILE}"
  cp "${WEB_TMP}" "${SNAP_DIR}/web-${DATE_TAG}.html"
fi

if [ "${IG_STATUS}" != "unchanged" ] && [ "${IG_SIZE}" -ge 1000 ]; then
  echo "${IG_HASH}" > "${PREV_IG_HASH_FILE}"
  cp "${IG_TMP}" "${SNAP_DIR}/ig-${DATE_TAG}.html"
fi

# --- ログ追記 ---
{
  echo ""
  echo "## ${TIMESTAMP}"
  echo ""
  echo "- Web: ${WEB_STATUS} (size: ${WEB_SIZE}, hash: ${WEB_HASH:0:12}…)"
  if [ -n "${WEB_HEADLINES}" ] && [ "${WEB_STATUS}" != "unchanged" ]; then
    echo "  - 見出し抜粋:"
    echo "${WEB_HEADLINES}" | head -10 | sed 's/^/    - /'
  fi
  echo "- Instagram: ${IG_STATUS} (size: ${IG_SIZE}, hash: ${IG_HASH:0:12}…)"
  if [ -n "${IG_DESC}" ] && [ "${IG_STATUS}" != "unchanged" ]; then
    echo "  - og:description: ${IG_DESC}"
    [ -n "${IG_IMG_KEY}" ] && echo "  - 最新投稿画像 key: ${IG_IMG_KEY}"
  fi
  if [ "${ANY_CHANGE}" -eq 1 ] && [ "${PREV_WEB_HASH}" != "INITIAL" ]; then
    echo "  - 🚨 変化検出: 詳細は ${SNAP_DIR}/{web,ig}-${DATE_TAG}.html を確認"
  fi
} >> "${LOG_FILE}"

# --- 変化検出時のメール送信 ---
EMAIL_CONFIG="${HOME}/.config/masu-p-watch/email.json"
SEND_EMAIL_PY="${ROOT}/scripts/lib/send-email.py"

if [ "${ANY_CHANGE}" -eq 1 ] && [ "${PREV_WEB_HASH}" != "INITIAL" ]; then
  if [ -f "${EMAIL_CONFIG}" ] && [ -x "${SEND_EMAIL_PY}" ]; then
    SUBJECT="🚨 MASU-p 変化検出 ${TIMESTAMP%% *}"
    BODY_TMP="/tmp/masu-p-watch-mail-${DATE_TAG}.txt"
    {
      echo "MASU-p 監視で変化を検出しました (${TIMESTAMP})"
      echo ""
      echo "Web (https://masu-p.com/): ${WEB_STATUS}"
      echo "  size: ${WEB_SIZE}, hash: ${WEB_HASH:0:16}…"
      if [ -n "${WEB_HEADLINES}" ] && [ "${WEB_STATUS}" != "unchanged" ]; then
        echo "  見出し抜粋:"
        echo "${WEB_HEADLINES}" | head -10 | sed 's/^/    - /'
      fi
      echo ""
      echo "Instagram (@masup_official): ${IG_STATUS}"
      echo "  size: ${IG_SIZE}, hash: ${IG_HASH:0:16}…"
      if [ -n "${IG_DESC}" ] && [ "${IG_STATUS}" != "unchanged" ]; then
        echo "  og:description: ${IG_DESC}"
        [ -n "${IG_IMG_KEY}" ] && echo "  最新投稿画像 key: ${IG_IMG_KEY}"
      fi
      echo ""
      echo "スナップショット保存先:"
      echo "  ${SNAP_DIR}/web-${DATE_TAG}.html"
      echo "  ${SNAP_DIR}/ig-${DATE_TAG}.html"
      echo ""
      echo "ログ全体: ${LOG_FILE}"
    } > "${BODY_TMP}"
    "${SEND_EMAIL_PY}" --subject "${SUBJECT}" --body-file "${BODY_TMP}" >> /tmp/masu-p-watch-launchd.log 2>&1
    rm -f "${BODY_TMP}"
  else
    echo "[masu-p-watch] email skipped: config or sender missing" >> /tmp/masu-p-watch-launchd.log
  fi
fi

# tmp 掃除
rm -f "${WEB_TMP}" "${IG_TMP}"

exit 0
