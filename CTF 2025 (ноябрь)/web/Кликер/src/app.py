"""
Flask Clicker — single-file Flask app with frontend and mechanics.
Run: python flask_clicker.py
Requires: Flask (pip install flask)

Features:
- Click to earn coins
- Buildings that produce coins per second (CPS)
- Upgrades that increase click value or building output
- Prestige (reset for prestige points)
- Achievements
- Offline progress (based on last save time)
- Simple leaderboard stored in sqlite
- Per-player persistence via a server-side sqlite DB keyed by session id

This file contains everything: Flask app, simple DB, templates rendered via render_template_string.
"""

from flask import Flask, request, jsonify, render_template_string, g, redirect, url_for, make_response
import sqlite3
import time
import uuid
import math
import os
from datetime import datetime

DB_PATH = 'clicker.db'
SAVE_INTERVAL = 10  # seconds for auto-save on client (client-side; server accepts anytime)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'replace-with-secure-secret'

# -------------------- Database helpers --------------------

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        need_init = not os.path.exists(DB_PATH)
        db = g._database = sqlite3.connect(DB_PATH, check_same_thread=False)
        db.row_factory = sqlite3.Row
        if need_init:
            init_db(db)
    return db


def init_db(db):
    c = db.cursor()
    c.execute('''
        CREATE TABLE players (
            sid TEXT PRIMARY KEY,
            data TEXT,
            last_save INTEGER,
            total_coins REAL DEFAULT 0
        )
    ''')
    c.execute('''
        CREATE TABLE leaderboard (
            sid TEXT PRIMARY KEY,
            name TEXT,
            best_coins REAL,
            updated INTEGER
        )
    ''')
    db.commit()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# -------------------- Game definitions --------------------

# Base game configuration
BUILDINGS = [
    { 'id': 'cursor', 'name': 'Cursor', 'base_cost': 15, 'base_cps': 0.1, 'desc': 'Small helper that clicks for you.' },
    { 'id': 'factory', 'name': 'Factory', 'base_cost': 100, 'base_cps': 1, 'desc': 'Produces coins steadily.' },
    { 'id': 'bank', 'name': 'Bank', 'base_cost': 1100, 'base_cps': 8, 'desc': 'Large-scale production.' },
]

UPGRADES = [
    { 'id': 'click_power_2', 'name': 'Double Click', 'cost': 100, 'type': 'click', 'mult': 2, 'desc': 'Double coin per manual click.' },
    { 'id': 'factory_boost', 'name': 'Factory Boost', 'cost': 500, 'type': 'building', 'target': 'factory', 'mult': 2, 'desc': 'Factory output x2.' },
]

ACHIEVEMENTS = [
    {'id':'first_click','name':'First Click','hint':'Click once.','condition': lambda s: s['total_coins']>=1},
    {'id':'small_empire','name':'Small Empire','hint':'Own 10 Cursors.','condition': lambda s: s['buildings'].get('cursor',0)>=10},
    {'id':'rich','name':'Rich','hint':'Reach 10000 total coins.','condition': lambda s: s['total_coins']>=10000},
]

# -------------------- Player state handling --------------------

def make_default_state():
    now = int(time.time())
    return {
        'coins': 0.0,
        'total_coins': 0.0,
        'click_value': 1.0,
        'buildings': {},  # id -> count
        'upgrades': [],
        'prestige_points': 0,
        'prestige_level': 0,
        'achievements': [],
        'last_ts': now,
        'name': None,
    }


def load_state(sid):
    db = get_db()
    cur = db.execute('SELECT data, last_save, total_coins FROM players WHERE sid = ?', (sid,))
    row = cur.fetchone()
    if not row:
        state = make_default_state()
        save_state(sid, state)
        return state
    else:
        import json
        state = json.loads(row['data'])
        # server-side total_coins may be kept separately for leaderboard purposes
        state['total_coins'] = row['total_coins']
        return state


def save_state(sid, state):
    db = get_db()
    import json
    now = int(time.time())
    total = state.get('total_coins', 0)
    db.execute('REPLACE INTO players (sid, data, last_save, total_coins) VALUES (?, ?, ?, ?)',
               (sid, json.dumps(state), now, total))
    db.commit()
    # update leaderboard best
    cur = db.execute('SELECT best_coins FROM leaderboard WHERE sid=?', (sid,))
    row = cur.fetchone()
    name = state.get('name') or 'Player'
    if not row:
        db.execute('REPLACE INTO leaderboard (sid, name, best_coins, updated) VALUES (?, ?, ?, ?)',
                   (sid, name, total, now))
    else:
        best = row['best_coins']
        if total > best:
            db.execute('UPDATE leaderboard SET best_coins=?, name=?, updated=? WHERE sid=?', (total, name, now, sid))
    db.commit()

# -------------------- Game mechanics --------------------

def compute_cps(state):
    cps = 0.0
    for b in BUILDINGS:
        count = state['buildings'].get(b['id'], 0)
        # cost multiplier or upgrade multiplier applied later
        base = b['base_cps'] * count
        cps += base
    # apply building-specific upgrades
    for upg in state['upgrades']:
        u = next((x for x in UPGRADES if x['id']==upg), None)
        if u and u['type']=='building':
            target = u['target']
            # multiply CPS for that target
            b = next((x for x in BUILDINGS if x['id']==target), None)
            if b:
                count = state['buildings'].get(target,0)
                cps += b['base_cps']*count*(u['mult']-1)
    # prestige bonus: each prestige point gives 1% CPS
    cps *= (1 + 0.01 * state.get('prestige_points',0))
    return cps


def click_action(state):
    value = state['click_value']
    # apply click upgrades
    for upg in state['upgrades']:
        u = next((x for x in UPGRADES if x['id']==upg), None)
        if u and u['type']=='click':
            value *= u['mult']
    # prestige increases click slightly
    value *= (1 + 0.005 * state.get('prestige_points',0))
    state['coins'] += value
    state['total_coins'] += value
    return value


def buy_building(state, bid):
    b = next((x for x in BUILDINGS if x['id']==bid), None)
    if not b: return False, 'No such building'
    count = state['buildings'].get(bid, 0)
    # exponential cost: base_cost * (1.15^count)
    cost = b['base_cost'] * (1.15 ** count)
    cost = math.ceil(cost)
    if state['coins'] >= cost:
        state['coins'] -= cost
        state['buildings'][bid] = count + 1
        return True, {'cost': cost}
    else:
        return False, 'Not enough coins'


def buy_upgrade(state, uid):
    u = next((x for x in UPGRADES if x['id']==uid), None)
    if not u: return False, 'No such upgrade'
    if uid in state['upgrades']:
        return False, 'Already bought'
    if state['coins'] >= u['cost']:
        state['coins'] -= u['cost']
        state['upgrades'].append(uid)
        return True, {}
    return False, 'Not enough coins'


def check_achievements(state):
    unlocked = []
    for a in ACHIEVEMENTS:
        if a['id'] in state['achievements']:
            continue
        try:
            if a['condition'](state):
                state['achievements'].append(a['id'])
                unlocked.append(a)
        except Exception:
            pass
    return unlocked


def prestige_calculate(state):
    # Example formula: prestige points = floor(sqrt(total_coins/1000)) - current
    pts = int(math.sqrt(state['total_coins'] / 1000))
    return max(0, pts - state.get('prestige_level',0))


def apply_prestige(state):
    pts = prestige_calculate(state)
    if pts <= 0:
        return False, 'No prestige points available'
    state['prestige_points'] += pts
    state['prestige_level'] += pts
    # reset most progress
    state['coins'] = 0.0
    state['buildings'] = {}
    state['upgrades'] = []
    # keep total_coins as record
    return True, {'gained': pts}

# -------------------- HTTP routes --------------------

INDEX_HTML = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Flask Clicker</title>
  <style>
    body{font-family:Inter,Segoe UI,Arial;padding:20px;background:#0f172a;color:#e6eef8}
    .container{max-width:980px;margin:0 auto}
    .bigbtn{font-size:28px;padding:30px 50px;border-radius:12px;background:#06b6d4;border:none;color:#042c3a;cursor:pointer}
    .panel{background:#071129;padding:12px;border-radius:10px;margin-top:12px}
    .shop-item{display:flex;justify-content:space-between;padding:8px;border-bottom:1px dashed #113}
    .muted{opacity:0.7}
    .small{font-size:13px}
    .ach{background:#06283a;padding:8px;border-radius:6px;margin:6px 0}
  </style>
</head>
<body>
<div class="container">
  <h1>Flask Clicker</h1>
  <div class="panel">
    <div style="display:flex;gap:20px;align-items:center">
      <div>
        <button id="clicker" class="bigbtn">Click</button>
      </div>
      <div>
        <div style="font-size:24px">Coins: <span id="coins">0</span></div>
        <div class="muted small">Total coins: <span id="total_coins">0</span></div>
        <div class="muted small">CPS: <span id="cps">0</span> | Click: <span id="click_val">1</span></div>
        <div class="muted small">Prestige points: <span id="prestige_points">0</span></div>
      </div>
    </div>
  </div>

  <div class="panel">
    <h3>Shop</h3>
    <div id="shop"></div>
  </div>

  <div class="panel">
    <h3>Upgrades</h3>
    <div id="upgrades"></div>
  </div>

  <div class="panel">
    <h3>Achievements</h3>
    <div id="achievements"></div>
  </div>

  <div class="panel">
    <h3>Controls</h3>
    <button id="save">Save</button>
    <button id="prestige">Prestige</button>
    <input id="name" placeholder="Your name for leaderboard">
    <button id="update_name">Update name</button>
    <div class="small muted">Last save: <span id="last_save">never</span></div>
  </div>

  <div class="panel">
    <h3>Leaderboard</h3>
    <ol id="leaderboard"></ol>
  </div>

  <div style="height:40px"></div>
</div>

<script>
// Frontend game logic
let state = null;
let sid = null;

async function api(path, data){
  const res = await fetch(path, {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify(data||{})
  });
  return res.json();
}

function fmt(x){
  if(x >= 1e9) return (x/1e9).toFixed(2)+'B';
  if(x >= 1e6) return (x/1e6).toFixed(2)+'M';
  if(x >= 1e3) return (x/1e3).toFixed(2)+'k';
  return Math.floor(x*100)/100;
}

function render(){
  if(!state) return;
  document.getElementById('coins').innerText = fmt(state.coins);
  document.getElementById('total_coins').innerText = fmt(state.total_coins);
  document.getElementById('cps').innerText = fmt(state.cps);
  document.getElementById('click_val').innerText = fmt(state.click_val);
  document.getElementById('prestige_points').innerText = state.prestige_points;
  document.getElementById('last_save').innerText = state.last_save ? new Date(state.last_save*1000).toLocaleString() : 'never';

  // shop
  const shop = document.getElementById('shop'); shop.innerHTML = '';
  for(const b of state.building_defs){
    const count = state.buildings[b.id]||0;
    const cost = Math.ceil(b.base_cost * Math.pow(1.15, count));
    const div = document.createElement('div'); div.className='shop-item';
    div.innerHTML = `<div><strong>${b.name}</strong> <span class="muted small">x${count}</span><div class="small muted">${b.desc}</div></div><div><div>${fmt(cost)}</div><button onclick="buy_building('${b.id}')">Buy</button></div>`;
    shop.appendChild(div);
  }
  // upgrades
  const ups = document.getElementById('upgrades'); ups.innerHTML='';
  for(const u of state.upgrade_defs){
    const bought = state.upgrades.includes(u.id);
    const div = document.createElement('div'); div.className='shop-item';
    div.innerHTML = `<div><strong>${u.name}</strong>${bought?'<span class="muted small"> (bought)</span>':''}<div class="small muted">${u.desc}</div></div><div><div>${fmt(u.cost)}</div><button onclick="buy_upgrade('${u.id}')" ${bought?'disabled':''}>Buy</button></div>`;
    ups.appendChild(div);
  }
  // achievements
  const ach = document.getElementById('achievements'); ach.innerHTML='';
  for(const a of state.ach_defs){
    const unlocked = state.achievements.includes(a.id);
    const d = document.createElement('div'); d.className='ach'; d.innerHTML = `<strong>${a.name}</strong> ${unlocked?'<span class="muted">(unlocked)</span>':''}<div class="small muted">${a.hint}</div>`;
    ach.appendChild(d);
  }
  // leaderboard
  const lb = document.getElementById('leaderboard'); lb.innerHTML='';
  for(const row of state.leaderboard){
    const li = document.createElement('li'); li.innerText = `${row.name} — ${fmt(row.best_coins)}`; lb.appendChild(li);
  }
}

async function load(){
  const res = await fetch('/api/load');
  state = await res.json();
  // normalize
  state.cps = state.cps || 0;
  state.click_val = state.click_value || 1;
  // copy defs
  state.building_defs = state.building_defs || [];
  state.upgrade_defs = state.upgrade_defs || [];
  state.ach_defs = state.ach_defs || [];
  render();
}

async function clicker(){
  const res = await api('/api/click');
  state.coins = res.coins; state.total_coins = res.total_coins; state.cps = res.cps; state.click_val = res.click_val;
  const unlocked = res.unlocked || [];
  if(unlocked.length) alert('Achievements unlocked: '+unlocked.map(a=>a.name).join(', '));
  render();
}

async function buy_building(id){
  const res = await api('/api/buy_building', {id});
  if(!res.ok) alert(res.msg);
  else{ state.coins = res.coins; state.buildings = res.buildings; state.cps = res.cps; render(); }
}

async function buy_upgrade(id){
  const res = await api('/api/buy_upgrade',{id});
  if(!res.ok) alert(res.msg);
  else{ state.coins = res.coins; state.upgrades = res.upgrades; state.cps = res.cps; render(); }
}

async function tick(){
  const res = await api('/api/tick');
  state.coins = res.coins; state.total_coins = res.total_coins; state.cps = res.cps; state.achievements = res.achievements; render();
}

// controls
document.getElementById('clicker').addEventListener('click', clicker);
setInterval(async ()=>{
  // update local CPS
  if(!state) return;
  state.coins += state.cps/10; // tick every 100ms
  state.total_coins += state.cps/10;
  document.getElementById('coins').innerText = fmt(state.coins);
}, 100);

// server tick
setInterval(tick, 1000);
// auto-save
setInterval(()=>{ fetch('/api/save', {method:'POST'}); }, 15000);

// Save button
document.getElementById('save').addEventListener('click', async ()=>{ await api('/api/save'); alert('Saved'); });

// prestige
document.getElementById('prestige').addEventListener('click', async ()=>{
  const res = await api('/api/prestige');
  if(!res.ok) alert(res.msg);
  else{ alert('Prestiged! Gained '+res.gained+' points'); load(); }
});

// update name
document.getElementById('update_name').addEventListener('click', async ()=>{
  const v = document.getElementById('name').value;
  const res = await api('/api/set_name', {name:v});
  if(res.ok) alert('Name updated'); load();
});

load();
</script>
</body>
</html>
'''

@app.route('/')
def index():
    # ensure session id cookie
    sid = request.cookies.get('sid')
    if not sid:
        sid = str(uuid.uuid4())
    resp = make_response(render_template_string(INDEX_HTML))
    resp.set_cookie('sid', sid, max_age=60*60*24*365)
    resp.headers.set('Debug', 'FECTF{nginx_1n7_0v3rfl0w}')
    return resp

# API endpoints
@app.route('/api/load', methods=['GET', 'POST'])
def api_load():
    sid = request.cookies.get('sid')
    if not sid:
        sid = str(uuid.uuid4())
    state = load_state(sid)
    # compute offline progress
    now = int(time.time())
    last = state.get('last_ts', now)
    elapsed = max(0, now - last)
    cps = compute_cps(state)
    gained = cps * elapsed
    state['coins'] += gained
    state['total_coins'] += gained
    state['last_ts'] = now
    state['last_save'] = int(time.time())
    save_state(sid, state)
    # send public defs
    out = {
        'coins': state['coins'], 'total_coins': state['total_coins'], 'cps': compute_cps(state),
        'click_value': state['click_value'], 'click_val': state['click_value'],
        'buildings': state['buildings'], 'upgrades': state['upgrades'],
        'achievements': state['achievements'], 'prestige_points': state['prestige_points'],
        'last_save': state.get('last_save'), 'name': state.get('name'),
        'building_defs': BUILDINGS, 'upgrade_defs': UPGRADES, 'ach_defs': [{'id':a['id'],'name':a['name'],'hint':a['hint']} for a in ACHIEVEMENTS]
    }
    # leaderboard
    db = get_db()
    cur = db.execute('SELECT name, best_coins FROM leaderboard ORDER BY best_coins DESC LIMIT 10')
    out['leaderboard'] = [dict(r) for r in cur.fetchall()]
    resp = jsonify(out)
    resp.set_cookie('sid', sid, max_age=60*60*24*365)
    return resp

@app.route('/api/click', methods=['POST'])
def api_click():
    sid = request.cookies.get('sid')
    if not sid: return jsonify({'ok':False,'msg':'No session'}), 400
    state = load_state(sid)
    # compute offline
    now = int(time.time())
    elapsed = now - state.get('last_ts', now)
    if elapsed > 0:
        gained = compute_cps(state) * elapsed
        state['coins'] += gained
        state['total_coins'] += gained
    val = click_action(state)
    state['last_ts'] = now
    state['cps'] = compute_cps(state)
    unlocked = check_achievements(state)
    save_state(sid, state)
    return jsonify({'ok':True, 'coins': state['coins'], 'total_coins': state['total_coins'], 'cps': state['cps'], 'click_val': val, 'unlocked': [a['id'] for a in unlocked], 'unlocked_full': unlocked})

@app.route('/api/tick', methods=['POST'])
def api_tick():
    sid = request.cookies.get('sid')
    if not sid: return jsonify({'ok':False})
    state = load_state(sid)
    now = int(time.time())
    elapsed = now - state.get('last_ts', now)
    if elapsed > 0:
        gained = compute_cps(state) * elapsed
        state['coins'] += gained
        state['total_coins'] += gained
    state['last_ts'] = now
    state['cps'] = compute_cps(state)
    unlocked = check_achievements(state)
    save_state(sid, state)
    return jsonify({'ok':True, 'coins': state['coins'], 'total_coins': state['total_coins'], 'cps': state['cps'], 'achievements':[a for a in state['achievements']], 'unlocked':[a['id'] for a in unlocked]})

@app.route('/api/buy_building', methods=['POST'])
def api_buy_building():
    sid = request.cookies.get('sid')
    data = request.get_json() or {}
    bid = data.get('id')
    state = load_state(sid)
    ok, info = buy_building(state, bid)
    if not ok:
        return jsonify({'ok':False, 'msg':info})
    state['cps'] = compute_cps(state)
    save_state(sid, state)
    return jsonify({'ok':True, 'coins': state['coins'], 'buildings': state['buildings'], 'cps': state['cps']})

@app.route('/api/buy_upgrade', methods=['POST'])
def api_buy_upgrade():
    sid = request.cookies.get('sid')
    data = request.get_json() or {}
    uid = data.get('id')
    state = load_state(sid)
    ok, info = buy_upgrade(state, uid)
    if not ok:
        return jsonify({'ok':False, 'msg':info})
    state['cps'] = compute_cps(state)
    save_state(sid, state)
    return jsonify({'ok':True, 'coins': state['coins'], 'upgrades': state['upgrades'], 'cps': state['cps']})

@app.route('/api/save', methods=['POST'])
def api_save():
    sid = request.cookies.get('sid')
    if not sid: return jsonify({'ok':False})
    state = load_state(sid)
    state['last_save'] = int(time.time())
    save_state(sid, state)
    return jsonify({'ok':True})

@app.route('/api/set_name', methods=['POST'])
def api_set_name():
    sid = request.cookies.get('sid')
    data = request.get_json() or {}
    name = data.get('name','')[:32]
    state = load_state(sid)
    state['name'] = name
    save_state(sid, state)
    return jsonify({'ok':True})

@app.route('/api/prestige', methods=['POST'])
def api_prestige():
    sid = request.cookies.get('sid')
    state = load_state(sid)
    pts = prestige_calculate(state)
    if pts <= 0:
        return jsonify({'ok':False,'msg':'No prestige points available'})
    ok, info = apply_prestige(state)
    save_state(sid, state)
    return jsonify({'ok':True, 'gained': info['gained']})

# -------------------- Run --------------------

if __name__ == '__main__':
    print('Starting Flask Clicker on http://127.0.0.1:5000')
    app.run(host='0.0.0.0', debug=False)
