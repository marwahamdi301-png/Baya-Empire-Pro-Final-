import streamlit as st
import plotly.express as px
from src.ui import setup_style, page_header

setup_style()
page_header("اقتصاد عملة $BAYA", "توزيع السيولة والرؤية المالية")

# بيانات توزيع العملة
df = {
    "القطاع": ["السيولة", "الفريق", "التسويق", "الأثر الأفريقي"],
    "النسبة": [50, 15, 15, 20]
}
fig = px.pie(df, values='النسبة', names='القطاع', hole=0.5,
             color_discrete_sequence=['#00f2ff', '#00ff88', '#ff0055', '#ffaa00'])

st.plotly_chart(fig, use_container_width=True)

st.success("💎 السعر المبدئي للإطلاق: $0.01")
