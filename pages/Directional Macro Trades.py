import streamlit as st
import plotly.graph_objs as go
import pandas as pd
import pandas_datareader.data as web
import datetime
import yfinance as yf
import random

# --- Fetch macro data ---
start = datetime.datetime(2020, 1, 1)
end = datetime.datetime.today()

symbols = {
    'CPI': 'CPIAUCSL',
    'PPI': 'PPIACO',
    'NFP': 'PAYEMS',
    'FED': 'FEDFUNDS'
}

macro_data = {}
for label, symbol in symbols.items():
    macro_data[label] = web.DataReader(symbol, 'fred', start, end)

# CPI YoY
macro_data['CPI']['YoY'] = macro_data['CPI']['CPIAUCSL'].pct_change(12) * 100
macro_data['PPI']['YoY'] = macro_data['PPI']['PPIACO'].pct_change(12) * 100

# --- Fetch BTC & ALTCOIN Prices ---
tokens = {
    "BTC": "BTC-USD",
    "ETH": "ETH-USD",
    "SOL": "SOL-USD",
    "ARB": "ARB-USD",
    "APT": "APT-USD",
    "OP": "OP-USD",
    "AVAX": "AVAX-USD"
}

prices = {}
for token, ticker in tokens.items():
    try:
        prices[token] = yf.Ticker(ticker).history(period="1y")
    except:
        prices[token] = pd.DataFrame()

# --- Streamlit UI ---
st.set_page_config(layout="wide")
st.title("📊 Makro + On-Chain + Crypto Strategy Dashboard")

st.header("Macro Economic Indicators")
fig_macro = go.Figure()
fig_macro.add_trace(go.Scatter(x=macro_data['CPI'].index, y=macro_data['CPI']['YoY'], name='CPI YoY'))
fig_macro.add_trace(go.Scatter(x=macro_data['PPI'].index, y=macro_data['PPI']['YoY'], name='PPI YoY'))
fig_macro.add_trace(go.Scatter(x=macro_data['NFP'].index, y=macro_data['NFP']['PAYEMS'], name='NFP'))
fig_macro.update_layout(title='📈 CPI / PPI / NFP Trend')
st.plotly_chart(fig_macro, use_container_width=True)

st.header("Crypto Market Overview")
fig_crypto = go.Figure()
for token, df in prices.items():
    if not df.empty:
        fig_crypto.add_trace(go.Scatter(x=df.index, y=df['Close'], name=token))
fig_crypto.update_layout(title='📉 Token Prices (BTC, ETH, SOL, ARB, APT, OP, AVAX)')
st.plotly_chart(fig_crypto, use_container_width=True)

st.header("🐋 Simulated Whale Inflow/Outflow (Mock Data)")
dates = pd.date_range(end=datetime.datetime.today(), periods=30)
whale_data = pd.DataFrame({
    'Date': dates,
    'Inflow': [random.randint(500, 1500) for _ in range(30)],
    'Outflow': [random.randint(500, 1500) for _ in range(30)]
})

fig_whale = go.Figure()
fig_whale.add_trace(go.Bar(x=whale_data['Date'], y=whale_data['Inflow'], name='Exchange Inflow'))
fig_whale.add_trace(go.Bar(x=whale_data['Date'], y=whale_data['Outflow'], name='Exchange Outflow'))
fig_whale.update_layout(barmode='group', title='🐳 Whale Activity (Simulated ETH/BTC Movements)')
st.plotly_chart(fig_whale, use_container_width=True)

st.header("🧠 Strategy Signal")
cpi_latest = macro_data['CPI']['YoY'].dropna().iloc[-1]
nfp_latest = macro_data['NFP']['PAYEMS'].dropna().iloc[-1]
fed_bias = "Hawkish" if cpi_latest > 3.0 and nfp_latest > 200000 else "Dovish"
whale_diff = whale_data['Inflow'].iloc[-1] - whale_data['Outflow'].iloc[-1]

if fed_bias == "Hawkish":
    strategy = "🔥 Suggested Trade: SHORT BTC & Altcoins"
    color = "#61adff"
else:
    strategy = "🚀 Suggested Trade: LONG BTC & Altcoins"
    color = "#db7b21"

st.markdown(f"""
<div style='background-color: {color}; padding: 20px; border-radius: 10px; font-size: 20px; text-align: center;'>
{strategy}
</div>
""", unsafe_allow_html=True)

# Combined logic
if cpi_latest > 3.0 and nfp_latest > 200000 and whale_diff > 200:
    strategy = "🔥 Trade Signal: SHORT (Bearish Macro & Whale Inflow)"
    color = "#db7b21"
elif cpi_latest < 3.0 and nfp_latest < 200000 and whale_diff < -200:
    strategy = "🚀 Trade Signal: LONG (Bullish Macro & Whale Outflow)"
    color = "#61adff"
else:
    strategy = "⏸️ Trade Signal: WAIT (No Clear Macro/Whale Bias)"
    color = "#75828f"

st.markdown(f"""
<div style='background-color: {color}; padding: 20px; border-radius: 10px; font-size: 20px; text-align: center;'>
{strategy}
</div>
""", unsafe_allow_html=True)
