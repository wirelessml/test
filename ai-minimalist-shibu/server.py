#!/usr/bin/env python3
"""AIミニマリストしぶ チャットサーバー（Claude CLI経由、無料）"""
import http.server, json, subprocess, os, urllib.parse

PORT = 8787
DIR = os.path.dirname(os.path.abspath(__file__))
KNOWLEDGE_DIR = os.path.join(DIR, 'knowledge')

# コアナレッジ読み込み
CORE_FILES = [
    'shibu-biography.md', 'minimalism-principles.md', 'video-pattern-analysis.md',
    'shibu-business.md', 'mono-herashi-coaching.md', 'minimal-life-program.md',
    'shibu-ecosystem.md', '30-questions.md', 'minimalist-life-cost.md',
]
knowledge = []
for f in CORE_FILES:
    path = os.path.join(KNOWLEDGE_DIR, f)
    if os.path.exists(path):
        with open(path, 'r') as fh:
            knowledge.append(fh.read().replace('**', ''))
KNOWLEDGE_TEXT = '\n---\n'.join(knowledge)

SYSTEM = f"""あなたはミニマリストしぶ（澁谷直人、31歳）です。以下のナレッジに基づいて、しぶ本人として対話してください。

口調のルール:
- タメ口で話す（敬語は使わない）
- 簡潔に話す（ミニマリストらしく短く）
- 断言する（「〜だと思う」ではなく「〜だよ」）
- 決まり文句を自然に使う:「迷ったら手放す」「全出し」「部屋は心の映し鏡」「あったら便利=なくても困らない」
- 具体的なエピソードを交える（テスラ車上生活、月7万円生活、ニトリマットレス11年等）
- 質問には短く答えてから、相手の状況を聞く（コーチング的アプローチ）
- 絵文字は最小限

ナレッジ:
{KNOWLEDGE_TEXT}"""

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
header { padding: 12px 16px; background: var(--surface); border-bottom: 1px solid var(--border); flex-shrink: 0; }
header h1 { font-size: 16px; color: var(--accent); }
header small { color: var(--muted); font-size: 11px; }
#chat { flex: 1; overflow-y: auto; padding: 16px; display: flex; flex-direction: column; gap: 12px; }
.msg { max-width: 85%; padding: 10px 14px; border-radius: 16px; font-size: 14px; line-height: 1.6; white-space: pre-wrap; word-break: break-word; }
.msg.ai { background: #1a2e1a; border: 1px solid #2d4a2d; align-self: flex-start; border-bottom-left-radius: 4px; }
.msg.user { background: #2a2a2a; align-self: flex-end; border-bottom-right-radius: 4px; }
.msg .name { font-size: 11px; color: var(--accent); margin-bottom: 4px; font-weight: 600; }
.msg.user .name { color: var(--muted); }
.typing { color: var(--muted); font-style: italic; font-size: 13px; align-self: flex-start; padding: 8px 14px; }
#input-area { padding: 12px 16px; background: var(--surface); border-top: 1px solid var(--border); display: flex; gap: 8px; flex-shrink: 0; }
#input-area textarea { flex: 1; padding: 10px 12px; background: var(--bg); border: 1px solid var(--border); border-radius: 12px; color: var(--text); font-size: 14px; font-family: inherit; resize: none; height: 42px; max-height: 120px; }
#input-area button { padding: 10px 16px; background: var(--accent); color: #000; border: none; border-radius: 12px; font-size: 14px; font-weight: 600; cursor: pointer; flex-shrink: 0; }
#input-area button:disabled { opacity: 0.4; cursor: default; }
</style>
</head>
<body>
<header>
<h1>AIミニマリストしぶ</h1>
<small>少ないことは、豊かなこと。</small>
</header>
<div id="chat"></div>
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
  name.textContent = role === 'ai' ? 'しぶ' : 'あなた';
  div.appendChild(name);
  const body = document.createElement('div');
  body.textContent = text;
  div.appendChild(body);
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}
async function send() {
  const input = document.getElementById('msg');
  const text = input.value.trim();
  if (!text) return;
  input.value = '';
  input.style.height = '42px';
  document.getElementById('send-btn').disabled = true;
  addMsg('user', text);
  history.push({ role: 'user', content: text });
  const typing = document.createElement('div');
  typing.className = 'typing';
  typing.textContent = 'しぶが考え中...';
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
  } catch (e) {
    typing.remove();
    addMsg('ai', '通信エラーが発生したよ。サーバーが起動してるか確認してみて。');
  }
  document.getElementById('send-btn').disabled = false;
  input.focus();
}
addMsg('ai', 'やあ。ミニマリストしぶだよ。\\n\\n何か気になることがあったら、何でも聞いてね。片付けのこと、ミニマリズムのこと、生き方のこと。');
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

        prompt_parts = []
        for h in hist[-10:]:
            role = 'ユーザー' if h['role'] == 'user' else 'しぶ'
            prompt_parts.append(f"{role}: {h['content']}")
        prompt_parts.append(f"ユーザー: {msg}")
        prompt_parts.append("しぶ:")
        full_prompt = '\n'.join(prompt_parts)

        try:
            result = subprocess.run(
                ['claude', '-p', f'{SYSTEM}\n\n{full_prompt}', '--output-format', 'text'],
                capture_output=True, text=True, timeout=120
            )
            reply = result.stdout.strip() if result.returncode == 0 else 'ごめん、ちょっとエラーが起きた。もう一度聞いてみて。'
        except subprocess.TimeoutExpired:
            reply = 'ちょっと時間がかかりすぎたみたい。もう一度試してみて。'

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'reply': reply}, ensure_ascii=False).encode())

    def log_message(self, fmt, *args):
        print(f"[shibu] {args[0]}")

print(f"AIミニマリストしぶサーバー起動: http://localhost:{PORT}")
print("ブラウザで開いてください。Ctrl+Cで停止。")
http.server.HTTPServer(('0.0.0.0', PORT), Handler).serve_forever()
