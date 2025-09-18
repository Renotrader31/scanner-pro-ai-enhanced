#!/usr/bin/env python3
"""
Scanner Pro AI - HTTP Server
Serves the advanced trading platform with live data capabilities
"""

import http.server
import socketserver
import os
import sys
import mimetypes
from pathlib import Path

class ScannerHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="/home/user/webapp", **kwargs)
    
    def end_headers(self):
        # Add CORS headers for API access
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()
    
    def log_message(self, format, *args):
        """Enhanced logging for the scanner"""
        timestamp = self.log_date_time_string()
        message = f"[{timestamp}] {format % args}"
        print(message)
        sys.stdout.flush()

def main():
    PORT = 8000
    
    print("🚀 Scanner Pro AI - Starting HTTP Server...")
    print(f"📡 Server: http://0.0.0.0:{PORT}")
    print(f"📁 Directory: /home/user/webapp")
    print(f"🔍 Mass Scanner: Ready for 4,500+ stocks")
    print(f"🧠 AI Analysis: Natural language queries supported")
    print(f"📊 Live Data: Polygon API integration ready")
    print("=" * 60)
    
    try:
        with socketserver.TCPServer(("0.0.0.0", PORT), ScannerHandler) as httpd:
            print(f"✅ Scanner Pro AI serving at port {PORT}")
            sys.stdout.flush()
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Scanner server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()