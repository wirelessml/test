import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
import seimu_watch_daily as sw


# --- Task 1: 国会APIパース ---
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


# --- Task 2: ニュースRSSパース ---
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


# --- Task 3: dedup ---
def test_filter_new_excludes_seen_and_empty():
    items = [{"id": "a"}, {"id": "b"}, {"id": ""}]
    assert sw.filter_new(items, {"a"}) == [{"id": "b"}]


def test_dedup_by_id_keeps_first():
    items = [{"id": "a", "n": 1}, {"id": "a", "n": 2}, {"id": "b", "n": 3}]
    out = sw.dedup_by_id(items)
    assert [x["id"] for x in out] == ["a", "b"]
    assert out[0]["n"] == 1


def test_limit_per_source_caps_but_keeps_order():
    items = (
        [{"id": f"a{i}", "source": "イクハク"} for i in range(4)] +
        [{"id": "b1", "source": "東洋経済オンライン"},
         {"id": "b2", "source": "東洋経済オンライン"}]
    )
    out = sw.limit_per_source(items, 3)
    assert [x["id"] for x in out] == ["a0", "a1", "a2", "b1", "b2"]


def test_limit_per_source_uses_url_when_source_empty():
    items = [{"id": "a", "source": "", "url": "https://n/a"},
             {"id": "b", "source": "", "url": "https://n/b"}]
    assert sw.limit_per_source(items, 1) == items


def test_cap_speeches_and_articles_limits_total_and_speech_share():
    speeches = [{"id": f"s{i}"} for i in range(25)]
    articles = [{"id": f"n{i}"} for i in range(25)]
    out_s, out_n = sw.cap_speeches_and_articles(speeches, articles, max_items=40, max_speeches=20)
    assert len(out_s) == 20
    assert len(out_n) == 20
    assert out_s[-1]["id"] == "s19"
    assert out_n[-1]["id"] == "n19"


def test_cap_speeches_and_articles_uses_news_when_few_speeches():
    speeches = [{"id": "s1"}]
    articles = [{"id": f"n{i}"} for i in range(50)]
    out_s, out_n = sw.cap_speeches_and_articles(speeches, articles, max_items=40, max_speeches=20)
    assert len(out_s) == 1
    assert len(out_n) == 39


# --- Task 4: プロンプト生成 / claude JSON パース ---
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


# --- Task 5: ダイジェスト整形 ---
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
    assert "(要約なし)" in md
    assert "無償化拡大" in md
    assert "https://k/x" in md


def test_render_digest_zero_items():
    md = sw.render_digest("2026-06-19", [], [], None)
    assert "新着なし" in md
    assert "本日新着なし" in md


if __name__ == '__main__':
    # pytest 非依存の自走ランナー（/usr/bin/python3 tests/test_seimu_watch.py）
    import traceback
    fns = [(n, f) for n, f in sorted(globals().items())
           if n.startswith('test_') and callable(f)]
    passed = 0
    for n, f in fns:
        try:
            f()
            passed += 1
            print(f'PASS {n}')
        except Exception:
            print(f'FAIL {n}')
            traceback.print_exc()
    print(f'{passed}/{len(fns)} passed')
    raise SystemExit(0 if passed == len(fns) else 1)
