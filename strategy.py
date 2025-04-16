def get_prices(spot, futures, symbol='BTC/USDT'):
    spot_price = spot.fetch_ticker(symbol)['last']
    futures_price = futures.fetch_ticker(symbol)['last']
    spread = futures_price - spot_price
    spread_pct = (spread / spot_price) * 100
    return {
        'spot': spot_price,
        'futures': futures_price,
        'spread': spread,
        'spread_pct': spread_pct
    }

def is_profitable(spread_pct, threshold=1.0):
    return spread_pct >= threshold