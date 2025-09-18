// Vercel Serverless Function - API Health Test
export default function handler(req, res) {
    // Set CORS headers for cross-origin requests
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    
    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }
    
    return res.status(200).json({
        status: "success",
        message: "FMP API Proxy is working with real-time data!",
        timestamp: new Date().toISOString(),
        api_provider: "Financial Modeling Prep (FMP)",
        environment: "Vercel Serverless",
        endpoints: [
            "/api/fmp/quote/[ticker]",
            "/api/bulk-quotes?universe=popular"
        ]
    });
}