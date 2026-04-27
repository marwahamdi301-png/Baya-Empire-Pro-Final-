import streamlit as st
import requests
import pandas as pd

st.markdown("<h1>📊 لوحة القيادة الإمبراطورية</h1>", unsafe_allow_html=True)

@st.cache_data(ttl=30)
def get_price(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
        data = requests.get(url, timeout=8).json()
        return float(data['lastPrice']), float(data['priceChangePercent'])
    except:
        return None, None

coins = {"BTCUSDT": "Bitcoin", "ETHUSDT": "Ethereum", "SOLUSDT": "Solana", "XRPUSDT": "Ripple"}

cols = st.columns(4)
for i, (symbol, name) in enumerate(coins.items()):
    price, change = get_price(symbol)
    with cols[i]:
        color = "#00ff9d" if change and change >= 0 else "#ff3b5c"
        st.metric(label=name, value=f"${price:,.2f}" if price else "—", 
                  delta=f"{change:.2f}%" if change else None, delta_color="normal")

st.markdown("---")
st.markdown("**رؤيتنا**: كل صفقة ناجحة تساهم في تمويل مشاريع تعليمية ومائية وطاقة شمسية في دول أفريقية.")
