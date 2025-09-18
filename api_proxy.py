#!/usr/bin/env python3
"""
Scanner Pro AI - API Proxy Server
Handles CORS and proxies requests to financial APIs
"""

import http.server
import socketserver
import urllib.request
import urllib.parse
import json
import sys
from urllib.error import HTTPError, URLError

class APIProxyHandler(http.server.BaseHTTPRequestHandler):
    
    # API Configuration
    POLYGON_API_KEY = '75rlu6cWGNnIqqR_x8M384YUjBgGk6kT'
    FMP_API_KEY = 'm2XfxOS0sZxs6hLEY5yRzUgDyp5Dur4V'
    
    def _send_cors_headers(self):
        """Send CORS headers for cross-origin requests"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-Type', 'application/json')
    
    def do_OPTIONS(self):
        """Handle preflight OPTIONS requests"""
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests and proxy to appropriate APIs"""
        try:
            parsed_path = urllib.parse.urlparse(self.path)
            path = parsed_path.path
            query_params = urllib.parse.parse_qs(parsed_path.query)
            
            print(f"📡 Proxy request: {path}")
            
            if path == '/api/test':
                self._handle_test_request()
            elif path == '/api/polygon/tickers':
                self._handle_polygon_tickers()
            elif path.startswith('/api/polygon/quote/'):
                ticker = path.split('/')[-1]
                self._handle_polygon_quote(ticker)
            elif path == '/api/polygon/batch-quotes':
                tickers = query_params.get('tickers', ['AAPL,MSFT,NVDA,GOOGL,TSLA'])[0].split(',')
                self._handle_polygon_batch_quotes(tickers)
            else:
                self._send_error_response(404, "Endpoint not found")
                
        except Exception as e:
            print(f"❌ Proxy error: {e}")
            self._send_error_response(500, f"Internal server error: {str(e)}")
    
    def _handle_test_request(self):
        """Handle test endpoint"""
        response_data = {
            "status": "success",
            "message": "API Proxy is working!",
            "timestamp": "2024-01-15T10:30:00Z",
            "endpoints": [
                "/api/polygon/tickers",
                "/api/polygon/quote/{ticker}",
                "/api/polygon/batch-quotes?tickers=AAPL,MSFT,..."
            ]
        }
        self._send_json_response(response_data)
    
    def _handle_polygon_tickers(self):
        """Fetch ticker list from Polygon API"""
        try:
            url = f"https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&limit=100&apikey={self.POLYGON_API_KEY}"
            
            with urllib.request.urlopen(url, timeout=10) as response:
                data = json.loads(response.read().decode())
                
            # Transform the data for frontend
            tickers = []
            if 'results' in data:
                for ticker_data in data['results'][:50]:  # Limit to 50 for demo
                    tickers.append({
                        'ticker': ticker_data.get('ticker', ''),
                        'name': ticker_data.get('name', ''),
                        'market': ticker_data.get('market', 'stocks'),
                        'primary_exchange': ticker_data.get('primary_exchange', '')
                    })
            
            response_data = {
                "status": "success",
                "count": len(tickers),
                "tickers": tickers
            }
            self._send_json_response(response_data)
            
        except HTTPError as e:
            self._send_error_response(e.code, f"Polygon API error: {e.reason}")
        except Exception as e:
            self._send_error_response(500, f"Error fetching tickers: {str(e)}")
    
    def _handle_polygon_quote(self, ticker):
        """Fetch single stock quote from Polygon API"""
        try:
            url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/prev?adjusted=true&apikey={self.POLYGON_API_KEY}"
            
            with urllib.request.urlopen(url, timeout=10) as response:
                data = json.loads(response.read().decode())
            
            if 'results' in data and len(data['results']) > 0:
                result = data['results'][0]
                
                # Calculate percentage change
                change_pct = ((result['c'] - result['o']) / result['o'] * 100) if result['o'] != 0 else 0
                
                quote_data = {
                    "ticker": ticker.upper(),
                    "price": result['c'],
                    "open": result['o'],
                    "high": result['h'],
                    "low": result['l'],
                    "volume": result['v'],
                    "change": round(change_pct, 2),
                    "timestamp": result.get('t', 0)
                }
                
                response_data = {
                    "status": "success",
                    "quote": quote_data
                }
            else:
                response_data = {
                    "status": "error",
                    "message": f"No data found for {ticker}"
                }
                
            self._send_json_response(response_data)
            
        except HTTPError as e:
            self._send_error_response(e.code, f"Polygon API error: {e.reason}")
        except Exception as e:
            self._send_error_response(500, f"Error fetching quote for {ticker}: {str(e)}")
    
    def _handle_polygon_batch_quotes(self, tickers):
        """Fetch multiple stock quotes"""
        try:
            quotes = []
            
            for ticker in tickers[:10]:  # Limit to 10 tickers to avoid rate limits
                try:
                    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/prev?adjusted=true&apikey={self.POLYGON_API_KEY}"
                    
                    with urllib.request.urlopen(url, timeout=5) as response:
                        data = json.loads(response.read().decode())
                    
                    if 'results' in data and len(data['results']) > 0:
                        result = data['results'][0]
                        change_pct = ((result['c'] - result['o']) / result['o'] * 100) if result['o'] != 0 else 0
                        
                        quotes.append({
                            "ticker": ticker.upper(),
                            "price": result['c'],
                            "change": round(change_pct, 2),
                            "volume": result['v'],
                            "timestamp": result.get('t', 0)
                        })
                
                except Exception as ticker_error:
                    print(f"⚠️ Error fetching {ticker}: {ticker_error}")
                    continue
            
            response_data = {
                "status": "success",
                "count": len(quotes),
                "quotes": quotes
            }
            self._send_json_response(response_data)
            
        except Exception as e:
            self._send_error_response(500, f"Error in batch quotes: {str(e)}")
    
    def _send_json_response(self, data):
        """Send JSON response with proper headers"""
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()
        
        json_data = json.dumps(data, indent=2)
        self.wfile.write(json_data.encode())
        
        print(f"✅ Response sent: {len(json_data)} bytes")
    
    def _send_error_response(self, status_code, message):
        """Send error response"""
        self.send_response(status_code)
        self._send_cors_headers()
        self.end_headers()
        
        error_data = {
            "status": "error",
            "message": message,
            "code": status_code
        }
        
        json_data = json.dumps(error_data, indent=2)
        self.wfile.write(json_data.encode())
        
        print(f"❌ Error response: {status_code} - {message}")
    
    def log_message(self, format, *args):
        """Custom logging"""
        timestamp = self.log_date_time_string()
        message = f"[{timestamp}] {format % args}"
        print(message)
        sys.stdout.flush()

def main():
    PORT = 8001
    
    print("🚀 Scanner Pro AI - API Proxy Server")
    print(f"📡 Proxy Server: http://0.0.0.0:{PORT}")
    print(f"🔑 Polygon API: Ready")
    print(f"🔑 FMP API: Ready")
    print("🌐 CORS: Enabled")
    print("=" * 50)
    
    try:
        with socketserver.TCPServer(("0.0.0.0", PORT), APIProxyHandler) as httpd:
            print(f"✅ API Proxy serving at port {PORT}")
            print("📋 Available endpoints:")
            print("   GET /api/test - Test endpoint")
            print("   GET /api/polygon/tickers - Get ticker list")
            print("   GET /api/polygon/quote/{ticker} - Get single quote")
            print("   GET /api/polygon/batch-quotes?tickers=A,B,C - Get batch quotes")
            sys.stdout.flush()
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 API Proxy stopped by user")
    except Exception as e:
        print(f"❌ Proxy server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()