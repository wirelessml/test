#!/usr/bin/env python3
"""AIミニマリストしぶ チャットサーバー（Claude CLI経由、無料）"""
import http.server, json, subprocess, os, urllib.parse, datetime

PORT = 8787
DIR = os.path.dirname(os.path.abspath(__file__))
KNOWLEDGE_DIR = os.path.join(DIR, 'knowledge')
LOG_DIR = os.path.join(DIR, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

def load_past_questions():
    """過去のログから全ユーザー質問を読み込む"""
    questions = []
    if not os.path.exists(LOG_DIR):
        return questions
    for fname in sorted(os.listdir(LOG_DIR)):
        if fname.endswith('.jsonl'):
            path = os.path.join(LOG_DIR, fname)
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        if entry.get('user'):
                            questions.append(entry['user'])
                    except: pass
    return questions

def find_duplicate(msg, past_questions):
    """同じ質問が過去にあったか判定"""
    msg_clean = msg.strip().lower().replace('？', '').replace('?', '').replace('。', '')
    for q in past_questions:
        q_clean = q.strip().lower().replace('？', '').replace('?', '').replace('。', '')
        if msg_clean == q_clean or (len(msg_clean) > 5 and msg_clean in q_clean) or (len(q_clean) > 5 and q_clean in msg_clean):
            return q
    return None

def log_chat(user_msg, ai_reply):
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    path = os.path.join(LOG_DIR, f'chat_{today}.jsonl')
    entry = {
        'timestamp': datetime.datetime.now().isoformat(),
        'user': user_msg,
        'ai': ai_reply
    }
    with open(path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')

# コアナレッジ読み込み（ファイル別に保持）
KNOWLEDGE_FILES = {
    'shibu-biography.md': ['しぶ', 'プロフィール', '年齢', '名前', '経歴', '誕生', '福岡', 'テスラ', '車', 'マット', '起業', '会社'],
    'minimalism-principles.md': ['ミニマリ', '原則', '哲学', '考え方', '価値観', '手放', '捨て'],
    'video-pattern-analysis.md': ['動画', 'YouTube', '口調', '全出し', '片付け', 'ビフォー', 'アフター'],
    'shibu-business.md': ['事業', 'ビジネス', '収入', '稼', 'Minimal Arts', 'ブランド'],
    'mono-herashi-coaching.md': ['コーチ', 'モノ減らし', '料金', '万円', 'プログラム', 'コンサル'],
    'minimal-life-program.md': ['プログラム', 'サービス', '申込', '特典'],
    'shibu-ecosystem.md': ['りくと', 'じゅん', 'sho', 'チーム', '弟子', '編集'],
    '30-questions.md': ['質問', '30', '手放し', '迷', '判断'],
    'minimalist-life-cost.md': ['生活費', 'コスト', '月', '万円', '家賃', '食費', '支出'],
}

knowledge_data = {}
for fname in KNOWLEDGE_FILES:
    path = os.path.join(KNOWLEDGE_DIR, fname)
    if os.path.exists(path):
        with open(path, 'r') as fh:
            knowledge_data[fname] = fh.read().replace('**', '')

# 必須ナレッジ（常に含める、短いファイル）
ALWAYS_INCLUDE = ['shibu-biography.md', 'minimalism-principles.md']

def select_knowledge(msg):
    """質問に関連するナレッジだけを選択"""
    selected = set(ALWAYS_INCLUDE)
    for fname, keywords in KNOWLEDGE_FILES.items():
        if any(kw in msg for kw in keywords):
            selected.add(fname)
    # マッチなしなら上位5ファイル
    if len(selected) <= 2:
        selected.update(list(KNOWLEDGE_FILES.keys())[:5])
    return '\n---\n'.join(knowledge_data[f] for f in selected if f in knowledge_data)

SYSTEM_BASE = """あなたはミニマリストしぶ（澁谷直人、31歳）です。以下のナレッジに基づいて、しぶ本人として対話してください。

口調のルール:
- タメ口で話す（敬語は使わない）
- 簡潔に話す（ミニマリストらしく短く）
- 断言する（「〜だと思う」ではなく「〜だよ」）
- 決まり文句を自然に使う:「迷ったら手放す」「全出し」「部屋は心の映し鏡」「あったら便利=なくても困らない」
- 具体的なエピソードを交える（テスラ車上生活、月7万円生活、ニトリマットレス11年等）
- 質問には短く答えてから、相手の状況を聞く（コーチング的アプローチ）
- 絵文字は最小限
- 同じ質問をされた時、絶対に回数を言わない（「3回目」「5回目」等は禁止）

ナレッジ:
"""

CHAT_HTML = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AIミニマリストしぶ</title>
<style>
:root { --bg: #0a0a0a; --surface: #161616; --border: #2a2a2a; --text: #e5e5e5; --muted: #888; --accent: #4ade80; }
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: var(--bg); color: var(--text); font-family: -apple-system, 'Noto Sans JP', sans-serif; height: 100dvh; display: flex; flex-direction: column; }
header { padding: 12px 16px; background: var(--surface); border-bottom: 1px solid var(--border); display: flex; align-items: center; justify-content: space-between; flex-shrink: 0; }
header h1 { font-size: 16px; color: var(--accent); }
header small { color: var(--muted); font-size: 11px; }
.calc-btn { background: none; border: 1px solid var(--border); color: var(--accent); font-size: 12px; padding: 4px 10px; border-radius: 6px; cursor: pointer; }
#chat { flex: 1; overflow-y: auto; padding: 16px; display: flex; flex-direction: column; gap: 12px; }
.msg { max-width: 85%; padding: 10px 14px; border-radius: 16px; font-size: 14px; line-height: 1.6; white-space: pre-wrap; word-break: break-word; }
.msg.ai { background: #1a2e1a; border: 1px solid #2d4a2d; align-self: flex-start; border-bottom-left-radius: 4px; }
.msg.user { background: #2a2a2a; align-self: flex-end; border-bottom-right-radius: 4px; }
.msg .name { font-size: 11px; color: var(--accent); margin-bottom: 4px; font-weight: 600; display: flex; justify-content: space-between; }
.msg .time { font-weight: 400; color: var(--muted); }
.msg.user .name { color: var(--muted); }
.typing { color: var(--muted); font-style: italic; font-size: 13px; align-self: flex-start; padding: 8px 14px; }
.suggest { display: flex; gap: 8px; flex-wrap: wrap; align-self: flex-start; }
.suggest button { background: none; border: 1px solid var(--accent); color: var(--accent); padding: 6px 12px; border-radius: 16px; font-size: 12px; cursor: pointer; }
.suggest button:active { background: var(--accent); color: #000; }
@keyframes dots { 0%,20% { content: '.'; } 40% { content: '..'; } 60%,100% { content: '...'; } }
.typing::after { content: ''; animation: dots 1.5s infinite; }
#input-area { padding: 12px 16px; background: var(--surface); border-top: 1px solid var(--border); display: flex; gap: 8px; flex-shrink: 0; }
#input-area textarea { flex: 1; padding: 10px 12px; background: var(--bg); border: 1px solid var(--border); border-radius: 12px; color: var(--text); font-size: 14px; font-family: inherit; resize: none; height: 42px; max-height: 120px; }
#input-area button { padding: 10px 16px; background: var(--accent); color: #000; border: none; border-radius: 12px; font-size: 14px; font-weight: 600; cursor: pointer; flex-shrink: 0; }
#input-area button:disabled { opacity: 0.4; cursor: default; }
#phrase-counter { padding: 6px 16px; background: var(--surface); border-top: 1px solid var(--border); font-size: 11px; color: var(--muted); text-align: center; flex-shrink: 0; }
#calc-panel { display: none; background: var(--surface); border: 1px solid var(--border); border-radius: 12px; margin: 8px 16px; padding: 16px; align-self: stretch; }
#calc-panel h2 { font-size: 14px; color: var(--accent); margin-bottom: 4px; }
#calc-panel p { font-size: 11px; color: var(--muted); margin-bottom: 12px; }
.calc-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.calc-item { display: flex; align-items: center; gap: 6px; }
.calc-item label { font-size: 12px; color: var(--muted); min-width: 70px; }
.calc-item input { flex: 1; padding: 6px 8px; background: var(--bg); border: 1px solid var(--border); border-radius: 6px; color: var(--text); font-size: 13px; text-align: right; max-width: 90px; }
#calc-total { margin-top: 12px; padding-top: 12px; border-top: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; }
#calc-total span { font-size: 16px; color: var(--accent); font-weight: 700; }
#calc-actions { margin-top: 10px; display: flex; gap: 8px; }
#calc-actions button { flex: 1; padding: 8px; border: none; border-radius: 8px; font-size: 13px; font-weight: 600; cursor: pointer; }
.btn-calc { background: var(--accent); color: #000; }
.btn-ask { background: #2a2a2a; color: var(--text); }
#custom-items { margin-top: 8px; }
</style>
</head>
<body>
<header>
<div>
<h1>AIミニマリストしぶ</h1>
<small>少ないことは、豊かなこと。</small>
</div>
<button class="calc-btn" onclick="toggleTheme()" id="theme-btn">☀</button>
<button class="calc-btn" onclick="resetChat()">リセット</button>
<button class="calc-btn" onclick="toggleCalc()">生活費計算</button>
</header>
<div id="calc-panel">
<h2>ミニマムライフコスト計算シート</h2>
<p>毎月いくらあれば生活できる？支出を書き出してお金の不安を手放そう。</p>
<div class="calc-grid">
<div class="calc-item"><label>家賃</label><input type="number" data-cost value="0"></div>
<div class="calc-item"><label>電気代</label><input type="number" data-cost value="0"></div>
<div class="calc-item"><label>水道代</label><input type="number" data-cost data-half value="0"></div>
<div class="calc-item"><label>ガス代</label><input type="number" data-cost value="0"></div>
<div class="calc-item"><label>食費</label><input type="number" data-cost value="0"></div>
<div class="calc-item"><label>通信費</label><input type="number" data-cost value="0"></div>
<div class="calc-item"><label>交通費</label><input type="number" data-cost value="0"></div>
<div class="calc-item"><label>日用品</label><input type="number" data-cost value="0"></div>
<div class="calc-item"><label>娯楽費</label><input type="number" data-cost value="0"></div>
<div class="calc-item"><label>交際費</label><input type="number" data-cost value="0"></div>
<div class="calc-item"><label>コワーキング</label><input type="number" data-cost value="0"></div>
<div class="calc-item"><label>保険料</label><input type="number" data-cost value="0"></div>
<div class="calc-item"><label>年金</label><input type="number" data-cost value="0"></div>
</div>
<div id="custom-items"></div>
<div id="calc-total"><span id="total-label">合計: ¥0</span></div>
<div id="calc-actions">
<button class="btn-calc" onclick="calcTotal()">計算する</button>
<button class="btn-ask" onclick="askShibu()">しぶに相談</button>
<button class="btn-ask" onclick="addItem()">+項目追加</button>
</div>
</div>
<div id="chat"></div>
<div id="phrase-counter"></div>
<div id="input-area">
<textarea id="msg" placeholder="メッセージを入力..." rows="1" onkeydown="if(event.key==='Enter'&&!event.shiftKey){event.preventDefault();send()}" oninput="this.style.height='42px';this.style.height=Math.min(this.scrollHeight,120)+'px'"></textarea>
<button id="send-btn" onclick="send()">送信</button>
</div>
<script>
let history = [];
function addMsg(role, text) {
  const chat = document.getElementById('chat');
  const div = document.createElement('div');
  div.className = 'msg ' + role;
  const name = document.createElement('div');
  name.className = 'name';
  const now = new Date();
  const ts = now.getHours() + ':' + String(now.getMinutes()).padStart(2,'0');
  name.innerHTML = (role === 'ai' ? 'しぶ' : 'あなた') + '<span class=\"time\">' + ts + '</span>';
  div.appendChild(name);
  const body = document.createElement('div');
  body.textContent = text;
  div.appendChild(body);
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}
async function send(text) {
  const input = document.getElementById('msg');
  if (!text) { text = input.value.trim(); input.value = ''; input.style.height = '42px'; }
  if (!text) return;
  document.getElementById('send-btn').disabled = true;
  addMsg('user', text);
  history.push({ role: 'user', content: text });
  const typing = document.createElement('div');
  typing.className = 'typing';
  typing.textContent = 'しぶが考え中';
  document.getElementById('chat').appendChild(typing);
  try {
    const res = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text, history: history })
    });
    typing.remove();
    const data = await res.json();
    history.push({ role: 'assistant', content: data.reply });
    addMsg('ai', data.reply);
    countPhrases(data.reply);
  } catch (e) {
    try {
      const res2 = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, history: history })
      });
      typing.remove();
      const data2 = await res2.json();
      history.push({ role: 'assistant', content: data2.reply });
      addMsg('ai', data2.reply);
      countPhrases(data2.reply);
    } catch (e2) {
      typing.remove();
      addMsg('ai', '通信エラーが発生したよ。サーバーが起動してるか確認してみて。');
    }
  }
  document.getElementById('send-btn').disabled = false;
  document.getElementById('msg').focus();
}
function toggleCalc() {
  const p = document.getElementById('calc-panel');
  p.style.display = p.style.display === 'none' ? 'block' : 'none';
}
function calcTotal() {
  let total = 0;
  document.querySelectorAll('[data-cost]').forEach(el => { const v = Number(el.value) || 0; total += el.hasAttribute('data-half') ? Math.round(v / 2) : v; });
  document.getElementById('total-label').textContent = '合計: \\u00a5' + total.toLocaleString() + '/月';
}
function addItem() {
  const name = prompt('項目名を入力');
  if (!name) return;
  const div = document.createElement('div');
  div.className = 'calc-item';
  div.innerHTML = '<label>' + name + '</label><input type="number" data-cost value="0">';
  document.getElementById('custom-items').appendChild(div);
}
function askShibu() {
  calcTotal();
  const items = [];
  document.querySelectorAll('.calc-item').forEach(el => {
    const label = el.querySelector('label').textContent;
    const inp = el.querySelector('input');
    const val = Number(inp.value) || 0;
    const monthly = inp.hasAttribute('data-half') ? Math.round(val / 2) : val;
    if (monthly > 0) items.push(label.replace('(2月分)','') + ': ' + monthly + '円/月');
  });
  let total = 0;
  document.querySelectorAll('[data-cost]').forEach(el => { const v = Number(el.value) || 0; total += el.hasAttribute('data-half') ? Math.round(v / 2) : v; });
  const msg = '私のミニマムライフコストを計算したよ。\\n' + items.join('\\n') + '\\n合計: ' + total.toLocaleString() + '円/月\\nこの生活費についてアドバイスちょうだい。';
  send(msg);
  toggleCalc();
}
function toggleTheme() {
  const r = document.documentElement;
  const isLight = r.style.getPropertyValue('--bg').trim() === '#f5f5f5';
  if (isLight) {
    r.style.setProperty('--bg','#0a0a0a'); r.style.setProperty('--surface','#161616');
    r.style.setProperty('--border','#2a2a2a'); r.style.setProperty('--text','#e5e5e5');
    r.style.setProperty('--muted','#888');
    document.getElementById('theme-btn').textContent = '\\u2600';
  } else {
    r.style.setProperty('--bg','#f5f5f5'); r.style.setProperty('--surface','#ffffff');
    r.style.setProperty('--border','#ddd'); r.style.setProperty('--text','#1a1a1a');
    r.style.setProperty('--muted','#666');
    document.getElementById('theme-btn').textContent = '\\u263D';
  }
}
const PHRASES = {'全出し':0, '手放す':0, '迷ったら':0, '部屋は心':0, '必要なもの':0};
function countPhrases(text) {
  for (const p in PHRASES) { const m = text.match(new RegExp(p, 'g')); if (m) PHRASES[p] += m.length; }
  const items = Object.entries(PHRASES).filter(([k,v]) => v > 0).map(([k,v]) => k + ' x' + v);
  document.getElementById('phrase-counter').textContent = items.length ? 'しぶ語録: ' + items.join('  ') : '';
}
function resetChat() {
  const aiMsgs = history.filter(h => h.role === 'assistant');
  const userMsgs = history.filter(h => h.role === 'user');
  if (aiMsgs.length > 0) {
    const avgLen = Math.round(aiMsgs.reduce((s,m) => s + m.content.length, 0) / aiMsgs.length);
    addMsg('ai', '会話まとめ: ' + userMsgs.length + '個の質問、しぶの平均回答 ' + avgLen + '文字。お疲れ。');
  }
  for (const p in PHRASES) PHRASES[p] = 0;
  document.getElementById('phrase-counter').textContent = '';
  history = [];
  document.getElementById('chat').innerHTML = '';
  addMsg('ai', 'リセットしたよ。身軽になったね。\\n\\n何でも聞いてね。');
}
addMsg('ai', 'やあ。ミニマリストしぶだよ。\\n\\n何か気になることがあったら、何でも聞いてね。片付けのこと、ミニマリズムのこと、生き方のこと。\\n\\n右上の「生活費計算」からミニマムライフコストも計算できるよ。水道代は請求額をそのまま入れれば自動で月額に変換するよ。');
const sugDiv = document.createElement('div');
sugDiv.className = 'suggest';
['片付けのコツは？', 'ミニマリストになるには？', '30の質問をやる'].forEach(q => {
  const b = document.createElement('button');
  b.textContent = q;
  b.onclick = () => { sugDiv.remove(); send(q); };
  sugDiv.appendChild(b);
});
document.getElementById('chat').appendChild(sugDiv);
</script>
</body>
</html>"""

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(CHAT_HTML.encode())

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        msg = body.get('message', '')
        hist = body.get('history', [])

        # 過去の同じ質問をチェック
        past = load_past_questions()
        dup = find_duplicate(msg, past)
        dup_note = "\n\n注意: この質問は過去にも聞かれたことがある。塩対応で「それ前にも聞かれたよ。」と短く返して、前回と違う角度で一言だけ答えて終わり。長く答えない。" if dup else ""

        # 30の質問モード
        if '30の質問' in msg and not any('30の質問' in h.get('content','') for h in hist[:-1] if h['role']=='user'):
            dup_note = ""
            msg = "30の質問をやりたい。手放すか迷ってるモノがある。1問目から順番に聞いて。1回のメッセージで1問だけ。質問番号と質問文を言って、相手の回答を待って。"

        prompt_parts = []
        for h in hist[-10:]:
            role = 'ユーザー' if h['role'] == 'user' else 'しぶ'
            prompt_parts.append(f"{role}: {h['content']}")
        prompt_parts.append(f"ユーザー: {msg}{dup_note}")
        prompt_parts.append("しぶ:")
        full_prompt = '\n'.join(prompt_parts)

        try:
            result = subprocess.run(
                ['claude', '-p', f'{SYSTEM_BASE}{select_knowledge(msg)}\n\n{full_prompt}', '--output-format', 'text'],
                capture_output=True, text=True, timeout=120
            )
            reply = result.stdout.strip().replace('**', '') if result.returncode == 0 else 'ごめん、ちょっとエラーが起きた。もう一度聞いてみて。'
        except subprocess.TimeoutExpired:
            reply = 'ちょっと時間がかかりすぎたみたい。もう一度試してみて。'

        log_chat(msg, reply)

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'reply': reply}, ensure_ascii=False).encode())

    def log_message(self, fmt, *args):
        print(f"[shibu] {args[0]}")

print(f"AIミニマリストしぶサーバー起動: http://localhost:{PORT}")
print("ブラウザで開いてください。Ctrl+Cで停止。")
http.server.HTTPServer(('0.0.0.0', PORT), Handler).serve_forever()
