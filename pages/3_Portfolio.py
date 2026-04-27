import streamlit as st
import pandas as pd

st.markdown("<h1>💼 المحفظة الافتراضية</h1>", unsafe_allow_html=True)

if 'portfolio' not in st.session_state:
    st.session_state.portfolio = {'balance_usdt': 10000.0, 'holdings': {'BTC': 0.12, 'ETH': 2.5, 'SOL': 45.0}}

p = st.session_state.portfolio

st.metric("الرصيد النقدي", f"${p['balance_usdt']:,.2f}")

st.subheader("الأصول المملوكة")
data = []
for coin, qty in p['holdings'].items():
    price = 78000 if coin == "BTC" else 2330 if coin == "ETH" else 86
    value = qty * price
    data.append({"العملة": coin, "الكمية": qty, "السعر الحالي": f"${price:,.2f}", "القيمة": f"${value:,.2f}"})

st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)

st.caption("💡 كل صفقة تنفذها في صفحة التداول تؤثر مباشرة على محفظتك")
