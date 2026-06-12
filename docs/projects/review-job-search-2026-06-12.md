## 1. 全体評価（3-5行）

本番ジョブとしては、スクレイピング、詳細確認、Markdown生成、GitHub push、メール送信まで1ファイルにまとまっており、日次運用の目的は読み取れます。
一方で、外部HTML変更・一時的な取得失敗・Git/メール失敗が「失敗」として利用者に届かない経路が多く、生命線ルーチンとしては検知設計が不足しています。
最も危険なのは、求人ボックス側の構造変更やブロックでカード抽出が0件になっても、正常な0件レポートとしてpush/メールされる点です。
詳細ページ検証は「ページが取れた」ことを確認済みに寄せすぎており、勤務地抽出不能でも確認済みになるため、geo水増し検出としては弱いです。

## 2. 壊れ方の予測（重要度順）

### 求人ボックス側のHTML/構造変更で最初に割れる箇所

- 最初に割れる可能性が高いのは `parse_cards()` のカード分割です。56行目が `<section ... class="...p-result_card...">` というタグ種別・class名・ダブルクォート前提の正規表現なので、`article`/`div`化、class名変更、シングルクォート化、SSR/JS構造変更でカード数が即0になります。
- 60行目の `grab()` は「指定classを持つ要素の直後から最初の `</p|div|span|h2>` まで」を拾うため、カード内にネストしたタグが入るだけで途中で切れます。給与・勤務地・会社名の一部欠落が起きても例外にならず、後続フィルタが誤判定します。
- 62行目はタイトルを任意の `<h2>` から取っています。タイトルが `<h3>`、`<a>`、`aria-label`、別class付き要素へ移ると `title=''` になり、73行目でカードごと破棄されます。
- 64行目は詳細URLを `href="(/jb/[0-9a-f]+)"` に限定しています。絶対URL、別パス、IDの文字種変更、リダイレクトURL化で `jb=''` になり、98行目で詳細検証が `△未確認` に落ちます。
- 58行目の `ch = ch[:12000]` は、カードHTMLが肥大化した場合に後方の会社名・勤務地・詳細リンクを切り落とす可能性があります。(推測) 広告タグや構造化データがカード内に増えると、この問題が先に出ます。
- 126-127行目と159-160行目は `parse_cards(h)` が0件ならページングを打ち切りますが、「構造変更で0件」と「本当に求人がない」を区別していません。ログにもparse 0件の理由が残りません。

### ネットワーク失敗・タイムアウト・部分取得時の挙動

- `fetch()` は38-46行目で最大3回取得し、最終失敗時に `''` を返します。例外はログに出ますが、呼び出し側では失敗と空ページの区別が消えます。
- 板宿検索の1ページ目が失敗すると、124-125行目で `break` し、`onsite_raw=[]` のまま進みます。これは後続で異常扱いされず、136行目に `onsite raw=0 kept=0` と出るだけです。
- 2ページ目以降の失敗は、124-128行目と158-161行目の構造上「そこまでの部分取得」で正常継続します。メール受信者には部分取得であることが伝わりません。
- 詳細ページ取得失敗は99-100行目で `△未確認` になります。この扱い自体は保守的ですが、全件または大半の詳細取得が失敗しても異常判定はありません。
- HTTP 200でボットブロック、メンテナンス、空HTML、文字化けHTMLが返った場合、42-43行目では成功扱いです。カード抽出0件や勤務地抽出不能に流れ、失敗として止まりません。

### 0件/異常値のときレポートとメールはどうなるか

- `onsite=0`、`remote=0` でも178-187行目で合計0件のレポートが生成され、216-218行目で保存されます。220行目以降のpush/emailにも進むため、silent failureになり得ます。
- `n_ok=0`、つまり詳細検証が全滅しても185行目で `✔確認済 0 / △未確認 N` と出るだけです。異常として件名・本文・終了コードに反映されません。
- 異常に少ない件数の検知がありません。136行目と173行目に件数ログはありますが、前日比・最低件数・取得失敗数によるfail gateがないため、メール本文上は通常レポートに見えます。
- push失敗時も229行目で `PUSH_FAILED` とログするだけで、232-234行目のメール送信へ進みます。メールが「GitHubに反映済み」の前提で運用されているなら、ここは実害があります。
- メール送信スクリプトの戻り値は233行目で確認されません。`email-job-report.sh` がexit 1でも234行目で `EMAIL_TRIGGERED` と記録されます。

## 3. ロジック検査

### 重複排除・二重送信防止の正しさ

- 重複排除キーは91行目の `(title[:32], company)` だけです。同一会社・同一タイトルで勤務地や雇用形態が違う求人は誤って潰れます。逆に同一求人でもタイトル先頭32文字や会社表記が少し揺れると残ります。
- `jb` URLが取れているのにdedupeキーに使っていません。詳細URLが最も強い識別子なので、64行目で取得できた場合はURL正規化後のキーを優先すべきです。
- 在宅側は156-168行目で独自の `seen_keys` を使っていますが、キーは同じくタイトル先頭32文字と会社名です。神戸市検索と兵庫県検索の同一求人排除としては弱いです。
- 二重送信防止は実質ありません。同じ日付で再実行して226行目のcommitが「変更なし」になっても、230-234行目でメールは送られます。LaunchAgentの再実行、手動再実行、前回push済みの再試行で同日メールが重複します。
- `git pull` と `git add` の戻り値は224-225行目で無視されています。pull失敗後にcommit/pushへ進む、add失敗後に「NO_CHANGE」と誤認する経路があります。

### 除外フィルタの漏れパターン

- 除外判定は75-85行目で `title + company` だけを見ています。勤務地、雇用形態、給与欄、詳細本文にだけ「資格必須」「電話対応」「介護施設」等が出る求人は漏れます。
- 資格必須系の表記ゆれに弱いです。29行目の `NG` では、例として `普通自動車免許必須`、`要普免`、`要自動車免許`、`初任者研修`、`実務者研修`、`社会福祉主事`、`サビ管`、`サービス管理責任者` が明示的には拾えません。
- 福祉系では `就労支援`、`障害者支援`、`生活支援`、`デイサービス`、`グループホーム`、`B型`、`A型` などが漏れ候補です。`支援員` は拾えますが、職種名が別表現だと抜けます。
- 飲食系では `厨房`、`洗い場`、`配膳`、`惣菜`、`ベーカリー`、`フード`、`ファストフード`、`調理補助` が漏れ候補です。`調理` は拾えますが、会社名・職種名に出ない場合は抜けます。
- 在宅の声出し除外は30行目の `VOICE_NG` ですが、`受電`、`架電`、`問い合わせ対応`、`お客様対応`、`予約受付`、`コンタクトセンター`、`インサイドセールス`、`オンライン面談` が漏れ候補です。
- 逆に `電話対応なし`、`電話なし`、`メール対応のみ` のような求人は、30行目の `電話` に引っかかって誤除外されます。
- 年齢制限は31行目で `35/40/45歳以下`、`〜30/40代`、`若年層のみ` 程度しか見ていません。`44歳以下`、`40歳未満`、`39歳まで`、`長期キャリア形成のため`、`例外事由3号のイ` は漏れます。

### 距離/勤務地検証（geo水増し検出）の妥当性

- 79-80行目は `徒歩(\d+)分` だけを見ます。`徒歩 約10分`、`徒歩10分以内`、全角数字、`駅から10分`、`板宿駅より徒歩10分` などは拾えません。
- 徒歩分がない場合、81行目で `TOWNS` の町名が含まれるだけで通します。検索結果の勤務地欄に近隣町名が含まれているだけの水増しや、複数勤務地の一部だけ板宿近辺という求人を通す可能性があります。
- 詳細検証は103-105行目で本文中の最初の `兵庫県` または `神戸市` から100文字を住所候補にしています。パンくず、関連求人、会社住所、フッター等を拾う可能性があります。
- 106行目の判定は `須磨区` を含めば通るため、須磨区内でも板宿駅1km外の勤務地を通します。板宿駅1km検証としては広すぎます。
- 逆に、長田区側の西代・大池町・千歳町など板宿駅近辺の勤務地は、住所表記次第で誤除外される可能性があります。(推測) `西代` という駅名・町名が詳細本文に出ない長田区住所では落ちます。
- 最も危険なのは、詳細本文に住所候補が見つからない場合です。103-110行目では `addr=''` のまま `('✔確認済', '')` を返すため、勤務地抽出不能な詳細ページを確認済みにしてしまいます。
- 詳細検証は137-143行目で最大15件だけです。16件目以降は詳細URLがあっても150行目で `△未確認` になります。件数が多い日に、実在検証の大半が未実施になります。

## 4. 運用性

### ログは障害調査に足りるか

- 33-36行目の `log()` は時刻付きで標準出力とファイルに出しており、最低限の時系列は残ります。
- ただし、取得URLごとのHTTPステータス、取得バイト数、カード抽出数、ページ番号、所要時間、リトライ回数が構造化されていません。障害時に「求人が本当に0件だった」のか「抽出できなかった」のかを後から判別しにくいです。
- `parse_cards()` が0件だったページ、HTMLサイズが小さすぎるページ、詳細検証で住所抽出不能だったページは異常ログになりません。
- Gitとメールの標準エラーが保存されません。224-233行目の `subprocess.run()` は `capture_output` していないため、LaunchAgent側のstdout/stderr設定に依存します。
- `SELF_DIR` やログディレクトリが存在しない場合、36行目で `open(LOG, 'a')` が失敗します。さらに239-240行目の例外処理でも `log()` を呼ぶため、同じ理由でFATALログすら残せない可能性があります。

### 失敗時に「失敗したと分かる」仕組みがあるか

- Python例外で落ちた場合は241行目で非0終了します。ただしLaunchAgent通知、失敗メール、失敗レポート生成はこのスクリプト内にはありません。
- 取得失敗、抽出0件、異常に少ない件数、詳細検証全滅、push失敗、メールスクリプト失敗の多くは、非0終了にも利用者向け通知にもなりません。
- 特にpush失敗後のメール送信、メールスクリプト失敗後の `EMAIL_TRIGGERED` ログは、運用者に誤った安心を与えるため優先して直すべきです。
- レポート本文に「取得失敗あり」「部分取得」「詳細未検証多数」といったラン状態が入らないため、受信者が異常を見抜くには件数の勘が必要です。

## 5. 具体パッチ提案トップ5（優先順。可能なら diff 形式または before/after コード断片）

### 1. 空/部分取得を正常レポートにしないfail gateを入れる

実害が最大です。求人ボックス側変更やネットワーク失敗が0件レポートとして流れるのを止めます。

```diff
@@
 DATE = os.environ.get('JS_DATE') or datetime.date.today().isoformat()
+MIN_TOTAL = int(os.environ.get('JS_MIN_TOTAL', '1'))
+MIN_ONSITE_RAW = int(os.environ.get('JS_MIN_ONSITE_RAW', '1'))
+WARNINGS = []
+
+def warn(msg):
+    WARNINGS.append(msg)
+    log('WARN ' + msg)
@@
     for pg in range(1, 15):
         h = fetch(ONSITE_URL + (f'?pg={pg}' if pg > 1 else ''))
-        if not h: break
+        if not h:
+            warn(f'onsite fetch empty pg={pg}')
+            break
         cs = parse_cards(h)
-        if not cs: break
+        if not cs:
+            warn(f'onsite parse zero pg={pg} html_len={len(h)}')
+            break
@@
     log(f'onsite raw={len(onsite_raw)} kept={len(onsite)}')
+    if len(onsite_raw) < MIN_ONSITE_RAW:
+        raise RuntimeError(f'abnormal onsite_raw={len(onsite_raw)}')
@@
     total = len(onsite) + len(remote)
+    if total < MIN_TOTAL:
+        raise RuntimeError(f'abnormal empty report total={total} warnings={WARNINGS}')
```

あわせて、例外時に失敗メールを送るか、少なくとも失敗レポートを作るべきです。現状の0件正常メールより、明示的な失敗通知の方が利用者にとって安全です。

### 2. 正規表現HTMLパーサをやめ、カード抽出をDOMベースにする

56-64行目の正規表現は求人ボックスの些細なHTML変更に弱いです。依存を増やせるならBeautifulSoup化が最短です。

```python
from bs4 import BeautifulSoup

def text_of(node):
    return norm(node.get_text(' ', strip=True)) if node else ''

def parse_cards(page_html):
    soup = BeautifulSoup(page_html, 'html.parser')
    nodes = soup.select('section.p-result_card, article.p-result_card, div.p-result_card, [class*="result_card"]')
    cards = []
    for node in nodes:
        title_node = node.select_one('h2, h3, a[class*="title"], [class*="title"]')
        link_node = node.select_one('a[href*="/jb/"]')
        href = link_node.get('href', '') if link_node else ''
        if href.startswith('/'):
            href = BASE + href.split('?', 1)[0]
        cards.append({
            'title': text_of(title_node)[:90],
            'company': text_of(node.select_one('.p-result_company, [class*="company"]'))[:60],
            'area': text_of(node.select_one('.p-result_area, [class*="area"]')),
            'pay': text_of(node.select_one('.p-result_pay, [class*="pay"]')),
            'emp': text_of(node.select_one('.p-result_employType, [class*="employ"]')),
            'jb': href if '/jb/' in href else '',
        })
    return [c for c in cards if c['title']]
```

BeautifulSoupを入れられない運用なら、少なくとも56行目のタグ種別固定、60行目の閉じタグ固定、64行目のURL文字種固定を緩め、ページごとの抽出件数をログ化してください。

### 3. 詳細検証は「住所が取れないなら確認済みにしない」へ変更する

103-110行目の現行ロジックは、住所抽出不能でも確認済みになるのが危険です。`須磨区` だけで通すのも広すぎます。

```diff
@@
+NEAR_TOKENS = tuple(TOWNS + ['板宿', '西代', '東須磨'])
+
 def verify(card):
@@
     mi = text.find('兵庫県')
     if mi < 0: mi = text.find('神戸市')
     addr = re.sub(r'\s+', '', text[mi:mi+100]) if mi >= 0 else ''
-    if addr and ('須磨区' not in addr and '板宿' not in addr and '西代' not in addr and '東須磨' not in addr):
+    if not addr:
+        log(f"ADDR_UNKNOWN: {card['title'][:40]}")
+        return ('△未確認', '勤務地抽出失敗')
+    if not any(x in addr for x in NEAR_TOKENS):
         log(f"GEO_MISMATCH: {card['title'][:40]} addr={addr[:40]}")
         card['mismatch'] = addr[:50]
         return None
```

さらに、137-143行目の最大15件制限は環境変数化し、未検証率が高い日はレポート上で警告するのが妥当です。

```diff
@@
-    # 検証（jbリンク持ちのみ、最大15件）
+    max_verify = int(os.environ.get('JS_MAX_VERIFY', '30'))
@@
-        if c['jb'] and jb_checked < 15:
+        if c['jb'] and jb_checked < max_verify:
```

### 4. GitHub pushとメール送信を戻り値で厳密に扱い、同日重複メールを止める

224-234行目は戻り値を見ないコマンドが多く、push失敗後もメールします。外部コマンドは共通ヘルパーでstderr込みで失敗させるべきです。

```python
def run_cmd(args, timeout):
    cp = subprocess.run(args, timeout=timeout, text=True, capture_output=True)
    if cp.returncode != 0:
        raise RuntimeError(f"command failed rc={cp.returncode}: {' '.join(args)} stderr={cp.stderr[-500:]}")
    return cp
```

```diff
@@
-    subprocess.run(['git', '-C', REPO, 'pull', '-q', '--rebase'], timeout=60)
-    subprocess.run(['git', '-C', REPO, 'add', 'reports'], timeout=30)
-    rc = subprocess.run(g + ['commit', '-q', '-m', f'report: {DATE} (mac-claude)'], timeout=30).returncode
+    run_cmd(['git', '-C', REPO, 'pull', '-q', '--rebase'], timeout=60)
+    run_cmd(['git', '-C', REPO, 'add', 'reports'], timeout=30)
+    rc = subprocess.run(g + ['commit', '-q', '-m', f'report: {DATE} (mac-claude)'],
+                        timeout=30, text=True, capture_output=True).returncode
@@
     if rc == 0:
-        rc = subprocess.run(['git', '-C', REPO, 'push', '-q'], timeout=120).returncode
-        log('PUSHED' if rc == 0 else 'PUSH_FAILED')
+        run_cmd(['git', '-C', REPO, 'push', '-q'], timeout=120)
+        log('PUSHED')
     else:
         log('NO_CHANGE (nothing to commit)')
     if not os.environ.get('JS_NO_EMAIL'):
-        subprocess.run(['/bin/bash', os.path.join(SELF_DIR, 'email-job-report.sh')], timeout=120)
+        sent_flag = os.path.join(SELF_DIR, f'email-sent-{DATE}')
+        if os.path.exists(sent_flag):
+            log('EMAIL_SKIP already sent')
+            return
+        run_cmd(['/bin/bash', os.path.join(SELF_DIR, 'email-job-report.sh')], timeout=120)
+        with open(sent_flag, 'w') as f:
+            f.write(datetime.datetime.now().isoformat() + '\n')
         log('EMAIL_TRIGGERED')
```

運用方針として「同日再実行でも必ずメールしたい」なら、`JS_FORCE_EMAIL=1` のような明示スイッチを設けるのが安全です。

### 5. 正規化した検索対象でdedupeと除外判定を強化する

91行目のdedupeと75-85行目の除外判定は、表記ゆれに弱く、見るフィールドも少ないです。まず正規化関数を1箇所に集めると保守しやすくなります。

```python
def norm_key(s):
    s = html.unescape(s or '')
    s = re.sub(r'\s+', '', s)
    return s.lower()

def searchable(c):
    return ' '.join([c.get('title',''), c.get('company',''), c.get('area',''), c.get('emp',''), c.get('pay','')])

NEGATED_VOICE = re.compile(r'電話(対応)?なし|電話なし|メール対応のみ|チャット対応のみ')
```

```diff
@@
 def onsite_keep(c):
-    t = c['title'] + ' ' + c['company']
+    t = searchable(c)
     if NG.search(t) or AGE_NG.search(t): return False
@@
 def remote_keep(c):
-    t = c['title'] + ' ' + c['company']
-    if NG.search(t) or VOICE_NG.search(t) or AGE_NG.search(t): return False
+    t = searchable(c)
+    if NG.search(t) or AGE_NG.search(t): return False
+    if VOICE_NG.search(t) and not NEGATED_VOICE.search(t): return False
     return True
@@
 def dedupe(cards):
     seen, out = set(), []
     for c in cards:
-        k = (c['title'][:32], c['company'])
+        k = ('jb', c['jb'].split('?', 1)[0]) if c.get('jb') else (
+            'text', norm_key(c['title'])[:48], norm_key(c['company']), norm_key(c['area'])[:32]
+        )
```

追加候補キーワードは、最低限以下を検討してください。

- 資格/福祉: `普通自動車免許`, `要普免`, `初任者研修`, `実務者研修`, `社会福祉主事`, `サービス管理責任者`, `サビ管`, `就労支援`, `生活支援`, `障害者支援`, `デイサービス`, `グループホーム`, `A型`, `B型`
- 飲食: `厨房`, `洗い場`, `配膳`, `惣菜`, `ベーカリー`, `フード`, `ファストフード`, `調理補助`
- 声出し: `受電`, `架電`, `問い合わせ対応`, `お客様対応`, `予約受付`, `コンタクトセンター`, `インサイドセールス`
- 年齢: `歳未満`, `歳まで`, `長期キャリア形成`, `例外事由3号のイ`
