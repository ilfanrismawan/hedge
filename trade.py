def execute_cash_and_carry(spot, futures, symbol='BTC/USDT', amount=0.001):
    # Long spot
    spot_order = spot.create_market_buy_order(symbol, amount)
    
    # Short futures
    futures_order = futures.create_market_sell_order(symbol, amount)

    return spot_order, futures_order