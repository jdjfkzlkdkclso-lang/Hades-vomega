#!/usr/bin/env python3
# ═══════════════════════════════════════════════
#  HADES TERMINAL — JSON UNIVERSAL PROTOCOL
#  Ejecutar: python3 hades-terminal.py
#  Abrir:    http://localhost:8888
# ═══════════════════════════════════════════════

import asyncio, websockets, subprocess, json, os, threading
from http.server import HTTPServer, BaseHTTPRequestHandler

AGENT_SCRIPT = os.path.expanduser("~/agente-supremo-json.sh")
HTTP_PORT  = 8888
WS_PORT    = 8889

HTML = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>HADES TERMINAL vΩ</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap');

  :root {
    --red:    #ff2233;
    --amber:  #ffaa00;
    --green:  #00ff88;
    --cyan:   #00eeff;
    --dim:    #1a1a2e;
    --mid:    #0f0f1a;
    --dark:   #07070f;
    --text:   #c8d0e0;
    --border: #ffffff11;
  }

  * { margin:0; padding:0; box-sizing:border-box; }

  body {
    background: var(--dark);
    color: var(--text);
    font-family: 'Share Tech Mono', monospace;
    height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  /* ── HEADER ── */
  header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 20px;
    background: linear-gradient(90deg, #0d0d1a, #12001a);
    border-bottom: 1px solid var(--red);
    flex-shrink: 0;
  }

  .logo {
    font-family: 'Orbitron', sans-serif;
    font-weight: 900;
    font-size: 1rem;
    letter-spacing: 4px;
    color: var(--red);
    text-shadow: 0 0 20px #ff223388;
  }

  .logo span { color: var(--amber); }

  .status-bar {
    display: flex;
    gap: 16px;
    font-size: 0.65rem;
    letter-spacing: 1px;
  }

  .stat {
    display: flex;
    align-items: center;
    gap: 5px;
    color: #666;
  }

  .stat.on  { color: var(--green); }
  .stat.off { color: var(--red); }

  .dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: currentColor;
    animation: pulse 2s infinite;
  }

  @keyframes pulse {
    0%,100% { opacity:1; }
    50%      { opacity:.3; }
  }

  /* ── MAIN LAYOUT ── */
  .workspace {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr auto;
    flex: 1;
    gap: 1px;
    background: var(--border);
    overflow: hidden;
  }

  /* ── OUTPUT PANEL ── */
  .panel {
    background: var(--dark);
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .panel-header {
    padding: 6px 14px;
    font-size: 0.6rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #444;
    border-bottom: 1px solid var(--border);
    background: var(--mid);
    flex-shrink: 0;
  }

  .panel-header span { color: var(--amber); }

  #output {
    flex: 1;
    overflow-y: auto;
    padding: 12px;
    scroll-behavior: smooth;
  }

  #output::-webkit-scrollbar { width: 3px; }
  #output::-webkit-scrollbar-thumb { background: var(--red); }

  .entry { margin-bottom: 14px; animation: fadeIn .2s ease; }

  @keyframes fadeIn { from { opacity:0; transform:translateY(4px); } to { opacity:1; transform:none; } }

  .entry-cmd {
    color: var(--amber);
    font-size: 0.75rem;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 6px;
  }

  .entry-cmd::before {
    content: 'HΩ»';
    color: var(--red);
    font-weight: bold;
  }

  .entry-out {
    font-size: 0.72rem;
    line-height: 1.5;
    padding-left: 12px;
    border-left: 2px solid var(--border);
    white-space: pre-wrap;
    word-break: break-all;
  }

  .entry-out.ok  { border-color: var(--green); }
  .entry-out.err { border-color: var(--red); color: var(--red); }

  /* JSON syntax highlight */
  .j-key   { color: var(--cyan); }
  .j-str   { color: var(--green); }
  .j-num   { color: var(--amber); }
  .j-bool  { color: #ff88aa; }
  .j-null  { color: #666; }

  /* ── VISUAL PANEL ── */
  #visual {
    flex: 1;
    overflow-y: auto;
    padding: 12px;
  }

  #visual::-webkit-scrollbar { width: 3px; }
  #visual::-webkit-scrollbar-thumb { background: var(--cyan); }

  .v-card {
    background: var(--mid);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 12px;
    margin-bottom: 10px;
    animation: fadeIn .3s ease;
  }

  .v-card h3 {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.6rem;
    letter-spacing: 3px;
    color: var(--cyan);
    margin-bottom: 10px;
    text-transform: uppercase;
  }

  .kv { display:flex; justify-content:space-between; padding:3px 0; border-bottom:1px solid var(--border); font-size:.7rem; }
  .kv:last-child { border:none; }
  .kv .k { color:#555; }
  .kv .v { color:var(--green); }
  .kv .v.red  { color:var(--red); }
  .kv .v.amber{ color:var(--amber); }

  .bar-wrap { margin:6px 0; }
  .bar-label { font-size:.65rem; color:#555; margin-bottom:3px; display:flex; justify-content:space-between; }
  .bar-track { height:4px; background:#ffffff08; border-radius:2px; overflow:hidden; }
  .bar-fill  { height:100%; border-radius:2px; transition: width .8s cubic-bezier(.4,0,.2,1); }
  .bar-fill.green { background: linear-gradient(90deg, var(--green), #00ffaa); box-shadow:0 0 8px var(--green); }
  .bar-fill.red   { background: linear-gradient(90deg, var(--red),   #ff6644); box-shadow:0 0 8px var(--red); }
  .bar-fill.amber { background: linear-gradient(90deg, var(--amber),  #ffdd44); box-shadow:0 0 8px var(--amber); }

  .badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 2px;
    font-size: .65rem;
    letter-spacing: 1px;
    text-transform: uppercase;
  }
  .badge.ok  { background:#00ff8818; color:var(--green); border:1px solid var(--green); }
  .badge.err { background:#ff223318; color:var(--red);   border:1px solid var(--red); }

  /* ── INPUT ── */
  .input-row {
    grid-column: 1 / -1;
    display: flex;
    align-items: center;
    background: var(--mid);
    border-top: 1px solid var(--red);
    padding: 8px 14px;
    gap: 10px;
    flex-shrink: 0;
  }

  .prompt-glyph {
    font-family: 'Orbitron', sans-serif;
    font-size: .85rem;
    font-weight: 900;
    color: var(--red);
    text-shadow: 0 0 12px var(--red);
    flex-shrink: 0;
  }

  #cmd {
    flex: 1;
    background: transparent;
    border: none;
    outline: none;
    color: var(--amber);
    font-family: 'Share Tech Mono', monospace;
    font-size: .85rem;
    caret-color: var(--red);
  }

  #cmd::placeholder { color: #333; }

  .send-btn {
    background: var(--red);
    color: #000;
    border: none;
    padding: 5px 14px;
    font-family: 'Orbitron', sans-serif;
    font-size: .6rem;
    font-weight: 700;
    letter-spacing: 2px;
    cursor: pointer;
    border-radius: 2px;
    transition: all .15s;
  }

  .send-btn:hover { background: var(--amber); transform: scale(1.05); }

  /* Quick actions */
  .quick-actions {
    grid-column: 1 / -1;
    display: flex;
    gap: 6px;
    padding: 6px 14px;
    background: var(--dark);
    border-top: 1px solid var(--border);
    flex-wrap: wrap;
    flex-shrink: 0;
  }

  .qa {
    background: #ffffff06;
    border: 1px solid var(--border);
    color: #555;
    font-family: 'Share Tech Mono', monospace;
    font-size: .6rem;
    padding: 3px 10px;
    cursor: pointer;
    border-radius: 2px;
    transition: all .15s;
    letter-spacing: 1px;
  }
  .qa:hover { background: #ff223318; color: var(--red); border-color: var(--red); }

  /* Scan animation for cards */
  .v-card::before {
    content:'';
    display:block;
    height:1px;
    background: linear-gradient(90deg, transparent, var(--cyan), transparent);
    margin-bottom:10px;
    animation: scan 3s ease infinite;
    opacity:.4;
  }
  @keyframes scan { 0%,100%{opacity:.1} 50%{opacity:.6} }

  .connecting {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    flex-direction: column;
    gap: 12px;
    color: var(--red);
    font-family: 'Orbitron', sans-serif;
    font-size: .7rem;
    letter-spacing: 3px;
    animation: pulse 1s infinite;
  }

  .spinner {
    width: 30px; height: 30px;
    border: 2px solid #ff223333;
    border-top-color: var(--red);
    border-radius: 50%;
    animation: spin .8s linear infinite;
  }
  @keyframes spin { to { transform: rotate(360deg); } }
</style>
</head>
<body>

<header>
  <div class="logo">HADES <span>TERMINAL</span> vΩ</div>
  <div class="status-bar">
    <div class="stat" id="s-ws">
      <div class="dot"></div> SOCKET
    </div>
    <div class="stat" id="s-agent">
      <div class="dot"></div> AGENT
    </div>
    <div class="stat" id="s-cpu">
      <div class="dot"></div> CPU —
    </div>
    <div class="stat" id="s-ram">
      <div class="dot"></div> RAM —
    </div>
  </div>
</header>

<div class="workspace">

  <!-- LEFT: raw JSON output -->
  <div class="panel">
    <div class="panel-header">◈ JSON <span>RAW OUTPUT</span></div>
    <div id="output">
      <div class="connecting" id="connecting">
        <div class="spinner"></div>
        CONECTANDO AL AGENTE...
      </div>
    </div>
  </div>

  <!-- RIGHT: visual render -->
  <div class="panel">
    <div class="panel-header">◈ <span>VISUAL</span> RENDER</div>
    <div id="visual"></div>
  </div>

  <!-- BOTTOM: input -->
  <div class="input-row">
    <div class="prompt-glyph">HΩ»</div>
    <input id="cmd" type="text"
           placeholder='{"action":"ping"}'
           autocomplete="off" spellcheck="false">
    <button class="send-btn" onclick="send()">EXEC</button>
  </div>

  <div class="quick-actions">
    <button class="qa" onclick="quick('ping')">PING</button>
    <button class="qa" onclick="quick('estado_sistema')">ESTADO</button>
    <button class="qa" onclick="quick('sync_hardware')">HARDWARE</button>
    <button class="qa" onclick="quick('wallet')">WALLET</button>
    <button class="qa" onclick="quick('protocolo')">PROTOCOLO</button>
    <button class="qa" onclick="quick('listar_agentes')">AGENTES</button>
    <button class="qa" onclick="quick('crontab')">CRON</button>
    <button class="qa" onclick="quick('pruebas_vida')">PRUEBAS</button>
  </div>

</div>

<script>
let ws, history = [], hIdx = -1;

function connect() {
  ws = new WebSocket(`ws://${location.hostname}:""" + str(WS_PORT) + r"""`);

  ws.onopen = () => {
    setStatus('s-ws', true, 'SOCKET');
    document.getElementById('connecting').style.display = 'none';
    // warm up
    ws.send(JSON.stringify({action:'ping'}));
    ws.send(JSON.stringify({action:'sync_hardware'}));
  };

  ws.onmessage = e => {
    try {
      const data = JSON.parse(e.data);
      renderJSON(data);
      renderVisual(data);
      updateStatusFromData(data);
    } catch(err) {
      renderRaw(e.data);
    }
  };

  ws.onclose = () => {
    setStatus('s-ws', false, 'SOCKET');
    setStatus('s-agent', false, 'AGENT');
    setTimeout(connect, 3000);
  };
}

function setStatus(id, on, label) {
  const el = document.getElementById(id);
  el.className = 'stat ' + (on ? 'on' : 'off');
  el.innerHTML = `<div class="dot"></div> ${label}`;
}

function quick(action) {
  document.getElementById('cmd').value = JSON.stringify({action});
  send();
}

function send() {
  const input = document.getElementById('cmd');
  const raw = input.value.trim();
  if (!raw || !ws || ws.readyState !== 1) return;

  let payload;
  try {
    payload = JSON.parse(raw);
  } catch {
    // try as bare action name
    payload = {action: raw};
  }

  history.unshift(raw);
  hIdx = -1;

  addCmd(JSON.stringify(payload, null, 2));
  ws.send(JSON.stringify(payload));
  input.value = '';
}

document.getElementById('cmd').addEventListener('keydown', e => {
  if (e.key === 'Enter') { send(); return; }
  if (e.key === 'ArrowUp') {
    hIdx = Math.min(hIdx + 1, history.length - 1);
    e.target.value = history[hIdx] || '';
  }
  if (e.key === 'ArrowDown') {
    hIdx = Math.max(hIdx - 1, -1);
    e.target.value = hIdx < 0 ? '' : history[hIdx];
  }
});

// ── JSON SYNTAX HIGHLIGHT ──
function highlight(obj) {
  const s = JSON.stringify(obj, null, 2);
  return s
    .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
    .replace(/"([^"]+)":/g, '<span class="j-key">"$1"</span>:')
    .replace(/: "([^"]*)"/g, ': <span class="j-str">"$1"</span>')
    .replace(/: (\d+\.?\d*)/g, ': <span class="j-num">$1</span>')
    .replace(/: (true|false)/g, ': <span class="j-bool">$1</span>')
    .replace(/: null/g, ': <span class="j-null">null</span>');
}

function addCmd(txt) {
  const out = document.getElementById('output');
  const div = document.createElement('div');
  div.className = 'entry';
  div.innerHTML = `<div class="entry-cmd">${txt}</div>`;
  out.appendChild(div);
  out.scrollTop = out.scrollHeight;
}

function renderJSON(data) {
  const out = document.getElementById('output');
  // find last entry without response
  const entries = out.querySelectorAll('.entry');
  const last = entries[entries.length - 1];
  const isErr = data.error !== undefined;
  const div = document.createElement('div');
  div.className = 'entry-out ' + (isErr ? 'err' : 'ok');
  div.innerHTML = highlight(data);
  if (last && !last.querySelector('.entry-out')) {
    last.appendChild(div);
  } else {
    const wrap = document.createElement('div');
    wrap.className = 'entry';
    wrap.appendChild(div);
    out.appendChild(wrap);
  }
  out.scrollTop = out.scrollHeight;
}

function renderRaw(text) {
  const out = document.getElementById('output');
  const div = document.createElement('div');
  div.className = 'entry';
  div.innerHTML = `<div class="entry-out err">${text}</div>`;
  out.appendChild(div);
}

// ── VISUAL RENDERER ──
function renderVisual(data) {
  const v = document.getElementById('visual');
  const action = data.action || (data.error ? 'error' : 'unknown');

  let html = '';

  if (action === 'pong') {
    const ts = new Date(data.ts * 1000).toLocaleTimeString();
    html = card('PING / PONG', `
      <div class="kv"><span class="k">STATUS</span><span class="v"><span class="badge ok">ONLINE</span></span></div>
      <div class="kv"><span class="k">TIMESTAMP</span><span class="v">${ts}</span></div>
      <div class="kv"><span class="k">LATENCY</span><span class="v amber">&lt; 1ms</span></div>
    `);
  }

  else if (action === 'hardware' || data.cpu) {
    const cpu = parseInt(data.cpu) || 0;
    const ram = parseInt(data.ram_mb) || 0;
    const ramMax = 8192;
    const ramPct = Math.round(ram / ramMax * 100);
    const stor = data.storage || '—';
    html = card('HARDWARE', `
      <div class="kv"><span class="k">CPU CORES</span><span class="v green">${cpu}</span></div>
      <div class="kv"><span class="k">STORAGE</span><span class="v amber">${stor}</span></div>
      <div class="bar-wrap">
        <div class="bar-label"><span>RAM</span><span style="color:var(--green)">${ram} MB / ${ramMax} MB</span></div>
        <div class="bar-track"><div class="bar-fill green" style="width:${ramPct}%"></div></div>
      </div>
    `);
  }

  else if (action === 'estado' || action === 'estado_sistema') {
    const bot = data.bot || '—';
    const web = data.web?.code || data.web?.status || '—';
    const gh  = data.github?.code || data.github?.status || '—';
    const cr  = data.crontab || '—';
    html = card('ESTADO DEL SISTEMA', `
      <div class="kv"><span class="k">BOT TELEGRAM</span>
        <span class="v ${bot==='activo'?'':'red'}">
          <span class="badge ${bot==='activo'?'ok':'err'}">${bot.toUpperCase()}</span>
        </span>
      </div>
      <div class="kv"><span class="k">WEB</span><span class="v ${web==200?'':'red'}">${web}</span></div>
      <div class="kv"><span class="k">GITHUB</span><span class="v ${gh==200?'':'red'}">${gh}</span></div>
      <div class="kv"><span class="k">CRONTAB</span><span class="v amber">${cr}</span></div>
    `);
  }

  else if (action === 'wallet') {
    const addr = data.address || '—';
    const btc  = data.balance_btc || data.balance_sat || '0';
    html = card('WALLET BTC', `
      <div class="kv"><span class="k">ADDRESS</span><span class="v amber" style="font-size:.6rem">${addr.slice(0,16)}…</span></div>
      <div class="kv"><span class="k">BALANCE</span><span class="v green">${btc} BTC</span></div>
    `);
  }

  else if (action === 'protocolo') {
    html = card('PROTOCOLO HADES', `
      <div class="kv"><span class="k">VERSION</span><span class="v green">${data.version||'vΩ'}</span></div>
      <div class="kv"><span class="k">NCP</span><span class="v amber">${data.ncp||data.ncpC||'x90'}</span></div>
      <div class="kv"><span class="k">AGENTES</span><span class="v">${data.agentes||data.agents||'—'}</span></div>
      <div class="kv"><span class="k">PROMPTS</span><span class="v">${data.prompts||'—'}</span></div>
      <div class="kv"><span class="k">SCRIPTS</span><span class="v">${data.scripts||'—'}</span></div>
      <div class="kv"><span class="k">LÍNEAS</span><span class="v">${data.lineas||data.lines||'—'}</span></div>
    `);
  }

  else if (action === 'listar_agentes') {
    const cats = data.categorias || data.categories || {};
    const rows = Object.entries(cats).map(([k,v]) => {
      const count = Array.isArray(v) ? v.length : (v.count || '?');
      return `<div class="kv"><span class="k">${k}</span><span class="v amber">${count} agentes</span></div>`;
    }).join('');
    html = card(`AGENTES (${data.total||'—'})`, rows);
  }

  else if (action === 'difusion') {
    const total = data.total || 0;
    const sent  = data.enviados || data.sent || 0;
    const pct   = total ? Math.round(sent/total*100) : 0;
    html = card('DIFUSIÓN TELEGRAM', `
      <div class="kv"><span class="k">TOTAL TARGETS</span><span class="v">${total}</span></div>
      <div class="kv"><span class="k">ENVIADOS</span><span class="v green">${sent}</span></div>
      <div class="bar-wrap">
        <div class="bar-label"><span>ÉXITO</span><span style="color:var(--green)">${pct}%</span></div>
        <div class="bar-track"><div class="bar-fill ${pct>50?'green':'red'}" style="width:${pct}%"></div></div>
      </div>
    `);
  }

  else if (action === 'ejecutar_bash' || action === 'exec_bash') {
    const out = data.salida || data.output || '';
    const code = data.codigo !== undefined ? data.codigo : (data.code !== undefined ? data.code : '?');
    html = card('BASH OUTPUT', `
      <div class="kv"><span class="k">EXIT CODE</span>
        <span class="v ${code===0||code==='0'?'':'red'}">${code}</span>
      </div>
      <div style="margin-top:8px;font-size:.65rem;color:#778;line-height:1.6;white-space:pre-wrap;word-break:break-all;max-height:160px;overflow-y:auto">${out||'(sin output)'}</div>
    `);
  }

  else if (data.error) {
    html = card('ERROR', `
      <div class="kv"><span class="k">TYPE</span><span class="v red">${data.error}</span></div>
      ${data.action ? `<div class="kv"><span class="k">ACTION</span><span class="v">${data.action}</span></div>` : ''}
    `);
  }

  else {
    // Generic key-value render
    const rows = Object.entries(data)
      .map(([k,v]) => `<div class="kv"><span class="k">${k}</span><span class="v">${JSON.stringify(v)}</span></div>`)
      .join('');
    html = card(action.toUpperCase(), rows);
  }

  if (html) {
    v.innerHTML = html + v.innerHTML;
  }
}

function card(title, body) {
  return `<div class="v-card"><h3>${title}</h3>${body}</div>`;
}

function updateStatusFromData(data) {
  if (data.action === 'pong') setStatus('s-agent', true, 'AGENT');
  if (data.cpu) {
    setStatus('s-cpu', true, `CPU ${data.cpu}c`);
    const pct = Math.round(parseInt(data.ram_mb)/8192*100);
    setStatus('s-ram', true, `RAM ${pct}%`);
  }
  if (data.action === 'estado' || data.action === 'estado_sistema') {
    setStatus('s-agent', data.bot === 'activo', 'AGENT');
  }
}

connect();
</script>
</body>
</html>
"""

# ── HTTP SERVER ──
class UI(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(HTML.encode())
    def log_message(self, *a): pass

def run_http():
    httpd = HTTPServer(('0.0.0.0', HTTP_PORT), UI)
    httpd.serve_forever()

# ── WEBSOCKET BRIDGE ──
def talk_to_agent(proc, cmd_json):
    """Send JSON command to agent, get response."""
    try:
        proc.stdin.write(cmd_json + '\n')
        proc.stdin.flush()
        line = proc.stdout.readline()
        return line.strip() or '{}'
    except Exception as e:
        return json.dumps({'error': str(e)})

async def bridge(websocket):
    print(f"[WS] Cliente conectado: {websocket.remote_address}")

    proc = subprocess.Popen(
        ['/data/data/com.termux/files/usr/bin/bash', AGENT_SCRIPT],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        bufsize=1
    )

    # consume startup line
    try:
        proc.stdout.readline()
    except: pass

    loop = asyncio.get_event_loop()

    try:
        async for message in websocket:
            message = message.strip()
            if not message:
                continue
            try:
                json.loads(message)  # validate
            except json.JSONDecodeError:
                await websocket.send(json.dumps({'error': 'json_invalido', 'input': message}))
                continue

            result = await loop.run_in_executor(None, talk_to_agent, proc, message)
            await websocket.send(result)
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        try:
            proc.terminate()
        except: pass
        print("[WS] Cliente desconectado")

async def run_ws():
    async with websockets.serve(bridge, '0.0.0.0', WS_PORT):
        print(f"[WS] Escuchando en ws://0.0.0.0:{WS_PORT}")
        await asyncio.Future()

# ── MAIN ──
if __name__ == '__main__':
    print(f"""
╔══════════════════════════════════════════╗
║   HADES TERMINAL vΩ — INICIANDO          ║
╠══════════════════════════════════════════╣
║  Agente : {AGENT_SCRIPT[:36]}
║  HTTP   : http://0.0.0.0:{HTTP_PORT}
║  WS     : ws://0.0.0.0:{WS_PORT}
╚══════════════════════════════════════════╝
Abre en tu navegador: http://localhost:{HTTP_PORT}
""")

    # HTTP en hilo separado
    t = threading.Thread(target=run_http, daemon=True)
    t.start()

    # WebSocket en asyncio
    try:
        asyncio.run(run_ws())
    except KeyboardInterrupt:
        print("\n[HADES] Terminal apagada.")
