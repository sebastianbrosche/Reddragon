#!/usr/bin/env python3
"""Focused Illium city explorer for IOM - captures rooms, objects, NPCs, exits"""
import socket, time, re, os, json

HOST, PORT = 'islandsofmyth.org', 3000
LOGDIR = '/root/.openclaw/workspace/mud/iom_illium_city'
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
    
    archive = {'rooms': {}, 'objects': {}, 'npcs': {}, 'exits': {}}
    
    # Start room - Central Square
    start = send_cmd(s, 'look', 2)
    archive['rooms']['central_square'] = start
    
    # Try 'look at' everything in the room
    # Parse objects from room description
    lines = start.split('\n')
    objects_found = []
    for line in lines:
        # Look for lines like "A large fountain sits..." or "You notice..."
        if any(x in line.lower() for x in ['fountain', 'machine', 'vine', 'potion', 'pyroclast']):
            # Extract object name - simplistic
            words = line.strip().split()
            for i, w in enumerate(words):
                if w.lower() in ['fountain', 'machine', 'vine', 'potion', 'pyroclast', 'shield']:
                    obj_name = ' '.join(words[max(0,i-2):i+1]).lower().replace('a ', '').replace('an ', '').replace('the ', '').replace('2 ', '').replace('3 ', '')
                    objects_found.append(obj_name)
    
    # Also try 'look at' common things
    things_to_look = ['fountain', 'machine', 'moonflower', 'vine', 'potion', 'pyroclast', 'shield', 'sign', 'board', 'window', 'river', 'tree', 'water', 'pools']
    for thing in things_to_look:
        r = send_cmd(s, f'look at {thing}', 1.5)
        if len(r) > 50 and 'cannot see' not in r.lower() and 'do not see' not in r.lower():
            archive['objects'][thing] = r
            print(f'Object: {thing} - {len(r)} chars')
    
    # Check exits
    exits = send_cmd(s, 'exits', 1)
    archive['exits']['central_square'] = exits
    
    # Movement from Central Square - document each direction
    directions = ['north', 'south', 'east', 'west', 'up', 'down']
    back = {'north':'south','south':'north','east':'west','west':'east','up':'down','down':'up'}
    
    for d in directions:
        print(f'Going {d}...')
        r = send_cmd(s, d, 2)
        archive['rooms'][f'central_square_{d}'] = r
        
        # Look at this room in detail
        look_r = send_cmd(s, 'look', 2)
        archive['rooms'][f'central_square_{d}_look'] = look_r
        
        # Look at objects here too
        for thing in things_to_look:
            r2 = send_cmd(s, f'look at {thing}', 1)
            if len(r2) > 50 and 'cannot see' not in r2.lower():
                archive['objects'][f'{d}_{thing}'] = r2
        
        # Go back
        send_cmd(s, back[d], 2)
        # Verify we're back
        back_look = send_cmd(s, 'look', 1)
        if 'Central Square' not in back_look:
            print(f'WARNING: Not back in Central Square after {d}!')
    
    # Try 'fountain' as an exit or action
    r = send_cmd(s, 'fountain', 2)
    archive['rooms']['fountain_action'] = r
    if 'Central Square' not in r:
        send_cmd(s, 'out', 2)
        send_cmd(s, 'look', 1)
    
    # Save everything
    with open(f'{LOGDIR}/illium_archive.json', 'w') as f:
        json.dump(archive, f, indent=2, default=str)
    
    # Also save as readable text
    with open(f'{LOGDIR}/illium_rooms.txt', 'w') as f:
        for name, content in archive['rooms'].items():
            f.write(f'\n=== {name.upper()} ===\n')
            f.write(content)
            f.write('\n\n')
    
    with open(f'{LOGDIR}/illium_objects.txt', 'w') as f:
        for name, content in archive['objects'].items():
            f.write(f'\n=== {name.upper()} ===\n')
            f.write(content)
            f.write('\n\n')
    
    s.close()
    print(f'Illium archive complete: {LOGDIR}')
    print(f'Rooms: {len(archive["rooms"])}')
    print(f'Objects: {len(archive["objects"])}')

if __name__ == '__main__':
    main()
