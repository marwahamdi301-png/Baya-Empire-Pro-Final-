import streamlit as st
from src.ui import setup_style, page_header

setup_style()
page_header("محفظتي الرقمية", "إدارة الأصول والاستثمارات الخاصة")

col1, col2, col3 = st.columns(3)
col1.metric("إجمالي الرصيد", "$12,450", "+12%")
col2.metric("رصيد $BAYA", "500,000", "جديد")
col3.metric("الأرباح المحققة", "$1,200", "+5%")

st.write("### 📜 سجل العمليات الأخير")
st.code("""
- شراء 100,000 $BAYA (ناجح)
- تحويل 0.5 BTC (قيد المعالجة)
""")
