#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
毎朝の求人サーチ（Mac 単独実行版、Codex 不使用）
- 求人ボックスを直接走査し、板宿駅 約1km・資格不要・全職種の求人を全件網羅
- 在宅可は「声を出さない」事務系のみ（神戸市→兵庫県内の優先順）
- 恒久除外: 介護・福祉 / 障がい福祉支援職 / 飲食 / 資格・免許必須職 / 50代不可明記
- /jb/ 詳細ページで実在・勤務地を検証（矛盾は除外しログに記載）
- レポートを GitHub (wirelessml/job-hunt-reports) に push し、メール送信をトリガー
2026-06-10 作成（実行主体を masup Codex から移管。経緯: docs/routines/job-search-daily.md）
環境変数: JS_DATE=YYYY-MM-DD（日付上書き） JS_NO_PUSH=1 JS_NO_EMAIL=1 JS_FORCE_EMAIL=1（テスト用/再送用）
"""
import re, os, sys, time, json, html, subprocess, datetime, urllib.request

BASE = 'https://xn--pckua2a7gp15o89zb.com'
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'
SELF_DIR = os.path.expanduser('~/Library/Application Support/job-report')
REPO = os.path.join(SELF_DIR, 'job-hunt-reports')
LOG = os.path.join(SELF_DIR, 'job-search-daily.log')
DATE = os.environ.get('JS_DATE') or datetime.date.today().isoformat()

ONSITE_URL = BASE + '/%E7%A5%9E%E6%88%B8%E5%B8%82%E6%9D%BF%E5%AE%BF%E9%A7%85%E3%81%A7%E3%81%AE%E4%BB%95%E4%BA%8B'  # 神戸市板宿駅での仕事
REMOTE_URLS = [
    ('神戸市', BASE + '/%E5%9C%A8%E5%AE%85-%E4%BA%8B%E5%8B%99%E3%81%AE%E4%BB%95%E4%BA%8B-%E5%85%B5%E5%BA%AB%E7%9C%8C%E7%A5%9E%E6%88%B8%E5%B8%82'),  # 在宅-事務の仕事-兵庫県神戸市
    ('兵庫県内', BASE + '/%E5%9C%A8%E5%AE%85-%E4%BA%8B%E5%8B%99%E3%81%AE%E4%BB%95%E4%BA%8B-%E5%85%B5%E5%BA%AB%E7%9C%8C'),  # 在宅-事務の仕事-兵庫県
]
TOWNS = ['戎町','飛松町','大黒町','大田町','平田町','前池町','板宿町','大手町','宝田町','菊池町','寺田町','庄山町','西代通','大池町','千歳町','堀池町','稲葉町','養老町','若松町','常盤町']
# 資格・免許必須職＋福祉＋飲食＋その他恒久除外（2026-06-10 ユーザー指定）
NG = re.compile(r'看護|薬剤師|歯科衛生|保育士|介護|ヘルパー|ケアマネ|福祉士|相談員|支援員|児童指導員|学童|児童発達|放課後等デイ|柔道整復|あん摩|マッサージ|鍼灸|理学療法|作業療法|言語聴覚|栄養士|美容師|理容師|アイリスト|ネイリスト|スタイリスト|エステ|サービス提供責任|生活相談|調理|ホール|キッチン|飲食|レストラン|居酒屋|カフェ|すき家|ケンタッキー|ピザ|ラーメン|串|寿司|焼肉|資格必須|有資格|要資格|保健師|助産師|心理師|心理士|教員免許|幼稚園教諭|重機|フォークリフト|玉掛|溶接|電気工事士|施工管理|危険物|新卒|警備|清掃')
VOICE_NG = re.compile(r'コール|テレオペ|テレアポ|電話|受付|窓口|カスタマー|サポートデスク|テクニカルサポート|ヘルプデスク|CS|オペレーター|アノテーション|営業(?!事務)')
AGE_NG = re.compile(r'(?:35|40|45)歳以下|〜(?:3|4)\d歳|若年層のみ')

def log(msg):
    line = f"{datetime.datetime.now().strftime('%F %T')} {msg}"
    print(line)
    with open(LOG, 'a') as f: f.write(line + '\n')


# 2026-06-12 堅牢化: 取得異常を warning として蓄積し、全滅時は正常レポートを出さず fail させる
WARNINGS = []
def warn(msg):
    WARNINGS.append(msg)
    log('WARN ' + msg)

def run_cmd(args, timeout):
    cp = subprocess.run(args, timeout=timeout, text=True, capture_output=True)
    if cp.returncode != 0:
        stderr = (cp.stderr or '').strip()[-800:]
        stdout = (cp.stdout or '').strip()[-400:]
        raise RuntimeError(f"command failed rc={cp.returncode}: {' '.join(args)} stdout={stdout!r} stderr={stderr!r}")
    return cp

def fetch(url, retries=2):
    for i in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept-Language': 'ja'})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode('utf-8', 'ignore')
        except Exception as e:
            if i == retries: log(f'FETCH_FAIL {url} {e}'); return ''
            time.sleep(3)

def strip_tags(s):
    return html.unescape(re.sub(r'<[^>]+>', ' ', s)).strip()

def norm(s):
    return re.sub(r'\s+', ' ', s).strip()

def parse_cards(page_html):
    cards = []
    chunks = re.split(r'<section[^>]*class="[^"]*p-result_card', page_html)[1:]
    for ch in chunks:
        ch = ch[:12000]
        def grab(cls):
            m = re.search(r'class="[^"]*' + cls + r'[^"]*"[^>]*>(.*?)</(?:p|div|span|h2)>', ch, re.S)
            return norm(strip_tags(m.group(1))) if m else ''
        title_m = re.search(r'<h2[^>]*>(.*?)</h2>', ch, re.S)
        title = norm(strip_tags(title_m.group(1))) if title_m else ''
        jb_m = re.search(r'href="(/jb/[0-9a-f]+)"', ch)
        cards.append({
            'title': title[:90],
            'company': grab('p-result_company')[:60],
            'area': grab('p-result_area'),
            'pay': grab('p-result_pay'),
            'emp': grab('p-result_employType'),
            'jb': (BASE + jb_m.group(1)) if jb_m else '',
        })
    return [c for c in cards if c['title']]

def onsite_keep(c):
    t = c['title'] + ' ' + c['company']
    if NG.search(t) or AGE_NG.search(t): return False
    a = c['area']
    w = re.search(r'徒歩(\d+)分', a)
    if w: return int(w.group(1)) <= 12 and '板宿駅' in a
    return any(x in a for x in TOWNS)

def remote_keep(c):
    t = c['title'] + ' ' + c['company']
    if NG.search(t) or VOICE_NG.search(t) or AGE_NG.search(t): return False
    return True

def dedupe(cards):
    seen, out = set(), []
    for c in cards:
        k = (c['title'][:32], c['company'])
        if k in seen: continue
        seen.add(k); out.append(c)
    return out

def verify(card):
    """詳細ページで実在・勤務地検証。return (mark, note) / None=除外"""
    if not card['jb']: return ('△未確認', '')
    body = fetch(card['jb'])
    if not body: return ('△未確認', '詳細ページ取得失敗')
    text = strip_tags(body)
    if re.search(r'掲載を?終了|募集は?終了', text): log(f"CLOSED: {card['title'][:40]}"); return None
    mi = text.find('兵庫県')
    if mi < 0: mi = text.find('神戸市')
    addr = re.sub(r'\s+', '', text[mi:mi+100]) if mi >= 0 else ''
    if not addr:
        log(f"ADDR_UNKNOWN: {card['title'][:40]}")
        return ('△未確認', '勤務地の記載を確認できず')
    if ('須磨区' not in addr and '板宿' not in addr and '西代' not in addr and '東須磨' not in addr):
        log(f"GEO_MISMATCH: {card['title'][:40]} addr={addr[:40]}")
        card['mismatch'] = addr[:50]
        return None
    return ('✔確認済', addr[:50])

def category(c):
    t = c['title']
    if re.search(r'事務|データ入力|庶務|経理|総務|歯科助手|秘書|バックオフィス', t): return '事務・オフィス系'
    if re.search(r'塾|講師|採点|チューター|個別指導|英語インストラクター|英会話|試験監督', t): return '塾講師・教育系'
    if re.search(r'買取|査定|リユース|リサイクル', t): return '買取・リユース系'
    return '販売・サービス・その他'

def main():
    log(f'=== start {DATE} ===')
    # --- 1) 板宿駅1km onsite ---
    onsite_raw = []
    for pg in range(1, 15):
        h = fetch(ONSITE_URL + (f'?pg={pg}' if pg > 1 else ''))
        if not h:
            warn(f'onsite fetch empty pg={pg}')
            break
        cs = parse_cards(h)
        if not cs:
            if pg == 1: warn(f'onsite parse zero pg=1 html_len={len(h)}')
            break
        onsite_raw += cs
        time.sleep(1.2)
    onsite = dedupe([c for c in onsite_raw if onsite_keep(c)])
    # 買取キーワード補完走査
    h = fetch(BASE + '/%E8%B2%B7%E5%8F%96%E3%81%AE%E4%BB%95%E4%BA%8B-%E7%A5%9E%E6%88%B8%E5%B8%82%E6%9D%BF%E5%AE%BF%E9%A7%85')
    if h:
        extra = [c for c in parse_cards(h) if onsite_keep(c) or ('買取' in c['title'] and ('板宿' in c['area'] or any(x in c['area'] for x in TOWNS)))]
        onsite = dedupe(onsite + extra)
    log(f'onsite raw={len(onsite_raw)} kept={len(onsite)}')
    if not onsite_raw:
        raise RuntimeError(f'板宿側の取得が0件 — 求人ボックス構造変更/ブロックの疑い (warnings={WARNINGS})')
    # 検証（jbリンク持ちのみ、最大15件）
    excluded = []
    verified = []
    jb_checked = 0
    for c in onsite:
        if c['jb'] and jb_checked < 15:
            jb_checked += 1
            r = verify(c)
            time.sleep(1.0)
            if r is None:
                excluded.append(c); continue
            c['mark'], c['note'] = r
        else:
            c['mark'], c['note'] = '△未確認', ''
        verified.append(c)
    onsite = verified

    # --- 2) 在宅・声を出さない事務系 ---
    remote = []
    seen_keys = set()
    for label, url in REMOTE_URLS:
        for pg in (1, 2):
            h = fetch(url + (f'?pg={pg}' if pg > 1 else ''))
            if not h:
                warn(f'remote fetch empty {label} pg={pg}')
                break
            cs = parse_cards(h)
            if not cs and pg == 1:
                warn(f'remote parse zero {label} pg=1 html_len={len(h)}')
            for c in cs:
                if not remote_keep(c): continue
                k = (c['title'][:32], c['company'])
                if k in seen_keys: continue
                seen_keys.add(k)
                c['pri'] = '神戸市' if '神戸市' in c['area'] else label
                c['src'] = url
                remote.append(c)
            time.sleep(1.2)
        if len(remote) >= 40: break
    remote = [c for c in remote if c['pri'] == '神戸市'] + [c for c in remote if c['pri'] != '神戸市']
    remote = remote[:40]
    log(f'remote kept={len(remote)}')

    # --- 3) レポート生成 ---
    cats = {}
    for c in onsite: cats.setdefault(category(c), []).append(c)
    total = len(onsite) + len(remote)
    if total == 0:
        raise RuntimeError(f'抽出結果が0件 — 0件の正常レポートは出さない (warnings={WARNINGS})')
    n_ok = sum(1 for c in onsite if c['mark'].startswith('✔'))
    L = []
    L.append(f'# 求人サーチレポート（{DATE}）\n')
    L.append(f'作成: {DATE} 04:30 JST 自動生成（Mac/Claude製スクリプト。求人ボックス実走査・Codex不使用）')
    L.append('条件: 板宿駅 約1km（徒歩約12分）・資格/免許必須職除外・福祉/飲食除外・50代不可除外。在宅可は「声を出さない」事務系のみ。\n')
    L.append('## サマリー\n')
    L.append(f'- 板宿駅 約1km（資格不要・全職種）: **{len(onsite)}件**（✔確認済 {n_ok} / △未確認 {len(onsite)-n_ok}）')
    L.append(f'- 在宅可・声を出さない事務系: **{len(remote)}件**（神戸市 {sum(1 for c in remote if c["pri"]=="神戸市")} / 兵庫県内 {sum(1 for c in remote if c["pri"]!="神戸市")}）')
    L.append(f'- 合計: **{total}件**\n')
    L.append(f'## 板宿駅 約1km の求人（{len(onsite)}件）\n')
    L.append('△のURLは検索結果ページ（https://xn--pckua2a7gp15o89zb.com/神戸市板宿駅での仕事 ）から各カードを参照。\n')
    for cat in ['事務・オフィス系', '塾講師・教育系', '買取・リユース系', '販売・サービス・その他']:
        rows = cats.get(cat, [])
        if not rows: continue
        L.append(f'### {cat}（{len(rows)}件）\n')
        L.append('| 確認 | 職種 | 会社名 | 勤務地 | 雇用形態 | 給与 | URL |')
        L.append('|---|---|---|---|---|---|---|')
        for c in rows:
            url = c['jb'] if (c['jb'] and c['mark'].startswith('✔')) else '検索ページ'
            L.append(f"| {c['mark']} | {c['title'][:60]} | {c['company'] or '（媒体掲載）'} | {c['area'][:45]} | {c['emp']} | {c['pay'][:35]} | {url} |")
        L.append('')
    L.append(f'## 在宅可・声を出さない事務系（{len(remote)}件）\n')
    L.append('電話応対が主業務の求人（コールセンター/CS/受付等）は除外済み。在宅実態（研修・機材・定例出社）は応募前に各詳細で要確認。\n')
    L.append('| 確認 | 優先 | 職種 | 会社名 | 勤務地表記 | 雇用形態 | 給与 | URL |')
    L.append('|---|---|---|---|---|---|---|---|')
    for c in remote:
        L.append(f"| △未確認 | {c['pri']} | {c['title'][:55]} | {c['company'] or '（媒体掲載）'} | {c['area'][:40]} | {c['emp']} | {c['pay'][:35]} | {c['jb'] or c['src']} |")
    L.append('')
    if excluded:
        L.append('## 検証で除外した求人（詳細ページとの矛盾・掲載終了）\n')
        for c in excluded:
            L.append(f"- {c['title'][:50]}（{c['company']}）: {c.get('mismatch','掲載終了')}")
        L.append('')
    if WARNINGS:
        L.append('## ⚠️ 実行警告（取得が部分的だった可能性あり）\n')
        for w in WARNINGS: L.append(f'- {w}')
        L.append('')
    L.append('## 注記\n')
    L.append('- 恒久除外: 介護・福祉/障がい福祉支援職/飲食/資格・免許必須職（看護・薬剤・保育士・美容師等）/50代不可明記/新卒限定。')
    L.append('- 応募の代行はしない（リスト化のみ）。個人情報は記載しない。誇張せず実在情報のみ。\n')
    report = '\n'.join(L)
    out = os.path.join(REPO, 'reports', f'job-report-{DATE}.md')
    with open(out, 'w') as f: f.write(report)
    log(f'REPORT_OK {out} ({len(report)} chars, total={total})')

    # --- 4) push & email ---
    if os.environ.get('JS_NO_PUSH'):
        log('NO_PUSH (test mode)'); return
    g = ['git', '-C', REPO, '-c', 'user.name=wirelessml', '-c', 'user.email=wirelessml@gmail.com']
    # 当日レポートを先に commit してから rebase する。旧実装は pull --rebase を add より前に
    # 実行しており、作業ツリーに未sta変更（テスト再生成の残骸など）が1つでもあると pull が
    # rc=128 で恒久失敗 → run_cmd が FATAL 化して push/メールに到達しなかった（2026-06-14〜19
    # のサイレント停止の原因、2026-06-19 修正）。--autostash は想定外の未sta変更への保険。
    run_cmd(['git', '-C', REPO, 'add', 'reports'], timeout=30)
    has_changes = subprocess.run(['git', '-C', REPO, 'diff', '--cached', '--quiet'], timeout=30).returncode != 0
    if has_changes:
        run_cmd(g + ['commit', '-q', '-m', f'report: {DATE} (mac-claude)'], timeout=30)
    run_cmd(['git', '-C', REPO, 'pull', '-q', '--rebase', '--autostash'], timeout=60)
    if has_changes:
        run_cmd(['git', '-C', REPO, 'push', '-q'], timeout=120)
        log('PUSHED')
    else:
        log('NO_CHANGE (nothing to commit)')
    if not os.environ.get('JS_NO_EMAIL'):
        run_cmd(['/bin/bash', os.path.join(SELF_DIR, 'email-job-report.sh')], timeout=120)
        log('EMAIL_TRIGGERED')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        log(f'FATAL {e!r}')
        sys.exit(1)
