from flask import Flask, jsonify, render_template_string
import pymem
import threading
import time

PROCESS_NAME   = "Gothic2.exe"
STATIC_PTR     = 0x8CECBC
OFFSETS = {
    "hp_cur":   0x1B8,
    "hp_max":   0x1BC,
    "mana_cur": 0x1C0,
    "mana_max": 0x1C4,
    "level":    0x234,
    "exp":      0x42C,
    "next_lvl": 0x430,
    "lp":       0x434,
}

app = Flask(__name__)
stats_cache = {}
pm = None

def get_prev_level_exp(level):
    return level * 250 * (level+1)

def connect():
    global pm
    while True:
        try:
            pm = pymem.Pymem(PROCESS_NAME)
            print(f"[+] Attached to {PROCESS_NAME} (PID {pm.process_id})")
            return
        except Exception:
            print("[-] Gothic2.exe not found, retrying...")
            time.sleep(2)

def poll_stats():
    global pm
    while True:
        try:
            obj_base = pm.read_uint(STATIC_PTR)
            if obj_base:
                s = {name: pm.read_int(obj_base + off) for name, off in OFFSETS.items()}
                cur_level = s["level"]
                s["prev_level_exp"] = get_prev_level_exp(cur_level)
                stats_cache.update(s)
        except Exception:
            stats_cache.clear()
            print("[-] Lost connection, reconnecting...")
            connect()
        time.sleep(0.5)

HTML = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Gothic 2 HUD</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: #0e0c0a;
      color: #d4c5a9;
      font-family: 'Georgia', serif;
      padding: 20px;
      min-height: 100vh;
    }
    h1 {
      text-align: center;
      font-size: 1.2rem;
      letter-spacing: 3px;
      text-transform: uppercase;
      color: #a08050;
      margin-bottom: 24px;
      border-bottom: 1px solid #333;
      padding-bottom: 12px;
    }
    .card {
      background: #1a1612;
      border: 1px solid #2e2820;
      border-radius: 6px;
      padding: 14px 18px;
      margin-bottom: 14px;
    }
    .row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 6px;
    }
    .label { font-size: 0.75rem; letter-spacing: 1px; text-transform: uppercase; color: #7a6a50; }
    .value { font-size: 1rem; color: #e8d9b8; }
    .bar-bg { background: #2a2420; border-radius: 3px; height: 8px; overflow: hidden; }
    .bar-fill { height: 100%; border-radius: 3px; transition: width 0.4s ease; }
    .bar-hp   { background: linear-gradient(90deg, #8b2020, #c44); }
    .bar-mana { background: linear-gradient(90deg, #1a2d6e, #36c); }
    .bar-exp  { background: linear-gradient(90deg, #4a3a10, #a80); }
    .stat-grid {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 10px;
      margin-bottom: 14px;
    }
    .stat-box {
      background: #1a1612;
      border: 1px solid #2e2820;
      border-radius: 6px;
      padding: 12px;
      text-align: center;
    }
    .stat-box .big { font-size: 1.6rem; color: #e8d9b8; }
    .stat-box .lbl { font-size: 0.65rem; color: #7a6a50; letter-spacing: 1px; text-transform: uppercase; margin-top: 2px; }
    #status { text-align: center; font-size: 0.7rem; color: #444; margin-top: 16px; }
  </style>
</head>
<body>
  <h1>&#9876; Gothic II</h1>

  <div class="stat-grid">
    <div class="stat-box">
      <div class="big" id="level">—</div>
      <div class="lbl">Level</div>
    </div>
    <div class="stat-box">
      <div class="big" id="lp">—</div>
      <div class="lbl">Learn pts</div>
    </div>
    <div class="stat-box">
      <div class="big" id="exp_pct">—</div>
      <div class="lbl">EXP %</div>
    </div>
  </div>

  <div class="card">
    <div class="row">
      <span class="label">HP</span>
      <span class="value"><span id="hp_cur">—</span> / <span id="hp_max">—</span></span>
    </div>
    <div class="bar-bg"><div class="bar-fill bar-hp" id="bar_hp" style="width:0%"></div></div>
  </div>

  <div class="card">
    <div class="row">
      <span class="label">Mana</span>
      <span class="value"><span id="mana_cur">—</span> / <span id="mana_max">—</span></span>
    </div>
    <div class="bar-bg"><div class="bar-fill bar-mana" id="bar_mana" style="width:0%"></div></div>
  </div>

  <div class="card">
    <div class="row">
      <span class="label">Experience</span>
      <span class="value"><span id="exp">—</span> / <span id="next_lvl">—</span></span>
    </div>
    <div class="bar-bg"><div class="bar-fill bar-exp" id="bar_exp" style="width:0%"></div></div>
    <div class="row" style="margin-top:6px">
      <span class="label">To next level</span>
      <span class="value" id="exp_remaining">—</span>
    </div>
  </div>

  <div id="status">connecting...</div>

  <script>
    function fmt(n) { return n.toLocaleString(); }

    async function update() {
      try {
        const r = await fetch('/api/stats');
        const s = await r.json();
        if (s.error) { document.getElementById('status').textContent = 'Game not running'; return; }

        const level_range    = s.next_lvl - s.prev_level_exp;
        const level_progress = s.exp - s.prev_level_exp;
        const exp_pct        = level_range > 0 ? Math.min(100, level_progress / level_range * 100) : 0;

        document.getElementById('level').textContent         = s.level;
        document.getElementById('lp').textContent            = s.lp;
        document.getElementById('hp_cur').textContent        = fmt(s.hp_cur);
        document.getElementById('hp_max').textContent        = fmt(s.hp_max);
        document.getElementById('mana_cur').textContent      = fmt(s.mana_cur);
        document.getElementById('mana_max').textContent      = fmt(s.mana_max);
        document.getElementById('exp').textContent           = fmt(s.exp);
        document.getElementById('next_lvl').textContent      = fmt(s.next_lvl);
        document.getElementById('exp_remaining').textContent = fmt(s.next_lvl - s.exp);
        document.getElementById('exp_pct').textContent       = exp_pct.toFixed(1) + '%';

        document.getElementById('bar_hp').style.width        = Math.min(100, s.hp_cur / s.hp_max * 100) + '%';
        document.getElementById('bar_mana').style.width      = Math.min(100, s.mana_cur / s.mana_max * 100) + '%';
        document.getElementById('bar_exp').style.width       = exp_pct + '%';

        document.getElementById('status').textContent = 'Updated ' + new Date().toLocaleTimeString();
      } catch(e) {
        document.getElementById('status').textContent = 'Error: ' + e.message;
      }
    }

    update();
    setInterval(update, 1000);
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/api/stats")
def api_stats():
    if not stats_cache:
        return jsonify({"error": "no data"})
    return jsonify(stats_cache)

if __name__ == "__main__":
    connect()
    t = threading.Thread(target=poll_stats, daemon=True)
    t.start()
    print("[*] Open http://<your-pc-ip>:5000 on your phone")
    app.run(host="0.0.0.0", port=5000)