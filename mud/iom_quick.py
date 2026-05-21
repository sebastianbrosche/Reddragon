#!/usr/bin/env python3
"""Quick IOM sebbe session - captures key data and exits"""
import socket, time, re, os

HOST, PORT = 'islandsofmyth.org', 3000
LOGDIR = '/root/.openclaw/workspace/mud/iom_sebbe_quick'
os.makedirs(LOGDIR, exist_ok=True)

def clean(t):
    return re.sub(r'\x1b\[[0-9;]*m', '', t)

def get(s, wait=2):
    time.sleep(wait)
    d = b''
    try:
        while True:
            c = s.recv(8192)
            if not c: break
            d += c
            time.sleep(0.5)
            try:
                c2 = s.recv(8192)
                if c2: d += c2
            except: break
    except: pass
    return d.decode('utf-8', errors='replace')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(10)
s.connect((HOST, PORT))

# Read login screen
data = get(s, 1)
with open(f'{LOGDIR}/00_login_prompt.txt', 'w') as f:
    f.write(clean(data))

# Login
s.send(b'sebbe\n')
data = get(s, 1)
with open(f'{LOGDIR}/01_password_prompt.txt', 'w') as f:
    f.write(clean(data))

s.send(b'creative\n')
data = get(s, 2)
with open(f'{LOGDIR}/02_post_login.txt', 'w') as f:
    f.write(clean(data))

# Core commands
cmds = ['look', 'exits', 'inventory', 'score', 'who', 'skills', 'spells', 'eq']
for cmd in cmds:
    s.send((cmd + '\n').encode())
    r = get(s, 1.5)
    with open(f'{LOGDIR}/cmd_{cmd}.txt', 'w') as f:
        f.write(clean(r))
    print(f'{cmd}: {len(r)} chars')

# Movement from start room
dirs = ['north', 'south', 'east', 'west', 'up', 'down']
back = {'north':'south','south':'north','east':'west','west':'east','up':'down','down':'up'}
for d in dirs:
    s.send((d + '\n').encode())
    r = get(s, 1.5)
    with open(f'{LOGDIR}/go_{d}.txt', 'w') as f:
        f.write(clean(r))
    s.send((back[d] + '\n').encode())
    get(s, 1)

s.close()
print(f'Done. Logs in {LOGDIR}')
