#!/usr/bin/env python3
"""AIミニマリストしぶ チャットサーバー（Claude CLI経由、無料）"""
import http.server, json, subprocess, os, urllib.parse, datetime, sys

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
        'ai': ai_reply,
        'title': user_msg[:30]
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

knowledge_mtime = {}
def reload_knowledge():
    """ファイル更新を検知してナレッジをリロード"""
    changed = False
    for fname in KNOWLEDGE_FILES:
        path = os.path.join(KNOWLEDGE_DIR, fname)
        if os.path.exists(path):
            mt = os.path.getmtime(path)
            if fname not in knowledge_mtime or knowledge_mtime[fname] != mt:
                with open(path, 'r') as fh:
                    knowledge_data[fname] = fh.read().replace('**', '')
                knowledge_mtime[fname] = mt
                changed = True
    if changed:
        print(f"ナレッジ更新検知: {len(knowledge_data)}ファイル")

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
- 回答は200文字以内を目安にする（ミニマリストらしく短く）

ナレッジ:
"""

CHAT_HTML = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="AIしぶ">
<meta name="theme-color" content="#0a0a0a">
<link rel="manifest" href="/manifest.json">
<title>AIミニマリストしぶ</title>
<style>
:root { --bg: #0a0a0a; --surface: #161616; --border: #2a2a2a; --text: #e5e5e5; --muted: #888; --accent: #4ade80; }
* { margin: 0; padding: 0; box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
body { background: var(--bg); color: var(--text); font-family: -apple-system, 'Noto Sans JP', sans-serif; height: 100dvh; display: flex; flex-direction: column; overscroll-behavior: none; -webkit-text-size-adjust: 100%; }
html { height: -webkit-fill-available; }
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
.copy-btn { background: none; border: none; color: var(--muted); font-size: 11px; cursor: pointer; padding: 2px 6px; float: right; opacity: 0.5; }
.copy-btn:active { opacity: 1; }
.del-btn { background: none; border: none; color: var(--muted); font-size: 10px; cursor: pointer; padding: 2px 4px; opacity: 0.3; }
.del-btn:hover { opacity: 1; color: #f87171; }
.typing { color: var(--muted); font-style: italic; font-size: 13px; align-self: flex-start; padding: 8px 14px; }
.suggest { display: flex; gap: 8px; flex-wrap: wrap; align-self: flex-start; }
.suggest button { background: none; border: 1px solid var(--accent); color: var(--accent); padding: 6px 12px; border-radius: 16px; font-size: 12px; cursor: pointer; }
.suggest button:active { background: var(--accent); color: #000; }
@keyframes dots { 0%,20% { content: '.'; } 40% { content: '..'; } 60%,100% { content: '...'; } }
.typing::after { content: ''; animation: dots 1.5s infinite; }
#input-area { padding: 12px 16px; padding-bottom: max(12px, env(safe-area-inset-bottom)); background: var(--surface); border-top: 1px solid var(--border); display: flex; gap: 8px; flex-shrink: 0; }
#input-area textarea { flex: 1; padding: 10px 12px; background: var(--bg); border: 1px solid var(--border); border-radius: 12px; color: var(--text); font-size: 16px; font-family: inherit; resize: none; height: 42px; max-height: 120px; }
#input-area button { padding: 10px 16px; background: var(--accent); color: #000; border: none; border-radius: 12px; font-size: 14px; font-weight: 600; cursor: pointer; flex-shrink: 0; }
#input-area button:disabled { opacity: 0.4; cursor: default; }
#credit { padding: 8px 16px; text-align: center; font-size: 10px; color: var(--muted); flex-shrink: 0; }
#phrase-counter { padding: 6px 16px; background: var(--surface); border-top: 1px solid var(--border); font-size: 11px; color: var(--muted); text-align: center; flex-shrink: 0; }
#calc-panel { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; margin: 8px 16px; padding: 16px; align-self: stretch; }
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
<button class="calc-btn" onclick="resetChat()">リセット</button>
<button class="calc-btn" id="calc-toggle">生活費計算</button>
</header>
<div id="calc-panel" style="display:none">
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
<div class="calc-item"><label>税金</label><input type="number" data-cost value="0"></div>
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
<div id="credit">Powered by Claude + ミニマリストしぶのナレッジ</div>
<div id="input-area">
<textarea id="msg" placeholder="メッセージを入力..." rows="1" onkeydown="if(event.key==='Enter'&&!event.shiftKey&&!('ontouchstart' in window)){event.preventDefault();send()}" oninput="this.style.height='42px';this.style.height=Math.min(this.scrollHeight,120)+'px';document.getElementById('char-count').textContent=this.value.length>0?this.value.length:''"></textarea>
<button id="mic-btn" onclick="toggleMic()" style="background:none;border:1px solid var(--border);color:var(--muted);border-radius:12px;padding:10px;cursor:pointer;flex-shrink:0">🎤</button>
<button id="voice-btn" onclick="playVoice()" style="background:none;border:1px solid var(--border);color:var(--muted);border-radius:12px;padding:10px;cursor:pointer;flex-shrink:0" title="しぶの声で読む">🔊</button>
<span id="char-count" style="font-size:10px;color:var(--muted);align-self:center"></span>
<button id="send-btn" onclick="send()">送信</button>
<audio id="voice-audio" style="display:none"></audio>
</div>
<script>
let history = [];
async function playVoice() {
  const msg = document.getElementById('msg').value.trim();
  if (!msg) return;
  const btn = document.getElementById('voice-btn');
  btn.textContent = '...';
  btn.disabled = true;
  try {
    const res = await fetch('/api/voice', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({text: msg})
    });
    if (!res.ok) throw new Error('Voice API error');
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const audio = document.getElementById('voice-audio');
    audio.src = url;
    audio.play();
  } catch(e) {
    alert('音声生成に失敗しました');
  }
  btn.textContent = '🔊';
  btn.disabled = false;
}
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
  body.innerHTML = miniMd(text);
  div.appendChild(body);
  const del = document.createElement('button');
  del.className = 'del-btn';
  del.textContent = 'x';
  del.onclick = () => div.remove();
  div.appendChild(del);
  if (role === 'ai') {
    const cb = document.createElement('button');
    cb.className = 'copy-btn';
    cb.textContent = 'コピー';
    cb.onclick = () => { navigator.clipboard.writeText(text).then(() => { cb.textContent = 'コピー済'; setTimeout(() => cb.textContent = 'コピー', 1500); }); };
    div.appendChild(cb);
  }
  chat.appendChild(div);
  setTimeout(() => chat.scrollTop = chat.scrollHeight, 50);
}
async function send(text) {
  const input = document.getElementById('msg');
  if (!text) { text = input.value.trim().replace(/\\n/g,'').trim(); input.value = ''; input.style.height = '42px'; }
  if (!text) return;
  const btn = document.getElementById('send-btn');
  btn.disabled = true; btn.textContent = '...';
  addMsg('user', text);
  history.push({ role: 'user', content: text });
  if (history.filter(h=>h.role==='user').length >= 20) {
    addMsg('ai', 'もう20個も質問したね。知識ばかり集めても部屋は片付かない。そろそろ実践しよう。リセットボタンを押して、1つだけ行動に移してみて。');
    btn.disabled = false; btn.textContent = '送信'; return;
  }
  const t0 = Date.now();
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
    const elapsed = ((Date.now()-t0)/1000).toFixed(1);
    const tEl = document.createElement('div');
    tEl.style.cssText = 'font-size:10px;color:var(--muted);padding:0 14px';
    tEl.textContent = elapsed + '秒';
    document.getElementById('chat').appendChild(tEl);
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
  btn.disabled = false; btn.textContent = '送信';
  document.getElementById('msg').focus();
}
document.getElementById('calc-toggle').addEventListener('click', function() {
  const p = document.getElementById('calc-panel');
  if (p.style.display === 'block') { p.style.display = 'none'; }
  else { p.style.display = 'block'; }
});
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
  document.querySelector('.calc-grid').appendChild(div);
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
  document.getElementById('calc-panel').style.display = 'none';
}
let recognition = null;
function toggleMic() {
  const btn = document.getElementById('mic-btn');
  if (recognition) { recognition.stop(); recognition = null; btn.style.color = 'var(--muted)'; return; }
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SR) { alert('音声入力非対応'); return; }
  recognition = new SR();
  recognition.lang = 'ja-JP';
  recognition.onresult = e => { document.getElementById('msg').value = e.results[0][0].transcript; btn.style.color = 'var(--muted)'; recognition = null; };
  recognition.onerror = () => { btn.style.color = 'var(--muted)'; recognition = null; };
  recognition.onend = () => { btn.style.color = 'var(--muted)'; recognition = null; };
  recognition.start();
  btn.style.color = 'var(--accent)';
}
function shareChat() {
  const lastAi = history.filter(h => h.role === 'assistant').pop();
  if (!lastAi) { alert('まだ会話がないよ'); return; }
  const text = 'AIミニマリストしぶ:\\n' + lastAi.content;
  if (navigator.share) {
    navigator.share({ text: text }).catch(() => {});
  } else {
    navigator.clipboard.writeText(text).then(() => alert('クリップボードにコピーしたよ'));
  }
}
function miniMd(t) {
  var s = t.replace(/&/g,'&amp;');
  s = s.replace(/</g,'&lt;').replace(/>/g,'&gt;');
  s = s.split('\\n').join('<br>');
  return s;
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
const PH = ['片付けのこと聞いてみて','何を手放したい？','ミニマリズムって何？','生活費いくらかかってる？','テスラ生活ってどう？'];
document.getElementById('msg').placeholder = PH[Math.floor(Math.random()*PH.length)];
const QUOTES = ['迷ったら手放す。','少ないことは、豊かなこと。','部屋は心の映し鏡。','あったら便利 = なくても困らない。','手放すたびに、手に入るものがある。','不便は本当に必要なものを教えてくれる先生。','モノを減らすんじゃなくて、大切なモノを選ぶ。'];
const q = QUOTES[Math.floor(Math.random()*QUOTES.length)];
addMsg('ai', 'やあ。ミニマリストしぶだよ。\\n\\n何か気になることがあったら、何でも聞いてね。片付けのこと、ミニマリズムのこと、生き方のこと。\\n\\n右上の「生活費計算」からミニマムライフコストも計算できるよ。水道代は請求額をそのまま入れれば自動で月額に変換するよ。\\n\\n今日の一言: ' + q);
const sugDiv = document.createElement('div');
sugDiv.className = 'suggest';
const challenges = ['靴箱を全出し','財布の中身を全出し','スマホのアプリを全出し','クローゼットを全出し','洗面台の下を全出し','冷蔵庫を全出し','本棚を全出し'];
const todayChallenge = challenges[new Date().getDay() % challenges.length];
['片付けのコツは？', '今日のチャレンジ: ' + todayChallenge, '30の質問をやる'].forEach(q => {
  const b = document.createElement('button');
  b.textContent = q;
  b.onclick = () => { sugDiv.remove(); send(q); };
  sugDiv.appendChild(b);
});
document.getElementById('chat').appendChild(sugDiv);
document.getElementById('msg').focus();
// 履歴復元は無効化（リロードで初期状態に戻る）
document.addEventListener('keydown', e => {
  if (e.ctrlKey && e.key === 'l') { e.preventDefault(); resetChat(); }
  if (e.ctrlKey && e.key === '/') { e.preventDefault(); document.getElementById('calc-toggle').click(); }
});
</script>
</body>
</html>"""

def get_stats():
    """会話ログから統計を集計"""
    from collections import Counter
    total = 0; today_count = 0; questions = []; phrases_count = Counter()
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    shibu_phrases = ['全出し', '手放す', '迷ったら', '部屋は心', '必要なもの']
    if os.path.exists(LOG_DIR):
        for fname in sorted(os.listdir(LOG_DIR)):
            if fname.endswith('.jsonl'):
                is_today = today in fname
                with open(os.path.join(LOG_DIR, fname), 'r') as f:
                    for line in f:
                        try:
                            e = json.loads(line.strip())
                            total += 1
                            if is_today: today_count += 1
                            if e.get('user'): questions.append(e['user'])
                            if e.get('ai'):
                                for p in shibu_phrases:
                                    phrases_count[p] += e['ai'].count(p)
                        except: pass
    q_counter = Counter(questions).most_common(5)
    return {'total': total, 'today': today_count, 'top_questions': q_counter, 'phrases': dict(phrases_count)}

STATS_HTML = """<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>しぶ統計</title>
<style>:root{--bg:#0a0a0a;--surface:#161616;--border:#2a2a2a;--text:#e5e5e5;--muted:#888;--accent:#4ade80}*{margin:0;padding:0;box-sizing:border-box}body{background:var(--bg);color:var(--text);font-family:-apple-system,'Noto Sans JP',sans-serif;padding:16px}
h1{font-size:18px;color:var(--accent);margin-bottom:16px}h2{font-size:14px;color:var(--accent);margin:16px 0 8px}.card{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:16px;margin-bottom:12px}
.big{font-size:32px;font-weight:700;color:var(--accent)}.row{display:flex;gap:12px}.row .card{flex:1;text-align:center}.list{font-size:13px;line-height:2}a{color:var(--accent)}</style></head><body>
<h1>AIミニマリストしぶ 統計</h1><div id="s">読み込み中...</div><p style="margin-top:16px"><a href="/">チャットに戻る</a></p>
<script>fetch('/api/stats').then(r=>r.json()).then(d=>{let h='<div class="row"><div class="card"><div class="big">'+d.total+'</div>総会話</div><div class="card"><div class="big">'+d.today+'</div>今日</div></div>';
h+='<h2>よく聞かれる質問</h2><div class="card"><div class="list">';d.top_questions.forEach(([q,c])=>{h+=c+'回: '+q+'<br>'});h+='</div></div>';
h+='<h2>しぶ語録の出現回数</h2><div class="card"><div class="list">';Object.entries(d.phrases).forEach(([k,v])=>{if(v>0)h+=k+': '+v+'回<br>'});h+='</div></div>';
document.getElementById('s').innerHTML=h})</script></body></html>"""

last_request = {}
RATE_LIMIT_SEC = 5
response_cache = {}
CACHE_MAX = 100

class Handler(http.server.BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_GET(self):
        path = self.path.split('?')[0]
        if path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            uptime = int(_time_module.time() - SERVER_START)
            self.wfile.write(f'ok v0.120 uptime:{uptime}s knowledge:{len(knowledge_data)}files'.encode())
        elif path == '/manifest.json':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"name":"AIミニマリストしぶ","short_name":"AIしぶ","start_url":"/","display":"standalone","background_color":"#0a0a0a","theme_color":"#0a0a0a"}, ensure_ascii=False).encode())
        elif path == '/stats':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(STATS_HTML.encode())
        elif path == '/api/export':
            logs = []
            if os.path.exists(LOG_DIR):
                for fname in sorted(os.listdir(LOG_DIR)):
                    if fname.endswith('.jsonl'):
                        with open(os.path.join(LOG_DIR, fname), 'r') as f:
                            for line in f:
                                try: logs.append(json.loads(line.strip()))
                                except: pass
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Disposition', 'attachment; filename="shibu-chat-export.json"')
            self.end_headers()
            self.wfile.write(json.dumps(logs, ensure_ascii=False, indent=2).encode())
        elif path == '/api/history':
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            today_log = os.path.join(LOG_DIR, f'chat_{today}.jsonl')
            entries = []
            if os.path.exists(today_log):
                with open(today_log, 'r') as f:
                    for line in f:
                        try: entries.append(json.loads(line.strip()))
                        except: pass
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(entries[-20:], ensure_ascii=False).encode())
        elif path.startswith('/api/search'):
            import urllib.parse as _up
            qs = _up.parse_qs(_up.urlparse(self.path).query)
            q = qs.get('q', [''])[0]
            results = []
            if q:
                for fname, content in knowledge_data.items():
                    if q.lower() in content.lower():
                        idx = content.lower().find(q.lower())
                        snippet = content[max(0,idx-50):idx+100].replace('\n',' ')
                        results.append({'file': fname, 'snippet': snippet})
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'query': q, 'count': len(results), 'results': results}, ensure_ascii=False).encode())
        elif path == '/api/knowledge':
            files = []
            for f in sorted(os.listdir(KNOWLEDGE_DIR)):
                if f.endswith('.md'):
                    p = os.path.join(KNOWLEDGE_DIR, f)
                    files.append({'name': f, 'size': os.path.getsize(p)})
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'count': len(files), 'files': files}, ensure_ascii=False).encode())
        elif path == '/api/export-md':
            logs = []
            if os.path.exists(LOG_DIR):
                for fname in sorted(os.listdir(LOG_DIR)):
                    if fname.endswith('.jsonl'):
                        with open(os.path.join(LOG_DIR, fname), 'r') as f:
                            for line in f:
                                try: logs.append(json.loads(line.strip()))
                                except: pass
            md = '# AIミニマリストしぶ 会話ログ\n\n'
            for e in logs:
                ts = e.get('timestamp','')[:16].replace('T',' ')
                if e.get('user'): md += f'**あなた** ({ts})\n{e["user"]}\n\n'
                if e.get('ai'): md += f'**しぶ** ({ts})\n{e["ai"]}\n\n---\n\n'
            self.send_response(200)
            self.send_header('Content-Type', 'text/markdown; charset=utf-8')
            self.send_header('Content-Disposition', 'attachment; filename="shibu-chat.md"')
            self.end_headers()
            self.wfile.write(md.encode())
        elif path == '/api/stats':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(get_stats(), ensure_ascii=False).encode())
        elif path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(CHAT_HTML.encode())
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write('<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>404</title><style>body{background:#0a0a0a;color:#e5e5e5;font-family:-apple-system,sans-serif;display:flex;justify-content:center;align-items:center;height:100vh;text-align:center}h1{color:#4ade80;font-size:48px}p{color:#888;margin-top:12px}a{color:#4ade80}</style></head><body><div><h1>404</h1><p>そのページ、もう手放したよ。</p><p>必要なものだけ残す。<a href="/">トップへ</a></p></div></body></html>'.encode())

    def do_POST(self):
        import time as _time

        # 音声生成エンドポイント
        if self.path == '/api/voice':
            body = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
            text = body.get('text', '')[:200]
            if not text:
                self.send_response(400)
                self.end_headers()
                return
            api_key = os.environ.get('ELEVENLABS_API_KEY', '')
            if not api_key:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'API key not set'}).encode())
                return
            try:
                import urllib.request
                req = urllib.request.Request(
                    'https://api.elevenlabs.io/v1/text-to-speech/LIDNtfJHRfi2AFJWPFeV',
                    data=json.dumps({
                        'text': text,
                        'model_id': 'eleven_v3',
                        'voice_settings': {'stability': 0.5, 'similarity_boost': 1.0, 'style': 0.0}
                    }).encode(),
                    headers={'xi-api-key': api_key, 'Content-Type': 'application/json', 'Accept': 'audio/mpeg'}
                )
                with urllib.request.urlopen(req, timeout=30) as resp:
                    audio = resp.read()
                self.send_response(200)
                self.send_header('Content-Type', 'audio/mpeg')
                self.send_header('Content-Length', str(len(audio)))
                self.end_headers()
                self.wfile.write(audio)
                print(f"[voice] {len(text)}chars -> {len(audio)//1024}KB")
            except Exception as e:
                print(f"[voice error] {e}")
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}, ensure_ascii=False).encode())
            return

        client = self.client_address[0]
        now = _time.time()
        if client in last_request and now - last_request[client] < RATE_LIMIT_SEC:
            self.send_response(429)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'reply': 'ちょっと待って。焦らないで。ミニマリストはゆっくりでいい。'}, ensure_ascii=False).encode())
            return
        last_request[client] = now
        reload_knowledge()
        body = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        msg = body.get('message', '')
        hist = body.get('history', [])

        # 過去の同じ質問をチェック
        past = load_past_questions()
        dup = find_duplicate(msg, past)
        dup_note = "\n\n注意: この質問は過去にも聞かれたことがある。塩対応で「それ前にも聞かれたよ。」と短く返して、前回と違う角度で一言だけ答えて終わり。長く答えない。" if dup else ""

        # キャッシュチェック
        cache_key = msg.strip().lower()
        if cache_key in response_cache and not any('30の質問' in h.get('content','') for h in hist):
            reply = response_cache[cache_key]
            log_chat(msg, reply + ' (cached)')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'reply': reply}, ensure_ascii=False).encode())
            return

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
            if result.returncode == 0:
                reply = result.stdout.strip().replace('**', '')
            else:
                reply = 'ごめん、ちょっとエラーが起きた。もう一度聞いてみて。'
                err_path = os.path.join(LOG_DIR, f'error_{datetime.datetime.now().strftime("%Y-%m-%d")}.log')
                with open(err_path, 'a') as ef:
                    ef.write(f'{datetime.datetime.now().isoformat()} | {result.stderr[:200]}\n')
        except subprocess.TimeoutExpired:
            reply = 'ちょっと時間がかかりすぎたみたい。もう一度試してみて。'

        elapsed_ms = int((_time.time() - now) * 1000)
        if len(response_cache) < CACHE_MAX:
            response_cache[cache_key] = reply
        log_chat(msg, reply)
        print(f"[shibu] {elapsed_ms}ms | {msg[:30]}")

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'reply': reply}, ensure_ascii=False).encode())

    def log_message(self, fmt, *args):
        ts = datetime.datetime.now().strftime('%H:%M:%S')
        line = f"[{ts}] {self.client_address[0]} {args[0]}"
        print(line)
        log_path = os.path.join(LOG_DIR, f'access_{datetime.datetime.now().strftime("%Y-%m-%d")}.log')
        with open(log_path, 'a') as f:
            f.write(line + '\n')

import time as _time_module
SERVER_START = _time_module.time()
total_kb = sum(len(v) for v in knowledge_data.values()) // 1024
print(f"AIミニマリストしぶサーバー起動: http://localhost:{PORT}")
print(f"ナレッジ: {len(knowledge_data)}ファイル, {total_kb}KB")
print("ブラウザで開いてください。Ctrl+Cで停止。")
import socketserver, signal

def graceful_shutdown(sig, frame):
    print("\nサーバー停止中... ログ保存完了。")
    sys.exit(0)
signal.signal(signal.SIGINT, graceful_shutdown)
signal.signal(signal.SIGTERM, graceful_shutdown)
class ThreadedServer(socketserver.ThreadingMixIn, http.server.HTTPServer): pass
ThreadedServer(('0.0.0.0', PORT), Handler).serve_forever()
