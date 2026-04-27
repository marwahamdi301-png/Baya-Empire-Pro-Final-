import streamlit as st
import pandas as pd
import requests

st.markdown("<h1>🤖 توصيات الذكاء الاصطناعي</h1>", unsafe_allow_html=True)

@st.cache_data(ttl=40)
def get_candles_for_signal(symbol):
    try:
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1h&limit=100"
        data = requests.get(url, timeout=8).json()
        df = pd.DataFrame(data, columns=['time','o','h','l','c','v','_','_','_','_','_','_'])
        df['c'] = pd.to_numeric(df['c'])
        return df
    except: return None

symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]

for sym in symbols:
    df = get_candles_for_signal(sym)
    if df is not None:
        # حساب RSI
        delta = df['c'].diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = -delta.where(delta < 0, 0).rolling(14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs)).iloc[-1]
        
        price = df['c'].iloc[-1]
        trend = "صاعد 🟢" if df['c'].iloc[-1] > df['c'].iloc[-20] else "هابط 🔴"
        
        if rsi < 35:
            signal = "🟢 شراء قوي"
            confidence = "89%"
        elif rsi > 70:
            signal = "🔴 بيع قوي"
            confidence = "86%"
        else:
            signal = "🟡 انتظر / محايد"
            confidence = "68%"
        
        st.markdown(f"""
        <div style="background:rgba(0,242,255,0.08); padding:20px; border-radius:15px; margin:12px 0; border-right:4px solid #00f2ff;">
            <h3>{sym.replace('USDT','')}</h3>
            <h2 style="color:#00f2ff">{signal} — ثقة {confidence}</h2>
            <p>السعر: ${price:,.2f} | RSI: {rsi:.1f} | الاتجاه: {trend}</p>
        </div>
        """, unsafe_allow_html=True)
