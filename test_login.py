import socket, time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 3000))
s.settimeout(5)

# Skip connect screen
s.recv(4096)
time.sleep(0.5)

# Create
s.send(b'create testplayer6 abc123\r\n')
time.sleep(1)
data = s.recv(4096)
print('=== CREATE ===')
print(data.decode('utf-8', errors='replace'))

# Confirm
s.send(b'Y\r\n')
time.sleep(1)
data = s.recv(4096)
print('=== AFTER Y ===')
print(data.decode('utf-8', errors='replace'))

# Connect
s.send(b'connect testplayer6 abc123\r\n')
time.sleep(1)
data = s.recv(4096)
print('=== CONNECT ===')
print(data.decode('utf-8', errors='replace'))

# Get follow-up
time.sleep(1)
try:
    data = s.recv(4096)
    print('=== FOLLOWUP ===')
    print(data.decode('utf-8', errors='replace'))
except:
    pass

s.close()
