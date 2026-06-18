#!/usr/bin/env python3
"""大学無償化ウォッチ 日次ダイジェスト。
国会会議録API＋Google News RSS から新着を収集→claude(Haiku)要約→メール。
job-search-daily の堅牢化教訓を反映（TCC回避・fail-loud・0件正常）。GitHub不使用。
環境変数: SW_DRY_RUN=1（メール/状態更新せず標準出力）、SW_NO_EMAIL=1、SW_SEED=1（既読ベースライン作成）。
"""
import os
import json
import datetime
import subprocess
import urllib.request
from urllib.parse import urlencode, quote
import xml.etree.ElementTree as ET

SELF_DIR = os.path.expanduser('~/Library/Application Support/seimu-watch')
REPORTS = os.path.join(SELF_DIR, 'reports')
SEEN_SPEECH = os.path.join(SELF_DIR, 'seen-speech-ids.txt')
SEEN_NEWS = os.path.join(SELF_DIR, 'seen-news-urls.txt')
LOG = os.path.join(SELF_DIR, 'seimu-watch.log')
SENDER = os.path.join(SELF_DIR, 'send-email.py')
CLAUDE_BIN = os.path.expanduser('~/.local/bin/claude')
HAIKU_MODEL = 'claude-haiku-4-5-20251001'
PY = '/usr/bin/python3'
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) seimu-watch/1.0'
KEYWORDS = ['大学無償化', '高等教育無償化', '授業料無償化', '高等教育の修学支援新制度']
WINDOW_DAYS = 365          # 国会は該当発言が疎なため広め（dedupで重複報告は防ぐ）
MAX_ITEMS = 40
MAX_SPEECH_ITEMS = 20
MAX_PER_SOURCE = 3         # 同一媒体の量産ページ（例: イクハクの地域別テンプレ）の氾濫を抑制


# --- pure: parsing -------------------------------------------------------
def parse_kokkai_response(data):
    out = []
    for r in (data.get('speechRecord') or []):
        out.append({
            'id': r.get('speechID', ''),
            'date': r.get('date', ''),
            'house': r.get('nameOfHouse', ''),
            'meeting': r.get('nameOfMeeting', ''),
            'speaker': r.get('speaker', ''),
            'text': (r.get('speech') or '').strip(),
            'url': r.get('speechURL', ''),
        })
    return out


def parse_news_rss(xml_text):
    out = []
    root = ET.fromstring(xml_text)
    for item in root.iterfind('.//item'):
        def t(tag):
            e = item.find(tag)
            return (e.text or '').strip() if e is not None and e.text else ''
        src_e = item.find('source')
        out.append({
            'id': t('guid') or t('link'),
            'date': t('pubDate'),
            'source': (src_e.text.strip() if src_e is not None and src_e.text else ''),
            'title': t('title'),
            'url': t('link'),
        })
    return out


# --- pure: dedup ---------------------------------------------------------
def filter_new(items, seen):
    return [it for it in items if it.get('id') and it['id'] not in seen]


def dedup_by_id(items):
    seen, out = set(), []
    for it in items:
        k = it.get('id')
        if k and k not in seen:
            seen.add(k)
            out.append(it)
    return out


def limit_per_source(items, max_per_source=MAX_PER_SOURCE):
    counts, out = {}, []
    for it in items:
        source = (it.get('source') or it.get('url') or it.get('id') or '').strip()
        if not source:
            out.append(it)
            continue
        count = counts.get(source, 0)
        if count >= max_per_source:
            continue
        counts[source] = count + 1
        out.append(it)
    return out


def cap_speeches_and_articles(speeches, articles, max_items=MAX_ITEMS, max_speeches=MAX_SPEECH_ITEMS):
    capped_speeches = speeches[:min(max_speeches, max_items)]
    remaining = max(0, max_items - len(capped_speeches))
    return capped_speeches, articles[:remaining]


# --- pure: summary prompt / parse ---------------------------------------
def build_summary_prompt(speeches, articles):
    lines = [
        '以下は「大学無償化」関連の国会発言とニュースの新着一覧です。',
        '各項目を日本語で1〜2文に要約し、さらに全体の要点を3〜5行でまとめてください。',
        '出力は次の形式のJSONのみ（前後に文章を付けない）:',
        '{"overall":"全体の要点","items":{"S1":"…","N1":"…"}}',
        '',
    ]
    for s in speeches:
        lines.append(f'[{s["key"]}] 国会発言 {s["date"]} {s["house"]}{s["meeting"]} '
                     f'{s["speaker"]}: {s["text"][:1500]}')
    for a in articles:
        lines.append(f'[{a["key"]}] ニュース {a["date"]} {a["source"]} 見出し: {a["title"]}')
    return '\n'.join(lines)


def parse_summary_json(stdout):
    if not stdout:
        return None
    i, j = stdout.find('{'), stdout.rfind('}')
    if i < 0 or j <= i:
        return None
    try:
        d = json.loads(stdout[i:j + 1])
    except Exception:
        return None
    if isinstance(d, dict) and isinstance(d.get('items'), dict):
        d.setdefault('overall', '')
        return d
    return None


# --- pure: render --------------------------------------------------------
def render_digest(date, speeches, articles, summaries):
    n = len(speeches) + len(articles)
    if n == 0:
        return f'# 【大学無償化ウォッチ】{date} 新着なし\n\n本日新着なし。\n'
    items = summaries.get('items', {}) if summaries else {}
    overall = summaries.get('overall', '') if summaries else ''
    L = [f'# 【大学無償化ウォッチ】{date} 新着{n}件', '']
    if overall:
        L += ['## 今日の要点', overall, '']
    if speeches:
        L.append(f'## 国会発言（{len(speeches)}件）')
        for s in speeches:
            summ = items.get(s['key']) or '(要約なし)'
            L.append(f'- [{s["date"]}｜{s["house"]}{s["meeting"]}｜{s["speaker"]}] {summ}　→ {s["url"]}')
        L.append('')
    if articles:
        L.append(f'## ニュース（{len(articles)}件）')
        for a in articles:
            summ = items.get(a['key']) or a['title']
            L.append(f'- [{a["source"]}｜{a["date"]}] {summ}　→ {a["url"]}')
        L.append('')
    return '\n'.join(L)


# --- I/O -----------------------------------------------------------------
def log(msg):
    os.makedirs(SELF_DIR, exist_ok=True)
    with open(LOG, 'a') as f:
        f.write(f'{datetime.datetime.now():%F %T} {msg}\n')


def http_get(url, timeout=30):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept-Language': 'ja'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode('utf-8', 'ignore')


def fetch_kokkai(keyword, frm, until, maximum=50):
    q = urlencode({'any': keyword, 'from': frm, 'until': until,
                   'maximumRecords': maximum, 'recordPacking': 'json'})
    return json.loads(http_get(f'https://kokkai.ndl.go.jp/api/speech?{q}'))


def fetch_news(keyword):
    return http_get(f'https://news.google.com/rss/search?q={quote(keyword)}'
                    f'&hl=ja&gl=JP&ceid=JP:ja')


def run_claude(prompt, timeout=120):
    try:
        cp = subprocess.run([CLAUDE_BIN, '-p', '--model', HAIKU_MODEL],
                            input=prompt, text=True, capture_output=True, timeout=timeout)
        if cp.returncode != 0:
            log(f'CLAUDE_FAIL rc={cp.returncode} {(cp.stderr or "").strip()[:300]}')
            return None
        return cp.stdout
    except Exception as e:
        log(f'CLAUDE_ERR {e}')
        return None


def send_email(subject, body_path):
    cp = subprocess.run([PY, SENDER, '--subject', subject, '--body-file', body_path],
                        capture_output=True, text=True, timeout=120)
    if cp.returncode != 0:
        log(f'EMAIL_FAIL {(cp.stderr or "").strip()[:300]}')
    return cp.returncode


def load_seen(path):
    try:
        with open(path) as f:
            return set(x.strip() for x in f if x.strip())
    except FileNotFoundError:
        return set()


def save_seen(path, ids):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write('\n'.join(sorted(ids)) + '\n')


def main():
    today = datetime.date.today()
    until = today.isoformat()
    frm = (today - datetime.timedelta(days=WINDOW_DAYS)).isoformat()
    log(f'=== start {until} ===')

    speeches, articles, fetch_ok = [], [], False
    for kw in KEYWORDS:
        try:
            speeches += parse_kokkai_response(fetch_kokkai(kw, frm, until))
            fetch_ok = True
        except Exception as e:
            log(f'KOKKAI_FAIL {kw} {e}')
        try:
            articles += parse_news_rss(fetch_news(kw))
            fetch_ok = True
        except Exception as e:
            log(f'NEWS_FAIL {kw} {e}')

    if not fetch_ok:
        log('FETCH_TOTAL_FAIL')
        if not os.environ.get('SW_DRY_RUN') and not os.environ.get('SW_NO_EMAIL'):
            os.makedirs(REPORTS, exist_ok=True)
            tmp = os.path.join(REPORTS, f'{until}.md')
            with open(tmp, 'w') as f:
                f.write('取得が全滅しました（ネットワーク/API異常の疑い）。ログを確認してください。\n')
            send_email(f'⚠️【大学無償化ウォッチ】{until} 取得失敗', tmp)
        return

    speeches, articles = dedup_by_id(speeches), dedup_by_id(articles)
    seen_s, seen_n = load_seen(SEEN_SPEECH), load_seen(SEEN_NEWS)
    new_s, new_n = cap_speeches_and_articles(
        filter_new(speeches, seen_s),
        limit_per_source(filter_new(articles, seen_n), MAX_PER_SOURCE),
        MAX_ITEMS,
        MAX_SPEECH_ITEMS,
    )

    if os.environ.get('SW_SEED'):
        os.makedirs(REPORTS, exist_ok=True)
        report_path = os.path.join(REPORTS, f'{until}.md')
        with open(report_path, 'w') as f:
            f.write(render_digest(until, [], [], None))
        save_seen(SEEN_SPEECH, seen_s | {s['id'] for s in speeches if s.get('id')})
        save_seen(SEEN_NEWS, seen_n | {a['id'] for a in articles if a.get('id')})
        log(f'SEED speeches={len(speeches)} articles={len(articles)} -> {report_path}')
        if os.environ.get('SW_DRY_RUN'):
            print(f'# 【大学無償化ウォッチ】{until} seed\n\n既存取得分を既読化しました。メール送信なし。')
        return
    for i, s in enumerate(new_s, 1):
        s['key'] = f'S{i}'
    for i, a in enumerate(new_n, 1):
        a['key'] = f'N{i}'
    n = len(new_s) + len(new_n)

    summaries = None
    if n:
        summaries = parse_summary_json(run_claude(build_summary_prompt(new_s, new_n)))
        if summaries is None:
            log('SUMMARY_FALLBACK')

    report = render_digest(until, new_s, new_n, summaries)
    os.makedirs(REPORTS, exist_ok=True)
    report_path = os.path.join(REPORTS, f'{until}.md')
    with open(report_path, 'w') as f:
        f.write(report)
    log(f'REPORT n={n} -> {report_path}')

    if os.environ.get('SW_DRY_RUN'):
        log('DRY_RUN (no email, no seen update)')
        print(report)
        return

    if n == 0:
        log('NO_NEW (email skipped)')
        return
    if os.environ.get('SW_NO_EMAIL'):
        log('NO_EMAIL flag (seen not updated)')
        return

    rc = send_email(f'【大学無償化ウォッチ】{until} 新着{n}件', report_path)
    log(f'EMAIL rc={rc}')
    if rc == 0:  # 送信成功時のみ既読化（失敗時は翌回リトライ）
        save_seen(SEEN_SPEECH, seen_s | {s['id'] for s in new_s})
        save_seen(SEEN_NEWS, seen_n | {a['id'] for a in new_n})


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        log(f'FATAL {e!r}')
        raise
