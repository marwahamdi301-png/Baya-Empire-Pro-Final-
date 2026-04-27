import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.markdown("<h1>⚡ مركز التداول</h1>", unsafe_allow_html=True)

if 'portfolio' not in st.session_state:
    st.session_state.portfolio = {
        'balance_usdt': 10000.0,
        'holdings': {'BTC': 0.12, 'ETH': 2.5, 'SOL': 45.0}
    }

@st.cache_data(ttl=25)
def get_candles(symbol, interval="1h", limit=150):
    try:
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
        data = requests.get(url, timeout=10).json()
        df = pd.DataFrame(data, columns=['time','o','h','l','c','v', '_','_','_','_','_','_'])
        df['time'] = pd.to_datetime(df['time'], unit='ms')
        for col in ['o','h','l','c','v']: df[col] = pd.to_numeric(df[col])
        return df
    except: return None

def calculate_indicators(df):
    if df is None: return df
    df['SMA20'] = df['c'].rolling(20).mean()
    df['SMA50'] = df['c'].rolling(50).mean()
    df['RSI'] = 100 - (100 / (1 + (df['c'].diff().where(lambda x: x>0, 0).rolling(14).mean() / 
                                 abs(df['c'].diff().where(lambda x: x<0, 0).rolling(14).mean()))))
    return df

with st.sidebar:
    symbol = st.selectbox("زوج التداول", ["BTCUSDT", "ETHUSDT", "SOLUSDT"])
    interval = st.selectbox("الإطار الزمني", ["15m", "1h", "4h", "1d"])
    show_rsi = st.checkbox("إظهار RSI", value=True)

df = get_candles(symbol, interval)
df = calculate_indicators(df)

if df is not None:
    fig = make_subplots(rows=2 if show_rsi else 1, cols=1, shared_xaxes=True, row_heights=[0.75, 0.25] if show_rsi else [1])
    
    fig.add_trace(go.Candlestick(x=df['time'], open=df['o'], high=df['h'], low=df['l'], close=df['c'],
                                 increasing_line_color='#00f2ff', decreasing_line_color='#ff00aa'), row=1, col=1)
    
    fig.add_trace(go.Scatter(x=df['time'], y=df['SMA20'], name="SMA 20", line=dict(color="#ffff00")), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['time'], y=df['SMA50'], name="SMA 50", line=dict(color="#ff00ff")), row=1, col=1)
    
    if show_rsi and 'RSI' in df.columns:
        fig.add_trace(go.Scatter(x=df['time'], y=df['RSI'], name="RSI", line=dict(color="#00f2ff")), row=2, col=1)
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
    
    fig.update_layout(template='plotly_dark', height=650, xaxis_rangeslider_visible=False, title=f"{symbol} - التحليل الفني")
    st.plotly_chart(fig, use_container_width=True)

    # منطقة التنفيذ
    col1, col2 = st.columns([1,2])
    with col1:
        side = st.radio("نوع الأمر", ["BUY 🟢", "SELL 🔴"])
        amount = st.number_input("الكمية", min_value=0.001, value=0.05)
        if st.button("🚀 تنفيذ الصفقة", type="primary"):
            coin = symbol.replace("USDT", "")
            price = df['c'].iloc[-1]
            cost = amount * price
            p = st.session_state.portfolio
            if side == "BUY 🟢" and p['balance_usdt'] >= cost:
                p['balance_usdt'] -= cost
                p['holdings'][coin] = p['holdings'].get(coin, 0) + amount
                st.success(f"✅ تم شراء {amount} {coin}")
            elif side == "SELL 🔴" and p['holdings'].get(coin, 0) >= amount:
                p['holdings'][coin] -= amount
                p['balance_usdt'] += cost
                st.success(f"✅ تم بيع {amount} {coin}")
            else:
                st.error("رصيد غير كافي")
