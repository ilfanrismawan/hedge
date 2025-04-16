import ccxt

def get_exchanges():
    binance_spot = ccxt.binance(
    #     {
    #     'apiKey': 'YOUR_SPOT_API_KEY',
    #     'secret': 'YOUR_SPOT_SECRET_KEY',
    #     'enableRateLimit': True,
    # }
    )

    binance_futures = ccxt.binance(
    #     {

    #     'apiKey': 'YOUR_FUTURES_API_KEY',
    #     'secret': 'YOUR_FUTURES_SECRET_KEY',
    #     'enableRateLimit': True,
    #     'options': {'defaultType': 'future'}
    # }

   
    )

    indodax = ccxt.indodax()
    kraken = ccxt.kraken()
    coinbase = ccxt.coinbase()
    return binance_spot, binance_futures