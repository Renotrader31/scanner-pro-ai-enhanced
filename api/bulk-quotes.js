// Vercel Serverless Function - Bulk Stock Quotes
export default async function handler(req, res) {
    // Set CORS headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    
    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }
    
    const { universe = 'popular' } = req.query;
    
    // FMP API Configuration
    const FMP_API_KEY = process.env.FMP_API_KEY || 'm2XfxOS0sZxs6hLEY5yRzUgDyp5Dur4V';
    const FMP_BASE_URL = 'https://financialmodelingprep.com/api/v3';
    
    // Define stock universes (same as Python version)
    const universes = {
        'popular': [
            'AAPL', 'MSFT', 'NVDA', 'GOOGL', 'GOOG', 'AMZN', 'META', 'TSLA',
            'NFLX', 'AMD', 'CRM', 'INTC', 'ORCL', 'ADBE', 'CSCO', 'AVGO',
            'JPM', 'BAC', 'WFC', 'GS', 'MS', 'C', 'AXP', 'BLK',
            'JNJ', 'PFE', 'UNH', 'ABBV', 'MRK', 'TMO', 'ABT', 'DHR',
            'KO', 'PEP', 'WMT', 'HD', 'MCD', 'DIS', 'NKE', 'SBUX',
            'XOM', 'CVX', 'COP', 'EOG', 'SLB', 'MPC', 'VLO', 'PSX'
        ],
        'sp500_top50': [
            'AAPL', 'MSFT', 'NVDA', 'AMZN', 'GOOGL', 'GOOG', 'META', 'TSLA',
            'BRK-B', 'LLY', 'AVGO', 'JPM', 'WMT', 'V', 'UNH', 'XOM',
            'MA', 'PG', 'JNJ', 'HD', 'CVX', 'ABBV', 'NFLX', 'BAC',
            'KO', 'CRM', 'COST', 'ASML', 'MRK', 'AMD', 'PEP', 'TMO',
            'LIN', 'ACN', 'CSCO', 'ABT', 'ADBE', 'DHR', 'TXN', 'MCD',
            'VZ', 'NEE', 'ORCL', 'WFC', 'PM', 'COP', 'NVS', 'BMY',
            'DIS', 'INTC'
        ],
        'crypto_miners': [
            'MSTR', 'COIN', 'MARA', 'RIOT', 'CLSK', 'BITF', 'HUT', 'BTBT',
            'CAN', 'ARGO', 'EBON', 'SOS', 'ANY', 'EBANG', 'NCTY', 'PHUN',
            'SDIG', 'WULF', 'IREN', 'CORZ', 'CIFR', 'BTC', 'GREE', 'SPRT'
        ],
        'biotech': [
            'GILD', 'AMGN', 'BIIB', 'REGN', 'VRTX', 'ILMN', 'MRNA', 'BNTX',
            'SGEN', 'ALNY', 'BMRN', 'TECH', 'SRPT', 'RARE', 'BLUE', 'FOLD',
            'ARWR', 'EDIT', 'CRSP', 'NTLA', 'BEAM', 'PRME', 'VCYT', 'PACB'
        ],
        'energy_oil': [
            'XOM', 'CVX', 'COP', 'EOG', 'SLB', 'HAL', 'BKR', 'OXY',
            'KMI', 'WMB', 'MPC', 'VLO', 'PSX', 'HES', 'DVN', 'FANG',
            'APA', 'EQT', 'CNX', 'RRC', 'CLR', 'MRO', 'OVV', 'SM'
        ],
        'tech_pure': [
            'AAPL', 'MSFT', 'NVDA', 'GOOGL', 'META', 'TSLA', 'CRM', 'ORCL',
            'ADBE', 'NOW', 'INTU', 'AMD', 'QCOM', 'INTC', 'TXN', 'LRCX',
            'KLAC', 'AMAT', 'MU', 'NXPI', 'MRVL', 'ADI', 'SNPS', 'CDNS'
        ]
    };
    
    try {
        const tickerList = universes[universe] || universes['popular'];
        console.log(`Processing ${tickerList.length} stocks for ${universe} universe`);
        
        const quotes = [];
        const batchSize = 8; // Process 8 stocks per batch
        
        // Process in batches to avoid API limits
        for (let i = 0; i < tickerList.length; i += batchSize) {
            const batch = tickerList.slice(i, i + batchSize);
            console.log(`Processing batch ${Math.floor(i/batchSize) + 1}: ${batch.join(', ')}`);
            
            try {
                const tickerString = batch.join(',');
                const url = `${FMP_BASE_URL}/quote/${tickerString}?apikey=${FMP_API_KEY}`;
                
                const response = await fetch(url);
                const data = await response.json();
                
                if (Array.isArray(data)) {
                    for (const quote of data) {
                        quotes.push({
                            ticker: quote.symbol || '',
                            price: quote.price || 0,
                            change: quote.changesPercentage || 0,
                            change_amount: quote.change || 0,
                            volume: quote.volume || 0,
                            market_cap: quote.marketCap || 0,
                            pe: quote.pe || null,
                            day_low: quote.dayLow || 0,
                            day_high: quote.dayHigh || 0,
                            timestamp: Math.floor(Date.now() / 1000),
                            is_real_time: true,
                            universe: universe
                        });
                    }
                }
            } catch (batchError) {
                console.log(`Batch error for ${batch.join(', ')}: ${batchError.message}`);
                continue;
            }
            
            // Small delay between batches
            await new Promise(resolve => setTimeout(resolve, 200));
        }
        
        console.log(`Successfully fetched ${quotes.length} quotes from ${universe} universe`);
        
        return res.status(200).json({
            status: "success",
            universe: universe,
            count: quotes.length,
            total_requested: tickerList.length,
            quotes: quotes,
            provider: "FMP Bulk Real-time",
            fetch_time: new Date().toISOString()
        });
        
    } catch (error) {
        console.error('Bulk quotes error:', error);
        return res.status(500).json({
            status: "error",
            message: `Error in FMP bulk quotes: ${error.message}`,
            universe: universe
        });
    }
}