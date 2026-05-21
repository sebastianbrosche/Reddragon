#!/usr/bin/env python3
"""Quick OAuth callback catcher. Run this, then click the link."""
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import sys

AUTH_CODE = None

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global AUTH_CODE
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        
        if 'code' in params:
            AUTH_CODE = params['code'][0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"<h1>Done!</h1><p>You can close this tab. Miha has the code.</p>")
            print(f"\n🎉 AUTH CODE RECEIVED: {AUTH_CODE[:20]}...")
            print("Copy this code and paste it back to Miha if needed.")
        elif 'error' in params:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(f"<h1>Error: {params['error'][0]}</h1>".encode())
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"<h1>Waiting for auth...</h1>")
    
    def log_message(self, format, *args):
        pass  # Quiet

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    server = HTTPServer(('0.0.0.0', port), Handler)
    print(f"Listening on port {port}...")
    print("Click the Google link now. This will auto-capture the code.")
    server.handle_request()  # One request then exit
    if AUTH_CODE:
        print(f"\nSUCCESS! Code: {AUTH_CODE}")
    else:
        print("\nNo code received.")
