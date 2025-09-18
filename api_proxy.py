#!/usr/bin/env python3
"""
Scanner Pro AI - API Proxy Server
Handles CORS and proxies requests to FMP (Financial Modeling Prep) for real-time data
"""

import http.server
import socketserver
import urllib.request
import urllib.parse
import json
import sys
import time
from urllib.error import HTTPError, URLError

class APIProxyHandler(http.server.BaseHTTPRequestHandler):
    
    # API Configuration - Using FMP for real-time live data
    FMP_API_KEY = 'm2XfxOS0sZxs6hLEY5yRzUgDyp5Dur4V'
    FMP_BASE_URL = 'https://financialmodelingprep.com/api/v3'
    
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
        """Handle GET requests and proxy to FMP API for real-time data"""
        try:
            parsed_path = urllib.parse.urlparse(self.path)
            path = parsed_path.path
            query_params = urllib.parse.parse_qs(parsed_path.query)
            
            print(f"📡 Proxy request: {path}")
            
            if path == '/api/test':
                self._handle_test_request()
            elif path == '/api/fmp/quote':
                ticker = query_params.get('ticker', ['AAPL'])[0]
                self._handle_fmp_quote(ticker)
            elif path.startswith('/api/fmp/quote/'):
                ticker = path.split('/')[-1]
                self._handle_fmp_quote(ticker)
            elif path == '/api/fmp/batch-quotes':
                tickers = query_params.get('tickers', ['AAPL,MSFT,NVDA,GOOGL,TSLA'])[0].split(',')
                self._handle_fmp_batch_quotes(tickers)
            elif path == '/api/fmp/realtime-quotes':
                tickers = query_params.get('tickers', ['AAPL,MSFT,NVDA,GOOGL,TSLA'])[0].split(',')
                self._handle_fmp_realtime_quotes(tickers)
            else:
                self._send_error_response(404, "Endpoint not found")
                
        except Exception as e:
            print(f"❌ Proxy error: {e}")
            self._send_error_response(500, f"Internal server error: {str(e)}")
    
    def _handle_test_request(self):
        """Handle test endpoint"""
        response_data = {
            "status": "success",
            "message": "FMP API Proxy is working with real-time data!",
            "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            "api_provider": "Financial Modeling Prep (FMP)",
            "endpoints": [
                "/api/fmp/quote/{ticker}",
                "/api/fmp/batch-quotes?tickers=AAPL,MSFT,...",
                "/api/fmp/realtime-quotes?tickers=AAPL,MSFT,..."
            ]
        }
        self._send_json_response(response_data)
    
    def _handle_fmp_quote(self, ticker):
        """Fetch single stock quote from FMP API (real-time)"""
        try:
            print(f"🔄 Fetching real-time quote for {ticker} from FMP...")
            
            # FMP real-time quote endpoint
            url = f"{self.FMP_BASE_URL}/quote/{ticker.upper()}?apikey={self.FMP_API_KEY}"
            
            with urllib.request.urlopen(url, timeout=10) as response:
                data = json.loads(response.read().decode())
            
            if data and len(data) > 0:
                quote = data[0]  # FMP returns array with single object
                
                # Extract real-time data
                quote_data = {
                    "ticker": quote.get('symbol', ticker.upper()),
                    "price": quote.get('price', 0),
                    "change": quote.get('changesPercentage', 0),
                    "change_amount": quote.get('change', 0),
                    "volume": quote.get('volume', 0),
                    "market_cap": quote.get('marketCap', 0),
                    "pe": quote.get('pe', None),
                    "day_low": quote.get('dayLow', 0),
                    "day_high": quote.get('dayHigh', 0),
                    "year_low": quote.get('yearLow', 0),
                    "year_high": quote.get('yearHigh', 0),
                    "timestamp": int(time.time()),
                    "exchange": quote.get('exchange', 'NASDAQ'),
                    "is_real_time": True
                }
                
                response_data = {
                    "status": "success",
                    "quote": quote_data
                }
                print(f"✅ Real-time quote: {ticker} = ${quote_data['price']} ({quote_data['change']:+.2f}%)")
                
            else:
                response_data = {
                    "status": "error",
                    "message": f"No real-time data found for {ticker}"
                }
                
            self._send_json_response(response_data)
            
        except HTTPError as e:
            self._send_error_response(e.code, f"FMP API error: {e.reason}")
        except Exception as e:
            self._send_error_response(500, f"Error fetching real-time quote for {ticker}: {str(e)}")
    
    def _handle_fmp_batch_quotes(self, tickers):
        """Fetch multiple stock quotes from FMP (real-time batch)"""
        try:
            print(f"🔄 Fetching real-time batch quotes for: {', '.join(tickers)}")
            
            # FMP batch quote endpoint - can handle multiple tickers at once
            ticker_string = ','.join([t.upper().strip() for t in tickers[:20]])  # Limit to 20 tickers
            url = f"{self.FMP_BASE_URL}/quote/{ticker_string}?apikey={self.FMP_API_KEY}"
            
            with urllib.request.urlopen(url, timeout=15) as response:
                data = json.loads(response.read().decode())
            
            quotes = []
            if data and isinstance(data, list):
                for quote in data:
                    quotes.append({
                        "ticker": quote.get('symbol', ''),
                        "price": quote.get('price', 0),
                        "change": quote.get('changesPercentage', 0),
                        "change_amount": quote.get('change', 0),
                        "volume": quote.get('volume', 0),
                        "market_cap": quote.get('marketCap', 0),
                        "timestamp": int(time.time()),
                        "is_real_time": True
                    })
            
            print(f"✅ Fetched {len(quotes)} real-time quotes from FMP")
            for quote in quotes:
                print(f"   📈 {quote['ticker']}: ${quote['price']:.2f} ({quote['change']:+.2f}%)")
            
            response_data = {
                "status": "success",
                "count": len(quotes),
                "quotes": quotes,
                "provider": "FMP Real-time"
            }
            self._send_json_response(response_data)
            
        except HTTPError as e:
            self._send_error_response(e.code, f"FMP API error: {e.reason}")
        except Exception as e:
            self._send_error_response(500, f"Error in FMP batch quotes: {str(e)}")
    
    def _handle_fmp_realtime_quotes(self, tickers):
        """Fetch real-time quotes using FMP's most current endpoint"""
        try:
            print(f"🚀 Fetching REAL-TIME quotes for: {', '.join(tickers)}")
            
            quotes = []
            
            # Use FMP's real-time quote endpoint for maximum freshness
            for ticker in tickers[:10]:  # Process up to 10 tickers
                try:
                    ticker = ticker.upper().strip()
                    url = f"{self.FMP_BASE_URL}/quote-short/{ticker}?apikey={self.FMP_API_KEY}"
                    
                    with urllib.request.urlopen(url, timeout=5) as response:
                        data = json.loads(response.read().decode())
                    
                    if data and len(data) > 0:
                        quote = data[0]
                        
                        # Get detailed quote for more info
                        detail_url = f"{self.FMP_BASE_URL}/quote/{ticker}?apikey={self.FMP_API_KEY}"
                        with urllib.request.urlopen(detail_url, timeout=5) as detail_response:
                            detail_data = json.loads(detail_response.read().decode())
                        
                        if detail_data and len(detail_data) > 0:
                            detail = detail_data[0]
                            
                            quotes.append({
                                "ticker": ticker,
                                "price": quote.get('price', detail.get('price', 0)),
                                "change": detail.get('changesPercentage', 0),
                                "change_amount": detail.get('change', 0),
                                "volume": quote.get('volume', detail.get('volume', 0)),
                                "timestamp": int(time.time()),
                                "is_real_time": True,
                                "source": "FMP Real-time API"
                            })
                            
                            print(f"   ⚡ {ticker}: ${quote.get('price', 0):.2f} (REAL-TIME)")
                
                except Exception as ticker_error:
                    print(f"⚠️ Error fetching real-time data for {ticker}: {ticker_error}")
                    continue
            
            response_data = {
                "status": "success",
                "count": len(quotes),
                "quotes": quotes,
                "provider": "FMP Real-time",
                "fetch_time": time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())
            }
            self._send_json_response(response_data)
            
        except Exception as e:
            self._send_error_response(500, f"Error in FMP real-time quotes: {str(e)}")
    
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
    
    print("🚀 Scanner Pro AI - FMP Real-Time API Proxy Server")
    print(f"📡 Proxy Server: http://0.0.0.0:{PORT}")
    print(f"🔑 FMP API: Ready (Real-time data)")
    print(f"💰 API Provider: Financial Modeling Prep")
    print("🌐 CORS: Enabled")
    print("⚡ Real-time quotes: ENABLED")
    print("=" * 60)
    
    try:
        with socketserver.TCPServer(("0.0.0.0", PORT), APIProxyHandler) as httpd:
            print(f"✅ FMP API Proxy serving at port {PORT}")
            print("📋 Available endpoints:")
            print("   GET /api/test - Test endpoint")
            print("   GET /api/fmp/quote/{ticker} - Get real-time quote")
            print("   GET /api/fmp/batch-quotes?tickers=A,B,C - Get batch quotes")
            print("   GET /api/fmp/realtime-quotes?tickers=A,B,C - Get real-time quotes")
            print("🎯 Ready for LIVE market data!")
            sys.stdout.flush()
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 FMP API Proxy stopped by user")
    except Exception as e:
        print(f"❌ Proxy server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()