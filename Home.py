import streamlit as st
import ccxt.async_support as ccxt
import asyncio
import time
st.set_page_config(page_title="Crypto Arbitrage Bot", layout="centered")


# === Konfigurasi Manajemen Risiko ===
MAX_RISK_PER_TRADE_USD = 500
MIN_SPREAD_USD = 20
STOP_LOSS_PERCENT = 1.5
TAKE_PROFIT_PERCENT = 2.0
symbol = 'BTC/USDT'

exchange_ids = ['binance', 'kraken', 'coinbase', 'bitfinex', 'indodax']

# Daftar pair yang bisa dipilih
available_pairs = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'ADA/USDT', 'XRP/USDT', 'LTC/USDT','DOGE/USDT','SOL/USDT','BTC/EUR', 'ETH/BTC']

# === Fetch harga dari exchange ===
async def fetch_price(exchange_id, symbol):
    try:
        exchange_class = getattr(ccxt, exchange_id)
        exchange = exchange_class()
        await exchange.load_markets()
        if symbol in exchange.symbols:
            ticker = await exchange.fetch_ticker(symbol)
            price = ticker['last']
        else:
            price = None
        await exchange.close()
        # st.warning(f"{exchange_id.upper()} tidak mendukung pasangan {symbol}")
        return exchange_id, price
    except Exception as e:
            # st.warning(f"Gagal ambil data dari {exchange_id.upper()}: {str(e)}")
            return exchange_id, None

async def fetch_all_prices(symbol):
    tasks = [fetch_price(eid, symbol) for eid in exchange_ids]
    results = await asyncio.gather(*tasks)
    return dict(results)
  
# === Analisis Spread ===
def analyze_spread(prices):
    clean_prices = {k: v for k, v in prices.items() if v is not None}
    if not clean_prices:
        return None

    max_exchange = max(clean_prices, key=clean_prices.get)
    min_exchange = min(clean_prices, key=clean_prices.get)
    spread = clean_prices[max_exchange] - clean_prices[min_exchange]

    return {
        "max_exchange": max_exchange,
        "min_exchange": min_exchange,
        "spread": spread,
        "max_price": clean_prices[max_exchange],
        "min_price": clean_prices[min_exchange],
    }

# === Streamlit UI ===


# Pilihan pair dari user
symbol = st.selectbox("🪙 Pilih Pair Crypto:", available_pairs)

st.title("📊 Market Neutral Crypto Arbitrage Bot")
st.write(f"Strategi arbitrase {symbol} antar beberapa exchange menggunakan manajemen risiko.")

# === Ambil harga dengan async ===
with st.spinner("Mengambil data harga dari exchange..."):
    prices = asyncio.run(fetch_all_prices(symbol))

# === Tampilkan harga ===
st.subheader(f"💰 Harga {symbol.split("/")[0]} Saat Ini:")
price_cols = st.columns(len(exchange_ids))
for i, exchange in enumerate(exchange_ids):
    price = prices.get(exchange)
    if price:
        price_cols[i].metric(label=exchange.upper(), value=f"${price:,.2f}")
    else:
        price_cols[i].write(f"{exchange.upper()}: ⚠️")


# === Analisis arbitrase ===
strategy = analyze_spread(prices)

if strategy:
    st.subheader("📈 Analisis Spread & Peluang Arbitrase")
    st.write(f"**Beli {symbol.lower().split("/")[0]} di:** `{strategy['min_exchange'].upper()}` @ `${strategy['min_price']:.2f}`")
    st.write(f"**Jual {symbol.lower().split("/")[0]} di:** `{strategy['max_exchange'].upper()}` @ `${strategy['max_price']:.2f}`")
    st.write(f"**🔁 Spread:** `${strategy['spread']:.2f}`")

    if strategy['spread'] >= MIN_SPREAD_USD:
        st.success("💡 Peluang arbitrase terdeteksi! Spread melebihi threshold minimum.")
        # Hitung ukuran trade
        trade_size = MAX_RISK_PER_TRADE_USD / strategy['min_price']
        stop_loss = strategy['min_price'] * (1 - STOP_LOSS_PERCENT / 100)
        take_profit = strategy['max_price'] * (1 + TAKE_PROFIT_PERCENT / 100)

        st.markdown(f"""
        #### 📌 Rencana Eksekusi (Simulasi):
        - Ukuran Posisi: **{trade_size:.6f} BTC**
        - Stop Loss: `${stop_loss:.2f}`
        - Take Profit: `${take_profit:.2f}`
        """)
    else:
        st.warning("❌ Spread terlalu kecil. Belum ada peluang arbitrase.")

else:
    st.error("Gagal menganalisis spread. Periksa koneksi atau API.")

# === Info Manajemen Risiko ===
with st.expander("⚙️ Pengaturan Manajemen Risiko"):
    st.write(f"- Maksimum Risiko per Trade: **${MAX_RISK_PER_TRADE_USD}**")
    st.write(f"- Spread Minimum: **${MIN_SPREAD_USD}**")
    st.write(f"- Stop Loss: **{STOP_LOSS_PERCENT}%**")
    st.write(f"- Take Profit: **{TAKE_PROFIT_PERCENT}%**")

st.caption("Built with ❤️ using Streamlit & CCXT | v0.1")

