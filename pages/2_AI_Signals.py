import streamlit as st
from src.ui import setup_style, page_header

setup_style()
page_header("مركز إشارات الذكاء الاصطناعي", "تحليل السوق عبر خوارزميات بايا")

col1, col2 = st.columns(2)

with col1:
    st.metric(label="دقة التوقعات الحالية", value="94.2%", delta="1.5%")
    st.write("🤖 **توصية النظام:** تجميع هادئ لعملة $BAYA")

with col2:
    st.warning("⚠️ إشارة تنبيه: تقلبات قادمة في زوج BTC/USDT")

st.markdown("""
### 🧠 التحليل الفني الذكي
- **RSI:** تشبع بيعي (فرصة شراء).
- **Moving Averages:** اتجاه صعودي على المدى المتوسط.
""")
