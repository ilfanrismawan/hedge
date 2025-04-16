import ccxt

# Inisialisasi exchange
exchange = ccxt.indodax()

# Load markets
markets = exchange.load_markets()

# Tampilkan semua symbol (pair)
for symbol in markets:
    print(symbol)