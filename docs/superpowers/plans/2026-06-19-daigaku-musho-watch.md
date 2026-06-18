# 大学無償化ウォッチ Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 「大学無償化」関連の国会発言＋ニュースを毎朝自動収集し、新着のみ claude(Haiku) で要約してメールする日次ダイジェストを作る。

**Architecture:** 単一スクリプト `seimu_watch_daily.py`。純粋関数（パース・dedup・プロンプト生成・要約パース・レポート整形）と I/O（HTTP取得・claude CLI・メール・状態ファイル）を分離。pure 関数を pytest で TDD、I/O は dry-run で結合確認。GitHub 不使用。`job-search-daily.py` を雛形に既存メール基盤を流用。

**Tech Stack:** Python3（標準ライブラリのみ: urllib / json / xml.etree / subprocess）、claude standalone CLI（Haiku）、send-email.py（既存）、LaunchAgent。

## Global Constraints

- 依存は **標準ライブラリのみ**（pip 追加なし）。実行は `/usr/bin/python3`。
- 実行ファイル一式は `~/Library/Application Support/seimu-watch/` に置く（launchd TCC 罠回避）。**git 正本は `scripts/`**、編集後 cp で同期。
- claude 実体は `~/.local/bin/claude`、モデルは `claude-haiku-4-5-20251001`。
- メールは既存 `send-email.py`＋`~/.config/masu-p-watch/email.json` を流用（新規シークレット不要）。宛先 `wirelessml@gmail.com`。
- **GitHub push なし**。
- 新着0件 → メール送らない（ログのみ）。取得全滅 → 警告。claude 失敗 → 要約なしで送る。
- ユーザー向け文字列は日本語。スケジュール毎日 06:00、LaunchAgent `com.yuika.seimu-watch`。
- スクリプト名はテスト import 可能にするため**アンダースコア** `seimu_watch_daily.py`（設計書の `seimu-watch-daily.py` から変更。LaunchAgent はフルパス実行なので影響なし）。
- pure 関数を持つモジュールは import 時に副作用を出さない（実行は `if __name__=='__main__':` 配下のみ）。

---

## File Structure

- `scripts/seimu_watch_daily.py` — 本体（git 正本）。consts＋pure 関数＋I/O＋main。
- `tests/test_seimu_watch.py` — pure 関数の pytest。
- `config/launchagents/com.yuika.seimu-watch.plist` — LaunchAgent 定義（git 正本、bootstrap 用）。
- デプロイ先（git 外）: `~/Library/Application Support/seimu-watch/{seimu_watch_daily.py, send-email.py, reports/, seen-speech-ids.txt, seen-news-urls.txt, seimu-watch.log}`、`~/Library/LaunchAgents/com.yuika.seimu-watch.plist`。

---

## Task 1: スケルトン＋定数＋国会APIレスポンスのパース

**Files:**
- Create: `scripts/seimu_watch_daily.py`
- Test: `tests/test_seimu_watch.py`

**Interfaces:**
- Produces: `parse_kokkai_response(data: dict) -> list[dict]`。各 dict は `{'id','date','house','meeting','speaker','text','url'}`（全て str）。

- [ ] **Step 1: 失敗するテストを書く**

`tests/test_seimu_watch.py`:
```python
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
import seimu_watch_daily as sw

def test_parse_kokkai_response_extracts_fields():
    data = {"speechRecord": [
        {"speechID": "ABC123", "date": "2026-03-15", "nameOfHouse": "衆議院",
         "nameOfMeeting": "文部科学委員会", "speaker": "山田太郎",
         "speech": "○山田太郎君 大学無償化について…", "speechURL": "https://kokkai.ndl.go.jp/x"}]}
    out = sw.parse_kokkai_response(data)
    assert len(out) == 1
    assert out[0]["id"] == "ABC123"
    assert out[0]["meeting"] == "文部科学委員会"
    assert out[0]["url"].startswith("https://kokkai.ndl.go.jp")

def test_parse_kokkai_response_empty():
    assert sw.parse_kokkai_response({}) == []
```

- [ ] **Step 2: テストが失敗することを確認**

Run: `python3 -m pytest tests/test_seimu_watch.py -q`
Expected: FAIL（`ModuleNotFoundError` または `AttributeError: parse_kokkai_response`）

- [ ] **Step 3: スケルトン＋関数を実装**

`scripts/seimu_watch_daily.py`:
```python
#!/usr/bin/env python3
"""大学無償化ウォッチ 日次ダイジェスト。
国会会議録API＋Google News RSS から新着を収集→claude(Haiku)要約→メール。
job-search-daily の堅牢化教訓を反映（TCC回避・fail-loud・0件正常）。GitHub不使用。
環境変数: SW_DRY_RUN=1（メール/状態更新せず標準出力）、SW_NO_EMAIL=1。
"""
import os, json, datetime, subprocess, urllib.request
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
WINDOW_DAYS = 45
MAX_ITEMS = 40


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
```

- [ ] **Step 4: テストが通ることを確認**

Run: `python3 -m pytest tests/test_seimu_watch.py -q`
Expected: PASS（2 passed）

- [ ] **Step 5: コミット**

```bash
git add scripts/seimu_watch_daily.py tests/test_seimu_watch.py
git commit -m "feat(seimu-watch): 国会APIレスポンスのパース＋スケルトン"
```

---

## Task 2: Google News RSS のパース

**Files:**
- Modify: `scripts/seimu_watch_daily.py`
- Test: `tests/test_seimu_watch.py`

**Interfaces:**
- Produces: `parse_news_rss(xml_text: str) -> list[dict]`。各 dict は `{'id','date','source','title','url'}`。`id` は guid（無ければ link）。

- [ ] **Step 1: 失敗するテストを書く**

`tests/test_seimu_watch.py` に追記:
```python
def test_parse_news_rss_extracts_items():
    xml = '''<?xml version="1.0"?><rss version="2.0"><channel>
    <item><title>大学無償化を拡大へ - 朝日新聞</title>
    <link>https://news.google.com/rss/articles/AAA</link>
    <guid isPermaLink="false">guid-AAA</guid>
    <pubDate>Wed, 18 Jun 2026 09:00:00 GMT</pubDate>
    <source url="https://asahi.com">朝日新聞</source></item>
    </channel></rss>'''
    out = sw.parse_news_rss(xml)
    assert len(out) == 1
    assert out[0]["id"] == "guid-AAA"
    assert out[0]["source"] == "朝日新聞"
    assert out[0]["url"] == "https://news.google.com/rss/articles/AAA"

def test_parse_news_rss_empty_channel():
    assert sw.parse_news_rss('<rss><channel></channel></rss>') == []
```

- [ ] **Step 2: テストが失敗することを確認**

Run: `python3 -m pytest tests/test_seimu_watch.py::test_parse_news_rss_extracts_items -q`
Expected: FAIL（`AttributeError: parse_news_rss`）

- [ ] **Step 3: 実装を追記**

`scripts/seimu_watch_daily.py` の `parse_kokkai_response` の後に追記:
```python
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
```

- [ ] **Step 4: テストが通ることを確認**

Run: `python3 -m pytest tests/test_seimu_watch.py -q`
Expected: PASS（4 passed）

- [ ] **Step 5: コミット**

```bash
git add scripts/seimu_watch_daily.py tests/test_seimu_watch.py
git commit -m "feat(seimu-watch): Google News RSS のパース"
```

---

## Task 3: 既出除外（dedup）

**Files:**
- Modify: `scripts/seimu_watch_daily.py`
- Test: `tests/test_seimu_watch.py`

**Interfaces:**
- Produces:
  - `filter_new(items: list[dict], seen: set) -> list[dict]`（`id` が seen に無いものだけ返す。`id` 空は除外）
  - `dedup_by_id(items: list[dict]) -> list[dict]`（同一 run 内の id 重複を先勝ちで除去）

- [ ] **Step 1: 失敗するテストを書く**

```python
def test_filter_new_excludes_seen_and_empty():
    items = [{"id": "a"}, {"id": "b"}, {"id": ""}]
    assert sw.filter_new(items, {"a"}) == [{"id": "b"}]

def test_dedup_by_id_keeps_first():
    items = [{"id": "a", "n": 1}, {"id": "a", "n": 2}, {"id": "b", "n": 3}]
    out = sw.dedup_by_id(items)
    assert [x["id"] for x in out] == ["a", "b"]
    assert out[0]["n"] == 1
```

- [ ] **Step 2: テストが失敗することを確認**

Run: `python3 -m pytest tests/test_seimu_watch.py -q`
Expected: FAIL（`AttributeError: filter_new`）

- [ ] **Step 3: 実装を追記**

```python
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
```

- [ ] **Step 4: テストが通ることを確認**

Run: `python3 -m pytest tests/test_seimu_watch.py -q`
Expected: PASS（6 passed）

- [ ] **Step 5: コミット**

```bash
git add scripts/seimu_watch_daily.py tests/test_seimu_watch.py
git commit -m "feat(seimu-watch): 既出除外 filter_new / dedup_by_id"
```

---

## Task 4: 要約プロンプト生成＋claude出力(JSON)のパース

**Files:**
- Modify: `scripts/seimu_watch_daily.py`
- Test: `tests/test_seimu_watch.py`

**Interfaces:**
- Consumes: speeches/articles dict（Task1/2 形式）＋ `key`（`'S1'`,`'N1'`…）が付与済み。
- Produces:
  - `build_summary_prompt(speeches: list[dict], articles: list[dict]) -> str`
  - `parse_summary_json(stdout: str) -> dict | None`（`{'overall': str, 'items': {key: str}}`。抽出/JSON失敗で `None`）

- [ ] **Step 1: 失敗するテストを書く**

```python
def test_build_summary_prompt_contains_keys_and_text():
    sp = [{"key": "S1", "date": "2026-03-15", "house": "衆議院",
           "meeting": "文科委", "speaker": "山田", "text": "大学無償化の本文"}]
    ar = [{"key": "N1", "date": "2026-06-18", "source": "朝日", "title": "無償化拡大"}]
    p = sw.build_summary_prompt(sp, ar)
    assert "S1" in p and "N1" in p
    assert "大学無償化の本文" in p and "無償化拡大" in p
    assert "JSON" in p

def test_parse_summary_json_extracts_object_in_prose():
    out = 'これが結果です:\n{"overall":"要点","items":{"S1":"発言要約","N1":"記事要約"}}\n以上'
    d = sw.parse_summary_json(out)
    assert d["overall"] == "要点"
    assert d["items"]["S1"] == "発言要約"

def test_parse_summary_json_bad_returns_none():
    assert sw.parse_summary_json("要約できませんでした") is None
    assert sw.parse_summary_json("") is None
```

- [ ] **Step 2: テストが失敗することを確認**

Run: `python3 -m pytest tests/test_seimu_watch.py -q`
Expected: FAIL（`AttributeError: build_summary_prompt`）

- [ ] **Step 3: 実装を追記**

```python
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
```

- [ ] **Step 4: テストが通ることを確認**

Run: `python3 -m pytest tests/test_seimu_watch.py -q`
Expected: PASS（9 passed）

- [ ] **Step 5: コミット**

```bash
git add scripts/seimu_watch_daily.py tests/test_seimu_watch.py
git commit -m "feat(seimu-watch): 要約プロンプト生成＋claude JSON出力パース"
```

---

## Task 5: ダイジェスト整形（render_digest）

**Files:**
- Modify: `scripts/seimu_watch_daily.py`
- Test: `tests/test_seimu_watch.py`

**Interfaces:**
- Consumes: keyed speeches/articles＋summaries（`parse_summary_json` 形式 or `None`）。
- Produces: `render_digest(date: str, speeches: list[dict], articles: list[dict], summaries: dict | None) -> str`（Markdown）。

- [ ] **Step 1: 失敗するテストを書く**

```python
def _sp():
    return [{"key": "S1", "date": "2026-03-15", "house": "衆議院",
             "meeting": "文科委", "speaker": "山田", "text": "x", "url": "https://k/x"}]
def _ar():
    return [{"key": "N1", "date": "2026-06-18", "source": "朝日",
             "title": "無償化拡大", "url": "https://n/a"}]

def test_render_digest_with_summaries():
    md = sw.render_digest("2026-06-19", _sp(), _ar(),
                          {"overall": "要点X", "items": {"S1": "発言要約", "N1": "記事要約"}})
    assert "新着2件" in md and "要点X" in md
    assert "発言要約" in md and "https://k/x" in md
    assert "記事要約" in md and "https://n/a" in md

def test_render_digest_fallback_when_no_summary():
    md = sw.render_digest("2026-06-19", _sp(), _ar(), None)
    assert "(要約なし)" in md          # 発言は要約なし表記
    assert "無償化拡大" in md          # ニュースは見出しで代替
    assert "https://k/x" in md

def test_render_digest_zero_items():
    md = sw.render_digest("2026-06-19", [], [], None)
    assert "新着なし" in md
    assert "本日新着なし" in md
```

- [ ] **Step 2: テストが失敗することを確認**

Run: `python3 -m pytest tests/test_seimu_watch.py -q`
Expected: FAIL（`AttributeError: render_digest`）

- [ ] **Step 3: 実装を追記**

```python
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
```

- [ ] **Step 4: テストが通ることを確認**

Run: `python3 -m pytest tests/test_seimu_watch.py -q`
Expected: PASS（12 passed）

- [ ] **Step 5: コミット**

```bash
git add scripts/seimu_watch_daily.py tests/test_seimu_watch.py
git commit -m "feat(seimu-watch): ダイジェスト整形 render_digest（要約/フォールバック/0件）"
```

---

## Task 6: I/O層＋main オーケストレーション＋ドライラン確認

**Files:**
- Modify: `scripts/seimu_watch_daily.py`

**Interfaces:**
- Consumes: Task1-5 の全 pure 関数。
- Produces（I/O・テストは dry-run 結合で確認）:
  - `http_get(url, timeout=30) -> str` / `fetch_kokkai(keyword, frm, until, maximum=50) -> dict` / `fetch_news(keyword) -> str`
  - `run_claude(prompt, timeout=120) -> str | None`
  - `send_email(subject, body_path) -> int`
  - `load_seen(path) -> set` / `save_seen(path, ids: set)` / `log(msg)`
  - `main()`

- [ ] **Step 1: I/O 関数と main を追記**

`scripts/seimu_watch_daily.py` の末尾（pure 関数の後）に追記:
```python
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
            speeches += parse_kokkai_response(fetch_kokkai(kw, frm, until)); fetch_ok = True
        except Exception as e:
            log(f'KOKKAI_FAIL {kw} {e}')
        try:
            articles += parse_news_rss(fetch_news(kw)); fetch_ok = True
        except Exception as e:
            log(f'NEWS_FAIL {kw} {e}')

    if not fetch_ok:
        log('FETCH_TOTAL_FAIL')
        if not os.environ.get('SW_DRY_RUN') and not os.environ.get('SW_NO_EMAIL'):
            tmp = os.path.join(SELF_DIR, 'reports', f'{until}.md')
            os.makedirs(os.path.dirname(tmp), exist_ok=True)
            with open(tmp, 'w') as f:
                f.write('取得が全滅しました（ネットワーク/API異常の疑い）。ログを確認してください。\n')
            send_email(f'⚠️【大学無償化ウォッチ】{until} 取得失敗', tmp)
        return

    speeches, articles = dedup_by_id(speeches), dedup_by_id(articles)
    seen_s, seen_n = load_seen(SEEN_SPEECH), load_seen(SEEN_NEWS)
    new_s = filter_new(speeches, seen_s)[:MAX_ITEMS]
    new_n = filter_new(articles, seen_n)[:MAX_ITEMS]
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
```

- [ ] **Step 2: py_compile で構文確認**

Run: `python3 -m py_compile scripts/seimu_watch_daily.py && echo OK`
Expected: `OK`

- [ ] **Step 3: pure 関数テストが壊れていないか確認**

Run: `python3 -m pytest tests/test_seimu_watch.py -q`
Expected: PASS（12 passed）

- [ ] **Step 4: claude CLI の stdin 受理を確認**

Run: `printf '次の文を5文字で要約: 大学無償化の議論が進んでいる' | ~/.local/bin/claude -p --model claude-haiku-4-5-20251001`
Expected: 短い日本語の要約が標準出力に出る（exit 0）。
※ 出ない/エラーなら `run_claude` を引数渡し `[CLAUDE_BIN,'-p',prompt,'--model',HAIKU_MODEL]` に変更し再確認。

- [ ] **Step 5: ドライラン結合確認（実 API・メールなし）**

Run: `SW_DRY_RUN=1 python3 scripts/seimu_watch_daily.py`
Expected: 標準出力に `# 【大学無償化ウォッチ】YYYY-MM-DD …` のダイジェスト。`~/Library/Application Support/seimu-watch/seimu-watch.log` に `REPORT n=…`。`seen-*.txt` は未更新（dry-run）。
※ 国会APIが0件でもニュース側が出ること、`KOKKAI_FAIL`/`NEWS_FAIL` がログに無いことを確認。`any` パラメータでエラーなら API 仕様（横断キーワード名）を `kokkai.ndl.go.jp/api.html` で確認し修正。

- [ ] **Step 6: コミット**

```bash
git add scripts/seimu_watch_daily.py
git commit -m "feat(seimu-watch): I/O層＋main（取得→dedup→要約→整形→メール、dry-run/0件/fail-loud）"
```

---

## Task 7: デプロイ（App Support 配置・送信スクリプト・LaunchAgent 06:00）

**Files:**
- Create: `config/launchagents/com.yuika.seimu-watch.plist`
- Modify: `scripts/launchagents-expected.txt`（存在すれば）

**Interfaces:** なし（運用デプロイ）。

- [ ] **Step 1: App Support へ配置＋送信スクリプト流用**

```bash
mkdir -p "$HOME/Library/Application Support/seimu-watch/reports"
cp scripts/seimu_watch_daily.py "$HOME/Library/Application Support/seimu-watch/seimu_watch_daily.py"
cp "$HOME/Library/Application Support/job-report/send-email.py" "$HOME/Library/Application Support/seimu-watch/send-email.py"
```
Expected: エラーなし。`send-email.py` は既存の job-report 版（`~/.config/masu-p-watch/email.json` を読む）。

- [ ] **Step 2: plist を作成（git 正本）**

`config/launchagents/com.yuika.seimu-watch.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.yuika.seimu-watch</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>/Users/yuika/Library/Application Support/seimu-watch/seimu_watch_daily.py</string>
  </array>
  <key>StartCalendarInterval</key>
  <dict><key>Hour</key><integer>6</integer><key>Minute</key><integer>0</integer></dict>
  <key>StandardOutPath</key><string>/tmp/seimu-watch-launchd.log</string>
  <key>StandardErrorPath</key><string>/tmp/seimu-watch-launchd-error.log</string>
</dict>
</plist>
```

- [ ] **Step 3: plist を配置してロード**

```bash
cp config/launchagents/com.yuika.seimu-watch.plist "$HOME/Library/LaunchAgents/com.yuika.seimu-watch.plist"
launchctl unload "$HOME/Library/LaunchAgents/com.yuika.seimu-watch.plist" 2>/dev/null
launchctl load "$HOME/Library/LaunchAgents/com.yuika.seimu-watch.plist"
launchctl list | grep seimu-watch
```
Expected: `com.yuika.seimu-watch` が一覧に出る（PID は `-`、status 0）。

- [ ] **Step 4: 手動キックで本番経路を1回確認（メール送信あり）**

```bash
launchctl kickstart -k gui/$(id -u)/com.yuika.seimu-watch
sleep 60
tail -8 "$HOME/Library/Application Support/seimu-watch/seimu-watch.log"
```
Expected: `REPORT n=…` と、新着があれば `EMAIL rc=0`／無ければ `NO_NEW (email skipped)`。新着ありなら `wirelessml@gmail.com` に `【大学無償化ウォッチ】…` 着信。`seen-*.txt` が生成される。

- [ ] **Step 5: 期待リストへ追加（存在すれば）**

`scripts/launchagents-expected.txt` に `com.yuika.seimu-watch` の行を追加（launchagent-doctor の突合用）。無ければスキップ。
Run: `bash scripts/launchagent-doctor.sh 2>/dev/null | tail -5 || true`

- [ ] **Step 6: コミット**

```bash
git add config/launchagents/com.yuika.seimu-watch.plist scripts/launchagents-expected.txt
git commit -m "feat(seimu-watch): LaunchAgent 06:00 デプロイ（plist・期待リスト）"
```

---

## Self-Review

**1. Spec coverage:**
- 議事録＋ニュース → Task1/2/6 ✓ ／ 既出除外 → Task3/6 ✓ ／ claude(Haiku)要約・1回/日・フォールバック → Task4/6 ✓ ／ 出力フォーマット・0件「本日新着なし」 → Task5 ✓ ／ メール＋ローカル保存・GitHubなし → Task6 ✓ ／ 0件メール抑止 → Task6 ✓ ／ 06:00・TCC回避・状態ファイル → Task6/7 ✓ ／ 取得全滅警告・二重送信(seen-id)・fail-loud → Task6 ✓ ／ dry-run → Task6 ✓。spec 全項目に対応タスクあり。
- spec の `last-sent-date.txt` は **seen-id dedup が同等機能（2回目実行=新着0=送信なし）を提供するため不採用**（YAGNI）。
**2. Placeholder scan:** TBD/TODO/曖昧表現なし。各コードステップに完全な実装あり。
**3. Type consistency:** dict キー（id/date/house/meeting/speaker/text/url ・ id/date/source/title/url ・ key='S{n}'/'N{n}' ・ summaries={'overall','items':{key:str}}）が Task1-6 で一貫。関数名 parse_kokkai_response / parse_news_rss / filter_new / dedup_by_id / build_summary_prompt / parse_summary_json / render_digest / http_get / fetch_kokkai / fetch_news / run_claude / send_email / load_seen / save_seen / main で一貫。
