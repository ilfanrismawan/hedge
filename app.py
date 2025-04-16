import streamlit as st
import ccxt

st.title("📊 Crypto Arbitrage Opportunity Finder")
st.markdown("Pantau perbedaan harga **BTC/USDT** di berbagai exchange dan temukan peluang arbitrase.")

exchange_ids = ['binance', 'indodax', 'kraken', 'coinbasepro', 'indodax']
symbol = 'BTC/USDT'
prices = {}

with st.spinner("Mengambil data harga dari exchange..."):
    for exchange_id in exchange_ids:
        try:
            exchange_class = getattr(ccxt, exchange_id)
            exchange = exchange_class()
            exchange.load_markets()  # <- INI WAJIB UNTUK BINANCE, INDODAX, DLL
            ticker = exchange.fetch_ticker(symbol)
            price = ticker['last']
            prices[exchange_id] = price
        except Exception as e:
            prices[exchange_id] = None
            st.warning(f"Gagal fetch data dari {exchange_id.upper()}: {str(e)}")

st.subheader("💰 Harga BTC Saat Ini:")
price_cols = st.columns(len(exchange_ids))
for i, exchange in enumerate(exchange_ids):
    price = prices.get(exchange)
    if price:
        price_cols[i].metric(label=exchange.upper(), value=f"${price:,.2f}")
    else:
        price_cols[i].write(f"{exchange.upper()}: ❌")

valid_prices = {k: v for k, v in prices.items() if v is not None}
if valid_prices:
    max_exchange = max(valid_prices, key=valid_prices.get)
    min_exchange = min(valid_prices, key=valid_prices.get)
    spread = valid_prices[max_exchange] - valid_prices[min_exchange]

    st.subheader("🚀 Peluang Arbitrase:")
    st.success(f"""
    Beli di **{min_exchange.upper()}** @ `${valid_prices[min_exchange]:.2f}`  
    Jual di **{max_exchange.upper()}** @ `${valid_prices[max_exchange]:.2f}`  
    🔁 **Spread**: `${spread:.2f}`
    """)
else:
    st.error("Tidak cukup data harga untuk menganalisis peluang arbitrase.")

st.caption("Data diperoleh secara real-time dari API exchange menggunakan CCXT.")
