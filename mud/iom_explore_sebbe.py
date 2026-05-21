#!/usr/bin/env python3
"""IOM explorer - connects as sebbe and archives everything"""
import socket, time, re, sys, json, os

HOST = 'islandsofmyth.org'
PORT = 3000
LOGDIR = '/root/.openclaw/workspace/mud/iom_sebbe_explore'
os.makedirs(LOGDIR, exist_ok=True)

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    s.connect((HOST, PORT))
    return s

def send_recv(s, cmd, wait=2):
    if cmd:
        s.send((cmd + '\n').encode())
    time.sleep(wait)
    try:
        data = b''
        while True:
            chunk = s.recv(8192)
            if not chunk:
                break
            data += chunk
            time.sleep(0.3)
            # try once more
            try:
                chunk2 = s.recv(8192)
                if chunk2:
                    data += chunk2
            except:
                break
        return data.decode('utf-8', errors='replace')
    except socket.timeout:
        return ''
    except Exception as e:
        return f'ERROR: {e}'

def strip_ansi(text):
    ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
    return ansi_escape.sub('', text)

def main():
    s = connect()
    # login sequence
    time.sleep(1)
    r = send_recv(s, 'sebbe', 1)
    print('USERNAME SCREEN CAPTURED')
    r = send_recv(s, 'creative', 2)
    print('LOGGED IN')
    
    # Save login screen
    with open(f'{LOGDIR}/00_login.txt', 'w') as f:
        f.write(strip_ansi(r))
    
    commands = [
        ('look', '01_room_start'),
        ('exits', '02_exits'),
        ('inventory', '03_inventory'),
        ('score', '04_score'),
        ('who', '05_who'),
        ('skills', '06_skills'),
        ('spells', '07_spells'),
        ('hp', '08_hp'),
        ('eq', '09_equipment'),
        ('i', '10_i'),
        ('help', '11_help'),
        ('commands', '12_commands'),
        ('mail', '13_mail'),
        ('news', '14_news'),
        ('board', '15_board'),
        ('map', '16_map'),
        ('recall', '17_recall'),
        ('say Hello from the archivist', '18_say'),
        ('tell nailman Hello, just exploring', '19_tell_nailman'),
        ('clan', '20_clan'),
        ('guild', '21_guild'),
        ('title', '22_title'),
        ('alignment', '23_alignment'),
        ('money', '24_money'),
        ('time', '25_time'),
        ('weather', '26_weather'),
    ]
    
    results = {}
    for cmd, fname in commands:
        print(f'Running: {cmd}')
        r = send_recv(s, cmd, 2)
        clean = strip_ansi(r)
        with open(f'{LOGDIR}/{fname}.txt', 'w') as f:
            f.write(clean)
        results[cmd] = clean[:500]  # preview
        print(f'  -> {len(clean)} chars')
    
    # Movement exploration - try to map from start room
    directions = ['north', 'south', 'east', 'west', 'up', 'down',
                  'n', 's', 'e', 'w', 'u', 'd',
                  'enter', 'out', 'portal']
    
    # First, get current room
    r = send_recv(s, 'look', 2)
    start_room = strip_ansi(r)
    with open(f'{LOGDIR}/00_start_room.txt', 'w') as f:
        f.write(start_room)
    
    # Try each direction and return
    for d in directions:
        print(f'Moving: {d}')
        r = send_recv(s, d, 2)
        clean = strip_ansi(r)
        with open(f'{LOGDIR}/dir_{d}.txt', 'w') as f:
            f.write(clean)
        # Try to return
        opp = {'north':'south','south':'north','east':'west','west':'east',
               'up':'down','down':'up','n':'s','s':'n','e':'w','w':'e',
               'u':'d','d':'u'}.get(d, 'out' if d=='enter' else 'enter')
        send_recv(s, opp, 1)
    
    s.close()
    print(f'Done. All files in {LOGDIR}')
    # Save summary
    with open(f'{LOGDIR}/summary.json', 'w') as f:
        json.dump({k: v[:300] for k,v in results.items()}, f, indent=2)

if __name__ == '__main__':
    main()
