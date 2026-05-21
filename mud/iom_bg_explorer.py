#!/usr/bin/env python3
"""Background IOM explorer - runs standalone, nohup"""
import socket, time, re, os, json, sys

HOST, PORT = 'islandsofmyth.org', 3000
LOGDIR = '/root/.openclaw/workspace/mud/iom_sebbe_archive'
os.makedirs(LOGDIR, exist_ok=True)

def clean(t):
    return re.sub(r'\x1b\[[0-9;]*m', '', t)

def recv_all(s, timeout=3):
    s.settimeout(timeout)
    d = b''
    try:
        while True:
            c = s.recv(16384)
            if not c: break
            d += c
    except socket.timeout:
        pass
    except:
        pass
    return d.decode('utf-8', errors='replace')

def send_cmd(s, cmd, wait=2):
    if cmd:
        s.send((cmd + '\n').encode())
    time.sleep(wait)
    return clean(recv_all(s))

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    s.connect((HOST, PORT))
    
    # Login
    recv_all(s, 2)
    s.send(b'sebbe\n')
    recv_all(s, 1)
    s.send(b'creative\n')
    login_data = recv_all(s, 2)
    
    with open(f'{LOGDIR}/login.txt', 'w') as f:
        f.write(clean(login_data))
    
    # Core character data
    core = {
        'look': send_cmd(s, 'look', 2),
        'score': send_cmd(s, 'score', 2),
        'inventory': send_cmd(s, 'inventory', 2),
        'eq': send_cmd(s, 'eq', 2),
        'who': send_cmd(s, 'who', 2),
        'skills': send_cmd(s, 'skills', 3),
        'spells': send_cmd(s, 'spells', 3),
        'exits': send_cmd(s, 'exits', 1),
        'title': send_cmd(s, 'title', 1),
        'alignment': send_cmd(s, 'alignment', 1),
        'money': send_cmd(s, 'money', 1),
        'time': send_cmd(s, 'time', 1),
        'hp': send_cmd(s, 'hp', 1),
        'guild': send_cmd(s, 'guild', 2),
        'clan': send_cmd(s, 'clan', 1),
        'tell history': send_cmd(s, 'tell history', 1),
    }
    
    for cmd, data in core.items():
        fname = cmd.replace(' ', '_')
        with open(f'{LOGDIR}/{fname}.txt', 'w') as f:
            f.write(data)
        print(f'{cmd}: {len(data)} chars')
    
    # Map from Central Square - try all directions and note unique rooms
    dirs = ['north', 'south', 'east', 'west', 'up', 'down', 'n', 's', 'e', 'w']
    back = {'north':'south','south':'north','east':'west','west':'east','up':'down','down':'up','n':'s','s':'n','e':'w','w':'e'}
    rooms = {}
    
    for d in dirs:
        r = send_cmd(s, d, 1.5)
        rooms[d] = r[:500]
        # return
        send_cmd(s, back.get(d, ''), 1)
    
    with open(f'{LOGDIR}/rooms_from_square.json', 'w') as f:
        json.dump(rooms, f, indent=2)
    
    # Try to find guild halls from square
    # Common IOM paths - Illium guilds are usually around the square
    guild_paths = [
        ['north', 'north'],
        ['south', 'south'],
        ['east', 'east'],
        ['west', 'west'],
        ['north', 'east'],
        ['north', 'west'],
        ['south', 'east'],
        ['south', 'west'],
        ['east', 'north'],
        ['west', 'north'],
        ['up'],
        ['down'],
        ['fountain'],
    ]
    
    guild_rooms = {}
    for path in guild_paths:
        # go out and back
        current_room = ''
        for step in path:
            r = send_cmd(s, step, 1.5)
            current_room = r[:300]
        # Record what we found
        guild_rooms['__'.join(path)] = current_room
        # Return via reverse
        for step in reversed(path):
            opp = back.get(step, '')
            if opp:
                send_cmd(s, opp, 1)
    
    with open(f'{LOGDIR}/guild_paths.json', 'w') as f:
        json.dump(guild_rooms, f, indent=2)
    
    # Commands list
    send_cmd(s, 'commands', 2)
    
    s.close()
    print(f'Done. Archive in {LOGDIR}')
    print(f'Files: {os.listdir(LOGDIR)}')

if __name__ == '__main__':
    main()
