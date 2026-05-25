import socket, time, sys, re

def strip_ansi(text):
    """Remove ANSI escape codes"""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def read_until_prompt(sock, timeout=5):
    """Read data until we get something useful or timeout"""
    sock.settimeout(timeout)
    buffer = b''
    start = time.time()
    while time.time() - start < timeout:
        try:
            chunk = sock.recv(4096)
            if chunk:
                buffer += chunk
                text = strip_ansi(buffer.decode('utf-8', errors='replace'))
                # Look for meaningful content
                if any(marker in text for marker in ["MUD", "RAGON", "player", "create", "connect", "Welcome"]):
                    return text
        except socket.timeout:
            break
    # Return whatever we got
    return strip_ansi(buffer.decode('utf-8', errors='replace'))

def test_login_flow():
    """Test full user login flow on localhost:3000"""
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 3000))
    
    # 1. Read connection screen (handle telnet negotiation)
    screen = read_until_prompt(s, timeout=3)
    assert len(screen) > 50, f"Connection screen too short: {repr(screen[:100])}"
    assert any(x in screen for x in ["MUD", "RAGON", "Welcome", "create", "connect"]), f"No MUD content in screen: {repr(screen[:200])}"
    print("✓ Connection screen received")
    
    # 2. Create account
    s.send(b'create testflow2 abc123\r\n')
    create_response = read_until_prompt(s, timeout=3)
    assert "intended" in create_response.lower() or "create" in create_response.lower(), f"No create prompt. Got: {repr(create_response[:300])}"
    print("✓ Create account prompt received")
    
    # 3. Confirm
    s.send(b'Y\r\n')
    confirm_response = read_until_prompt(s, timeout=3)
    assert "created" in confirm_response.lower(), f"Account not created. Got: {repr(confirm_response[:300])}"
    print("✓ Account created")
    
    # 4. Connect
    s.send(b'connect testflow2 abc123\r\n')
    connect_response = read_until_prompt(s, timeout=3)
    
    # 5. Check for success indicators
    success_markers = ["testflow2", "Level", "HP", "Limbo", "become", "character"]
    found = any(m.lower() in connect_response.lower() for m in success_markers)
    
    if found:
        print("✓ Login SUCCESS - Character active")
        print(f"Response preview: {connect_response[:300]}")
        s.close()
        return True
    else:
        print(f"✗ Login FAILED. Response: {repr(connect_response[:500])}")
        s.close()
        return False

if __name__ == "__main__":
    try:
        result = test_login_flow()
        sys.exit(0 if result else 1)
    except Exception as e:
        print(f"✗ TEST EXCEPTION: {e}")
        sys.exit(1)
